# Devotionals · Andachten · Oordenkings

Devotional series by Dr. Johannes A. Nortjé in German, English and Afrikaans – as a website, A5 PDF booklets and small-group kits.

**Website:** https://hannesnortje.github.io/devotionals/

| Series | Website | Booklets | Small-group kit |
|---|---|---|---|
| Jona – *Unterwegs mit Jona / Journey through Jonah / Reis deur Jona* (10 days, own translation from the Hebrew) | [`/jona/`](https://hannesnortje.github.io/devotionals/jona/) | `docs/jona/pdf/jona-{de,en,af}.pdf` | `docs/jona/pdf/jona-kit-{lang}.pdf`, `jona-slides-{lang}.pdf` |
| 1 Timothy – *Treu im Haus Gottes / Faithful in God's Household / Getrou in God se Huis* (16 days, own translation from the Greek, SBLGNT) | [`/1tim/`](https://hannesnortje.github.io/devotionals/1tim/) | `docs/1tim/pdf/1tim-{de,en,af}.pdf` | `docs/1tim/pdf/1tim-kit-{lang}.pdf`, `1tim-slides-{lang}.pdf` |

## Layout

| Path | What |
|---|---|
| `series/<slug>/series.yml` | Series settings: titles, book name, website address |
| `series/<slug>/bible/<slug>-{lang}.md` | Own Bible translation for the series (Hebrew verse numbering) |
| `series/<slug>/bible/translation-notes.md` | Key-word renderings and translation choices |
| `series/<slug>/{af,de,en}/NN-*.md` | Devotionals, one per day per language; the build inserts the Bible passage from `ref` |
| `series/<slug>/kit/{lang}/session-N.yml` | Small-group sessions (format: `series/jona/kit/SPEC.md`) |
| `series/<slug>/CONVENTIONS.md` | Writing conventions for the series |
| `build/` | `build.py` (website), `pdf.py` (PDFs), `strings.py` (interface text) |
| `site/` | Templates, styles and fonts shared by all series |
| `site/legal/legal.yml` | Imprint details (name, address, email) and licence text |
| `docs/` | Generated website (GitHub Pages) – don't edit by hand |

## How the site behaves

- `/` is a router: first-time visitors go to the start page in their browser's language (`/home/{lang}.html`); returning readers go straight to their next devotional.
- "Next" = the day just read stays on screen for the rest of that calendar day; from the next day on, the first unread day opens. When a series is finished, its "completed" page opens.
- Progress is shared across languages and stored only in the browser (`localStorage` key `dev-state`). The ☰ menu on every page leads to the start page, all days, other series, language, legal page and "reset progress".
- The site is installable ("Add to Home Screen") and works offline via `docs/sw.js`.

## Build

```bash
pip install markdown pyyaml jinja2 playwright
python -m playwright install chromium   # once
python3 build/build.py   # website → docs/
python3 build/pdf.py     # PDFs → docs/<slug>/pdf/
# test the reading flow: serve a folder containing devotionals → docs on :8765, then
python3 build/test_flow.py /tmp/shots
```

## Adding a series

**Full procedure: [PLAYBOOK.md](PLAYBOOK.md)** (and [CLAUDE.md](CLAUDE.md) for Claude sessions). Short version:

1. Copy `series/jona/` to `series/<new-slug>/` and empty the day, kit and Bible folders.
2. Edit `series.yml` (slug, order, book name, titles, site_url, `original_language: he` or `grc`). Keep `draft: true` until it is ready; `DRAFTS=1 python3 build/build.py` builds drafts locally.
3. Add the Bible translation as `bible/<new-slug>-{lang}.md`, the devotionals and (optionally) the kit sessions.
4. Run the build. The new series appears on the collection page automatically.

Fonts: Literata, Inter and Noto Serif Hebrew (SIL Open Font License), in `site/assets/fonts/`.

© Dr. Johannes A. Nortjé · Texts licensed under [CC BY-NC-ND 4.0](https://creativecommons.org/licenses/by-nc-nd/4.0/). Code (build scripts, templates) © Dr. Johannes A. Nortjé.
