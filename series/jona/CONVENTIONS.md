# Jona series – conventions for devotional files

## Files
- One file per day per language: `{lang}/{NN}-{slug}.md`, lang ∈ `af`, `de`, `en`, NN = 01…10.
- The Bible passage is NOT written in the devotional. The build inserts it from `bible/jona-{lang}.md` using `ref`.

## Day plan (Hebrew versification everywhere)
| Day | ref | Source Google Doc ID |
|---|---|---|
| 01 | 1:1-1:3 | 19X-PTJNJuZjHqAlSveDEwOxKOxTJlgDipiTNSf1eOEo |
| 02 | 1:4-1:10 | 1hYCoqpCkXbZt9JMArk0LoLJP2cfD7QiBGS9g9z7IYQI |
| 03 | 1:11-1:16 | 1lUWBaaM7e71wyF-S_JPGALvhcDjDNin89rYNbZhz0KE |
| 04 | 2:1-2:7 | 10SPNm1qN9T59woNN0dEbPe8NV-EBzQI3KqBSVARRvOc |
| 05 | 2:8-2:11 | 1AEVT8qJkbkbLqd7gpwJYvfUq-Egf2Gg39vhBSewlUAA |
| 06 | 3:1-3:4 | 1I3c5vFpE-nm7OYpmmvflYKlhJ1ANNEbzsR3djg5OFik |
| 07 | 3:5-3:10 | 19-RShtnd4zZ1MnV_VxusgMaXeOi9aRfgGV_gMeLEArY |
| 08 | 4:1-4:4 | 1YAQmhI4Hgjhu5xBN5RzUIAeDwHcPzjodhDL5dM1DZiM |
| 09 | 4:5-4:8 | 18dDCmaYu7s8mVgeyXy-s8Gfiea1rHpqflb9kt5iybEA |
| 10 | 4:9-4:11 | 14rqv20dQTgzLtQcwCLyLRi4FHE7HLSfJEywiYFYyxBE |

The originals were two series of five ("Dag 1–5" twice). Renumber as one series of 10 and fix any references ("gister se gedeelte", "Dag 3", "the end of our journey through chapters 1–2", etc.) so they make sense in a 10-day series.

## Front matter
```
---
day: 4
lang: de
title: "…"            # translated title, no "Tag 4:" prefix
ref: "2:1-2:7"
---
```

## Body structure (headings exactly)
| | AF | DE | EN |
|---|---|---|---|
| H2 | Dieper Delf: Konteks en Betekenis | Tiefer graben: Zusammenhang und Bedeutung | Digging Deeper: Context and Meaning |
| H3 | Historiese, Kulturele en Literêre Konteks | Geschichtlicher, kultureller und literarischer Hintergrund | Historical, Cultural and Literary Background |
| H3 | Insigte uit die Hebreeus | Einsichten aus dem Hebräischen | Insights from the Hebrew |
| H3 | Teologiese Kernwaarhede | Zentrale theologische Wahrheiten | Core Theological Truths |
| H2 | Praktiese Toepassing | Für das Leben heute | Living It Out |
| H3 | Vrae vir Selfondersoek | Fragen zur persönlichen Besinnung | Questions for Personal Reflection |
| H2 | Gebed | Gebet | Prayer |

No H1 (the build adds "Tag N: Title"). Drop the original progress table and any closing chat line ("Laat weet my …").

## Translation rules
- DE and EN: freely adapted but faithful. Every point, Hebrew note, question and prayer line kept; natural idiom; German addresses the reader as **du**.
- AF: keep the original text; only (a) fix formatting, (b) make every quotation of Jona match `bible/jona-af.md` exactly, (c) fix day references, (d) apply the rules below.
- Every quotation of Jona must match our own translation in `bible/jona-{lang}.md` word for word. Where a Hebrew note discusses a word, use the rendering from `bible/translation-notes.md` §1 (e.g. *qum* = Steh auf / Get up / Staan op; *yarad* = hinabsteigen / go down / afklim; *manah* = bestellen / appoint / beskik; *ra'ah* = Böses / evil / kwaad).
- Verse numbers follow the Hebrew. In EN, where chapter 2 is cited, add once per devotional: "(Hebrew numbering; English Bibles 1:17–2:10)" or the specific equivalent.
- Quotations from other Bible books: keep them short (one verse) and give your own rendering, NOT Luther 2017, 1933/53 or any other copyrighted translation.
- Divine name: HERR / LORD / HERE written as in the Bible files.
- Hebrew in the form: *transliteration* – Hebrew script, as in the Day 1 sample.
- Prayer in italics, one paragraph per `*…*` block.
