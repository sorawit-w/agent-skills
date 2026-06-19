---
name: ai-eval-review
description: >
  Audit the evaluation layer of an AI product against design-completeness questions: offline
  criteria, ground-truth quality, online signal, cohort/disparate-impact, adversarial +
  robustness coverage, and drift detection. Eval-side companion to `ai-ux-review`. Produces an
  editable Markdown artifact plus a self-contained HTML report under `docs/ai-ux/`. Use when
  the user asks to "review my AI eval setup", "audit my eval design", "is my AI eval rigorous
  enough", "responsible-AI eval review", "fairness eval check", or "drift detection design",
  or ships an LLM/ML feature and wants an eval-rigor check. Invoke even if only one block is
  named — the others stress-test it. Does NOT trigger for: human-AI UX review
  (`ai-ux-review`); lean-canvas work (`validation-canvas`); adversarial pre-mortem with a
  verdict (`startup-grill`); SKILL.md audits (`skill-evaluator`); implementing eval pipelines,
  writing eval code, or labeling datasets (this skill names gaps, it does not build them).
metadata:
  tier: draft
---

# AI Eval Review

Audit the eval layer of an AI product or feature against a structured set of
design-completeness questions. Each of the seven blocks is a *gap detector* —
the value of this skill is whether the elicitation surfaces eval decisions
the builder hasn't made yet, not whether the artifact looks complete.

The job is **eval-design-completeness**: *have we designed how we'll know if
this works?* Covers offline criteria, ground-truth quality, online signal,
cohort breakdowns and disparate impact, adversarial / robustness coverage,
and drift detection. Regulatory rigor (EU AI Act, FDA SaMD, FTC) is a
cross-cutting lens applied across blocks, not a separate block.

This skill is the eval-side companion to `ai-ux-review`. Same shape, same
elicitation pattern, different subject — `ai-ux-review` audits the
human-AI design surface (was the experience intentionally designed?);
this skill audits the measurement layer behind it (do we have signal for
whether the design works?).

This is not an implementation tool. It does not write eval code, label
datasets, set up monitoring dashboards, or compute metrics. It names the
gaps; you take them to your tools or your team to close.

## What this skill produces

Always produced under the resolved review root (default
`docs/ai-ux/` — same folder as `ai-ux-review` for clean composition):

1. **`ai-eval-review.md`** — canonical, editable Markdown with one top-level
   section per block (seven blocks total), plus a `## Gap Summary` section
   listing the eval decisions still unmade. Headings are load-bearing if
   downstream tools (e.g., a future eval-plan or eval-task generator) need
   to grep them.
2. **`ai-eval-review.html`** — single self-contained HTML rendering the
   seven blocks visually, with `[GAP]` chips on blocks with unresolved
   decisions and a Gap Summary footer. Opens in any browser, prints
   cleanly to PDF, zero network dependencies.

Both files carry the same content — the HTML is the visual primary; the
Markdown is the source of truth.

## What this skill is NOT

- **Not an eval implementation tool.** Block 1 names what success means;
  Block 3 names how you'd measure it offline. The skill does not write
  the code, build the labeling pipeline, configure W&B / Evidently /
  Arize, or compute the metric. For implementation, point at HELM,
  Anthropic's eval cookbook, OpenAI Evals, or your team's preferred
  eval platform.
- **Not a benchmark suite.** It doesn't run MMLU, HELM, or your custom
  eval set. It helps you decide *which* benchmark or custom set fits
  your problem.
- **Not a substitute for `ai-ux-review`.** UX design and eval design are
  different surfaces. A product can have great evals on a poorly designed
  UX (users distrust accurate outputs); it can also have great UX on
  poorly evaluated AI (users trust outputs that are silently wrong). Both
  matter; use the two skills together.
- **Not a regulatory compliance assessment.** It surfaces regulatory hooks
  (EU AI Act, FDA SaMD, FTC AI guidance) as a cross-block lens, but does
  not certify compliance. For formal regulatory submissions, escalate to
  `team-composer` with `@legal_compliance_advisor`.
- **Not a model-quality benchmark.** It doesn't tell you whether your
  model is good. It tells you whether you have the design in place to
  *know* whether your model is good.
- **Not a pitch-deck builder.** Pitch construction belongs to `pitch-deck`.

## Skill Boundaries

| Skill | Owns |
|-------|------|
| `ai-ux-review` Block 6 (Output Integrity) | Design intent: how the product surfaces verifiability, provenance, prompt-injection mitigation, autonomy levels. *Was this designed?* |
| `ai-eval-review` Block 6 (Adversarial & Robustness) | Measurement: how robustness is tested — red-team coverage, injection-eval results, OOD detection accuracy, jailbreak rates. *Is this measured?* |

If both skills are run, treat them as a pair: `ai-ux-review` asks "did we design for X?", `ai-eval-review` asks "do we measure X?". The boundary is design vs. measurement.

When `ai-ux-review.md` already exists in the working folder, this skill reads it as context — Block 7 (Success & Evaluation) gaps seed Block 1 here. Don't re-elicit what's already been named.

> **Influences.** This skill is informed by several open eval frameworks and
> regulatory texts:
> - [Holistic Evaluation of Language Models (HELM)](https://github.com/stanford-crfm/helm) — Stanford CRFM, Apache 2.0. Multi-dimensional eval (accuracy, calibration, robustness, fairness, bias, toxicity, efficiency).
> - [Anthropic's claude-cookbooks](https://github.com/anthropics/anthropic-cookbook) — MIT. Patterns for designing and running LLM evals.
> - [OpenAI Evals](https://github.com/openai/evals) — MIT. Framework + registry of benchmarks.
> - [`GoogleChrome/modern-web-guidance-src`](https://github.com/GoogleChrome/modern-web-guidance-src) — Apache-2.0. Closed-loop calibration methodology: paired gold-standard + negative fixtures to prove a test discriminates the rule it claims to test, plus *opportunity* (`100% − unguided-pass`) and *uplift* (`guided − unguided`) vocabulary for measuring whether a feature actually helps. Applied here to Block 3 (offline eval set construction must include hard negatives) and Block 4 (online metrics should be framed against an unguided baseline when feasible).
> - [EU AI Act](https://artificialintelligenceact.eu/) — regulatory text, reusable with attribution. High-risk system requirements drive Block 5 cohort + Block 6 robustness probes.
> - FTC AI guidance, FDA SaMD eval expectations — US federal works, public domain.
>
> The skill uses general eval-design concepts (the kinds of decisions to
> make, not specific benchmark scores) and authors its own elicitation flow,
> probes, and acceptance criteria. No verbatim content lifted from any of
> the above sources. See `README.md` for the full influences note and the
> copyright-vs-derivative-work reasoning.
>
> For the gold+negative fixture pattern in concrete form, cross-reference
> [`skill-evaluator/references/calibration-loop.md`](../skill-evaluator/references/calibration-loop.md)
> rather than duplicating the methodology here.

---

## The Seven Blocks

Claude must internalize all seven before interviewing. Blocks follow the
reasoning order from "what is success?" → "what do we measure against?" →
"how do we measure?" → "what do we measure in production?" → "who does it
work for?" → "how does it fail?" → "how do we know it's still working?".

| # | Block | Core question |
|---|-------|---------------|
| 1 | **Eval necessity & success definition** | What does "good enough to ship" mean? What's the offline criterion that, if cleared, means the AI is doing its job? |
| 2 | **Ground truth & label quality** | Where do labels come from? Who labels them? What's the inter-annotator agreement? Where does ground truth not exist? |
| 3 | **Offline eval design** | What's the eval set composition? Distribution coverage? Leakage protection? Statistical power? |
| 4 | **Online metrics & signal** | What's measured in production? Direct vs. proxy. Failure signals that distinguish silent degradation from engagement. |
| 5 | **Cohort breakdown & disparate impact** | Per-segment performance. Fairness. Disparate impact. Which segments are under-served and how would you know? |
| 6 | **Adversarial & robustness** | Red-team coverage, prompt-injection eval, OOD detection, jailbreak resistance, distribution shift. |
| 7 | **Drift detection & monitoring** | How do you know the system is still working tomorrow? Model drift, behavior drift, data drift, alerting cadence. |

**Cross-block lens — Regulatory rigor.** EU AI Act (high-risk systems), FDA SaMD (risk-class-proportional eval), FTC AI guidance (disparate impact, deception). Not its own block — applied as a Phase 2 check across the seven, surfacing where regulatory rigor changes the bar for Blocks 1, 5, and 6 specifically.

See `references/blocks/01-necessity-success.md` through
`references/blocks/07-drift-monitoring.md` for each block's deep probe
questions, acceptance criteria, and common gap patterns. The skill body
uses these references lazily — read them when the phase calls for them,
not all up front.

---

## Phase 0: Intake (RUN FIRST, BEFORE ANY BLOCK WORK)

**Goal:** establish context — what's being reviewed, what AI type, what
lifecycle stage, what regulatory context, what adjacent artifacts exist.

### Step 0.1 — Resolve the review root

Look for these in order; first match wins:

1. **Explicit `output_dir` arg** → use as-is.
2. **`STARTUP_KIT_DOCS_ROOT` env var** → `${STARTUP_KIT_DOCS_ROOT}/ai-ux/`.
3. **Smart default — `docs/startup-kit/` exists** → `docs/startup-kit/ai-ux/`.
4. **Smart default — `docs/ai-ux/` exists** → `docs/ai-ux/` (sibling of an existing `ai-ux-review` run).
5. **Solo fallback** → `docs/ai-ux/`.

Both `ai-ux-review` and `ai-eval-review` share the `ai-ux/` folder by
convention — the human-AI design layer and its measurement layer belong
side-by-side.

If `ai-eval-review.md` already exists at the resolved root, this is an
**update-mode** run — see "Update mode" below.

### Step 0.2 — Scan for adjacent artifacts

Before asking questions, check for files this skill can read as context:

- **`<resolved-root>/ai-ux-review.md`** — if present, read it. **Block 7
  (Success & Evaluation)** is the load-bearing input: any `[Gap — …]`
  markers there seed this skill's Block 1. Mirror back the gaps and ask:
  *"`ai-ux-review` flagged these eval gaps: [list]. Should I seed Block 1
  from them, or are you starting fresh?"*
- **`<resolved-canvas-root>/validation-canvas.md`** — if present, this
  is an AI startup. Block 5 (Cohort breakdown) reads Customer Segments
  to anchor per-segment eval questions.
- **`<resolved-brand-root>/DESIGN.md`** — for HTML token styling, same
  pattern as `ai-ux-review`.
- **Eval plan / metric dashboard description / labeling guide** — if
  attached, read it. Don't re-ask for information already there.

### Step 0.3 — Establish four intake facts

Ask only the ones not already obvious from context:

1. **What's the AI doing?** One sentence. (Pulled from `ai-ux-review.md`
   Block 1 if it exists.)
2. **What kind of AI?** LLM, classical ML (classification / ranking /
   regression / recommendation), CV, multi-modal, agentic. This determines
   which Block 6 probes apply.
3. **Where in the lifecycle?** Pre-MVP / prototype / in development /
   shipped. Sets eval-rigor expectations.
4. **What regulatory context?** Unregulated / consumer-trust-sensitive /
   EU AI Act limited-risk / EU AI Act high-risk / FDA SaMD (any class) /
   FTC consent decree adjacent. This drives Phase 2's regulatory cross-
   check.

### Step 0.4 — Confirm framing in one line

Before proceeding to block work, mirror back the framing:

> *"Reviewing the eval layer for an LLM-powered email-draft feature, in
> development, no formal regulatory regime. Reading `ai-ux-review.md`
> Block 7 gaps — there are three. I'll seed Block 1 from them. Stop me
> if I should reframe."*

Then proceed to Phase 1.

### Hard rules for Phase 0

- **Never start block work without the four intake facts** (or their
  context-inferred equivalents).
- **Never re-elicit `ai-ux-review` Block 7 gaps when the file is present.**
  Read them. Mirror them back as Block 1 seeds. Confirm.
- **Never invent the regulatory context.** Ask. Misclassifying an
  EU AI Act high-risk system as unregulated invalidates the rest of the
  review.

---

## Phase 1: Block-by-Block Elicitation

**Goal:** Walk the seven blocks in order. For each, the output is either
a concrete eval decision or an explicit gap marker
(`[Gap — what hasn't been decided yet]`).

### Role setup

| Role | Lens |
|------|------|
| `@data_scientist` | Lead interviewer. Asks block-by-block. Pushes for specificity on labels, metrics, statistical rigor. |
| `@ai_system_architect` | Eval orchestration, infrastructure realism, where eval lives in the system. |
| `@ai_safety_specialist` | Blocks 5 + 6 (cohorts + adversarial). Flags disparate-impact gaps and red-team coverage. |
| `@senior_product_manager` | Block 1 + 4 (necessity + online signal). Flags vague success criteria and proxy metrics treated as direct. |
| `@legal_compliance_advisor` | Cross-block regulatory lens. Surfaces EU AI Act / FDA SaMD / FTC hooks where they apply. |

### Block reasoning order (mandatory)

Do not jump around. Each block sets up constraints later blocks inherit.

1. **Eval necessity & success definition** (anchors everything — what is the AI supposed to do, and what does "doing it" look like)
2. **Ground truth & label quality** (the measurement substrate — without ground truth, nothing else has meaning)
3. **Offline eval design** (pre-launch rigor — composition, coverage, leakage, power)
4. **Online metrics & signal** (production rigor — direct vs. proxy, failure signal)
5. **Cohort breakdown & disparate impact** (per-segment performance — fairness, harm distribution)
6. **Adversarial & robustness** (failure modes — red team, injection, OOD, drift-resistance)
7. **Drift detection & monitoring** (continued vigilance — alerting, retraining cadence)

### Per-block protocol

For each block:

1. **State the block in one sentence** from `references/blocks/<NN>-<name>.md`.
2. **Ask the block's primary probe** (one question). Probes are in the
   reference file.
3. **Listen for specificity.** "We measure accuracy" is not specific.
   "Token-level F1 on our held-out test set of 800 hand-labeled examples"
   is. Push back on category answers.
4. **Walk secondary probes** if the primary was thin.
5. **Apply acceptance criteria.** Each block has 3–5. Note met vs. gap.
6. **Mark gaps explicitly.** `[Gap — what hasn't been decided: <what>]`.

### What "enough" looks like

Each block has at least one specific, testable eval decision OR an
explicit gap marker. "We'll figure out metrics later" is a gap, not an
answer.

### What to do when the builder doesn't know

Mark `[Gap — <what hasn't been decided>: <why it matters>]`. A review
with honest gaps is more useful than one with invented confidence.

### Pacing

Full seven-block walk takes 30–60 minutes depending on AI type and
lifecycle stage. Single-block work is ~10 minutes — but still invoke
the skill, since adjacent blocks stress-test the one being reviewed.

---

## Phase 2: Cross-Block Stress Test

**Goal:** Surface contradictions, dependencies, and gaps that only show
up when blocks are read together. Six mandatory checks plus the
regulatory cross-cutting lens.

1. **Necessity ↔ Online metrics.** If Block 1 says success is "users find
   drafts useful," does Block 4 measure that, or measure a proxy? Proxy
   metrics treated as direct are the dominant failure mode here.
2. **Ground truth ↔ Offline eval.** If Block 2 says ground truth is
   hand-labeled with single annotator, does Block 3 acknowledge the
   resulting label-noise ceiling on offline eval signal?
3. **Cohort ↔ Ground truth.** Are per-segment evals in Block 5 actually
   labeled per-segment (Block 2)? Aggregate ground truth can hide
   segment-level imbalance.
4. **Adversarial ↔ Output integrity (ai-ux-review Block 6 boundary).** If
   `ai-ux-review.md` exists and Block 6 names prompt-injection
   mitigations, does this skill's Block 6 actually *measure* injection
   resistance? Designed mitigations without eval signal are theater.
5. **Drift ↔ Online metrics.** If Block 7 says drift is detected via
   metric Z, is Z actually one of the online metrics in Block 4? A drift
   signal that lives nowhere in production observability is aspirational.
6. **All blocks ↔ Lifecycle stage.** Pre-MVP gaps in Block 5 (cohort
   eval) are different urgency than post-launch gaps in Block 5. Tag
   urgency by lifecycle.

**Regulatory cross-cutting lens (mandatory when regulatory context is
non-trivial):** EU AI Act high-risk requires data quality, human
oversight, accuracy + robustness, and post-market monitoring — these
map to Blocks 2, 4, 6, 7 respectively. FDA SaMD ties eval-rigor to risk
class. FTC AI guidance emphasizes disparate impact (Block 5) and
truthfulness (Block 6). Surface where regulatory rigor *changes the
bar*, not just where regulators have an opinion.

### Output of Phase 2

Append a `## Gap Summary` section with the 3–5 most urgent unmade eval
decisions. For each:

- The gap in plain language ("No ground-truth labels for refusal cases")
- Why it matters ("Block 1 said refusal-handling is part of success;
  Block 5 says cohort 'declined requests' has no metrics; without
  labels, neither can be measured")
- The cheapest experiment to resolve ("Label 100 refusal cases this
  week with 2 annotators; if agreement >0.7, proceed to scale; if lower,
  the refusal taxonomy itself is the gap")

---

## Phase 3: Render & Ship

Same structure as `ai-ux-review`. Produce two files at the resolved
root, present via `present_files` or `computer://` links, close with
three lines.

### Step 1 — Produce `ai-eval-review.md`

Structure (headings must match exactly):

```markdown
# AI Eval Review — [Product / Feature Name]

> Generated on [YYYY-MM-DD]. AI type: [LLM | classical-ML | CV | multi-modal | agentic]. Lifecycle: [pre-MVP | prototype | development | shipped]. Regulatory: [unregulated | consumer-trust-sensitive | EU AI Act limited-risk | EU AI Act high-risk | FDA SaMD class N | FTC adjacent].

## Block 1 — Eval Necessity & Success Definition
- ...

## Block 2 — Ground Truth & Label Quality
- ...

## Block 3 — Offline Eval Design
- ...

## Block 4 — Online Metrics & Signal
- ...

## Block 5 — Cohort Breakdown & Disparate Impact
- ...

## Block 6 — Adversarial & Robustness
- ...

## Block 7 — Drift Detection & Monitoring
- ...

---

## Gap Summary

1. **[Gap in one line]**
   - Why it matters: ...
   - Cheapest experiment to resolve: ...
```

### Step 2 — Produce `ai-eval-review.html`

Read the template at `templates/ai-eval-review.html` and produce a single
self-contained HTML that:

- Renders the seven blocks as cards in a 3+3+1 grid (mirrors
  `ai-ux-review` for visual parity when both reviews exist for the same
  product).
- Marks any block with unresolved gaps using a `[GAP]` chip.
- Reads brand tokens from `<resolved-brand-root>/DESIGN.md` if present.
- Includes Gap Summary footer.
- Prints cleanly to PDF via CSS paged media.
- Carries zero network dependencies, no localStorage.

### Step 3 — Save to the resolved review folder

- `<review-root>/ai-eval-review.md`
- `<review-root>/ai-eval-review.html`

Side-by-side with `ai-ux-review.md` + `ai-ux-review.html` when present.

### Step 4 — Present to the user

End with **three lines**:

1. *"The unresolved eval decision with the highest urgency is: …"*
2. *"The cheapest experiment to resolve it is: …"* — typically one of:
   label N examples, run baseline against eval set, instrument metric Y,
   add cohort segmentation, run red-team for failure mode Z.
3. *"Next step: …"* — pick from: "implement eval pipeline for metric X
   using your team's tools (HELM / W&B / Evidently / custom)," "if
   regulatory rigor is in scope, escalate to `team-composer` with
   `@legal_compliance_advisor` for compliance pass," "if `ai-ux-review`
   hasn't been run for this product, run it next to close the design
   side."

---

## Update mode (loop-back)

When `ai-eval-review.md` already exists:

1. **Read the existing file first.** Don't overwrite blocks the builder
   hasn't asked to change.
2. **Confirm scope.** *"Your last review had gaps in Block 5 (Cohorts)
   and Block 7 (Drift). Update those, or re-run the full seven?"*
3. **Apply the same rigor.** Glib revisions get push-back.
4. **Mark changes visibly.** `<!-- updated YYYY-MM-DD: <reason> -->`.

---

## Output Files

```
<review-root>/ai-eval-review.md     Canonical, editable source of truth
<review-root>/ai-eval-review.html   Self-contained visual review (primary deliverable)
```

No other files.

---

## Quality Checklist

**Phase 0 (Intake)**
- [ ] Review root resolved (shared with `ai-ux-review` when present)
- [ ] Adjacent artifacts scanned (`ai-ux-review.md`, `validation-canvas.md`, `DESIGN.md`, attached eval plan)
- [ ] Four intake facts established (AI does what / type / lifecycle / regulatory)
- [ ] Framing confirmed in one line
- [ ] If `ai-ux-review.md` Block 7 has gaps, they're surfaced and Block 1 is seeded from them

**Content (per block)**
- [ ] Every block has at least one specific, testable eval decision OR an explicit `[Gap — ...]` marker
- [ ] Specificity gate enforced — "we measure accuracy" is rejected
- [ ] Acceptance criteria checked per block
- [ ] Block 6 probes applied to the AI type (LLM-specific for LLM products, classical-ML for tabular, etc.)
- [ ] Block 1's success definition is distinct from Block 4's online metric (one is the target, the other is the signal — proxy vs. direct named)

**Cross-block (Phase 2)**
- [ ] All six cross-block checks run
- [ ] Regulatory lens applied if context is non-trivial
- [ ] Gap Summary has 3–5 gaps with why-it-matters and cheapest experiment
- [ ] Gaps tagged by urgency for the lifecycle stage

**Rendering**
- [ ] Exact heading structure (load-bearing for any future composability)
- [ ] HTML opens in a browser, prints cleanly to PDF
- [ ] Brand tokens applied if `DESIGN.md` present
- [ ] Zero network deps, no localStorage

**Shipping**
- [ ] Both files saved to resolved review folder (sibling of `ai-ux-review.md` when present)
- [ ] Files presented via `present_files` or `computer://` links
- [ ] Response ends with the three lines

---

## Cross-Skill Integration

| Skill | When to Use |
|-------|-------------|
| `ai-ux-review` (our own) | **Sibling skill.** Different subject, same shape. Run both for a complete review of an AI product. If `ai-ux-review.md` exists, this skill reads Block 7 as input and seeds Block 1 from `[Gap — …]` markers. |
| `validation-canvas` (our own) | Upstream when the product is idea-stage. Block 5 (Cohort breakdown) reads Customer Segments. |
| `brand-workshop` (our own) | Upstream when a brand exists. HTML output styled from `DESIGN.md`. |
| `team-composer` (our own) | Alternative when the builder wants a *discussion* on one narrow eval question (e.g., "let's debate offline vs. online for our use case") rather than a full review artifact. Use `team-composer` with `@data_scientist` + `@ai_safety_specialist`. |
| `riskiest-assumption-test` (our own) | Composition. If the Gap Summary surfaces eval assumptions that need *testing* (not just deciding — e.g., "we assume single-annotator labels are accurate enough"), hand them to RAT. |
| `startup-grill` (our own) | Adjacent. Adversarial pre-mortem with verdict. Different mode. |
| `pitch-deck` (our own) | Downstream. Strong eval decisions seed slide content for traction / validation claims. |
| HELM (Stanford CRFM, Apache 2.0) | Implementation reference. Multi-dimensional eval (accuracy, calibration, robustness, fairness, bias, toxicity, efficiency) — point at it when Block 3 or Block 5 needs an actual benchmark. |
| Anthropic claude-cookbooks (MIT) | Implementation reference. Patterns for designing LLM evals; useful when Block 3 needs concrete examples. |
| OpenAI Evals (MIT) | Implementation reference. Framework + benchmark registry; useful when Block 3 needs to scope an eval-set build. |
| `theme-factory` (Anthropic) | When the HTML review needs branded styling and no `DESIGN.md` exists. |
| `pdf` (Anthropic) | When merging the review into a regulatory submission or board packet. |
| `docx` (Anthropic) | When the review needs to ship as `.docx`. |
| `ai-safety-mindset` (Anthropic) | When the team lacks shared vocabulary for responsible-AI eval. Block 5 + 6 specifically benefit. |

**Principle:** this skill owns the **eval-design-completeness artifact** —
whether the measurement layer of an AI product has been intentionally
designed. It does not implement the eval (that's the team's eval
platform), validate beliefs (that's `validation-canvas`), test hypotheses
(`riskiest-assumption-test`), pitch the product (`pitch-deck`),
adversarially probe it (`startup-grill`), or audit the human-AI design
surface (that's `ai-ux-review` — the sibling skill).

**Graceful degradation:** if a referenced skill is not installed, this
skill still ships `ai-eval-review.md` + `.html`. Cross-skill chains are
enhancements, not requirements.

---

## Reference files

- `references/blocks/01-necessity-success.md` — what success means; offline criterion; AI-type-specific success patterns
- `references/blocks/02-ground-truth-labels.md` — label sources; quality; coverage gaps; inter-annotator agreement
- `references/blocks/03-offline-eval-design.md` — eval set composition; distribution coverage; leakage protection; statistical power
- `references/blocks/04-online-metrics-signal.md` — production metrics; proxy vs. direct; failure signal vs. engagement
- `references/blocks/05-cohort-disparate-impact.md` — per-segment performance; fairness; harm distribution; regulatory hooks
- `references/blocks/06-adversarial-robustness.md` — red-team coverage; prompt injection; OOD detection; jailbreak resistance; classical-ML adversarial
- `references/blocks/07-drift-monitoring.md` — model / behavior / data drift; alerting; retraining cadence; monitoring infrastructure

Read these when the phase calls for them. Do not front-load all references
at once — that's the progressive disclosure pattern this repo uses (see
`CLAUDE.md` → "Harness vocabulary").

**Tags:** ai, eval, evaluation, mlops, responsible-ai, fairness, drift, llm, design-review
