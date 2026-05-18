#!/usr/bin/env python3
"""Build a wooden-roll pipeline YAML from generated text, image, and music."""

import argparse
import json
import random
import sys
from datetime import datetime
from pathlib import Path

import yaml

CONFIGS_DIR = Path(__file__).parent.parent / "output" / "configs"
VIDEOS_DIR = Path(__file__).parent.parent / "output" / "videos"
WOODEN_ROLL_DIR = Path(__file__).parent.parent.parent / "wooden-roll"


VOICE_PROFILES = {
    "female": {
        "voice": [
            {"af_nicole": 0.1},
            {"af_heart": 0.1},
            {"bf_emma": 0.1},
            {"af_aoede": 0.4},
            {"pf_dora": 0.3},
        ],
        "speed": 0.80,
    },
    "male": {
        "voice": [
            {"am_eric": 0.4},
            {"bm_fable": 0.35},
            {"am_adam": 0.15},
            {"am_liam": 0.1},
        ],
        "speed": 0.88,
    },
}


def build_text_block(lines: list[str]) -> str:
    """Format lines for wooden-roll: single newline = same screen, blank line = next screen."""
    return "\n\n".join(lines)


def build_config(text_file: Path, image: Path, music: Path) -> tuple[Path, dict]:
    text_data = json.loads(text_file.read_text())

    short_id = f"short_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    output_video = VIDEOS_DIR / f"{short_id}.mp4"
    config_path = CONFIGS_DIR / f"{short_id}.yaml"

    # Paths relative to wooden-roll dir (where node runs from)
    image_rel = str(image.resolve())
    music_rel = str(music.resolve())
    output_rel = str(output_video.resolve())

    config = {
        "steps": [
            {
                "type": "audio",
                "text": build_text_block(text_data["lines"]),
                "outDir": str((WOODEN_ROLL_DIR / "output" / "audio" / short_id).resolve()),
                **random.choice(list(VOICE_PROFILES.values())),
            },
            {
                "type": "video",
                "background": image_rel,
                "output": output_rel,
                "fontSize": 75,
                "textFadeDuration": 0.3,
                "introDelay": 0.5,
                "outroText": "Follow for more 🌍",
                "outroDuration": 2.5,
                "outroFontSize": 60,
                "music": music_rel,
                "musicVolume": 0.08,
                "voiceVolume": 1.5,
            },
        ]
    }

    # Metadata for YouTube (stored separately in the yaml under a comment block)
    lines = text_data["lines"]
    metadata = {
        "title": f"{lines[0]} #languagelearning #motivation",
        "description": " ".join(lines),
        "tags": ["languagelearning", "motivation", "language", "shorts", "studytips"],
        "category_id": "27",
        "short_id": short_id,
        "video_path": str(output_video.resolve()),
    }

    CONFIGS_DIR.mkdir(parents=True, exist_ok=True)
    VIDEOS_DIR.mkdir(parents=True, exist_ok=True)

    # Write wooden-roll config
    config_path.write_text(yaml.dump(config, allow_unicode=True, sort_keys=False))

    # Write metadata sidecar
    meta_path = CONFIGS_DIR / f"{short_id}_meta.json"
    meta_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False))

    return config_path, metadata


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--text-file", required=True)
    parser.add_argument("--image", required=True)
    parser.add_argument("--music", required=True)
    args = parser.parse_args()

    text_file = Path(args.text_file)
    image = Path(args.image)
    music = Path(args.music)

    for p in (text_file, image, music):
        if not p.exists():
            sys.exit(f"File not found: {p}")

    config_path, metadata = build_config(text_file, image, music)

    print(f"config:{config_path}")
    print(f"video:{metadata['video_path']}")
    print(f"title:{metadata['title']}")


if __name__ == "__main__":
    main()
