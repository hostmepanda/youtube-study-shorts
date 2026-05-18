#!/usr/bin/env python3
"""Pick a random music track for the given mood."""

import argparse
import random
import sys
from pathlib import Path

MUSIC_DIR = Path(__file__).parent.parent / "music"
VALID_MOODS = ("motivational", "calm", "uplifting")


def select_track(mood: str) -> str:
    folder = MUSIC_DIR / mood
    tracks = list(folder.glob("*.mp3"))
    if not tracks:
        sys.exit(f"No .mp3 files found in {folder} — add tracks manually from pixabay.com/music or similar")
    return str(random.choice(tracks))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--mood", required=True, choices=VALID_MOODS)
    args = parser.parse_args()

    print(select_track(args.mood))


if __name__ == "__main__":
    main()
