# Intake — mode classifier, gap-questions, match-vs-fix tiebreak

Loaded in Phase 1. Goal: pick the mode, capture the brief, ask **only** what you can't
infer. Default aggressively; let the user correct a draft rather than answer a quiz.

## Mode classifier

Read what the user actually handed you:

| You were given… | Mode | Then |
|---|---|---|
| A **mockup image** + "build / make / match this" | **A1 match** | Build to match; fidelity diffs the render against the image (hard gate on the shown viewport). |
| A **screenshot of a current render** + "fix / it looks wrong / off" | **A2 fix-from-image** | Fix toward the brief + DESIGN.md; the image is *what's wrong*, not the target. |
| **UI code** (HTML/JSX/Vue/etc.) + a change request | **B fix-from-code** | Produce updated HTML + a plain-language change description; render before & after. |
| Only a **text brief**, no image, no code | A1-as-text | Treat the brief as the target; fidelity is advisory (no reference). |
| Any of the above **but no DESIGN.md exists** | **C bootstrap first** | Resolve brand (Phase 2), then run the matching mode above. |

## Match-vs-fix tiebreak (the one that matters)

Misclassifying match vs fix flips the entire verification path, so when an image is present
but intent is unclear, **ask exactly one question** — don't guess silently.

Default lean before asking:
- Image looks like a **polished mockup / design comp** → **match** (A1).
- Image looks like a **rough or visibly-broken render** and the brief lists problems →
  **fix** (A2).
- Genuinely ambiguous → one question: *"Should I build a new screen to match this image
  (match), or fix the screen this image shows (fix)?"*

## Gap-questions (batch, default, don't interrogate)

Ask these **only if uninferable from the brief/repo**, in **one batched message**, each
with a stated default so the user can just say "yes":

| Question | Default if unanswered |
|---|---|
| Surface type — page, mobile screen, or component? | Infer from the brief; component if it names one element |
| Target viewports? | **Both** desktop + mobile (generate the one not shown) |
| States to cover beyond the happy path? | empty / loading / error **if the surface implies data**; skip for static |
| Brand source, if no DESIGN.md and ambiguous? | Run the brand ladder; offer templates only if greenfield |
| Reference image — target or current-state? | The match-vs-fix tiebreak above |

**Hard rule:** never exceed ~3 questions. If you're tempted to ask more, paint a draft on
your best assumptions and let the user redirect — a wrong draft is cheaper than a long
interrogation, and the render loop will surface most ambiguities anyway.
