#!/usr/bin/env python3
"""
animal_044 v3 — each clip loops to fill its own timeline entry duration.
Clips from clips_v2/, elder TTS, music at 15%.
"""
import json, subprocess, shutil
from pathlib import Path

CLIPS_DIR = Path("experiments/text-to-video/clips_v2")
OUT_DIR   = Path("experiments/text-to-video")
AUDIO     = OUT_DIR / "animal_044_voice_elder.wav"
TIMELINE  = OUT_DIR / "animal_044_timeline.json"
PARABLE   = Path("formats/parable-animal/drafts/parables_20260831_120000.json")
TMP       = OUT_DIR / "tmp_v3"
TMP.mkdir(exist_ok=True)

timeline = json.load(open(TIMELINE))
parable  = json.load(open(PARABLE))[0]
screens  = parable["screens"]

result = subprocess.run(
    ["ffprobe", "-v", "error", "-show_entries", "format=duration",
     "-of", "default=noprint_wrappers=1:nokey=1", str(AUDIO)],
    capture_output=True, text=True)
audio_duration = float(result.stdout.strip())
hook_duration  = 3.0
tail_duration  = 2.0
total_duration = hook_duration + audio_duration + tail_duration
print(f"Audio: {audio_duration:.1f}s  total: {total_duration:.1f}s")

# Map: clip index → clip file (clips are 1-indexed s01..s13)
CLIP_FILES = [CLIPS_DIR / f"clip_s{i:02d}_{n}.mp4" for i, n in enumerate([
    "intro","book","pullscroll","scrollflat","pigeonfly",
    "twobirds","owlglide","owlscroll","pigeontalk",
    "groupbirds","owlalone","tuckscroll","owlstep"
], start=1)]

# Build one segment per timeline entry:
# segment covers [entry.start, next_entry.start) or [entry.start, audio_end) for last
segments = []
for i, entry in enumerate(timeline):
    t_start = entry["startSeconds"]
    t_end = timeline[i+1]["startSeconds"] if i+1 < len(timeline) else audio_duration
    seg_dur = t_end - t_start
    clip = CLIP_FILES[i % len(CLIP_FILES)]
    seg_out = TMP / f"seg_{i:02d}.mp4"
    # Loop clip to fill seg_dur
    loops = int(seg_dur / 4) + 2
    concat_txt = TMP / f"concat_{i:02d}.txt"
    with open(concat_txt, "w") as f:
        for _ in range(loops):
            f.write(f"file '{clip.resolve()}'\n")
    subprocess.run([
        "ffmpeg", "-y",
        "-f", "concat", "-safe", "0", "-i", str(concat_txt),
        "-t", str(seg_dur),
        "-vf", "scale=704:1280:force_original_aspect_ratio=increase,crop=704:1280",
        "-c:v", "libx264", "-preset", "fast", "-crf", "22",
        "-r", "24", "-an", str(seg_out)
    ], check=True, capture_output=True)
    print(f"  seg_{i:02d}  {clip.name[:20]:20s}  {seg_dur:.1f}s", flush=True)
    segments.append(seg_out)

# Hook segment (3s) — use clip_s01
hook_seg = TMP / "seg_hook.mp4"
subprocess.run([
    "ffmpeg", "-y", "-stream_loop", "-1",
    "-i", str(CLIP_FILES[0]),
    "-t", str(hook_duration),
    "-vf", "scale=704:1280:force_original_aspect_ratio=increase,crop=704:1280",
    "-c:v", "libx264", "-preset", "fast", "-crf", "22",
    "-r", "24", "-an", str(hook_seg)
], check=True, capture_output=True)
print(f"  hook  {hook_duration}s")

# Tail segment (2s) — use last clip
tail_seg = TMP / "seg_tail.mp4"
subprocess.run([
    "ffmpeg", "-y", "-stream_loop", "-1",
    "-i", str(CLIP_FILES[-1]),
    "-t", str(tail_duration),
    "-vf", "scale=704:1280:force_original_aspect_ratio=increase,crop=704:1280",
    "-c:v", "libx264", "-preset", "fast", "-crf", "22",
    "-r", "24", "-an", str(tail_seg)
], check=True, capture_output=True)

# Concat all segments
all_segs = [hook_seg] + segments + [tail_seg]
final_concat = TMP / "final_concat.txt"
with open(final_concat, "w") as f:
    for s in all_segs:
        f.write(f"file '{s.resolve()}'\n")

raw_video = TMP / "raw_v3.mp4"
subprocess.run([
    "ffmpeg", "-y",
    "-f", "concat", "-safe", "0", "-i", str(final_concat),
    "-c:v", "libx264", "-preset", "fast", "-crf", "22",
    "-r", "24", "-an", str(raw_video)
], check=True, capture_output=True)
print(f"Raw video ready: {raw_video.stat().st_size//1024//1024}MB")

# Text overlays
font_path = "/System/Library/Fonts/Helvetica.ttc"

def escape(text):
    return (text.replace("\\","\\\\").replace("'","'")
            .replace(":","\\:").replace(",","\\,")
            .replace("[","\\[").replace("]","\\]"))

def wrap(text, max_chars=36):
    words = text.split()
    lines, cur = [], []
    for w in words:
        if cur and sum(len(x) for x in cur) + len(cur) + len(w) > max_chars:
            lines.append(" ".join(cur)); cur = [w]
        else:
            cur.append(w)
    if cur: lines.append(" ".join(cur))
    return lines

drawtext_filters = []

# Hook
hook_lines = screens[0]["text"].split("\n")
n = len(hook_lines)
for li, line in enumerate(hook_lines):
    y_off = li * 85 - (n - 1) * 42
    drawtext_filters.append(
        f"drawtext=fontfile={font_path}:text='{escape(line)}':"
        f"fontsize=64:fontcolor=white:x=(w-text_w)/2:y=(h/2+{y_off}):"
        f"enable='between(t,0,{hook_duration})':"
        f"shadowcolor=black:shadowx=3:shadowy=3"
    )

# Story screens from timeline
for entry in timeline:
    t_start = hook_duration + entry["startSeconds"]
    t_end   = hook_duration + entry["endSeconds"]
    all_lines = []
    for rl in entry["phrase"].split("\n"):
        all_lines.extend(wrap(rl, 34))
    for li, line in enumerate(all_lines):
        y = f"h*0.70+{li*58}"
        drawtext_filters.append(
            f"drawtext=fontfile={font_path}:text='{escape(line)}':"
            f"fontsize=42:fontcolor=white:x=(w-text_w)/2:y={y}:"
            f"enable='between(t,{t_start:.2f},{t_end:.2f})':"
            f"shadowcolor=black:shadowx=2:shadowy=2"
        )

vf = ",".join(drawtext_filters)

music_files = list(Path("music/calm").glob("*.mp3"))
music_path  = music_files[0] if music_files else None

out_path = OUT_DIR / "animal_044_v3.mp4"
print("Assembling final…", flush=True)

if music_path:
    cmd = [
        "ffmpeg", "-y",
        "-i", str(raw_video),
        "-i", str(AUDIO),
        "-stream_loop", "-1", "-i", str(music_path),
        "-filter_complex",
        f"[0:v]{vf}[v];"
        f"[2:a]volume=0.15[music];"
        f"[1:a][music]amix=inputs=2:duration=first[a]",
        "-map", "[v]", "-map", "[a]",
        "-t", str(total_duration),
        "-c:v", "libx264", "-preset", "fast", "-crf", "26",
        "-c:a", "aac", "-b:a", "128k",
        str(out_path)
    ]
else:
    cmd = [
        "ffmpeg", "-y",
        "-i", str(raw_video), "-i", str(AUDIO),
        "-filter_complex", f"[0:v]{vf}[v]",
        "-map", "[v]", "-map", "1:a",
        "-t", str(total_duration),
        "-c:v", "libx264", "-preset", "fast", "-crf", "26",
        "-c:a", "aac", "-b:a", "128k",
        str(out_path)
    ]

subprocess.run(cmd, check=True, capture_output=True)
print(f"\n✅ {out_path.name}  {out_path.stat().st_size//1024//1024}MB  {total_duration:.0f}s")

shutil.rmtree(TMP)
print("Temp cleaned.")
