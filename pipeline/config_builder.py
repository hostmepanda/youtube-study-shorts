#!/usr/bin/env python3
"""Build a wooden-roll pipeline YAML from generated text, image, and music."""

import argparse
import json
import os
import random
import sys
from datetime import datetime
from pathlib import Path

import yaml

SUPPORT_LINES = [
    "You've got this.",
    "One step at a time.",
    "Keep going.",
    "Progress over perfection.",
    "Every word counts.",
    "You're closer than you think.",
    "Small steps. Big results.",
    "Believe in the process.",
    "It gets easier. Keep talking.",
    "Your effort is already paying off.",
    "Proud of you for trying.",
    "The best is ahead of you.",
    "One conversation can change everything.",
    "You're doing better than you know.",
    "Courage sounds like your voice.",
    "Stay curious. Stay speaking.",
    "Growth is happening. Trust it.",
    "Every mistake is a step forward.",
    "The world wants to hear you.",
    "You belong in this language.",
]

CHANNEL = "@StudyGoTogether"

SUBSCRIBE_CTAS = [
    "Subscribe to keep going",
    "Subscribe to stay on track",
    "Subscribe — show up tomorrow",
    "Subscribe for your daily push",
    "Subscribe — one day at a time",
]

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
    cleaned = [line.rstrip(".") for line in lines]
    return "\n\n".join(cleaned)


def build_parable_text(screens: list[dict]) -> str:
    # Each screen is one subtitle phrase; lines within a screen stay together
    return "\n\n".join(s["text"] for s in screens)


def build_config(text_file: Path, images: list[Path], music: Path) -> tuple[Path, dict]:
    text_data = json.loads(text_file.read_text())
    if isinstance(text_data, list):
        text_data = text_data[0]

    short_id = f"short_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    output_video = VIDEOS_DIR / f"{short_id}.mp4"
    config_path = CONFIGS_DIR / f"{short_id}.yaml"

    images_abs = [str(Path(img).resolve()) for img in images]
    music_rel = str(music.resolve())
    output_rel = str(output_video.resolve())

    config = {
        "steps": [
            {
                "type": "audio",
                "text": build_text_block(text_data["lines"] + [random.choice(SUPPORT_LINES)]),
                "outDir": str((WOODEN_ROLL_DIR / "output" / "audio" / short_id).resolve()),
                **random.choice(list(VOICE_PROFILES.values())),
                "phraseGap": 0.5,
                **({"cloneVoice": os.environ["CLONE_VOICE_PATH"]} if os.environ.get("CLONE_VOICE_PATH") else {}),
            },
            {
                "type": "video",
                "backgroundImages": images_abs,
                "imageTransition": "fade",
                "imageTransitionDuration": 0.5,
                "output": output_rel,
                "fontSize": 205,
                "textOutlineSize": 8,
                "textOutlineColor": "#000000",
                "textFadeDuration": 0.3,
                "introDelay": 0.5,
                "outroText": f"{random.choice(SUBSCRIBE_CTAS)}\n{CHANNEL}",
                "outroDuration": 5.0,
                "outroFontSize": 100,
                "music": music_rel,
                "musicVolume": 0.08,
                "musicOffset": "random",
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


def build_parable_config(parable_file: Path, images: list[Path], music: Path) -> tuple[Path, dict]:
    parable = json.loads(parable_file.read_text())
    if isinstance(parable, list):
        parable = parable[0]

    short_id = f"parable_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    output_video = VIDEOS_DIR / f"{short_id}.mp4"
    config_path = CONFIGS_DIR / f"{short_id}.yaml"

    images_abs = [str(Path(img).resolve()) for img in images]

    # Slower speed and longer phrase gap — parables need space to breathe
    voice_profile = random.choice(list(VOICE_PROFILES.values())).copy()
    voice_profile["speed"] = round(voice_profile["speed"] * 0.92, 2)

    config = {
        "steps": [
            {
                "type": "audio",
                "text": build_parable_text(parable["screens"]),
                "outDir": str((WOODEN_ROLL_DIR / "output" / "audio" / short_id).resolve()),
                **voice_profile,
                "phraseGap": 0.8,
                **({"cloneVoice": os.environ["CLONE_VOICE_PATH"]} if os.environ.get("CLONE_VOICE_PATH") else {}),
            },
            {
                "type": "video",
                "backgroundImages": images_abs,
                "imageTransition": "fade",
                "imageTransitionDuration": 1.0,
                "output": str(output_video.resolve()),
                "fontSize": 185,
                "textOutlineSize": 7,
                "textOutlineColor": "#000000",
                "textFadeDuration": 0.5,
                "introDelay": 0.8,
                "outroText": f"{random.choice(SUBSCRIBE_CTAS)}\n{CHANNEL}",
                "outroDuration": 5.0,
                "outroFontSize": 100,
                "music": str(music.resolve()),
                "musicVolume": 0.10,
                "musicOffset": "random",
                "voiceVolume": 1.5,
            },
        ]
    }

    first_screen_first_line = parable["screens"][0]["text"].split("\n")[0]
    metadata = {
        "title": f"{first_screen_first_line} #languagelearning #parable",
        "description": " ".join(s["text"].replace("\n", " ") for s in parable["screens"]),
        "tags": ["languagelearning", "parable", "motivation", "shorts", "studytips"],
        "category_id": "27",
        "short_id": short_id,
        "video_path": str(output_video.resolve()),
    }

    CONFIGS_DIR.mkdir(parents=True, exist_ok=True)
    VIDEOS_DIR.mkdir(parents=True, exist_ok=True)

    config_path.write_text(yaml.dump(config, allow_unicode=True, sort_keys=False))
    meta_path = CONFIGS_DIR / f"{short_id}_meta.json"
    meta_path.write_text(json.dumps(metadata, indent=2, ensure_ascii=False))

    return config_path, metadata


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--text-file", required=True)
    parser.add_argument("--images", required=True, help="Comma-separated image paths")
    parser.add_argument("--music", required=True)
    parser.add_argument("--type", default="text", choices=["text", "parable"])
    args = parser.parse_args()

    text_file = Path(args.text_file)
    images = [Path(p.strip()) for p in args.images.split(",")]
    music = Path(args.music)

    for p in ([text_file] + images + [music]):
        if not p.exists():
            sys.exit(f"File not found: {p}")

    if args.type == "parable":
        config_path, metadata = build_parable_config(text_file, images, music)
    else:
        config_path, metadata = build_config(text_file, images, music)

    print(f"config:{config_path}")
    print(f"video:{metadata['video_path']}")
    print(f"title:{metadata['title']}")


if __name__ == "__main__":
    main()
