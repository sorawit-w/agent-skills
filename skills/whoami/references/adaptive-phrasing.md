# whoami — Adaptive Phrasing

Two adaptation levers, **different mechanisms**.

## Tone — a delivery register

The agent delivers the canonical question text in a target register. Two axes,
derived from background:

- **Formality** — casual ↔ professional. From `field`, `role`, and the user's
  own free-text style.
- **Explanation** — explained ↔ terse. Driven by `ai_experience` (`new` →
  define terms, gentler; `high` → terse, assumes fluency).

Default when signal is thin: **neutral-friendly, plain language, lightly warm.**
Tone applies to the whole interview.

## Domain-skinning — controlled substitution

A pre-authored lookup, **not runtime generation**. The confirmed `field` (with
`primary_uses` as tiebreaker) selects a domain bucket: `software/technical` ·
`writing/content` · `data/analysis` · `design/creative` · `business/ops` ·
`generic` (fallback). Each skinnable question (Q1, Q6, Q7, Q8) ships
pre-authored variants per bucket; the skill selects by lookup.

**Equal-stakes rule:** every variant of a question holds the same risk/weight —
the substituted example never raises or lowers the stakes of the choice
(critical for the Initiative questions).

## Hard invariants — what may NEVER change

Tone and skinning may only touch the *surface*. Neither may:

- change which dial a question measures;
- change the choice options' meaning, or add/remove an option;
- change the choice→delta mapping;
- alter the scenario's stakes.

If unsure how to skin or tone a question, fall back to the canonical default.
Every variant is a fixed, reviewed string — so "this variant measures dial X"
stays unit-testable.
