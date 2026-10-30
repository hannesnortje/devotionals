"""Render the print HTML in build/out/<series>/ to PDFs in docs/<series>/pdf/."""
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "build" / "out"
JOBS = [("booklet", ""), ("kit", "-kit"), ("slides", "-slides")]

with sync_playwright() as p:
    b = p.chromium.launch()
    pg = b.new_page()
    pg.emulate_media(media="print")
    for sout in sorted(d for d in OUT.iterdir() if d.is_dir()):
        slug = sout.name
        pdf_dir = ROOT / "docs" / slug / "pdf"
        pdf_dir.mkdir(parents=True, exist_ok=True)
        for lang in ("de", "en", "af"):
            for src_name, suffix in JOBS:
                src = sout / f"{src_name}-{lang}.html"
                if not src.exists():
                    continue
                pg.goto(src.as_uri())
                pg.evaluate("document.fonts.ready")
                pg.wait_for_timeout(400)
                dst = pdf_dir / f"{slug}{suffix}-{lang}.pdf"
                pg.pdf(path=str(dst), prefer_css_page_size=True, print_background=True)
                print(f"{slug}/pdf/{dst.name}", dst.stat().st_size // 1024, "KB")
    b.close()
