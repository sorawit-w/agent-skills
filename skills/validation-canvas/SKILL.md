---
name: validation-canvas
description: Elicits founder beliefs block-by-block to produce a Lean Canvas (Maurya) + Value Proposition Canvas (Osterwalder) combined artifact as both `validation-canvas.md` (canonical, editable) and `validation-canvas.html` (self-contained visual). Job — "what do we believe?" (declarative). Adapts to founder experience via a 3-question intake at invocation that maps to Guided / Focused / Compressed-with-Challenge modes. Use whenever the user asks to "build a validation canvas", "lean canvas for my startup", "VPC", "value proposition canvas", "map out my business model", "fill in the lean blocks", or uploads a product idea and asks how to articulate the model. Also trigger when the user has brand-workshop output ready and wants the next strategy artifact, or when `@startup_strategist` is the right lens. Even if the user only asks for one block (e.g., "help me figure out my unfair advantage"), use this skill — the other blocks stress-test that block's claims. NOTE: this skill replaces the prior `business-model-canvas` (BMC) skill; the Lean Canvas is the right altitude for an idea-stage founder, where BMC was wrong altitude (Series-A operating plan). For nine-block BMC compatibility (board packets, regulated pitches), use `team-composer` with `@startup_strategist` instead.
---

# Validation Canvas

Produce a rigorous **Lean Canvas + Value Proposition Canvas** combined artifact from
founder inputs. Each block is a stress-tested *belief*, not a template field. The
canvas is the primary deliverable; the interview that produces it is where most of
the value lives. The job here is declarative — *what do we believe?* — and is the
upstream half of validation. The downstream half (*what have we proven?*) is owned
by the `riskiest-assumption-test` skill that runs after this one.

## What this skill produces

Always produced under the resolved canvas root (see Phase 0.0 for path
resolution; default is `docs/canvas/` for solo runs,
`docs/startup-kit/canvas/` when invoked via orchestrator):

1. **`validation-canvas.md`** — canonical, editable Markdown with two top-level
   sections: `## Lean Canvas` (nine blocks per Maurya) and `## Value Proposition
   Canvas` (six blocks per Osterwalder), plus a `## Stress Tests` section listing
   the assumptions most likely to fail. Headings are load-bearing — `pitch-deck`,
   `riskiest-assumption-test`, and `startup-grill` grep them by name.
2. **`validation-canvas.html`** — single self-contained HTML file rendering the
   Lean Canvas grid (top) and the VPC fit diagram (bottom) visually. Opens in any
   browser, prints cleanly to PDF, zero network dependencies.

Both files carry the same content — the HTML is the visual primary; the Markdown is
the source of truth founders edit as the business evolves.

## What this skill is NOT

- **Not a 9-block Osterwalder Business Model Canvas.** That's a Series-A operating
  plan tool. This skill ships the Lean Canvas (Maurya) — Problem, Customer Segments,
  UVP, Solution, Channels, Revenue Streams, Cost Structure, Key Metrics, Unfair
  Advantage — because that's the right altitude for an idea-stage founder. If a
  board or grant explicitly requires the Osterwalder grid (Key Resources, Key
  Activities, Key Partners, Customer Relationships), use `team-composer` with
  `@startup_strategist` for a discussion-grade fill.
- **Not an assumption-testing skill.** Naming what you believe is half the job.
  Naming what you've *proven* is `riskiest-assumption-test`'s job — a separate
  step that runs after this one. Do not bundle the two.
- **Not a pitch deck builder.** Pitch construction belongs to `pitch-deck`.
- **Not a financial model.** Revenue Streams and Cost Structure are *structural*
  (how money flows), not *quantitative* (how much and when).
- **Not market research.** The canvas records the founder's current thinking. It
  does not go validate it. Validation is the next step.
- **Not a competitive-analysis skill.** SWOT, Porter's Five Forces, and Wardley
  mapping are explicitly out of scope — wrong altitude / wrong stage / overlap
  with `startup-grill`.
- **Not a substitute for domain expertise.** In regulated domains (fintech, health,
  education with minors), the canvas surfaces the right questions but does not
  answer regulatory ones — escalate to `team-composer` with
  `@legal_compliance_advisor`.

## Skill Boundaries

This skill intentionally overlaps with `team-composer` (`@startup_strategist` is
active there too) but differs in deliverable:

- **Use `validation-canvas` when:** the founder wants a *persistent artifact* they
  can return to, edit, and share. The Lean Canvas + VPC structure is the
  load-bearing feature.
- **Use `team-composer` with `@startup_strategist` when:** the founder wants a
  *discussion* on one narrow question (pricing model, channel strategy, partner
  selection) without committing to a full canvas. Discussion-grade, not
  artifact-grade.

> **Companion plugin:** `brand-workshop`. If a brand artifact exists (at
> `<brand-root>/design-system.md` per the conventions doc, or legacy
> `brand-kit/design-system.md` at cwd root for backward compat), the HTML
> canvas adopts the brand's color tokens from it. If not, falls back to
> neutral defaults.

> **Pipeline placement.** This skill is step 2 of 5 in the startup pipeline:
> `brand-workshop` → **`validation-canvas`** → `riskiest-assumption-test` →
> `pitch-deck` → `startup-grill`. See [`references/folder-contract.md`](references/folder-contract.md)
> for the inter-step contract, gate weights, and loop-back protocol.

---

## The Two Canvases

Claude must internalize the structure of both canvases before interviewing.

### Lean Canvas (Maurya) — nine blocks

The right altitude for an idea-stage founder. Replaces BMC's Key Activities / Key
Resources / Key Partners / Customer Relationships with **Problem**, **Solution**,
**Key Metrics**, and **Unfair Advantage** — the things that actually decide
whether the idea survives contact with reality.

```
┌───────────────────┬──────────────────┬──────────────────┬──────────────────┬───────────────────┐
│ Problem           │ Solution         │ Unique Value     │ Unfair Advantage │ Customer          │
│                   │                  │ Proposition      │                  │ Segments          │
│ (top 3 problems)  │ (top 3 features) │ (single, clear,  │ (can't be easily │ (target users     │
│                   │                  │  compelling)     │  copied/bought)  │  + early adopters)│
│                   ├──────────────────┤                  ├──────────────────┤                   │
│                   │ Key Metrics      │                  │ Channels         │                   │
│                   │ (key activities  │                  │ (path to         │                   │
│                   │  measured)       │                  │  customers)      │                   │
├───────────────────┴──────────────────┴──────────────────┴──────────────────┴───────────────────┤
│ Cost Structure                                  │ Revenue Streams                              │
└─────────────────────────────────────────────────┴──────────────────────────────────────────────┘
```

### Value Proposition Canvas (Osterwalder) — six blocks, two sides

Forces alignment between *what the customer needs* (Customer Profile) and *what
you offer* (Value Map). Run as a second pass after the Lean Canvas.

```
       Customer Profile (right circle)              Value Map (left square)
     ┌──────────────────────────────┐         ┌──────────────────────────────┐
     │  Customer Jobs               │         │  Products & Services         │
     │  (functional, social,        │  ◄───►  │  (the offering)              │
     │   emotional jobs)            │         │                              │
     ├──────────────────────────────┤         ├──────────────────────────────┤
     │  Pains                       │  ◄───►  │  Pain Relievers              │
     │  (frustrations, obstacles,   │         │  (how the offering reduces   │
     │   risks)                     │         │   each pain)                 │
     ├──────────────────────────────┤         ├──────────────────────────────┤
     │  Gains                       │  ◄───►  │  Gain Creators               │
     │  (outcomes, benefits         │         │  (how the offering produces  │
     │   sought)                    │         │   each gain)                 │
     └──────────────────────────────┘         └──────────────────────────────┘
                                  Fit Check
```

**Fit check:** for each Pain, name the Pain Reliever. For each Gain, name the Gain
Creator. Pains without relievers and Gains without creators are red flags — they
belong in Stress Tests.

See `references/canvas-blocks.md` for the deep definition of each block, canonical
examples, and the stress tests that surface shaky assumptions.

---

## Phase 0: Experience-Adaptive Intake (RUN FIRST, BEFORE ANY CANVAS WORK)

**Goal:** calibrate the rigor and tone of the interview to the founder's actual
experience level. A first-time founder needs definitions and examples; a repeat
founder needs push-back, not teaching.

### Step 0.0 — Path resolution + manifest awareness (v2.2.0+)

**Resolve the canvas root** once at invocation, in this precedence order
(canonical chain):

1. **Explicit `output_dir` arg** (passed by `startup-launch-kit`) → use as-is.
2. **`STARTUP_KIT_DOCS_ROOT` env var** set → `${STARTUP_KIT_DOCS_ROOT}/canvas/`.
3. **Smart default — `docs/startup-kit/` exists** → `docs/startup-kit/canvas/`.
   Surface the smart-default notice: *"Writing to `docs/startup-kit/canvas/`
   (smart default — `docs/startup-kit/` exists). Set
   `STARTUP_KIT_DOCS_ROOT=./docs` to write standalone instead."*
4. **Solo fallback** → `docs/canvas/`.

**Manifest awareness.** Look for `kit-manifest.json` at
`<resolved-kit-root>/kit-manifest.json` first (e.g.,
`docs/startup-kit/kit-manifest.json`); fall back to the working-directory
root for backward compat. If found at the legacy path, surface a one-line
migration suggestion. Use it as a hint, never as a bypass:

- **Intake-cache (special case for this skill):** if the manifest's
  `intake_answers` cache is populated (the orchestrator already asked the
  3-question intake), present the cached answers and **ask the founder to
  confirm or update them** — do **NOT** silently skip Step 0.1. Single code
  path through Phase 0; manifest is a hint that lets you start with defaults.
  Example prompt: *"Manifest says: repeat founder, no domain experience, has
  segment experience → focused mode. Confirm, or update any of these?"*
- If the manifest lists `validation-canvas` as `completed` with a recent
  mtime, surface that fact: *"Manifest says you ran validation-canvas on
  [date]. Update mode (revise specific blocks per loop-back protocol),
  fresh run, or skip to the next step?"*
- Manifest read failures (corrupt JSON, missing fields) are non-fatal — log
  the issue inline and proceed as if no manifest exists.

After this skill ships its artifacts (Phase 3 — render & ship), if a
manifest exists, append/update this skill's entry. Use atomic write (write
`.tmp`, then rename). Increment the `iterations` counter on update-mode
runs. If the manifest doesn't exist, do **NOT** create it — that's the
`startup-launch-kit` orchestrator's job. See
[`startup-launch-kit/references/manifest-schema.md`](../startup-launch-kit/references/manifest-schema.md)
for the schema.

### Step 0.1 — Scan context for experience signals

Before asking any calibration questions, scan the conversation context, working
directory, and any provided materials for signals on three dimensions:

1. **Founding history.** Has the founder run a startup that reached paying
   customers? Look for: prior `validation-canvas.md` files, memory entries,
   explicit statements ("at my last startup…"), LinkedIn-style language ("3rd
   time founder", "ex-Stripe").
2. **Domain experience.** Has the founder worked professionally in this idea's
   domain? Look for: stated work history, technical depth in the idea description,
   industry-specific vocabulary used naturally.
3. **Customer-segment experience.** Does the founder have direct experience with
   the customer they're targeting? Look for: "I am the customer" framings,
   anecdotes from the segment, prior roles inside the segment.

### Step 0.2 — Ask only the delta

For each of the three dimensions:

- **Clear signal** → use it silently. Do not ask the question.
- **Ambiguous or missing signal** → ask the question.

The three calibration questions, asked verbatim when needed:

1. *"Have you founded or co-founded a startup that reached paying customers
   before?"*
2. *"Is this idea in a domain you've worked in professionally?"*
3. *"Do you have direct experience with this customer segment?"*

**Hard rule — ask immediately at invocation, BEFORE canvas work begins.** Never
ask mid-canvas. Never ask post-canvas. Calibration is a Phase 0 gate; commit to
the inferred mode and adjust through behavior.

### Step 0.3 — Map answers to mode

The three answers form a 2×2×2 matrix. Map to one of three modes:

| Founding history | Domain | Customer | Mode |
|---|---|---|---|
| No | No | Either | **Guided** (full walkthrough, definitions, ~60–90 min) |
| No | Yes | Either | **Focused** (lighter scaffolding, emphasize underweighted boxes) |
| Yes | Yes | Either | **Compressed-with-Challenge** (rapid-fill ~15–20 min, push back hard) |
| Yes | No | Either | **Focused** (founder knows process, needs domain scaffolding) |
| No | No | Yes | **Focused** (founder knows the customer, needs structural scaffolding) |
| Yes | Yes | Yes | **Compressed-with-Challenge** (push back hardest — risk of pattern-matching from prior) |

**Mode descriptions:**

- **Guided** — full walkthrough. Define each block before asking. Offer 2–3
  examples per block from `references/canvas-blocks.md`. Ask 2–3 questions per
  block. Pace: ~60–90 minutes for a first pass.
- **Focused** — lighter scaffolding. Skip definitions for blocks the founder
  clearly understands. Emphasize commonly underweighted boxes: **channels** and
  **cost structure** for ex-engineers; **key metrics** and **customer segments**
  for ex-designers; **unfair advantage** and **problem** for ex-PMs. Pace:
  ~30–45 minutes.
- **Compressed-with-Challenge** — rapid-fill. The skill's job shifts from
  teaching to *challenging*. Accept short answers but push back on glib ones.
  Pace: ~15–20 minutes.

### Step 0.4 — Confirm mode in one line

Before proceeding to canvas work, confirm the inferred mode in **one line** so the
founder can correct you. Examples:

- *"Treating this as a repeat-founder session — say so if I should slow down."*
- *"You haven't worked in this segment before, so I'll spend more time on the
  Customer Profile — say so if you want me to skip ahead."*
- *"First-pass guided mode. I'll define each block as we go. Stop me anytime."*

Then proceed to Phase 1.

### Hard rules for Phase 0

- **Never delegate intake to `grill-with-docs`.** That skill is for stress-testing
  plans against project docs — wrong job, wrong tone, wrong target for founder
  calibration.
- **Mode sets default rigor; observed answer quality overrides it.** A
  self-declared "repeat founder" giving glib answers gets push-back regardless of
  declared mode. The 3-question intake calibrates the *opening posture*, not a
  permanent contract.
- **One sharp exception** — a repeat founder doing a *near-identical* startup to
  a prior one (same segment, same UVP, just a different brand) can skim the
  canvas. Flag this as the exception, not the norm: *"You've shipped this canvas
  before for a similar idea — I'll move fast and only stop on real deltas."*

---

## Phase 1: Discovery (Founder Interview)

**Goal:** Extract enough raw material to fill each block substantively. A canvas
filled with "freelancers and small businesses" in Customer Segments is worthless
— the job is to force specificity.

### Role setup

Run the interview in first-person voice with these roles active. If the user
invokes `team-composer` separately, skip duplicates.

| Role | Lens |
|------|------|
| `@startup_strategist` | Workshop lead. Asks block-by-block. Pushes for specificity and internal consistency. |
| `@vc_partner` | Read-test. "Could a Series A partner understand this in 90 seconds?" Flags handwaving on Revenue / Traction adjacency. |
| `@finance_manager` | Stress-tests Revenue Streams and Cost Structure. Flags missing unit economics or undefined payment triggers. |
| `@senior_product_manager` | UVP ↔ Customer Segment alignment. Flags "value props" that are really feature lists. |

### Lean Canvas interview protocol

Go through the **Lean Canvas reasoning order** (problem-and-customer-first), one
block at a time:

1. **Problem** (top 3 problems for the segment)
2. **Customer Segments** (target users + early adopters, named separately)
3. **Unique Value Proposition** (single, clear, compelling)
4. **Solution** (top 3 features that address the problems)
5. **Channels** (path to customers)
6. **Revenue Streams** (how money is captured)
7. **Cost Structure** (the actual cost drivers, not generic startup costs)
8. **Key Metrics** (the activities that get measured to know if it's working)
9. **Unfair Advantage** (what can't be easily copied or bought)

For each block:

1. Read the block's prompts from `references/founder-prompts.md`.
2. **In Guided mode:** define the block first, offer 1–2 examples, then ask up to
   3 questions. **In Focused mode:** ask straight to questions; offer definitions
   only if the founder hesitates. **In Compressed mode:** ask one direct question
   and push back if the answer is glib.
3. Capture the founder's answer in their own words. Do not paraphrase into
   consultant-ese.
4. Flag the assumption most likely to fail. Name it. These roll up into the final
   Stress Tests section.

**What "enough" looks like:** each block has at least one specific, testable claim.
"Targets SMBs" is not specific. "Targets 5–25 person legal-tech firms in the US
northeast that currently use paper intake forms" is specific.

**What to do when the founder doesn't know:** mark the block
`[Unknown — ${what-to-learn}]` and add a row to the Stress Tests section: "We
don't yet know ${what}; to find out, do ${experiment}." A canvas with honest
unknowns is more useful than a canvas with invented confidence.

### Value Proposition Canvas interview protocol (run after Lean Canvas)

Once the Lean Canvas is filled, run a second focused pass on the VPC — this
deliberately re-asks Customer Segments + UVP from a different angle (the
customer's perspective, not the founder's), which surfaces gaps the Lean Canvas
alone misses.

Right side first (Customer Profile — the founder may not know all of this; mark
unknowns):

1. **Customer Jobs** — functional, social, and emotional jobs the customer is
   trying to get done.
2. **Pains** — frustrations, obstacles, risks the customer encounters.
3. **Gains** — outcomes and benefits the customer is seeking.

Then the left side (Value Map — what your offering does, mapped 1:1 to the right
side):

4. **Products & Services** — the actual offering.
5. **Pain Relievers** — for each Pain, name the specific Pain Reliever (or mark
   the pain as un-relieved).
6. **Gain Creators** — for each Gain, name the specific Gain Creator.

**Fit Check (mandatory):** at the end of VPC, list every Pain without a Reliever
and every Gain without a Creator. These are red flags — they roll up into Stress
Tests.

### When the user skips the interview

If the founder gives you a paragraph dump or says "just fill it in from what I
said," still apply the thin-input rule: any block where your fill comes from
inference, not the founder's words, gets marked
`[Unknown — founder did not specify: <what's missing>]`.

Why: a canvas full of plausible-sounding AI guesses is worse than a canvas with 3
explicit unknowns. The unknowns are where the next founder conversation goes.

---

## Phase 2: Draft & Consistency Check

**Goal:** Produce the canonical canvas content and catch cross-block contradictions
before rendering.

### Step 1 — Draft all blocks

Write each Lean Canvas block 2–4 bullets long. Bullets are specific claims, not
categories. Write each VPC block as a tight list (3–6 items) — Jobs, Pains, Gains
are the customer's, not yours. See `references/canvas-blocks.md` for good/bad
examples per block.

### Step 2 — Consistency pass (MANDATORY, do not skip)

This rule applies even when the user explicitly asks to skip it
("I don't have time," "I know my business cold," "just render it").

Why: the canvas's value is the cross-block pressure test. Skipping it produces a
template that looks like a canvas but carries none of the stress-test signal. The
founder loses the one thing they came for.

How to apply: decline the skip, then offer a fast path —

- Run the consistency checks silently
- Surface only contradictions that would block the canvas from shipping
- Skip the prose write-up, keep the structured findings

Never emit a canvas with the consistency check silently omitted.

Run these seven checks:

1. **Problem ↔ Customer Segments:** Is each Problem genuinely felt by the named
   Customer Segments (not "people in general")?
2. **UVP ↔ Customer Segments:** Is the UVP written in the segment's language
   (not the founder's)?
3. **Solution ↔ Problem:** Does each Solution feature address a stated Problem?
   (Solutions without problems are gold-plating.)
4. **Channels ↔ Customer Segments:** Is each Channel a plausible way to reach the
   specific segment (not "the internet")?
5. **Revenue ↔ UVP:** Is there a revenue stream that captures part of the value
   the UVP creates? A valuable free feature with no upsell path is a flag, not a
   violation — note it.
6. **Cost Structure ↔ Solution + Channels:** Does the Cost Structure reflect the
   *actual* cost drivers of the Solution and Channels, or is it a generic list
   of startup costs?
7. **VPC Fit:** Does every Pain have a Reliever, and every Gain have a Creator?
   (Unrelieved pains and uncreated gains are explicit red flags.)

### Step 3 — Stress Tests

At the end of `validation-canvas.md`, add a `## Stress Tests` section with the
3–5 assumptions most likely to break. For each:

- The assumption in plain language.
- Why the business fails if it's wrong.
- The cheapest experiment that would disconfirm it.

Stress tests are the most-read part of the canvas six months later AND the
**direct hand-off to `riskiest-assumption-test`** — that skill greps this
section first to seed its assumption dump. Do not treat them as filler.

---

## Phase 3: Render & Ship

**Goal:** Produce `validation-canvas.md` and `validation-canvas.html`, save them
to a known folder, and present them to the user.

### Step 1 — Produce `validation-canvas.md`

Structure (headings must match exactly — downstream tools parse them):

```markdown
# Validation Canvas — [Business Name]

> Generated on [YYYY-MM-DD]. Edit this file as the business evolves.

## Lean Canvas

### Problem
- ...

### Customer Segments
- ...

### Unique Value Proposition
- ...

### Solution
- ...

### Channels
- ...

### Revenue Streams
- ...

### Cost Structure
- ...

### Key Metrics
- ...

### Unfair Advantage
- ...

## Value Proposition Canvas

### Customer Jobs
- ...

### Customer Pains
- ...

### Customer Gains
- ...

### Products & Services
- ...

### Pain Relievers
- ... (for each Pain above)

### Gain Creators
- ... (for each Gain above)

---

## Stress Tests

1. **[Assumption in one line]**
   - Failure mode: ...
   - Disconfirming experiment: ...
```

The heading anchors `### Customer Segments`, `### Unique Value Proposition`,
`### Revenue Streams`, `### Customer Jobs`, `### Customer Pains`, `### Customer
Gains`, and `## Stress Tests` are **load-bearing cross-plugin contracts** —
`pitch-deck`, `riskiest-assumption-test`, and `startup-grill` grep these by
name. If you rename, update those skills' Phase 1 inputs in lockstep.

### Step 2 — Produce `validation-canvas.html`

Read the template pattern in `references/canvas-html-template.md` and produce a
single self-contained HTML file that:

- Renders the Lean Canvas grid (top half) and the VPC fit diagram (bottom half).
- Reads brand tokens from the brand artifact at `<kit-root>/brand/design-system.md`
  (sibling of `<kit-root>/canvas/`) if it exists. Falls back to the legacy
  path `brand-kit/design-system.md` (cwd-relative) for backward compat.
  Otherwise uses neutral defaults.
- Prints cleanly to PDF via CSS paged media (`@page` rules).
- Carries zero network dependencies.
- Includes a footer line: "Generated [YYYY-MM-DD] · `validation-canvas.md` is
  the source of truth."

### Step 3 — Save to the resolved canvas folder

Save both files to the canvas folder resolved in Phase 0.0 Step 0.0:

- `<canvas-root>/validation-canvas.md`
- `<canvas-root>/validation-canvas.html`

Where `<canvas-root>` is `docs/startup-kit/canvas/` (orchestrated),
`docs/canvas/` (solo default), or the env-var override. Create the folder
if absent. This matches the folder contract shared with `brand-workshop`,
`riskiest-assumption-test`, `pitch-deck`, and `startup-grill`. See
`references/folder-contract.md` for cross-skill loop-back protocol.

### Step 4 — Present to the user

Use `present_files` if available. Otherwise emit clickable `computer://` links.
Present the HTML first (visual primary), Markdown second (source of truth).

End with **three lines**:

1. *"The assumption most likely to kill this business is: …"*
2. *"The cheapest way to test that this week is: …"*
3. *"Next step: run `riskiest-assumption-test` to convert your top assumptions
   into testable hypotheses with success criteria."*

Every run ends this way — first-pass canvases AND updates to existing canvases
AND regenerations. The third line is the **medium gate** — the founder is
expected to run `riskiest-assumption-test` next, before pitch-deck. Do not
replace these three lines with a summary block, a "final deliverable" header, or
meta-commentary about what changed.

---

## Update mode (loop-back from downstream)

When this skill is invoked and `validation-canvas.md` already exists at
the resolved canvas root (or its legacy fallback), treat the run as an
**update**, not a rewrite:

1. **Read the existing file first.** Do not overwrite blocks the founder hasn't
   asked to change.
2. **Detect what changed upstream.** If the assumption-test plan exists
   (`<rat-root>/assumption-test-plan.md` or legacy
   `rat/assumption-test-plan.md`) and has populated `## Results`, read it.
   Invalidated hypotheses point to specific Lean Canvas / VPC blocks that
   need revision.
3. **Confirm the scope of update.** *"Your last canvas had X. The RAT results
   invalidated [hypothesis] — that maps to [block]. Update just that block, or
   re-run the full canvas?"*
4. **Apply mode-appropriate rigor to the changed blocks.** Compressed mode
   founders get push-back on glib revisions; first-timers get the full
   block-redo flow.
5. **Mark the change visibly.** The output canvas should show updated blocks
   marked `<!-- updated YYYY-MM-DD: <reason> -->`.

This is the **loop-back protocol** — invalidated assumptions are a normal action,
not a failure mode. See `references/folder-contract.md` for the full protocol.

---

## Output Files

```
<canvas-root>/validation-canvas.md     Canonical, editable source of truth
<canvas-root>/validation-canvas.html   Self-contained visual canvas (primary deliverable)
```

Where `<canvas-root>` resolves per Phase 0.0 Step 0.0:

- `docs/startup-kit/canvas/` — orchestrated (via `startup-launch-kit`)
- `docs/canvas/` — solo default
- `docs/startup-kit/canvas/` — solo with `docs/startup-kit/` smart default
- `${STARTUP_KIT_DOCS_ROOT}/canvas/` — env-var override

No other files. Do not scatter intermediate drafts across the working folder.

---

## Quality Checklist

Before presenting to the user, verify each:

**Phase 0 (Intake)**
- [ ] 3-question calibration ran at invocation, BEFORE canvas work
- [ ] Mode confirmed in one line to the founder
- [ ] Mode-appropriate scaffolding applied (Guided / Focused / Compressed)

**Content**
- [ ] Every Lean Canvas block has at least one specific, testable claim (no "SMBs", no "the internet")
- [ ] Every Pain has a Pain Reliever (or is explicitly marked unrelieved)
- [ ] Every Gain has a Gain Creator (or is explicitly marked uncreated)
- [ ] UVP is written in the customer segment's language, not the founder's
- [ ] Each Solution feature addresses a stated Problem (no gold-plating)
- [ ] Channels are concrete (named platforms, named partnerships, named tactics)
- [ ] Cost Structure reflects *this* business's cost drivers, not generic startup costs
- [ ] Key Metrics are measurable activities, not aspirational outcomes
- [ ] Unfair Advantage is something competitors can't easily copy or buy
- [ ] Unknowns are marked `[Unknown — …]` rather than invented
- [ ] Stress Tests section has 3–5 assumptions, each with failure mode and disconfirming experiment
- [ ] **No SWOT, no Porter, no Wardley** — those route to `team-composer` or `startup-grill`

**Rendering**
- [ ] `validation-canvas.md` uses the exact heading structure above (so downstream tools can parse it)
- [ ] `validation-canvas.html` is a single file, opens in a browser, prints cleanly to PDF
- [ ] HTML canvas uses brand tokens if `<kit-root>/brand/design-system.md` (or legacy `brand-kit/design-system.md`) is present; neutral defaults otherwise
- [ ] No external network dependencies in the HTML

**Shipping**
- [ ] Both files saved to the resolved canvas folder per Phase 0.0 Step 0.0 (not cwd root, not a scratch folder)
- [ ] Smart-default notice surfaced if smart-default fired
- [ ] Files presented via `present_files` or `computer://` links
- [ ] Response ends with the three lines (top stress test + cheapest experiment + next-step gate to `riskiest-assumption-test`)

---

## Cross-Skill Integration

| Skill | When to Use |
|-------|-------------|
| `brand-workshop` (our own) | Before this skill, when a brand identity is needed. This skill reads `<kit-root>/brand/design-system.md` (or legacy `brand-kit/design-system.md`) if present to style the HTML canvas. |
| `riskiest-assumption-test` (our own) | **Required next step** (medium gate). After this skill ships, the founder is expected to run `riskiest-assumption-test` to convert Stress Tests into falsifiable hypotheses with success criteria. |
| `pitch-deck` (our own) | Two steps downstream. The pitch-deck skill reads `validation-canvas.md` from the resolved canvas folder to seed slides 2, 3, 6 and to stress-test the Ask. Pitch-deck is gated on `<rat-root>/assumption-test-plan.md` having populated `## Results` (heavy gate). |
| `startup-grill` (our own) | Last step. Reads `validation-canvas.md` Stress Tests, RAT results, and pitch deck slides as direct grilling ammunition. |
| `team-composer` (our own) | Instead of this skill, when the founder wants a *discussion* on one narrow block rather than a full canvas artifact. Also when a 9-block Osterwalder BMC is explicitly required (board, grant). |
| `tech-stack-recommendations` (our own) | When Solution or Channels include technology choices the founder hasn't made yet. |
| `theme-factory` (Anthropic) | When the HTML canvas needs branded styling and no brand artifact (`<kit-root>/brand/design-system.md` or legacy `brand-kit/design-system.md`) is present. Apply theme-factory's tokens after content is finalized. |
| `docx` (Anthropic) | When the founder wants the canonical canvas as a `.docx` (board packet, grant application). Hand off `validation-canvas.md` as source. |
| `web-artifacts-builder` (Anthropic) | For interactive canvas variants (filters, block toggling, nested details). Out of scope for v1 but natural upgrade path. |
| `pdf` (Anthropic) | When merging the canvas into a larger packet. The HTML already prints cleanly to PDF; `pdf` is for programmatic assembly across multiple artifacts. |

**Principle:** this skill owns the **declarative artifact** — what the founder
believes about the business model. It does not test those beliefs (that's
`riskiest-assumption-test`), does not pitch them (that's `pitch-deck`), does not
adversarially probe them (that's `startup-grill`), and does not do
discussion-only narrow questions (that's `team-composer`). Hand off rather than
over-reach.

**Graceful degradation:** if a referenced skill is not installed, this skill
still ships `validation-canvas.md` + `validation-canvas.html` — downstream
integrations are enhancements, not requirements.
