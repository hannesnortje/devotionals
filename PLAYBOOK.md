# Playbook: adding a new devotional series

This is the exact procedure used for Jona and 1 Timothy (30 Oct 2026). Follow it step by step in a new session. Every decision Hannes makes goes into `series/<slug>/DECISIONS.md` – a later session must not undo them.

**Roles.** Hannes writes the devotionals in Afrikaans (Google Docs in his Drive). Claude prepares German and English versions, an Afrikaans edition aligned with our own Bible translation, a small-group kit, PDFs, and publishes the series on https://hannesnortje.github.io/devotionals/.

**Hannes reviews twice:** (a) the Bible translation, before the devotionals are translated; (b) the list of content changes, before publishing. Optional (c): a sample day in DE/EN before the rest – only if Hannes asks for it.

**A series is published only when it is complete.** Until then `draft: true` stays in `series.yml`.

---

## 0. Prerequisites (check first)

- [ ] **Google Drive** is connected in this session (tools `mcp__Google_Drive__*`). Without it, stop and ask Hannes to connect it.
- [ ] **GitHub repo** `hannesnortje/devotionals` is attached with push access and cloned (in Claude Code on the web: `add_repo` with access "push", then `git clone`).
- [ ] Python packages: `pip install markdown pyyaml jinja2 playwright pypdf` (most are usually present); Chromium for Playwright (`python -m playwright install chromium` if missing).
- [ ] Read `CLAUDE.md`, this playbook, and one existing series (`series/1tim/`) as the model.

## 1. Inventory in Google Drive (don't rename or move Hannes's files)

The docs are in the Drive root and are named inconsistently ("Dag 3", "Gaan asseblief voort na Dag 14 …", "Please create a devotional …"). Several series are mixed together.

1. Search by the Afrikaans book name in the content, e.g. for Micah:
   `parentId = 'root' and fullText contains 'Miga'` (use `snippetVerbosity: BRIEF`).
   Each doc starts with `## Dag N: <Title>` and `Skriflesing: <Book> c:v–v`.
2. Build a table: Day | passage | title | doc ID | created. Watch for:
   - **duplicates** (same day twice – use the newest, mention it),
   - **gaps** (missing days – ask Hannes; he may add them to Drive),
   - **other series** mixed in (ignore),
   - passages that don't join up (overlaps/gaps between days).
3. Show the table to Hannes and confirm the day plan. Ask whether the series is **complete**.

## 2. Decisions to settle with Hannes (record in DECISIONS.md)

Propose sensible defaults; ask in one go:
- slug (short, lowercase, e.g. `micha`, `2tim`), OSIS book id (see `build/fetch_source.py`), original language `he` or `grc`;
- series titles DE/EN/AF (propose; Jona/1 Tim used a short evocative title + "N Andachten zum …");
- **whole book or only passages?** If only passages: translate only those (plus enough context); set `whole_book` / `whole_book_intro` in `series.yml` to "Die Abschnitte aus …" etc.;
- small-group kit: one session per chapter (default), or another split;
- anything contested in the book (e.g. 1 Tim 2:8–15) – translate literally, list options, Hannes decides;
- **verse numbering** (OT): always Hebrew numbering; English devotionals note the English number where it differs (Jona 2:1 = EN 1:17; Micah 4:14 = EN 5:1, 5:1 = EN 5:2; Joel 3–4 = EN 2:28–3:21; Malachi 3:19–24 = EN 4:1–6; Psalm titles count as v. 1 in Hebrew).

Constants (already decided, don't ask again): German uses **du**; DE/EN are freely adapted but faithful; divine name YHWH = HERR / LORD / HERE in small capitals (OT), NT "Herr/Lord/Here" normal case; quotes from other Bible books: short, own rendering; licence CC BY-NC-ND 4.0.

## 3. Scaffold

```bash
python3 build/new_series.py <slug> <he|grc> "<Book DE>" "<Book EN>" "<Book AF>"
python3 build/fetch_source.py <OSIS> <slug>      # base text → series/<slug>/source/<OSIS>-source.txt
```
Then fill in `series/<slug>/series.yml` (titles, subtitles, kit_intro – replace every TODO) and the day plan in `series/<slug>/CONVENTIONS.md` (Day | ref `c:v-c:v` | doc ID). Refs use the base-text (Hebrew/Greek) numbering.

## 4. Bible translation → Hannes review (a)

One agent (fork or general-purpose) with this brief:

> Translate <Book> (<chapters/passages>) from the <Hebrew/Greek> base text `series/<slug>/source/<OSIS>-source.txt` into German, English and Afrikaans, in the style and format of `series/1tim/bible/1tim-{de,en,af}.md` and `translation-notes.md` (read them first). Write `series/<slug>/bible/<slug>-{de,en,af}.md` (front matter lang/title/translation; `# <Book title>`; chapter headings exactly `## Kapitel N` / `## Chapter N` / `## Hoofstuk N`; verse markers `**n**`; poetry as `> ` lines) and `translation-notes.md` (§1 key-word table Hebrew/Greek | verses | DE | EN | AF, kept consistent through the book; §2 choices for Hannes with options; attribution of the base text). Close to the original, natural to read; German "du" where the text addresses one person; Afrikaans modern standard, NOT copying 1933/53 or 1983 wording; German NOT copying Luther. Keep the book's repeated key words the same each time. Translate contested passages literally and set out options instead of deciding. Verify verse counts per chapter against the base text. Reply with paths, counts, and the 5 most important choices for Hannes.

Send the three files + notes to Hannes. Apply his decisions, write them to DECISIONS.md, and fill `avoid_words` in `series.yml` with old-Bible wording that must not appear (e.g. 1933/53 or Luther terms for the book's key words).

## 5. Devotionals (parallel)

Split the days into batches of ~4 and run one agent per batch at the same time:

> Produce <Series> devotionals for days NN–MM in af, de, en, following `series/<slug>/CONVENTIONS.md` and the general writing rules in PLAYBOOK.md §11, and the approved Bible text `series/<slug>/bible/<slug>-{lang}.md` + `translation-notes.md` (+ DECISIONS.md). Read the source Google Docs with `mcp__Google_Drive__read_file_content` (doc IDs in CONVENTIONS.md). Use `series/1tim/{lang}/` as the quality and format model. Write `series/<slug>/{lang}/NN-<slug-of-title>.md`. Day 1 opens the series; the last day closes it. Do not touch other files. Reply with file paths and every content change you made beyond translation (facts corrected, claims softened, titles changed), one line each.

Collect all "content changes" lines – they go to Hannes in step 9 (b).

## 6. Small-group kit (parallel)

Copy `series/1tim/kit/SPEC.md` to `series/<slug>/kit/SPEC.md` and adapt the session table (ref, devotional days). Then 2–3 agents:

> Write <Series> small-group kit sessions X–Y in de, en, af per `series/<slug>/kit/SPEC.md`. Read the devotionals of those days and the Bible files; use `series/1tim/kit/{lang}/session-1.yml` as format model. Write `series/<slug>/kit/{lang}/session-N.yml`; validate YAML. Every quote from <Book> must match the Bible file word for word. Reply with paths and up to 3 issues.

(The field `hebrew` holds the Hebrew or Greek word; the templates use `original_language` from series.yml.)

## 7. Checks

1. Automatic: `python3 build/check_series.py <slug> --report /tmp/check.md` – fix every **error**. Look at each **warning**: fix real misquotations; add intentional ones (prayers, paraphrases, older readings quoted on purpose) as a line to `series/<slug>/check-allow.txt`.
2. Independent review (general-purpose agent, not a fork – fresh eyes):

> Review task, read-only except a report file. In `series/<slug>` are the devotionals (af/de/en) and our own Bible translation (bible/<slug>-{lang}.md, translation-notes.md §1), base text in source/. Check every devotional and kit file for: (1) quotations of <Book> that don't match that language's Bible file word for word – old wording from 1933/53, Luther, KJV/ESV is the main risk; (2) Hebrew/Greek words misspelled, with foreign letters, or transliteration not matching; glosses contradicting §1; (3) wrong verse references (Hebrew numbering); (4) leftovers: progress tables, batch labels, chat lines, day references that don't fit one N-day series; (5) the three languages disagreeing on substance. Write a table to `review/<slug>-quotes.md` (file | line | found | expected | type). Don't edit. Reply with counts per type.

3. One fork applies the fixes from the report (keeping Hannes's positions). Re-run `check_series.py`.

## 8. Build and test (still as draft)

```bash
DRAFTS=1 python3 build/build.py
mkdir -p /tmp/serve && ln -sfn "$PWD/docs" /tmp/serve/devotionals && (cd /tmp/serve && python3 -m http.server 8765 &)
python3 build/test_flow.py /tmp/shots <slug>      # reading flow, menu, language, completion, offline
```
Look at a few screenshots (mobile day page, start page) – e.g. with `build/shots.py`.

## 9. Report to Hannes (b)

Send: the list of content changes (step 5), anything open from the review, and the proposed titles. Optional (c): two sample days as PDF. Apply his answers; record in DECISIONS.md.

## 10. Publish

```bash
# remove the line "draft: true" from series/<slug>/series.yml
python3 build/build.py && python3 build/pdf.py && python3 build/check_site.py
python3 build/check_series.py <slug>
git add -A && git commit -m "Add <Book> series (DE/EN/AF)" && git push origin main
```
Update the series table in README.md. GitHub Pages publishes from `main` / `docs` within a minute or two; installed apps update themselves (service worker version changes with every build). Send Hannes the PDFs (booklets + one leader's guide) and the list from step 9.

---

## 11. Writing rules for devotionals (all series)

- One file per day per language: `series/<slug>/{lang}/NN-<slug>.md`, front matter `day`, `lang`, `title` (no "Tag N:" prefix), `ref` (`c:v-c:v`). No H1. No Bible passage in the file – the build inserts it from `ref`.
- Headings exactly as in `series/<slug>/CONVENTIONS.md` (seven headings; the originals sometimes lack sub-headings – split them).
- AF: keep Hannes's text; only align Bible quotations with our translation, fix formatting and day references, remove progress tables and chat lines.
- DE/EN: freely adapted but faithful – every point, word note, question and prayer line kept.
- Every quotation of the series' book matches our Bible text word for word; key words as in translation-notes §1.
- Hebrew/Greek as `*transliteration* – original script`; check spelling against the base text.
- Other Bible books: one verse at most, own rendering.
- **What may change:** factual errors (correct and report), claims stated more firmly than the evidence allows (soften and report), titles that no longer fit the translation (adjust and report). **What may not change:** Hannes's theological positions and the substance of his application and prayers.
- Prayers in italics, one paragraph per `*…*` block.

## 12. Things the build supports / doesn't

- Any number of days and sessions; Hebrew (rtl) and Greek; series ordered by `order` in series.yml.
- One Bible book per series. A topical series spanning several books would need a build change (ref format with book names).
- `DRAFTS=1` builds draft series locally; the published build skips them.
