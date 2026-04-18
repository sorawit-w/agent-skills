<p align="center">
  <img src="https://raw.githubusercontent.com/sorawit-w/agent-skills/main/assets/i18n-contextual-rewriting-li.svg" alt="i18n-contextual-rewriting — surgical edits, cultural rewrites" width="100%"/>
</p>

# i18n-contextual-rewriting

A Claude Code skill for working with internationalization files the way a careful localization engineer would — surgical edits on large translation files, and translations that feel like they were written by someone who lives in the market, not machine-converted from English.

## Why this exists

Two failure modes kill i18n work done by LLMs.

The first is **blowing up on file size**. Production translation files routinely carry thousands of keys. Ask a model to "add these five strings to `en.json`" and it will cheerfully rewrite the entire file, truncate at the output limit, and ship you a half-file with silently dropped keys. The fix is boring and load-bearing: never rewrite the whole file, target only the affected lines, and reach for a script when the edit is genuinely bulk.

The second is **word-for-word translation dressed as localization**. Machine-converted `zh-CN → zh-TW` looks Traditional but reads as mainland text in different clothes. A mechanical Thai translation omits counter words and sounds like a textbook. A German string overflows the button. These aren't edge cases — they are what happens every time "translate" is treated as string substitution instead of *contextual rewriting inside cultural reality*.

This skill encodes both halves: the file-handling discipline and a role-based review pass that runs before any translation ships.

## What it does

- **Refuses to rewrite large translation files in full.** Surgical edits only — target the affected lines, leave the rest alone. Full-file writes are allowed for genuinely new locales and small files, nothing else.
- **Uses scripts for bulk operations.** Adding 50+ keys, restructuring namespaces, syncing across all locales — the skill writes a one-off script that reads, merges without overwriting, and writes back. Not a manual pass through 14 files.
- **Handles JSON, YAML, TypeScript, and JS formats** — including the TS-specific cases where `as const` / `satisfies` annotations must be preserved after a round-trip.
- **Runs a multi-role translation review per locale.** Every language gets at least a native market copywriter, a cultural consultant, and a specialist reviewer. Their feedback is reconciled with bias toward clarity and cultural fit.
- **Knows the pluralization category per language.** Japanese / Korean / Thai / Chinese → no plural forms. English / French / German / Italian / Spanish → `one` / `other`. The skill doesn't generate plural keys a language doesn't use.
- **Flags counter words as mandatory.** Thai (ลักษณนาม), Japanese (助数詞), Korean (분류사), Chinese (量词) — quantities without classifiers sound unnatural to native speakers, so the skill does not omit them.
- **Treats `zh-CN → zh-TW` as a retranslation, not a character swap.** OpenCC and friends are rejected as a shipping path — vocabulary, idiom, and register diverge at a level no automated pass captures.
- **Ships ready-to-use teams for 15+ locales and variants.** Standard languages plus culturally-specific sub-variants: `en-genz`, `th-genz`, `th-isan`, `th-lanna`, `th-south`, `th-bupphe` (Ayutthaya classical), `zh-CN`, `zh-TW`, `zh-HK`.
- **Has a template for adding more.** Minimum team per language is three roles; the skill names the optional roles you may need (internet culture insider, sociolinguistic consultant, RTL reviewer, historical language consultant, and so on).

## It's opinionated about what "localized" means

Some defaults worth naming up front, because they shape the output:

- **Machine conversion isn't localization.** If you ask the skill to "just run OpenCC on the zh-CN file to make zh-TW," it will push back before doing it. Accepted only as a draft starting point, flagged as unshippable, and only with a retranslation pass queued behind it.
- **Cultural consultant is not optional.** Every locale team includes one. Monarchy / religious / hierarchy sensitivities in Thai, GDPR-ingrained privacy expectations in German, regional variant policy in Spanish, Académie Française norms in French — these are not style preferences, they are failure modes if ignored.
- **Slang has a shelf life.** Gen Z variants (`en-genz`, `th-genz`) flag volatile slang with `[shelf-life: short]` so it gets reviewed on a cycle. "555+" was fine five years ago. It isn't now.
- **Register is a product decision, not a per-string decision.** du vs. Sie, tu vs. vous, tu vs. Lei, 합니다 vs. 해요, formal vs. casual Japanese, 書面語 vs. written Cantonese — the skill expects a product-level register policy, then applies it consistently.
- **Some tech terms should stay in transliterated English.** "อีเมล" not "ไปรษณีย์อิเล็กทรอนิกส์". "다운로드" not a forced Korean equivalent. The skill defaults to established platform conventions rather than inventing purist alternatives.

If you want a neutral translate-these-strings service that takes the English as gospel and converts the characters, this isn't it.

## When to use it

- Editing an existing translation file with more than a few hundred keys — and you want the edit to actually land without file truncation.
- Adding a new locale to a product and you want the first draft to not sound like it came out of a translation memory.
- Syncing new keys across every locale file after a feature ships.
- Reviewing existing translations before a launch — especially when a variant is launching (Taiwan after Mainland, Gen Z after standard, regional Thai after Central).
- Producing translations in culturally-weighted variants: Thai regional dialects, Ayutthaya-era classical Thai, Hong Kong Cantonese-written register, Gen Z voices.
- Writing i18n helper scripts where type-annotated TS files (`as const`, `satisfies`) have to survive a round-trip.

## When not to use it

- **One-shot machine translation** where the brief is literally "translate this English sentence, I'll post-edit." A direct translation is fine; you don't need a multi-role pass.
- **RTL layout work itself.** The skill names RTL reviewers as an optional role, but laying out Arabic / Hebrew / Urdu in the UI is an engineering concern, not this skill's scope.
- **Non-user-facing strings** — error codes, log messages, ops output. Not where cultural fit earns its keep.
- **Markdown or prose translation** at article length. The skill is built for UI strings and translation files, not blog posts.
- **OpenCC / character-conversion requests** where the user refuses a retranslation pass. The skill will still produce the draft, but flagged as unshippable. If that's not acceptable, use a conversion library directly.

## How it works

1. **Part 1 — File handling runs first.** On any edit to an existing translation file, the skill checks file size and change volume. Small change + small file → surgical edit. Big change → one-off script that merges without overwriting. Full-file rewrite only for new locales.
2. **TS files get special handling.** Dynamic import when structure is simple, `ts-morph` AST manipulation when `as const` / `satisfies` must be preserved exactly, regex insertion for trivial appends.
3. **Part 2 — Translation pass runs per locale.** The skill identifies the target locale (including sub-variant — `th` ≠ `th-genz` ≠ `th-isan`), drafts an initial translation, and routes it through that locale's team.
4. **Team composition is minimum three, more as needed.** Native market copywriter + cultural consultant + specialist reviewer (dialect, digital-native, historical, inclusivity, etc., depending on the variant).
5. **Pluralization category is applied before key generation.** The skill does not emit `one` / `other` keys for a language that doesn't pluralize.
6. **Counter words / classifiers are added where the language requires them.** Thai, Japanese, Korean, Chinese.
7. **Cross-file sync is scripted.** If the task is "add these keys to every locale," the skill writes an iterator that reads → merges → writes each file, logs what changed, and does not rely on manual editing.
8. **Validation runs after changes.** Parseable JSON / valid TS, no existing keys silently overwritten, type-check if a command is available.

## What the output looks like

Depends on the ask. For a file edit, you'll see surgical diffs (or a one-off script plus a summary of what it changed) and a note on what was validated. For a translation pass, you'll see the final strings with the team's reconciled voice applied, plus brief notes where a key required non-obvious cultural adaptation — typically a register choice, a counter word insertion, a politeness-particle decision, or a flagged shelf-life term.

For `zh-CN → zh-TW` specifically, the output is a proper retranslation through the Taiwanese team, not an OpenCC pass.

## Locales in the box

Shipped teams (not exhaustive — the skill is extensible):

- `en` and `en-genz`
- `de` (with DE / AT / CH awareness)
- `es` (with es-ES / es-419 / country-specific guidance)
- `fr` (with fr-FR / fr-CA guidance)
- `it`
- `ja`, `ko`
- `th`, `th-genz`, `th-isan`, `th-lanna`, `th-south`, `th-bupphe` (Ayutthaya classical, บุพเพสันนิวาส-flavored)
- `zh-CN`, `zh-TW`, `zh-HK`

Adding a new locale follows a documented template: minimum three roles (copywriter, cultural consultant, specialist reviewer), plus optional roles named in the skill when the language / variant needs them.

## Cross-skill integration

| Skill | When it kicks in |
|---|---|
| [`team-composer`](../team-composer) | When a localization decision needs multi-perspective strategic input (not per-string). `team-composer` owns the discussion; this skill owns the translation output. |
| [`ui-ux-pro-max`](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | Pairs with this skill when UI overflow, line-break behavior, or RTL layout is at stake (German 20–35% longer, Thai no word spaces, Arabic RTL, etc.). |
| `brand-workshop` / `tech-stack-recommendations` | Separate concerns — identity and platform selection don't overlap with translation work. |

## Install

This skill is distributed as a [Claude Code](https://docs.claude.com/en/docs/claude-code) plugin inside the [`sorawit-w/agent-skills`](https://github.com/sorawit-w/agent-skills) marketplace. From Claude Code or Cowork:

```
/plugin marketplace add sorawit-w/agent-skills
/plugin install i18n-contextual-rewriting@sorawit-w
```

Once installed, Claude picks up the skill automatically from the description in its `SKILL.md` frontmatter. Invocation triggers on phrases like "translate," "i18n," "localization," "locale," "add language," "translation keys," or any mention of a specific locale code (`th`, `ja`, `ko`, `zh-CN`, `de`, `fr`, `es`, `it`, `zh-TW`, `zh-HK`, `th-bupphe`, etc.).

## Status and scope

v0.1. Covers the two concerns most i18n work trips over: safe edits on large files, and culturally authentic output.

- **Supported:** JSON / YAML / TypeScript / JS translation files; 15+ locales and cultural variants; surgical edits, bulk scripts, cross-locale sync; pluralization and counter-word handling; multi-role review.
- **Adaptable:** New locales via the documented template.
- **Not supported:** Long-form prose translation; RTL layout engineering; OpenCC-only pipelines where retranslation is refused; non-user-facing strings.

## Contributions

Not accepting external contributions right now. Feel free to fork.

## License

MIT — see the [LICENSE](https://github.com/sorawit-w/agent-skills/blob/main/LICENSE) file at the repo root.
