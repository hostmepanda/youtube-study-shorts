"""Generate a branded thumbnail for long-monologue videos.

Layout: navy gradient background, gold accent bar on left, hook text (last line in gold),
channel avatar + handle in bottom-right corner.

Usage:
    python3 pipeline/thumbnail_generator.py \
        --lines "He was in prison." "He chose to learn" "their language." \
        --output formats/long-monologue/configs/new/longmono_xxx_thumbnail.jpg
"""

import argparse
from pathlib import Path

from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).parent.parent

W, H = 1280, 720
NAVY_TOP    = (30, 50, 80)
NAVY_BOTTOM = (13, 27, 42)
GOLD        = (245, 166, 35)
WHITE       = (255, 255, 255)

FONT_PATH   = "/System/Library/Fonts/Supplemental/Verdana Bold.ttf"
AVA_PATH    = ROOT / "channel-ava.png"
HANDLE      = "@StudyGoTogether"

FONT_SIZE_MAIN   = 100
FONT_SIZE_HANDLE = 32
AVA_SIZE         = 120
MARGIN           = 40
TEXT_X           = 100
TEXT_Y_START     = 160
LINE_SPACING     = 120


def generate(lines: list[str], output: Path) -> Path:
    if not lines:
        raise ValueError("At least one hook line is required")

    img  = Image.new("RGB", (W, H), NAVY_BOTTOM)
    draw = ImageDraw.Draw(img)

    # Gradient background
    for y in range(H):
        t = y / H
        r = int(NAVY_TOP[0] + (NAVY_BOTTOM[0] - NAVY_TOP[0]) * t)
        g = int(NAVY_TOP[1] + (NAVY_BOTTOM[1] - NAVY_TOP[1]) * t)
        b = int(NAVY_TOP[2] + (NAVY_BOTTOM[2] - NAVY_TOP[2]) * t)
        draw.line([(0, y), (W, y)], fill=(r, g, b))

    # Gold accent bar
    draw.rectangle([60, 80, 68, H - 80], fill=GOLD)

    # Fonts
    try:
        font_main   = ImageFont.truetype(FONT_PATH, FONT_SIZE_MAIN)
        font_handle = ImageFont.truetype(FONT_PATH, FONT_SIZE_HANDLE)
    except OSError:
        font_main = font_handle = ImageFont.load_default()

    # Hook text — last line in gold, rest in white
    for i, line in enumerate(lines):
        color = GOLD if i == len(lines) - 1 else WHITE
        draw.text((TEXT_X, TEXT_Y_START + i * LINE_SPACING), line, font=font_main, fill=color)

    # Avatar + handle block, right-aligned
    hbbox    = draw.textbbox((0, 0), HANDLE, font=font_handle)
    handle_w = hbbox[2] - hbbox[0]
    handle_h = hbbox[3] - hbbox[1]

    block_w  = max(AVA_SIZE, handle_w)
    block_x  = W - block_w - MARGIN
    ava_x    = block_x + (block_w - AVA_SIZE) // 2
    handle_x = block_x + (block_w - handle_w) // 2

    block_h  = AVA_SIZE + 8 + handle_h
    block_y  = H - block_h - MARGIN
    ava_y    = block_y
    handle_y = block_y + AVA_SIZE + 8

    if AVA_PATH.exists():
        ava  = Image.open(AVA_PATH).convert("RGBA")
        ava  = ava.resize((AVA_SIZE, AVA_SIZE), Image.LANCZOS)
        mask = Image.new("L", (AVA_SIZE, AVA_SIZE), 0)
        ImageDraw.Draw(mask).ellipse([0, 0, AVA_SIZE, AVA_SIZE], fill=255)
        ava.putalpha(mask)
        img.paste(ava, (ava_x, ava_y), ava)

    draw.text((handle_x, handle_y), HANDLE, font=font_handle, fill=GOLD)

    output.parent.mkdir(parents=True, exist_ok=True)
    img.save(str(output), "JPEG", quality=95)
    return output


def main():
    parser = argparse.ArgumentParser(description="Generate a long-monologue thumbnail")
    parser.add_argument("--lines", nargs="+", required=True, help="Hook lines (last line rendered in gold)")
    parser.add_argument("--output", required=True, help="Output path for the thumbnail JPEG")
    args = parser.parse_args()

    out = generate(args.lines, Path(args.output))
    print(f"✓ Thumbnail saved: {out}")


if __name__ == "__main__":
    main()
