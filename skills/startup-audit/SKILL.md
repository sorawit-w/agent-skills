---
name: startup-audit
description: >
  Fast, code-grounded triage of an ALREADY-BUILT product. Ingests an existing
  codebase (primary) and/or a live URL (secondary), infers the business model from
  what's actually built, diffs it against the claimed story, and ships a single
  self-contained interactive HTML dossier that opens with an opinionated
  Continue / Pivot / Kill verdict and a Red/Amber/Green band.
  The verdict is a FAST first read — for a consequential call (especially Kill or
  Pivot) the dossier points you to `startup-grill` for the deep adversarial
  confirmation.
  Use this skill when the user says: "audit my startup", "grill my built product",
  "grill my startup from the code / the repo / the URL", "should I continue, pivot,
  or kill this", "score my startup from the codebase", "is my product worth
  continuing", "technical due diligence on this repo", "does the code match the
  pitch", or points the skill at a repo / URL and asks whether to keep going.
  Every claim is tiered by confidence (observed / inferred / unknown) and pinned to
  a provenance pointer; every verdict is explicitly OPINION, not investment, legal,
  or financial advice. A pure-diligence dossier (no verdict) is available on request.
  Do NOT use this skill for: pre-build idea validation (use `startup-launch-kit` /
  `validation-canvas` — there's no product to read yet); a DEEP ADVERSARIAL verdict
  on belief artifacts (a Lean Canvas or pitch deck), or to CONFIRM a consequential
  Kill/Pivot (use `startup-grill` — its 3-round probe is the heavier verdict); deep
  UI/UX review of an AI feature (use `ai-ux-review`); auditing a SKILL.md's rule
  adherence (use `skill-evaluator`).
  Boundary by INPUT and RIGOR: this skill reads a BUILT artifact (codebase/URL) and
  gives a FAST triage verdict; `startup-grill` reads BELIEF artifacts (canvas/deck)
  and gives a DEEP adversarial verdict. `startup-launch-kit` is pre-build; this is
  post-build. The INPUT decides, not the verb: if the user points at a codebase or
  URL and asks for a verdict, a score, or "should I continue / pivot / kill" — that
  is THIS skill, EVEN IF they say "grill" or "kill". Those words alone do NOT route
  to `startup-grill`; `startup-grill` only applies when the input is a belief
  artifact (canvas / deck / one-pager), not a codebase.
instructions: |
  Load this skill when the user wants a fast, code-grounded read on an EXISTING,
  already-built product — pointing at a codebase and/or live URL and asking what
  it's worth or whether to continue, pivot, or kill. Triggers: "grill my startup
  from the code", "should I continue/pivot/kill", "score my product from the repo/
  URL", "audit my built product", "does the code match the pitch".
  Do NOT load when: the product doesn't exist yet (pre-build → `startup-launch-kit`);
  the user wants a DEEP adversarial verdict on a canvas/deck or to confirm a
  Kill/Pivot (`startup-grill`); UI/UX-only review (`ai-ux-review`); a SKILL.md
  audit (`skill-evaluator`).
tags:
  - startup
  - diligence
  - codebase-analysis
  - business-model
  - verdict
  - triage
---

# Startup Audit

Read an already-built product and give a fast, code-grounded **Continue / Pivot /
Kill** triage call. Ingest the codebase (and optionally a live URL), infer the
business model **into a Lean Canvas**, diff coded reality against the claimed
story, and ship a self-contained interactive HTML dossier that opens with the
verdict.

This skill is a **fast triage, not a deep adversarial verdict.** Its Stage 2 is a
single-pass per-lens findings sweep — no rebuttal round — so the verdict is an
honest *first read*, not a grilled one. For a consequential call (especially **Kill
or Pivot**), the dossier points to `startup-grill` for the adversarial
confirmation. Every claim is tiered by confidence and pinned to a provenance
pointer; overclaiming is the cardinal sin. **The verdict is opinion, not advice** —
the disclaimer ships with every run.

A pure-diligence dossier (evidence only, **no verdict**) is available on request —
see Phase 0 mode detection.

---

## STOP — When NOT to use this skill

Hand off — do not run the audit — if any of these apply:

- **The product doesn't exist yet** (idea / pre-build) → use `startup-launch-kit`
  or `validation-canvas`. There is no codebase to read; this skill would have
  nothing to infer from.
- **The user wants a DEEP adversarial verdict** on belief artifacts (a Lean Canvas
  or pitch deck), or wants to **confirm a consequential Kill/Pivot** this skill
  flagged → use `startup-grill`. This skill gives the *fast code-grounded triage*;
  grill gives the heavier *3-round adversarial verdict* on text artifacts. They are
  siblings split by **input** (built code/URL vs belief artifacts) and **rigor**
  (triage vs adversarial).
- **The user wants deep UI/UX review** of an AI feature → use `ai-ux-review`
  (and `ai-eval-review` for the eval layer). This skill *delegates* the UI/UX
  layer to those skills rather than rebuilding it.
- **The user wants to audit a SKILL.md's rule adherence** → use `skill-evaluator`.
  Different "audit" — that one reads skill text, this one reads a product.

**Bright-line rule:** if there is no built artifact to read (no repo, no live URL),
this is not the skill — pre-build work routes to `startup-launch-kit`. If the user
wants the *deep adversarial* verdict on a canvas/deck, that's `startup-grill`.

**Redirect discipline.** When the STOP gate fires and you route to
`startup-grill` or `team-composer`, describe the *kind of lens* needed — don't
coin role tags. The canonical persona catalog is
`skills/team-composer/references/role-personas.md`; defer naming specific roles
to those skills.

---

## Skill Boundaries

| Request | Skill |
|---|---|
| "Grill my startup from the codebase / repo / URL" | `startup-audit` (this skill) |
| "Should I continue, pivot, or kill — from the code?" | `startup-audit` |
| "Score my built product / does my code match my pitch?" | `startup-audit` |
| "Grill my pitch deck / Lean Canvas (deep adversarial)" | `startup-grill` |
| "Confirm the Kill/Pivot this audit flagged" | `startup-grill` |
| "Validate my idea / build my lean canvas (pre-build)" | `validation-canvas` / `startup-launch-kit` |
| "Review my AI feature's UX" | `ai-ux-review` |
| "Audit my eval setup" | `ai-eval-review` |
| "Audit whether my SKILL.md rules land" | `skill-evaluator` |

The split with `startup-grill` is **input + rigor**, not evidence-vs-verdict:
this skill reads a **built artifact** and gives a **fast triage** verdict; grill
reads **belief artifacts** and gives a **deep adversarial** verdict. When this
skill returns a Kill or Pivot, it recommends grill for the heavier confirmation —
that's a handoff, not a boundary the user has to manage.

---

## What this skill produces

Every run produces files inside the resolved audit root (see Phase 0 for path
resolution; default `docs/audit/` for solo runs, `docs/startup-kit/audit/` when
invoked under the kit root):

1. **`startup-audit.html`** — the single self-contained interactive dossier. In
   **default (verdict) mode** it opens with the **Continue / Pivot / Kill** verdict
   + Red/Amber/Green band + the disclaimer, then the evidence. In **diligence-only
   mode** the verdict section is omitted (evidence only). Format + template:
   `references/dossier-html-template.md`.
2. **`startup-audit.md`** — canonical, editable Markdown mirror of the dossier.
3. **`inferred-canvas.md`** — the inferred Lean Canvas using `validation-canvas`'s
   exact headings, every field carrying a provenance pointer + confidence tier.

**The handoff bridge (read carefully — this is where the chain connects).**
Downstream skills do **not** read `inferred-canvas.md`: `startup-grill` and
`pitch-deck` grep `<canvas-root>/validation-canvas.md`, and
`riskiest-assumption-test` reads its own `assumption-test-plan.md`. So
`inferred-canvas.md` is this skill's **evidence artifact**, not an auto-consumed
pipeline input. The bridge is the **offer-to-seed** step (Phase 2): if no founder
`validation-canvas.md` exists, this skill offers to seed one — and *that seeded
file* is what grill consumes when the user takes a Kill/Pivot for confirmation. For
`riskiest-assumption-test`, the handoff is a **pointer**: the dossier recommends
running RAT on the `unknown` blocks. State this honestly — do not imply an
automatic feed that isn't wired.

Existing files from prior sessions are appended-to / re-rendered, never silently
overwritten. **Never overwrite a founder-authored `validation-canvas.md`** — see
Phase 2.

---

## Phase 0: Path resolution + mode + dependency pre-flight

**Resolve the audit root** once, in this precedence order:

1. **Explicit `output_dir` arg** → use as-is.
2. **`STARTUP_KIT_DOCS_ROOT` env var set** → `${STARTUP_KIT_DOCS_ROOT}/audit/`.
3. **`docs/startup-kit/` exists** → `docs/startup-kit/audit/` (surface the
   smart-default notice: *"Writing to `docs/startup-kit/audit/`. Set
   `STARTUP_KIT_DOCS_ROOT=./docs` to write standalone instead."*).
4. **Solo fallback** → `docs/audit/`.

Sibling reads (`<canvas-root>/`, `<rat-root>/`) resolve as siblings of the audit
root, matching `startup-grill`'s chain.

**Mode detection.** Default mode emits the verdict. Switch to **diligence-only
mode** (evidence dossier, no verdict / no score / no disclaimer-as-opinion) when
the user asks for it — phrases like "diligence only", "evidence only", "no
verdict", "just the dossier / no opinion", or an explicit `mode=diligence` arg.
Record which mode ran; the dossier states it.

**Dependency pre-flight (fail loud).** Before doing any work, check that the
**required** sibling skills are present (see Dependencies). If a required
reference is missing, **refuse with a clear message** — do not silently degrade:

> *"`startup-audit` requires `team-composer`, `validation-canvas`, and
> `riskiest-assumption-test` to be installed (it reads their reference files and
> writes artifacts they consume). One or more is missing — install the full
> agent-skills plugin, not just this skill."*

**Capability gate (degrade with notice).** Detect optional runtime capabilities
and pick the lane; record which lane ran so the dossier can state it:

- **SocratiCode MCP** present (`mcp__socraticode__codebase_*`) → use it for the
  semantic map. Absent → glob/grep fallback over high-signal files.
- **WebFetch / Playwright** present AND user supplied a URL AND URL fetch is
  explicitly opted-in → fetch the live surface. Absent / not opted-in →
  codebase-only; note the URL was skipped. **If a fetch is attempted but fails**
  (timeout, auth wall, error) → fall back to codebase-only, record the failure in
  the lane note, and continue — a failed URL fetch never blocks the audit.

---

## Phase 1: Signal extraction (Stage 1a)

**Goal:** sweep the codebase for deterministic business signal. This is a
structured extraction, not a judgment call — precision lives here.

Apply `references/signal-extraction.md` end-to-end. Detect the ecosystem
(JS/TS, Python, or generic fallback) and run the matching extractors over the
universal source taxonomy:

**dependency manifests · data model / schema · routes / pages · auth & tenancy ·
`.env(.example)` · money code · README / docs claims (+ roadmap markers) · commit
recency / contributor count.**

**Secret-redaction rule (hard).** Extract key *names / presence* only — never
values. A `STRIPE_SECRET_KEY` entry in `.env.example` is signal that Stripe is
wired; its value (if ever present) must never be read into any artifact. If a
real secret is encountered, record only "<redacted secret present>" and move on.

Output of this phase is a structured **signal set** (internal), each signal
tagged with its source file/path — that tag becomes the provenance pointer in
Phase 2.

---

## Phase 2: Inference (Stage 1b) → inferred canvas + build-vs-claim diff

**Goal:** turn signals into an inferred business model, tiered by confidence,
and surface the gap against the claimed story.

Apply `references/inference-mapping.md`:

1. **Infer into the nine Lean Canvas blocks** using `validation-canvas`'s **exact**
   headings: `### Problem`, `### Customer Segments`, `### Unique Value Proposition`,
   `### Solution`, `### Channels`, `### Revenue Streams`, `### Cost Structure`,
   `### Key Metrics`, `### Unfair Advantage`. (These headings are grepped by
   `startup-grill` and `riskiest-assumption-test` — match byte-for-byte.)
2. **Derive the confidence tier from provenance — do not judge it:**
   - **observed** — a deterministic signal is directly present (e.g. an
     `invoice.paid` webhook handler + a populated plan table).
   - **inferred** — reasoned from a pattern (e.g. a Stripe dep + a `Subscription`
     entity → probably recurring SaaS).
   - **unknown** — no signal. The block renders empty.
   - **Hard gate: `provenance == null` → the field cannot render as a claim.**
     No provenance pointer, no claim. Unknowns stay unknown; they are not filled
     by reasoning about the market.
3. **Build-vs-claim diff (the headline evidence).** Contrast the inferred (coded)
   model against the *claimed* story (README / marketing copy / URL). Run it
   **bidirectionally**: claimed-but-not-built AND built-but-not-claimed. Parse
   README roadmap markers ("Future", "Coming soon", "Roadmap") — a feature the
   tagline sells but the roadmap marks "Future" is a diff finding.

**Write `inferred-canvas.md`** to the audit root. The blocks code evidences
poorly — typically `Problem`, `Unique Value Proposition`, `Unfair Advantage` —
render as `unknown` and become the **`riskiest-assumption-test` handoff** (these
are exactly the beliefs a built artifact can't prove).

**Thin / greenfield repos are a valid result, not a failure.** A sparse repo
(prototype, few deps, no schema) legitimately yields a mostly-`unknown` canvas.
Still run the audit — report the unknowns honestly, **downgrade the verdict's
confidence accordingly** (see Phase 3), and route the unknowns to
`riskiest-assumption-test`. Do NOT pad the canvas with market reasoning to make it
look complete; that trips the provenance gate. Yield scales with repo maturity.

**Never overwrite a founder-authored `validation-canvas.md`.** Write to the
separate `inferred-canvas.md`. If no `validation-canvas.md` exists at the
canvas root, **offer to seed one** from the inferred canvas (the founder can then
correct the machine's inference) — but only on explicit confirmation.

---

## Phase 3: Audit panel + verdict synthesis (Stage 2)

**Goal:** apply domain-aware lenses to the inferred canvas + diff, then synthesize
a **fast triage verdict**. This is a **single-pass per-lens findings pass, NOT a
multi-round debate.** The adversarial opening/rebuttal/synthesis panel is
`startup-grill`'s job — do not rebuild it here. The verdict here is an honest
*first read* derived from that single pass; consequential calls route to grill for
confirmation.

Apply `references/audit-panel-resolution.md`, then `references/verdict-and-scoring.md`:

1. **Pre-fill team-composer Phase 1 signals from the inference** (not from a
   brief): tenancy model → `audience`; compliance configs / regulated entities →
   `is_regulated`; ML/LLM deps → `is_data_intensive` + AI-feature flag; i18n /
   locale dirs → `is_international`; voting / nudge / gamification code →
   `involves_behavior_design`; commit history / maturity → `stage`.
2. **Resolve the lens panel** using the selection algorithm in
   `audit-panel-resolution.md`, which **reads personas from
   `skills/team-composer/references/role-personas.md`** (capability-gated; generic
   lens fallback if absent). Do **not** invoke `team-composer` as a sub-skill —
   read its catalog, mirror `startup-grill`'s read-then-select pattern.
3. **Each composed lens emits exactly one findings block** against the inferred
   canvas + diff — focused, evidence-anchored, no debate. Every finding cites the
   canvas field / diff row / signal it rests on, and is tagged with a
   `finding-id` (F1, F2, …) and a severity×fixability per `verdict-and-scoring.md`.
4. **AI features detected** → add the AI-safety lens AND route to the conditional
   skills `ai-ux-review` (human-AI design + integrity surface) and
   `ai-eval-review` (eval rigor). If they run, embed/link their
   `docs/ai-ux/*.html` outputs into the dossier rather than re-assessing AI
   quality here.
5. **Options the evidence suggests.** Generate grounded options (including pivot
   directions). **Hard gate: every option must cite the finding that motivates it
   — no citation, the option is suppressed.** When the verdict is Pivot, these
   options ARE the code-grounded pivot directions.
6. **Verdict synthesis (default mode only; skipped in diligence-only mode).**
   Per `references/verdict-and-scoring.md`, derive from the tagged findings:
   - a **headline verdict — Continue / Continue-with-conditions / Pivot / Kill**
     (the headline carries the recommendation; never let the band stand in for it);
   - a **Red / Amber / Green** heat band (coarse, layered under the headline);
   - an **evidence-confidence** label — a Kill/Red resting on majority-`unknown`
     signals **downgrades its own confidence and says so**;
   - a **headline reason** that **cites specific `finding-id`s** (no verdict
     without a finding pointer);
   - for **Kill or Pivot**, the explicit handoff: *"This is a fast code-grounded
     read — run `startup-grill` for the deep adversarial confirmation."*
   The verdict is **opinion** — render the disclaimer block from
   `verdict-and-scoring.md` with it, and never use a banned term
   ("valuation" / "guarantee" / "will succeed/fail").

---

## Phase 4: Render the dossier

Apply `references/dossier-html-template.md`. Write the canonical
`startup-audit.md`, then render `startup-audit.html` from it.

Dossier sections, in order:

1. **Verdict** *(default mode only — omitted in diligence-only mode)* —
   Continue/Pivot/Kill headline + R/A/G band + evidence-confidence + headline
   reason citing findings + (for Kill/Pivot) the grill-confirm handoff + the
   **disclaimer block**.
2. **Executive summary** — what this product is, in evidence terms.
3. **Build-vs-claim diff** — two columns (coded reality vs claimed story); the
   headline finding sits at the top.
4. **Inferred Lean Canvas** — nine blocks, each color-coded by confidence tier,
   each field with an expandable provenance pointer.
5. **Audit findings** — per-lens findings blocks (with finding-ids + severity).
6. **Options the evidence suggests** — each option linked to its source finding.
7. **Handoff & next steps** — `startup-grill` to confirm a Kill/Pivot;
   `riskiest-assumption-test` for the `unknown` blocks; which optional skills ran.

The HTML is **self-contained** (inline CSS + vanilla JS, zero network deps,
base64 any images, `@media print` clean) with interactivity: expandable
provenance per field, confidence-tier filter, collapsible blocks. Brand tokens
injected from `DESIGN.md` if present.

Run the verifier checklist before presenting:

- [ ] Every rendered canvas field has a provenance pointer (or renders as `unknown`)
- [ ] `inferred-canvas.md` headings match `validation-canvas`'s spec byte-for-byte
- [ ] Build-vs-claim diff ran bidirectionally
- [ ] Every "Options" entry cites a finding (uncited options suppressed)
- [ ] **Default mode:** verdict is one of Continue / Continue-with-conditions /
      Pivot / Kill, cites ≥1 finding-id, carries an R/A/G band + evidence-confidence,
      and ships the disclaimer; Kill/Pivot includes the grill-confirm handoff
- [ ] **Default mode:** a Kill/Red on majority-`unknown` evidence self-flags low confidence
- [ ] No banned term ("valuation" / "guarantee" / "will succeed/fail") appears
- [ ] **Diligence-only mode:** no verdict / band / score rendered
- [ ] No secret values written anywhere in the artifacts
- [ ] HTML opens offline (no network requests) and prints clean
- [ ] The lane + mode that ran is stated

If any box fails, fix before presenting. Then present the files.

---

## Quality bars (skill-wide)

The skill must refuse to ship if any of these are true:

- **A canvas field claims something with no provenance pointer** — provenance or
  unknown, never a bare assertion.
- **An "Options" recommendation cites no finding** — that's blind advice; suppress it.
- **(Default mode) a verdict appears with no `finding-id` citation** — a verdict
  without support is rhetoric; cite the findings that drive it.
- **(Default mode) the R/A/G band is presented AS the recommendation** instead of
  the Continue/Pivot/Kill headline — the headline carries the call; the band is
  coarse heat only.
- **(Default mode) a Kill/Red on majority-`unknown` evidence that does NOT
  self-flag low confidence** — the verdict must inherit the evidence quality.
- **(Default mode) the disclaimer block is missing, or a banned term appears**
  ("valuation" / "guarantee" / "will succeed/fail") — the verdict is opinion, and
  must say so.
- **A secret value (not just a key name) appears** in any artifact.
- **The build-vs-claim diff ran only one direction** — under-marketed built
  capability is as much a finding as over-claimed unbuilt capability.

---

## Dependencies

Declared explicitly (unlike most repo skills, which discover deps implicitly) so
a per-skill install fails loud rather than mysteriously.

**Required skills (fail loud if absent — see Phase 0 pre-flight):**

- `team-composer` — Phase 3 reads `references/role-personas.md` for lens personas.
- `validation-canvas` — Phase 2 infers into its exact Lean Canvas headings; the
  inferred canvas is consumable only because it mirrors this skill's spec.
- `riskiest-assumption-test` — the unknown-block handoff target.

**Conditional skills (invoked on signal; skip + note if absent):**

- `startup-grill` — recommended for the deep adversarial confirmation of a Kill/
  Pivot. The verdict vocabulary in `references/verdict-and-scoring.md` is aligned
  to grill's `kill-report.md` labels but is **self-contained** (no runtime read),
  so grill's absence never blocks this skill's verdict.
- `ai-ux-review` + `ai-eval-review` — invoked only when AI features are detected.

**Runtime capabilities (capability-gate WITH fallback; absence is normal):**

- SocratiCode MCP → glob/grep fallback.
- WebFetch / Playwright → codebase-only (drop URL input).

> **Install note:** install the full agent-skills plugin, not just this skill.
> A per-skill `npx` install copies only this folder and breaks the cross-skill
> reference reads above.

---

## Cross-Skill Integration

| Skill | When to use |
|---|---|
| `startup-grill` | **Sibling verdict skill, split by input + rigor.** This skill gives a fast code/URL-grounded triage verdict; grill gives the deep 3-round adversarial verdict on belief artifacts. When this skill returns **Kill or Pivot**, it recommends grill to confirm. The verdict vocabulary is aligned (`verdict-and-scoring.md` maps grill's labels → Continue/Pivot/Kill) but not forked. |
| `validation-canvas` | Phase 2 infers into its exact Lean Canvas headings. This skill writes a separate `inferred-canvas.md` and offers to seed `validation-canvas.md` if none exists — never overwrites a founder's. **The seeded `validation-canvas.md` is the bridge** that lets grill confirm a Kill/Pivot. The founder then corrects the inference in `validation-canvas`. |
| `riskiest-assumption-test` | **Pointer handoff.** RAT reads its own `assumption-test-plan.md` (which this skill does not write). The dossier *recommends* running RAT on the `unknown` blocks (Problem / UVP / Unfair Advantage) — the beliefs a built artifact can't prove. |
| `pitch-deck` | Consumes the seeded `validation-canvas.md` / build-vs-claim diff when the founder re-cuts a deck grounded in coded reality. |
| `team-composer` | Phase 3 reads its `references/role-personas.md` persona catalog for the audit lenses (read, not invoked). Use team-composer directly for collaborative, constructive multi-role review (this skill is one-pass triage). |
| `ai-ux-review` / `ai-eval-review` | Conditional — invoked when AI features are detected. This skill delegates AI UX + eval assessment to them and embeds their HTML rather than rebuilding it. |
| `skill-evaluator` | To audit this skill's own rules end-to-end (the provenance gate, the verdict-cites-a-finding rule, the diff-bidirectionality rule, the diligence-only flag). |

**Principle:** this skill owns the **fast, code-grounded triage verdict** — read a
built product (codebase/URL) and call it Continue / Pivot / Kill, with every claim
provenance-tiered and the verdict framed as opinion. It is the light front-of-line
read; `startup-grill` is the heavy adversarial confirmation.

**Graceful degradation:** with SocratiCode absent it falls back to glob/grep;
with no URL it runs codebase-only; with a thin / greenfield repo it honestly
reports mostly `unknown`, downgrades the verdict's confidence, and routes to
`validation-canvas` + `riskiest-assumption-test` (yield scales with repo maturity —
a thin repo can't support a confident verdict, and the band says so rather than
faking certainty).
