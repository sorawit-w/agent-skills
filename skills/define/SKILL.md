---
name: define
description: >
  Contextual definition and translation of a single word or phrase, resolved from the sentence
  or paragraph around it — the true in-context sense, not the dictionary default. The user
  names a target word/phrase and supplies surrounding text; this skill disambiguates the sense
  and explains it for a language learner (meaning, why this sense, register, etymology,
  related senses, difficulty), and can translate it contextually into another language.
  Triggers on "what does X mean here", "what does this word mean in this sentence", "define X
  in context", "meaning of X as used here", "translate just this word in context", or any
  word-sense / vocabulary / reading-comprehension request that supplies a target plus its
  context. Does NOT trigger on editing, creating, or syncing translation/locale files, adding
  a language to a product, or i18n JSON/YAML/TS keys — that is the `i18n` skill. Does NOT
  trigger on full-document translation, or a context-free dictionary lookup with no
  surrounding text.
instructions: |
  Load this skill when the user supplies (or can supply) a TARGET word or phrase AND the
  CONTEXT it appears in (a sentence or paragraph), and wants its meaning or a contextual
  translation of just that target.
  Do NOT load this skill for i18n/localization file work (use `i18n`), for translating an
  entire document, or for a plain dictionary definition with no context to disambiguate.
tags:
  - define
  - translation
  - word-sense-disambiguation
  - vocabulary
  - language-learning
  - comprehension
---

# define — Contextual Definition & Translation

A word's true meaning lives in its context. "Bank" by a river is not "bank" that holds
money; Thai "เอา" shifts sense with the verb beside it; an idiom means nothing if you
read it word by word. This skill takes a **target** (a word or phrase) plus the
**context** it sits in, resolves the sense the context selects, and explains it the way a
good language teacher would — then, on request, translates *just that target*
contextually into another language.

This is a **comprehension** tool, not a localization tool. For editing translation files,
adding locales, or syncing translation keys, use the sibling `i18n` skill. The two share
a cultural knowledge base (see [Locale & cultural nuance](#locale--cultural-nuance)) but
do different jobs: `i18n` *produces* localized strings; `define` *explains* a word in
context.

---

## Input contract

| Field | Required | Default |
|-------|----------|---------|
| **target** | yes | the word or phrase to define/translate |
| **context** | yes (for a true contextual answer) | the surrounding sentence or paragraph |
| **source language** | no | auto-detect from the context |
| **explanation language** | no | the language the user is writing in |
| **target language** (for translation) | no | only if the user asks to translate |
| **learner level** | no | inferred; difficulty reported as a CEFR band |

If the **context is missing or too thin to disambiguate**, do not silently pick one
sense. State the most likely sense, name the alternative(s), and ask for more context
only when it would materially change the answer.

---

## Core principle

**Resolve the sense the context selects — not the dictionary-default sense, and not a
word-for-word translation.** The disambiguating cue is part of the answer: a learner
learns more from *why* a word means what it does here than from the gloss alone.

---

## Workflow

1. **Identify** the target + context (+ source/explanation/target languages, + level if given).
2. **Disambiguate the sense** using the context:
   - **Polysemy** — when the target has several dictionary senses, pick the one the context supports.
   - **Idioms / collocations / phrasal verbs / fixed expressions** — detect multiword units and read them as a unit; warn against the literal reading.
   - **Figurative vs literal** — metaphor, hyperbole, irony/sarcasm (literal meaning ≠ intended meaning).
   - **Domain / jargon** — the legal, medical, technical, or slang sense when the context is in that domain.
   - **Named entities** — identify a proper noun as a referent; do not force a common-word definition onto it.
   - **Morphology** — lemmatize inflected forms; note what the inflection contributes grammatically.
3. **Produce the learner gloss** (include only the fields that earn their place):
   - **Contextual meaning** — plain-language definition of the sense *as used here*. Lead with this.
   - **Why this sense** — the specific cue in the surrounding text that selects it.
   - **Part of speech / grammatical role** in this sentence.
   - **Register & connotation** — formal/informal, polite/blunt, positive/negative, archaic/slang, regional.
   - **Etymology / roots** — only when it illuminates the meaning or aids memory (morphemes, origin).
   - **Related senses & near-synonyms** — senses it does *not* mean here; near-synonyms and how they differ.
   - **Difficulty** — CEFR band (A1–C2); "n/a" for proper nouns.
   - **Contextual translation** (only if a target language is requested) — the sense-appropriate rendering, not literal; flag when no clean equivalent exists.
   - **Example** — one fresh sentence reusing the same sense.
4. **Locale & cultural nuance** — see below.

---

## Locale & cultural engine (shared with `i18n`)

`define` and `i18n` run the **same cultural engine** — the per-locale teams and facts in
[`../i18n/references/locale-knowledge.md`](../i18n/references/locale-knowledge.md). The
only difference is the surface: `i18n` works on translation files in a coding project;
`define` answers inline, in chat. So when a target is culturally loaded, dialectal,
honorific, classical, or classifier-bearing, **load that reference and use the target
locale's team** — the `@native market copywriter`, `@cultural consultant`, dialect /
sociolinguistic / historical advisors — exactly as `i18n` would. They are what make a
contextual translation read natively and a gloss culturally true. Don't restate or fork
it.

Examples where it matters:
- A Japanese honorific verb (召し上がる vs 食べる) → the register difference *is* the answer.
- A Thai classifier in the context → name it; explain why the count needs it.
- A th-bupphe word (เพคะ, ออเจ้า) → flag the classical/Ayutthaya register, not a modern gloss.

---

## Review lenses

Two layers, reconciled toward the sense the context actually supports:

**1. The shared locale team (cultural engine).** For the target locale, simulate its team
from `locale-knowledge.md` — the same personas `i18n` uses (`@native market copywriter`,
`@cultural consultant`, and any dialect / sociolinguistic / historical advisor the locale
needs). This guarantees cultural authenticity and a native-sounding contextual translation.

**2. Comprehension lenses (define's layer on top).** What the translation team doesn't
specialize in — the learner-facing gloss:

- **@lexicographer** — sense inventory; picks the right sense; distinguishes near-synonyms.
- **@etymologist** — roots and morphology that make the meaning stick.
- **@register & pragmatics analyst** — formality, tone, connotation, social appropriateness.
- **@idiom & collocation detector** — flags multiword expressions; prevents literal misreading.

---

## Output format

Default to a **concise structured gloss**: lead with the one-line contextual meaning,
then the relevant fields trimmed to what matters for this target. Expand any field on
request. Don't pad — a clear A1 word needs three lines; a polysemous idiom in a sarcastic
sentence needs the full treatment.

---

## Edge cases & heuristics

- **Thin context** → give the most likely sense, name the alternative(s), and ask for more only if it changes the answer.
- **Genuinely two senses** → present both, ranked, each with the cue that would select it.
- **Sarcasm / irony** → state that the literal meaning differs from the intended one.
- **Slang / neologism** → flag volatility with `[shelf-life: short]` (same convention as `i18n`'s Gen Z variants).
- **Code-switching / loanwords** → identify the source language, then gloss in context.
- **Multi-word target** → treat a fixed expression as a unit; otherwise gloss head + modifiers.
- **Proper nouns / named entities** → identify the referent; don't define them as common words.

---

## What define does NOT do

- Editing, creating, or syncing translation files; adding locales; translation keys → use **`i18n`**.
- Full-document or article-length translation → out of scope.
- Context-free dictionary dumps → context is the whole point; ask for it.

---

## Cross-skill integration

| Skill | Relationship |
|-------|-------------|
| `i18n` | Shares `references/locale-knowledge.md`. `i18n` produces localized strings and translation files; `define` explains a word/phrase in context. Disjoint triggers — file/locale work → `i18n`, "what does this mean here" → `define`. |
| `team-composer` | For multi-perspective *discussion* when a definition or translation choice is contested or strategically loaded, rather than a single contextual gloss. |
