# Small-group kit – content spec

Thirteen sessions, one per chapter of Hebrews, each 75–90 minutes. They draw on the devotionals for those days.

| Session | ref | Devotional days |
|---|---|---|
| 1 | 1:1-1:14 | 1, 2 |
| 2 | 2:1-2:18 | 3, 4, 5 |
| 3 | 3:1-3:19 | 6, 7 |
| 4 | 4:1-4:16 | 8, 9 |
| 5 | 5:1-5:14 | 9, 10 |
| 6 | 6:1-6:20 | 10, 11, 12 |
| 7 | 7:1-7:28 | 13, 14 |
| 8 | 8:1-8:13 | 15 |
| 9 | 9:1-9:28 | 16, 17, 18 |
| 10 | 10:1-10:39 | 19, 20, 21 |
| 11 | 11:1-11:40 | 22, 23, 24 |
| 12 | 12:1-12:29 | 25, 26 |
| 13 | 13:1-13:25 | 27, 28 |

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
- Quotes from Hebrews must match `bible/hebr-{lang}.md` exactly. Key-word renderings from `bible/translation-notes.md`.
- Draw on the devotionals of those days (read them: `{lang}/NN-*.md`); don't invent new exegesis.
- Leader notes: practical (timing, where groups get stuck, a sensitive point to handle with care).

Hebrews specifics
- Word studies are Greek (field `hebrew` holds the Greek).
- Days 9 and 10 cover chapter boundaries (4:14–5:10, 5:11–6:3): use them for both sessions, focusing on the session's chapter.
- Decisions (DECISIONS.md): 2:9 "by the grace of God"; 9:16–17 "will/testament", elsewhere "covenant"; 11:11 Abraham is the subject; OT quotations as Hebrews has them (LXX). The author is unknown – never say "Paul wrote".
- Sessions 3, 6 and 10 (3:6/3:14, 6:4–6, 10:26–31): leader notes help leaders handle different convictions in the group respectfully; follow Hannes's positions as in those days' devotionals, don't add new ones.
- Session 13 closes the series.
- Bible verses in discussion refs use the same numbering as our text.
