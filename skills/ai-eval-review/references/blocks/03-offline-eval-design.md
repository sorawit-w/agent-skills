# Block 3 — Offline Eval Design

## Definition

Pre-launch rigor: the composition of the eval set, the distribution it covers, the leakage protection, and the statistical power to detect the differences you care about. This is the bridge between Block 1 (success definition) and Block 4 (online signal) — offline eval is the last gate before production.

A pretty score on a small or skewed eval set is one of the most common failure modes in shipping AI. Block 3 is where that failure is caught before launch — or surfaced as a gap if it isn't.

## Primary probe

> "If your offline eval scores went up 5 points tomorrow, what would you actually be able to conclude? Specifically — about which inputs, which user populations, in which conditions?"

## Secondary probes

1. **Eval set composition.** How many examples? Broken out how (by task type, user segment, difficulty, source)? Random sample, stratified, or hand-curated? Each choice has different consequences for what scores actually mean.
2. **Distribution alignment.** Does the eval set's distribution match production? If 70% of production traffic is short asks and 30% is long, but the eval set is 50/50, your aggregate score is meaningless for production.
3. **Leakage protection.** If you're using LLMs, did any of your eval set show up in training data (model-side leakage)? If you have a custom fine-tuned model, did examples leak from train to eval? Without leakage protection, scores are arbitrarily inflated.
4. **Statistical power.** With your eval set size, what difference in score is statistically meaningful? A 50-example eval set has wide confidence intervals — a 1-point F1 improvement might be noise.
5. **Stability across runs.** If you ran the same eval twice on the same model, would you get the same score? Non-deterministic LLMs need multiple runs aggregated. Sampling-temperature matters.
6. **Hard-negative coverage.** Easy examples are easy. Hard examples are where you actually need signal. Does your eval set over-represent easy cases? Hard examples should be intentionally curated, not just random.
7. **Baseline comparison.** What's the no-AI baseline? Random guess? Best deterministic alternative? A model that scores 0.85 isn't impressive if the baseline scores 0.83.
8. **Calibration.** For probabilistic outputs: when the model says it's 80% confident, is it actually right ~80% of the time? Miscalibrated confidence is invisible in headline accuracy but kills trust calibration (ai-ux-review Block 3).

## Acceptance criteria

- [ ] **Eval set size and breakdown** stated explicitly.
- [ ] **Distribution alignment to production** explicitly checked, OR an acknowledgment that alignment is unmeasured.
- [ ] **Leakage protection** named (held-out from training; LLM-providers' contamination acknowledged; or explicit "we accept some contamination because…").
- [ ] **Confidence interval / variance** estimated for the headline score.
- [ ] **Baseline named.** What you're comparing your model against.
- [ ] **Hard-negative or edge-case coverage** intentional, not just random sampling.

## Common gap patterns

- **Random 50-example eval set.** Common in early-stage AI work. Random examples over-represent easy cases; small N produces wide confidence intervals; you can't make any segment-level claims.
- **Production-distribution drift unmeasured.** The eval set was curated 6 months ago; production traffic shifted. Aggregate scores no longer reflect production.
- **LLM leakage unconsidered.** Using GPT-4 to evaluate a benchmark that's been in GPT-4's training data. Scores inflated; comparisons across model versions invalid.
- **Single-run scores treated as ground truth.** Non-deterministic LLMs have variance run-to-run. A 1-point score difference might be sampling noise. Run multiple times, report mean + variance.
- **No baseline.** "Model scores 0.85" without comparison to "random guess scores 0.5" or "previous version scores 0.83" or "rule-based baseline scores 0.80." Without baseline, scores are uncalibrated.
- **All-easy eval set.** "We curated examples we thought would be representative." Curation toward easy is the default human bias. Hard negatives must be intentionally sought.
- **Calibration ignored.** Model outputs a confidence score; the eval reports accuracy. Calibration is never measured. Users see the confidence and trust accordingly, often wrongly.

## Worked example (LLM email drafting)

| Field | Filled |
|-------|--------|
| Eval set size | 50 examples graded fully (labeled in Block 2). 800 examples used for automated rubric pre-filtering (LLM-as-judge). |
| Composition | Stratified: 35% one-line professional asks, 25% personal/casual, 20% with factual claims to preserve, 15% multi-turn correction asks, 5% refusal-required. |
| Distribution alignment | "Approximated from 2 weeks of beta-user logs. Beta isn't fully production yet — gap acknowledged. We'll re-sample after public launch." |
| Leakage protection | "Eval examples drawn from beta users who opted out of training-data inclusion. LLM contamination from base model is acknowledged but not measured — accepted risk for v1." |
| Statistical power | "n=50 with binomial CI: a 10-point difference in send-as-is rate has ~90% power. Smaller differences are noise. We don't claim improvements smaller than 10 points." |
| Stability across runs | "Eval run 3 times per model version; report median + range. Temperature fixed at 0.3 for eval consistency." |
| Hard-negative coverage | "20% of eval set is the 'with factual claims' cohort — hardest cases (where hallucination risk is highest). Intentionally over-represented vs. production distribution to stress-test Block 6 mitigations." |
| Baseline | "Template library + best-tone-match — the manual override path from `ai-ux-review` Block 4. Baseline scores 'send-as-is or minor-edits' at 42%. AI version scores 71%. Improvement is 29 points (well above noise floor)." |
| Calibration | "[Gap] We surface a voice-match chip but don't measure whether the chip's claimed match correlates with annotator pairwise judgment. Add calibration check before next eval cycle." |

## When the block is "complete enough"

When eval set composition is stated, distribution alignment is checked or honestly flagged, leakage protection has a stance, statistical power is acknowledged (not necessarily formal — even "we know n=50 limits us to ~10-point claims" is enough), a baseline exists, and hard-negative coverage is intentional.

This block is where engineering rigor most often surfaces gaps that PM-driven discussions miss. Push hard on statistical power and baseline — those two alone catch most "the model is great" claims that don't survive contact with production.
