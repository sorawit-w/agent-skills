<p align="center">
  <img src="https://raw.githubusercontent.com/sorawit-w/agent-skills/main/assets/business-model-canvas-li.svg" alt="business-model-canvas — nine blocks, honestly filled" width="100%"/>
</p>

# business-model-canvas

Interview a founder block-by-block and produce a rigorous 9-block Business Model Canvas — as both an editable Markdown file and a self-contained HTML visual canvas you can open, share, or print to PDF.

This is not a template fill-in. The value is in the interview: customer-first reasoning order, specificity gates that refuse category answers ("SMBs", "the internet"), a cross-block consistency check, and an explicit Stress Tests section that names the 3–5 assumptions most likely to kill the business.

## What it does

- Runs a focused interview in `@startup_strategist` + `@vc_partner` + `@finance_manager` + `@senior_product_manager` voices — at most 3 questions per block, total ~45–75 minutes for a first pass.
- Enforces customer-first reasoning order: Customer Segments → Value Propositions → Channels → Customer Relationships → Revenue Streams → Key Resources → Key Activities → Key Partners → Cost Structure. Working inside-out produces a model the founder believes but no one buys.
- Runs a mandatory consistency pass across blocks (segment ↔ value-prop, value-prop ↔ revenue, channel ↔ segment, activity ↔ resource, cost ↔ activity, partner ↔ activity).
- Produces **two files**, both saved to the founder's working directory:
  - `business-model.md` — canonical, editable source of truth with headings the downstream pitch-deck plugin can parse.
  - `business-model.html` — single self-contained HTML canvas in the canonical Osterwalder grid layout. Opens in any browser, prints cleanly to PDF (CSS paged media, landscape A4), zero network dependencies.
- Applies brand tokens from `brand-kit/design-system.md` automatically if a `brand-workshop` kit is present in the working directory. Otherwise uses neutral defaults.
- Ends with an explicit call-out of the strongest stress test and the cheapest disconfirming experiment the founder can run this week.

## What it doesn't do

- **Pitch deck construction.** Problem → solution → traction → ask storytelling belongs to the `pitch-deck` companion skill, which reads `business-model.md` directly.
- **Financial projections.** The Revenue Streams and Cost Structure blocks are *structural* (how money flows), not *quantitative* (how much and when). No P&L, no cohort curves.
- **Market validation.** The canvas captures current thinking — it doesn't go run customer interviews to validate it. Validation is a separate pass.
- **Regulated-domain legal work.** The canvas surfaces the right questions but doesn't answer regulatory ones. Escalate to `team-composer` with `@legal_compliance_advisor`.

## When to use it

- You have a startup, product, or business line and want a **persistent artifact** — one you'll return to, edit, and share — rather than a one-shot discussion.
- You just finished `brand-workshop` and want the next strategy artifact before pitching.
- You're preparing to fundraise or write a pitch deck, and you need the underlying business model crisp before you start telling the story.
- A cofounder, advisor, or early hire asked "what's your business model?" and the answer isn't yet tight enough to fit on a napkin.

## When to use something else

- **Brand / logo / tagline** → `brand-workshop` (upstream of this skill).
- **Narrow strategic question** (pricing model alone, channel strategy alone, partner selection alone) → `team-composer` with `@startup_strategist`. Faster, discussion-grade, no artifact.
- **Pitch deck with real content** → `pitch-deck` (downstream companion), or `team-composer` with `@startup_strategist` + `@vc_partner`.
- **Financial model** → a spreadsheet tool + `xlsx` skill; this plugin deliberately stays structural.

## How it works

Three phases, all in one Claude session.

**Phase 1 — Discovery (~45–75 min).** Block-by-block interview in customer-first order. `@startup_strategist` leads; `@vc_partner`, `@finance_manager`, `@senior_product_manager` rebut. Max 3 questions per block. Unknowns get marked `[Unknown — what-to-learn]` rather than invented.

**Phase 2 — Draft & Consistency Check.** All nine blocks written 3–6 bullets long. Then a six-question cross-block consistency pass (see `references/nine-blocks.md`) that forces revision when segment ↔ value-prop alignment breaks, or when a Key Activity has no supporting Key Resource, or when Cost Structure is just generic startup costs. Then a Stress Tests section with the 3–5 assumptions most likely to fail, each with its failure mode and a disconfirming experiment.

**Phase 3 — Render & Ship.** `business-model.md` written with an exact heading structure (downstream tools parse it). `business-model.html` rendered from the template in `references/bmc-html-template.md`, adopting `brand-kit/design-system.md` tokens when present. Both files saved to the founder's working directory. Response ends with the top stress test and the cheapest this-week experiment.

## What the output looks like

```
<your-working-folder>/
├── business-model.md       canonical, editable source of truth
└── business-model.html     self-contained visual canvas (the primary deliverable)
```

The HTML canvas renders the canonical Osterwalder grid: Key Partners / Key Activities + Key Resources / Value Propositions / Customer Relationships + Channels / Customer Segments on the top row; Cost Structure and Revenue Streams on the bottom. Prints to PDF cleanly. Adopts your brand tokens if `brand-kit/` is present.

## Design principles

- **Customer-first, not founder-first.** The interview starts from the customer and works back to cost. The other order produces a canvas the founder believes but no customer buys.
- **Specificity is a gate, not a suggestion.** "SMBs" and "the internet" are rejected. The skill asks again until the segment and channel are named concretely.
- **Unknowns are data.** A canvas with honest `[Unknown — …]` markers is more useful than one padded with invented confidence. Unknowns roll up into Stress Tests with a cheapest-experiment-to-disconfirm attached.
- **Stress Tests are the most-read part six months later.** 3–5 assumptions, each with failure mode and disconfirming experiment, are non-negotiable.
- **The HTML is the visual primary; Markdown is the source of truth.** Founders share the HTML, edit the Markdown. Both carry the same content.
- **Zero network dependencies in the HTML.** No CDN, no webfonts, no external CSS or JS. A canvas you can't open on a plane isn't shippable.
- **Folder conventions over configuration.** No manifest file in v1. If `brand-kit/design-system.md` is present, adopt its tokens; if not, fall back. The contract is: read cheap, write to known paths, never clobber another plugin's output.

## Install

This skill is distributed as a [Claude Code](https://docs.claude.com/en/docs/claude-code) plugin inside the [`sorawit-w/agent-skills`](https://github.com/sorawit-w/agent-skills) marketplace. From Claude Code or Cowork:

```
/plugin marketplace add sorawit-w/agent-skills
/plugin install business-model-canvas@sorawit-w
```

## Related skills

- **`brand-workshop`** — upstream. Produces the `brand-kit/` this skill reads to style the HTML canvas.
- **`team-composer`** — the discussion-grade alternative when you want to think through one narrow block without committing to a full canvas artifact.
- **`pitch-deck`** (planned) — downstream. Consumes `business-model.md` as input when constructing the pitch narrative.
- **`tech-stack-recommendations`** — sibling skill for when Key Resources or Key Activities include technology choices the founder hasn't made yet.

## Status and scope

v0.1. The interview and canvas structure are locked; the HTML template is opinionated but designed to be customized via brand tokens. Planned improvements:

- Auto-detect and read `business-model.md` on a second run, treat as update-in-place rather than rewrite.
- Second HTML view: a pitch-ready one-pager that summarizes the canvas in narrative form for when a full-grid visual is too dense.
- Optional Claude in Chrome preview step to verify print-to-PDF quality before shipping.

**Supported:** first-pass canvas for a single business line. Updates to an existing canvas (manual Markdown edit, re-render).

**Not supported:** multiple business lines in a single canvas (run the skill once per line), financial projections, automated market research, regulatory compliance assessment.
