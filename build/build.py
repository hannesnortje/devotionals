#!/usr/bin/env python3
"""Build the Jona devotional website (docs/) and booklet HTML (build/out/).

Usage: python3 build/build.py   (run from the repo root)
"""
import datetime
import html
import json
import re
import shutil
from pathlib import Path

import markdown
import yaml
from jinja2 import Environment, FileSystemLoader

from strings import LANGS, REF_SEP, STRINGS

ROOT = Path(__file__).resolve().parent.parent
SITE = ROOT / "site"
DOCS = ROOT / "docs"
OUT = ROOT / "build" / "out"
SERIES = None      # set per series in build(): dict from series/<slug>/series.yml + paths
BOOK = {}
YEAR = datetime.date.today().year
CHAPTER_WORDS = ("Kapitel", "Chapter", "Hoofstuk")

HEBREW_RUN = re.compile(r"[֐-׿יִ-ﭏ](?:[֐-׿יִ-ﭏ\s־]*[֐-׿יִ-ﭏ])?")


GREEK_RUN = re.compile(r"[\u0370-\u03FF\u1F00-\u1FFF](?:[\u0370-\u03FF\u1F00-\u1FFF\s\u0300-\u036F'’ʼ·]*[\u0370-\u03FF\u1F00-\u1FFF])?")


def wrap_hebrew(s: str) -> str:
    """Tag Hebrew (rtl) and Greek runs in text (outside tags)."""
    parts = re.split(r"(<[^>]+>)", s)
    out = []
    for p in parts:
        if p.startswith("<"):
            out.append(p); continue
        p = HEBREW_RUN.sub(lambda m: f'<span class="he" lang="he" dir="rtl">{m.group(0)}</span>', p)
        p = GREEK_RUN.sub(lambda m: f'<span class="gr" lang="grc">{m.group(0)}</span>', p) if not 'class="he"' in p else p
        out.append(p)
    return "".join(out)


DIVINE = re.compile(r"(?<![\w>])(HERRN|HERR|LORD|HERE)(?![\w<])")


def small_caps(s: str) -> str:
    """Render the divine name (HERR / LORD / HERE) in small capitals, outside tags."""
    parts = re.split(r"(<[^>]+>)", s)
    return "".join(p if p.startswith("<") else DIVINE.sub(r'<span class="sc">\1</span>', p) for p in parts)


def md_inline(text: str) -> str:
    out = markdown.markdown(text.strip())
    return re.sub(r"^<p>|</p>$", "", out)


def read_front_matter(path: Path):
    raw = path.read_text(encoding="utf-8")
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", raw, re.S)
    if not m:
        raise ValueError(f"No front matter in {path}")
    return yaml.safe_load(m.group(1)), m.group(2)


# ---------------------------------------------------------------- Bible text
def parse_bible(lang: str):
    """Return (meta, verses) where verses is an ordered list of dicts:
    {ch, v, kind: 'prose'|'poetry', parts: [str], para: bool}"""
    meta, body = read_front_matter(SERIES["dir"] / "bible" / f"{SERIES['slug']}-{lang}.md")
    verses, chapter, cur, new_para = [], 0, None, True
    marker = re.compile(r"\*\*(\d+)\*\*\s*")
    for line in body.splitlines():
        s = line.rstrip()
        if s.startswith("## "):
            if any(w in s for w in CHAPTER_WORDS):
                chapter = int(re.search(r"\d+", s).group())
                new_para = True
            continue
        if s.startswith("# ") or not s.strip():
            if not s.strip():
                new_para = True
            continue
        poetry = s.startswith(">")
        content = s.lstrip(">").strip()
        if not content:
            continue
        pieces = marker.split(content)
        # pieces: [pre, num, text, num, text, ...]
        if pieces[0].strip():
            if poetry and cur["kind"] == "prose":
                # a prose verse that continues as poetry (e.g. 2:3 "and said:")
                cur = {"ch": cur["ch"], "v": cur["v"], "kind": "poetry",
                       "parts": [pieces[0].strip()], "para": False, "cont": True}
                verses.append(cur)
            else:
                cur["parts"].append(pieces[0].strip())
        for i in range(1, len(pieces), 2):
            cur = {"ch": chapter, "v": int(pieces[i]), "kind": "poetry" if poetry else "prose",
                   "parts": [pieces[i + 1].strip()], "para": new_para}
            verses.append(cur)
            new_para = False
    return meta, verses


def parse_ref(ref: str):
    a, b = ref.split("-")
    ca, va = map(int, a.split(":"))
    cb, vb = map(int, b.split(":"))
    return (ca, va), (cb, vb)


def select(verses, ref):
    (ca, va), (cb, vb) = parse_ref(ref)
    return [x for x in verses if (ca, va) <= (x["ch"], x["v"]) <= (cb, vb)]


def ref_label(lang, ref):
    (ca, va), (cb, vb) = parse_ref(ref)
    sep = REF_SEP[lang]
    book = BOOK[lang]
    if ca == cb:
        return f"{book} {ca}{sep}{va}–{vb}"
    return f"{book} {ca}{sep}{va} – {cb}{sep}{vb}"


def render_passage(vs, show_chapter=False, chapter_word=""):
    """Render verses to HTML, grouping prose paragraphs and poetry blocks."""
    out, mode, last_ch = [], None, None

    def close():
        nonlocal mode
        if mode == "prose":
            out.append("</p>")
        elif mode == "poetry":
            out.append("</div>")
        mode = None

    for x in vs:
        if show_chapter and x["ch"] != last_ch:
            close()
            out.append(f'<h2 class="chapter" id="k{x["ch"]}">{chapter_word} {x["ch"]}</h2>')
            last_ch = x["ch"]
        num = "" if x.get("cont") else f'<sup class="vn">{x["v"]}</sup>'
        if x["kind"] == "prose":
            if mode != "prose" or x["para"]:
                close()
                out.append("<p>")
                mode = "prose"
            out.append(f'{num}{md_inline(" ".join(x["parts"]))} ')
        else:
            if mode != "poetry":
                close()
                out.append('<div class="poetry">')
                mode = "poetry"
            for i, part in enumerate(x["parts"]):
                out.append(f'<span class="line">{num if i == 0 else ""}{md_inline(part)}</span>')
    close()
    return small_caps("".join(out))


# ---------------------------------------------------------------- Devotionals
def fix_list_indent(text):
    """Python-Markdown needs 4 spaces for a nested list; the sources often use 2 or 3
    (as other Markdown renderers accept). Normalise so sub-lists render as lists."""
    return re.sub(r"^ {2,3}(?=(?:[-*+]|\d+\.) )", "    ", text, flags=re.M)


def load_days(lang):
    days = []
    for p in sorted((SERIES["dir"] / lang).glob("[0-9][0-9]-*.md")):
        meta, body = read_front_matter(p)
        html_body = markdown.markdown(fix_list_indent(body), extensions=["extra", "sane_lists"])
        html_body = small_caps(wrap_hebrew(html_body))
        # prayer: italic paragraphs inside the last H2 section get a class
        html_body = re.sub(r"(<h2>[^<]*</h2>)((?:\s*<p><em>.*?</em></p>)+)\s*$",
                           lambda m: m.group(1) + '<div class="prayer">' + m.group(2) + "</div>",
                           html_body, flags=re.S)
        days.append({
            "n": int(meta["day"]),
            "title": meta["title"],
            "ref": meta["ref"],
            "slug": f"{STRINGS[lang]['day'].lower()}-{int(meta['day']):02d}",
            "html": html_body,
            "src": p.name,
        })
    return days


# ---------------------------------------------------------------- Small-group kit
def chunk_verses(vs, limit=600):
    """Split a chapter into slide-sized chunks (by characters, never inside a verse)."""
    chunks, cur, size = [], [], 0
    for x in vs:
        # estimate screen lines: every part starts a new line (poetry lines, and the short prose lines
        # between quotations in books like Hebrews), long parts wrap at about 68 characters
        n = sum(68 * (-(-len(p) // 68)) for p in x["parts"]) + (28 * len(x["parts"]) if x["kind"] == "poetry" else 0)
        if cur and size + n > limit and not x.get("cont"):
            chunks.append(cur); cur, size = [], 0
        cur.append(x); size += n
    if cur:
        chunks.append(cur)
    return chunks


def ref_one(lang, r):
    c, v = r.split(":")
    return f"{BOOK[lang]} {c}{REF_SEP[lang]}{v}"


def load_kit(lang, verses):
    sessions = []
    for p in sorted((SERIES["dir"] / "kit" / lang).glob("session-*.yml")):
        s = yaml.safe_load(p.read_text(encoding="utf-8"))
        s["ref_label"] = ref_label(lang, s["ref"])
        s["slug"] = f"kit-{s['session']}"
        s["slides_slug"] = f"slides-{s['session']}"
        for q in s.get("discussion", []):
            if q.get("ref"):
                q["ref_label"] = ref_label(lang, q["ref"]) if "-" in str(q["ref"]) else ref_one(lang, str(q["ref"]))
        sel = select(verses, s["ref"])
        s["passage"] = render_passage(sel)
        chunks = []
        for ch in chunk_verses(sel):
            nums = [x for x in ch if not x.get("cont")]
            a, b = nums[0], nums[-1]
            chunks.append({"label": ref_label(lang, f"{a['ch']}:{a['v']}-{b['ch']}:{b['v']}"),
                           "html": render_passage(ch)})
        s["chunks"] = chunks
        def sc_all(o):
            if isinstance(o, str):
                return small_caps(o)
            if isinstance(o, list):
                return [sc_all(v) for v in o]
            if isinstance(o, dict):
                return {k: (v if k in ("ref", "slug", "slides_slug", "passage", "chunks", "hebrew") and isinstance(v, str) else sc_all(v)) for k, v in o.items()}
            return o
        for k in ("big_idea", "opening", "context", "prayer", "read_aloud_tip", "application", "leader_notes", "discussion", "hebrew"):
            if k in s:
                s[k] = sc_all(s[k])
        sessions.append(s)
    return sessions


# ---------------------------------------------------------------- Build
DAYWORD = {l: STRINGS[l]["day"].lower() for l in LANGS}


import os
INCLUDE_DRAFTS = os.environ.get("DRAFTS") == "1"


def series_dirs():
    """Series to build; series marked `draft: true` only with DRAFTS=1."""
    out = []
    for p in sorted((ROOT / "series").iterdir()):
        if not (p / "series.yml").exists():
            continue
        conf = yaml.safe_load((p / "series.yml").read_text(encoding="utf-8"))
        if conf.get("draft") and not INCLUDE_DRAFTS:
            continue
        out.append(p)
    return out


def series_osis(sdir: Path):
    src = sorted((sdir / "source").glob("*-source.txt"))
    return src[0].name[: -len("-source.txt")] if src else None


def load_catalog():
    from books import BOOKS, GROUP_ORDER
    cat = []
    for sdir in series_dirs():
        conf = yaml.safe_load((sdir / "series.yml").read_text(encoding="utf-8"))
        total = len(list((sdir / LANGS[0]).glob("[0-9][0-9]-*.md")))
        osis = conf.get("osis") or series_osis(sdir)
        b = BOOKS.get(osis, {"testament": "nt", "group": "general", "canon": 999})
        cat.append({"slug": conf["slug"], "order": conf.get("order", 99), "total": total,
                    "strings": conf["strings"], "book": conf.get("book", {}),
                    "testament": b["testament"], "group": b["group"], "canon": b["canon"]})
    cat.sort(key=lambda c: (c["canon"], c["order"]))
    return cat


def catalog_for(lang):
    return [{"slug": c["slug"], "total": c["total"], "title": c["strings"][lang]["series_title"],
             "subtitle": c["strings"][lang]["series_subtitle"], "book": c["book"].get(lang, c["slug"]),
             "testament": c["testament"], "group": c["group"]} for c in CATALOG]


def shelves_for(lang):
    """Catalog grouped for the start page: [(testament, group, [series…]), …] in canonical order."""
    out = []
    for c in catalog_for(lang):
        if out and out[-1][1] == c["group"]:
            out[-1][2].append(c)
        else:
            out.append((c["testament"], c["group"], [c]))
    return out


def dev_json(lang, root, series=None, day=None, total=None, page=None):
    return json.dumps({"root": root, "lang": lang, "series": series, "day": day, "total": total,
                       "page": page, "langs": LANGS, "dayword": DAYWORD,
                       "catalog": [{"slug": c["slug"], "total": c["total"]} for c in CATALOG]},
                      ensure_ascii=False)


CATALOG = []


def build_series(env, sdir: Path):
    global SERIES, BOOK
    conf = yaml.safe_load((sdir / "series.yml").read_text(encoding="utf-8"))
    SERIES = dict(conf, dir=sdir)
    BOOK = conf["book"]
    slug = conf["slug"]
    sdocs = DOCS / slug
    sout = OUT / slug
    sout.mkdir(parents=True, exist_ok=True)
    summary = {}
    for lang in LANGS:
        t = dict(STRINGS[lang], **conf["strings"][lang])
        bmeta, verses = parse_bible(lang)
        days = load_days(lang)
        for d in days:
            d["ref_label"] = ref_label(lang, d["ref"])
            d["passage"] = render_passage(select(verses, d["ref"]))
        whole = render_passage(verses, show_chapter=True, chapter_word=t["chapter"])
        all_t = {l: dict(STRINGS[l], **conf["strings"][l]) for l in LANGS}
        ctx = dict(t=t, lang=lang, langs=LANGS, strings=all_t, days=days, year=YEAR,
                   copyright=t["copyright"].format(year=YEAR), whole=whole, series=slug,
                   pdf_name=f"{slug}-{lang}.pdf", collection="../../index.html",
                   site_url=conf.get("site_url"), olang=conf.get("original_language", "he"))
        ctx["catalog_lang"] = catalog_for(lang)
        ldir = sdocs / lang
        ldir.mkdir(parents=True)
        web = dict(root="../../")
        total = len(days)

        def W(page=None, day=None, fname="index.html"):
            return dict(web, page=page, alt={l: f"../{l}/{fname}" for l in LANGS},
                        dev_json=dev_json(lang, "../../", slug, day, total, page))
        (ldir / "index.html").write_text(env.get_template("index.html").render(**ctx, **W("series")), encoding="utf-8")
        (ldir / "done.html").write_text(env.get_template("done.html").render(**ctx, **W("done", fname="done.html")), encoding="utf-8")
        (ldir / "book.html").write_text(env.get_template("bible.html").render(**ctx, **W("bible", fname="book.html")), encoding="utf-8")
        for i, d in enumerate(days):
            prev = days[i - 1] if i > 0 else None
            nxt = days[i + 1] if i + 1 < len(days) else None
            w = W("day", d["n"])
            w["alt"] = {l: f"../{l}/{DAYWORD[l]}-{d['n']:02d}.html" for l in LANGS}
            page = env.get_template("day.html").render(**ctx, **w, d=d, prev=prev, next=nxt)
            (ldir / f"{d['slug']}.html").write_text(page, encoding="utf-8")
        prt = dict(root=str(SITE) + "/")
        (sout / f"booklet-{lang}.html").write_text(env.get_template("booklet.html").render(**ctx, **prt), encoding="utf-8")
        sessions = load_kit(lang, verses)
        if sessions:
            days_by_n = {d["n"]: d for d in days}
            kctx = dict(ctx, sessions=sessions, days_by_n=days_by_n)
            (ldir / "kit.html").write_text(env.get_template("kit.html").render(**kctx, **W("kit", fname="kit.html")), encoding="utf-8")
            for s in sessions:
                (ldir / f"{s['slug']}.html").write_text(
                    env.get_template("session.html").render(**kctx, **W("kit", fname=s["slug"] + ".html"), s=s), encoding="utf-8")
                (ldir / f"{s['slides_slug']}.html").write_text(
                    env.get_template("slides.html").render(**kctx, **web, decks=[{"s": s, "chunks": s["chunks"]}]), encoding="utf-8")
            (sout / f"kit-{lang}.html").write_text(env.get_template("kit_print.html").render(**kctx, **prt), encoding="utf-8")
            (sout / f"slides-{lang}.html").write_text(
                env.get_template("slides.html").render(**kctx, **prt, decks=[{"s": s, "chunks": s["chunks"]} for s in sessions]),
                encoding="utf-8")
        summary[lang] = {"sessions": len(sessions), "days": len(days),
                         "verses": len({(x["ch"], x["v"]) for x in verses})}
    all_t = {l: dict(STRINGS[l], **conf["strings"][l]) for l in LANGS}
    (sdocs / "index.html").write_text(
        env.get_template("router.html").render(langs=LANGS, strings=STRINGS, root="../",
                                               dev_json=dev_json("de", "../", slug, None, None, "series-router")),
        encoding="utf-8")
    return conf, summary


def build():
    env = Environment(loader=FileSystemLoader(SITE / "templates"), autoescape=False)
    DOCS.mkdir(exist_ok=True)
    # wipe generated HTML but keep each series' pdf/ folder between builds
    for child in DOCS.iterdir():
        if child.is_dir() and (ROOT / "series" / child.name).is_dir():
            for sub in child.iterdir():
                if sub.name != "pdf":
                    shutil.rmtree(sub) if sub.is_dir() else sub.unlink()
        else:
            shutil.rmtree(child) if child.is_dir() else child.unlink()
    shutil.copytree(SITE / "assets", DOCS / "assets")
    (DOCS / ".nojekyll").write_text("")
    global CATALOG
    CATALOG = load_catalog()
    series_list, summary = [], {}
    for sdir in series_dirs():
        conf, summ = build_series(env, sdir)
        series_list.append(conf)
        summary[conf["slug"]] = summ
    series_list.sort(key=lambda c: c.get("order", 99))
    legal = yaml.safe_load((SITE / "legal" / "legal.yml").read_text(encoding="utf-8"))
    for sub in ("home", "legal"):
        (DOCS / sub).mkdir(exist_ok=True)
    for lang in LANGS:
        t = STRINGS[lang]
        base = dict(t=t, lang=lang, langs=LANGS, strings=STRINGS, year=YEAR, root="../", series=None, days=None,
                    catalog_lang=catalog_for(lang), shelves=shelves_for(lang), copyright=t["copyright"].format(year=YEAR))
        (DOCS / "home" / f"{lang}.html").write_text(env.get_template("home.html").render(
            **base, page="home", alt={l: f"{l}.html" for l in LANGS},
            dev_json=dev_json(lang, "../", page="home")), encoding="utf-8")
        (DOCS / "legal" / f"{lang}.html").write_text(env.get_template("legal.html").render(
            **base, page="legal", alt={l: f"{l}.html" for l in LANGS}, legal=legal,
            legal_date=datetime.date.today().strftime("%d.%m.%Y"),
            dev_json=dev_json(lang, "../", page="legal")), encoding="utf-8")
    (DOCS / "index.html").write_text(env.get_template("router.html").render(
        langs=LANGS, strings=STRINGS, root="", dev_json=dev_json("de", "", page="router")), encoding="utf-8")
    shutil.copy(SITE / "manifest.webmanifest", DOCS / "manifest.webmanifest")
    write_service_worker()
    print(json.dumps(summary))


def write_service_worker():
    """Offline support: precache every page and asset (PDFs are cached when first opened)."""
    import hashlib
    files = sorted(str(p.relative_to(DOCS)) for p in DOCS.rglob("*")
                   if p.is_file() and p.suffix != ".pdf" and p.name not in ("sw.js", ".nojekyll"))
    h = hashlib.sha1()
    for f in files:
        h.update(f.encode()); h.update((DOCS / f).read_bytes())
    version = h.hexdigest()[:10]
    urls = ["./"] + [f for f in files if not f.endswith("index.html") or f.count("/") > 0]
    js = (SITE / "sw.js").read_text(encoding="utf-8")
    js = js.replace("__VERSION__", version).replace("__FILES__", json.dumps(urls))
    (DOCS / "sw.js").write_text(js, encoding="utf-8")


if __name__ == "__main__":
    build()
