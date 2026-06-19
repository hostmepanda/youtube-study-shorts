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

PROJECT_ROOT = Path(__file__).parent.parent
CONFIGS_DIR = PROJECT_ROOT / "output" / "configs"
VIDEOS_DIR = PROJECT_ROOT / "output" / "videos"
WOODEN_ROLL_DIR = PROJECT_ROOT.parent / "wooden-roll"
SETTINGS_FILE = PROJECT_ROOT / "config" / "settings.yaml"


def _settings() -> dict:
    return yaml.safe_load(SETTINGS_FILE.read_text()) if SETTINGS_FILE.exists() else {}


def _clone_voice_path() -> str | None:
    """Return voice reference path: CLONE_VOICE_PATH env > settings.yaml > None."""
    explicit = os.environ.get("CLONE_VOICE_PATH")
    if explicit:
        return explicit
    rel = _settings().get("voice", {}).get("custom_voice")
    if rel:
        path = PROJECT_ROOT / rel
        if path.exists():
            return str(path)
    return None


def _premiss_config(voice: str | None = None) -> dict | None:
    """Return Premiss config if api_key is available (env or settings.yaml), else None."""
    settings = _settings()
    premiss = settings.get("premiss", {}) or {}
    api_key = os.environ.get("PREMISS_API_KEY") or premiss.get("api_key")
    if not api_key:
        return None
    return {
        "api_url": premiss.get("api_url", "https://core.premiss.ru"),
        "api_key": api_key,
        "voice": voice or os.environ.get("PREMISS_VOICE") or premiss.get("voice", "violet"),
    }


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


def build_parable_tts_text(screens: list[dict]) -> str:
    """Build punctuated text for TTS. Lines within a screen are joined as flowing speech."""
    import re
    parts = []
    for s in screens:
        lines = [l.strip() for l in s["text"].split("\n") if l.strip()]
        punctuated = []
        for line in lines:
            if re.search(r"[.!?,;]$", line):
                punctuated.append(line)
            else:
                punctuated.append(line + ".")
        parts.append(" ".join(punctuated))
    return "\n\n".join(parts)


def build_config(text_file: Path, images: list[Path], music: Path, voice: str | None = None) -> tuple[Path, dict]:
    text_data = json.loads(text_file.read_text())
    if isinstance(text_data, list):
        text_data = text_data[0]

    short_id = f"short_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    output_video = VIDEOS_DIR / f"{short_id}.mp4"
    config_path = CONFIGS_DIR / f"{short_id}.yaml"

    images_abs = [str(Path(img).resolve()) for img in images]
    music_rel = str(music.resolve())
    output_rel = str(output_video.resolve())

    premiss = _premiss_config(voice)
    if premiss:
        audio_step = {
            "type": "premiss-audio",
            "text": build_text_block(text_data["lines"] + [random.choice(SUPPORT_LINES)]),
            "outDir": str((WOODEN_ROLL_DIR / "output" / "audio" / short_id).resolve()),
            "apiUrl": premiss["api_url"],
            "apiKey": premiss["api_key"],
            "voice": premiss["voice"],
        }
    else:
        audio_step = {
            "type": "audio",
            "text": build_text_block(text_data["lines"] + [random.choice(SUPPORT_LINES)]),
            "outDir": str((WOODEN_ROLL_DIR / "output" / "audio" / short_id).resolve()),
            **random.choice(list(VOICE_PROFILES.values())),
            "phraseGap": 0.5,
            **( {"cloneVoice": _clone_voice_path()} if _clone_voice_path() else {}),
        }

    config = {
        "steps": [
            audio_step,
            {
                "type": "video",
                "backgroundImages": images_abs,
                "imageTransition": "fade",
                "imageTransitionDuration": 0.5,
                "output": output_rel,
                "fontSize": 160,
                "textOutlineSize": 8,
                "textOutlineColor": "#000000",
                "textFadeDuration": 0.3,
                "introDelay": 0.5,
                "outroText": f"{random.choice(SUBSCRIBE_CTAS)}\n{CHANNEL}",
                "outroDuration": 5.0,
                "outroFontSize": 100,
                "music": music_rel,
                "musicVolume": 0.3,
                "musicOffset": "random",
                "voiceVolume": 1.2,
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


def build_parable_config(parable_file: Path, images: list[Path], music: Path, voice: str | None = None, short_id: str | None = None) -> tuple[Path, dict]:
    parable = json.loads(parable_file.read_text())
    if isinstance(parable, list):
        parable = parable[0]

    short_id = short_id or f"parable_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
    output_video = VIDEOS_DIR / f"{short_id}.mp4"
    config_path = CONFIGS_DIR / f"{short_id}.yaml"

    images_abs = [str(Path(img).resolve()) for img in images]

    # Separate hook (screen 0) from story screens
    all_screens = parable["screens"]
    hook_screen = next((s for s in all_screens if s["screen"] == 0), None)
    story_screens = [s for s in all_screens if s["screen"] != 0]

    # Slower speed and longer phrase gap — parables need space to breathe
    voice_profile = random.choice(list(VOICE_PROFILES.values())).copy()
    voice_profile["speed"] = round(voice_profile["speed"] * 0.92, 2)

    premiss = _premiss_config(voice)
    if premiss:
        audio_step = {
            "type": "premiss-audio",
            "text": build_parable_tts_text(story_screens),
            "outDir": str((WOODEN_ROLL_DIR / "output" / "audio" / short_id).resolve()),
            "apiUrl": premiss["api_url"],
            "apiKey": premiss["api_key"],
            "voice": premiss["voice"],
            "speed": 1.0,
            "phraseGap": 0.52,
        }
    else:
        audio_step = {
            "type": "audio",
            "text": build_parable_text(story_screens),
            "outDir": str((WOODEN_ROLL_DIR / "output" / "audio" / short_id).resolve()),
            **voice_profile,
            "phraseGap": 0.8,
            **( {"cloneVoice": _clone_voice_path()} if _clone_voice_path() else {}),
        }

    # Use per-screen video queries if available, otherwise fall back to images
    video_queries = parable.get("video_queries")
    if video_queries:
        background = {
            "backgroundVideos": [{"query": q} for q in video_queries],
            "imageTransition": "fade",
            "imageTransitionDuration": 1.0,
        }
    else:
        background = {
            "backgroundImages": images_abs,
            "imageTransition": "fade",
            "imageTransitionDuration": 1.0,
        }

    config = {
        "steps": [
            audio_step,
            {
                "type": "video",
                **background,
                "output": str(output_video.resolve()),
                "fontSize": 113,
                **( {"hookText": hook_screen["text"], "hookFontSize": 180, "hookDuration": 3.0} if hook_screen else {} ),
                "lastScreenCentered": True,
                "lastFontSize": 180,
                "textAlignment": 2,
                "textMarginV": 80,
                "textOutlineSize": 7,
                "textOutlineColor": "#000000",
                "textFadeDuration": 0.5,
                "introDelay": 3.5,
                "outroText": f"Didn't motivate?\nDrop a message in comments\n\n{random.choice(SUBSCRIBE_CTAS)}\n{CHANNEL}",
                "outroDuration": 5.0,
                "outroFontSize": 100,
                "music": str(music.resolve()),
                "musicVolume": 0.3,
                "musicOffset": 0,
                "voiceVolume": 1.3,
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
    parser.add_argument("--voice", default=None, help="Premiss voice name (overrides settings.yaml and PREMISS_VOICE env)")
    parser.add_argument("--short-id", default=None, help="Override output filename (without extension)")
    args = parser.parse_args()

    text_file = Path(args.text_file)
    images = [Path(p.strip()) for p in args.images.split(",")]
    music = Path(args.music)

    for p in ([text_file] + images + [music]):
        if not p.exists():
            sys.exit(f"File not found: {p}")

    if args.type == "parable":
        config_path, metadata = build_parable_config(text_file, images, music, voice=args.voice, short_id=getattr(args, 'short_id', None))
    else:
        config_path, metadata = build_config(text_file, images, music, voice=args.voice)

    print(f"config:{config_path}")
    print(f"video:{metadata['video_path']}")
    print(f"title:{metadata['title']}")


if __name__ == "__main__":
    main()
