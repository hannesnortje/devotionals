#!/usr/bin/env python3
"""Create the folder structure for a new devotional series (as a draft).

Usage:  python3 build/new_series.py <slug> <he|grc> "<Book DE>" "<Book EN>" "<Book AF>"
        e.g. python3 build/new_series.py micha he "Micha" "Micah" "Miga"

Creates series/<slug>/ with series.yml (draft: true, placeholders to fill in),
CONVENTIONS.md (from the template in PLAYBOOK.md terms), DECISIONS.md, and empty
af/ de/ en/ bible/ kit/{af,de,en}/ source/ folders. Nothing is published until
`draft: true` is removed from series.yml.
"""
import sys
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
HEAD = {
    "he": {"af": "Insigte uit die Hebreeus", "de": "Einsichten aus dem Hebräischen", "en": "Insights from the Hebrew"},
    "grc": {"af": "Insigte uit die Grieks", "de": "Einsichten aus dem Griechischen", "en": "Insights from the Greek"},
}
LOOK = {
    "he": {"de": "Ein Blick ins Hebräische", "en": "A look at the Hebrew", "af": "'n Blik op die Hebreeus"},
    "grc": {"de": "Ein Blick ins Griechische", "en": "A look at the Greek", "af": "'n Blik op die Grieks"},
}
NOTE = {
    "he": {"de": "Bibeltext: eigene Übersetzung aus dem Hebräischen (Masoretischer Text) von Dr. Johannes A. Nortjé. Die Verszählung folgt dem hebräischen Text.",
           "en": "Scripture: own translation from the Hebrew (Masoretic Text) by Dr. Johannes A. Nortjé. Verse numbers follow the Hebrew text.",
           "af": "Skrifteks: eie vertaling uit die Hebreeus (Masoretiese Teks) deur Dr. Johannes A. Nortjé. Die versnommering volg die Hebreeuse teks."},
    "grc": {"de": "Bibeltext: eigene Übersetzung aus dem Griechischen von Dr. Johannes A. Nortjé. Grundtext: SBL Greek New Testament, © 2010 Society of Biblical Literature und Logos Bible Software (CC BY 4.0).",
            "en": "Scripture: own translation from the Greek by Dr. Johannes A. Nortjé. Base text: SBL Greek New Testament, © 2010 Society of Biblical Literature and Logos Bible Software (CC BY 4.0).",
            "af": "Skrifteks: eie vertaling uit die Grieks deur Dr. Johannes A. Nortjé. Grondteks: SBL Greek New Testament, © 2010 Society of Biblical Literature en Logos Bible Software (CC BY 4.0)."},
}


def main():
    if len(sys.argv) != 6 or sys.argv[2] not in HEAD:
        sys.exit(__doc__)
    slug, ol, de, en, af = sys.argv[1:]
    d = ROOT / "series" / slug
    if d.exists():
        sys.exit(f"{d} already exists")
    for sub in ["af", "de", "en", "bible", "source", "kit/af", "kit/de", "kit/en"]:
        (d / sub).mkdir(parents=True)
    order = 1 + max([yaml.safe_load((p / "series.yml").read_text()).get("order", 0)
                     for p in (ROOT / "series").iterdir() if (p / "series.yml").exists()] or [0])
    conf = {
        "slug": slug, "order": order, "draft": True, "original_language": ol,
        "site_url": f"https://hannesnortje.github.io/devotionals/{slug}/",
        "book": {"de": de, "en": en, "af": af},
        # words from older Bible translations that must not appear in this series (checked by check_series.py)
        "avoid_words": {"af": [], "de": [], "en": []},
        "strings": {
            "de": {"series_title": "TODO", "series_subtitle": f"TODO Andachten zum Buch {de}", "author": "Dr. Johannes A. Nortjé",
                   "whole_book": f"Das ganze Buch {de}", "whole_book_intro": f"Der vollständige Text des Buches {de} in der Übersetzung, die in diesen Andachten verwendet wird.",
                   "kit_intro": "TODO Treffen für Hauskreise und Kleingruppen – ein Treffen pro Kapitel, je 75 bis 90 Minuten.",
                   "k_hebrew": LOOK[ol]["de"], "translation_note": NOTE[ol]["de"]},
            "en": {"series_title": "TODO", "series_subtitle": f"TODO devotionals on {en}", "author": "Dr. Johannes A. Nortjé",
                   "whole_book": f"The whole book of {en}", "whole_book_intro": f"The complete text of {en} in the translation used in these devotionals.",
                   "kit_intro": "TODO sessions for home groups and small groups – one per chapter, 75 to 90 minutes each.",
                   "k_hebrew": LOOK[ol]["en"], "translation_note": NOTE[ol]["en"]},
            "af": {"series_title": "TODO", "series_subtitle": f"TODO oordenkings oor {af}", "author": "Dr. Johannes A. Nortjé",
                   "whole_book": f"Die hele boek {af}", "whole_book_intro": f"Die volledige teks van {af} in die vertaling wat in hierdie oordenkings gebruik word.",
                   "kit_intro": "TODO byeenkomste vir huisgroepe en kleingroepe – een per hoofstuk, elk 75 tot 90 minute.",
                   "k_hebrew": LOOK[ol]["af"], "translation_note": NOTE[ol]["af"]},
        },
    }
    (d / "series.yml").write_text("# Series settings – see PLAYBOOK.md\n" + yaml.safe_dump(conf, allow_unicode=True, sort_keys=False, width=1000), encoding="utf-8")
    h = HEAD[ol]
    (d / "CONVENTIONS.md").write_text(f"""# {en} series – conventions

General rules: see PLAYBOOK.md ("Writing rules"). Series-specific:

## Day plan (fill in from the Drive inventory)
| Day | ref | Source Google Doc ID |
|---|---|---|
| 01 | c:v-c:v | … |

## Headings (exactly)
| | AF | DE | EN |
|---|---|---|---|
| H2 | Dieper Delf: Konteks en Betekenis | Tiefer graben: Zusammenhang und Bedeutung | Digging Deeper: Context and Meaning |
| H3 | Historiese, Kulturele en Literêre Konteks | Geschichtlicher, kultureller und literarischer Hintergrund | Historical, Cultural and Literary Background |
| H3 | {h['af']} | {h['de']} | {h['en']} |
| H3 | Kern Teologiese Waarhede | Zentrale theologische Wahrheiten | Core Theological Truths |
| H2 | Praktiese Toepassing | Für das Leben heute | Living It Out |
| H3 | Vrae vir Persoonlike Selfondersoek | Fragen zur persönlichen Besinnung | Questions for Personal Reflection |
| H2 | Gebed | Gebet | Prayer |
""", encoding="utf-8")
    (d / "DECISIONS.md").write_text(f"# {en} – decisions\n\nRecord every decision Hannes makes for this series (date, what, why). Later sessions must not undo these.\n\n| Date | Decision |\n|---|---|\n", encoding="utf-8")
    print(f"Created {d} (draft). Next: fill in series.yml TODOs and CONVENTIONS.md day plan.")


if __name__ == "__main__":
    main()
