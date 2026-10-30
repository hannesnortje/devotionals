#!/usr/bin/env python3
"""Check the built website in docs/: broken internal links and slides that overflow.

Usage:  python3 build/check_site.py            (after build.py)
Exit code 1 if anything is wrong.
"""
import glob
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
DOCS = ROOT / "docs"
problems = []

os.chdir(DOCS)
pages = glob.glob("**/*.html", recursive=True)
for f in pages:
    for h in re.findall(r'(?:href|src)="([^"#:?]+)', open(f, encoding="utf-8").read()):
        if h.startswith(("http", "mailto", "data")):
            continue
        if not os.path.exists(os.path.normpath(os.path.join(os.path.dirname(f), h))):
            problems.append(f"broken link in {f}: {h}")
print(f"{len(pages)} pages checked for links")

from playwright.sync_api import sync_playwright  # noqa: E402
decks = sorted(glob.glob("*/*/slides-*.html"))
with sync_playwright() as p:
    b = p.chromium.launch()
    for vp in ({"width": 1280, "height": 720}, {"width": 1024, "height": 768}):
        for d in decks:
            pg = b.new_page(viewport=vp)
            pg.goto((DOCS / d).resolve().as_uri())
            over = pg.evaluate("""[...document.querySelectorAll('.slide')].map((s,i)=>{s.classList.add('active');
                const r=s.querySelector('.sl-inner');const o=r.scrollHeight>s.clientHeight*0.94;
                s.classList.remove('active');return o?i+1:0}).filter(Boolean)""")
            if over:
                problems.append(f"slides overflow in {d} at {vp['width']}x{vp['height']}: slide(s) {over}")
            pg.close()
    b.close()
print(f"{len(decks)} slide decks checked")
print("\n".join(problems) if problems else "OK – no problems")
sys.exit(1 if problems else 0)
