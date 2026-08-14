---
name: plain-english
description: >
  Installs a lasting plain-English rule set into the user's global CLAUDE.md, so every later
  reply stays readable for people who read English as a second language — common words, the
  answer first, no idioms. Also rewrites a dense passage on demand. Triggers on: "say that in
  plain English", "simpler English", "your replies are too long / too dense / hard to read",
  "write for non-native English readers", "ESL readers", "install / update / uninstall the
  plain-English rules", "/plain-english". Does NOT trigger for: drafting messages sent as the
  user (`ghostwriter`); explaining what one word means in context (`define`); translation
  files or locale work (`i18n`); tuning the whole collaboration or its defaults (`whoami`,
  `handshake`) — this fixes readability only; or teaching English — no lesson plans, grammar
  drills, or test prep. Keeps technical terms (React, async, migration, cache) unchanged.
instructions: |
  Load this skill when: the user wants the agent's own replies to be easier to
  read, wants the plain-English rules installed, updated, checked, or removed,
  or hands over a dense passage to be rewritten in plain words.
  Do NOT load this skill when: the user wants a message drafted in their own
  voice (ghostwriter), one word explained (define), locale or translation files
  edited (i18n), or English teaching material written.
tags:
  - plain-english
  - readability
  - second-language
  - accessibility
  - communication-style
metadata:
  tier: draft
---

# plain-english

Make the agent's replies readable for someone who reads English as a second
language. Two problems, three rule groups: **words** (common ones, no idioms),
**amount** (answer what was asked), **order** (the answer first).

The rules live in [references/rule-block.md](references/rule-block.md). That
file is the single source. This skill does not restate the rules, does not
paraphrase them, and does not write its own version of them.

## Why this skill does not enforce anything

A skill loads when something triggers it. "Write plainly" has no trigger — it
applies to every reply, including the ones where nobody mentions writing. So
the skill cannot be the enforcer.

It is the **source**, the **installer**, and the **updater**. It copies the
rules into `~/.claude/CLAUDE.md`, which is re-sent as input on every turn.
After that, the user can forget this skill exists.

## Modes

Route on the argument.

| Argument | Mode | Do this |
|---|---|---|
| none, or `install` | Install | Follow [references/install.md](references/install.md) → Install |
| `update` | Update | Same file → Update |
| `status` | Status | Same file → Status |
| `uninstall` | Uninstall | Same file → Uninstall |
| a passage of text, or "rewrite this" | Rewrite | See below |

If the argument is ambiguous, ask one short question. Do not guess between
installing and rewriting — one edits the user's global config.

## Rewrite mode

Apply every rule in [references/rule-block.md](references/rule-block.md) to the
text the user gave you.

1. **Read the rule block first.** Do not rewrite from memory of these rules.
2. **Swap every listed word.** Scan the passage for each row of the table.
3. **Fix order.** Move the answer to the first sentence. Caveats go after.
4. **Cut what was not asked for.** Drop points that answer a question nobody
   asked.
5. **Keep every technical term.** React, async, migration, cache, and the like
   stay exactly as they are. Apply the keep-test in the rule block: domain
   nouns stay, borrowed pictures go. A real term of art is kept and explained
   in plain words beside it, never replaced.

   **When the user asks you to remove them** ("no jargon", "explain this for
   someone non-technical", "rewrite it for my mum"), their instruction wins.
   Do it. Then use the note in step 8 to say the terms were dropped and that
   the result is no longer precise enough for a reader who needs them. Do not
   refuse, and do not quietly keep the terms after being asked to remove them.
6. **Keep the warmth.** Swap the hard word for a kind one. Do not delete the
   sentence to make the text shorter.
7. **Check what you wrote.** If `scripts/check-swaps.py` is reachable, run it
   on your output. It is the only check here that is not you grading yourself:

   ```bash
   python3 skills/plain-english/scripts/check-swaps.py -
   ```

   Fix every hit, then run it again. If the script cannot run, scan the real
   characters of your output against the swap table by hand. Either way, a note
   in your reasoning saying you used plain words does not count.

   A clean result is not proof the text is plain. The script only sees the
   listed words, in the forms it can match. Hard words that are not on the list
   are still yours to catch.
8. **Output the rewritten text only.** No preamble, no list of what you
   changed.

   **One exception, one line.** Add a note in exactly two cases:

   - You dropped a technical term because the user asked you to.
   - You kept a harder word because the plain swap would have lost meaning.

   That is the whole list. Making an ordinary swap is following the rules, not
   departing from them, so it never earns a note — not even a true one, and not
   to show your work. "The passage was already plain, so I changed little" is
   not a departure either. When the rewrite is clean, the text is the whole
   answer and you add nothing.

   When a note is due, it must be true. Do not write "the only change was X"
   unless X really was the only change. An inaccurate note is worse than no
   note, because it tells the reader to stop checking.

Never change what the passage means. If a swap would lose real information,
keep the meaning and find a different plain wording. Losing content is a worse
failure than using a hard word.

## What this skill cannot do

Say this plainly when it comes up. Do not claim more.

- **It cannot promise the rules are followed.** Installing them puts them in
  context every turn. Whether the agent follows them late in a long session is
  not measured. If replies get denser as a session goes on, that is worth
  reporting — the fix would be a `UserPromptSubmit` hook that repeats the short
  version, and that has not been built.
- **It is English only.** It does not translate, and it does not make text
  easier to read in any other language.
- **The swap list is not complete.** It was built from real failures, in one
  variety of English. Users will meet hard words that are not on it. The
  general rule covers those; the list is the teaching examples.

## Boundaries

| Skill | Owns | Not this skill because |
|---|---|---|
| `ghostwriter` | Text the user sends to other people, in the user's voice | `plain-english` governs what the agent says **to** the user |
| `define` | What one word means in its sentence | It explains a word; it does not change how replies are written |
| `i18n` | Translation files, locale data, cultural rewriting | Different language, not English readability |
| — | English teaching: lesson plans, grammar drills, test prep | This skill writes for readers, it does not teach them |
