<p align="center">
  <img src="https://raw.githubusercontent.com/sorawit-w/agent-skills/main/assets/ai-ux-review-li.svg" alt="ai-ux-review — design-completeness review for AI products" width="100%"/>
</p>

# ai-ux-review

Audit an AI product or feature against a structured set of human-AI design questions — and produce both an editable Markdown artifact and a self-contained HTML visualization you can open, share, or print to PDF.

This skill exists to answer one question: **have we intentionally designed the human side of this AI product?** Most AI features ship with a great prompt and an underdesigned interaction layer. The seven blocks below force the design layer into view, surface what's been decided versus what's still a gap, and hand off the unresolved items to whatever comes next.

The job is **design-completeness**: classical UX concerns (user need, mental models, trust, feedback, errors) **plus** the gen-AI integrity surface that emerged after 2022 (hallucination handling, output verifiability, provenance, prompt-injection exposure, agent autonomy). This is what differentiates the skill from a re-housing of pre-2022 frameworks — block 6 is where it earns its seat.

This is not a quality assessment of an AI product's output. It is a structured review of whether the *design around* that output is intentional.

## What it does

- **Phase 0 — Intake.** Resolves the output path, scans for adjacent artifacts (`validation-canvas.md`, brand `DESIGN.md`, attached specs), and confirms three intake facts in one line — what the AI does, where it is in the lifecycle, what kind of AI it is. Skips business-model questions entirely when a `validation-canvas` exists.
- **Phase 1 — Block-by-block elicitation.** Walks the seven blocks in a fixed reasoning order (necessity → mental model → trust → feedback → errors → output integrity → success). Roles active: `@ux_researcher`, `@ai_safety_specialist`, `@lead_behavioral_scientist`, `@senior_product_designer`, `@senior_product_manager`. Each block has a primary probe, secondary probes, and 2–4 acceptance criteria.
- **Phase 2 — Cross-block stress test.** Six mandatory checks across blocks: necessity ↔ integrity, mental model ↔ trust, trust ↔ feedback, errors ↔ feedback, integrity ↔ eval, all ↔ lifecycle urgency. Surfaces contradictions and unmade design decisions.
- **Phase 3 — Render & ship.** Produces two files:
  - `ai-ux-review.md` — canonical, editable source of truth with one H2 section per block plus a `## Gap Summary` (3–5 unmade design decisions, each with why-it-matters and a cheapest-experiment).
  - `ai-ux-review.html` — single self-contained HTML rendering the seven blocks as cards in a 3+3+1 grid, with `[GAP]` chips on blocks that have unresolved decisions. Opens in any browser, prints cleanly to PDF, zero network dependencies.
- **Brand-aware.** Reads tokens from `<brand-root>/DESIGN.md` if a `brand-workshop` artifact is present, per the [Google Labs spec](https://github.com/google-labs-code/design.md) (alpha). Otherwise uses neutral defaults.
- **Specificity gate.** "We handle errors" and "users will trust it" are rejected. The skill pushes back until either a concrete design decision is named or an explicit `[Gap — ...]` is logged.
- **Closes with three lines:** the unresolved decision with the highest urgency, the cheapest design experiment to resolve it, the next step.

## What it doesn't do

- **Not a lean canvas or business-model review.** That's `validation-canvas`. This skill assumes the model is settled and audits UX execution.
- **Not adversarial.** No verdict label, no kill report. This is cooperative gap detection. For "would this survive a VC tear-down?", use `startup-grill`.
- **Not a SKILL.md audit.** That's `skill-evaluator`. This skill audits AI products, not agent-skill text.
- **Not a substitute for user research.** Surfaces "have you spoken to users about this?" but does not run interviews.
- **Not an evaluation-pipeline builder.** Block 7 *names* eval gaps. It does not implement metrics, label datasets, or write eval code. That layer is a candidate for a future `ai-eval-rubric` companion skill.
- **Not a pitch-deck builder.** Pitch construction belongs to `pitch-deck`.
- **Not a substitute for regulatory advice.** Surfaces the questions; does not answer EU AI Act, FDA SaMD, or FTC compliance asks. Escalate to `team-composer` with `@legal_compliance_advisor` for compliance.

## When to use it

- You're about to ship an AI feature and want a structured pre-launch review — not a checklist, but a forced walk through the decisions that quietly get skipped.
- You shipped an LLM feature and you're seeing fluent-but-wrong outputs in production; you suspect Block 3 (Trust) or Block 6 (Output integrity) is underdesigned.
- You've completed `validation-canvas` for an AI startup and the business-model layer is settled — this skill picks up at the UX-execution layer.
- You're designing an agentic feature (multi-step actions, tool use) and want the autonomy + reversibility surface made explicit before launch.
- A cofounder, advisor, or PM asked "how do we know this is responsible AI?" and the answer isn't yet structured enough to defend.

## When to use something else

- **Business model / lean canvas** → `validation-canvas` (upstream of this skill).
- **Adversarial pre-mortem with a verdict** → `startup-grill` (different mode: kill report, not gap summary).
- **One narrow discussion** (just trust calibration, just error handling) → `team-composer` with `@ux_researcher` + `@ai_safety_specialist` (discussion-grade, no artifact).
- **SKILL.md rule-adherence audit** → `skill-evaluator` (different subject: agent-skill text, not AI products).
- **Brand / logo work** → `brand-workshop`.
- **Pitch deck** → `pitch-deck`.
- **Test the assumptions surfaced in the Gap Summary** → `riskiest-assumption-test`.
- **Actual evaluation pipelines** (label data, write eval code, set up online metrics) → a future `ai-eval-rubric` companion skill or your engineering team.

## How it works

Three phases, all in one Claude session.

**Phase 0 — Intake (immediate, before block work).** Resolves output path. Scans for adjacent `validation-canvas.md`, `DESIGN.md`, attached spec. Confirms three intake facts (what the AI does, lifecycle stage, AI type) in one line so the user can correct framing.

**Phase 1 — Block-by-block elicitation.** Seven blocks in fixed reasoning order. Each block uses its primary probe to elicit a design decision in specific terms; gaps are explicitly marked. Specificity gate rejects category answers ("we handle errors") and forces a real decision or a real `[Gap — ...]` marker.

**Phase 2 — Cross-block stress test.** Six mandatory cross-checks. Contradictions between blocks are surfaced as gaps even when individual blocks were "complete." Gap Summary written with 3–5 most urgent unmade decisions, each with a cheapest-experiment-to-resolve.

**Phase 3 — Render & ship.** Markdown + HTML written to `docs/ai-ux/` (or `docs/startup-kit/ai-ux/` under the kit orchestrator). Three closing lines: the most urgent gap, the cheapest experiment, the next step.

## What the output looks like

```
<your-working-folder>/
└── docs/
    └── ai-ux/
        ├── ai-ux-review.md       canonical, editable source of truth
        └── ai-ux-review.html     self-contained visual review (primary deliverable)
```

The HTML renders the seven blocks as cards in a 3+3+1 layout (Blocks 1–3 top row, 4–6 middle row, 7 full-width). Block headers carry a `[GAP]` chip when the block has unresolved decisions. A `Gap Summary` section at the bottom lists the unmade decisions with why-it-matters and cheapest-experiment for each. Prints cleanly to PDF.

## Design choices worth knowing

- **Seven blocks, not six.** PAIR's original 2021 framework has six chapters. This skill adds Block 6 (Output Integrity) as a first-class block specifically to cover the gen-AI surface — hallucination handling, prompt injection, verifiability, agent autonomy — that pre-2022 frameworks under-cover. Without it, the skill is just a re-housing of known ground.
- **Block-by-block, not chapter-by-chapter.** Each block ships with a primary probe, secondary probes, and 2–4 acceptance criteria. The criteria are the gate; they force decisions or explicit gaps rather than vague reassurance.
- **Gaps are data, not failure.** A review with three honest `[Gap — ...]` markers is more useful than a review padded with invented confidence. Gap Summary is the most-read part six months later.
- **The cross-block check is mandatory.** Individual blocks completed in isolation miss most of what fails in production. The six Phase 2 checks force the team to see whether the *system* of design decisions is coherent, not just whether each was named.
- **Block 1's necessity check is the audit's anchor.** If "why AI here?" can't be answered specifically, every downstream block rests on an unexamined assumption. Pushing back on Block 1 saves time everywhere else.
- **No `[GAP]` chip on every block by default.** The default HTML is "designed, with explicit gaps where they exist." A review where every block is `[GAP]` is a different message than a review where Block 3 is `[GAP]` — surface the difference.
- **Specificity is a gate, not a suggestion.** "We handle errors" and "users will trust it" are rejected with push-back. The block stays open until either a real decision or a real gap is logged.
- **Validation-canvas integration is one-way.** This skill reads `validation-canvas.md` if it exists and skips business-model questions. It does NOT update the canvas — the canvas is upstream and authoritative for those blocks.
- **Zero network dependencies in the HTML.** A review you can't open on a plane isn't shippable.

## Influences

This skill is inspired by Google's [People + AI Guidebook](https://pair.withgoogle.com/guidebook/) — a six-chapter framework on human-centered AI design published by Google's PAIR (People + AI Research) team in 2019 and last updated in 2021. The Guidebook's chapter structure is the conceptual ancestor of Blocks 1–5 in this skill.

**License compliance.** The Guidebook is published under [Creative Commons Attribution-NonCommercial-ShareAlike 4.0 International (CC BY-NC-SA 4.0)](https://creativecommons.org/licenses/by-nc-sa/4.0/). This skill is **not a derivative work** of the Guidebook under copyright law — copyright protects expression, not ideas or facts. This skill uses general AI UX concepts (the kind of question to ask, not the specific question wording) and authors its own elicitation flow, probe wording, acceptance criteria, examples, and worksheets from first principles. No Guidebook prose, worksheets, illustrations, or pattern names are reproduced anywhere in this skill or its references.

Block 6 (Output Integrity) goes beyond the Guidebook's 2021 framework into the gen-AI surface — hallucination, verifiability, prompt injection, agent autonomy — that hadn't crystallized when the Guidebook was last updated. That's where this skill differentiates rather than re-houses.

**If you want the original Guidebook**, read it at [pair.withgoogle.com/guidebook](https://pair.withgoogle.com/guidebook/). It's free, well-written, and worth ~30 minutes. This skill is a different shape (structured elicitation for an agentic context), not a replacement.

## Install

This skill is distributed as a [Claude Code](https://docs.claude.com/en/docs/claude-code) plugin inside the [`sorawit-w/agent-skills`](https://github.com/sorawit-w/agent-skills) marketplace. From Claude Code or Cowork:

```
/plugin marketplace add sorawit-w/agent-skills
/plugin install ai-ux-review@sorawit-w
```

To install the whole shelf instead of just this skill:

```
/plugin install agent-skills@sorawit-w
```

## Related skills

- **`ai-eval-review`** — **sibling skill.** Different subject, same shape. This skill audits whether the human-AI experience was intentionally designed; `ai-eval-review` audits whether you have signal for whether that design works. Run both for a complete review. Block 7 (Success & Evaluation) gaps from this skill seed Block 1 of `ai-eval-review` when both are run.
- **`validation-canvas`** — upstream when the AI product is idea-stage. This skill reads `validation-canvas.md` and skips business-model questions when it's present.
- **`brand-workshop`** — upstream when a brand identity exists. This skill reads `<brand-root>/DESIGN.md` to style the HTML output.
- **`team-composer`** — alternative for one-block discussions (e.g., "let's debate the trust-calibration approach for chatbots") rather than a full review artifact.
- **`startup-grill`** — adjacent. Adversarial pre-mortem with a verdict. Different mode from this skill's cooperative gap detection.
- **`riskiest-assumption-test`** — composition. When the Gap Summary surfaces design assumptions that need *testing* (not just deciding), hand them to RAT.
- **`pitch-deck`** — downstream. Strong design decisions from this review can seed pitch slides 3 and 6.
*Block 7 of this skill names "eval gap to companion" as an explicit hand-off field. That hand-off now lives in [`ai-eval-review`](../ai-eval-review/README.md) — the sibling skill shipped alongside this one.*

## Status and scope

**Supported:** first-pass review for a single AI product or feature. Update-mode runs (loop-back when the file already exists). All AI types — LLM, classical ML, computer vision, multi-modal, agentic — with type-specific Block 6 probes.

**Not supported:** multi-feature review in a single artifact (run the skill once per feature), engineering eval implementation, formal regulatory submissions, model-quality benchmarking, A/B test design (use `riskiest-assumption-test` for hypotheses).

**Versioning.** Initial release at the plugin version that introduces it. Block structure is load-bearing for any future `ai-eval-rubric` companion — adding or renumbering blocks is a MINOR bump at minimum and triggers a downstream contract review.

## Contributions

Not accepting external contributions right now — feel free to fork. Issues and suggestions welcome via [GitHub](https://github.com/sorawit-w/agent-skills/issues).

## License

MIT. See repo `LICENSE`. The skill text itself is MIT-licensed and contains no derivative material from the PAIR Guidebook (which is CC BY-NC-SA 4.0). See "Influences" above for the full attribution and compliance reasoning.
