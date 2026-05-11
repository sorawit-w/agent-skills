# Block 5 — Cohort Breakdown & Disparate Impact

## Definition

Per-segment performance. Aggregate metrics hide cohort-level failures — a feature that "works on average" can fail catastrophically for a minority of users while the headline number looks fine. This block surfaces those failures and forces the question: who does this AI work for, and who does it not work for?

This block carries the responsible-AI eval weight in the skill. Fairness, disparate impact, and harm distribution all live here. The block is also where the EU AI Act high-risk requirements (representativeness, bias mitigation) and FTC AI guidance (disparate impact) most directly apply.

## Primary probe

> "Of all the users your AI serves, name the segment for whom it works *worst*. How do you know? What's the size of that segment, and what's the gap between their performance and the aggregate?"

## Secondary probes

1. **Cohort enumeration.** Which segmentation dimensions matter — demographic, geographic, language, user tenure, use-case, input length, input modality, accessibility (screen readers, low vision), device class? Many AI products only segment on use-case and miss the demographic / accessibility cuts.
2. **Per-cohort eval set.** Is each cohort represented in Block 3's eval set? An "African American Vernacular English" cohort can't have measured performance if the eval set has no AAVE examples.
3. **Disparate-impact threshold.** What gap between best-served and worst-served cohort is acceptable? The "80% rule" (FTC / EEOC tradition) is one anchor; some teams set tighter (90%). Name the bar.
4. **Harm distribution.** For products with failure modes that can harm users (financial advice, medical info, legal info, identity), is harm-prevalence measured per cohort? "Hallucination rate" may be 2% aggregate but 12% for one segment.
5. **Why does the gap exist?** Data-side (less training data for cohort), model-side (model fails on certain language patterns), product-side (UI assumptions break for cohort)? Different causes have different fixes.
6. **What's the mitigation strategy?** Re-sampling training data, reweighting metrics, per-cohort thresholding, surfacing the limitation, declining to serve the cohort? Each has trade-offs.
7. **Regulatory hooks.** EU AI Act high-risk requires "representative" datasets. FTC has stated that AI products causing disparate impact may violate consumer-protection laws. FDA SaMD requires evaluation across demographic groups for clinical products. Surface where regulation changes the bar.
8. **Stated trade-offs.** Sometimes you can't close a gap without making a different cohort worse. Name the trade-off explicitly; document the choice.

## Acceptance criteria

- [ ] **At least three cohort dimensions** enumerated and measured (or explicit acknowledgment of "we only segment by X and accept the blind spot").
- [ ] **Worst-served cohort named** with size and performance gap.
- [ ] **Disparate-impact threshold** stated (a number or "we don't have a formal threshold and that's a gap").
- [ ] **Harm distribution** measured for failure modes with user-impact (or explicit "this AI's failure modes are low-stakes — no harm measurement needed").
- [ ] **Mitigation stance** named for the largest cohort gap.
- [ ] **Regulatory cross-check** if context is non-trivial.

## Common gap patterns

- **Aggregate-only metrics.** Block 5 simply doesn't exist; nobody computes per-cohort performance. Most common gap in this block.
- **Use-case segmentation only.** The team segments by feature usage (power user / casual user / new user) but not by demographic / accessibility / language. Misses the cohorts where harm tends to land.
- **Cohort imbalance hidden.** Some cohorts have <50 examples in the eval set; their per-cohort scores are noise. Reporting them anyway creates false confidence; not reporting hides the gap.
- **"AI doesn't see demographics."** True for the input pipeline but false for the outcomes. A model trained on a non-representative corpus produces non-representative outputs regardless of whether demographics are explicit inputs.
- **Bias as a "fix later" item.** Disparate impact identified but mitigation deferred indefinitely. Ships anyway. Becomes a regulatory liability and a customer-trust liability.
- **No accessibility cohort.** Users with screen readers / motor disabilities / low-vision are almost never a measured cohort. The AI may interact terribly with assistive tech and nobody knows.
- **Single-axis disparate impact.** Measured along race OR gender OR age, but not intersectionally. Black women may be served worse than Black men or white women individually, in ways single-axis analysis misses.
- **Regulatory blind spot.** Team isn't aware that their domain is regulated (e.g., a fintech AI that's an "advice tool" may be regulated as a credit decision tool depending on use). Block 0 should have flagged this; if not, do it here.

## Worked example (LLM email drafting)

| Field | Filled |
|-------|--------|
| Cohort dimensions measured | (1) User tenure: <30d / 30-90d / 90d+. (2) Email type: professional / casual / with-factual-claims. (3) Voice-sample availability: <3 samples / 3-10 / 10+. **[Gap]** No measured cohorts on: native vs. non-native English speakers; users with disabilities; geographic region. |
| Worst-served cohort | New users (<30d, ~25% of weekly active users) with <3 voice samples. Send-as-is rate: 38% vs. aggregate 65%. Gap: 27 percentage points. |
| Disparate-impact threshold | "We use 80% rule as a soft anchor: worst-cohort / best-cohort >= 0.8. New-user-low-samples cohort at 38% vs. best (long-tenure, 10+ samples) at 81% — ratio 0.47, well below threshold. Acknowledged gap, not yet mitigated." |
| Harm distribution | "Hallucination rate (factual span doesn't match user's ask): 1.8% aggregate. For 'with-factual-claims' cohort: 6.4%. For new-user-low-samples cohort: 2.4% (slightly elevated but not catastrophic). For 'with-factual-claims' new-user-low-samples: 9.1% (intersection effect — worst case)." |
| Why the gap exists | (1) Voice-sample inference works worse with <3 samples (data-side). (2) New users don't yet trust the override / regenerate paths — they accept first drafts more (product-side, connects to ai-ux-review Block 3 trust calibration). |
| Mitigation strategy | "Two mitigations queued: (a) Lower the voice-sample prompt threshold from 3 to 1 for first-time users; show samples-collection onboarding inline. (b) For new users, default to 'show the basis chip prominently' instead of the collapsed default. **[Gap]** Mitigations haven't shipped; cohort gap is acknowledged but not closed." |
| Regulatory cross-check | "Consumer-trust-sensitive product, no formal regulatory regime. FTC AI guidance is relevant: 'AI tools that work better for some groups may risk disparate impact claims.' Documented for record. Not yet a compliance issue, but the trajectory matters." |
| Accessibility | "[Gap] Not measured. Screen-reader compatibility of the draft UI hasn't been eval'd. Likely fine (it's text), but the chip / voice-sample UI hasn't been audited." |

## When the block is "complete enough"

When at least three cohort dimensions are measured (with explicit acknowledgment of gaps for unmeasured cohorts), the worst-served cohort is named with size and gap, a disparate-impact threshold exists or is explicitly absent, harm distribution is per-cohort where harm exists, mitigation has a stance (even if "acknowledged, not yet shipped"), and regulatory context is at the right altitude.

This block surfaces the most reputationally damaging gaps. Push hard.
