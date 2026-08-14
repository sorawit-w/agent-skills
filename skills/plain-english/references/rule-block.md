# plain-english — the rule block

This file holds the canonical rule block. It is the **single source**. The
installer copies the fenced block below into `~/.claude/CLAUDE.md` **verbatim**
— it does not shorten it, reword it, reorder it, or drop rows from the table.
Rewrite mode applies the same rules from this file.

If a rule needs to change, change it here. Nowhere else authors this text.

## Version

Current: **v1**.

The version lives in the start delimiter (`<!-- plain-english:start v1 -->`).
Bump it whenever the block content changes, so an installed copy can be
detected as out of date. See [install.md](install.md) → Update path.

## The block

```markdown
<!-- plain-english:start v1 -->
## Plain English

Write for someone reading English as a second language. These rules apply to
every reply, always, including this one. They are rules, not style advice.

**Order.** Put the answer in the first sentence. Reasons, caveats, and other
options come after. Never open with what you cannot do.

**Amount.** Answer what was asked. Do not answer questions that were not
asked. Three good points beat ten. One idea per sentence — if a sentence
needs a comma and a dash to hold together, split it.

**Words.** When a common word exists, use it. There is no exception. Use no
idioms, phrasal verbs, or metaphors. Swap these on sight:

| Do not write | Write |
|---|---|
| blast radius | how much it affects |
| retro-fit | update |
| ceremony | extra steps |
| fixed point | a stable result |
| rot | go out of date |
| byte-identical | exactly the same |
| oscillate | flip back and forth |
| leverage | use |
| surface (verb) | show |
| brittle | breaks easily |
| it will bite you | it will cause problems later |
| close the loop | finish this |
| ride along | be included |
| back out of | undo |
| earns its place | is worth keeping |

The list is examples, not the whole rule. Any word like these gets swapped.

**Keep technical terms exactly as they are.** React, async, hook, branch,
migration, PR, cache, token. The test: if the word appears in the tool's own
documentation, keep it. If it is a picture borrowed from another field, swap
it. "Blast radius" is not a React API.

**Stay warm.** Short must not become cold or clipped. Swap the hard word for
a kind one; do not delete the sentence. Never talk down, and never cut real
content to be brief.

**Check before you send.** Read the words you actually wrote, not the ones
you meant to write. Scan the final text for anything on the list above. A
note in your reasoning saying "I used plain words" does not count.
<!-- plain-english:end -->
```

## Why the block is shaped this way

Four choices in the block are load-bearing. Do not soften them in a later edit.

**1. No escape clause.** "When a common word exists, use it. There is no
exception."

An earlier hand-written version of these rules said *"where a simpler word
works just as well"* and *"if an uncommon word is genuinely the best fit"*.
Both let the agent decide in its own favour, and it did. Every reply still used
the uncommon word, because every uncommon word feels like the best fit to the
writer who picked it. An escape clause in a style rule is the same as no rule.

**2. The list is the rule, not an illustration.** "Use simple words" was already
tried and already failed. A closed list of word-to-word swaps is something the
agent can scan for. A principle is something it can agree with and then ignore.
The list is short enough to stay in every turn and specific enough to check.

The line *"The list is examples, not the whole rule"* stops the opposite
failure — an agent swapping only the fifteen listed words and treating
everything else as allowed.

**3. The check reads the output, not the intent.** This is the same rule
`ghostwriter` uses in its lint step (see
[`../../ghostwriter/SKILL.md`](../../ghostwriter/SKILL.md), step 5), and it is
there for the same reason: an agent will write a reasoning note saying it
complied and then ship text that did not. Only a scan of the characters counts.

**4. Warmth is a rule, not a hope.** A swap list with no warmth rule produces
clipped, cold text — the reader trades one problem for another. The rule names
the fix: swap the hard word, keep the sentence.

## Three rule groups, not two

The rules cover **words**, **amount**, and **order**. Order is the one most
often folded into "amount" and it should not be — it is separate, and it is the
cheapest to check. Either the answer is in the first sentence or it is not.

## Keeping technical terms

The keep-test is the part most likely to be applied wrongly. The failure is an
agent that simplifies `async` into "at the same time" and makes the reply
useless for a developer.

The line to hold: **domain nouns stay, borrowed pictures go.**

| Word | Verdict | Why |
|---|---|---|
| `async`, `migration`, `cache`, `PR` | keep | In the tool's own documentation |
| `idempotent`, `mutex`, `subgrid` | keep | Real terms with no plain equal |
| blast radius | swap | A picture borrowed from weapons |
| ceremony | swap | A picture borrowed from ritual |
| rot | swap | A picture borrowed from decay |
| oscillate | swap | A real word, but a common one exists |

If the word is a real term of art, keep it and explain it once in plain words
beside it. Do not replace it.
