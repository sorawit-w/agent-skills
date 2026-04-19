---
name: business-model-canvas
description: Elicits founder inputs block-by-block and produces a 9-block Business Model Canvas (Osterwalder) as both `business-model.md` (canonical, editable) and `business-model.html` (self-contained visual canvas). Use whenever the user asks to "build a business model canvas", "BMC for my startup", "map out my business model", "help me think through my business model", "fill in the nine blocks", or uploads a product idea and asks how to monetize or structure it. Also trigger when the user has brand-workshop output ready and wants the next strategy artifact, or when `@startup_strategist` is the right lens. Even if the user only asks for one block (e.g., "help me figure out my revenue streams"), use this skill — the other eight blocks stress-test that block's claims.
---

# Business Model Canvas

Produce a rigorous 9-block Business Model Canvas from founder inputs. Each block is
a stress-tested claim, not a template field. The canvas is the primary deliverable;
the interview that produces it is where most of the value lives.

## What this skill produces

Always produced:

1. **`business-model.md`** — canonical, editable Markdown. Nine clearly-labelled blocks
   with founder-specific content, inline notes on uncertainty, and a "Stress Tests"
   section at the end listing the assumptions most likely to fail.
2. **`business-model.html`** — single self-contained HTML file that renders the
   canonical Osterwalder 9-block grid visually. Opens in any browser, prints cleanly
   to PDF, zero network dependencies (inline CSS, no webfonts by default).

Both files carry the same content — the HTML is the visual primary; the Markdown is
the source of truth founders edit as the business evolves.

## What this skill is NOT

- **Not a pitch deck builder.** Pitch construction (problem → solution → traction → ask
  narrative) belongs to the `pitch-deck` companion skill (which reads `business-model.md`
  directly) or to `team-composer` with `@startup_strategist` + `@vc_partner`.
- **Not a financial model.** No spreadsheet projections, no cohort curves, no TAM/SAM/SOM
  waterfall. Revenue Streams and Cost Structure blocks are *structural* (how money
  flows), not *quantitative* (how much and when).
- **Not market research.** The canvas records the founder's current thinking. It does
  not go validate it. Validation is a separate pass (interviews, experiments) that uses
  the canvas as input.
- **Not a substitute for domain expertise.** In regulated domains (fintech, health,
  education with minors), the canvas surfaces the right questions but does not answer
  regulatory ones — escalate to `team-composer` with `@legal_compliance_advisor`.

## Skill Boundaries

This skill intentionally overlaps with `team-composer` (`@startup_strategist` is active
there too) but differs in deliverable:

- **Use `business-model-canvas` when:** the founder wants a *persistent artifact* they
  can return to, edit, and share. The nine-block structure is the load-bearing feature.
- **Use `team-composer` with `@startup_strategist` when:** the founder wants a
  *discussion* on one narrow question (pricing model, channel strategy, partner
  selection) without committing to a full canvas. Discussion-grade, not artifact-grade.

> **Companion plugin:** `brand-workshop`. If a `brand-kit/` directory exists in the
> working folder, the HTML canvas adopts the brand's color tokens from
> `brand-kit/design-system.md`. If not, falls back to neutral defaults.

> **Planned companion plugins:** `pitch-deck` (consumes this canvas as input) and an
> umbrella `startup-launch-kit` orchestrator that runs `brand-workshop` →
> `business-model-canvas` → `pitch-deck` as one founder-facing flow.

---

## The Nine Blocks

Claude must internalize the canonical grid order. Left → right, top → bottom:

```
┌───────────────┬───────────────┬─────────────────────┬───────────────────────┬───────────────┐
│ Key Partners  │ Key Activities│                     │ Customer Relationships│               │
│               ├───────────────┤ Value Propositions  ├───────────────────────┤ Customer       │
│               │ Key Resources │                     │ Channels              │ Segments       │
├───────────────┴───────────────┴─────────────────────┴───────────────────────┴───────────────┤
│ Cost Structure                              │ Revenue Streams                                │
└─────────────────────────────────────────────┴────────────────────────────────────────────────┘
```

**Order of reasoning (NOT the grid order):** interview and fill in this sequence —
Customer Segments → Value Propositions → Channels → Customer Relationships → Revenue
Streams → Key Resources → Key Activities → Key Partners → Cost Structure. Start from
the customer, end at the cost. Working inside-out leads to a model the founder believes
but no one buys.

See `references/nine-blocks.md` for the deep definition of each block, canonical
examples, and the stress tests that surface shaky assumptions.

---

## Phase 1: Discovery (Founder Interview)

**Goal:** Extract enough raw material to fill each block substantively. A BMC filled with
"freelancers and small businesses" in Customer Segments is worthless — the job is to
force specificity.

### Role setup

Run the interview in first-person voice with these roles active. If the user invokes
`team-composer` separately, skip duplicates.

| Role | Lens |
|------|------|
| `@startup_strategist` | Workshop lead. Asks block-by-block. Pushes for specificity and internal consistency. |
| `@vc_partner` | Read-test. "Could a Series A partner understand this in 90 seconds?" Flags handwaving on Revenue / Traction adjacency. |
| `@finance_manager` | Stress-tests Revenue Streams and Cost Structure. Flags missing unit economics or undefined payment triggers. |
| `@senior_product_manager` | Value Proposition ↔ Customer Segment alignment. Flags "value props" that are really feature lists. |

### Interview protocol

Go through the **reasoning order** (customer-first), one block at a time. For each
block:

1. Read the block's prompts from `references/founder-prompts.md`.
2. Ask the founder **at most 3 questions per block.** If you need more than 3, either
   the block is too broad (split the customer segment) or the founder doesn't know yet
   (note the uncertainty and move on — don't stall the canvas).
3. Capture the founder's answer in their own words. Do not paraphrase into consultant-ese.
4. Flag the assumption most likely to fail. Name it. These roll up into the final
   Stress Tests section.

**What "enough" looks like:** each block has at least one specific, testable claim.
"Targets SMBs" is not specific. "Targets 5–25 person legal-tech firms in the US
northeast that currently use paper intake forms" is specific.

**What to do when the founder doesn't know:** mark the block `[Unknown — ${what-to-learn}]`
and add a row to the Stress Tests section: "We don't yet know ${what}; to find out, do
${experiment}." A canvas with honest unknowns is more useful than a canvas with invented
confidence.

### When the user skips the interview

If the founder gives you a paragraph dump or says "just fill it in from what I
said," still apply the thin-input rule: any block where your fill comes from
inference, not the founder's words, gets marked
`[Unknown — founder did not specify: <what's missing>]`.

Why: a BMC full of plausible-sounding AI guesses is worse than a BMC with 3
explicit unknowns. The unknowns are where the next founder conversation goes.

---

## Phase 2: Draft & Consistency Check

**Goal:** Produce the canonical canvas content and catch cross-block contradictions
before rendering.

### Step 1 — Draft all nine blocks

Write each block 3–6 bullets long. Bullets are specific claims, not categories.
See `references/nine-blocks.md` for good/bad examples per block.

### Step 2 — Consistency pass (MANDATORY, do not skip)

This rule applies even when the user explicitly asks to skip it
("I don't have time," "I know my business cold," "just render it").

Why: the canvas's value is the cross-block pressure test. Skipping it
produces a 9-cell template that looks like a BMC but carries none of
the stress-test signal. The founder loses the one thing they came for.

How to apply: decline the skip, then offer a fast path —

- Run the 6 relationship checks silently
- Surface only contradictions that would block the canvas from shipping
- Skip the prose write-up, keep the structured findings

Never emit a canvas with the consistency check silently omitted.

Read the full draft and answer each question in writing. If any answer is "no" or
"unclear," revise before producing final files.

1. **Segment ↔ Value Prop:** Does each customer segment map to at least one value
   proposition written in *that segment's* language (not the founder's)?
2. **Value Prop ↔ Revenue:** For each value proposition, is there a revenue stream
   that captures part of the value it creates? A valuable free feature with no upsell
   path is a flag, not a violation — note it.
3. **Channel ↔ Segment:** Is each channel a plausible way to reach the specific segment
   (not "the internet")?
4. **Activity ↔ Resource:** Does each Key Activity have the Key Resources required to
   execute it (people, tech, capital, IP)? A Key Activity with no supporting Resource
   is unfunded work.
5. **Cost ↔ Activity:** Does the Cost Structure reflect the *actual* cost drivers of
   the Key Activities, or is it a generic list of startup costs?
6. **Partner ↔ Activity:** For each Key Partner, is there at least one Key Activity
   the partner meaningfully de-risks or accelerates? Vanity partnerships get cut.

### Step 3 — Stress Tests

At the end of `business-model.md`, add a **Stress Tests** section with the 3–5
assumptions most likely to break. For each:

- The assumption in plain language.
- Why the business fails if it's wrong.
- The cheapest experiment that would disconfirm it.

Stress tests are the most-read part of the canvas six months later. Do not treat them
as filler.

---

## Phase 3: Render & Ship

**Goal:** Produce `business-model.md` and `business-model.html`, save them to a known
folder, and present them to the user.

### Step 1 — Produce `business-model.md`

Structure (headings must match exactly — downstream tools parse them):

```markdown
# Business Model Canvas — [Business Name]

> Generated on [YYYY-MM-DD]. Edit this file as the business evolves.

## Customer Segments
- ...

## Value Propositions
- ...

## Channels
- ...

## Customer Relationships
- ...

## Revenue Streams
- ...

## Key Resources
- ...

## Key Activities
- ...

## Key Partners
- ...

## Cost Structure
- ...

---

## Stress Tests

1. **[Assumption in one line]**
   - Failure mode: ...
   - Disconfirming experiment: ...
```

### Step 2 — Produce `business-model.html`

Read the template pattern in `references/bmc-html-template.md` and produce a single
self-contained HTML file that:

- Renders the canonical Osterwalder 9-block grid (two-row layout with the top row split
  as shown above and the bottom row split between Cost Structure and Revenue Streams).
- Reads brand tokens from `brand-kit/design-system.md` if the file exists in the working
  directory. Otherwise uses neutral defaults: dark text on off-white, simple sans-serif,
  light grid borders.
- Prints cleanly to PDF via CSS paged media (`@page` rules).
- Carries zero network dependencies — no CDN links, no external fonts, no external CSS.
- Includes a footer line: "Generated [YYYY-MM-DD] · `business-model.md` is the source
  of truth."

### Step 3 — Save to the working folder

Save both files to the founder's working directory, not a scratch folder:

- `business-model.md`
- `business-model.html`

This matches the folder contract shared with `brand-workshop` and `pitch-deck`.
See `references/folder-contract.md`.

### Step 4 — Present to the user

Use `present_files` if available. Otherwise emit clickable `computer://` links.
Present the HTML first (visual primary), Markdown second (source of truth).

End with two lines:
- The strongest stress test ("The assumption most likely to kill this business is: …")
- The suggested next step ("The cheapest way to test that this week is: …")

Every run ends this way — first-pass canvases AND updates to existing canvases
AND regenerations. Do not replace these two lines with a summary block, a
"final deliverable" header, or meta-commentary about what changed. The founder
reads the bottom of the canvas for the action, not the top.

---

## Output Files

```
business-model.md              Canonical, editable source of truth
business-model.html            Self-contained visual canvas (primary deliverable)
```

No other files. Do not scatter intermediate drafts across the working folder.

---

## Quality Checklist

Before presenting to the user, verify each:

**Content**
- [ ] Every block has at least one specific, testable claim (no "SMBs", no "the internet")
- [ ] Each Customer Segment maps to at least one Value Proposition written in the segment's language
- [ ] Each Value Proposition has a path to capture value (Revenue Stream) — or is explicitly noted as a loss-leader
- [ ] Each Channel is plausible for the segment it reaches
- [ ] Cost Structure reflects *this* business's cost drivers, not generic startup costs
- [ ] Unknowns are marked `[Unknown — …]` rather than invented
- [ ] Stress Tests section has 3–5 assumptions, each with failure mode and disconfirming experiment

**Rendering**
- [ ] `business-model.md` uses the exact heading structure above (so downstream tools can parse it)
- [ ] `business-model.html` is a single file, opens in a browser, prints cleanly to PDF
- [ ] HTML canvas uses brand tokens if `brand-kit/design-system.md` is present; neutral defaults otherwise
- [ ] No external network dependencies in the HTML (no CDN, no webfont URLs, no `<script src="http...">`)

**Shipping**
- [ ] Both files saved to the founder's working directory (not a scratch folder)
- [ ] Files presented via `present_files` or `computer://` links
- [ ] Response ends with the top stress test + cheapest disconfirming experiment

---

## Cross-Skill Integration

| Skill | When to Use |
|-------|-------------|
| `brand-workshop` (our own) | Before this skill, when a brand identity is needed. This skill reads `brand-kit/design-system.md` if present to style the HTML canvas. |
| `pitch-deck` (our own) | After this skill, to construct an investor-facing pitch using the canvas as input. The pitch-deck skill reads `business-model.md` directly to seed slides 2, 3, 6, 7 and to stress-test the Ask against the Stress Tests section. |
| `team-composer` (our own) | Instead of this skill, when the founder wants a *discussion* on one narrow block rather than a full canvas artifact. |
| `tech-stack-recommendations` (our own) | When Key Resources or Key Activities include technology choices the founder hasn't made yet. |
| `theme-factory` (Anthropic) | When the HTML canvas needs branded styling and no `brand-kit/design-system.md` is present. Apply theme-factory's tokens after content is finalized. |
| `docx` (Anthropic) | When the founder wants the canonical canvas as a `.docx` (board packet, grant application). Hand off the `business-model.md` as source. |
| `web-artifacts-builder` (Anthropic) | For interactive canvas variants (filters, block toggling, nested details). Out of scope for v1 but natural upgrade path. |
| `pdf` (Anthropic) | When merging the canvas into a larger packet (investor memo, pitch dossier). The HTML already prints cleanly to PDF via CSS paged media; `pdf` is for programmatic assembly across multiple artifacts. |

**Principle:** this skill owns the nine-block artifact. It does not do discussion-only
narrow questions, does not do financial projections, does not do validation research.
Hand off rather than over-reach.

**Graceful degradation:** if a referenced skill is not installed, this skill still
ships `business-model.md` + `business-model.html` — downstream integrations are
enhancements, not requirements.
