#!/usr/bin/env python3
"""Download the original-language base text of a Bible book for a series.

Usage:  python3 build/fetch_source.py <OSIS-book> <series-slug>
        e.g. python3 build/fetch_source.py Mic micha
             python3 build/fetch_source.py 2Tim 2tim

Old Testament: Westminster Leningrad Codex via the Open Scriptures Hebrew Bible
  (public domain text; morphology CC BY 4.0) – https://github.com/openscriptures/morphhb
New Testament: SBL Greek New Testament (CC BY 4.0, © 2010 Society of Biblical Literature
  and Logos Bible Software) – https://github.com/LogosBible/SBLGNT

Writes series/<slug>/source/<Book>-source.txt with one verse per line: "c:v<TAB>text"
(Hebrew: vowels kept, cantillation marks removed; Greek: SBL apparatus signs removed),
plus the raw download. Prints verse counts per chapter for checking.
"""
import re
import sys
import urllib.request
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path

OT = "Gen Exod Lev Num Deut Josh Judg Ruth 1Sam 2Sam 1Kgs 2Kgs 1Chr 2Chr Ezra Neh Esth Job Ps Prov Eccl Song Isa Jer Lam Ezek Dan Hos Joel Amos Obad Jonah Mic Nah Hab Zeph Hag Zech Mal".split()
NT = "Matt Mark Luke John Acts Rom 1Cor 2Cor Gal Eph Phil Col 1Thess 2Thess 1Tim 2Tim Titus Phlm Heb Jas 1Pet 2Pet 1John 2John 3John Jude Rev".split()
ROOT = Path(__file__).resolve().parent.parent


def fetch(url):
    with urllib.request.urlopen(url, timeout=60) as r:
        return r.read()


def hebrew(book):
    raw = fetch(f"https://raw.githubusercontent.com/openscriptures/morphhb/master/wlc/{book}.xml")
    ns = "{http://www.bibletechnologies.net/2003/OSIS/namespace}"
    lines = []
    for v in ET.fromstring(raw).iter(ns + "verse"):
        words = []
        for e in v.iter():
            if e.tag == ns + "w":
                t = "".join(e.itertext()).replace("/", "")
                words.append(re.sub("[֑-ֽ֯׀׃]", "", t))
        _, c, vv = v.get("osisID").split(".")
        lines.append(f"{c}:{vv}\t{' '.join(words)}")
    return raw, lines


def greek(book):
    raw = fetch(f"https://raw.githubusercontent.com/LogosBible/SBLGNT/master/data/sblgnt/text/{book}.txt")
    lines = []
    for line in raw.decode("utf-8").splitlines():
        m = re.match(r"^\S+ (\d+):(\d+)\t(.*)$", line)
        if m:
            text = re.sub("[⸀⸁⸂⸃⸄⸅]", "", m.group(3)).strip()
            lines.append(f"{m.group(1)}:{m.group(2)}\t{text}")
    return raw, lines


def main():
    if len(sys.argv) != 3:
        sys.exit(__doc__)
    book, slug = sys.argv[1], sys.argv[2]
    if book in OT:
        raw, lines = hebrew(book); ext = "xml"
    elif book in NT:
        raw, lines = greek(book); ext = "txt"
    else:
        sys.exit(f"Unknown OSIS book '{book}'. OT: {' '.join(OT)}\nNT: {' '.join(NT)}")
    out = ROOT / "series" / slug / "source"
    out.mkdir(parents=True, exist_ok=True)
    (out / f"{book}-raw.{ext}").write_bytes(raw)
    (out / f"{book}-source.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")
    counts = Counter(l.split(":")[0] for l in lines)
    print(f"{book}: {len(lines)} verses → {out}/{book}-source.txt")
    print("verses per chapter:", ", ".join(f"{c}:{n}" for c, n in counts.items()))


if __name__ == "__main__":
    main()
