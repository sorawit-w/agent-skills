---
name: ai-ux-review
description: >
  Audit an AI product against structured human-AI design questions — classical UX (user need,
  mental models, trust calibration, feedback + control, graceful failure) plus the gen-AI
  integrity surface older frameworks miss: hallucination handling, output verifiability,
  provenance + citation, prompt-injection exposure, and agent autonomy. Produces an editable
  Markdown artifact plus a self-contained HTML report under `docs/ai-ux/`. Use when the user
  asks to "review my AI feature", "audit my AI product", "is my AI experience trustworthy",
  "responsible AI UX review", or ships an LLM feature and wants a pre-launch trust review. If
  `validation-canvas` output exists, assume the business model is settled and focus on UX
  execution. Does NOT trigger for: lean-canvas work (`validation-canvas`); adversarial
  pre-mortem with a verdict (`startup-grill`); SKILL.md audits (`skill-evaluator`); brand/logo
  work (`brand-workshop`); building eval pipelines or writing eval code (names gaps only).
---

# AI UX Review

Audit an AI product or feature against a structured set of human-AI design
questions. Each of the seven blocks is a *gap detector*, not a template field —
the value of this skill is whether the elicitation surfaces design decisions the
builder hadn't made yet, not whether the artifact looks complete.

The job is **design-completeness**: *have we designed the human side of this
responsibly?* It covers both the classical human-AI UX surface (user need,
mental models, trust, feedback, errors) and the gen-AI integrity surface that
showed up after 2022 (hallucination handling, verifiability, provenance,
prompt-injection exposure, agent autonomy).

This is not a quality assessment of an AI product's output. It is a structured
review of whether the *design around* that output is intentional.

## What this skill produces

Always produced under the resolved review root (default `docs/ai-ux/`):

1. **`ai-ux-review.md`** — canonical, editable Markdown with one top-level
   section per block (seven blocks total), plus a `## Gap Summary` section
   listing the design decisions still unmade. Headings are load-bearing for
   future composability with a potential `ai-eval-rubric` companion skill.
2. **`ai-ux-review.html`** — single self-contained HTML file rendering the
   seven blocks visually, with gap-marker glyphs for blocks where the builder
   said "we haven't designed for this yet." Opens in any browser, prints
   cleanly to PDF, zero network dependencies.

Both files carry the same content — the HTML is the visual primary; the
Markdown is the source of truth the builder edits as the product matures.

## What this skill is NOT

- **Not a lean canvas or business-model review.** That's `validation-canvas`.
  This skill assumes the business model is settled and audits the UX
  execution layer.
- **Not adversarial.** No verdict label, no kill report. This skill is
  cooperative gap detection. For "would this survive a VC tear-down?", use
  `startup-grill`.
- **Not a SKILL.md audit.** That's `skill-evaluator`. This skill audits AI
  *product* designs, not agent-skill text.
- **Not a substitute for user research.** It surfaces "have you spoken to
  users about this?" but does not run interviews. Hand off to actual research
  when blocks expose unknowns.
- **Not an evaluation-pipeline builder.** Block 7 *names* eval gaps (what
  "working" looks like, what's measurable, what's a proxy). It does not
  implement metrics, label datasets, or write eval code. If you need that
  layer, build it separately or in a future companion skill.
- **Not a pitch-deck builder.** Pitch construction belongs to `pitch-deck`.
- **Not a substitute for regulatory advice.** In domains with formal AI
  regulation (EU AI Act high-risk systems, FDA SaMD, FTC AI guidance), this
  skill surfaces the questions but does not answer them. Escalate to
  `team-composer` with `@legal_compliance_advisor` for compliance work.

## Skill Boundaries

This skill intentionally overlaps with `team-composer` (`@ux_researcher` and
`@ai_safety_specialist` are active there too) but differs in deliverable:

- **Use `ai-ux-review` when:** the builder wants a *persistent artifact* they
  can return to, edit, and share. The seven-block structure and the gap
  summary are the load-bearing features.
- **Use `team-composer` with `@ux_researcher` + `@ai_safety_specialist` when:**
  the builder wants a *discussion* on one narrow question (one specific trust
  affordance, one prompt-injection mitigation) without committing to a full
  review. Discussion-grade, not artifact-grade.

When `validation-canvas` output already exists in the working folder, this
skill reads it as context — Problem, Customer Segments, UVP are inputs, not
re-elicited. Block 1 ("Why AI here?") becomes a pressure test rather than a
discovery.

> **Influences.** This skill is inspired by Google's [People + AI
> Guidebook](https://pair.withgoogle.com/guidebook/) (CC BY-NC-SA 4.0). The
> Guidebook's six-chapter scaffolding is the conceptual ancestor of blocks
> 1–5. This skill is **not a derivative work** under copyright law — it uses
> general AI UX concepts (ideas / facts, not protected expression) and
> authors its own elicitation flow, probes, and acceptance criteria. No
> Guidebook prose, worksheets, illustrations, or pattern names are
> reproduced. See `README.md` for full attribution.

---

## The Seven Blocks

Claude must internalize all seven before interviewing. Blocks 1–5 cover the
classical human-AI UX surface; block 6 is the gen-AI integrity layer; block 7
closes the loop with success measurement.

| # | Block | Core question |
|---|-------|---------------|
| 1 | **Why AI here?** | What human task is the AI doing, and what makes AI the right tool here vs. a deterministic alternative? |
| 2 | **Mental model** | What model will users build of how this works, and where will their model diverge from reality? |
| 3 | **Trust calibration** | When and how does the system surface confidence, sources, or limits? What are the under-trust and over-trust failure paths? |
| 4 | **Feedback & control** | What can users do when the AI is wrong? How do they correct, override, hand off, or take over? |
| 5 | **Errors & graceful failure** | What does failure look like in the UI, and what's the recovery path per severity tier? |
| 6 | **Output integrity** | Hallucination handling, provenance + citation, output verifiability, prompt-injection surface, multi-turn drift, agent-autonomy levels. |
| 7 | **Success & evaluation** | What does "working" mean in production from the user's perspective? What's measurable, what's a proxy, what's left to judgment? |

See `references/blocks/01-why-ai.md` through `references/blocks/07-success-eval.md`
for each block's deep probe questions, acceptance criteria, and common gap
patterns. The skill body uses these references lazily — read them when the
phase calls for them, not all up front.

---

## Phase 0: Intake (RUN FIRST, BEFORE ANY BLOCK WORK)

**Goal:** establish context — what's being reviewed, who built it, what
artifacts already exist — so the elicitation can adapt.

### Step 0.1 — Resolve the review root

Look for these in order; first match wins:

1. **Explicit `output_dir` arg** → use as-is.
2. **`STARTUP_KIT_DOCS_ROOT` env var** → `${STARTUP_KIT_DOCS_ROOT}/ai-ux/`.
3. **Smart default — `docs/startup-kit/` exists** → `docs/startup-kit/ai-ux/`.
   Surface: *"Writing to `docs/startup-kit/ai-ux/` (smart default — kit folder
   exists). Set `STARTUP_KIT_DOCS_ROOT=./docs` for standalone."*
4. **Solo fallback** → `docs/ai-ux/`.

If a prior `ai-ux-review.md` exists at the resolved root, this is an
**update-mode** run — see "Update mode" below.

### Step 0.2 — Scan for adjacent artifacts

Before asking questions, check for files this skill can read as context:

- **`<resolved-canvas-root>/validation-canvas.md`** — if present, the business
  model is settled. Read it. Block 1's probes shift from "what's the user
  task" (discovery) to "is your stated UVP defensible without the AI?"
  (pressure test).
- **`<resolved-brand-root>/DESIGN.md`** — if present, use brand tokens for
  the HTML output. Extract `colors.primary` from YAML front matter per the
  [Google Labs spec](https://github.com/google-labs-code/design.md).
- **Spec / PRD / prototype description** — if the user attached or referenced
  one, read it. Don't re-ask for information already there.

### Step 0.3 — Establish three intake facts

Ask only the ones not already obvious from context:

1. **What's the AI doing?** One sentence — what the AI feature actually does
   for the user. ("Generates email drafts from a one-line prompt." "Suggests
   replies in a customer-support thread." "Routes incoming tickets to the
   right team.")
2. **Where in the lifecycle?** Idea / prototype / in development / shipped.
   This sets the rigor: a shipped product gets the same elicitation but with
   "what is the current behavior?" framing instead of "what will it be?".
3. **What kind of AI?** LLM-powered, classical ML (recommendations,
   classification, ranking), computer vision, multi-modal, agentic
   (multi-step actions). This determines which Block 6 probes apply.

### Step 0.4 — Confirm the framing in one line

Before proceeding to block work, mirror back the framing so the builder can
correct you:

> *"Reviewing an LLM-powered email-draft feature, currently in development.
> Validation canvas exists — I'll skip business-model questions and pressure-test
> the UX execution. Stop me if I should reframe."*

Then proceed to Phase 1.

### Hard rules for Phase 0

- **Never start block work without resolving the path.** Files saved to the
  wrong folder are the most common skill failure mode.
- **Never re-elicit business-model questions when `validation-canvas` is
  present.** Read it instead. If the canvas is silent on a relevant fact,
  surface that as a gap *in the canvas*, not as a question for this skill.
- **Never invent answers to Phase 0 questions from scant context.** Ask. The
  three facts take 30 seconds to confirm and prevent every downstream block
  from drifting off-target.

---

## Phase 1: Block-by-Block Elicitation

**Goal:** Walk the seven blocks in order, eliciting design decisions per block.
For each block, the output is either a concrete answer (the design decision)
or an explicit gap marker (`[Gap — what hasn't been designed yet]`).

### Role setup

Run the interview in first-person voice with these roles active. If
`team-composer` is invoked separately, skip duplicates.

| Role | Lens |
|------|------|
| `@ux_researcher` | Lead interviewer. Asks block-by-block. Pushes for specificity. |
| `@ai_safety_specialist` | Trust calibration, output integrity, autonomy levels (blocks 3, 6). Flags responsible-AI gaps. |
| `@lead_behavioral_scientist` | Mental model and trust dynamics (blocks 2, 3). Flags assumptions about user cognition. |
| `@senior_product_designer` | Feedback affordances, error UI, recovery paths (blocks 4, 5). Flags UI patterns that won't survive contact with users. |
| `@senior_product_manager` | Success criteria and measurability (block 7). Flags "metrics" that are actually aspirations. |

### Block reasoning order (mandatory)

The order matters — earlier blocks set up the constraints later blocks
inherit. Do not jump around.

1. **Why AI here?** (necessity check — sets what counts as success)
2. **Mental model** (frames how trust must be calibrated)
3. **Trust calibration** (frames what feedback affordances must exist)
4. **Feedback & control** (frames what error states must do)
5. **Errors & graceful failure** (frames the catalog the rest of the
   review references)
6. **Output integrity** (gen-AI-specific surface — modernization layer)
7. **Success & evaluation** (closes the loop: does this design actually
   ship measurable signal?)

### Per-block protocol

For each block:

1. **State the block in one sentence** (definition) — from `references/blocks/<NN>-<name>.md`.
2. **Ask the block's primary probe** (one question, not five). Probes are
   in the reference file.
3. **Listen for specificity.** Category answers ("we handle errors", "users
   will trust it") fail the specificity gate. Push back.
4. **Walk the secondary probes** if the primary answer was thin. Two to
   four secondary probes per block, in the reference file.
5. **Apply acceptance criteria.** Each block has 2–4 criteria — measurable
   markers of "complete enough to ship." Note which are met, which are gaps.
6. **Mark gaps explicitly.** Anything the builder hasn't designed for goes
   in the block's output as `[Gap — <what's missing>]`. Gaps are data, not
   failure — they roll up into Phase 2's Gap Summary.

### What "enough" looks like

Each block has at least one specific, testable design decision OR an explicit
gap marker. "We have trust calibration" is not enough; "When confidence is
below 0.7, the chip color shifts to amber and we add 'verify before using'
text" is enough. "We haven't decided how to surface confidence yet" is also
enough — it's a gap, not a missing answer.

### What to do when the builder doesn't know

Mark the block `[Gap — <what hasn't been designed>: <why it matters>]`. A
review with honest gaps is more useful than a review with invented confidence.

### Pacing

The full seven-block walk takes 30–60 minutes depending on product
complexity. Single-block work (the user only wants to review one block) is
~10 minutes — but still invoke the skill, since the surrounding blocks
stress-test the one being reviewed.

---

## Phase 2: Cross-Block Stress Test

**Goal:** Surface contradictions, dependencies, and gaps that only show up
when the blocks are read together — the cross-block pressure test.

Apply these six checks. They are mandatory.

1. **Why AI ↔ Output integrity:** If Block 1 said "AI is necessary because
   X requires generative output," does Block 6 actually design for the
   integrity risks of generative output? Necessity claims that don't take
   on the cost of generation are red flags.

2. **Mental model ↔ Trust calibration:** Is the trust calibration in Block 3
   aligned with the mental model in Block 2? A system that surfaces
   confidence scores has implicitly committed users to a probabilistic
   mental model — does Block 2 actually say that?

3. **Trust calibration ↔ Feedback & control:** If Block 3 says users will
   sometimes need to verify, does Block 4 actually give them the
   affordances to verify? Cited sources without click-to-source is a flag.

4. **Errors ↔ Feedback & control:** Every failure mode in Block 5 should
   have a corresponding recovery affordance in Block 4. Failure modes
   without recovery paths are gaps.

5. **Output integrity ↔ Success & evaluation:** Block 6's mitigations
   (hallucination guards, citation requirements, agent autonomy limits)
   should show up as measurable signal in Block 7. A mitigation with no
   measurement plan is theater.

6. **All blocks ↔ Lifecycle stage:** A shipped product with `[Gap]` markers
   in Blocks 3, 5, or 6 is a different urgency than the same gaps in a
   prototype. Tag the urgency of each gap based on lifecycle.

### Output of Phase 2

Append a `## Gap Summary` section to `ai-ux-review.md` with the 3–5 most
urgent unmade design decisions. For each:

- The gap in plain language ("No defined behavior for output the user can't
  verify against ground truth")
- Why it matters ("Block 1 said the AI is necessary for generation; without
  this, users have no way to know when the system is wrong")
- The cheapest design experiment to resolve it ("Add a side panel that shows
  the sources used; A/B test against current; if engagement with side panel
  is <5%, redesign or remove the unverifiable surface")

Gap Summary is the most-read part of the review six months later. Do not
treat it as filler. It is also the direct hand-off if a future
`ai-eval-rubric` companion skill ships — that skill will grep this section
to seed its eval coverage.

---

## Phase 3: Render & Ship

**Goal:** Produce `ai-ux-review.md` and `ai-ux-review.html`, save them to the
resolved review folder, and present them to the user.

### Step 1 — Produce `ai-ux-review.md`

Structure (headings must match exactly):

```markdown
# AI UX Review — [Product / Feature Name]

> Generated on [YYYY-MM-DD]. Lifecycle: [idea | prototype | development | shipped]. AI type: [LLM | classical-ML | CV | multi-modal | agentic].

## Block 1 — Why AI Here?
- ...

## Block 2 — Mental Model
- ...

## Block 3 — Trust Calibration
- ...

## Block 4 — Feedback & Control
- ...

## Block 5 — Errors & Graceful Failure
- ...

## Block 6 — Output Integrity
- ...

## Block 7 — Success & Evaluation
- ...

---

## Gap Summary

1. **[Gap in one line]**
   - Why it matters: ...
   - Cheapest design experiment to resolve: ...
```

The heading anchors `## Block 1`...`## Block 7` and `## Gap Summary` are
load-bearing. If a future `ai-eval-rubric` companion ships, it will grep
these by name. Do not rename.

### Step 2 — Produce `ai-ux-review.html`

Read the template at `templates/ai-ux-review.html` and produce a single
self-contained HTML file that:

- Renders the seven blocks as cards in a 3+3+1 grid (Blocks 1–3 top row,
  4–6 middle row, 7 bottom full-width).
- Marks any block with unresolved gaps using a `[GAP]` chip in its header.
- Reads brand tokens from `<resolved-brand-root>/DESIGN.md` if it exists,
  extracting `colors.primary` from YAML front matter and binding to
  `--ai-ux-accent`. Otherwise uses neutral defaults.
- Includes a Gap Summary footer block listing the unresolved decisions.
- Prints cleanly to PDF via CSS paged media.
- Carries zero network dependencies. No localStorage, no external fonts,
  no remote images.

### Step 3 — Save to the resolved review folder

- `<review-root>/ai-ux-review.md`
- `<review-root>/ai-ux-review.html`

Create the folder if absent.

### Step 4 — Present to the user

Use `present_files` if available; otherwise emit clickable `computer://`
links. Present the HTML first (visual primary), Markdown second (source of
truth).

End with **three lines**:

1. *"The unresolved design decision with the highest urgency is: …"*
2. *"The cheapest design experiment to resolve it is: …"*
3. *"Next step: …"* — pick from: "speak to N users about the mental model
   gap," "prototype the recovery affordance and test with one user," "if
   the gap is Block 6 / Output integrity, escalate to `team-composer` with
   `@ai_safety_specialist`."

Every run ends this way. Do not replace with a "final deliverable" header
or meta-commentary.

---

## Update mode (loop-back)

When `ai-ux-review.md` already exists at the resolved review root:

1. **Read the existing file first.** Do not overwrite blocks the builder
   hasn't asked to change.
2. **Confirm scope.** *"Your last review had gaps in Block 3 (Trust) and
   Block 6 (Output integrity). Update those blocks, or re-run the full
   seven?"*
3. **Apply the same rigor on the changed blocks.** A glib revision gets
   the same push-back as a glib first answer.
4. **Mark changes visibly.** Updated blocks carry `<!-- updated YYYY-MM-DD:
   <reason> -->`.

This is the loop-back protocol — gaps closed over time are progress, not
failure.

---

## Output Files

```
<review-root>/ai-ux-review.md     Canonical, editable source of truth
<review-root>/ai-ux-review.html   Self-contained visual review (primary deliverable)
```

Where `<review-root>` resolves per Phase 0.1:

- `docs/startup-kit/ai-ux/` — orchestrated (smart default or env-var override)
- `docs/ai-ux/` — solo default
- `${STARTUP_KIT_DOCS_ROOT}/ai-ux/` — env-var override

No other files. Do not scatter intermediate drafts.

---

## Quality Checklist

Before presenting to the user, verify each:

**Phase 0 (Intake)**
- [ ] Review root resolved correctly
- [ ] Adjacent artifacts scanned (`validation-canvas.md`, `DESIGN.md`, attached spec)
- [ ] Three intake facts established (AI does what / lifecycle / AI type)
- [ ] Framing confirmed in one line

**Content (per block)**
- [ ] Every block has at least one specific testable design decision OR an explicit `[Gap — ...]` marker
- [ ] Specificity gate enforced — no "we handle errors" or "users will trust it" without elaboration
- [ ] Acceptance criteria checked per block (met vs. gap)
- [ ] Block 6 probes applied to the AI type (LLM-specific probes for LLM products, etc.)
- [ ] Block 7 distinguishes measurable signal from proxy from judgment-only

**Cross-block (Phase 2)**
- [ ] All six cross-block checks run
- [ ] Gap Summary has 3–5 gaps, each with why-it-matters and design experiment
- [ ] Gaps tagged by urgency for the lifecycle stage

**Rendering**
- [ ] `ai-ux-review.md` uses the exact heading structure (so downstream tools can parse)
- [ ] `ai-ux-review.html` is a single file, opens in a browser, prints cleanly to PDF
- [ ] HTML uses brand tokens if `<brand-root>/DESIGN.md` is present; neutral defaults otherwise
- [ ] No external network dependencies, no localStorage in the HTML

**Shipping**
- [ ] Both files saved to the resolved review folder
- [ ] Smart-default notice surfaced if it fired
- [ ] Files presented via `present_files` or `computer://` links
- [ ] Response ends with the three lines (top gap + design experiment + next step)

---

## Cross-Skill Integration

| Skill | When to Use |
|-------|-------------|
| `ai-eval-review` (our own) | **Sibling skill.** Same shape, different subject — `ai-ux-review` audits the human-AI design surface; `ai-eval-review` audits the measurement layer. Block 7 (Success & Evaluation) gaps from this review seed Block 1 of `ai-eval-review` when both are run. Block 6 boundary is explicit: this skill names *designed* mitigations (verifiability, provenance, prompt-injection mitigation, autonomy); `ai-eval-review` Block 6 names *measured* signal (resistance rates, OOD detection, jailbreak eval). Run both for a complete AI product review. |
| `validation-canvas` (our own) | Upstream when the product is idea-stage and the business model isn't settled. This skill reads `validation-canvas.md` if present and skips business-model questions. |
| `brand-workshop` (our own) | Upstream when a brand identity exists. This skill reads `<brand-root>/DESIGN.md` to style the HTML output. Extracts brand tokens from YAML front matter per [Google Labs spec](https://github.com/google-labs-code/design.md) (alpha). |
| `team-composer` (our own) | Alternative when the builder wants a *discussion* on one narrow block (e.g., "let's debate the trust-calibration approach") rather than a full review artifact. Use `team-composer` with `@ux_researcher` + `@ai_safety_specialist`. |
| `startup-grill` (our own) | Adjacent. After this skill ships, the builder may grill the resulting design adversarially before launch. Distinct deliverable (kill report with verdict) vs. this skill's gap summary. |
| `pitch-deck` (our own) | Downstream. If the review surfaces strong design decisions (block-by-block trust + integrity story), they can seed slides 3 and 6 of the deck. |
| `riskiest-assumption-test` (our own) | Composition. If the Gap Summary surfaces design assumptions that need *testing* (not just deciding), hand the gaps to RAT to convert into falsifiable hypotheses. |
| `theme-factory` (Anthropic) | When the HTML review needs branded styling and no `DESIGN.md` exists. Apply after content is finalized. |
| `web-artifacts-builder` (Anthropic) | For interactive review variants (filter by block, toggle gaps). Out of scope for v1; natural upgrade path. |
| `pdf` (Anthropic) | When merging the review into a larger packet. The HTML already prints cleanly to PDF; `pdf` is for programmatic assembly across artifacts. |
| `docx` (Anthropic) | When the review needs to ship as `.docx` (legal review, regulator submission, board packet). Hand `ai-ux-review.md` as source. |
| `ai-safety-mindset` (Anthropic) | When the team is missing shared vocabulary for responsible-AI framing — load this skill alongside for Anthropic's HHH framing rather than ad-hoc definitions. |

**Principle:** this skill owns the **design-completeness artifact** — whether
the human side of an AI product has been intentionally designed. It does not
validate beliefs (that's `validation-canvas`), test hypotheses (that's
`riskiest-assumption-test`), pitch the product (that's `pitch-deck`),
adversarially probe it (that's `startup-grill`), or implement evaluation
pipelines (out of scope; future companion).

**Graceful degradation:** if a referenced skill is not installed, this skill
still ships `ai-ux-review.md` + `ai-ux-review.html`. Cross-skill chains are
enhancements, not requirements.

---

## Reference files

- `references/blocks/01-why-ai.md` — necessity check; AI vs. deterministic alternative; falsifiable success
- `references/blocks/02-mental-model.md` — user's expected model; misalignment patterns; teaching affordances
- `references/blocks/03-trust-calibration.md` — confidence surfacing; under/over-trust risks; explanation depth
- `references/blocks/04-feedback-control.md` — correction affordances; override paths; autonomy spectrum
- `references/blocks/05-errors-graceful-failure.md` — failure-mode catalog; severity tiers; recovery paths
- `references/blocks/06-output-integrity.md` — hallucination guards; provenance; verifiability; prompt-injection surface; multi-turn drift; agent autonomy
- `references/blocks/07-success-evaluation.md` — production success criteria; measurable signal vs. proxy; eval gaps

Read these when the phase calls for them. Do not front-load all references
at once — that's the progressive disclosure pattern this repo uses (see
`CLAUDE.md` → "Harness vocabulary").

**Tags:** ai, ux, human-centered-ai, design-review, llm, responsible-ai
