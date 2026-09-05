#!/usr/bin/env python3
"""Render a list of specific animal parable IDs through the full pipeline."""
import json, math, shutil, subprocess, sys
from pathlib import Path

from dotenv import load_dotenv
load_dotenv()

ROOT = Path(__file__).parent
WOODEN_ROLL = ROOT.parent / "wooden-roll"
ICLOUD_OUTPUT = Path("/Users/panda/Library/Mobile Documents/com~apple~CloudDocs/Experiments/Youtube-shorts/output")

TARGET_IDS = ["animal_037", "animal_038", "animal_039", "animal_040", "animal_041"]

def copy_to_icloud(video_path: str):
    src = Path(video_path)
    if not src.exists():
        return
    ICLOUD_OUTPUT.mkdir(parents=True, exist_ok=True)
    dst = ICLOUD_OUTPUT / src.name
    shutil.copy2(src, dst)
    print(f"\n⚠️  WARNING: video exists in TWO places:")
    print(f"   LOCAL : {src}")
    print(f"   iCLOUD: {dst}")

def cleanup_render_scratch(short_id: str):
    scratch_dir = WOODEN_ROLL / "output" / "audio" / short_id
    if scratch_dir.exists():
        shutil.rmtree(scratch_dir, ignore_errors=True)

def run_step(label: str, cmd: list[str]) -> str:
    print(f"\n▶ {label}")
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(result.stderr)
        sys.exit(f"✗ {label} failed")
    output = result.stdout.strip()
    print(f"  {output}")
    return output

# Find drafts and used.json for parable-animal
fmt_dir = ROOT / "formats" / "parable-animal"
used_file = fmt_dir / "used.json"
used_ids = set(json.loads(used_file.read_text()) if used_file.exists() else [])

# Build map of id → item from all draft files
all_drafts = {}
for f in sorted((fmt_dir / "drafts").glob("parables_*.json")):
    for item in json.loads(f.read_text()):
        if isinstance(item, dict) and "id" in item:
            all_drafts[item["id"]] = item

for target_id in TARGET_IDS:
    print(f"\n{'='*50}")
    print(f"  Rendering {target_id}")
    print(f"{'='*50}")

    if target_id in used_ids:
        print(f"  Already used — skipping"); continue

    item = all_drafts.get(target_id)
    if not item:
        print(f"  Not found in drafts — skipping"); continue

    print(f"  Topic: {item.get('topic', '?')}")

    text_file = ROOT / "output" / "texts" / f"{target_id}_tmp.json"
    text_file.parent.mkdir(parents=True, exist_ok=True)
    text_file.write_text(json.dumps(item, indent=2))

    keywords = ",".join(item.get("keywords", ["animal", "nature"]))
    screen_count = len(item.get("screens", []))
    image_count = str(max(3, math.ceil(screen_count / 2)))

    images_output = run_step(
        "Fetching images",
        ["python3", str(ROOT / "src" / "pipeline" / "image_fetcher.py"),
         "--keywords", keywords, "--count", image_count],
    )
    image_paths = ",".join(images_output.splitlines())

    music_path = run_step(
        "Selecting music",
        ["python3", str(ROOT / "src" / "pipeline" / "music_selector.py"), "--mood", "parable"],
    )

    config_output = run_step(
        "Building config",
        ["python3", str(ROOT / "src" / "pipeline" / "config_builder.py"),
         "--text-file", str(text_file),
         "--images", image_paths,
         "--music", music_path,
         "--type", "parable"],
    )

    config_path = next(
        (line.split("config:")[1] for line in config_output.splitlines() if line.startswith("config:")),
        None,
    )
    video_path = next(
        (line.split("video:")[1] for line in config_output.splitlines() if line.startswith("video:")),
        None,
    )
    if not config_path:
        print("  config_builder returned no config path — skipping"); continue

    print(f"\n▶ Rendering video")
    result = subprocess.run(["node", "src/pipeline.js", config_path], cwd=str(WOODEN_ROLL))
    if result.returncode != 0:
        print(f"  ✗ Render failed — skipping"); continue

    used_ids.add(target_id)
    used_file.write_text(json.dumps(sorted(used_ids), indent=2))
    text_file.unlink(missing_ok=True)

    for img_path in image_paths.split(","):
        Path(img_path.strip()).unlink(missing_ok=True)

    if video_path:
        copy_to_icloud(video_path)
        cleanup_render_scratch(Path(config_path).stem)
        print(f"\n  Done! {video_path}")
