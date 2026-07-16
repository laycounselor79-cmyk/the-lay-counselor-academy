"""
Render every page of the built site as a full-page PNG for client review.

Each route is loaded in headless Chrome at a tall viewport, screenshotted,
then trimmed at the bottom where the page ends (everything below the last
non-background row is cropped).

Usage:
  npm run build
  python3 scripts/generate-site-images.py

Output: dist-images/<NN>-<slug>.png  (one PNG per page)
"""
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path
from PIL import Image, ImageChops

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
OUT_DIR = ROOT / "dist-images"
OUT_DIR.mkdir(exist_ok=True)

CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PORT = 4322
BASE = f"http://localhost:{PORT}"

VIEWPORT_W = 1440
VIEWPORT_H = 14000  # well taller than any page, trimmed afterwards

# Slugs intentionally include leading numbers so file ordering matches the
# narrative we want the client to follow.
ROUTES = [
    ("/", "01-home"),
    ("/curriculum/", "02-curriculum"),
    ("/pricing/", "03-pricing"),
    ("/faq/", "04-faq"),
    ("/reviews/", "05-reviews"),
    ("/contact/", "06-contact"),
    ("/teachers/elizabeth-morrison/", "07-elizabeth-morrison"),
    ("/teachers/alli-moreno/", "08-alli-moreno"),
    ("/accessibility/", "09-accessibility"),
    ("/404.html", "10-404-en"),
    ("/es/", "11-es-home"),
    ("/es/curriculum/", "12-es-curriculum"),
    ("/es/pricing/", "13-es-pricing"),
    ("/es/faq/", "14-es-faq"),
    ("/es/reviews/", "15-es-reviews"),
    ("/es/contact/", "16-es-contact"),
    ("/es/404/", "17-404-es"),
]


def start_server():
    print(f"Starting static server on :{PORT}…")
    proc = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
        cwd=str(DIST),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    for _ in range(40):
        try:
            urllib.request.urlopen(BASE + "/", timeout=0.5)
            print("  → server up")
            return proc
        except (urllib.error.URLError, ConnectionResetError):
            time.sleep(0.25)
    proc.terminate()
    raise RuntimeError("Server failed to start")


def screenshot_raw(route: str, raw_path: Path) -> None:
    """Capture a tall viewport screenshot. Trimming happens afterwards."""
    subprocess.run(
        [
            CHROME,
            "--headless=new",
            "--disable-gpu",
            "--no-sandbox",
            "--hide-scrollbars",
            "--virtual-time-budget=4000",
            "--run-all-compositor-stages-before-draw",
            f"--window-size={VIEWPORT_W},{VIEWPORT_H}",
            f"--screenshot={raw_path}",
            BASE + route,
        ],
        check=True,
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )


def trim_bottom(img: Image.Image, bottom_pad: int = 24) -> Image.Image:
    """Crop the image at the last row that visibly differs from the page's
    background color. We sample the bottom-right pixel as the background
    (it's almost always outside the last footer pixel, in the body bg)."""
    rgb = img.convert("RGB")
    w, h = rgb.size
    bg = rgb.getpixel((w - 5, h - 5))
    # Build a single-color reference image and diff it to find non-background.
    bg_img = Image.new("RGB", rgb.size, bg)
    diff = ImageChops.difference(rgb, bg_img)
    bbox = diff.getbbox()
    if not bbox:
        return rgb
    _, _, _, last_y = bbox
    last_y = min(h, last_y + bottom_pad)
    return rgb.crop((0, 0, w, last_y))


def main() -> None:
    if not DIST.exists():
        raise SystemExit("dist/ not found. Run `npm run build` first.")
    if not Path(CHROME).exists():
        raise SystemExit(f"Chrome not at {CHROME}")

    raw_dir = OUT_DIR / "_raw"
    raw_dir.mkdir(exist_ok=True)

    proc = start_server()
    try:
        print("Capturing pages…")
        for route, slug in ROUTES:
            raw = raw_dir / f"{slug}.png"
            final = OUT_DIR / f"{slug}.png"
            screenshot_raw(route, raw)
            img = Image.open(raw)
            trimmed = trim_bottom(img)
            trimmed.save(final, "PNG", optimize=True)
            print(f"  → {slug}.png ({trimmed.size[0]}×{trimmed.size[1]}, {final.stat().st_size//1024} KB)")
    finally:
        proc.terminate()
        proc.wait()

    # Optional: clean up the raw uncropped versions
    import shutil
    shutil.rmtree(raw_dir, ignore_errors=True)
    print(f"\nDone. {len(ROUTES)} PNGs in {OUT_DIR.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
