# Block 2 — Mental Model

## Definition

The model users will build of how the AI works, why it produces what it
produces, and what it can be trusted to do. The user's mental model is
almost never the team's actual implementation model — the gap between them
is where misuse, distrust, and disappointment live.

This block is upstream of trust calibration (Block 3). You cannot calibrate
trust for a user whose model of the system is wrong — they'll either
under-trust (refuse the AI's good outputs) or over-trust (accept its bad
outputs).

## Primary probe

> "Describe, in one paragraph, what you think a typical user believes is
> happening when they use this feature. Not what *is* happening — what
> *they think* is happening."

## Secondary probes

1. **Where will the user's model diverge from reality?** Name two specific
   misalignments. ("They think it 'knows' about their company. It doesn't —
   it's reading the last 5 emails as context.") Misalignments without
   names are gaps.
2. **How does the user form this model?** First use? Onboarding tour?
   Marketing copy? Watching what the system does? Different formation paths
   produce different models and require different teaching affordances.
3. **What evidence does the UI give the user about how it works?** Listing
   sources, showing intermediate steps, naming the model ("powered by
   GPT-4"), showing token counts — these are *teaching* moments that shape
   the mental model whether the team designed them or not.
4. **Does the mental model differ across user segments?** A power user and
   a first-time user almost always model the same AI differently.
5. **Has the team observed users articulate their model?** "We think users
   probably think…" is much weaker than "Five users in interviews said
   X." If the answer is "we haven't asked," that's a gap.

## Acceptance criteria

- [ ] **Described user model.** One paragraph in user words.
- [ ] **Named misalignment risks.** At least two specific divergences from
      the actual system behavior.
- [ ] **Mitigation per risk.** For each named misalignment, either a
      teaching affordance ("we show the sources used so users understand
      what context the AI has") or an accepted-risk note ("we expect
      misalignment X; we're tolerating it because…").
- [ ] **Evidence basis.** Either user-research evidence for the described
      model, or an explicit acknowledgment that the model is inferred
      and needs validation.

## Common gap patterns

- **"Users will figure it out."** A pattern-matching dodge. Users do
  figure things out — they form *some* mental model. The question is
  whether the model they form lets them use the system well. "Will figure
  it out" without specifying *what* they'll figure out is a gap.
- **No observed user articulation.** The team's described mental model is
  what *the team thinks users think*. This is almost always wrong in
  specific, predictable ways. A review that doesn't surface this gap is
  shallow.
- **Anthropomorphic model unexamined.** Users almost always partially
  anthropomorphize AI ("it gets me," "it remembers"). Whether to support
  this model, gently correct it, or actively undermine it is a design
  choice — pretending the choice doesn't exist is a gap.
- **No teaching affordances in the UI.** The mental model is being shaped
  entirely by marketing copy and first-impression behavior. Teaching
  affordances inside the product (showing context used, naming the
  intermediate step, surfacing limits) shape the model more reliably.

## Worked example (LLM email drafting)

| Field | Filled |
|-------|--------|
| User model (paragraph) | "Users think the AI 'knows' how they write — that it studied their previous emails and can imitate their voice. They also think it has access to context about the recipient ('I bet it knows that I emailed them last month')." |
| Misalignment 1 | "Voice imitation: actually inferred from a small fixed prompt with 3 sample emails, not from a model trained on their corpus." |
| Misalignment 2 | "Recipient context: actually none beyond what's in the user's one-line description." |
| Mitigation 1 | "Onboarding shows the 3 'voice samples' selected and lets the user swap them — makes the inference mechanism visible." |
| Mitigation 2 | "Below the draft, a small panel: 'Based on: your one-line ask + your 3 voice samples. Not based on: recipient's previous emails.'" |
| Evidence basis | "Inferred from 4 user interviews on the prototype; no formal validation yet — flagged as gap to retest after onboarding ships." |

## When the block is "complete enough"

When the user model is described, two misalignments are named, each has a
mitigation or accepted-risk note, and the team either has evidence or
explicitly acknowledges the model is inferred. Mental model is usually the
block teams most underestimate — pushing back here pays off.
