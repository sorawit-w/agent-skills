---
name: whoami
description: >
  Runs a short, conversational interview that builds a portable profile of the
  user — who they are and how they want to be collaborated with — so the agent
  can tailor every response. Triggers on `/whoami`, "get to know me", "set up
  my profile", "personalize how you work with me", "calibrate how you respond",
  the user mentioning they are new to AI or switching agent vendors, or a
  request for their collaboration "character sheet" or player profile. Produces
  six collaboration dials (Initiative, Depth, Breadth, Rationale, Warmth,
  Challenge), an RPG-style class + subclass with a character portrait, a stored
  memory profile, and a self-contained HTML character sheet. When a profile
  already exists, bare `/whoami` shows what the agent knows and offers to
  correct or re-run; `/whoami rerun` re-runs the interview. Does NOT trigger
  for project- or task-specific work calibration (use `handshake`), routine
  memory edits or CRUD (use the memory-management skill), or brand-voice work.
  `whoami` is the broad, person-level profile; `handshake` is the narrow,
  project-level one — whoami feeds handshake.
---

# whoami

`whoami` builds a profile of the user — who they are and how they want to be
collaborated with — and stores it so every future response can be tailored. The
profile is a **revisable prior, not a verdict**: a snapshot the user owns and can
correct any time.

Sibling skill: `handshake` calibrates one project; `whoami` is the broad,
person-level profile and feeds `handshake`.

## Core principles

1. Everything converges on the **six dials** (Initiative, Depth, Breadth,
   Rationale, Warmth, Challenge). Memory, background, MBTI, prior profile, and
   scenario questions are all inputs to those six numbers.
2. **Nothing is stored without explicit confirmation.** Every inferred value is
   shown before it lands.
3. **Skip what you already know.** Only ask a scenario question for a dial you
   cannot fill confidently.
4. **Hold the profile lightly** — revise on contradiction; never let it override
   what the user does now.
5. **The knowing is the point; the character sheet is the delight.** Calibrate
   behavior from the six dial values, never from the class label.

## Invocation

| Invocation | Profile exists? | Behavior |
|---|---|---|
| `/whoami` | No | Run the full flow (Steps 1–9). |
| `/whoami` | Yes | Show mode — present the summary + class, offer: correct / re-run / looks good. |
| `/whoami rerun` | Yes | Re-run — show the profile, ask "start from current and confirm/adjust, or fresh?", then run the flow. |
| `/whoami rerun` | No | Same as `/whoami` with no profile. |

`/whoami` is the primary entry point. Suggest whoami unprompted only when user
memory is sparse and tailored help would clearly benefit — never mid-task.

The flow itself adapts: no prior data → runs cold (**Fresh**); existing user
memory → pre-fills and confirms (**Review-and-correct**); the user offers an
MBTI type or prior profile → pre-fills from it (**Import**); a re-run → the
existing profile pre-fills everything (**Re-run**).

## The flow

**Step 1 — Open.** Briefly say what this is: a short conversational setup so you
can tailor how you work together; it ends in a character sheet they keep; any
question is skippable, everything changeable later.

**Step 2 — Review what you know.** Read runtime memory. Prior `whoami` profile →
Re-run. Other user memory, no profile → summarize what you already know in plain
language. Nothing → say "We're starting fresh" and go to Step 4.

**Step 3 — Correct.** Let the user fix anything stale or wrong before continuing.

**Step 4 — Background.** Ask the background questions
(`references/background-questions.md`), one at a time, conversational, every item
opt-out. Follow the data-handling rules below. Answers set the domain bucket and
tone for adaptive phrasing.

**Step 5 — Optional fast input.** Offer the shortcuts: an MBTI type or a prior
`whoami-profile.md`. Map per `references/mbti-mapping.md` or parse the file.
Treat results as estimates, never final.

**Step 6 — Infer dial estimates.** From memory + background + MBTI/profile,
estimate each of the six dials; tag each high / medium / low confidence.

**Step 7 — Confirm and fill gaps.** Per dial: high-confidence → state it
conversationally, ask the user to confirm or nudge; medium/low → ask that dial's
scenario question(s) from `references/question-bank.md`, one at a time, in your
own voice, with adaptive phrasing (`references/adaptive-phrasing.md`). Every dial
ends explicitly user-confirmed.

**Step 8 — Finalize.** Score per `references/question-bank.md`; derive class +
subclass from `references/class-map.md`; carry forward existing flexible traits
(≤5).

**Step 9 — Persist and report.** Per `references/persistence.md`:
1. Optionally offer a cosmetic color-theme pick (or use the class default).
2. Generate the character portrait — capability-gated: if `pixel-art` + an image
   generator are available, generate a class-anchored pixel character and
   base64-embed it; otherwise use the default class SVG from
   `assets/characters/`.
3. Write the portable `whoami-profile.md` (`templates/profile-template.md`) and
   the self-contained HTML character sheet (`templates/character-sheet.html`).
4. Write runtime memory (capability-gated) + a dated snapshot.
5. Show the user the result and where it lives.

## Show mode & the correction path

When bare `/whoami` finds an existing profile, present the prose summary +
class/subclass (offer to open the HTML sheet), then offer three choices:

- **Correct something** → the user describes the change in free text. Interpret
  it → map to the affected dial(s), background, or trait → show the proposed
  change → confirm → persist (new dated snapshot; canonical + memory updated in
  place). If the correction is ambiguous, ask one targeted question rather than
  guessing. This does **not** re-run the interview.
- **Re-run** → enter Re-run mode.
- **Looks good** → done; nothing written.

## Data-handling rules

- **Never solicit protected attributes.** Background questions stay scoped to
  collaboration-relevant facts; the free-text field is the only entry point for
  volunteered sensitive info.
- **Volunteered sensitive info:** keep only with explicit per-item confirmation;
  store as a *separate* standard `user`-type memory — never in the whoami
  profile, never scored, never on shareable artifacts.
- **Secrets** (SSNs, bank/account numbers, passwords, government IDs): never
  store; if volunteered, drop them and say so once.
- Defer to the host runtime's data policy; never override it.

## handshake integration

`handshake` reads `whoami-profile.md` to pre-fill its core questions. `whoami`
is upstream and one-directional — it never reads or depends on `handshake`.

## References & assets

- `references/dials.md` — the six dial definitions (canonical pole labels)
- `references/question-bank.md` — 9 scenario questions, domain variants, scoring
- `references/class-map.md` — 12-class taxonomy, Wildcard, derivation
- `references/subclass-blurbs.md` — the 120 class/subclass combination blurbs
- `references/background-questions.md` — background set + data-handling policy
- `references/adaptive-phrasing.md` — tone + domain-skinning rules
- `references/mbti-mapping.md` — MBTI → dial priors
- `references/persistence.md` — profile schema, memory contract, snapshots
- `templates/profile-template.md`, `templates/character-sheet.html`
- `assets/characters/*.svg` — 13 default class characters
- `commands/whoami.md` — slash-command entry point (`/whoami`, `/whoami rerun`)

## When to use this skill

Load when the user wants to set up, view, or update a personal collaboration
profile. Do NOT load for project/task calibration (use `handshake`), routine
memory edits, or content generation. Primary entry point is `/whoami`;
`/whoami rerun` forces a re-interview. Auto-triggering is conservative — only
suggest whoami when user memory is sparse and tailored help would clearly
benefit, never mid-task.

**Tags:** personalization, onboarding, user-profile, memory, gamification
