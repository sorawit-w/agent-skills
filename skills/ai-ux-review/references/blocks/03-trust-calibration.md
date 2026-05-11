# Block 3 — Trust Calibration

## Definition

When and how the system surfaces confidence, sources, or limits — and the
failure paths in both directions. **Under-trust** means users reject good
output because the system doesn't show enough basis for trust. **Over-trust**
means users accept bad output because the system shows too much basis (or
the wrong basis). Both are equally bad outcomes, and the design has to take
on both.

Trust calibration depends on the mental model in Block 2 — a user with a
probabilistic mental model will read a confidence chip differently than a
user with a deterministic mental model.

## Primary probe

> "Pick one moment in the user flow. At that moment, what evidence does the
> user have for trusting the system's output? Be specific — is it text, a
> chip, a source list, an action affordance? And what's the user supposed
> to do with that evidence?"

## Secondary probes

1. **What's the under-trust failure path?** Walk through the specific user
   who refuses the output. What did they see that didn't convince them?
   What would have convinced them?
2. **What's the over-trust failure path?** Walk through the specific user
   who accepts a wrong output. What did they see that *over*-convinced
   them? Often this is fluent, confident prose without sources.
3. **Where does the system surface confidence numerically vs. through
   language?** "78% confidence" reads differently to a user than "I'm
   pretty sure" — both are calibration choices.
4. **Where does the system surface sources, citations, or provenance?**
   If the user can't trace where an answer came from, the trust signal is
   "this AI said so," which is rarely the trust signal you want.
5. **Where does the system surface its limits?** "I don't have access to
   the recipient's recent emails," "I can't verify this fact" — explicit
   limit-surfacing is a trust-calibration tool that's almost always
   undersold.

## Acceptance criteria

- [ ] **Trust-surfacing moments enumerated.** At least three specific
      moments in the flow where the system gives the user evidence about
      whether to trust the output. "Globally show a model name" doesn't
      count; per-output trust signals do.
- [ ] **Confidence-surfacing strategy.** Either numerical, linguistic,
      visual (color chips, asterisks, side-by-side), or "we don't surface
      confidence here because…" — but a deliberate choice.
- [ ] **Both failure paths named.** A specific under-trust scenario and a
      specific over-trust scenario. If only one is named, the design is
      one-sided.
- [ ] **Mitigation per path.** What in the UI prevents the failure, or an
      accepted-risk note.

## Common gap patterns

- **Confidence shown without explanation.** "78% confidence" without
  telling users what 78% means is decoration. Calibrated users won't
  trust it; uncalibrated users will treat 78% the way they treat a
  weather forecast — wrong.
- **Sources cited without click-through.** "Based on these sources" with
  no way to verify is a trust signal that can't actually be checked. It
  produces over-trust by default.
- **No over-trust path considered.** Teams often design only for the
  under-trust failure (the user who won't try the AI). The user who
  trusts too much is the more dangerous one for most products.
- **"It feels accurate" as the trust mechanism.** The output reads fluent
  and confident, and the team trusts that surface signal. This is the
  default failure mode for LLM products and the one Block 6 will press
  hard on.
- **No limit-surfacing at all.** The system pretends to know everything.
  Users either over-trust (until they discover a limit catastrophically)
  or under-trust (after their first over-trust mistake).

## Worked example (LLM email drafting)

| Field | Filled |
|-------|--------|
| Trust-surfacing moment 1 | "After draft generation: chip showing which of the 3 voice samples weighted most heavily, clickable to see the sample text." |
| Trust-surfacing moment 2 | "If the user's one-line ask contained a factual claim ('mention I'm in Seattle this week'), the draft includes a 'verify this' chip near that factual span." |
| Trust-surfacing moment 3 | "Header strip: 'Based on your ask + 3 voice samples. Not based on: recipient context, current company news, your calendar.'" |
| Confidence strategy | "Linguistic, not numerical. We don't show a confidence number for prose generation — calibrated meaning is hard. We do show *what the AI was working from*, which is the trust signal users actually use." |
| Under-trust failure | "User receives a usable draft but doesn't trust 'AI-on-brand voice' as a category; rewrites from scratch. Mitigation: voice-samples chip lets them see the basis and edit the samples — they're in control." |
| Over-trust failure | "User accepts a draft that asserts a meeting time the AI invented from ambiguous input. Mitigation: 'verify this' chip on factual spans; future block 6 mitigations add structured extraction for dates/times." |

## When the block is "complete enough"

When three trust-surfacing moments are enumerated, the confidence strategy
is named and justified, both failure paths have specific scenarios with
mitigations, and the team has thought about *what* the trust signals are
based on (not just whether they exist).
