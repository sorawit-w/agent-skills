<p align="center">
  <img src="https://raw.githubusercontent.com/sorawit-w/agent-skills/main/assets/ai-eval-review-li.svg" alt="ai-eval-review — design-completeness review for the eval layer of AI products" width="100%"/>
</p>

# ai-eval-review

Audit the **evaluation layer** of an AI product or feature against a structured set of design-completeness questions — and produce both an editable Markdown artifact and a self-contained HTML visualization you can open, share, or print to PDF.

This skill is the **sibling of `ai-ux-review`**. Same shape, same elicitation pattern, different subject. Where `ai-ux-review` asks *was the human-AI design intentional?*, `ai-eval-review` asks *do we have signal for whether the design works?*. Run both for a complete review.

The job is **eval-design-completeness**: have we defined what "good enough to ship" means, do we have ground truth, is our offline eval rigorous, what do we measure in production, who does the AI work for and not work for, how does it fail under stress, and how do we know it's still working tomorrow? Seven blocks. Six mandatory cross-block checks. Gap Summary that names the unmade decisions with cheapest-experiment-to-resolve.

This is **not** an eval implementation tool. It names the eval gaps and helps decide *what* to measure. It does not write the eval code, build the labeling pipeline, configure W&B / Evidently / Arize, or run benchmark suites. Implementation lives in your team's eval platform.

## What it does

- **Phase 0 — Intake.** Resolves the output path (shares `docs/ai-ux/` with `ai-ux-review` by convention), scans for adjacent artifacts (`ai-ux-review.md` Block 7 gaps seed Block 1 here; `validation-canvas.md` informs Block 5; `DESIGN.md` styles the HTML), confirms four intake facts — what the AI does, AI type, lifecycle stage, regulatory context — in one line.
- **Phase 1 — Block-by-block elicitation.** Walks seven blocks in fixed reasoning order (necessity → ground truth → offline eval → online metrics → cohorts → adversarial → drift). Roles active: `@data_scientist`, `@ai_system_architect`, `@ai_safety_specialist`, `@senior_product_manager`, `@legal_compliance_advisor`. Specificity gate rejects category answers; gaps are first-class outputs marked `[Gap — …]`.
- **Phase 2 — Cross-block stress test.** Six mandatory checks (necessity ↔ online, ground-truth ↔ offline, cohort ↔ ground-truth, adversarial ↔ ai-ux-review Block 6, drift ↔ online, all ↔ lifecycle) plus a regulatory cross-cutting lens (EU AI Act, FDA SaMD, FTC).
- **Phase 3 — Render & ship.** Two files:
  - `ai-eval-review.md` — canonical Markdown with one H2 per block plus `## Gap Summary` (3–5 unmade decisions with why-it-matters + cheapest-experiment).
  - `ai-eval-review.html` — self-contained HTML rendering the seven blocks as a 3+3+1 grid with `[GAP]` chips on blocks with unresolved decisions, Gap Summary footer. Block 6 includes an adversarial-eval table (failure mode × severity × eval set × resistance rate).
- **Sibling-aware.** When `ai-ux-review.md` exists in the working folder, Block 7 (Success & Evaluation) gaps from that review seed Block 1 here. The Phase 2 check explicitly cross-references the two skills' Block 6 — designed mitigations in ai-ux-review should have measurement signal here.
- **Closes with three lines:** the highest-urgency unresolved eval decision, the cheapest experiment to resolve it, the next step.

## What it doesn't do

- **Not an eval implementation tool.** Names what to measure, not how to instrument it. For implementation: HELM, Anthropic's claude-cookbooks, OpenAI Evals, Weights & Biases, Evidently, Arize, or your team's preferred platform.
- **Not a benchmark suite.** Doesn't run MMLU, HELM benchmarks, or your eval set. Helps you decide which benchmark or custom set fits.
- **Not a substitute for `ai-ux-review`.** Different surface, different failure modes. Use both.
- **Not a regulatory compliance assessment.** Surfaces EU AI Act / FDA SaMD / FTC hooks as a cross-block lens; does not certify compliance. For formal submissions, escalate to `team-composer` with `@legal_compliance_advisor`.
- **Not a model-quality benchmark.** Doesn't tell you whether your model is good. Tells you whether you have the design in place to *know*.
- **Not a pitch-deck builder.** Pitch construction belongs to `pitch-deck`.

## When to use it

- You're about to ship an AI feature and want a structured pre-launch eval review — not "we ran some tests," a forced walk through the decisions that quietly get skipped (ground-truth quality, cohort breakdown, adversarial coverage, drift detection).
- You already shipped and you're discovering eval gaps in production (a cohort underperforming, a metric that turned out to be a proxy, drift you didn't see coming).
- You completed `ai-ux-review` and Block 7 (Success & Evaluation) surfaced gaps — this skill picks them up.
- You're in a regulated context (EU AI Act high-risk, FDA SaMD, FTC adjacent) and need to ensure eval rigor is proportional to risk class.
- A data-science colleague asked "how rigorous is our eval, really?" and the answer isn't structured enough to defend.

## When to use something else

- **Human-AI UX design review** → `ai-ux-review` (the sibling — different surface, same shape).
- **Business model / lean canvas** → `validation-canvas`.
- **Adversarial pre-mortem with a verdict** → `startup-grill`.
- **One narrow discussion** (just ground truth, just cohorts) → `team-composer` with `@data_scientist` + `@ai_safety_specialist`.
- **SKILL.md rule-adherence audit** → `skill-evaluator`.
- **Actual implementation** (label data, write eval code, set up dashboards) → your team's eval platform.
- **Formal regulatory compliance** → `team-composer` with `@legal_compliance_advisor`.

## How it works

Three phases, all in one Claude session.

**Phase 0 — Intake (immediate, before block work).** Resolves output path (shared with `ai-ux-review` when present). Scans for adjacent artifacts. Establishes four intake facts (what the AI does, AI type, lifecycle, regulatory). Mirrors framing in one line.

**Phase 1 — Block-by-block elicitation.** Seven blocks in fixed reasoning order. Each block uses primary probe to elicit a specific eval decision; gaps are explicitly marked. Specificity gate rejects category answers ("we measure accuracy") and forces a real decision or a real `[Gap — ...]`.

**Phase 2 — Cross-block stress test.** Six mandatory cross-checks + regulatory cross-cutting lens. Gap Summary written with 3–5 most urgent unmade decisions, each with cheapest-experiment-to-resolve.

**Phase 3 — Render & ship.** Markdown + HTML written to `docs/ai-ux/` (or kit-orchestrator path). Three closing lines: the most urgent gap, the cheapest experiment, the next step.

## What the output looks like

```
<your-working-folder>/
└── docs/
    └── ai-ux/
        ├── ai-ux-review.md       (sibling — if you ran ai-ux-review)
        ├── ai-ux-review.html     (sibling)
        ├── ai-eval-review.md     this skill's output
        └── ai-eval-review.html   this skill's output (visual primary)
```

The HTML renders the seven blocks as cards in a 3+3+1 grid. Block 6 (Adversarial & Robustness) includes a failure-mode × severity × eval-set × resistance-rate table. The teal accent (vs. ai-ux-review's warm orange) makes the sibling relationship visually legible when both reviews are open.

## Design choices worth knowing

- **Seven blocks, sibling shape to `ai-ux-review`.** Both skills carry seven blocks in a 3+3+1 layout for visual + structural parity. The block subjects differ, but the elicitation pattern (primary probe → secondary probes → acceptance criteria → explicit gaps) is identical.
- **Regulatory rigor is a cross-cutting lens, not its own block.** EU AI Act / FDA SaMD / FTC apply *across* blocks. Treating regulation as a separate block compresses it into a checklist; treating it as a lens forces it to influence eval rigor where it actually applies (Blocks 2, 4, 5, 6, 7).
- **Block 1 (necessity) ≠ Block 4 (online metrics).** The most common failure mode in AI evals is conflating the success target with the production metric. Block 1 is the oracle question; Block 4 is the signal that approximates it. The proxy-vs-direct relationship between them must be named honestly.
- **Block 2 (ground truth) is the substrate for everything.** A 0.9-model on 0.6-quality labels has a 0.6 ceiling, full stop. This block surfaces label-quality debt that teams typically treat as solved.
- **Block 5 carries responsible-AI weight as a first-class block.** Cohort breakdown and disparate impact aren't a footnote — they're a dedicated block. Mirrors `ai-ux-review`'s decision to make Block 6 (Output Integrity) a first-class gen-AI surface rather than a sub-bullet.
- **Block 6 boundary with `ai-ux-review` Block 6 is explicit.** Design intent (was injection mitigation designed?) lives in `ai-ux-review`; measurement (do we measure injection resistance?) lives here. The Phase 2 check cross-references them.
- **Eval-set freshness matters.** Block 7 explicitly asks about eval-set refresh cadence. Stale eval sets are a silent failure mode — the eval measures yesterday's product, not today's.
- **The skill names gaps; it doesn't close them.** Closing eval gaps is implementation work (label data, instrument metrics, build pipelines) that lives outside any skill. The "cheapest experiment" in Gap Summary is the bridge to implementation.
- **Zero network dependencies in the HTML.** Same constraint as `ai-ux-review`.

## Influences

This skill is informed by multiple open eval frameworks and regulatory texts. Each is cited with attribution; none are reproduced verbatim. The skill uses general eval-design concepts (the kinds of decisions to make) and authors its own elicitation flow.

| Influence | License | Relevance |
|-----------|---------|-----------|
| [HELM](https://github.com/stanford-crfm/helm) — Stanford CRFM | Apache 2.0 | Multi-dimensional eval (accuracy, calibration, robustness, fairness, bias, toxicity, efficiency). Influences Blocks 3, 5, 6. |
| [Anthropic's claude-cookbooks](https://github.com/anthropics/anthropic-cookbook) | MIT | Patterns for LLM eval design. Influences Block 3 (offline eval design). |
| [OpenAI Evals](https://github.com/openai/evals) | MIT | Framework + benchmark registry. Influences Block 3 (offline eval design) and the implementation-handoff framing. |
| [EU AI Act](https://artificialintelligenceact.eu/) | EU regulatory text, reusable with attribution | High-risk system requirements drive Block 2 (data quality), Block 5 (representativeness), Block 6 (robustness), Block 7 (post-market monitoring). |
| FTC AI guidance | US federal work, public domain | Influences Block 5 (disparate impact) and Block 6 (truthfulness). |
| FDA SaMD eval expectations | US federal work, public domain | Influences how regulatory rigor scales with risk class — applied as cross-cutting lens. |

**License compliance.** Copyright protects expression, not ideas or general design concepts. This skill uses ideas about how to think about evals — what to label, what to measure, what cohorts to consider — in its own voice with its own elicitation flow. No verbatim content (worksheets, benchmark schemas, regulatory text) is reproduced. Each influence is named with attribution; the skill is not a derivative work of any of them.

## Install

This skill is distributed as a [Claude Code](https://docs.claude.com/en/docs/claude-code) plugin inside the [`sorawit-w/agent-skills`](https://github.com/sorawit-w/agent-skills) marketplace. From Claude Code or Cowork:

```
/plugin marketplace add sorawit-w/agent-skills
/plugin install agent-skills@sorawit-w
```

Installing the `agent-skills` plugin brings the whole shelf, including this skill.

## Related skills

- **`ai-ux-review`** — sibling skill. Different subject, same shape. Run both for a complete review of an AI product. This skill reads `ai-ux-review.md` Block 7 gaps as input when present.
- **`validation-canvas`** — upstream when the product is idea-stage. Block 5 (Cohort breakdown) reads Customer Segments.
- **`brand-workshop`** — upstream when a brand identity exists. This skill reads `<brand-root>/DESIGN.md` to style the HTML output.
- **`team-composer`** — alternative for one-block discussions (e.g., "let's debate ground-truth labeling strategy") rather than a full review artifact.
- **`riskiest-assumption-test`** — composition. When the Gap Summary surfaces eval assumptions that need *testing* (not just deciding), hand them to RAT.
- **`startup-grill`** — adjacent. Adversarial pre-mortem with verdict. Different mode from this skill's cooperative gap detection.
- **`pitch-deck`** — downstream. Strong eval decisions seed traction / validation slide content.

## Status and scope

**Supported:** first-pass eval-design review for a single AI product or feature. Update-mode runs (loop-back when the file already exists). All AI types — LLM, classical ML (classification / regression / ranking / recommendation), CV, multi-modal, agentic — with type-specific Block 6 probes.

**Not supported:** multi-feature review in a single artifact (run the skill once per feature), eval pipeline implementation, dataset labeling, dashboard configuration, formal regulatory submissions, model-quality benchmarking, A/B test design (use `riskiest-assumption-test` for hypotheses).

**Versioning.** Initial release at the plugin version that introduces it. Block structure is load-bearing — adding or renumbering blocks is a MINOR bump at minimum.

## Contributions

Not accepting external contributions right now — feel free to fork. Issues and suggestions welcome via [GitHub](https://github.com/sorawit-w/agent-skills/issues).

## License

MIT. See repo `LICENSE`. The skill text is MIT-licensed and contains no verbatim content from any of the cited influences. See "Influences" above for the full attribution and copyright-vs-derivative-work reasoning.
