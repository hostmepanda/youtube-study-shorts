#!/usr/bin/env python3
"""Entry point — runs the full pipeline for one short."""

import json
import subprocess
import sys
from datetime import datetime
from pathlib import Path

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
        sys.exit(result.returncode)

    print("=" * 50)
    print("  YouTube Shorts Pipeline")
    print("=" * 50)

    # 1. Text — passed in as a JSON file or use a sample
    text_files = sorted((ROOT / "output" / "texts").glob("*.json"))
    if not text_files:
        sys.exit("No text files found in output/texts/. Run /generate-short to create one.")

    # Pick the most recent unused text
    text_file = text_files[-1]
    text_data = json.loads(text_file.read_text())
    print(f"\n▶ Text: {text_file.name}")
    for line in text_data["lines"]:
        print(f"  {line}")

    # 2. Fetch image
    keywords = ",".join(text_data.get("keywords", ["language", "learning"]))
    image_path = run_step(
        "Fetching image",
        ["python3", str(ROOT / "pipeline" / "image_fetcher.py"), "--keywords", keywords],
    )

    # 3. Select music
    mood = text_data.get("mood", "motivational")
    music_path = run_step(
        "Selecting music",
        ["python3", str(ROOT / "pipeline" / "music_selector.py"), "--mood", mood],
    )

    # 4. Build wooden-roll config
    config_output = run_step(
        "Building config",
        [
            "python3", str(ROOT / "pipeline" / "config_builder.py"),
            "--text-file", str(text_file),
            "--image", image_path,
            "--music", music_path,
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

    print("\n" + "=" * 50)
    print(f"  Done! {video_path}")
    print("=" * 50)


if __name__ == "__main__":
    main()
