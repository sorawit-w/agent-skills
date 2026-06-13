# Skill graph

The canonical map of every skill on the shelf — what it does, who reaches for it, and how the skills relate. This is the single source the root [`README.md`](../README.md)'s "Start here" and "Building on the shelf" sections point at. When you add or change a skill, update this file (see [`CLAUDE.md` → Release ritual](../CLAUDE.md#release-ritual)).

For per-skill usage, design notes, and cross-skill detail, follow each name to its own README under [`skills/`](../skills/).

## Nodes — the skills

Audience buckets map to the README's "Start here" rows: **Startup** (build & validate a startup), **Review** (review a product or AI product), **Code** (writing & shipping code), **Author** (authoring & auditing skills), **Calibrate/visual** (calibrate, localize & visuals).

| Skill | Purpose | Primary audience | Status | Audience bucket(s) |
|---|---|---|---|---|
| [`brand-workshop`](../skills/brand-workshop/README.md) | Discovery → Concept → Creation → brand identity package (logo, tagline, brief, DESIGN.md tokens) | Founders, product leads | stable | Startup · Calibrate/visual |
| [`validation-canvas`](../skills/validation-canvas/README.md) | Lean Canvas + Value Proposition Canvas (Markdown + HTML) | Early founders, product leads | stable | Startup · Review |
| [`riskiest-assumption-test`](../skills/riskiest-assumption-test/README.md) | Falsifiable hypotheses, risk×impact matrix, test plan | Founders de-risking before funding | stable | Startup |
| [`pitch-deck`](../skills/pitch-deck/README.md) | Investor-ready self-contained HTML deck (Reveal.js) | Founders fundraising | stable | Startup |
| [`startup-grill`](../skills/startup-grill/README.md) | Adversarial panel → kill report (Investable / Pivot / Pass) | Founders (pre-mortem), advisors | stable | Startup |
| [`startup-audit`](../skills/startup-audit/README.md) | Built-artifact triage: codebase/URL → inferred Lean Canvas + build-vs-claim diff → **fast Continue/Pivot/Kill verdict + R/A/G band** (opinion, not advice); diligence-only flag for no-verdict | Founders triaging their build, investors doing technical DD | stable | Startup · Review |
| [`startup-launch-kit`](../skills/startup-launch-kit/README.md) | Opt-in orchestrator sequencing the 5-step pipeline; greenfield or existing-project (reuses `startup-audit` to seed the canvas from a codebase) | Founders wanting end-to-end, pre- or post-build | stable | Startup |
| [`gtm`](../skills/gtm/README.md) | Phased go-to-market playbook + content + scheduling | Founders post-pipeline getting users | 🚧 BETA | Startup |
| [`team-composer`](../skills/team-composer/README.md) | Multi-role 3-round discussion → conclusion + plan | PMs, engineers, anyone planning | stable | Review · Author |
| [`ai-ux-review`](../skills/ai-ux-review/README.md) | 7-block human-AI design-completeness review (MD + HTML) | AI product teams, designers, PMs | stable | Review |
| [`ai-eval-review`](../skills/ai-eval-review/README.md) | 7-block AI eval-design review + regulatory lens (MD + HTML) | AI teams, measurement eng, compliance | stable | Review |
| [`gamification-fit`](../skills/gamification-fit/README.md) | Restraint-first gamification *recommender*: resources + goal → the few mechanics that honestly fit + a prominent "deliberately NOT gamified" refusals section; structural ethics veto (MD + HTML) | Product teams, founders adding engagement | stable | Review |
| [`skill-evaluator`](../skills/skill-evaluator/README.md) | Audit a SKILL.md for rule adherence; targeted diffs | Skill authors, QA gatekeepers | stable | Author |
| [`coding-rules`](../skills/coding-rules/README.md) | Load/install opinionated agentic-coding guardrails | Individual devs, teams | ⚠️ OPINIONATED | Code |
| [`tech-stack-recommendations`](../skills/tech-stack-recommendations/README.md) | Opinionated TS/JS stack + named alternates | Founders, architects, engineers | stable | Code |
| [`sub-agent-coordinator`](../skills/sub-agent-coordinator/README.md) | Orchestrate parallel sub-agents (brief, coordinate, verify) | Coordinators, multi-file devs | stable | Code · Author |
| [`wear-the-hat`](../skills/wear-the-hat/README.md) | Single-role solo embodiment (one lens, no panel) | Anyone wanting one expert lens | stable | Code |
| [`whoami`](../skills/whoami/README.md) | Person-level collaboration profile (6 dials, RPG class) | Users new to AI / switching vendors | stable | Calibrate/visual |
| [`handshake`](../skills/handshake/README.md) | Brief project/collaboration calibration ritual | Anyone wanting tailored calibration | stable | Calibrate/visual |
| [`i18n`](../skills/i18n/README.md) | Safe edits on large translation files + cultural rewriting | Localization eng, product teams | stable | Calibrate/visual |
| [`define`](../skills/define/README.md) | Contextual definition/translation of a word or phrase from its surrounding sentence (learner gloss) | Language learners, readers, translators | stable | Calibrate/visual |
| [`ghostwriter`](../skills/ghostwriter/README.md) | Personal-voice message drafting (email/Slack/DM/LinkedIn) — zero AI tells, ban-list lint, samples > ban list, six style presets + free-form | Anyone sending messages under their own name | stable | Calibrate/visual |
| [`pixel-art`](../skills/pixel-art/README.md) | Hi-fi / lo-fi pixel art + prompt briefs + SVG title cards | Designers, game devs, creators | 🚧 BETA | Calibrate/visual |

## Edges — how the skills relate

```mermaid
graph LR
  %% Startup pipeline (solid = gated handoff)
  BW[brand-workshop] --> VC[validation-canvas] --> RAT[riskiest-assumption-test] --> PD[pitch-deck] --> SG[startup-grill] --> GTM["gtm (beta)"]
  SLK[startup-launch-kit] -.->|orchestrates| BW
  SLK -.->|existing-project: mode=diligence code read| SA

  %% Delegation pipeline
  TC[team-composer] -->|Phase 6 delegate| SAC[sub-agent-coordinator]

  %% AI-review siblings
  AUX[ai-ux-review] -.->|sibling| AEV[ai-eval-review]

  %% Gamification fit (two-parent fork: startup-audit ingest + ai-ux-review render + startup-grill veto)
  VC -.->|goal source| GF[gamification-fit]
  GTM -.->|North Star goal| GF
  AUX -.->|where mechanics live| GF
  GF -.->|scope the build| TC

  %% Personalization
  WAI[whoami] --> HS[handshake]
  GW[ghostwriter] -.->|consumes profile| WAI
  GW -.->|opt-in draft critique| TC

  %% Post-build diligence (mirror of the pre-build pipeline)
  SA[startup-audit] -.->|offers to seed canvas| VC
  SA -.->|recommends tests for unknowns| RAT
  SA -.->|Kill/Pivot → confirm (deep verdict)| SG
  SA -.->|reads personas| TC
  SA -.->|AI features| AUX

  %% Key cross-edges (dashed = pairs-with / consumes / suggests)
  WTH[wear-the-hat] -.->|role catalog| TC
  BW -.->|brand tokens| VC
  VC -.->|AI startups| AUX
  RAT -.->|gaps to tests| AUX
  GTM -.->|content fan-out| SAC
  GTM -.->|non-EN content| I18N[i18n]
  DEF[define] -.->|shared locale engine| I18N
  PXL[pixel-art] -.->|portrait| WAI
  SE[skill-evaluator] -.->|audits any skill| TC
  CR[coding-rules] -.->|discipline + lens| WTH
  TSR[tech-stack-recommendations] -.->|architect anchor| TC
```

**Legend.** Solid arrow = gated or structured handoff (the downstream skill reads the upstream output, sometimes refusing to proceed without it). Dashed arrow = pairs-with / consumes / suggests (a softer relationship). `skill-evaluator` audits *every* skill on the shelf; one representative edge is shown to keep the graph readable.

## Two pipelines worth knowing

- **Startup pipeline** — `brand-workshop` → `validation-canvas` → `riskiest-assumption-test` → `pitch-deck` → `startup-grill` → `gtm` 🚧. Sequential by default, gated (some handoffs refuse without upstream output), loop-back is first-class. `startup-launch-kit` is an opt-in orchestrator over the five core steps. It runs greenfield (step-by-step) or in **existing-project mode** — when pointed at a built repo it reuses `startup-audit` (`mode=diligence`) to read the code and seed `validation-canvas.md`, then `validation-canvas` confirms the machine-inferred seed (tiered) instead of interviewing blind. See the root README's [How skills chain](../README.md#how-skills-chain) for the gate weights and artifact-compounding detail.
- **Delegation pipeline** — `team-composer` → `sub-agent-coordinator`. Discussion concludes, then deliverables fan out through the coordinator's briefing patterns.
- **Built-artifact triage** — `startup-audit` is the post-build sibling of `startup-grill`, split by **input + rigor**: audit reads a *built product* (codebase/URL) and gives a *fast* Continue/Pivot/Kill triage verdict; grill reads *belief artifacts* (canvas/deck) and gives the *deep* 3-round adversarial verdict. A Kill/Pivot from audit routes to grill to confirm (seed `validation-canvas.md` first — grill/pitch-deck read that file, not audit's `inferred-canvas.md`). For `riskiest-assumption-test` the handoff is a recommendation to test the `unknown` blocks. The verdict is opinion, not advice.
