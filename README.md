# Devotionals · Andachten · Oordenkings

Devotional series by Dr. Johannes (Hannes) A. Nortjé in German, English and Afrikaans – as a website, A5 PDF booklets and small-group kits.

**Website:** https://hannesnortje.github.io/devotionals/

| Series | Website | Booklets | Small-group kit |
|---|---|---|---|
| Jona – *Unterwegs mit Jona / Journey through Jonah / Reis deur Jona* (10 days, own translation from the Hebrew) | [`/jona/`](https://hannesnortje.github.io/devotionals/jona/) | `docs/jona/pdf/jona-{de,en,af}.pdf` | `docs/jona/pdf/jona-kit-{lang}.pdf`, `jona-slides-{lang}.pdf` |
| 1 Timothy – *Treu im Haus Gottes / Faithful in God's Household / Getrou in God se Huis* (16 days, own translation from the Greek, SBLGNT) | [`/1tim/`](https://hannesnortje.github.io/devotionals/1tim/) | `docs/1tim/pdf/1tim-{de,en,af}.pdf` | `docs/1tim/pdf/1tim-kit-{lang}.pdf`, `1tim-slides-{lang}.pdf` |
| 2 Timothy – *Bis zum Ende treu / Faithful to the End / Getrou tot die Einde* (9 days, own translation from the Greek, SBLGNT) | [`/2tim/`](https://hannesnortje.github.io/devotionals/2tim/) | `docs/2tim/pdf/2tim-{de,en,af}.pdf` | `docs/2tim/pdf/2tim-kit-{lang}.pdf`, `2tim-slides-{lang}.pdf` |
| Hebrews – *Den Blick auf Jesus gerichtet / Eyes Fixed on Jesus / Die Oë op Jesus Gevestig* (28 days, own translation from the Greek, SBLGNT; 2:9 majority reading) | [`/hebr/`](https://hannesnortje.github.io/devotionals/hebr/) | `docs/hebr/pdf/hebr-{de,en,af}.pdf` | `docs/hebr/pdf/hebr-kit-{lang}.pdf`, `hebr-slides-{lang}.pdf` |
| Revelation – *Hinter den Kulissen / Behind the Curtain / Agter die Skerms* (31 days, own translation from the Greek, SBLGNT; days 10–31 written by Claude per WRITING-BRIEF.md) | [`/offb/`](https://hannesnortje.github.io/devotionals/offb/) | `docs/offb/pdf/offb-{de,en,af}.pdf` | `docs/offb/pdf/offb-kit-{lang}.pdf`, `offb-slides-{lang}.pdf` |
| Micah – *Wer ist ein Gott wie du? / Who Is a God Like You? / Wie is 'n God soos U?* (14 days, own translation from the Hebrew, WLC; Hebrew verse numbering) | [`/micha/`](https://hannesnortje.github.io/devotionals/micha/) | `docs/micha/pdf/micha-{de,en,af}.pdf` | `docs/micha/pdf/micha-kit-{lang}.pdf`, `micha-slides-{lang}.pdf` |
| Nahum – *Eine Zuflucht am Tag der Not / A Refuge in the Day of Distress / 'n Toevlug op die Dag van Nood* (6 days, own translation from the Hebrew, WLC; Hebrew verse numbering) | [`/nahum/`](https://hannesnortje.github.io/devotionals/nahum/) | `docs/nahum/pdf/nahum-{de,en,af}.pdf` | `docs/nahum/pdf/nahum-kit-{lang}.pdf`, `nahum-slides-{lang}.pdf` |
| Habakkuk – *Dennoch will ich jubeln / Yet I Will Rejoice / Tog sal ek Jubel* (6 days, own translation from the Hebrew, WLC) | [`/habakuk/`](https://hannesnortje.github.io/devotionals/habakuk/) | `docs/habakuk/pdf/habakuk-{de,en,af}.pdf` | `docs/habakuk/pdf/habakuk-kit-{lang}.pdf`, `habakuk-slides-{lang}.pdf` |
| Zephaniah – *Er jubelt über dich / He Rejoices over You / Hy Jubel oor Jou* (5 days, own translation from the Hebrew, WLC) | [`/zefanja/`](https://hannesnortje.github.io/devotionals/zefanja/) | `docs/zefanja/pdf/zefanja-{de,en,af}.pdf` | `docs/zefanja/pdf/zefanja-kit-{lang}.pdf`, `zefanja-slides-{lang}.pdf` |

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
- The start page is a catalogue in Bible order: a "Continue reading" card for the series in progress, then foldable shelves (Old/New Testament · group, e.g. Minor Prophets, Paul's letters) with one compact row per series (book, title, days, progress). Shelf and order come automatically from the book's OSIS code (`series/<slug>/source/<OSIS>-source.txt`, see `build/books.py`); group names are in `build/strings.py` (`shelf_*`). Each row opens the series overview, whose main button starts or continues the series and which offers "Already started?".
- Progress is shared across languages and stored only in the browser (`localStorage` key `dev-state`; folded shelves in `folded`). The ☰ menu on every page leads to the start page, all days of the current series, series in progress, "All series", language, legal page and "reset progress".
- Text size: the "Aa" button in the header (and the ☰ menu) has five steps (90–150 %). Only the reading area (`article.day`, CSS variable `--fs`) scales; header and buttons keep their size. Stored as `dev-state.fontSize` and applied by an inline script in `<head>` before the first paint.
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
