# Block 1 — Why AI here?

## Definition

The necessity check. What human task is the AI doing, and what makes AI the
right tool here as opposed to a deterministic alternative (rules, templates,
look-up tables, structured forms, human review)?

Why this block goes first: every later block inherits a posture from this
one. A feature where AI is *necessary* (open-ended generation, large
unstructured inputs, judgment under ambiguity) must take on the full cost
of integrity, trust, and error handling. A feature where AI is *optional*
(could be solved by a sorted list or a regex) should justify the additional
complexity it imports.

## Primary probe

> "If you removed the AI from this feature, what would the user lose? Be
> specific. 'It wouldn't work as well' is not specific."

## Secondary probes

1. **What was the user doing before this AI existed (or in the manual
   alternative)?** Force the comparison. The before-state names the
   benchmark the AI must clear.
2. **What's the simplest non-AI alternative?** A form. A template library.
   A search box over a curated corpus. A rule. If the simplest non-AI
   alternative is "not bad," the AI must justify why it's enough better
   to take on the integrity surface.
3. **Where does the AI's value actually come from — generation, ranking,
   classification, summarization, extraction?** Different sources of value
   imply different design constraints in later blocks.
4. **Who decided AI was the right tool here?** A product manager assuming
   AI is the right answer is different from a user research insight saying
   "users repeatedly tried to phrase open-ended requests."

## Acceptance criteria

- [ ] **Stated user task.** A specific user goal in user words, not in
      product-team words. "Get a usable email draft from a one-line ask"
      is good. "Improve email productivity" is not.
- [ ] **Named non-AI alternative.** A specific simpler tool that *would*
      partially solve the task. "A form with required fields" is good.
      "Doing it manually" is too vague.
- [ ] **Reason AI wins.** A specific dimension the AI clears: open-ended
      input handling, scale, latency, personalization, judgment under
      ambiguity. "It's smarter" is not specific.
- [ ] **Cost acknowledged.** The reviewer names at least one cost the AI
      imports (probabilistic output, hallucination risk, latency, opacity)
      that the non-AI alternative doesn't have.

## Common gap patterns

- **"AI because that's the strategy."** The feature exists because
  leadership wants AI features, not because the user task requires it.
  Surface this gap explicitly — it predicts every other block being
  shallow.
- **"AI because the inputs are unstructured."** Real but usually not
  enough. Many unstructured-input problems can be solved with templates +
  fuzzy matching. Press for the actual unstructured-input dimension that
  resists rules.
- **"AI because LLMs are good at this."** A capability claim, not a user
  claim. Reframe: what does the user gain from the LLM being good at
  this?
- **No stated alternative.** If the team can't describe a simpler
  alternative, they haven't considered whether AI was necessary. This is
  the most common gap in this block.

## Worked example (LLM email drafting)

| Field | Filled |
|-------|--------|
| Stated user task | "Send a polite, on-brand cold email to a specific person based on a one-line description of what to say" |
| Non-AI alternative | "Template library with 12 tones × 6 lengths, user picks the closest and edits" |
| Reason AI wins | "User's one-line description usually encodes context (relationship, tone) the user can't articulate in advance for template-picking" |
| Cost acknowledged | "AI may produce on-brand-looking text that misstates a fact the user didn't intend to make" |

The cost acknowledged becomes a load-bearing input to Block 6 (Output
integrity) — the team has explicitly named what could go wrong.

## When the block is "complete enough"

This block is rarely interesting on its own — its job is to set up the
later blocks honestly. If the four acceptance criteria are answered with
specificity, move on. If the team can't answer them, that itself is the
finding: the product hasn't decided why AI is necessary, which means every
downstream design choice rests on an unexamined assumption.
