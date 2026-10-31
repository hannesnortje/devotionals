# Devotionals – instructions for Claude

Website and booklets of devotional series by Dr. Johannes (Hannes) A. Nortjé (Hannes) in German, English and Afrikaans: https://hannesnortje.github.io/devotionals/

## Adding a new series
Follow **PLAYBOOK.md** step by step. Don't skip the two reviews by Hannes (Bible translation; list of content changes). Record every decision in `series/<slug>/DECISIONS.md`.

## Rules that must never be broken
- **Bible text is our own translation** from the Hebrew (WLC) or Greek (SBLGNT) – never paste Luther, 1933/53, 1983, ESV, NIV etc. (copyright). Quotations in devotionals and kit must match `series/<slug>/bible/<slug>-{lang}.md` word for word.
- **Respect DECISIONS.md** of each series (e.g. 1 Tim: AF "godsvrug"; Jona: "komkommerplant").
- **Hannes's theological positions stay as he wrote them.** Factual corrections are allowed but must be reported to him.
- **Don't rename, move or edit Hannes's Google Docs.** Read only.
- **Publish a series only when it is complete** (`draft: true` in series.yml until then).
- German addresses the reader with **du**.
- Don't edit `docs/` by hand – it is generated (`python3 build/build.py`, `python3 build/pdf.py`).
- Imprint details live in `site/legal/legal.yml`; texts are CC BY-NC-ND 4.0.

## Commands
```bash
python3 build/build.py                 # website → docs/   (DRAFTS=1 to include drafts)
python3 build/pdf.py                   # booklets, leader's guides, slides → docs/<slug>/pdf/
python3 build/check_series.py <slug>   # structure + quotations of one series
python3 build/check_site.py            # links + slide overflow of the built site
python3 build/test_flow.py /tmp/shots [<slug>]   # browser test (needs local server, see file header)
python3 build/new_series.py …          # scaffold a series (see PLAYBOOK.md)
python3 build/fetch_source.py <OSIS> <slug>      # download Hebrew/Greek base text
```

## Where things are
- `series/<slug>/` – everything of one series (series.yml, bible/, af|de|en/, kit/, source/, CONVENTIONS.md, DECISIONS.md, check-allow.txt)
- `build/` – scripts; `build/strings.py` – interface text in three languages
- `site/` – templates, CSS/JS, fonts, service worker, legal page settings
- Reading flow (landing → next devotional, progress, menu, offline app): see README.md "How the site behaves".
