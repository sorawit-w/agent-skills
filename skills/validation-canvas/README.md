<p align="center">
  <img src="https://raw.githubusercontent.com/sorawit-w/agent-skills/main/assets/validation-canvas-li.svg" alt="validation-canvas — Lean Canvas + VPC, honestly filled" width="100%"/>
</p>

# validation-canvas

Interview a founder block-by-block and produce a rigorous **Lean Canvas (Maurya) + Value Proposition Canvas (Osterwalder)** combined artifact — as both an editable Markdown file and a self-contained HTML visual you can open, share, or print to PDF.

This skill replaces the prior `business-model-canvas` (BMC). The 9-block Osterwalder BMC is a Series-A operating-plan tool — wrong altitude for an idea-stage founder. The Lean Canvas swaps Key Activities / Key Resources / Key Partners / Customer Relationships for **Problem**, **Solution**, **Key Metrics**, and **Unfair Advantage** — the things that actually decide whether the idea survives contact with reality.

The job is **declarative**: *what do we believe?* Naming what you've **proven** is the next step (`riskiest-assumption-test`).

This is not a template fill-in. The value is in the interview: experience-adaptive intake (Guided / Focused / Compressed-with-Challenge), customer-first reasoning order, specificity gates that refuse category answers ("SMBs", "the internet"), a cross-block consistency check, a Value Proposition Canvas fit pass, and an explicit Stress Tests section that names the assumptions most likely to kill the business — which are then handed off to `riskiest-assumption-test`.

## What it does

- **Phase 0 — Experience-adaptive intake.** Three calibration questions at invocation (founding history × domain experience × customer-segment experience) map to one of three modes — Guided (~60–90 min), Focused (~30–45 min), Compressed-with-Challenge (~15–20 min). Scans context first; asks only the delta. Confirms inferred mode in one line.
- Runs a focused interview in `@startup_strategist` + `@vc_partner` + `@finance_manager` + `@senior_product_manager` voices with mode-appropriate scaffolding.
- Enforces **Lean Canvas reasoning order**: Problem → Customer Segments → UVP → Solution → Channels → Revenue Streams → Cost Structure → Key Metrics → Unfair Advantage. Then a second pass on the **Value Proposition Canvas** (Customer Jobs / Pains / Gains ↔ Products / Pain Relievers / Gain Creators).
- Runs a mandatory 7-question consistency pass across blocks (problem ↔ segment, UVP ↔ segment, solution ↔ problem, channel ↔ segment, revenue ↔ UVP, cost ↔ solution+channel, VPC fit).
- Produces **two files**, both saved to the founder's working directory:
  - `validation-canvas.md` — canonical, editable source of truth with headings the downstream skills (`pitch-deck`, `riskiest-assumption-test`, `startup-grill`) can parse.
  - `validation-canvas.html` — single self-contained HTML rendering the Lean Canvas grid (top) and VPC fit diagram (bottom). Opens in any browser, prints cleanly to PDF, zero network dependencies.
- Applies brand tokens from `<brand-root>/DESIGN.md` automatically if a `brand-workshop` kit is present in the working directory. Extracts primary color from `colors.primary` in the YAML front matter per [Google Labs spec](https://github.com/google-labs-code/design.md) (version: alpha). Otherwise uses neutral defaults.
- Ends with an explicit call-out of the strongest stress test, the cheapest disconfirming experiment, and the **next-step gate**: run `riskiest-assumption-test`.

## What it doesn't do

- **9-block Osterwalder BMC.** That's wrong altitude for an idea-stage founder. If a board or grant explicitly requires the Osterwalder grid, use `team-composer` with `@startup_strategist` for a discussion-grade fill.
- **Assumption testing.** Naming beliefs is half the job. Testing them is `riskiest-assumption-test`'s job — a separate step that runs after this one. Do not bundle the two.
- **Pitch deck construction.** Belongs to `pitch-deck`, which reads `validation-canvas.md` directly.
- **Financial projections.** The Revenue Streams and Cost Structure blocks are *structural* (how money flows), not *quantitative* (how much and when). No P&L, no cohort curves.
- **Market validation.** The canvas captures current thinking — it doesn't go run customer interviews to validate it.
- **Competitive analysis (SWOT, Porter, Wardley).** Wrong altitude / wrong stage / overlap with `startup-grill`. Explicitly out of scope.
- **Regulated-domain legal work.** Surfaces the right questions but doesn't answer regulatory ones. Escalate to `team-composer` with `@legal_compliance_advisor`.

## When to use it

- You have a startup, product, or business line and want a **persistent artifact** — one you'll return to, edit, and share — rather than a one-shot discussion.
- You just finished `brand-workshop` and want the next strategy artifact before testing assumptions or pitching.
- You've run `riskiest-assumption-test` and an assumption was invalidated — invoke this skill in **update mode** to revise the affected blocks (loop-back protocol).
- A cofounder, advisor, or early hire asked "what's your business model?" and the answer isn't yet tight enough to fit on a napkin.

## When to use something else

- **Brand / logo / tagline** → `brand-workshop` (upstream of this skill).
- **Test the assumptions in your canvas** → `riskiest-assumption-test` (downstream, the next step).
- **Pitch deck** → `pitch-deck` (two steps downstream — only after RAT results land).
- **Adversarial probe** → `startup-grill` (last step in the pipeline).
- **9-block Osterwalder BMC** → `team-composer` with `@startup_strategist`. Discussion-grade.
- **Narrow strategic question** (pricing model alone, channel strategy alone) → `team-composer` with `@startup_strategist`. Faster, no artifact.
- **Financial model** → a spreadsheet tool + `xlsx` skill; this plugin deliberately stays structural.

## How it works

Four phases, all in one Claude session.

**Phase 0 — Experience-adaptive intake (immediate, before any canvas work).** Scans context for signals on founding history, domain experience, and customer-segment experience. Asks only the calibration questions whose signal is missing. Confirms inferred mode (Guided / Focused / Compressed-with-Challenge) in one line.

**Phase 1 — Discovery (mode-dependent pace).** Block-by-block Lean Canvas interview in problem-and-customer-first order. Then a second pass on the Value Proposition Canvas. Mode dictates rigor: Guided gets definitions+examples; Focused skips definitions; Compressed pushes back on glib answers. Unknowns get marked `[Unknown — what-to-learn]` rather than invented.

**Phase 2 — Draft & Consistency Check.** All blocks written. Then a 7-question cross-block consistency pass that forces revision when problem ↔ segment alignment breaks, when a Solution feature has no Problem, when Cost Structure is just generic startup costs, or when Pains have no Relievers and Gains have no Creators. Then a Stress Tests section with the 3–5 assumptions most likely to fail, each with its failure mode and a disconfirming experiment.

**Phase 3 — Render & Ship.** `validation-canvas.md` written with an exact heading structure (load-bearing cross-plugin contract). `validation-canvas.html` rendered from the template in `references/canvas-html-template.md`, adopting `DESIGN.md` tokens when present, extracting from YAML front matter. Both files saved to the founder's working directory. Response ends with three lines: the top stress test, the cheapest this-week experiment, and the next-step gate to `riskiest-assumption-test`.

## What the output looks like

```
<your-working-folder>/
├── validation-canvas.md       canonical, editable source of truth
└── validation-canvas.html     self-contained Lean+VPC visual (the primary deliverable)
```

The HTML renders the Lean Canvas grid (Problem / Solution+Key Metrics / UVP / Unfair Advantage+Channels / Customer Segments on the top half; Cost Structure and Revenue Streams on the bottom) and the VPC fit diagram (Customer Profile ↔ Value Map). Prints to PDF cleanly. Adopts your brand tokens from `DESIGN.md` if present, extracting colors from the YAML front matter.

## Pipeline placement

This skill is step 2 of 5 in the startup pipeline:

```
brand-workshop ─▶ validation-canvas ─▶ riskiest-assumption-test ─▶ pitch-deck ─▶ startup-grill
 (identity)        (this skill)          (test plan + results)        (HTML deck)   (kill report)
```

Inter-step gates are weighted: `brand-workshop` → here is **light**, here → `riskiest-assumption-test` is **medium** (the third closing line is the gate prompt), `riskiest-assumption-test` → `pitch-deck` is **heavy** (pitch-deck STOPs without populated `## Results`), `pitch-deck` → `startup-grill` is **light**. Loop-back is first-class — invalidated assumptions in RAT trigger a re-run of this skill in update mode. See [`references/folder-contract.md`](references/folder-contract.md) for the full protocol.

## Design principles

- **Right altitude for the stage.** Lean Canvas + VPC, not 9-block BMC. Idea-stage founders need to name beliefs that can be tested cheaply, not allocate Key Resources for a Series-A operating plan.
- **Adapt to the founder, not the template.** First-time and repeat founders get materially different scaffolding. Mode is set by 3-question intake, then adjusted through observed answer quality.
- **Push back on glib answers regardless of declared mode.** A "repeat founder" giving "we'll figure it out" doesn't get a free pass. Mode calibrates opening posture, not a permanent contract.
- **Customer-first, not founder-first.** Problem and Customer Segments come before Solution. The other order produces a canvas the founder believes but no customer buys.
- **Specificity is a gate, not a suggestion.** "SMBs" and "the internet" are rejected. The skill asks again until the segment and channel are named concretely.
- **Unknowns are data.** A canvas with honest `[Unknown — …]` markers is more useful than one padded with invented confidence. Unknowns roll up into Stress Tests with a cheapest-experiment-to-disconfirm attached — and feed directly into `riskiest-assumption-test`.
- **Stress Tests are the bridge to the next step.** They're not filler — `riskiest-assumption-test` greps them as the seed for its assumption dump.
- **Loop-back is normal.** Invalidated assumptions trigger an update-mode re-run, not a re-write.
- **Zero network dependencies in the HTML.** A canvas you can't open on a plane isn't shippable.
- **Folder conventions over configuration.** Read cheap, write to known paths, never clobber another plugin's output.

## Install

This skill is distributed as a [Claude Code](https://docs.claude.com/en/docs/claude-code) plugin inside the [`sorawit-w/agent-skills`](https://github.com/sorawit-w/agent-skills) marketplace. From Claude Code or Cowork:

```
/plugin marketplace add sorawit-w/agent-skills
/plugin install validation-canvas@sorawit-w
```

## Related skills

- **`brand-workshop`** — upstream. Produces `DESIGN.md` ([Google Labs spec](https://github.com/google-labs-code/design.md), alpha) which this skill reads to style the HTML canvas. Tokens are extracted from YAML front matter.
- **`riskiest-assumption-test`** — downstream (medium gate). Reads this canvas's Stress Tests section as the seed for its assumption dump. Invalidations loop back to this skill in update mode.
- **`pitch-deck`** — two steps downstream (heavy gate). Consumes `validation-canvas.md` to seed slides 2, 3, 6, and to stress-test the Ask. Gated on populated RAT `## Results`.
- **`startup-grill`** — last step. Reads this canvas's Stress Tests + RAT results + pitch deck slides as direct grilling ammunition.
- **`team-composer`** — the discussion-grade alternative for one narrow block (or for a 9-block Osterwalder BMC when explicitly required).
- **`tech-stack-recommendations`** — sibling skill when Solution or Channels include technology choices the founder hasn't made yet.

## Status and scope

**Supported:** first-pass canvas for a single business line. Update-mode runs (loop-back from RAT). All three intake modes (Guided / Focused / Compressed-with-Challenge).

**Not supported:** multiple business lines in a single canvas (run the skill once per line), financial projections, automated market research, regulatory compliance assessment, 9-block Osterwalder BMC (use `team-composer`), competitive analysis frameworks (SWOT / Porter / Wardley — use `startup-grill`).

**Migration from `business-model-canvas` (v1):** rename `business-model.md` to `validation-canvas.md` and restructure under the new Lean+VPC heading contract. The existing `## Stress Tests` section can carry over verbatim — that's the one block the new skill preserves from the old one.
