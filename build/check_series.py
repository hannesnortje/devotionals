#!/usr/bin/env python3
"""Check a devotional series before publishing.

Usage:  python3 build/check_series.py <slug> [--report FILE]

Errors (exit code 1): wrong structure – missing days, wrong headings or refs,
verse counts that don't match the base text, refs outside the translated text,
non-Greek letters inside Greek words, leftover progress tables or chat lines.
Warnings: words from older Bible translations (series.yml `avoid_words`) and
quotations that look like Bible quotes but don't match our translation exactly.
Warnings still need a human/agent look – they are not always wrong.
"""
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT / "build"))
from new_series import HEAD  # noqa: E402

LANGS = ["af", "de", "en"]
COMMON = {
    "af": ["Dieper Delf: Konteks en Betekenis", "Historiese, Kulturele en Literêre Konteks", None,
           "Teologiese Kernwaarhede", "Praktiese Toepassing", "Vrae vir Selfondersoek", "Gebed"],
    "de": ["Tiefer graben: Zusammenhang und Bedeutung", "Geschichtlicher, kultureller und literarischer Hintergrund", None,
           "Zentrale theologische Wahrheiten", "Für das Leben heute", "Fragen zur persönlichen Besinnung", "Gebet"],
    "en": ["Digging Deeper: Context and Meaning", "Historical, Cultural and Literary Background", None,
           "Core Theological Truths", "Living It Out", "Questions for Personal Reflection", "Prayer"],
}
LEFTOVERS = re.compile(r"Vorderingstabel|Fortschrittstabelle|Progress table|Hangende|Laat weet my|Let me know|Lass mich wissen|vervolg-studieplan|🟢|⚪", re.I)
CHAPTER = re.compile(r"^## (?:Kapitel|Chapter|Hoofstuk) (\d+)")
MARK = re.compile(r"\*\*(\d+)\*\*")
GREEK_WORD = re.compile(r"[Ͱ-Ͽἀ-῿][\ẁ-ͯͰ-Ͽἀ-῿]*")

errors, warnings = [], []


def err(msg): errors.append(msg)
def warn(msg): warnings.append(msg)


def front(path):
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", path.read_text(encoding="utf-8"), re.S)
    return (yaml.safe_load(m.group(1)), m.group(2)) if m else ({}, path.read_text(encoding="utf-8"))


def bible(sdir, slug, lang):
    """verse texts {(c, v): text} from the Markdown Bible file."""
    _, body = front(sdir / "bible" / f"{slug}-{lang}.md")
    verses, ch, cur = {}, 0, None
    for line in body.splitlines():
        m = CHAPTER.match(line)
        if m:
            ch = int(m.group(1)); continue
        if line.startswith("#") or not line.strip():
            continue
        content = line.lstrip("> ").strip()
        parts = MARK.split(content)
        if parts[0].strip() and cur:
            verses[cur] += " " + parts[0].strip()
        for i in range(1, len(parts), 2):
            cur = (ch, int(parts[i])); verses[cur] = parts[i + 1].strip()
    return verses


def source_verses(sdir):
    files = list((sdir / "source").glob("*-source.txt"))
    if not files:
        return None
    out = {}
    for line in files[0].read_text(encoding="utf-8").splitlines():
        ref, _, text = line.partition("\t")
        c, v = ref.split(":"); out[(int(c), int(v))] = text
    return out


def parse_ref(ref):
    a, b = ref.split("-")
    return tuple(map(int, a.split(":"))), tuple(map(int, b.split(":")))


def norm(s):
    s = re.sub(r"<[^>]+>|[*_`]", "", s).lower()
    s = re.sub(r"[^\w\s']", " ", s)
    return re.sub(r"\s+", " ", s).strip()


QUOTE = re.compile(r"„([^“\n]{12,}?)“|“([^”\n]{12,}?)”|\"([^\"\n]{12,}?)\"|(?<![*\w])\*([^*\n]{12,}?)\*(?![*\w])")


ALLOW = []   # filled from series/<slug>/check-allow.txt (reviewed, intentional wording)


def check_quotes(where, text, bible_norm, windows):
    for m in QUOTE.finditer(text):
        q = next(g for g in m.groups() if g)
        if any(a and a in q for a in ALLOW):
            continue
        q_clean = re.sub(r"\([^)]*\)|\[[^\]]*\]", " ", q)          # drop (transliterations) and [insertions]
        pieces = [norm(x) for x in re.split(r"…|\.\.\.", q_clean) if norm(x)]
        if pieces and all(f" {x} " in bible_norm or len(x.split()) < 3 for x in pieces):
            continue
        nq = norm(q_clean)
        words = nq.split()
        if len(words) < 5 or GREEK_WORD.search(q) or re.search(r"[֐-׿]", q):
            continue
        if nq in bible_norm:
            continue
        # does it look like a quote from our text (most words appear in one nearby passage)?
        qs = set(words)
        best = max((len(qs & w) / len(qs) for w in windows), default=0)
        if best >= 0.8:
            warn(f"{where}: near-quote not exact: “{q[:90]}”")


def main():
    if len(sys.argv) < 2:
        sys.exit(__doc__)
    slug = sys.argv[1]
    sdir = ROOT / "series" / slug
    conf = yaml.safe_load((sdir / "series.yml").read_text(encoding="utf-8"))
    ol = conf.get("original_language", "he")
    allow_file = sdir / "check-allow.txt"
    if allow_file.exists():
        ALLOW.extend(l.strip() for l in allow_file.read_text(encoding="utf-8").splitlines()
                     if l.strip() and not l.startswith("#"))
    src = source_verses(sdir)

    # ---- Bible files
    texts = {}
    for lang in LANGS:
        p = sdir / "bible" / f"{slug}-{lang}.md"
        if not p.exists():
            err(f"missing {p.relative_to(ROOT)}"); continue
        texts[lang] = bible(sdir, slug, lang)
    keysets = {l: set(v) for l, v in texts.items()}
    if keysets and len({frozenset(k) for k in keysets.values()}) > 1:
        err("Bible files don't contain the same verses in all languages: " +
            ", ".join(f"{l}={len(k)}" for l, k in keysets.items()))
    if src and keysets:
        some = next(iter(keysets.values()))
        extra = sorted(some - set(src))
        if extra:
            err(f"verses in our translation that are not in the base text: {extra[:8]}")
        chapters = {c for c, _ in some}
        missing = sorted(k for k in src if k[0] in chapters and k not in some)
        if missing:
            err(f"verses of translated chapters missing from our translation: {missing[:10]}")
    for lang, vs in texts.items():
        ch_counts = Counter(c for c, _ in vs)
        if src:
            sc = Counter(c for c, _ in src)
            for c, n in ch_counts.items():
                if sc.get(c) and sc[c] != n:
                    warn(f"{lang}: chapter {c} has {n} verses, base text {sc[c]} (partial chapter?)")

    # ---- devotionals
    heads = {l: [h if h else HEAD[ol][l] for h in COMMON[l]] for l in LANGS}
    avoid = conf.get("avoid_words") or {}
    days_by_lang = {}
    for lang in LANGS:
        files = sorted((sdir / lang).glob("[0-9][0-9]-*.md"))
        days_by_lang[lang] = {}
        vs = texts.get(lang, {})
        bnorm = " " + " ".join(norm(t) for _, t in sorted(vs.items())) + " "
        ordered = [norm(t) for _, t in sorted(vs.items())]
        windows = [set(" ".join(ordered[i:i + 3]).split()) for i in range(len(ordered))]
        for f in files:
            fm, body = front(f)
            rel = f.relative_to(ROOT)
            for k in ("day", "lang", "title", "ref"):
                if k not in fm:
                    err(f"{rel}: front matter lacks '{k}'")
            if fm.get("lang") != lang:
                err(f"{rel}: lang is {fm.get('lang')}")
            days_by_lang[lang][fm.get("day")] = fm.get("ref")
            hs = re.findall(r"^#{2,3} (.+)$", body, re.M)
            if hs != heads[lang]:
                err(f"{rel}: headings {hs} ≠ {heads[lang]}")
            if re.search(r"^# ", body, re.M):
                err(f"{rel}: has an H1 (the build adds the title)")
            if LEFTOVERS.search(body):
                err(f"{rel}: leftover from the original (progress table / chat line): {LEFTOVERS.search(body).group(0)}")
            try:
                a, b = parse_ref(fm.get("ref", ""))
                if vs and (a not in vs or b not in vs):
                    err(f"{rel}: ref {fm.get('ref')} not in our translation")
            except Exception:
                err(f"{rel}: ref '{fm.get('ref')}' is not c:v-c:v")
            for w in GREEK_WORD.findall(body):
                if re.search(r"[Ѐ-ӿ]", w):
                    err(f"{rel}: Greek word with Cyrillic letter: {w}")
            for w in avoid.get(lang, []):
                for m in re.finditer(re.escape(w), body, re.I):
                    line = body[:m.start()].count("\n") + 1
                    warn(f"{rel}:{line}: avoid-word “{w}”")
            if vs:
                check_quotes(str(rel), body, bnorm, windows)
    counts = {l: len(d) for l, d in days_by_lang.items()}
    if len(set(counts.values())) > 1:
        err(f"number of days differs per language: {counts}")
    for lang, d in days_by_lang.items():
        want = list(range(1, len(d) + 1))
        if sorted(k for k in d if isinstance(k, int)) != want:
            err(f"{lang}: day numbers are not 1..{len(d)}: {sorted(d)}")
    base = days_by_lang.get("de", {})
    for lang, d in days_by_lang.items():
        for n, r in d.items():
            if base.get(n) and base[n] != r:
                err(f"{lang} day {n}: ref {r} ≠ de {base[n]}")

    # ---- kit
    kit = {l: sorted((sdir / "kit" / l).glob("session-*.yml")) for l in LANGS}
    if any(kit.values()):
        if len({len(v) for v in kit.values()}) > 1:
            err(f"kit: different number of sessions per language: { {l: len(v) for l, v in kit.items()} }")
        for lang, files in kit.items():
            vs = texts.get(lang, {})
            bnorm = " " + " ".join(norm(t) for _, t in sorted(vs.items())) + " "
            ordered = [norm(t) for _, t in sorted(vs.items())]
            windows = [set(" ".join(ordered[i:i + 3]).split()) for i in range(len(ordered))]
            for f in files:
                try:
                    s = yaml.safe_load(f.read_text(encoding="utf-8"))
                except Exception as e:
                    err(f"{f.relative_to(ROOT)}: invalid YAML: {e}"); continue
                for k in ("session", "title", "ref", "big_idea", "opening", "context", "hebrew", "discussion", "application", "prayer", "leader_notes", "timing"):
                    if k not in s:
                        err(f"{f.relative_to(ROOT)}: missing '{k}'")
                if vs:
                    check_quotes(str(f.relative_to(ROOT)), f.read_text(encoding="utf-8"), bnorm, windows)

    # ---- report
    out = [f"# Check: {slug}", "", f"{len(errors)} error(s), {len(warnings)} warning(s)", ""]
    if errors:
        out += ["## Errors", ""] + [f"- {e}" for e in errors] + [""]
    if warnings:
        out += ["## Warnings (look at each)", ""] + [f"- {w}" for w in warnings]
    text = "\n".join(out)
    if "--report" in sys.argv:
        Path(sys.argv[sys.argv.index("--report") + 1]).write_text(text, encoding="utf-8")
    print(text if len(text) < 6000 else text[:6000] + "\n… (see report file)")
    sys.exit(1 if errors else 0)


if __name__ == "__main__":
    main()
