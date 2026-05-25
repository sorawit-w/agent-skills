# Skill graph

The canonical map of every skill on the shelf — what it does, who reaches for it, and how the skills relate. This is the single source the root [`README.md`](../README.md)'s "Start here" and "Building on the shelf" sections point at. When you add or change a skill, update this file (see [`CLAUDE.md` → Release ritual](../CLAUDE.md#release-ritual)).

For per-skill usage, design notes, and cross-skill detail, follow each name to its own README under [`skills/`](../skills/).

## Nodes — the 19 skills

Audience buckets map to the README's "Start here" rows: **Startup** (build & validate a startup), **Review** (review a product or AI product), **Author** (authoring, auditing & coordinating skills), **Calibrate/visual** (calibrate, localize & visuals).

| Skill | Purpose | Primary audience | Status | Audience bucket(s) |
|---|---|---|---|---|
| [`brand-workshop`](../skills/brand-workshop/README.md) | Discovery → Concept → Creation → brand identity package (logo, tagline, brief, DESIGN.md tokens) | Founders, product leads | stable | Startup · Calibrate/visual |
| [`validation-canvas`](../skills/validation-canvas/README.md) | Lean Canvas + Value Proposition Canvas (Markdown + HTML) | Early founders, product leads | stable | Startup · Review |
| [`riskiest-assumption-test`](../skills/riskiest-assumption-test/README.md) | Falsifiable hypotheses, risk×impact matrix, test plan | Founders de-risking before funding | stable | Startup |
| [`pitch-deck`](../skills/pitch-deck/README.md) | Investor-ready self-contained HTML deck (Reveal.js) | Founders fundraising | stable | Startup |
| [`startup-grill`](../skills/startup-grill/README.md) | Adversarial panel → kill report (Investable / Pivot / Pass) | Founders (pre-mortem), advisors | stable | Startup |
| [`startup-launch-kit`](../skills/startup-launch-kit/README.md) | Opt-in orchestrator sequencing the 5-step pipeline | Founders wanting end-to-end | stable | Startup |
| [`gtm`](../skills/gtm/README.md) | Phased go-to-market playbook + content + scheduling | Founders post-pipeline getting users | 🚧 BETA | Startup |
| [`team-composer`](../skills/team-composer/README.md) | Multi-role 3-round discussion → conclusion + plan | PMs, engineers, anyone planning | stable | Review · Author |
| [`ai-ux-review`](../skills/ai-ux-review/README.md) | 7-block human-AI design-completeness review (MD + HTML) | AI product teams, designers, PMs | stable | Review |
| [`ai-eval-review`](../skills/ai-eval-review/README.md) | 7-block AI eval-design review + regulatory lens (MD + HTML) | AI teams, measurement eng, compliance | stable | Review |
| [`skill-evaluator`](../skills/skill-evaluator/README.md) | Audit a SKILL.md for rule adherence; targeted diffs | Skill authors, QA gatekeepers | stable | Author |
| [`coding-rules`](../skills/coding-rules/README.md) | Load/install opinionated agentic-coding guardrails | Individual devs, teams | ⚠️ OPINIONATED | Author |
| [`tech-stack-recommendations`](../skills/tech-stack-recommendations/README.md) | Opinionated TS/JS stack + named alternates | Founders, architects, engineers | stable | Author |
| [`sub-agent-coordinator`](../skills/sub-agent-coordinator/README.md) | Orchestrate parallel sub-agents (brief, coordinate, verify) | Coordinators, multi-file devs | stable | Author |
| [`wear-the-hat`](../skills/wear-the-hat/README.md) | Single-role solo embodiment (one lens, no panel) | Anyone wanting one expert lens | stable | Author |
| [`whoami`](../skills/whoami/README.md) | Person-level collaboration profile (6 dials, RPG class) | Users new to AI / switching vendors | stable | Calibrate/visual |
| [`handshake`](../skills/handshake/README.md) | Brief project/collaboration calibration ritual | Anyone wanting tailored calibration | stable | Calibrate/visual |
| [`i18n-contextual-rewriting`](../skills/i18n-contextual-rewriting/README.md) | Safe edits on large translation files + cultural rewriting | Localization eng, product teams | stable | Calibrate/visual |
| [`pixel-art`](../skills/pixel-art/README.md) | Hi-fi / lo-fi pixel art + prompt briefs + SVG title cards | Designers, game devs, creators | 🚧 BETA | Calibrate/visual |

## Edges — how the skills relate

```mermaid
graph LR
  %% Startup pipeline (solid = gated handoff)
  BW[brand-workshop] --> VC[validation-canvas] --> RAT[riskiest-assumption-test] --> PD[pitch-deck] --> SG[startup-grill] --> GTM["gtm (beta)"]
  SLK[startup-launch-kit] -. orchestrates .-> BW

  %% Delegation pipeline
  TC[team-composer] -->|Phase 6 delegate| SAC[sub-agent-coordinator]

  %% AI-review siblings
  AUX[ai-ux-review] <-. sibling .-> AEV[ai-eval-review]

  %% Personalization
  WAI[whoami] --> HS[handshake]

  %% Key cross-edges (dashed = pairs-with / consumes / suggests)
  WTH[wear-the-hat] -. role catalog .-> TC
  BW -. DESIGN.md tokens .-> VC
  VC -. AI startups .-> AUX
  RAT -. gaps to tests .-> AUX
  GTM -. content fan-out .-> SAC
  GTM -. non-EN content .-> I18N[i18n-contextual-rewriting]
  PXL[pixel-art] -. portrait .-> WAI
  SE[skill-evaluator] -. audits any skill .-> TC
  CR[coding-rules] -. discipline + lens .-> WTH
  TSR[tech-stack-recommendations] -. architect anchor .-> TC
```

**Legend.** Solid arrow = gated or structured handoff (the downstream skill reads the upstream output, sometimes refusing to proceed without it). Dashed arrow = pairs-with / consumes / suggests (a softer relationship). `skill-evaluator` audits *every* skill on the shelf; one representative edge is shown to keep the graph readable.

## Two pipelines worth knowing

- **Startup pipeline** — `brand-workshop` → `validation-canvas` → `riskiest-assumption-test` → `pitch-deck` → `startup-grill` → `gtm` 🚧. Sequential by default, gated (some handoffs refuse without upstream output), loop-back is first-class. `startup-launch-kit` is an opt-in orchestrator over the five core steps. See the root README's [How skills chain](../README.md#how-skills-chain) for the gate weights and artifact-compounding detail.
- **Delegation pipeline** — `team-composer` → `sub-agent-coordinator`. Discussion concludes, then deliverables fan out through the coordinator's briefing patterns.
