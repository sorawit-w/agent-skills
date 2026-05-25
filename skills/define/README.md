<p align="center">
  <img src="https://raw.githubusercontent.com/sorawit-w/agent-skills/main/assets/define-li.svg" alt="define — the true meaning of a word, from the sentence around it" width="100%"/>
</p>

# define

A Claude Code skill that does one thing well: tell you what a **word or phrase** means
*as it's used in a specific sentence or paragraph* — the true in-context sense, not the
dictionary default — and explain it the way a good language teacher would. It can also
translate just that target contextually into another language.

Think of the "Sider" select-and-define experience, minus the browser selection: you name
the target and give the surrounding text, and `define` resolves the sense, says *why*
that sense fits, and unpacks register, etymology, related senses, and difficulty.

## Why this exists

A dictionary gives you every sense of a word. Context picks one. "Bank" by a river isn't
the "bank" that holds money. "Run" in *run a business*, *run a fever*, and *run late* are
three different verbs wearing one spelling. An idiom read literally means nothing. Thai
"เอา" shifts meaning with the verb beside it; a Japanese honorific changes who's speaking
to whom.

A learner who only gets the gloss learns the gloss. A learner who gets *why this sense
fits here* learns to read. `define` is built for the second one — it treats the
disambiguating cue as part of the answer.

This is the comprehension half of a pair. Its sibling, [`i18n`](../i18n/README.md), is
the production half — it edits translation files and ships localized UI strings. They
share a cultural knowledge base but do opposite jobs: `i18n` *writes* a language; `define`
*reads* it.

## What it does

- **Resolves the in-context sense** of a target word or phrase from the surrounding sentence/paragraph — polysemy, idioms, phrasal verbs, figurative vs. literal, domain jargon, sarcasm.
- **Explains *why*** — names the specific cue in the text that selects the sense, so the next sentence is easier to read.
- **Gives a learner-grade gloss** — contextual meaning, part of speech, register & connotation, etymology/roots when useful, related senses & near-synonyms, and a CEFR difficulty band.
- **Translates contextually on request** — the sense-appropriate rendering into a target language, not a word-for-word swap, with a flag when no clean equivalent exists.
- **Handles culturally-loaded targets** — counter words, honorifics, dialect vocabulary, classical registers (e.g. th-bupphe ออเจ้า) — by reusing `i18n`'s shared locale knowledge.
- **Flags volatility** — slang and neologisms get a `[shelf-life: short]` note.

## What it doesn't do

- **Edit, create, or sync translation files**, add locales, or touch translation keys — that's [`i18n`](../i18n/README.md).
- **Translate whole documents or articles** — it's built for a target plus its context, not long-form prose.
- **Define out of context** — a context-free dictionary dump defeats the purpose; if there's no surrounding text, it asks for it.

## When to use it

- You're reading something in a second language and one word or phrase doesn't fit the meaning you know.
- You hit an idiom, a phrasal verb, or a figurative usage and a literal reading makes no sense.
- A word is polysemous and you want the sense *this* sentence intends — plus why.
- You want a contextual translation of one term, not the whole passage.
- You're studying vocabulary and want register, roots, near-synonyms, and a difficulty read, not just a one-line gloss.

## When not to use it

- You're shipping a product and need translation files edited or a locale added → [`i18n`](../i18n/README.md).
- You need a full document translated → a general translation pass, not this.
- You want a plain dictionary entry with no sentence to disambiguate → any dictionary.

## How it works

1. **Identify** the target and its context (auto-detecting the source language; noting the explanation/target language and any learner level).
2. **Disambiguate** the sense — checking polysemy, multiword expressions, figurative use, domain jargon, named entities, and inflection.
3. **Gloss it for a learner** — lead with the contextual meaning, then *why this sense*, part of speech, register, etymology where it helps, related senses, CEFR difficulty, and (if asked) a contextual translation plus a fresh example.
4. **Add cultural nuance** — for honorific, dialectal, classifier-bearing, or classical targets, consult the shared `i18n` locale knowledge.

Internally it reconciles a few comprehension lenses — lexicographer, etymologist, register/pragmatics analyst, idiom detector, and a locale cultural consultant — biased toward the sense the context actually supports.

## Design choices worth knowing

- **The cue is part of the answer.** `define` always says *why* a sense fits, not just *what* it means. That's the difference between a dictionary and a teacher.
- **Context is mandatory, not optional.** No surrounding text → it asks, rather than guessing the default sense.
- **It shares, doesn't fork.** Cultural facts (counter words, honorifics, dialects, classical registers) live in `i18n`'s `references/locale-knowledge.md`; `define` reads the same file. One source of truth.
- **Learner-framed by default.** Difficulty as CEFR, near-synonyms with distinctions, etymology when it aids memory — calibrated for someone learning, not just decoding.

## Install

This skill is distributed as a [Claude Code](https://docs.claude.com/en/docs/claude-code) plugin inside the [`sorawit-w/agent-skills`](https://github.com/sorawit-w/agent-skills) marketplace:

```
/plugin marketplace add sorawit-w/agent-skills
/plugin install agent-skills@sorawit-w
```

Once installed, Claude picks up the skill from its `SKILL.md` description. It triggers on phrases like "what does X mean here," "define this word in context," "what does this phrase mean in this sentence," or a request to translate just one term contextually.

## Cross-skill integration

| Skill | When it kicks in |
|---|---|
| [`i18n`](../i18n/README.md) | The production sibling. Shares `references/locale-knowledge.md`. Editing locale files / adding a language → `i18n`; "what does this word mean here" → `define`. |
| [`team-composer`](../team-composer/README.md) | When a definition or translation choice is contested or strategically loaded and benefits from multi-perspective discussion rather than a single gloss. |

## Status and scope

v0.1. A focused comprehension tool: contextual sense resolution + learner-grade glossing, with optional contextual translation.

- **Supported:** single word/phrase targets with surrounding context; polysemy, idiom, and figurative disambiguation; register, etymology, near-synonyms, CEFR difficulty; contextual translation; culturally-loaded targets via the shared locale knowledge.
- **Not supported:** translation-file/locale engineering (use `i18n`); full-document translation; context-free dictionary lookups.

## Contributions

Not accepting external contributions right now. Feel free to fork.

## License

MIT — see the [LICENSE](https://github.com/sorawit-w/agent-skills/blob/main/LICENSE) file at the repo root.
