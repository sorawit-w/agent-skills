# Block 4 — Feedback & Control

## Definition

What the user can do when the AI is wrong. Correction affordances (edit the
output), override paths (reject the AI's choice and use the manual
alternative), hand-off (escalate to a human), take-over (suspend AI
involvement), and the autonomy spectrum (how much initiative the AI takes
vs. the user retains).

This block inherits from Block 3 (trust calibration): every trust signal
implies a user action — the user is supposed to do *something* with that
trust. If Block 3 says "we show the sources," Block 4 must say "users can
click through to verify them." Trust without affordance is theater.

## Primary probe

> "Walk through a specific scenario where the AI is confidently wrong. What
> does the user do to fix it? What does the UI give them to do that with?"

## Secondary probes

1. **Correction granularity.** Can the user edit a word? A sentence? The
   whole output? Regenerate with a constraint? Different granularities
   imply different control surfaces.
2. **Override path.** Is there a non-AI way to complete the task in the
   same UI? Or do users have to abandon the feature entirely to fall back?
3. **Hand-off path.** When the AI shouldn't be in the loop (high stakes,
   user uncertainty, edge case), what's the path to human review? "Email
   support" is a fallback, not a designed hand-off.
4. **Autonomy spectrum.** Is the AI proposing, suggesting, drafting, or
   acting? Each step up the autonomy ladder shifts the burden between AI
   and user. Where on the spectrum is each user-facing action?
5. **Feedback signals back to the system.** When the user corrects the AI,
   does anything happen with that correction? Even if not for training,
   does the user *see* their correction acknowledged?
6. **Take-over.** Can the user say "stop using AI for this task" mid-flow?
   Or are they locked into the AI path once they start?

## Acceptance criteria

- [ ] **Correction affordances enumerated.** At least the granularities
      the design supports — word-level / sentence-level / regenerate /
      manual edit.
- [ ] **Override path stated.** Either a non-AI completion path in the
      same UI, or an explicit acknowledgment that the only fallback is
      "leave the feature."
- [ ] **Autonomy spectrum named.** Where on the suggest/draft/act spectrum
      each user-facing surface sits.
- [ ] **At least one path for "the AI shouldn't be doing this here."**
      User signal, hand-off, or take-over.

## Common gap patterns

- **"Users can just edit it."** Treats correction as the universal
  affordance. Editing fluent prose to be slightly wrong in a different
  way is hard — users often abandon rather than edit. The block should
  surface this.
- **No override path.** The AI is the only way to do the task. When it's
  wrong, the user has nowhere to go. Common in launch-day features where
  the team removed the manual path "to focus on the AI flow."
- **No take-over.** The user is committed to the AI path once they
  start. Especially bad for agentic features where the AI is taking
  multi-step actions.
- **Hand-off as afterthought.** "User can email support" — support has
  no context, no record of what the AI did, no path back into the user's
  flow. Hand-off without continuity is a dead end, not a hand-off.
- **Autonomy spectrum not named.** The team built an "AI feature"
  without deciding whether the AI proposes, drafts, or acts. The user
  experience varies wildly across these and they need different
  controls — naming the autonomy level is a forcing function.
- **Correction with no acknowledgment.** User fixes the AI's output;
  the system gives no signal it noticed. Even without training-loop
  intent, the absent acknowledgment reads as "the system isn't
  learning."

## Worked example (LLM email drafting)

| Field | Filled |
|-------|--------|
| Correction granularity | "Word: inline edit. Sentence: select + regenerate-this-sentence-only. Whole: regenerate with new constraint chip ('shorter', 'more direct', 'add specific detail X')." |
| Override path | "Switch to template library inline (button: 'Skip AI, pick a template'). Templates load in-place, same UI." |
| Autonomy level | "Drafts. The user always reviews before sending — no auto-send. Stated explicitly in onboarding." |
| Hand-off | "If user corrects the same sentence 3+ times: surface 'Want to write this one yourself?' with the draft already cleared from that point onward." |
| Take-over | "Top-right toggle: 'Hide AI suggestions for this thread.' Persists per recipient." |
| Feedback acknowledgment | "Edited words are flagged in the next regeneration: 'I won't change [your-edited-words] again unless you ask.' Builds trust over multi-turn." |

## When the block is "complete enough"

When the user has at least one specific correction granularity, an explicit
override path (or acknowledgment of none), an autonomy level named for each
surface, and a path for "this isn't working — get me out." If any of those
is missing, the block isn't complete — it's a gap.
