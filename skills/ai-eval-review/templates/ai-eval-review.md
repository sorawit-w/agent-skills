# AI Eval Review — {{PRODUCT_NAME}}

> Generated on {{DATE}}. AI type: {{AI_TYPE}}. Lifecycle: {{LIFECYCLE}}. Regulatory: {{REGULATORY_CONTEXT}}.
>
> Edit this file as the eval design evolves. Headings (`## Block N — …` and
> `## Gap Summary`) are load-bearing for downstream composability.

## Block 1 — Eval Necessity & Success Definition

- **Oracle question:** {{the one question that, if answerable, would tell you the AI is doing its job}}
- **AI-type family:** {{classification / regression / ranking / generation / retrieval / agentic}}
- **Offline criterion:** {{specific number on a specific eval set; "≥85% send-as-is on 50-example held-out" not "pass the eval"}}
- **Distance from oracle to criterion:** {{quantified correlation if known, or explicit "unmeasured"}}
- **Sanity check against user need:** {{how the success definition was validated against actual users, not just engineering taste}}

## Block 2 — Ground Truth & Label Quality

- **Label source(s):** {{hand-labeled by who, auto-extracted from what, self-labeled, bootstrapped — per eval cut}}
- **Annotator profile:** {{trade-off named — domain experts vs. crowd, internal vs. external, single vs. multi}}
- **Inter-annotator agreement:** {{measured kappa / pairwise rate, OR "single annotator with accepted noise ceiling"}}
- **Coverage gaps:** {{enumerated — what classes / segments / cases are NOT labeled}}
- **Generative eval strategy** (if applicable): {{rubric / pairwise / human-only / LLM-judge with human-verification path}}

## Block 3 — Offline Eval Design

- **Eval set size + composition:** {{N examples, stratified or random or curated, breakdown by axis}}
- **Distribution alignment to production:** {{checked vs. unmeasured; if checked, against what production sample}}
- **Leakage protection:** {{held-out from training; LLM-vendor contamination acknowledged; or accepted-risk note}}
- **Statistical power:** {{noise floor on the headline metric; what difference is meaningful}}
- **Stability across runs:** {{deterministic / N runs with variance / temperature-fixed}}
- **Baseline:** {{what you compare against — random, manual, previous model, deterministic alternative}}
- **Hard-negative coverage:** {{intentional vs. random; which difficult cases are over-represented}}
- **Calibration** (if probabilistic outputs): {{calibration measured or gap}}

## Block 4 — Online Metrics & Signal

- **Success-tracking metric:** {{the metric closest to Block 1's oracle, with proxy-relationship named}}
- **Proxy vs. direct (per metric):** {{explicit statement of which metrics approximate vs. directly measure}}
- **Failure signal:** {{a metric independent of engagement that catches silent degradation}}
- **Counter-metrics:** {{metrics designed to NOT improve — flag adversarial optimization}}
- **Per-cohort visibility:** {{dashboard breakdown axes; connects to Block 5}}
- **Latency + cost:** {{instrumented at the lifecycle-appropriate level, or explicit deferral}}
- **User feedback affordance:** {{thumbs / explicit-flag / inline-correction — how users surface failures}}
- **Sample size / noise:** {{daily / weekly noise floor on the headline metric}}

## Block 5 — Cohort Breakdown & Disparate Impact

- **Cohort dimensions measured:** {{at least three; if fewer, name the blind spot explicitly}}
- **Worst-served cohort:** {{name, size, performance gap vs. aggregate}}
- **Disparate-impact threshold:** {{the bar — 80% rule, 90% rule, or explicit absence}}
- **Harm distribution:** {{harm-prevalence per cohort if failures can harm users}}
- **Why the gap exists:** {{data-side / model-side / product-side cause}}
- **Mitigation stance:** {{queued / shipped / accepted-risk}}
- **Regulatory cross-check:** {{EU AI Act / FDA SaMD / FTC where applicable}}
- **Accessibility cohort:** {{measured or explicit gap}}

## Block 6 — Adversarial & Robustness

| Failure mode | Severity | Eval set | Resistance rate | Notes |
|--------------|----------|----------|-----------------|-------|
| {{e.g., prompt injection — direct}} | {{embarrassing / user-harming / company-liability / regulatory}} | {{name + size}} | {{%}} | {{...}} |
| {{indirect injection}} | {{...}} | {{...}} | {{...}} | {{...}} |
| {{jailbreak — generic}} | {{...}} | {{...}} | {{...}} | {{...}} |
| {{multi-turn drift / OOD / adversarial perturbation, as applicable}} | {{...}} | {{...}} | {{...}} | {{...}} |

- **Red-team coverage:** {{who tested, where the gaps are}}
- **Severity tiering applied:** {{eval rigor proportional to consequence}}
- **Cross-check with `ai-ux-review` Block 6** (if present): {{do designed mitigations have measurement signal here?}}

## Block 7 — Drift Detection & Monitoring

- **Model drift detector:** {{canary set / cadence / alert threshold, or "we accept this drift type isn't monitored"}}
- **Behavior drift detector:** {{distribution check / cadence / alert threshold}}
- **Data drift detector:** {{embedding-distance / population-stability / explicit absence}}
- **Retraining cadence** (if applicable): {{schedule and decision authority}}
- **Model-vendor drift handling:** {{pinned snapshot / post-update eval / accepted-risk note}}
- **Alert ownership:** {{person / rotation / channel + SLA}}
- **Silent-drift scenario:** {{the failure mode that would NOT trigger headline-metric alarms + the defense}}
- **Eval-set refresh cadence:** {{stated cadence + whether it's been practiced yet}}
- **Runbook:** {{exists at path X / tabletop-validated / explicit gap}}

---

## Gap Summary

The three to five most urgent unmade eval decisions. For each: the gap in
plain language, why it matters, and the cheapest experiment to resolve it.

1. **{{Gap in one line}}**
   - Why it matters: {{which block surfaced it; what fails without it}}
   - Cheapest experiment to resolve: {{specific test, ideally <1 week}}

2. **{{Gap in one line}}**
   - Why it matters: {{...}}
   - Cheapest experiment to resolve: {{...}}

3. **{{Gap in one line}}**
   - Why it matters: {{...}}
   - Cheapest experiment to resolve: {{...}}

---

*This review was produced by the `ai-eval-review` skill in
[sorawit-w/agent-skills](https://github.com/sorawit-w/agent-skills). Informed
by [HELM](https://github.com/stanford-crfm/helm) (Apache 2.0), [Anthropic's
claude-cookbooks](https://github.com/anthropics/anthropic-cookbook) (MIT),
[OpenAI Evals](https://github.com/openai/evals) (MIT), and EU AI Act / FTC /
FDA SaMD regulatory texts; authored from first principles. See the skill's
README for the full influences note.*
