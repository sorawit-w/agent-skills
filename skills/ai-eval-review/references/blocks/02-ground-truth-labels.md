# Block 2 — Ground Truth & Label Quality

## Definition

The measurement substrate. Where do labels come from? Who labels them? What's the inter-annotator agreement? Where does ground truth not exist? Every later block's signal is bounded by the quality of this block — a 0.9 model on 0.6-quality labels has a 0.6 ceiling, full stop.

This block is the single biggest predictor of whether an eval is real or theater. Most AI teams treat labels as a solved problem when they're the central problem.

## Primary probe

> "Show me five examples from your eval set and tell me, for each: who labeled it, what they were instructed to label, and what evidence you have that another competent labeler would have produced the same label."

## Secondary probes

1. **Label source.** Hand-labeled (by who — engineers, PMs, paid annotators, domain experts, end users), auto-extracted (from rules or another model), self-labeled (user behavior treated as label), bootstrapped (model labels its own training data)? Each source has different failure modes.
2. **Annotator profile.** Same-team labelers know the product too well; crowd labelers don't know enough. Domain experts are expensive; novices are noisy. Name the trade-off you made.
3. **Inter-annotator agreement.** If two annotators label the same example, do they agree? Kappa / agreement-rate / pairwise consistency. <0.6 agreement means the label itself is poorly defined — eval signal will be capped at the agreement ceiling.
4. **Coverage gaps.** Where does ground truth not exist? Refusal cases, OOD inputs, edge-case user intents, multi-turn contexts. Name what's *not* in your labeled set.
5. **Label drift.** Did the labeling guidelines change over time? Were old labels re-graded? An eval set with mixed-vintage labels is silently inconsistent.
6. **Ground truth for generative outputs.** This is the hardest case. There's no single correct output. Strategies: rubric grading (specific criteria, multi-axis), pairwise preference (output A vs. B), human-only end-to-end (slow but valid), LLM-as-judge (fast but bias-prone — verify against humans). Name yours.
7. **The "right answer doesn't exist" honest case.** For some tasks (creative writing, open-ended questions, ambiguous user intent), there's no objective ground truth. Pretending there is creates false eval signal.

## Acceptance criteria

- [ ] **Named label source** per eval set (not one source for all — different cuts may use different sources).
- [ ] **Annotator profile** and the trade-off accepted.
- [ ] **Inter-annotator agreement** measured for at least one cut. Or an explicit "we use single annotator and accept the resulting ceiling" note.
- [ ] **Coverage gaps named.** What classes / segments / cases your labels don't cover.
- [ ] **Generative eval strategy** if applicable: rubric / pairwise / human-only / LLM-judge — with the verification step for LLM-judge.

## Common gap patterns

- **Single-annotator labels treated as ground truth.** The most common eval failure. A noisy label set lets a model trained to fit the noise score well. Inter-annotator agreement must exist for ground-truth claims.
- **Team members labeling their own product.** Built-in bias toward seeing the product work. Symptom: eval scores higher than user-facing reality.
- **LLM-as-judge without human verification.** A model judging another model's output can be very fast, very confident, and very wrong. Always validate LLM-judge against human labels on a subset, and report the agreement.
- **No coverage gap awareness.** "Our eval set has 1000 examples" without knowing which user behaviors / inputs / failure modes those 1000 cover. The 1001st example is where production fails.
- **Auto-extracted labels from user behavior.** "User didn't edit the AI's draft, so it was good." Conflates non-edit with satisfaction (could be: user didn't notice the error, gave up, was lazy). Common in click-through-as-success patterns.
- **Drift in labeling guidelines.** Guidelines were revised mid-data-collection; old labels carry old definitions. Symptom: model scores well on new examples and badly on old ones, with no model change between them.
- **Refusal / safety labels missing.** No examples of "the model should decline." Common gap; ai-ux-review Block 5 (Errors) often surfaces this dependency back to Block 2.

## Worked example (LLM email drafting)

| Field | Filled |
|-------|--------|
| Label source — main eval (50 ex) | Hand-labeled by 2 paid annotators familiar with email writing but not the product. Each labels independently; disagreements resolved by a third senior annotator. |
| Label source — refusal cases (20 ex) | Hand-labeled by 1 internal safety reviewer (gap noted: single annotator, agreement not measured). |
| Label source — voice-match cohort (50 ex) | Pairwise preference: annotator sees the AI draft AND 3 real emails from the user (anonymized samples), judges "does the draft match this writer's voice?" Inter-annotator agreement: 0.74 (good). |
| Inter-annotator agreement | Main set: 0.81 (good). Refusal cases: not measured (gap). Voice cohort: 0.74. |
| Coverage gaps | "[Gap] Multi-turn corrections (user responds to first draft asking for changes) — no labeled examples. [Gap] Languages other than English — eval set is English-only. [Gap] B2B vs. personal voice asymmetry — eval covers personal voice well, B2B sparsely." |
| Generative eval strategy | Rubric grading on three axes: factual correctness (did the draft preserve user's stated facts?), voice match (sample-based pairwise), tone-appropriateness (binary judgment with reasoning). LLM-as-judge tried for tone-appropriateness; agreed with humans 0.71. Used for triage; humans grade samples where LLM-judge disagrees with itself across reruns. |

## When the block is "complete enough"

When the label source is named per eval cut, the annotator profile is honest about trade-offs, inter-annotator agreement is measured (or explicitly accepted as not measured), coverage gaps are enumerated rather than papered over, and any LLM-as-judge use case has a human-verification path.

This block is where most eval reviews surface their biggest gap. Builders who think evals are "solved" usually have label-quality debt they haven't seen yet.
