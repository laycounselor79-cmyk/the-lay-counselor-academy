"""
Render every page of the built site to PDF for a client deliverable.

Uses Playwright so each route becomes ONE PDF page sized to the rendered
content, no Letter-sized slicing, no blank pages. The result is a tall,
continuous, one-page-per-route document.

Usage:
  npm run build
  python3 scripts/generate-site-pdf.py

Output: dist-pdf/the-lay-counselor-academy.pdf
"""
import io
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

import pikepdf
from PIL import Image
from playwright.sync_api import sync_playwright
from pypdf import PdfReader, PdfWriter

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
OUT_DIR = ROOT / "dist-pdf"
PAGES_DIR = OUT_DIR / "pages"
OUT_DIR.mkdir(exist_ok=True)
PAGES_DIR.mkdir(exist_ok=True)

PORT = 4322
BASE = f"http://localhost:{PORT}"

VIEWPORT_WIDTH = 1280  # narrower than 1440 → smaller PDF, still desktop-grade
SAFETY_PX = 8           # tiny pad to absorb sub-pixel rounding

ROUTES = [
    ("/", "01-home-en"),
    ("/curriculum/", "02-curriculum-en"),
    ("/pricing/", "03-pricing-en"),
    ("/faq/", "04-faq-en"),
    ("/reviews/", "05-reviews-en"),
    ("/contact/", "06-contact-en"),
    ("/teachers/elizabeth-morrison/", "07-elizabeth-en"),
    ("/teachers/alli-moreno/", "08-alli-en"),
    ("/accessibility/", "09-accessibility-en"),
    ("/404.html", "10-404-en"),
    ("/es/", "11-home-es"),
    ("/es/curriculum/", "12-curriculum-es"),
    ("/es/pricing/", "13-pricing-es"),
    ("/es/faq/", "14-faq-es"),
    ("/es/reviews/", "15-reviews-es"),
    ("/es/contact/", "16-contact-es"),
    ("/es/404/", "17-404-es"),
]


def start_server() -> subprocess.Popen:
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


def capture(page, route: str, slug: str) -> Path:
    """Render a single route to a single-page PDF sized to content height."""
    out = PAGES_DIR / f"{slug}.pdf"
    print(f"  → {route}")
    page.goto(BASE + route, wait_until="networkidle")
    # Ensure web fonts have actually painted before we measure height.
    page.evaluate("document.fonts && document.fonts.ready")
    # Force lazy-loaded images and reveal-on-scroll content to render.
    page.evaluate("window.scrollTo(0, document.body.scrollHeight)")
    page.wait_for_timeout(250)
    page.evaluate("window.scrollTo(0, 0)")
    page.wait_for_timeout(150)

    height_px = page.evaluate(
        "Math.max("
        " document.body.scrollHeight,"
        " document.documentElement.scrollHeight,"
        " document.body.offsetHeight,"
        " document.documentElement.offsetHeight"
        ")"
    )
    height_px = int(height_px) + SAFETY_PX

    page.pdf(
        path=str(out),
        width=f"{VIEWPORT_WIDTH}px",
        height=f"{height_px}px",
        print_background=True,
        margin={"top": "0", "right": "0", "bottom": "0", "left": "0"},
        prefer_css_page_size=False,
    )
    return out


def merge(pdfs: list[Path], out_path: Path) -> None:
    writer = PdfWriter()
    for p in pdfs:
        reader = PdfReader(str(p))
        for page in reader.pages:
            writer.add_page(page)
    with open(out_path, "wb") as f:
        writer.write(f)


def compress_images(pdf_path: Path, jpeg_quality: int = 70, max_width: int = 1100) -> None:
    """Recompress every embedded raster image to JPEG and downscale wide ones.

    The homepage embeds large photos at source resolution, which dominates PDF
    size. Rewriting each Stream in place to /DCTDecode keeps the visual
    fidelity needed for a desktop review document while cutting size sharply.
    """
    seen: set[int] = set()
    with pikepdf.open(pdf_path, allow_overwriting_input=True) as pdf:
        for page in pdf.pages:
            for _name, raw in page.images.items():
                obj_id = (raw.objgen[0], raw.objgen[1]) if raw.objgen != (0, 0) else id(raw)
                if obj_id in seen:
                    continue
                seen.add(obj_id)

                try:
                    pdf_image = pikepdf.PdfImage(raw)
                    pil = pdf_image.as_pil_image()
                except Exception:
                    continue

                if pil.mode != "RGB":
                    pil = pil.convert("RGB")
                if pil.width > max_width:
                    new_h = max(1, int(pil.height * (max_width / pil.width)))
                    pil = pil.resize((max_width, new_h), Image.LANCZOS)

                buf = io.BytesIO()
                pil.save(buf, format="JPEG", quality=jpeg_quality, optimize=True)

                raw.write(buf.getvalue(), filter=pikepdf.Name("/DCTDecode"))
                raw.Width = pil.width
                raw.Height = pil.height
                raw.ColorSpace = pikepdf.Name("/DeviceRGB")
                raw.BitsPerComponent = 8
                for stale in ("/DecodeParms", "/SMask", "/Mask"):
                    if stale in raw:
                        del raw[stale]
        pdf.save(pdf_path, object_stream_mode=pikepdf.ObjectStreamMode.generate)


def main() -> None:
    if not DIST.exists():
        raise SystemExit("dist/ not found. Run `npm run build` first.")

    proc = start_server()
    pdfs: list[Path] = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            context = browser.new_context(
                viewport={"width": VIEWPORT_WIDTH, "height": 900},
                device_scale_factor=1,
            )
            page = context.new_page()
            print("Capturing pages…")
            for route, slug in ROUTES:
                pdfs.append(capture(page, route, slug))
            browser.close()
    finally:
        proc.terminate()
        proc.wait()

    final = OUT_DIR / "the-lay-counselor-academy.pdf"
    print(f"Merging {len(pdfs)} PDFs → {final.relative_to(ROOT)}")
    merge(pdfs, final)
    raw_mb = final.stat().st_size / 1024 / 1024
    print(f"  Merged: {raw_mb:.1f} MB")

    print("Compressing embedded images…")
    compress_images(final)
    size_mb = final.stat().st_size / 1024 / 1024
    print(f"Done. {size_mb:.1f} MB")


if __name__ == "__main__":
    main()
