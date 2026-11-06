# Small-group kit – content spec

Eleven sessions on Revelation, each 75–90 minutes, one to three chapters each. They draw on the devotionals for those days.

| Session | ref | Devotional days |
|---|---|---|
| 1 | 1:1-1:20 | 1, 2 |
| 2 | 2:1-2:29 | 3, 4, 5, 6 |
| 3 | 3:1-3:22 | 7, 8, 9 |
| 4 | 4:1-5:14 | 10, 11 |
| 5 | 6:1-7:17 | 12, 13 |
| 6 | 8:1-9:21 | 14, 15 |
| 7 | 10:1-11:19 | 16, 17 |
| 8 | 12:1-13:18 | 18, 19 |
| 9 | 14:1-16:21 | 20, 21, 22 |
| 10 | 17:1-19:21 | 23, 24, 25, 26 |
| 11 | 20:1-22:21 | 27, 28, 29, 30, 31 |

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
- Quotes from Revelation must match `bible/offb-{lang}.md` exactly. Key-word renderings from `bible/translation-notes.md`.
- Draw on the devotionals of those days (read them: `{lang}/NN-*.md`); don't invent new exegesis.
- Leader notes: practical (timing, where groups get stuck, a sensitive point to handle with care).

Revelation specifics
- Word studies are Greek (field `hebrew` holds the Greek).
- Interpretive position (CONVENTIONS.md): "for everyone, always" – first what each vision meant for the seven churches, then what it means for us; 20:1–6 = Christ's present reign. Leader notes help groups where members hold other views (futurist, dispensational, preterist): name them fairly in a sentence, keep the focus on the book's pastoral message – God reigns, the Lamb has conquered, the church is called to faithful witness and endurance.
- Each session has at least one question that sends the group to the OT background of the passage ("the Old Testament in the New Testament").
- Avoid date-setting, decoding 666 to modern persons, or fear-driven application.
- Sessions 2 and 3 (the seven letters) let each group member take one church.
- Session 11 closes the series (22:20 "Amen. Come, Lord Jesus").
- Bible verses in discussion refs use the same numbering as our text.
