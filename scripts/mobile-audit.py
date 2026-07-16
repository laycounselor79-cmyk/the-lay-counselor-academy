"""Audit each route at iPhone-13 viewport. Find real mobile issues."""
import json
import subprocess
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
DIST = ROOT / "dist"
OUT_DIR = ROOT / "tmp-mobile-audit"
OUT_DIR.mkdir(exist_ok=True)
PORT = 4323
BASE = f"http://localhost:{PORT}"

ROUTES = [
    "/",
    "/pricing/",
    "/curriculum/",
    "/faq/",
    "/reviews/",
    "/contact/",
    "/accessibility/",
    "/teachers/elizabeth-morrison/",
    "/teachers/alli-moreno/",
    "/es/",
    "/es/pricing/",
    "/es/faq/",
]


def start_server():
    proc = subprocess.Popen(
        [sys.executable, "-m", "http.server", str(PORT), "--bind", "127.0.0.1"],
        cwd=str(DIST),
        stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL,
    )
    for _ in range(40):
        try:
            urllib.request.urlopen(BASE + "/", timeout=0.5)
            return proc
        except (urllib.error.URLError, ConnectionResetError):
            time.sleep(0.25)
    proc.terminate()
    raise RuntimeError("Server failed to start")


# Audit script run on each page
AUDIT_JS = """
() => {
    const issues = [];
    const viewportWidth = window.innerWidth;
    const docWidth = document.documentElement.scrollWidth;

    // 1. Horizontal overflow
    if (docWidth > viewportWidth + 1) {
        // find offenders
        const offenders = [];
        document.querySelectorAll('*').forEach(el => {
            const rect = el.getBoundingClientRect();
            if (rect.right > viewportWidth + 1 && rect.width > 50 && rect.width <= docWidth) {
                offenders.push({
                    tag: el.tagName.toLowerCase(),
                    cls: el.className && typeof el.className === 'string' ? el.className.slice(0, 80) : '',
                    id: el.id || '',
                    width: Math.round(rect.width),
                    right: Math.round(rect.right),
                    text: (el.textContent || '').slice(0, 60).trim(),
                });
            }
        });
        issues.push({
            type: 'overflow',
            docWidth,
            viewportWidth,
            offenders: offenders.slice(0, 8),
        });
    }

    // 2. Small touch targets
    const tappable = document.querySelectorAll('a, button, [role="button"], input[type="submit"], input[type="checkbox"], select');
    const smallTargets = [];
    tappable.forEach(el => {
        const rect = el.getBoundingClientRect();
        if (rect.width === 0 || rect.height === 0) return; // hidden
        if (rect.width < 36 || rect.height < 36) {
            smallTargets.push({
                tag: el.tagName.toLowerCase(),
                cls: el.className && typeof el.className === 'string' ? el.className.slice(0, 80) : '',
                w: Math.round(rect.width),
                h: Math.round(rect.height),
                text: (el.textContent || el.value || '').slice(0, 40).trim(),
                href: el.href ? new URL(el.href).pathname : '',
            });
        }
    });
    if (smallTargets.length) issues.push({ type: 'small_touch', count: smallTargets.length, samples: smallTargets.slice(0, 8) });

    // 3. Small font sizes (<14px in body content)
    const allTextEls = document.querySelectorAll('p, li, span, div, h1, h2, h3, h4, button, input, label');
    const smallFonts = new Map();
    allTextEls.forEach(el => {
        if (!el.textContent.trim()) return;
        const fs = parseFloat(window.getComputedStyle(el).fontSize);
        if (fs < 14) {
            const key = `${el.tagName.toLowerCase()}.${(el.className || '').toString().slice(0, 40)}`;
            if (!smallFonts.has(key)) smallFonts.set(key, { fontSize: fs, sample: el.textContent.slice(0, 40).trim() });
        }
    });
    if (smallFonts.size) {
        issues.push({
            type: 'small_font',
            count: smallFonts.size,
            samples: Array.from(smallFonts.entries()).slice(0, 6).map(([k, v]) => ({ selector: k, ...v })),
        });
    }

    // 4. Input font sizes (iOS zooms inputs <16px on focus)
    const inputs = document.querySelectorAll('input[type="email"], input[type="text"], input[type="tel"], input[type="search"], textarea');
    const zoomInputs = [];
    inputs.forEach(el => {
        const fs = parseFloat(window.getComputedStyle(el).fontSize);
        if (fs < 16) {
            zoomInputs.push({
                type: el.type || el.tagName.toLowerCase(),
                fontSize: fs,
                name: el.name || el.id || '',
            });
        }
    });
    if (zoomInputs.length) issues.push({ type: 'ios_zoom_input', inputs: zoomInputs });

    // 5. Page header height (sticky nav should not consume too much)
    const header = document.querySelector('header, .site-header, nav.site-nav');
    if (header) {
        const headerRect = header.getBoundingClientRect();
        if (headerRect.height > 90) {
            issues.push({ type: 'tall_header', height: Math.round(headerRect.height) });
        }
    }

    return {
        url: window.location.pathname,
        viewportWidth,
        docWidth,
        scrollHeight: document.documentElement.scrollHeight,
        issues,
    };
}
"""


def main():
    if not DIST.exists():
        raise SystemExit("dist/ not found. Run `npm run build` first.")
    proc = start_server()
    results = []
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch()
            # iPhone 13: 390 x 844, dpr 3
            context = browser.new_context(
                viewport={"width": 390, "height": 844},
                device_scale_factor=3,
                is_mobile=True,
                has_touch=True,
                user_agent="Mozilla/5.0 (iPhone; CPU iPhone OS 16_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.0 Mobile/15E148 Safari/604.1",
            )
            page = context.new_page()
            for route in ROUTES:
                print(f"Auditing {route}...")
                page.goto(BASE + route, wait_until="networkidle")
                page.wait_for_timeout(300)
                # Take screenshot for reference
                slug = route.strip("/").replace("/", "_") or "home"
                page.screenshot(path=str(OUT_DIR / f"{slug}.png"), full_page=True)
                # Run audit
                result = page.evaluate(AUDIT_JS)
                results.append(result)
            browser.close()
    finally:
        proc.terminate()
        proc.wait()

    # Write JSON results
    out = OUT_DIR / "audit.json"
    out.write_text(json.dumps(results, indent=2))
    print(f"\nResults: {out}")
    # Summary
    total_issues = sum(len(r["issues"]) for r in results)
    print(f"Pages: {len(results)}  Issues: {total_issues}")
    for r in results:
        if r["issues"]:
            print(f"\n  {r['url']}:")
            for issue in r["issues"]:
                print(f"    - {issue['type']}: {issue.get('count', '')} {issue.get('docWidth', '')} {issue.get('height', '')}")


if __name__ == "__main__":
    main()
