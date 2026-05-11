# Block 1 — Eval Necessity & Success Definition

## Definition

The anchor. What does "good enough to ship" actually mean for this AI feature? What is the offline criterion that, if cleared, says the AI is doing its job? This is the eval-side equivalent of `ai-ux-review`'s "why AI here?" — the question every later block inherits from.

Block 4 (online metrics) is downstream. Block 1 is the *target* — the thing online metrics are trying to track. Conflating the two is the dominant failure mode of AI product evals: teams build a metric, optimize the metric, and never check whether the metric actually correlates with the target.

## Primary probe

> "If I gave you a magic oracle that could answer one question about every output your AI produces, what would the question be? Write it down. That's your success definition. Now: how close is your current offline eval to actually asking that question?"

## Secondary probes

1. **The oracle question.** What does the oracle actually evaluate — accuracy, helpfulness, faithfulness, on-brand-ness, safety, user task completion? Name it. Without naming, every later block drifts.
2. **What's the offline criterion?** A specific number on a specific test set that, if cleared, means "good enough to ship." If you don't have one, that's the gap. "We'll know it when we see it" is a gap, not an answer.
3. **What's the distance from oracle to offline criterion?** Real evals approximate the oracle. Quantify the approximation — e.g., "our offline F1 is a proxy for usefulness; we estimate ~0.7 correlation based on a 50-example spot check."
4. **AI-type-specific success.** Classification: accuracy / F1 / per-class precision-recall. Regression: MAE / MSE / calibration. Ranking: NDCG / MRR. Generation: human eval / pairwise / rubric. Retrieval: recall@k / MRR. Agentic: task completion / step-level correctness. Name the family.
5. **Has the success definition been validated against users?** A success metric that engineering invented in isolation often diverges from what users actually need. "We aligned with PMs" is weaker than "we ran 10 users through the eval set and rated outputs."

## Acceptance criteria

- [ ] **Named oracle question.** One sentence in plain language. "Did this draft accomplish the email task as the user intended?" is good. "Was the output high quality" is not.
- [ ] **Offline criterion.** A specific number on a specific eval set. "0.75 F1 on 800-example held-out set" is good. "Pass the eval" is not.
- [ ] **AI-type-specific metric family named.** Classification / regression / ranking / generation / retrieval / agentic.
- [ ] **Stated distance from oracle to offline criterion.** Either a quantified correlation estimate or an explicit acknowledgment that the distance is unmeasured.
- [ ] **Sanity check against user need.** Some signal that the success definition resembles what users actually value, not just what's easy to measure.

## Common gap patterns

- **"Accuracy" as the answer.** Accuracy is rarely the right metric for generative AI, ranking, or anything user-facing. If the answer is "accuracy," ask what accuracy is computing against and whether that's the oracle question.
- **No offline criterion at all.** "We'll see how it does in production." Shipping AI without a pre-launch bar is the dominant fast-startup failure mode. This is always a gap, even at idea-stage.
- **Proxy mistaken for direct.** Engagement, click-through, time-on-page treated as success metrics. They're proxies for satisfaction; satisfaction is a proxy for task completion. Name the chain.
- **Success definition lives in engineering.** PMs and users haven't seen the definition; engineers wrote it. Almost always diverges from what matters in production.
- **AI-type confusion.** Treating a generative LLM eval like a classifier eval (precision/recall on token match) misses what generative AI is actually doing. Name the family correctly.
- **Single-number summarization.** A single F1 / accuracy / score hides everything that matters. The success definition should be decomposable — by task type, by difficulty, by cohort (Block 5 territory).

## Worked example (LLM email drafting — continuing from ai-ux-review)

| Field | Filled |
|-------|--------|
| Oracle question | "If a recipient received this draft and the user sent it as-is, would the recipient interpret it the way the user intended?" |
| AI-type family | Generative (LLM). Eval family: human pairwise + rubric grading. NOT token-level overlap metrics. |
| Offline criterion | "On 50-example held-out set graded by 2 annotators: ≥85% of drafts rated 'send-as-is' or 'minor edits.' ≤2% rated 'misleading or wrong.' Below either threshold, don't ship." |
| Distance from oracle | "Annotator pairwise reflects the oracle reasonably well — they read the draft AND the original ask AND simulate recipient interpretation. Estimated ~0.85 correlation with the oracle. The 15% gap is mostly annotator disagreement on tone/voice." |
| Sanity check | "Eval set was built from 50 real user one-line asks (consenting, anonymized). User intent was extracted via follow-up survey: 'what did you actually want this draft to convey?' Annotators graded against THAT intent, not against the draft alone." |

## When the block is "complete enough"

When the oracle question is named in plain language, the offline criterion has a specific number and eval set, the AI-type family is correct, the distance from oracle to criterion is acknowledged (even if unmeasured), and there's some signal the success definition aligns with what users value.

Block 1 is the most-revisited block in update mode — when downstream blocks expose contradictions, the success definition is usually where they trace back to. Treat it as load-bearing.
