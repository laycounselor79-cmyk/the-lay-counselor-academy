"""
Generate favicon assets from /public/images/lca-logo.png.

The source lockup is 268x268 with the circular mark in the top ~60% and the
wordmark in the bottom ~40%. We crop to a square covering just the mark, then
resample to the standard favicon sizes:

  favicon-32.png       (browser tab)
  favicon-180.png      (apple-touch-icon, iOS home screen)
  favicon-512.png      (PWA / high-DPI fallback)
  favicon.ico          (legacy multi-size)

Outputs land in /public/. The existing favicon.svg is kept as the primary
declaration (browsers prefer SVG), but the PNGs are also registered in
Layout.astro for tabs and home-screen tiles.

Usage:
  python3 scripts/generate-favicon.py
"""
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
SRC = ROOT / "public" / "images" / "lca-logo.png"
OUT = ROOT / "public"

src_img = Image.open(SRC).convert("RGBA")
w, h = src_img.size
print(f"Source: {SRC.name} {w}x{h}")

# Crop a square framed around the circular mark. The mark itself (the navy
# circle with the heart) spans roughly y=15 to y=155 in the 268px source;
# we center the crop on the circle and give ~8px of breathing room on each
# side so the bottom edge isn't kissing the favicon edge.
side = int(h * 0.60)
left = (w - side) // 2
top = int(h * 0.022)
right = left + side
bottom = top + side
mark = src_img.crop((left, top, right, bottom))

# Square the alpha background so transparent regions stay transparent.
SIZES = {
    "favicon-32.png": 32,
    "favicon-180.png": 180,
    "favicon-512.png": 512,
}

for filename, size in SIZES.items():
    resized = mark.resize((size, size), Image.LANCZOS)
    out_path = OUT / filename
    resized.save(out_path, "PNG", optimize=True)
    print(f"  → {filename} {size}x{size} ({out_path.stat().st_size//1024} KB)")

# Multi-size .ico for legacy browsers (Windows pinned, RSS readers, etc.)
ico_sizes = [(16, 16), (32, 32), (48, 48), (64, 64)]
mark.resize((64, 64), Image.LANCZOS).save(
    OUT / "favicon.ico",
    format="ICO",
    sizes=ico_sizes,
)
print(f"  → favicon.ico (multi-size: {ico_sizes})")

print("Done.")
