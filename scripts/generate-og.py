"""
Generate per-page social-share (Open Graph) images for the LCA site.

Each page gets a unique 1200x630 PNG saved to /public/og/<slug>.png. The
Layout.astro template computes the right OG URL per page from the current
pathname.

Uses macOS system Georgia and Helvetica as web-safe stand-ins for Lora and
Poppins so the script runs without external font downloads.

Run manually:
  python3 scripts/generate-og.py

Or wire into the build with an npm script:
  "prebuild": "python3 scripts/generate-og.py"
"""
import os
from pathlib import Path
from typing import Optional
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parent.parent
OUT_DIR = ROOT / "public" / "og"
OUT_DIR.mkdir(parents=True, exist_ok=True)

# Canvas
W, H = 1200, 630

# Brand colors (matching --color-navy, --color-on-navy, --color-coral)
NAVY = (14, 45, 92)              # ~ oklch(0.27 0.10 261)
NAVY_DEEP = (8, 35, 73)          # ~ oklch(0.21 0.09 261)
CREAM = (254, 245, 239)          # ~ oklch(0.97 0.012 70)
CREAM_SOFT = (218, 209, 198)     # ~ on-navy-soft, slightly dimmed
CORAL = (255, 85, 94)            # ~ oklch(0.68 0.20 21)

# Real brand fonts, Lora variable + Poppins SemiBold. Downloaded from the
# google/fonts repo into scripts/fonts/ once; commit alongside this script.
FONTS = Path(__file__).resolve().parent / "fonts"
LORA_VAR = str(FONTS / "Lora-Variable.ttf")
LORA_ITALIC_VAR = str(FONTS / "Lora-Italic-Variable.ttf")
POPPINS_SEMIBOLD = str(FONTS / "Poppins-SemiBold.ttf")


def fnt(path: str, size: int, weight: Optional[int] = None) -> ImageFont.FreeTypeFont:
    """Load a TTF at the requested size. For variable fonts, optionally set
    the wght axis (Pillow >=10.0 supports `set_variation_by_axes`)."""
    f = ImageFont.truetype(path, size=size)
    if weight is not None and hasattr(f, "set_variation_by_axes"):
        try:
            f.set_variation_by_axes([weight])
        except (OSError, ValueError):
            pass  # not a variable font, ignore
    return f


def wrap_text(text: str, font: ImageFont.FreeTypeFont, max_width: int) -> list[str]:
    """Greedy word-wrap on a fixed pixel width."""
    words = text.split()
    lines: list[str] = []
    current = ""
    for w in words:
        trial = (current + " " + w).strip()
        bbox = font.getbbox(trial)
        width = bbox[2] - bbox[0]
        if width <= max_width or not current:
            current = trial
        else:
            lines.append(current)
            current = w
    if current:
        lines.append(current)
    return lines


def draw_card(out_path: Path, eyebrow: str, headline: str, sublabel: str = "") -> None:
    img = Image.new("RGB", (W, H), NAVY)
    draw = ImageDraw.Draw(img)

    # Subtle gradient suggestion: a darker band on the bottom third
    band = Image.new("RGB", (W, H // 3), NAVY_DEEP)
    img.paste(band, (0, H - H // 3))

    # Coral accent rule on the left edge
    draw.rectangle([(0, 0), (12, H)], fill=CORAL)

    # Padding
    pad_x = 80
    pad_y = 70

    # Eyebrow (small caps, coral)
    eyebrow_font = fnt(POPPINS_SEMIBOLD, 26)
    # Slight letter-spacing emulation: pad the string with a thin space; for
    # cleaner kerning we just rely on the font's natural metrics.
    draw.text((pad_x, pad_y), eyebrow.upper(), fill=CORAL, font=eyebrow_font)

    # Brand wordmark anchor, small, top-left, under eyebrow
    brand_font = fnt(POPPINS_SEMIBOLD, 22)
    brand_line = "THE LAY COUNSELOR ACADEMY  ·  SELF-PACED"
    draw.text((pad_x, pad_y + 46), brand_line, fill=CREAM_SOFT, font=brand_font)

    # Headline (Lora variable, large, wrapped)
    title_size = 88 if len(headline) < 80 else 74 if len(headline) < 110 else 62
    title_font = fnt(LORA_VAR, title_size, weight=400)
    line_height = int(title_size * 1.08)
    max_width = W - (pad_x * 2)
    lines = wrap_text(headline, title_font, max_width)

    # Vertically center the headline block in the middle band
    block_top = pad_y + 130
    for i, line in enumerate(lines):
        draw.text((pad_x, block_top + i * line_height), line, fill=CREAM, font=title_font)

    # Optional sublabel (Lora italic, smaller, below headline)
    if sublabel:
        sub_font = fnt(LORA_ITALIC_VAR, 30, weight=400)
        sub_y = block_top + len(lines) * line_height + 24
        draw.text((pad_x, sub_y), sublabel, fill=CREAM_SOFT, font=sub_font)

    # Footer: URL on the right, with a coral dot
    url = "thelaycounseloracademy.com"
    url_font = fnt(POPPINS_SEMIBOLD, 20)
    bbox = url_font.getbbox(url)
    url_w = bbox[2] - bbox[0]
    url_y = H - pad_y - 8
    url_x = W - pad_x - url_w
    # coral dot before url
    dot_r = 6
    draw.ellipse(
        [(url_x - 24, url_y + 8), (url_x - 24 + dot_r * 2, url_y + 8 + dot_r * 2)],
        fill=CORAL,
    )
    draw.text((url_x, url_y), url, fill=CREAM_SOFT, font=url_font)

    img.save(out_path, "PNG", optimize=True)
    print(f"  → {out_path.relative_to(ROOT)}")


# One card per page that's likely to be shared
PAGES = [
    {
        "slug": "home",
        "eyebrow": "Mental health counseling, for non-clinicians",
        "headline": "Learn to sit with someone who is suffering, without making it worse.",
    },
    {
        "slug": "curriculum",
        "eyebrow": "Curriculum",
        "headline": "Seven modules. Fourteen sessions. Seventy hours.",
        "sublabel": "Paced for evenings and weekends.",
    },
    {
        "slug": "pricing",
        "eyebrow": "Pricing",
        "headline": "Two ways to learn. Same craft.",
        "sublabel": "Self-Paced $1,200. Live cohort $5,500 over 14 weeks.",
    },
    {
        "slug": "faq",
        "eyebrow": "Frequently asked questions",
        "headline": "Straight answers about the program.",
        "sublabel": "Everything we get asked, in one place.",
    },
    {
        "slug": "contact",
        "eyebrow": "Get in touch",
        "headline": "Write to Angelica.",
        "sublabel": "Enrollment, organizational pricing, scholarships.",
    },
    {
        "slug": "reviews",
        "eyebrow": "Outside voices",
        "headline": "What people say about the work.",
        "sublabel": "Press coverage, the CHCF evaluation, graduate stories.",
    },
    {
        "slug": "teachers-elizabeth-morrison",
        "eyebrow": "Founder, Co-Creator",
        "headline": "Elizabeth Morrison",
        "sublabel": "PhD, LCSW, MAC. Twenty-five years of clinical practice.",
    },
    {
        "slug": "teachers-alli-moreno",
        "eyebrow": "Co-Creator",
        "headline": "Alli Moreno",
        "sublabel": "Flourish Counselor Emeritus. The lived practice of peer counseling.",
    },
    {
        "slug": "es-home",
        "eyebrow": "Consejería en salud mental, para no-clínicos",
        "headline": "Aprende a sentarte con alguien que sufre, sin empeorar las cosas.",
    },
]

print("Generating OG cards →")
for page in PAGES:
    out = OUT_DIR / f"{page['slug']}.png"
    draw_card(
        out,
        eyebrow=page["eyebrow"],
        headline=page["headline"],
        sublabel=page.get("sublabel", ""),
    )
print(f"\nDone. {len(PAGES)} cards in {OUT_DIR.relative_to(ROOT)}/")
