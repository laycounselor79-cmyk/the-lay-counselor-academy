"""
Generate WebP versions of selected content images alongside the originals.

Runs once. Originals are kept so any reference outside the rebuild (Schema.org
Person.image URLs, external links to the OG card images) still resolves.

Usage:
  python3 scripts/convert-webp.py
"""
import os
from pathlib import Path
from PIL import Image

ROOT = Path(__file__).resolve().parent.parent
IMAGES = ROOT / "public" / "images"

# Photographic content images worth converting (high LCP value). Logos and
# watermarks stay PNG because they have transparency and crisp edges that
# WebP lossy can muddy, and the perf delta on small SVG-equivalent PNGs is
# negligible.
TARGETS = [
    "alli-moreno-headshot.png",
    "elizabeth-headshot.png",
    "chcf-evaluation.png",
    "lca-book-cover-en.png",
    "lca-book-cover-es.png",
    "book-cover.png",
    "what-is-lay-counselor.png",
    "pdf-thumb-self-paced.jpg",
    "pdf-thumb-self-paced-faq.jpg",
    "pdf-thumb-course-options.jpg",
    "pdf-thumb-live-faq.png",
    "press-logos.jpg",
]

print(f"Converting {len(TARGETS)} images to WebP…")
for filename in TARGETS:
    src = IMAGES / filename
    if not src.exists():
        print(f"  ! missing: {filename}")
        continue
    dst = src.with_suffix(".webp")
    img = Image.open(src)
    # Preserve alpha if present; encode at quality 82 (visually lossless for
    # photographic content, ~30-40% size reduction vs PNG, ~50% vs JPG).
    save_kwargs = {"quality": 82, "method": 6}
    if img.mode in ("RGBA", "LA", "P"):
        save_kwargs["lossless"] = False
    img.save(dst, "WEBP", **save_kwargs)
    src_size = src.stat().st_size
    dst_size = dst.stat().st_size
    pct = (1 - dst_size / src_size) * 100
    print(f"  → {filename} → {dst.name} ({src_size//1024} KB → {dst_size//1024} KB, -{pct:.0f}%)")

print("Done.")
