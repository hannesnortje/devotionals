# Writing brief – devotionals written by Claude

Used when a series (or part of one) is written by Claude instead of being drafted by Hannes's Gemini Gem. Start of use: Revelation days 10–31 (6 Nov 2026). It combines Hannes's own Gem instructions (section 1, verbatim) with the conventions this project has learnt in the reviews (sections 2–5). Where they differ, sections 2–5 win; they only adapt the Gem brief to the website and to our own Bible translation.

## 1. Hannes's Gem instructions (verbatim, 6 Nov 2026)

> You are an expert, authentic Bible teacher and devotional writer. Your goal is to guide the user through deep, daily devotional journeys through books of the Bible or specific topics.
>
> **Devotional structure & length.** Each day's devotional must be detailed, rich, and comprehensive (approx. 600–1200 words / half to full A4 page). Structure every single daily output as follows:
> 1. Day [X]: [Engaging Title] – Scripture Reading: passage reference; quote the key Scripture passage in full.
> 2. Deeper Dive (Context & Meaning) – historical, cultural and literary context; original language insights (Greek/Hebrew word meanings) where applicable; break down the theological truths into clear, numbered or bulleted points.
> 3. Practical Application – connect the passage directly to daily modern life, struggles, mindset and choices; include probing, reflective questions for personal self-examination.
> 4. Prayer Focus – a rich, heartfelt, first-person prayer grounded in the truths of the daily passage.
>
> **Tone & style.** Authentic, warm, insightful, and reverent yet practical. Use strong formatting (bolding, headings, bullet points, blockquotes) for optimal scannability and structure.

(The Gem's chat workflow – study plan first, one day per prompt, progress table at the bottom, "let me know when you're ready" – is not used: the day plan is agreed with Hannes in advance and recorded in the series' CONVENTIONS.md.)

## 2. Form on the website

- One file per day and language, `series/<slug>/{lang}/NN-<slug-of-title>.md`, front matter `day`, `lang`, `title`, `ref` as in CONVENTIONS.md. No H1 and no printed passage – the build inserts the Bible text from our own translation.
- The seven headings exactly as in the series' CONVENTIONS.md (AF: *Dieper Delf: Konteks en Betekenis* – *Historiese, Kulturele en Literêre Konteks* – *Insigte uit die Hebreeus/Grieks* – *Teologiese Kernwaarhede* – *Praktiese Toepassing* – *Vrae vir Selfondersoek* – *Gebed*).
- Length about 900–1200 words of prose per day (Hannes, 6 Nov: keep the length of Revelation days 10–12).
- Language order: **Afrikaans first** (Hannes reviews the AF), then German and English translated from the AF, faithful in substance, natural in each language. German addresses the reader with **du**; Afrikaans with **jy**; God in prayers *U* (AF), *du* (DE), *you* (EN). AF possessives for God in lower case (*u*, *sy*), as in the other series.

## 3. Content – what makes a day "Hannes-like"

Taken from the series Hannes has approved (models: `series/micha/af/11-*`, `series/habakuk/af/04-*`, `series/hebr/af/`):

- **One central picture or question** carries the day (e.g. the beursie vol gate, the louwarm water of Laodicea). Open the context section by placing the reader in the original situation.
- **Historical, cultural, literary context:** 2–4 paragraphs, concrete (places, people, dates where known), and connected to what came the day before ("Gister het ons …").
- **Insights from the Hebrew/Greek:** 3–5 bullets. Each: *transliteration* (script) – meaning in our translation's wording – why it matters for the passage. Script exactly as in `series/<slug>/source/`; glosses consistent with the series' translation-notes §1.
- **Core theological truths:** 3–4 numbered points, each a bold one-line thesis plus 2–4 sentences. Christ-centred: show where the passage leads to Christ, the gospel and the church, as Hannes always does – but from the text, not forced.
- **Practical application:** 3–5 paragraphs, everyday and specific (work, family, money, fear, prayer, church), honest about struggle, always ending in grace and one concrete next step. No moralising, no fear-driven application.
- **Questions for self-examination:** 3–4, personal and searching, each tied to a verse.
- **Prayer:** first person, 2–3 italic paragraphs (one `*…*` block each): adoration from the passage – confession/struggle – trust and commitment; ends "Amen." (often "In Jesus se Naam").
- First day of a series opens with 1–2 sentences of welcome to the journey; the last day closes the series and links back to its title.

### Flow first
A day must read like one warm, clear piece, not like a list of everything that could be said. One central picture; background, word notes and truths all serve it. Series-level ideas (recorded in the series' CONVENTIONS.md) are lenses, not a checklist: use at most one or two per day, where the passage itself raises them, and never repeat them as slogans.

## 4. Accuracy rules (learnt from the reviews of the Gemini drafts)

- Quote the Bible **only from our own translation** (`series/<slug>/bible/<slug>-{lang}.md`) – word for word, or no quotation marks. Other books: our files where they exist (jona, micha, nahum, habakuk, zefanja, 1tim, 2tim, hebr); otherwise an own short rendering from the Hebrew/Greek, never Luther, 1933/53, 1983, KJV, ESV, NIV, NASB, CSB etc. Respect the series' `avoid_words`.
- Say only what can be supported. Hedge what is uncertain ("waarskynlik", "volgens baie uitleggers", "some think"). No "historians confirm", "literally means" unless it literally does, no invented etymologies or roots, no precise figures where sources differ, no anecdotes about famous people unless they are well attested.
- Ancient sources by name only when correctly cited (e.g. Tacitus, *Annals* 14.27 on Laodicea's rebuilding).
- Hebrew/Greek words: give the form that stands in the text; a dictionary form is marked as such ("from *qadam*").
- Hannes's theological positions as recorded in the series' DECISIONS.md and CONVENTIONS.md (e.g. Revelation: "for everyone, always" – first the seven churches, then us). Contested points: Hannes's position clearly, other readings in one fair sentence.

## 5. Checks before handing over

- `python3 build/check_series.py <slug>` – 0 warnings (quotations, avoid words).
- An independent review agent checks quotations, Hebrew/Greek, references, claims and the three languages against each other (as in PLAYBOOK.md §7).
- Hannes reviews the AF (review b) before publishing.
