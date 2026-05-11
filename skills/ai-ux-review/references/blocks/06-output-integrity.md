# Block 6 — Output Integrity

## Definition

The gen-AI-specific surface that didn't exist (or existed only marginally) in
pre-2022 human-AI design frameworks. Covers hallucination handling, output
verifiability, provenance and citation, prompt-injection exposure, multi-turn
drift, and agent-autonomy levels. This is where this skill differentiates
from a straightforward re-housing of pre-2022 frameworks.

This block applies most heavily to LLM-powered products and agentic systems.
For classical-ML products (recommendations, classification, ranking), the
probes adapt — but the underlying question remains: "what's the integrity
surface of the AI's output, and how do you take it on?"

## Primary probe

> "Pick one piece of the AI's output that you would lose your job over if it
> were silently wrong. What's the integrity mechanism for that piece — how
> would you know it was wrong before the user did?"

## Secondary probes (LLM-specific)

1. **Hallucination handling.** Where in the output is the AI most likely to
   confabulate? What's the design response — structured extraction,
   retrieval grounding, post-generation verification, surfaced
   uncertainty, none?
2. **Provenance and citation.** Can the user trace any factual claim back
   to a source? Even a partial source map is much better than none.
3. **Verifiability.** When the AI says something is true, can the user
   check it without re-doing the task? Verifiability without click-through
   is theater (callback to Block 3).
4. **Prompt-injection surface.** What user input is concatenated into the
   prompt? What happens if a user (or a recipient of the AI's output)
   embeds prompt-injection content? Even non-adversarial user content
   sometimes contains accidental injection.
5. **Multi-turn drift.** Across a long conversation, does the AI's
   adherence to its initial instructions degrade? What's the design
   response — re-grounding, conversation reset, instruction reinforcement?

## Secondary probes (agentic-specific)

6. **Autonomy levels.** Where on the suggest/recommend/draft/act/auto-act
   spectrum does the AI sit? What actions can it take without confirmation?
   What's the blast radius of a wrong action?
7. **Action reversibility.** Are the AI's actions reversible by the user?
   "Send email" is irreversible. "Draft an email" is. The design has to
   take on irreversibility.
8. **Confirmation gates.** Where are the human-in-the-loop checkpoints
   for high-stakes actions? "User can always cancel" is not a checkpoint
   if cancellation requires real-time vigilance.
9. **Tool-use boundaries.** If the AI uses tools (search, code execution,
   API calls), are the boundaries scoped? Can the user see what tools
   ran?

## Secondary probes (classical-ML adaptation)

10. **Confidence calibration.** Are the model's confidence scores
    calibrated against actual accuracy? Or are they raw softmax
    probabilities?
11. **Out-of-distribution behavior.** What happens when the input is
    unlike the training data? Does the system know it's OOD, or does
    it confidently predict?
12. **Bias surface.** Where are the known disparate impacts? What's the
    design response — reweighting, threshold-per-segment, surfacing the
    disparity, accepted-risk note?

## Acceptance criteria

- [ ] **Verifiability strategy named.** For at least one class of output,
      the user has a defined path to verify (or an accepted-risk note for
      why not).
- [ ] **Provenance scheme.** Sources, citations, intermediate steps, or
      "we don't expose provenance because…" — a deliberate choice.
- [ ] **Prompt-injection surface acknowledged.** Where user (or external)
      input enters the prompt; what the design response is. For
      classical-ML products, the equivalent is adversarial input handling.
- [ ] **Autonomy level explicit.** Where on the spectrum the AI sits; what
      actions need confirmation; what's reversible.
- [ ] **Multi-turn drift considered** (LLM only) or **OOD behavior
      considered** (classical ML).

## Common gap patterns

- **"The model is good."** The team has tested the model on benchmarks and
  decided integrity is handled by model quality. This is the dominant gap
  for teams that haven't shipped an LLM product before. Benchmarks don't
  cover the user-input distribution.
- **No hallucination defense beyond "we tell users it might be wrong."**
  A disclaimer is a CYA mechanism, not an integrity mechanism. Press for
  the actual design response.
- **Citations without verification.** "Powered by sources" with no click-
  through, or click-through to a generic search. Provenance theater.
- **Prompt injection unconsidered.** Especially for products where the AI
  reads user-generated content (email replies, customer-support tickets,
  documents), the injection surface is real. Even non-adversarial users
  embed instructions accidentally.
- **Autonomy creep.** The team built a "suggest" feature, then added an
  "apply suggestion with one click" button, then defaulted that to true.
  The product is now an "act" feature with the UX of a "suggest" feature.
  Surface this gap explicitly.
- **Reversibility ignored.** The AI takes an action; there's no undo.
  Common in agentic features and silent in most early designs.
- **No multi-turn re-grounding.** A 30-turn conversation drifts arbitrarily
  far from the initial constraints. The team hasn't measured how far.

## Worked example (LLM email drafting)

| Field | Filled |
|-------|--------|
| Verifiability strategy | "Factual spans (dates, times, names, numbers) are extracted via structured pass before generation; the draft renders them as separately-styled chips that surface the source ('from your original ask: \"this Tuesday\"'). User can click chip to see source." |
| Provenance | "Voice tone basis: 3 sample emails. Content basis: user's one-line ask. Recipient context: explicitly none. All three shown in a header strip above the draft." |
| Hallucination defense | "Two-pass generation: structured extraction of factual claims first, then prose generation that's constrained to use only the extracted facts. Hallucinations would have to come from the structured-extraction step, which is narrower." |
| Prompt-injection surface | "User's one-line ask is sanitized for known injection patterns ('ignore previous', '\\n\\nNew instructions:', etc.) and length-capped. We do NOT include the recipient's previous emails in the prompt — that's the most likely injection vector and we've decided not to take it on for v1." |
| Multi-turn drift | "Each regeneration re-includes the voice samples and the user's edits as constraints. Drift bounded by re-injection." |
| Autonomy level | "Draft. Explicitly never auto-send. The 'send' button is not an AI affordance — it's the user's." |

The "we've decided not to take it on for v1" note on prompt-injection is a
mature design decision — surfacing the *choice not to act* is itself an
output of this block.

## When the block is "complete enough"

When verifiability, provenance, prompt-injection surface, autonomy level,
and multi-turn (or OOD) behavior all have specific design choices or
explicit accepted-risk notes. This block is the longest in most reviews —
that's the point. Block 6 is where this skill earns its keep.
