# Audit Panel Resolution

How to resolve which lenses examine the inferred canvas + build-vs-claim diff.
This is **Stage 2 — a single-pass per-lens findings pass, NOT a multi-round
debate.** The adversarial opening/rebuttal/synthesis panel is `startup-grill`'s
job; do not rebuild it here. (Feed, don't compete.)

We **read** `team-composer`'s persona catalog
(`skills/team-composer/references/role-personas.md`) for the lens voices and run
an OWN selection algorithm — mirroring `startup-grill`'s read-then-select
pattern. We do **not** invoke `team-composer` as a sub-skill. If
`role-personas.md` is unavailable (capability-gate miss), fall back to generic
lens descriptions and note it in the dossier.

---

## Phase A — Signals are pre-filled from the inference (not from a brief)

Unlike `team-composer` (which detects signals from a user brief) and
`startup-grill` (from a one-pager), this skill **derives the signals from the
Stage 1 inference**. Map once:

| Inferred from code | → team-composer Phase 1 signal |
|---|---|
| Tenancy model (`users` only / `org`+`team`+`seat` / public API) | `audience` (b2c / b2b / developer) |
| Compliance configs, regulated entities (`Patient`, `Claim`, payment, PII) | `is_regulated` |
| ML/LLM deps (`OPENROUTER_*`, `OPENAI_*`, model-call code, `aiUsageLogs`) | `is_data_intensive` + **AI-feature flag** |
| i18n libs / locale dirs / `*_REGION` keys | `is_international` |
| Voting / ranking / gamification / nudge code | `involves_behavior_design` |
| Statistical / algorithmic correctness claims (in code + README) | `has_statistical_claim` |
| Commit history / contributor count / maturity | `stage` |

**Ambiguity rule:** if a signal is genuinely ambiguous, default to the more
risk-bearing interpretation (assume `is_regulated=true` if unsure) — err toward
including the risk-blocking lens. (`Revenue model` specifics are canvas content,
not a panel signal — they don't appear here.)

---

## Phase B — The fixed core (3 lenses, always)

A diligence readout is leaner than a grilling panel. These three cover the
universal axes of a build audit and are non-droppable:

| # | Lens | Audit focus |
|---|------|-------------|
| 1 | `@senior_software_architect` | Execution reality — what's actually built, architecture health, scale/debt, build-vs-claim from the technical side |
| 2 | `@startup_strategist` | Business-model coherence — does the inferred model hang together; the build-vs-claim gap in strategy terms; wedge/moat readability |
| 3 | `@senior_product_manager` | Product coherence — does the built surface map to a real user problem and the inferred Customer Segment |

---

## Phase C — Specialist injection (signal-driven; the dynamic, domain-aware part)

Each row is a hard rule — if the inferred signal fired, inject the lens. Cap is
**3 specialists** (panel ≤ 6 total).

| Signal trigger (from inference) | Specialist lens injected |
|---|---|
| AI-feature flag set | `@ai_safety_specialist` **+ route to `ai-ux-review` and `ai-eval-review`** (conditional skills) |
| `has_statistical_claim` OR `is_data_intensive` with a correctness claim | `@data_scientist` (does the algorithm/ranking actually do what it claims?) |
| `involves_behavior_design = true` (voting, ranking, gamification, nudges) | `@lead_behavioral_scientist` |
| `is_regulated = true` (fintech, health, insurance, voting, crypto, minors data) | `@legal_compliance_advisor` |
| Handles money / PII / credentials | `@security_specialist` (also confirms the secret-redaction surface) |
| `involves_minors = true` | `@developmental_psychologist` |
| `domain = health` / `biotech` AND evidence-based claims | `@clinical_researcher` |
| `audience = developer` (dev tools, public API, SDK) | `@developer_advocate` |
| `is_international = true` AND consumer surface | `@i18n_specialist` |
| `has_brand_impact = true` AND `audience = b2c` | `@brand_strategist` |

---

## Phase D — Cap and trim (panel ≤ 6)

3 fixed core + up to 3 specialists. If injection fires more than 3 times, trim by
priority — higher survives:

1. **Risk-blocking** — `@legal_compliance_advisor`, `@developmental_psychologist`,
   `@ai_safety_specialist`, `@security_specialist` (never cut if their trigger fired).
2. **Claim-validating** — `@data_scientist`, `@clinical_researcher` (the lenses
   that test whether a load-bearing claim is real).
3. **Domain / reach** — `@lead_behavioral_scientist`, `@developer_advocate`,
   `@i18n_specialist`, `@brand_strategist`.

Specialists trimmed by the cap are **named in the dossier's panel footnote** with
the diligence concern they didn't get to cover — the user must see what was left
out. (No silent caps.)

---

## Phase E — Per-lens findings pass + panel write-up

Output the panel summary block (goes into the dossier's Audit findings section
header and is echoed so the user can challenge it before the pass — if they
redirect, re-trim, don't re-debate):

```markdown
**Audit panel (3 core + N specialists):**

| Lens | Why included | Slot |
|---|---|---|
| @senior_software_architect | Core | Fixed |
| @startup_strategist | Core | Fixed |
| @senior_product_manager | Core | Fixed |
| @ai_safety_specialist | AI-feature flag set | Specialist |
| @data_scientist | has_statistical_claim | Specialist |

**Signals (inferred):** audience=b2c, is_data_intensive=true, AI-feature=true, ...
```

Then **each lens emits exactly one findings block** — single pass, no debate:

```markdown
#### @<lens> — <one-line focus>
- **Finding [Fn]:** <observation> — grounded in <canvas field / diff row Fk / signal:provenance>.
- **Finding [Fn+1]:** ...
```

**Hard rules for the findings pass:**

- Every finding cites the canvas field, diff row, or signal provenance it rests
  on. A finding with no anchor is rhetoric — drop it.
- Each lens emits **one** block. No back-and-forth, no rebuttal round — that's
  grill's distinct job downstream.
- The AI-safety lens, when present, references the `ai-ux-review` /
  `ai-eval-review` outputs (if those skills ran) rather than re-deriving AI
  quality findings.

**Advice tier — "Options the evidence suggests":** after the findings, generate
grounded options (including pivot directions). **Every option must cite the
`finding-id` that motivates it — uncited options are suppressed.** Do **not** emit
an Investable / Pivot / Pass verdict; that is `startup-grill`'s job, reached via
the dossier handoff.

---

## Worked example (synthetic — regression check)

Inferred signals for "PollWise" (from `inference-mapping.md`): `audience=b2c`,
`is_data_intensive=true`, AI-feature=true, `involves_behavior_design=true`
(pairwise voting), `has_statistical_claim=true` ("statistically valid ranking").

Resolved panel: 3 core (`@senior_software_architect`, `@startup_strategist`,
`@senior_product_manager`) + specialists `@ai_safety_specialist` (AI flag, routes
to ai-ux-review/ai-eval-review), `@data_scientist` (the ranking-validity claim),
`@lead_behavioral_scientist` (voting mechanics). 3 specialists — within cap.

Each emits one findings block (e.g. `@data_scientist`: *"Finding F4 — the
'statistically valid ranking emerges' claim rests on pairwise aggregation in
`pairVoteCounts`; with sparse participation the ranking confidence is unproven —
grounded in Solution block + schema:pairVoteCounts."*). Options cite findings;
no verdict emitted.
