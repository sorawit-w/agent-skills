---
name: startup-audit
description: >
  Post-build diligence readout of an ALREADY-BUILT product. Ingests an existing
  codebase (primary) and/or a live URL (secondary), infers the business model
  from what's actually built, contrasts it against the claimed story, and ships a
  single self-contained interactive HTML dossier. The mirror image of
  `startup-launch-kit`: that validates an idea before building; this audits a
  product after building.
  Use this skill when the user says: "audit my startup", "audit this codebase as
  a business", "review my built product", "technical due diligence on this repo",
  "what does my codebase say about my business", "diligence this product",
  "investor diligence on a built product", "does the code match the pitch", or
  points the skill at a repo / URL and asks what it reveals about the business.
  This skill is DILIGENCE, never "validation" — it reports evidence with
  confidence tiers (observed / inferred / unknown), and every claim carries a
  provenance pointer back to the file or signal that produced it.
  Do NOT use this skill for: pre-build idea validation (use `startup-launch-kit`
  / `validation-canvas` — there's no product to read yet); an adversarial verdict
  of Investable / Pivot / Pass (use `startup-grill` — this skill produces
  evidence, not a verdict); deep UI/UX review of an AI feature (use
  `ai-ux-review`); auditing a SKILL.md's rule adherence (use `skill-evaluator`).
  Hard boundary: `startup-launch-kit` is pre-build belief work; `startup-grill`
  is the adversarial verdict; `skill-evaluator` audits skill text; this skill
  reads a built product and asks "what business does this code imply, and does it
  match the claim?"
instructions: |
  Load this skill when the user wants to assess an EXISTING, already-built product
  from its codebase and/or live URL — a post-build diligence readout, not pre-build
  idea validation. Triggers: "audit my startup/product", "diligence this repo",
  "does the code match the pitch", "technical due diligence", pointing at a repo.
  Do NOT load when: the product doesn't exist yet (pre-build → `startup-launch-kit`);
  the user wants a verdict (`startup-grill`); UI/UX-only review (`ai-ux-review`);
  a SKILL.md audit (`skill-evaluator`).
tags:
  - startup
  - diligence
  - codebase-analysis
  - business-model
  - due-diligence
---

# Startup Audit

Read an already-built product and report the business it implies. Ingest the
codebase (and optionally a live URL), infer the business model **into a Lean
Canvas**, contrast coded reality against the claimed story, and ship a
self-contained interactive HTML dossier.

This skill is **diligence, not validation.** It does not decide whether the idea
is good (that's pre-build work) and does not pronounce a verdict (that's
`startup-grill`). It reports **what is built, what is claimed, and the gap** —
every claim tiered by confidence and pinned to a provenance pointer. Overclaiming
is the cardinal sin; the provenance contract is the guardrail.

---

## STOP — When NOT to use this skill

Hand off — do not run the audit — if any of these apply:

- **The product doesn't exist yet** (idea / pre-build) → use `startup-launch-kit`
  or `validation-canvas`. There is no codebase to read; this skill would have
  nothing to infer from.
- **The user wants a verdict** (Investable / Pivot / Pass) or adversarial
  pressure → use `startup-grill`. This skill produces *evidence*; grill produces
  the *verdict*. Feed this skill's dossier into grill.
- **The user wants deep UI/UX review** of an AI feature → use `ai-ux-review`
  (and `ai-eval-review` for the eval layer). This skill *delegates* the UI/UX
  layer to those skills rather than rebuilding it.
- **The user wants to audit a SKILL.md's rule adherence** → use `skill-evaluator`.
  Different "audit" — that one reads skill text, this one reads a product.

**Bright-line rule:** if there is no built artifact to read (no repo, no live
URL), this is not the skill. If the user wants a judgment call rather than
evidence, that's `startup-grill`.

**Redirect discipline.** When the STOP gate fires and you route to
`startup-grill` or `team-composer`, describe the *kind of lens* needed — don't
coin role tags. The canonical persona catalog is
`skills/team-composer/references/role-personas.md`; defer naming specific roles
to those skills.

---

## Skill Boundaries

| Request | Skill |
|---|---|
| "Audit my built product / repo as a business" | `startup-audit` (this skill) |
| "Does my code match my pitch?" | `startup-audit` |
| "Technical due diligence on this product" | `startup-audit` |
| "Validate my idea / build my lean canvas" | `validation-canvas` / `startup-launch-kit` |
| "Is this investable? Give me a verdict" | `startup-grill` |
| "Review my AI feature's UX" | `ai-ux-review` |
| "Audit my eval setup" | `ai-eval-review` |
| "Audit whether my SKILL.md rules land" | `skill-evaluator` |

If the request mixes auditing with verdict-seeking ("audit my product *and* tell
me if it's fundable"), run the audit first to ship the dossier, then route the
verdict to `startup-grill` with the dossier as input. Don't emit a verdict here —
that collapses the diligence/verdict boundary.

---

## What this skill produces

Every run produces files inside the resolved audit root (see Phase 0 for path
resolution; default `docs/audit/` for solo runs, `docs/startup-kit/audit/` when
invoked under the kit root):

1. **`startup-audit.html`** — the single self-contained interactive dossier
   (zero network deps; expandable provenance; confidence-tier filter;
   print-clean). Format + template: `references/dossier-html-template.md`.
2. **`startup-audit.md`** — canonical, editable Markdown mirror of the dossier
   content (the dossier HTML is rendered from this).
3. **`inferred-canvas.md`** — the inferred Lean Canvas using
   `validation-canvas`'s exact headings, every field carrying a provenance
   pointer + confidence tier.

**The handoff bridge (read carefully — this is where the chain actually
connects).** Downstream skills do **not** read `inferred-canvas.md`: `startup-grill`
and `pitch-deck` grep `<canvas-root>/validation-canvas.md`, and
`riskiest-assumption-test` reads its own `assumption-test-plan.md` — neither reads
this skill's audit-root files. So `inferred-canvas.md` is this skill's **evidence
artifact**, not an auto-consumed pipeline input. The bridge is the **offer-to-seed**
step (Phase 3): if no founder `validation-canvas.md` exists, this skill offers to
seed one from the inferred canvas — and *that seeded file* is what grill/pitch-deck
consume. For `riskiest-assumption-test`, the handoff is a **pointer**, not a file:
the dossier's handoff section recommends running RAT on the `unknown` blocks. State
this honestly in the dossier — do not imply an automatic feed that isn't wired.

Existing files from prior sessions are appended-to / re-rendered, never silently
overwritten. **Never overwrite a founder-authored `validation-canvas.md`** — see
Phase 3.

---

## Phase 0: Path resolution + dependency pre-flight

**Resolve the audit root** once, in this precedence order:

1. **Explicit `output_dir` arg** → use as-is.
2. **`STARTUP_KIT_DOCS_ROOT` env var set** → `${STARTUP_KIT_DOCS_ROOT}/audit/`.
3. **`docs/startup-kit/` exists** → `docs/startup-kit/audit/` (surface the
   smart-default notice: *"Writing to `docs/startup-kit/audit/`. Set
   `STARTUP_KIT_DOCS_ROOT=./docs` to write standalone instead."*).
4. **Solo fallback** → `docs/audit/`.

Sibling reads (`<canvas-root>/`, `<rat-root>/`) resolve as siblings of the audit
root, matching `startup-grill`'s chain.

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
3. **Build-vs-claim diff (the headline).** Contrast the inferred (coded) model
   against the *claimed* story (README / marketing copy / URL). Run it
   **bidirectionally**: claimed-but-not-built AND built-but-not-claimed. Parse
   README roadmap markers ("Future", "Coming soon", "Roadmap") — a feature the
   tagline sells but the roadmap marks "Future" is a diff finding.

**Write `inferred-canvas.md`** to the audit root. The blocks code evidences
poorly — typically `Problem`, `Unique Value Proposition`, `Unfair Advantage` —
render as `unknown` and become the **`riskiest-assumption-test` handoff** (these
are exactly the beliefs a built artifact can't prove).

**Thin / greenfield repos are a valid result, not a failure.** A sparse repo
(prototype, few deps, no schema) legitimately yields a mostly-`unknown` canvas.
Still run the audit — report the unknowns honestly and route them to
`riskiest-assumption-test`. Do NOT pad the canvas with market reasoning to make it
look complete; that trips the provenance gate. Yield scales with repo maturity.

**Never overwrite a founder-authored `validation-canvas.md`.** Write to the
separate `inferred-canvas.md`. If no `validation-canvas.md` exists at the
canvas root, **offer to seed one** from the inferred canvas (the founder can then
correct the machine's inference) — but only on explicit confirmation.

---

## Phase 3: Audit panel (Stage 2 — per-lens findings pass)

**Goal:** apply domain-aware lenses to the inferred canvas + diff. This is a
**single-pass per-lens findings pass, NOT a multi-round debate.** The adversarial
opening/rebuttal/synthesis panel is `startup-grill`'s job — do not rebuild it
here. (Feed, don't compete.)

Apply `references/audit-panel-resolution.md`:

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
   canvas field / diff row / signal it rests on.
4. **AI features detected** → add the AI-safety lens AND route to the conditional
   skills `ai-ux-review` (human-AI design + integrity surface) and
   `ai-eval-review` (eval rigor). If they run, embed/link their
   `docs/ai-ux/*.html` outputs into the dossier rather than re-assessing AI
   quality here.
5. **Advice tier — "Options the evidence suggests."** Generate grounded options
   (including pivot directions). **Hard gate: every option must cite the finding
   that motivates it — no citation, the option is suppressed.** Do **not** emit an
   Investable / Pivot / Pass verdict; that is delegated to `startup-grill` via the
   dossier handoff.

---

## Phase 4: Render the dossier

Apply `references/dossier-html-template.md`. Write the canonical
`startup-audit.md`, then render `startup-audit.html` from it.

Dossier sections, in order:

1. **Executive summary** — what this product is, in evidence terms.
2. **Build-vs-claim diff** — two columns (coded reality vs claimed story); the
   headline finding sits at the top.
3. **Inferred Lean Canvas** — nine blocks, each color-coded by confidence tier,
   each field with an expandable provenance pointer.
4. **Audit findings** — per-lens findings blocks.
5. **Options the evidence suggests** — each option linked to its source finding.
6. **Handoff & next steps** — where to take the `inferred-canvas.md` next
   (`riskiest-assumption-test` for the unknown blocks; `startup-grill` for the
   verdict), and which optional skills ran (`ai-ux-review` / `ai-eval-review`).

The HTML is **self-contained** (inline CSS + vanilla JS, zero network deps,
base64 any images, `@media print` clean) with interactivity: expandable
provenance per field, confidence-tier filter, collapsible blocks. Brand tokens
injected from `DESIGN.md` if present.

Run the verifier checklist before presenting:

- [ ] Every rendered canvas field has a provenance pointer (or renders as `unknown`)
- [ ] `inferred-canvas.md` headings match `validation-canvas`'s spec byte-for-byte
- [ ] Build-vs-claim diff ran bidirectionally
- [ ] Every "Options" entry cites a finding (uncited options suppressed)
- [ ] No Investable / Pivot / Pass verdict emitted (delegated to `startup-grill`)
- [ ] No secret values written anywhere in the artifacts
- [ ] HTML opens offline (no network requests) and prints clean
- [ ] The lane that ran (SocratiCode vs glob/grep; URL fetched vs skipped) is stated

If any box fails, fix before presenting. Then present the files.

---

## Quality bars (skill-wide)

The skill must refuse to ship if any of these are true:

- **A canvas field claims something with no provenance pointer** — provenance or
  unknown, never a bare assertion.
- **An "Options" recommendation cites no finding** — that's blind advice; suppress it.
- **An Investable / Pivot / Pass verdict appears** — that's `startup-grill`'s job.
- **A secret value (not just a key name) appears** in any artifact.
- **The word "validation"** is used to describe this skill's output as if demand
  were proven — it reads a build, it does not prove a market.
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

- `startup-grill` — downstream verdict; the dossier feeds it.
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
| `validation-canvas` | Phase 2 infers into its exact Lean Canvas headings. This skill writes a separate `inferred-canvas.md` and offers to seed `validation-canvas.md` if none exists — never overwrites a founder's. **The seeded `validation-canvas.md` is the bridge** that makes the inferred model consumable downstream; without it, `inferred-canvas.md` stays a standalone evidence artifact. The founder then corrects the inference in `validation-canvas`. |
| `riskiest-assumption-test` | **Pointer handoff, not a file handoff.** RAT reads its own `assumption-test-plan.md` (which this skill does not write). The dossier *recommends* running RAT on the `unknown` blocks (Problem / UVP / Unfair Advantage) — the beliefs a built artifact can't prove. |
| `startup-grill` | Downstream verdict. Grill greps `<canvas-root>/validation-canvas.md` — so it consumes this skill's work **only once the inferred canvas is seeded there** (or the user points grill at `inferred-canvas.md` directly). This skill produces evidence; grill produces the Investable / Pivot / Pass verdict. |
| `pitch-deck` | Consumes the seeded `validation-canvas.md` / build-vs-claim diff when the founder builds or re-cuts a deck grounded in coded reality (same seed-bridge as grill). |
| `team-composer` | Phase 3 reads its `references/role-personas.md` persona catalog for the audit lenses (read, not invoked). Use team-composer directly for collaborative, constructive multi-role review (this skill is one-pass diligence). |
| `ai-ux-review` / `ai-eval-review` | Conditional — invoked when AI features are detected. This skill delegates AI UX + eval assessment to them and embeds their HTML rather than rebuilding it. |
| `skill-evaluator` | To audit this skill's own rules end-to-end (the provenance gate, the no-verdict rule, the diff-bidirectionality rule). |

**Principle:** this skill owns *post-build diligence* — reading a built product
and reporting the business it implies, with provenance-tiered confidence. It does
not validate ideas, does not pronounce verdicts, does not rebuild UI/UX review.
It is the upstream evidence producer that feeds the rest of the chain.

**Graceful degradation:** with SocratiCode absent it falls back to glob/grep;
with no URL it runs codebase-only; with a thin / greenfield repo it honestly
reports mostly `unknown` and routes to `validation-canvas` + `riskiest-assumption-test`
(yield scales with repo maturity — a thin repo can't support inference, and the
confidence tiers say so rather than hallucinating).
