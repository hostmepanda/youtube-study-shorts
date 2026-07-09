#!/usr/bin/env python3
"""Entry point — runs the full pipeline for one short."""

import json
import math
import shutil
import subprocess
import sys
from datetime import datetime
from pathlib import Path

ICLOUD_OUTPUT = Path("/Users/panda/Library/Mobile Documents/com~apple~CloudDocs/Experiments/Youtube-shorts/output")


def copy_to_icloud(video_path: str):
    src = Path(video_path)
    if not src.exists():
        return
    ICLOUD_OUTPUT.mkdir(parents=True, exist_ok=True)
    dst = ICLOUD_OUTPUT / src.name
    shutil.copy2(src, dst)
    print("\n⚠️  WARNING: video exists in TWO places:")
    print(f"   LOCAL : {src}")
    print(f"   iCLOUD: {dst}")


def cleanup_render_scratch(short_id: str):
    """Delete the wooden-roll scratch dir (TTS audio, bg_clips, subtitles) for a finished render."""
    scratch_dir = WOODEN_ROLL / "output" / "audio" / short_id
    if scratch_dir.exists():
        shutil.rmtree(scratch_dir, ignore_errors=True)

from dotenv import load_dotenv
load_dotenv()

ROOT = Path(__file__).parent
WOODEN_ROLL = ROOT.parent / "wooden-roll"


def run_step(label: str, cmd: list[str]) -> str:
    print(f"\n▶ {label}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr)
        sys.exit(f"✗ {label} failed")
    output = result.stdout.strip()
    print(f"  {output}")
    return output


def main():
    if not (ROOT.parent / "wooden-roll").exists():
        sys.exit("wooden-roll repo not found at ../wooden-roll")

    # If a config path is passed, skip straight to rendering
    if len(sys.argv) == 2:
        config_path = sys.argv[1]
        print(f"\n▶ Rendering {config_path}")
        result = subprocess.run(
            ["node", "src/pipeline.js", str(Path(config_path).resolve())],
            cwd=str(WOODEN_ROLL),
        )
        if result.returncode == 0:
            import yaml
            cfg = yaml.safe_load(Path(config_path).read_text())
            video_path = next(
                (s.get("output") for s in cfg.get("steps", []) if s.get("type") == "video"),
                None,
            )
            if video_path:
                copy_to_icloud(video_path)
            cleanup_render_scratch(Path(config_path).stem)
        sys.exit(result.returncode)

    print("=" * 50)
    print("  YouTube Shorts Pipeline")
    print("=" * 50)

    # 1. Pick next unused item — scans legacy output/texts/ plus all formats/*/drafts/
    legacy_dir = ROOT / "output" / "texts"
    legacy_used = legacy_dir / "used_texts.json"
    sources = [(f, legacy_used) for f in sorted(legacy_dir.glob("batch_*.json")) + sorted(legacy_dir.glob("parables_*.json"))]

    formats_dir = ROOT / "formats"
    if formats_dir.exists():
        for fmt_dir in sorted(formats_dir.iterdir()):
            drafts_dir = fmt_dir / "drafts"
            if drafts_dir.exists():
                fmt_used = fmt_dir / "used.json"
                sources += [(f, fmt_used) for f in sorted(drafts_dir.glob("*.json"))]

    text_data = None
    source_batch = None
    used_file = None
    used_ids = None
    for batch_file, candidate_used_file in reversed(sources):
        candidate_used_ids = set(json.loads(candidate_used_file.read_text()) if candidate_used_file.exists() else [])
        batch = json.loads(batch_file.read_text())
        for item in batch:
            if item["id"] not in candidate_used_ids:
                text_data = item
                source_batch = batch_file
                used_file = candidate_used_file
                used_ids = candidate_used_ids
                break
        if text_data:
            break

    if not text_data:
        sys.exit("No unused texts left. Run /generate-texts, /generate-parables, or /generate-animal-parable to create a new batch.")

    is_parable = text_data.get("type") == "parable"

    if is_parable:
        print(f"\n▶ Parable [{text_data['id']}] from {source_batch.name}")
        print(f"  Topic: {text_data['topic']}")
        for s in text_data["screens"]:
            print(f"  [{s['screen']}] {s['text'].splitlines()[0]}")
    else:
        print(f"\n▶ Text [{text_data['id']}] from {source_batch.name}")
        for line in text_data["lines"]:
            print(f"  {line}")

    # Write to a temp single-text file for the pipeline scripts
    text_file = ROOT / "output" / "texts" / f"{text_data['id']}_tmp.json"
    text_file.write_text(json.dumps(text_data, indent=2))

    # 2. Fetch images — parables need one per 2 screens
    keywords = ",".join(text_data.get("keywords", ["language", "learning"]))
    if is_parable:
        screen_count = len(text_data.get("screens", []))
        image_count = str(max(3, math.ceil(screen_count / 2)))
    else:
        image_count = "3"
    images_output = run_step(
        "Fetching images",
        ["python3", str(ROOT / "src" / "pipeline" / "image_fetcher.py"), "--keywords", keywords, "--count", image_count],
    )
    image_paths = ",".join(images_output.splitlines())

    # 3. Select music
    mood = text_data.get("mood", "motivational")
    music_path = run_step(
        "Selecting music",
        ["python3", str(ROOT / "src" / "pipeline" / "music_selector.py"), "--mood", mood],
    )

    # 4. Build wooden-roll config
    config_output = run_step(
        "Building config",
        [
            "python3", str(ROOT / "src" / "pipeline" / "config_builder.py"),
            "--text-file", str(text_file),
            "--images", image_paths,
            "--music", music_path,
            "--type", "parable" if is_parable else "text",
        ],
    )

    config_path = next(
        (line.split("config:")[1] for line in config_output.splitlines() if line.startswith("config:")),
        None,
    )
    if not config_path:
        sys.exit("config_builder did not return a config path")

    video_path = next(
        (line.split("video:")[1] for line in config_output.splitlines() if line.startswith("video:")),
        None,
    )

    # 5. Render via wooden-roll
    print(f"\n▶ Rendering video")
    result = subprocess.run(
        ["node", "src/pipeline.js", config_path],
        cwd=str(WOODEN_ROLL),
    )
    if result.returncode != 0:
        sys.exit("✗ Render failed")

    # Mark text as used
    used_ids.add(text_data["id"])
    used_file.write_text(json.dumps(sorted(used_ids), indent=2))
    text_file.unlink(missing_ok=True)

    # Remove images — no longer needed once video is rendered
    for img_path in image_paths.split(","):
        Path(img_path.strip()).unlink(missing_ok=True)

    copy_to_icloud(video_path)
    cleanup_render_scratch(Path(config_path).stem)

    print("\n" + "=" * 50)
    print(f"  Done! {video_path}")
    print("=" * 50)


if __name__ == "__main__":
    main()
