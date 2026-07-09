#!/usr/bin/env python3
"""One-off: Duck Language Lesson YouTube Short.

No voiceover. Duck quacking as audio. Subtitles at bottom.
Background: Pexels duck images (portrait).
"""

import os
import json
import subprocess
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

load_dotenv()

ROOT = Path(__file__).resolve().parent
DUCK_SOUND = ROOT / "music" / "duck-quacking.mp3"
OUTPUT_VIDEO = ROOT / "output" / "videos" / "duck_lesson.mp4"
SCRATCH = Path("/private/tmp/duck-lesson")
SCRATCH.mkdir(parents=True, exist_ok=True)

# (text, duration_seconds)
SCREENS = [
    ("Today, ducklings,\nwe will learn to quack.", 3.5),
    ("Focus.\nTake a deep breath.", 2.0),
    ("And…", 1.5),
    ("QUACK!", 2.5),
    ("Again. All together.\nFocus. Fill your lungs. And…", 3.0),
    ("QUACK!! QUACK!!", 2.5),
    ("Excellent.", 1.5),
    ("Now — basic phrases:", 1.5),
    ("Hello — quack!\nHow are you — quaack?\nNice weather — quaaack!", 4.0),
    ("Got anything to eat —\nquack quack quack!", 3.0),
    ("Let's practice. All together!", 1.5),
    ("Hello! — quack! Quaack?", 3.0),
    ("Excellent!", 1.5),
    ("Got food? And together —\nQUACK QUACK QUACK!", 3.0),
    ("Outstanding.", 1.5),
    ("Homework: say Hello 30 times.\nGot food? 40 times.\nTest tomorrow.", 4.0),
    ("Class dismissed.", 2.0),
    ("Dear viewer:\nYou now know basic Quackish.\nTry it with a real duck.", 4.0),
    ("Didn't make you laugh?\nDrop a comment.\nFollow for more @StudyGoTogether", 3.5),
]

TOTAL_DURATION = sum(d for _, d in SCREENS)

PEXELS_QUERIES = [
    "duck pond water nature",
    "duck group flock water",
    "duckling cute nature",
    "duck classroom illustration",
    "duck bird outdoor",
]


def fetch_pexels_images(n: int = 5) -> list[str]:
    api_key = os.environ["PEXELS_API_KEY"]
    images = []
    used_ids: set[int] = set()

    for q in PEXELS_QUERIES:
        if len(images) >= n:
            break
        resp = requests.get(
            "https://api.pexels.com/v1/search",
            headers={"Authorization": api_key},
            params={"query": q, "per_page": 5, "orientation": "portrait"},
            timeout=10,
        )
        for photo in resp.json().get("photos", []):
            if photo["id"] not in used_ids and len(images) < n:
                url = photo["src"]["large2x"]
                path = SCRATCH / f"duck_{photo['id']}.jpg"
                if not path.exists():
                    data = requests.get(url, timeout=15).content
                    path.write_bytes(data)
                print(f"  [{q}] -> photo {photo['id']}")
                images.append(str(path))
                used_ids.add(photo["id"])

    if not images:
        sys.exit("No images fetched from Pexels")
    return images


def generate_ass() -> str:
    def ts(secs: float) -> str:
        h = int(secs // 3600)
        m = int((secs % 3600) // 60)
        s = secs % 60
        cs = int(round((s - int(s)) * 100))
        return f"{h}:{m:02d}:{int(s):02d}.{cs:02d}"

    lines = [
        "[Script Info]",
        "ScriptType: v4.00+",
        "PlayResX: 1080",
        "PlayResY: 1920",
        "WrapStyle: 0",
        "",
        "[V4+ Styles]",
        "Format: Name, Fontname, Fontsize, PrimaryColour, SecondaryColour, OutlineColour, BackColour, Bold, Italic, Underline, StrikeOut, ScaleX, ScaleY, Spacing, Angle, BorderStyle, Outline, Shadow, Alignment, MarginL, MarginR, MarginV, Encoding",
        # Regular: bottom-center, white, 3px black outline
        "Style: Sub,Arial,60,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,1,0,0,0,100,100,0,0,1,3,1,2,60,60,100,1",
        # Big: centered (alignment 5), large for QUACK moments
        "Style: Big,Arial,110,&H00FFFFFF,&H000000FF,&H00000000,&H00000000,-1,0,0,0,100,100,0,0,1,5,2,5,60,60,80,1",
        "",
        "[Events]",
        "Format: Layer, Start, End, Style, Name, MarginL, MarginR, MarginV, Effect, Text",
    ]

    t = 0.0
    for text, dur in SCREENS:
        start = ts(t)
        end = ts(t + dur - 0.05)
        ass_text = text.replace("\n", "\\N")
        is_big = text.strip().upper().startswith("QUACK") and len(text) < 25
        style = "Big" if is_big else "Sub"
        lines.append(f"Dialogue: 0,{start},{end},{style},,0,0,0,,{ass_text}")
        t += dur

    path = SCRATCH / "duck_lesson.ass"
    path.write_text("\n".join(lines), encoding="utf-8")
    return str(path)


def render(images: list[str], ass_path: str):
    n = len(images)
    dur_per_img = TOTAL_DURATION / n
    xfade_dur = 0.5
    fade_offset = dur_per_img - xfade_dur  # per-image offset step

    # Build input args: images + duck audio (stream-looped)
    input_args = []
    for img in images:
        input_args += ["-loop", "1", "-t", str(dur_per_img + 2), "-i", img]
    # Duck audio looped — input index n
    input_args += ["-stream_loop", "-1", "-t", str(TOTAL_DURATION + 2), "-i", str(DUCK_SOUND)]
    audio_idx = n

    filters = []

    # Scale each image to 1080x1920, black padding, 25fps
    for i in range(n):
        filters.append(
            f"[{i}:v]scale=1080:1920:force_original_aspect_ratio=decrease,"
            f"pad=1080:1920:(ow-iw)/2:(oh-ih)/2:color=black,"
            f"setsar=1,fps=25[v{i}]"
        )

    # Crossfade chain
    if n == 1:
        filters.append("[v0]copy[vid_bg]")
    else:
        filters.append(
            f"[v0][v1]xfade=transition=fade:duration={xfade_dur}:offset={fade_offset:.3f}[xv1]"
        )
        for i in range(2, n):
            offset = i * fade_offset
            prev = f"xv{i - 1}"
            out = f"xv{i}"
            filters.append(
                f"[{prev}][v{i}]xfade=transition=fade:duration={xfade_dur}:offset={offset:.3f}[{out}]"
            )
        filters.append(f"[xv{n - 1}]copy[vid_bg]")

    # Overlay ASS subtitles — escape colons in path (none here, but safe)
    ass_escaped = ass_path.replace("\\", "/")
    filters.append(f"[vid_bg]ass={ass_escaped}[vid_out]")

    # Audio: trim duck loop to exact duration
    filters.append(
        f"[{audio_idx}:a]atrim=duration={TOTAL_DURATION:.3f},"
        f"aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo[a_out]"
    )

    filter_complex = ";".join(filters)

    cmd = [
        "ffmpeg", "-y",
        *input_args,
        "-filter_complex", filter_complex,
        "-map", "[vid_out]",
        "-map", "[a_out]",
        "-t", f"{TOTAL_DURATION:.3f}",
        "-c:v", "h264_videotoolbox",
        "-b:v", "6000k",
        "-c:a", "aac", "-b:a", "128k",
        str(OUTPUT_VIDEO),
    ]

    print(f"\nRendering {TOTAL_DURATION:.1f}s video…")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr[-4000:])
        sys.exit("Render failed")
    print(f"\n✅ Done: {OUTPUT_VIDEO}")


if __name__ == "__main__":
    print(f"Total duration: {TOTAL_DURATION:.1f}s  ({len(SCREENS)} screens)")

    print("\n1. Fetching Pexels images…")
    images = fetch_pexels_images(n=5)
    print(f"   {len(images)} images ready")

    print("\n2. Generating ASS subtitles…")
    ass_path = generate_ass()
    print(f"   {ass_path}")

    print("\n3. Rendering…")
    render(images, ass_path)
