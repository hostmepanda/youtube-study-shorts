#!/usr/bin/env python3
"""
Generate background music tracks using MusicGen (small) via mlx-examples.

Setup (one time):
    git clone https://github.com/ml-explore/mlx-examples ../mlx-examples
    pip install -r ../mlx-examples/musicgen/requirements.txt

Usage:
    python scripts/generate_music.py --mood motivational
    python scripts/generate_music.py --mood calm --count 5
    python scripts/generate_music.py --mood uplifting --force
"""

import argparse
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ROOT = Path(__file__).parent.parent
MUSIC_DIR = ROOT / "music"
MLX_MUSICGEN = ROOT.parent / "mlx-examples" / "musicgen" / "generate.py"

MOOD_PROMPTS = {
    "motivational": [
        "uplifting motivational background music, driving beat, inspiring, 90bpm, no vocals",
        "energetic positive background track, piano and strings, hopeful, 85bpm, no vocals",
        "motivational cinematic background, building energy, triumphant, no vocals",
    ],
    "calm": [
        "calm relaxing ambient background music, soft piano, peaceful, slow, no vocals",
        "gentle lo-fi background, soft pads, meditative, 60bpm, no vocals",
        "soothing acoustic background, warm, minimal, no vocals",
    ],
    "uplifting": [
        "cheerful uplifting background music, bright, positive, acoustic guitar, no vocals",
        "happy light background track, playful melody, optimistic, 80bpm, no vocals",
        "warm uplifting instrumental, feel-good, gentle rhythm, no vocals",
    ],
}

DURATION = 28  # seconds — stays within MusicGen's native 30s limit


def check_setup():
    if not MLX_MUSICGEN.exists():
        print("MusicGen not found. Run:")
        print(f"  git clone https://github.com/ml-explore/mlx-examples {ROOT.parent / 'mlx-examples'}")
        print(f"  pip install -r {ROOT.parent / 'mlx-examples' / 'musicgen' / 'requirements.txt'}")
        sys.exit(1)


def generate_track(prompt: str, output_path: Path) -> bool:
    if output_path.exists():
        print(f"  [skip] {output_path.name} already exists")
        return True

    print(f"  [gen] {output_path.name} (~{DURATION}s, takes 3-4 min on M1)...")
    result = subprocess.run(
        [
            sys.executable,
            str(MLX_MUSICGEN),
            "--model", "facebook/musicgen-small",
            "--text", prompt,
            "--max-steps", str(DURATION * 50),  # ~50 steps per second
            "--output-path", str(output_path),
        ],
        capture_output=True,
        text=True,
        cwd=str(MLX_MUSICGEN.parent),
    )

    if result.returncode != 0:
        print(f"  [err] {result.stderr.strip()}")
        return False

    print(f"  [ok] {output_path.name}")
    return True


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mood", required=True, choices=list(MOOD_PROMPTS.keys()))
    parser.add_argument("--count", type=int, default=3, help="Number of tracks to generate")
    parser.add_argument("--force", action="store_true", help="Regenerate existing tracks")
    args = parser.parse_args()

    check_setup()

    dest_dir = MUSIC_DIR / args.mood
    dest_dir.mkdir(parents=True, exist_ok=True)

    prompts = MOOD_PROMPTS[args.mood]
    generated = 0

    for i in range(args.count):
        prompt = prompts[i % len(prompts)]
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_path = dest_dir / f"musicgen_{args.mood}_{timestamp}_{i+1}.wav"

        if args.force and output_path.exists():
            output_path.unlink()

        print(f"\n[{i+1}/{args.count}] mood={args.mood}")
        print(f"  prompt: {prompt}")
        if generate_track(prompt, output_path):
            generated += 1

    print(f"\nDone — {generated}/{args.count} tracks generated in music/{args.mood}/")


if __name__ == "__main__":
    main()
