<p align="center">
  <em>riskiest-assumption-test — convert beliefs into falsifiable hypotheses with success and kill criteria</em>
</p>

# riskiest-assumption-test

Convert the **beliefs** captured in your `validation-canvas` Stress Tests into **falsifiable hypotheses** with explicit test methods, success criteria, and kill criteria. Ship a 1-page Assumption Test Plan plus an interactive risk × impact matrix.

This skill is step 3 of 5 in the startup pipeline:

```
brand-workshop ─▶ validation-canvas ─▶ riskiest-assumption-test ─▶ pitch-deck ─▶ startup-grill
```

The job here is **experimental**: *what have we proven, and what's the cheapest experiment that would invalidate the next belief?* Pitching on untested assumptions is sales theater — this skill is the gate between believing and proving.

## What it does

- **Phase 0 — Read prior artifacts (medium gate).** Reads `validation-canvas.md`. STOPs and routes back if missing.
- **Phase 1 — Assumption Dump.** Extracts every implicit belief from the Lean Canvas + VPC + Stress Tests, categorized into desirability / viability / feasibility (Christensen). Quotes the canvas line that surfaced each belief.
- **Phase 2 — Risk × Impact Ranking.** Scores each assumption on (likelihood of being wrong) × (impact if wrong). Picks Top 3 from the high-impact corner.
- **Phase 3 — Hypothesis Rewriting.** Converts each top-3 belief into a falsifiable hypothesis: "We believe X. We'll know this is true if [measurable outcome] within [time]." Refuses unfalsifiable framings.
- **Phase 4 — Test Method Selection.** Matches each hypothesis to the cheapest method that can falsify it (5-interview rule, landing page, fake-door, concierge MVP, Wizard of Oz, pre-sale, smoke test, expert interview). Specifies success criteria, kill criteria, sample, time bound, cost.
- **Phase 5 — Render & Ship.** Produces `rat/assumption-test-plan.md` (canonical, editable) and `rat/test-matrix.html` (interactive risk × impact matrix with drag-to-rerank, click-to-expand, print-clean).

## What it doesn't do

- **Build the experiments.** RAT produces a *plan*. The actual landing page / concierge service / Wizard of Oz prototype is built in your real product surface (or with `web-artifacts-builder`).
- **Validate the canvas.** That's `validation-canvas`'s job. RAT reads the canvas, doesn't write it.
- **Build the pitch deck.** That's `pitch-deck`'s job — and pitch-deck refuses to ship if RAT Results are empty for top-3 hypotheses (heavy gate).
- **Run optimization-grade A/B tests.** Methods here are early-stage validation experiments, not statistical-significance optimization.
- **Talk to your customers for you.** Several methods *require* customer interviews. The skill helps design them; it doesn't run them.
- **Commission market research reports.** RAT is about cheap, fast, founder-runnable tests.

## When to use it

- You just shipped `validation-canvas.md` and your Stress Tests are calling out 3+ assumptions you're unsure of.
- You've been told (by an investor, mentor, or your own gut) that you should "validate before pitching" and you don't have a structured way to pick what to test.
- You want a 1-page test plan you can put in front of an advisor or co-founder for sanity check.
- A previous test invalidated something — re-invoke this skill in update mode to revise the plan and pick the next top-3.

## When to use something else

- **Build the canvas** → `validation-canvas` (upstream, required).
- **Build the test surface** (landing page, fake door) → `web-artifacts-builder` after this skill names the design.
- **Discuss validation strategy with a team** → `team-composer` with `@startup_strategist` + `@ux_researcher`.
- **Update canvas because a test invalidated something** → `validation-canvas` in update mode (loop-back).
- **Build the pitch deck** → `pitch-deck` (downstream, gated on RAT Results).
- **Adversarially probe the whole startup** → `startup-grill` (last step).

## How it works

Five phases, all in one Claude session.

1. **Read upstream.** `validation-canvas.md` is parsed; Stress Tests + `[Unknown — …]` markers + un-relieved Pains + un-created Gains form the assumption seed.
2. **Dump.** 8–15 assumptions surfaced, categorized desirability / viability / feasibility, each quoting the canvas line that surfaced it.
3. **Rank.** 3×3 risk × impact matrix. Top 3 picked from high-impact corner.
4. **Rewrite as falsifiable hypotheses + select tests.** Each top-3 belief becomes "We believe X. We'll know this is true if [measurable outcome] within [time bound]." Each hypothesis gets a method, sample, success criteria, kill criteria, time bound, and cost estimate.
5. **Ship.** Markdown test plan + interactive HTML matrix. Response ends with the riskiest assumption, the cheapest test, and the heavy-gate note to `pitch-deck`.

## What the output looks like

```
<your-working-folder>/
└── rat/
    ├── assumption-test-plan.md   canonical test plan with Results section
    └── test-matrix.html          interactive risk × impact matrix (drag to rerank, click to expand)
```

The matrix is a 3×3 grid (Risk × Impact). Each assumption is a draggable card. Color-coded by category. Top 3 get a visible badge and a thicker border. Click to expand the hypothesis, success/kill criteria, and chosen test method. Prints cleanly to PDF for board decks.

## Loop-back is first-class

When a top-3 hypothesis is invalidated, you don't restart from scratch. The skill's update mode:

1. Detects which hypothesis failed.
2. Names the affected canvas block.
3. Routes you back to `validation-canvas` in update mode to revise that block.
4. Suggests the next top 3 from the ranking matrix.

This is normal pipeline behavior — pristine pipelines (no iteration after testing) are the actual yellow flag, which `startup-grill` checks for in its kill report.

## Test method catalog (quick reference)

See [`references/test-method-catalog.md`](references/test-method-catalog.md) for the full catalog with cost estimates, when-to-use, when-not-to-use, and worked examples.

| Hypothesis category | Cheapest methods |
|---|---|
| **Desirability** (do they want it?) | 5-interview rule, landing page + email capture, fake-door test, social-media smoke test |
| **Viability** (will they pay?) | Pre-sale, concierge MVP with explicit pricing, willingness-to-pay survey + interview |
| **Feasibility** (can we deliver?) | Wizard of Oz, technical spike, prototype with stub data, expert interview |

## Install

This skill is distributed as a [Claude Code](https://docs.claude.com/en/docs/claude-code) plugin inside the [`sorawit-w/agent-skills`](https://github.com/sorawit-w/agent-skills) marketplace. From Claude Code or Cowork:

```
/plugin marketplace add sorawit-w/agent-skills
/plugin install riskiest-assumption-test@sorawit-w
```

## Related skills

- **`validation-canvas`** — required upstream (medium gate). Loop-back target when hypotheses invalidate.
- **`pitch-deck`** — required downstream (heavy gate). Pitch refuses to ship without populated RAT Results for top-3 hypotheses.
- **`startup-grill`** — last step. Reads RAT Results to check for iteration evidence.
- **`brand-workshop`** — upstream, optional. Tokens for the matrix HTML.
- **`team-composer`** — discussion alternative for multi-role validation strategy.
- **`web-artifacts-builder`** (Anthropic) — for actually building landing-page / fake-door test surfaces after this skill names the design.

## Status and scope

**Supported:** test plans for early-stage idea / pre-seed / seed startups. Update-mode runs after Results land. The eight standard test methods listed above.

**Not supported:** optimization-grade A/B testing, statistical sample-size calculators, automated experiment execution, customer interviews (the skill helps design them; the founder runs them), market research at the Forrester/Gartner level.
