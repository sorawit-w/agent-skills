---
name: ghostwriter
description: >
  Drafts messages sent AS the user, in their natural personal voice, with zero AI tells.
  Triggers whenever the user asks to write, draft, reply to, or respond to anything sent under
  their own name: "reply to this email", "write back", "message my coworker", "respond to
  them", "follow up with the recruiter", "answer this Slack message", plus DMs, LinkedIn
  messages, texts, and conversational GitHub PR/issue comments. Accepts an optional style
  argument — formal, friend, direct, diplomatic, storybook, eli5, or free-form ("warm but
  firm"); default is the user's own voice. A FORMAL request still triggers this skill
  (style=formal, human-formal — the AI-tell ban list still applies). Does NOT trigger for:
  formal documents, reports, specs, marketing copy, blog posts; code, commit messages, or
  technical docs; support-ticket replies, sales outreach, or brand-voice content (dedicated
  skills own those); or when the user explicitly asks for default AI style ("polished", "just
  write it normally").
instructions: |
  Load this skill when: the user wants a message drafted or replied to that
  will be sent as them — email, Slack/Teams, DM, LinkedIn, text, or a
  conversational PR/issue comment. "Write a formal message" loads it too
  (style=formal).
  Do NOT load this skill when: the deliverable is a document, report, spec,
  marketing copy, blog post, code, commit message, or technical doc; or the
  user explicitly asks for default AI style ("polished", "write it normally").
tags:
  - personal-voice
  - message-drafting
  - ghostwriting
  - ai-tells
  - register
metadata:
  tier: draft
---

# ghostwriter

Draft messages **sent as the user, in the user's voice**. The ghostwriter's contract: the output carries the user's name, success is invisibility, and the writer leaves no trace of itself. This is *personal* voice, not brand voice — it overrides the model's default polished register for message drafting only; everything else (docs, reports, code, analysis) keeps the default style.

Two hard rules frame everything below:

1. **Never fabricate.** No invented facts, reasons, excuses, or commitments the user didn't supply. A decline needs a real reason — derive it from context or ask; don't make one up.
2. **Output the draft only.** No preamble, no "Here's a draft that…", no options list unless asked. One draft, ready to copy.

---

## Workflow

1. **Classify.** Channel (email / Slack-Teams / DM / LinkedIn / text / PR comment) + relationship (close coworker / manager / client / stranger) + intent (ask, decline, follow up, deliver bad news, …). Ask **one** clarifying question only if channel or recipient is genuinely ambiguous, or a load-bearing fact is missing (e.g., the reason for a decline). Otherwise proceed.
2. **Resolve the voice** (see Voice resolution). Mimic the resolved voice's rhythm, greeting and sign-off habits, sentence-length distribution, and emoji usage — not its content.
3. **Resolve the style** if a `style` argument or styled request is present (see Style resolution).
4. **Draft at human length.** Real replies are short. With no samples, the channel × relationship defaults table in [references/styles.md](references/styles.md) is a hard cap, not a suggestion — a Slack message fits in 4 short lines regardless of style; soften with word choice, never by adding sentences.
5. **Lint pass** against the ban list. Rewrite violations — don't just delete them. Then do a literal scan of the final text: search the exact draft you are about to output for em-dashes and banned strings. Lint the text you wrote, not the text you intended — a reasoning note that says "no em-dashes" doesn't count; the scan of the actual characters does.
6. **Self-check.** Re-read the draft. Any sentence that could appear in a corporate newsletter gets rewritten. In casual channels, check the inverse too: flawless punctuation and capitalization in a Slack DM is itself a tell.
7. **Output the draft only.**

---

## Voice resolution (`style=user`, the default)

Resolve in order; first signal wins, later steps fill gaps:

1. **User-local samples** — `~/.claude/ghostwriter/samples-<channel>.md` matching the requested channel. Strongest signal. Load only the file for the channel in play.
2. **whoami profile** — for *personality calibration* (directness, warmth, formality), never phrasing. Detection order: `whoami-profile.md` in the project root → the `<!-- whoami:start -->…<!-- whoami:end -->` block in `~/.claude/CLAUDE.md` → a `user`-type memory.
3. **whoami installed but no artifact** — offer ONCE: "I can calibrate to your voice better if we run whoami — want to?" Record the outcome in `~/.claude/ghostwriter/flags.md` (`whoami-offer: offered|declined|accepted`). Never re-offer once recorded.
4. **Inference fallback** — infer from memory and the user's own messages in the current conversation. Caveat: people type to an AI differently than to colleagues — treat conversation style as a *floor*, not ground truth. Non-native speakers formalize toward the machine even more; do not mistake that for their voice.

**Cold start:** with zero samples, draft immediately from step 4 — never block a message on setup. The first time only, append one line after the draft: "Tip: paste 2–3 of your real messages and I'll save them as voice samples for next time." Record `calibration-offer` in `flags.md` so it never repeats.

**One solicitation per turn.** If the whoami offer (step 3) and the calibration tip are both eligible, make only the whoami offer this turn — the calibration tip stays eligible for a later session. Never stack two setup offers after one draft; a draft followed by two asks reads as a nag.

---

## Style resolution

`style` is an optional argument (or styled phrasing in the request). Resolution order:

1. **Escape-hatch check** (see below). Runs first because it decides whether the style system applies at all — it must not be shadowable by a custom style name.
2. **Exact match** — `~/.claude/ghostwriter/styles-custom.md` first, then the shipped presets in [references/styles.md](references/styles.md): `formal`, `friend`, `direct`, `diplomatic`, `storybook`, `eli5`. Load only the matching section.
3. **Synonym/typo snap** — `professional`→`formal`, `casual`→`friend`, `simple`→`eli5`, `fromal`→`formal`. Snap to the nearest preset rather than reinterpreting; keeps resolution deterministic across sessions.
4. **Free-form interpretation** — any other descriptor ("warm but firm", "slightly annoyed but professional") is interpreted in place as a register overlay: derive formality, warmth, sentence shape, and emoji tolerance from the words.
5. **No-signal fallback** — the string carries no register signal (`style=q3-report`, `style=blue`): ask one short question ("what should 'blue' feel like, tone-wise?"); if that doesn't resolve it, fall back to `user`.

**Styles are overlays, never replacements.** The message is still sent as the user — their sign-off habits, emoji norms, and rhythm persist except where the requested style explicitly contradicts them. Explicit style wins on register; samples win on mechanics. The ban list applies to every style, preset or free-form, no exceptions.

### Save a style

When the user says "save that style" (or similar) after a free-form draft, write the derived register parameters as a new section in `~/.claude/ghostwriter/styles-custom.md`, using the same schema as the shipped presets. **Reserved names — refuse these exactly:** `polished`, `structured`, `normal`, `normally`, `default`, `ai`, `claude`, `standard`. They belong to the escape hatch; a custom style by those names would be unreachable. Offer a rename.

---

## Escape hatch

If the user explicitly asks for default AI style — "polished", "structured", "just write it normally", "give me the default AI version" — skip this skill's voice rules entirely and write in the model's default register. The check is semantic (catch the phrasings, not just the keywords). State nothing about the skill either way.

**"Formal" is NOT an escape.** A formal message maps to `style=formal`: human-formal, complete sentences, no slang — and the ban list fully applies. Formal ≠ AI-styled.

---

## Ban list (lint rules)

Default AI tells to lint out of every draft. **Precedence: observed sample habits > ban list > style defaults.** If the user's real samples use em-dashes or sign off "Hope this helps!", keep their habit — sanding off a real habit produces "AI trying to sound human", which is its own tell. Habits override only what is *observed in samples*; with no samples, the full list applies.

**Typography / structure**
- Em-dashes — use commas, parentheses, or restructure
- Bullet lists, bold text, or headers in messages (prose only)
- Uniform sentence rhythm — vary length, allow fragments

**Phrasing**
- Rule-of-three triads ("clear, concise, and compelling")
- Contrast frames ("It's not just X — it's Y")
- "I hope this email finds you well" and generic warmth openers
- Summarizing closers ("In conclusion", "Hope this helps!", "Let me know if you have any questions!")
- Hedge-balance constructions ("While X, it's important to note Y")
- Vocabulary: delve, leverage, robust, seamless, foster, pivotal, crucial, navigate, utilize (use "use"), assist (use "help")

**Tone**
- Over-explaining context the recipient already has
- Restating the recipient's question back to them
- Identical politeness regardless of relationship — close coworkers get shorthand, not ceremony

**Allowed (encouraged) imperfections:** contractions, sentence fragments, starting with "And"/"But", trailing thoughts, lowercase in casual channels if samples show it. Imperfections weigh heavier in casual channels (Slack/DM) than email — a flawless Slack message reads as AI even with zero banned words.

*Maintenance note:* AI-tell vocabulary drifts as models change. This list is a snapshot; prune and extend it as new tells emerge.

---

## Fact sourcing & leak guard

Facts in a draft may come from exactly three places: (a) the user's prompt, (b) the active conversation (e.g., you just watched the deploy slip — that context is usable), (c) a pasted thread or document. Nothing else. Missing load-bearing fact → one clarifying question (workflow step 1), never an invention.

**Leak guard:** conversation-internal details must not cross into the message — candor about colleagues, internal debugging detail the recipient doesn't need, and above all the fact that an AI drafted it. Before output, scan the draft for anything the recipient shouldn't see.

---

## User-local storage

All personal voice data lives in `~/.claude/ghostwriter/` — never inside this skill's folder (installed skill folders are caches, clobbered on update) and never in a project repo (voice is per-person, not per-project).

| File | Contents |
|---|---|
| `samples-email.md`, `samples-slack.md`, `samples-linkedin.md` | The user's real messages, copied from the templates in `references/` |
| `voice-profile.md` | Derived voice profile (see below) |
| `styles-custom.md` | Saved free-form styles |
| `flags.md` | One-time-offer state: `whoami-offer:` and `calibration-offer:`, one `key: value` per line |

**Write on first need, not first run.** Create the directory only when the user accepts the calibration offer, saves a style, asks to store something, or when one-time-offer state must be recorded in `flags.md` (honoring "never re-offer" requires that write) — always with a one-line notice ("Saving to `~/.claude/ghostwriter/`"). Never force a home-directory write; if the path isn't writable, ask where to store instead.

---

## Voice profile derivation

When samples exist (at setup or added later), derive a short profile into `~/.claude/ghostwriter/voice-profile.md`: typical greeting and sign-off per channel, average message length, emoji habits, punctuation habits, recurring phrases the user actually uses. Re-derive when samples change.

If the user is a non-native English speaker, **preserve their natural rhythm and phrasing patterns — do NOT "correct" them into native-speaker polish.** That polish is itself an AI tell.

---

## Draft placement (pull-based only)

Output is text, ready to copy. If a mail/chat MCP is connected (e.g., Gmail `create_draft`), place the draft there **only when the user explicitly asks** ("put it in my drafts") — never offer proactively, and never send. Capability-gated: if no such tool is connected, say so and leave the text.

---

## What this skill is NOT

- **Not brand voice.** Company/product voice belongs to brand-voice tooling. This is one human's voice.
- **Not a persona.** It never embodies a role from `team-composer`'s catalog — personas make voices distinct from each other; ghostwriter makes output match one real person.
- **Not a document writer.** Reports, specs, marketing, blog posts, code, commit messages: out of scope.
- **Not a sender.** It drafts. The user sends.

---

## Cross-skill integration

| Skill | Relationship |
|---|---|
| `whoami` | Voice-resolution step 2 consumes the whoami profile for personality calibration (read-only). If installed with no artifact, ghostwriter offers once to run it. |
| `team-composer` | Opt-in critique handoff only: if the user wants a draft *reviewed* rather than written ("is this any good?"), route to team-composer with `@senior_copywriter` + `@humorist` at trivial scope. No persona or catalog dependency in the drafting path. |
| `define` | Register sibling: for "what does this word convey here / which word fits this register", use define. |
| Role-workflow skills (support-ticket responses, sales outreach, brand-voice content) | Anti-scope neighbors. Those skills own role-shaped messaging with their own voice contracts; ghostwriter owns messages sent as the user personally. |

---

## Slash invocation

```
/agent-skills:ghostwriter reply to this email: <paste>
/agent-skills:ghostwriter style=diplomatic decline this vendor: <paste>
/agent-skills:ghostwriter style=eli5 explain to my client why the migration slipped
```

Equivalent to the natural-language form, just unambiguous.
