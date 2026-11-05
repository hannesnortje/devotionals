# Small-group kit – content spec

Three sessions, one per chapter of Nahum, each 75–90 minutes. They draw on the devotionals for those days.

| Session | ref | Devotional days |
|---|---|---|
| 1 | 1:1-1:14 | 1, 2 |
| 2 | 2:1-2:14 | 2, 3, 4 |
| 3 | 3:1-3:19 | 5, 6 |

One YAML file per session per language: `kit/{lang}/session-{n}.yml` (UTF-8, block scalars where needed).

```yaml
session: 1
lang: de
title: "…"                 # short, e.g. "Auf der Flucht"
ref: "1:1-1:20"
days: [1, 2, 3]
big_idea: "…"              # one sentence: the main point of the session
opening: "…"               # icebreaker question, everyday, not churchy
context: "…"               # 2–3 sentences: where we are in the story, for reading aloud
read_aloud_tip: "…"        # one line on how to read the chapter aloud (e.g. roles)
hebrew:                    # 2–3 word studies from the devotionals
  - word: "pistos ho logos" # transliteration
    hebrew: "πιστὸς ὁ λόγος"  # (field name kept for the build: put the Greek here)
    gloss: "steh auf"      # our translation's rendering
    point: "…"             # 1–2 sentences
discussion:                # 6–7 questions, moving from text → meaning → life
  - q: "…"
    ref: "1:3"             # optional, Hebrew numbering
application:               # 2 concrete invitations for the week
  - "…"
prayer: "…"                # 2–3 sentences: prompt for praying together
leader_notes:              # 4–6 bullets for the leader
  - "…"
timing:                    # suggested minutes
  welcome: 10
  read: 10
  context: 10
  discussion: 40
  prayer: 15
```

Rules
- Same content in all three languages for a session (EN master in spirit, but each language natural; DE uses "du"/"ihr").
- Quotes from Nahum must match `bible/nahum-{lang}.md` exactly. Key-word renderings from `bible/translation-notes.md`.
- Draw on the devotionals of those days (read them: `{lang}/NN-*.md`); don't invent new exegesis.
- Leader notes: practical (timing, where groups get stuck, a sensitive point to handle with care).

Nahum specifics
- Word studies are Hebrew (field `hebrew` holds the Hebrew, pointed, as in the WLC).
- Verse numbering is Hebrew (2:1 = EN 1:15; 2:2–14 = EN 2:1–13). In EN files give the English number in brackets where it differs; DE/AF Hebrew numbers only.
- Day 2 (1:9–2:1) spans the chapter boundary: use it in sessions 1 and 2.
- Divine name YHWH = HERR / LORD / HERE in small capitals as in the Bible files.
- Nahum is a book of judgement on Nineveh: leader notes help groups handle God's vengeance (1:2) and the violent imagery with care, following Hannes's positions in the devotionals; link to Jonah (God's mercy to Nineveh) where the devotionals do.
- Session 3 closes the series.
