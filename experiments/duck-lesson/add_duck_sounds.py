#!/usr/bin/env python3
"""Add duck sounds to duck_lesson.mp4 at precise quack moments.

Strategy:
- Voice was rendered WITHOUT quack phrases → no voice quacking
- Duck sounds go right after the "And—" / "Hello!" / "Got anything to eat?" phrases
- We extract audio from the rendered MP4 (correct volume), overlay duck sounds, mux back
"""

import json
import subprocess
import sys
from pathlib import Path

TIMELINE   = Path("/Users/panda/Development/private/wooden-roll/output/audio/duck_lesson/timeline.json")
INPUT_MP4  = Path("/Users/panda/Development/private/youtube-study-shorts/output/videos/duck_lesson.mp4")
OUTPUT_MP4 = Path("/Users/panda/Development/private/youtube-study-shorts/output/videos/duck_lesson_final.mp4")
DUCK_MP3   = Path("/Users/panda/Development/private/youtube-study-shorts/music/duck-quacking.mp3")
SCRATCH    = Path("/private/tmp/duck-lesson")

DUCK_TRIM     = 0.5   # seconds of quack to use
DUCK_VOL      = 1.1
QUACK_SPACING = 0.38

# Duck positions measured via ffmpeg silencedetect -35dB on actual WAV (phraseGap=0.6):
#
#   Phrase 2 "Focus. Take a deep breath. And—": speech ends at 5.784s
#   Phrase 3 "Again. Fill your lungs. And—": speech ends at 8.539s
#   "Hello!": Premiss adds leading silence; actual speech is at 23.459-23.974s
#             (NOT at the phrase 7 window 22.892-23.428!)
#   "Got anything to eat?": actual speech at 25.124-25.949s
#             Natural silence: 25.949-26.885s (0.937s) — room for 2 ducks
#
# All gaps exist naturally; no WAV surgery needed.

CUE_SPECS = [
    (5.834, 1),    # after "And—" #1 speech ends (5.784 + 0.05 buffer)
    (8.589, 1),    # after "And—" #2 speech ends (8.539 + 0.05 buffer)
    (24.024, 1),   # after "Hello!" speech ends (23.974 + 0.05 buffer)
    (25.999, 2),   # after "Got food?" speech ends (25.949 + 0.05 buffer), 2 ducks
]

cues_ms: list[int] = []
for t_start, count in CUE_SPECS:
    for i in range(count):
        cues_ms.append(int((t_start + i * QUACK_SPACING) * 1000))

print(f"Duck cues ({len(cues_ms)} sounds):")
for ms in cues_ms:
    print(f"  {ms}ms = {ms/1000:.3f}s")

# ── Step 1: extract audio from rendered MP4 (correct voiceVolume already applied)
extracted_aac = SCRATCH / "voice_extracted.aac"
subprocess.run(
    ["ffmpeg", "-y", "-i", str(INPUT_MP4), "-vn", "-c:a", "copy", str(extracted_aac)],
    check=True, capture_output=True,
)

# ── Step 2: build ffmpeg filter to overlay duck sounds
duck_inputs = []
for _ in cues_ms:
    duck_inputs += ["-i", str(DUCK_MP3)]

n_duck = len(cues_ms)
filter_parts = []
duck_labels = []

for i, delay_ms in enumerate(cues_ms):
    idx = 1 + i   # input 0 = extracted voice aac
    label = f"d{i}"
    filter_parts.append(
        f"[{idx}:a]"
        f"atrim=0:{DUCK_TRIM},"
        f"aformat=sample_fmts=fltp:sample_rates=44100:channel_layouts=stereo,"
        f"adelay={delay_ms}:all=1,"
        f"volume={DUCK_VOL}"
        f"[{label}]"
    )
    duck_labels.append(f"[{label}]")

all_inputs = "[0:a]" + "".join(duck_labels)
filter_parts.append(
    f"{all_inputs}amix=inputs={1 + n_duck}:normalize=0:dropout_transition=0[a_out]"
)

mixed_wav = SCRATCH / "duck_mixed.wav"
cmd_mix = [
    "ffmpeg", "-y",
    "-i", str(extracted_aac),
    *duck_inputs,
    "-filter_complex", ";".join(filter_parts),
    "-map", "[a_out]",
    str(mixed_wav),
]

print("\nMixing audio…")
r = subprocess.run(cmd_mix, capture_output=True, text=True)
if r.returncode != 0:
    print(r.stderr[-3000:])
    sys.exit("Audio mix failed")

# ── Step 3: mux mixed audio back with video
cmd_mux = [
    "ffmpeg", "-y",
    "-i", str(INPUT_MP4),
    "-i", str(mixed_wav),
    "-c:v", "copy",
    "-c:a", "aac", "-b:a", "128k",
    "-map", "0:v", "-map", "1:a",
    str(OUTPUT_MP4),
]

print("Muxing…")
r = subprocess.run(cmd_mux, capture_output=True, text=True)
if r.returncode != 0:
    print(r.stderr[-2000:])
    sys.exit("Mux failed")

print(f"\n✅ Done: {OUTPUT_MP4}")
