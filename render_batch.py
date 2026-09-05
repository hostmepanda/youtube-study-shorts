#!/usr/bin/env python3
"""Render specific IDs from any format through the full pipeline."""
import json, math, shutil, subprocess, sys
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

ROOT = Path(__file__).parent
WOODEN_ROLL = ROOT.parent / "wooden-roll"
ICLOUD_OUTPUT = Path("/Users/panda/Library/Mobile Documents/com~apple~CloudDocs/Experiments/Youtube-shorts/output")

# IDs to render — edit as needed
TARGET_IDS = [
    "text_072",
    "classic_028", "classic_029", "classic_030",
    "animal_042", "animal_043",
]

def copy_to_icloud(video_path: str):
    src = Path(video_path)
    if not src.exists():
        return
    ICLOUD_OUTPUT.mkdir(parents=True, exist_ok=True)
    dst = ICLOUD_OUTPUT / src.name
    shutil.copy2(src, dst)
    print(f"\n⚠️  iCLOUD: {dst}")

def cleanup_render_scratch(short_id: str):
    scratch_dir = WOODEN_ROLL / "output" / "audio" / short_id
    if scratch_dir.exists():
        shutil.rmtree(scratch_dir, ignore_errors=True)

def run_step(label: str, cmd: list[str]) -> str:
    print(f"\n▶ {label}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr[-2000:])
        sys.exit(f"✗ {label} failed")
    output = result.stdout.strip()
    print(f"  {output[:200]}")
    return output

# Build map: id → (item, used_file) from all formats
all_items = {}
for fmt_dir in sorted((ROOT / "formats").iterdir()):
    drafts_dir = fmt_dir / "drafts"
    used_file = fmt_dir / "used.json"
    if not drafts_dir.exists():
        continue
    used_ids = set(json.loads(used_file.read_text()) if used_file.exists() else [])
    for f in sorted(drafts_dir.glob("*.json")):
        for item in json.loads(f.read_text()):
            if isinstance(item, dict) and "id" in item:
                all_items[item["id"]] = (item, used_file, used_ids)

for target_id in TARGET_IDS:
    print(f"\n{'='*50}")
    print(f"  Rendering {target_id}")
    print(f"{'='*50}")

    if target_id not in all_items:
        print("  Not found in any draft — skipping"); continue

    item, used_file, used_ids = all_items[target_id]

    if target_id in used_ids:
        print("  Already in used.json — skipping"); continue

    is_parable = item.get("type") == "parable"
    print(f"  {'Parable' if is_parable else 'Text'}: {item.get('topic') or item.get('lines', ['?'])[0]}")

    text_file = ROOT / "output" / "texts" / f"{target_id}_tmp.json"
    text_file.parent.mkdir(parents=True, exist_ok=True)
    text_file.write_text(json.dumps(item, indent=2))

    keywords = ",".join(item.get("keywords", ["language", "learning"]))
    if is_parable:
        screen_count = len(item.get("screens", []))
        image_count = str(max(3, math.ceil(screen_count / 2)))
    else:
        image_count = "3"

    images_output = run_step(
        "Fetching images",
        ["python3", str(ROOT / "src" / "pipeline" / "image_fetcher.py"),
         "--keywords", keywords, "--count", image_count],
    )
    image_paths = ",".join(images_output.splitlines())

    mood = item.get("mood", "motivational")
    music_path = run_step(
        "Selecting music",
        ["python3", str(ROOT / "src" / "pipeline" / "music_selector.py"), "--mood", mood],
    )

    config_output = run_step(
        "Building config",
        ["python3", str(ROOT / "src" / "pipeline" / "config_builder.py"),
         "--text-file", str(text_file),
         "--images", image_paths,
         "--music", music_path,
         "--type", "parable" if is_parable else "text"],
    )

    config_path = next(
        (line.split("config:")[1] for line in config_output.splitlines() if line.startswith("config:")), None)
    video_path = next(
        (line.split("video:")[1] for line in config_output.splitlines() if line.startswith("video:")), None)

    if not config_path:
        print("  No config path returned — skipping"); continue

    print(f"\n▶ Rendering video")
    result = subprocess.run(["node", "src/pipeline.js", config_path], cwd=str(WOODEN_ROLL))
    if result.returncode != 0:
        print("  ✗ Render failed — skipping"); continue

    used_ids.add(target_id)
    used_file.write_text(json.dumps(sorted(used_ids), indent=2))
    text_file.unlink(missing_ok=True)

    for img_path in image_paths.split(","):
        Path(img_path.strip()).unlink(missing_ok=True)

    if video_path:
        copy_to_icloud(video_path)
        cleanup_render_scratch(Path(config_path).stem)
        print(f"\n  ✅ Done: {video_path}")
