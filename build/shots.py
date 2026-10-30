"""Screenshots of the built site for visual checks: python3 build/shots.py out_dir page..."""
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

ROOT = Path(__file__).resolve().parent.parent / "docs"
out = Path(sys.argv[1]); out.mkdir(parents=True, exist_ok=True)
pages = sys.argv[2:]
with sync_playwright() as p:
    b = p.chromium.launch()
    for scheme in ("light",):
        for name, vp in (("mobile", {"width": 390, "height": 844}), ("desktop", {"width": 1280, "height": 900})):
            ctx = b.new_context(viewport=vp, color_scheme=scheme, device_scale_factor=1)
            pg = ctx.new_page()
            for rel in pages:
                pg.goto((ROOT / rel).as_uri())
                pg.wait_for_timeout(300)
                fn = out / f"{rel.replace('/', '_').replace('.html', '')}-{name}.png"
                pg.screenshot(path=str(fn), full_page=(name == "mobile"))
            ctx.close()
    b.close()
print("ok")
