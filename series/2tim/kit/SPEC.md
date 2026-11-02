# Small-group kit – content spec

Four sessions, one per chapter of 2 Timothy, each 75–90 minutes. They draw on the devotionals for those days.

| Session | ref | Devotional days |
|---|---|---|
| 1 | 1:1-1:18 | 1, 2 |
| 2 | 2:1-2:26 | 3, 4, 5 |
| 3 | 3:1-3:17 | 6, 7 |
| 4 | 4:1-4:22 | 8, 9 |

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
- Quotes from 2 Timothy must match `bible/2tim-{lang}.md` exactly. Key-word renderings from `bible/translation-notes.md`.
- Draw on the devotionals of those days (read them: `{lang}/NN-*.md`); don't invent new exegesis.
- Leader notes: practical (timing, where groups get stuck, a sensitive point to handle with care).

2 Timothy specifics
- Word studies are Greek (field `hebrew` holds the Greek). AF uses "godsvrug" for eusebeia, "voorwerp (tot eer)" for skeuos.
- Session 1: 1:12 *parathēkē* is left open in our translation – leader notes may mention both readings without deciding.
- Session 3: 3:16 predicative ("Alle Schrift ist von Gott eingegeben und nützlich"); 3:6 *gynaikaria* – a leader note on handling it carefully (a judgment on particular people, not on women in general), following Hannes's Day 6.
- Session 4: 4:14 is a statement ("wird vergelten / will repay / sal vergeld"), not a curse; the session ends the series – Paul's last words.
- Bible verses in discussion refs use the same numbering as our text.
