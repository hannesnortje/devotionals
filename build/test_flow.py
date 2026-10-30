"""End-to-end test of the reading flow against a local server.

Run:  mkdir -p /tmp/serve && ln -sfn "$PWD/docs" /tmp/serve/devotionals
      (cd /tmp/serve && python3 -m http.server 8765 &)
      python3 build/test_flow.py /tmp/shots            # tests the first series on the start page
      python3 build/test_flow.py /tmp/shots 1tim       # tests a specific series
"""
import json
import re
import sys
from pathlib import Path
from playwright.sync_api import sync_playwright

BASE = "http://localhost:8765/devotionals/"
ROOT = Path(__file__).resolve().parent.parent
shots = Path(sys.argv[1] if len(sys.argv) > 1 else "/tmp/shots"); shots.mkdir(parents=True, exist_ok=True)
_home = (ROOT / "docs" / "home" / "de.html").read_text(encoding="utf-8")
_tiles = re.findall(r'data-series-tile="([^"]+)" data-total="(\d+)"', _home)
SLUG, TOTAL = (sys.argv[2], dict(_tiles)[sys.argv[2]]) if len(sys.argv) > 2 else _tiles[0]
TOTAL = int(TOTAL)
TILE = f'[data-series-tile="{SLUG}"] [data-tile-go]'
print(f"Testing series '{SLUG}' ({TOTAL} days)")
ok = []


def check(name, cond, extra=""):
    ok.append((name, bool(cond)))
    print(("PASS " if cond else "FAIL ") + name + (f"  [{extra}]" if extra else ""))


def path(pg):
    return pg.url.replace(BASE, "")


with sync_playwright() as p:
    b = p.chromium.launch()
    ctx = b.new_context(viewport={"width": 390, "height": 844}, device_scale_factor=2, locale="de-DE")
    pg = ctx.new_page()

    # 1 first visit -> German start page
    pg.goto(BASE); pg.wait_for_url("**/home/de.html")
    check("first visit lands on German start page", path(pg) == "home/de.html", path(pg))
    pg.screenshot(path=str(shots / "01-home-de.png"), full_page=True)
    check("tile says start", "Mit Tag 1 beginnen" in pg.inner_text(f'[data-series-tile="{SLUG}"]'))
    check("lost-progress link visible", pg.is_visible(".lost-wrap summary"))

    # 2 start the series
    pg.click(TILE); pg.wait_for_url(f"**/{SLUG}/de/tag-01.html")
    check("start goes to day 1", path(pg) == f"{SLUG}/de/tag-01.html")
    pg.screenshot(path=str(shots / "02-day1-top.png"))

    # 3 reload root before reading -> day 1 again
    pg.goto(BASE); pg.wait_for_url("**/tag-01.html")
    check("unread day 1 → root lands on day 1", path(pg).endswith("tag-01.html"))

    # 4 mark read -> stays; note appears
    pg.click(".mark-read"); pg.wait_for_timeout(100)
    check("button shows read", "Gelesen" in pg.inner_text(".mark-read"))
    check("tomorrow note visible", pg.is_visible("[data-read-note]"), pg.inner_text("[data-read-note]"))
    pg.locator(".read-row").scroll_into_view_if_needed()
    pg.screenshot(path=str(shots / "03-day1-read.png"))
    check("still on day 1 after marking", path(pg).endswith("tag-01.html"))

    # 5 same day: root still day 1
    pg.goto(BASE); pg.wait_for_url("**/tag-*.html")
    check("same day after reading → day 1", path(pg).endswith("tag-01.html"), path(pg))

    # 6 next day: shift the stored date back
    pg.evaluate("(slug) => { const s = JSON.parse(localStorage.getItem('dev-state')); s.progress[slug].last.date = '2000-01-01'; localStorage.setItem('dev-state', JSON.stringify(s)); }", SLUG)
    pg.goto(BASE); pg.wait_for_url("**/tag-02.html")
    check("next day → day 2", path(pg).endswith("tag-02.html"), path(pg))

    # 7 menu
    pg.click(".menu-btn"); pg.wait_for_timeout(350)
    check("menu opens", pg.is_visible("#drawer.open"))
    check("menu shows day 1 ticked", pg.locator('.drawer-days li[data-day="1"].read').count() == 1)
    check("continue link → day 2", pg.get_attribute("[data-continue]", "href").endswith("tag-02.html"))
    pg.screenshot(path=str(shots / "04-menu.png"))
    pg.keyboard.press("Escape"); pg.wait_for_timeout(300)
    check("menu closes with Esc", not pg.is_visible("#drawer.open"))

    # 8 switch language to English on day 2
    pg.click('header .langs a[lang="en"]'); pg.wait_for_url(f"**/{SLUG}/en/day-02.html")
    check("language switch keeps the day", path(pg) == f"{SLUG}/en/day-02.html")
    pg.goto(BASE); pg.wait_for_url(f"**/{SLUG}/en/day-*.html")
    check("language remembered + progress shared", path(pg) == f"{SLUG}/en/day-02.html", path(pg))

    # 9 deep link opens what it points to
    pg.goto(BASE + f"{SLUG}/de/tag-07.html")
    check("deep link opens day 7", path(pg) == f"{SLUG}/de/tag-07.html")
    pg.goto(BASE + "home/de.html")
    check("start page reachable", path(pg) == "home/de.html")
    check("tile says continue with day 2", "Weiter mit Tag 2" in pg.inner_text(TILE), pg.inner_text(TILE))
    pg.screenshot(path=str(shots / "05-home-continue.png"))

    # 10 finish the series -> completed page
    pg.evaluate("([slug, total]) => { const s = JSON.parse(localStorage.getItem('dev-state')); s.progress[slug].read = Array.from({length: total}, (_, i) => i + 1); s.progress[slug].last = {day: total, date: '2000-01-01'}; localStorage.setItem('dev-state', JSON.stringify(s)); }", [SLUG, TOTAL])
    pg.goto(BASE); pg.wait_for_url("**/done.html")
    check("all read → completed page", path(pg) == f"{SLUG}/de/done.html", path(pg))
    pg.screenshot(path=str(shots / "06-done.png"), full_page=True)
    pg.click("[data-restart]"); pg.wait_for_url("**/tag-01.html")
    st = json.loads(pg.evaluate("localStorage.getItem('dev-state')"))
    check("read again resets progress", st["progress"][SLUG]["read"] == [])

    # 11 lost progress: fresh browser, continue at day 5
    ctx2 = b.new_context(viewport={"width": 390, "height": 844}, locale="en-GB")
    pg2 = ctx2.new_page(); pg2.goto(BASE); pg2.wait_for_url("**/home/en.html")
    check("English browser → English start page", path(pg2) == "home/en.html")
    pg2.click(f'[data-series-tile="{SLUG}"] .lost-wrap summary'); pg2.select_option(f'[data-series-tile="{SLUG}"] [data-lost] select', "5"); pg2.click(f'[data-series-tile="{SLUG}"] [data-lost] button'); pg2.wait_for_url("**/day-05.html")
    check("lost-progress jumps to day 5", path(pg2) == f"{SLUG}/en/day-05.html")
    pg2.goto(BASE); pg2.wait_for_url("**/day-05.html")
    check("…and root continues there", path(pg2).endswith("day-05.html"))

    # 12 Afrikaans browser + migration from the old storage keys
    ctx3 = b.new_context(viewport={"width": 390, "height": 844}, locale="af-ZA")
    pg3 = ctx3.new_page(); pg3.goto(BASE + "home/af.html")
    pg3.evaluate("localStorage.clear(); localStorage.setItem('jona-read-af', '[1,2,3]')")  # migration only exists for jona
    pg3.goto(BASE); pg3.wait_for_url("**/dag-04.html")
    check("old progress migrated → day 4", path(pg3) == "jona/af/dag-04.html", path(pg3))

    # 13 legal page and desktop menu
    pg.goto(BASE + "legal/de.html"); pg.screenshot(path=str(shots / "07-legal.png"))
    check("legal page renders", "Impressum" in pg.inner_text("main"))
    d = b.new_context(viewport={"width": 1280, "height": 800}, locale="de-DE").new_page()
    d.goto(BASE + f"{SLUG}/de/tag-03.html"); d.screenshot(path=str(shots / "08-desktop-day.png"))
    d.click(".menu-btn"); d.wait_for_timeout(350); d.screenshot(path=str(shots / "09-desktop-menu.png"))
    d.goto(BASE + "home/de.html"); d.screenshot(path=str(shots / "10-desktop-home.png"))

    # 14 offline
    ctx4 = b.new_context(viewport={"width": 390, "height": 844}, locale="de-DE")
    pg4 = ctx4.new_page(); pg4.goto(BASE); pg4.wait_for_url("**/home/de.html")
    pg4.wait_for_function("navigator.serviceWorker && navigator.serviceWorker.controller !== null || (location.reload(), false)", timeout=15000) if False else None
    pg4.evaluate("navigator.serviceWorker.ready.then(() => true)")
    pg4.wait_for_timeout(2500)
    ctx4.set_offline(True)
    try:
        pg4.goto(BASE + f"{SLUG}/de/tag-06.html")
        check("works offline (day 6)", len(pg4.inner_text("main")) > 1500)
    except Exception as e:
        check("works offline (day 6)", False, str(e)[:80])
    b.close()

print(f"\n{sum(1 for _, c in ok if c)}/{len(ok)} checks passed")
