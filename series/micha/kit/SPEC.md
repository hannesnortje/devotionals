# Small-group kit – content spec

Seven sessions, one per chapter of Micah, each 75–90 minutes. They draw on the devotionals for those days.

| Session | ref | Devotional days |
|---|---|---|
| 1 | 1:1-1:16 | 1, 2 |
| 2 | 2:1-2:13 | 3, 4 |
| 3 | 3:1-3:12 | 5, 6 |
| 4 | 4:1-4:14 | 7, 8, 9 |
| 5 | 5:1-5:14 | 9, 10 |
| 6 | 6:1-6:16 | 11, 12 |
| 7 | 7:1-7:20 | 13, 14 |

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
- Quotes from Micah must match `bible/micha-{lang}.md` exactly. Key-word renderings from `bible/translation-notes.md`.
- Draw on the devotionals of those days (read them: `{lang}/NN-*.md`); don't invent new exegesis.
- Leader notes: practical (timing, where groups get stuck, a sensitive point to handle with care).

Micah specifics
- Word studies are Hebrew (field `hebrew` holds the Hebrew, pointed, as in the WLC).
- Verse numbering is Hebrew (4:14 = EN 5:1; 5:1–14 = EN 5:2–15). In EN files give the English number in brackets where it differs, e.g. "5:1 (English 5:2)"; DE/AF Hebrew numbers only.
- Day 9 (4:14–5:4) spans the chapter boundary: use it in sessions 4 and 5, focusing on the session's chapter.
- Divine name YHWH = HERR / LORD / HERE in small capitals as in the Bible files.
- Session 5 (5:1): Matthew 2:6 quotes it – fine to mention, but keep Hannes's Messianic reading as in day 9; leader notes may say Jewish readers understand it of a coming Davidic king.
- Session 7 closes the series (7:18 "Who is a God like you?" – the series title).
- Bible verses in discussion refs use the same numbering as our text.
