<p align="center">
  <img src="assets/hero.svg" alt="agent-skills — a personal shelf of Claude Code plugins" width="100%"/>
</p>

<h1 align="center">agent-skills</h1>

<p align="center">
  <em>A personal shelf of Claude Code plugins. Hand-crafted, one skill at a time.</em><br/>
  <sub>Specialized skills for Claude Code &amp; Cowork — each one narrow, opinionated, and evaluated before it ships.</sub>
</p>

<p align="center">
  <a href="#install"><img alt="install" src="https://img.shields.io/badge/install-%2Fplugin%20marketplace%20add%20sorawit--w%2Fagent--skills-1f2937?style=flat-square"></a>
  <a href="LICENSE"><img alt="MIT license" src="https://img.shields.io/badge/license-MIT-6b7280?style=flat-square"></a>
  <a href="https://docs.claude.com/en/docs/claude-code"><img alt="built for claude code" src="https://img.shields.io/badge/built%20for-Claude%20Code%20%7C%20Cowork-c2410c?style=flat-square"></a>
</p>

---

## TL;DR

- **What this is** — a single Claude Code plugin that installs a curated shelf of thirteen specialized skills in one go.
- **Who it's for** — anyone using Claude Code or Cowork who wants auto-triggering expertise for a specific job: founders pitching investors, PMs brainstorming with a team, engineers writing or auditing a skill, localizers rewriting inside cultural reality, founders who want their startup adversarially probed, and anyone who wants the agent to know how *they* prefer to collaborate before the work starts.
- **How to start** — run the two-line install below. Each skill triggers on its own description when you describe the job — you don't have to memorize them.

## Install

```bash
/plugin marketplace add sorawit-w/agent-skills
/plugin install agent-skills@sorawit-w
```

That's it — every skill below is now on the shelf. Works from both [Claude Code](https://docs.claude.com/en/docs/claude-code) and Cowork.

**When the plugin updates**, refresh once and reinstall:

```bash
/plugin marketplace update sorawit-w
/plugin install agent-skills@sorawit-w
```

> Claude Code caches the marketplace index locally — new skills and fixes only appear after an explicit refresh.

---

## The shelf

Click a skill to jump to its details.

|  | Skill | What it's for | Reach for it when |
|:---:|:---|:---|:---|
| <img src="assets/icons/team-composer.svg" alt="" width="64" align="middle"/> | [`team-composer`](#team-composer) | Assemble the right virtual team and run a 3-round discussion that forces real disagreement. | You want multi-perspective planning or review with a conclusion you can act on. |
| <img src="assets/icons/sub-agent-coordinator.svg" alt="" width="64" align="middle"/> | [`sub-agent-coordinator`](#sub-agent-coordinator) | Orchestrate multi-agent work — briefing, coordination, and verification that don't drift. | You're kicking off a task bigger than fifteen minutes that's at least partially parallelizable. |
| <img src="assets/icons/skill-evaluator.svg" alt="" width="64" align="middle"/> | [`skill-evaluator`](#skill-evaluator) | Audit a skill to see whether its rules actually land when Claude runs it. | You just wrote a skill, or one has been "mostly working" and you suspect a rule is being skipped. |
| <img src="assets/icons/tech-stack-recommendations.svg" alt="" width="64" align="middle"/> | [`tech-stack-recommendations`](#tech-stack-recommendations) | Opinionated default TS/JS stack (Bun + SvelteKit + Elysia + Neon + Drizzle + Clerk), plus named alternates. | You're starting a new project, or picking one layer, and want a default instead of a neutral grid. |
| <img src="assets/icons/handshake.svg" alt="" width="64" align="middle"/> | [`handshake`](#handshake) | A brief opt-in calibration ritual that shows you what's on file, then asks ≤4 high-leverage collaboration questions (and optionally ≤6 scoped project questions). Writes to the existing memory store. | You want the agent to know *how* you prefer to collaborate before it starts giving generic answers, or you want a transparent moment to see and correct what's been captured about you. |
| <img src="assets/icons/i18n-contextual-rewriting.svg" alt="" width="64" align="middle"/> | [`i18n-contextual-rewriting`](#i18n-contextual-rewriting) | Surgical edits on large translation files, plus a role-based review that turns "translate" into cultural rewriting. | You're editing a big i18n file without blowing token limits, or producing translations that shouldn't read as machine-converted English. |
| <img src="assets/icons/brand-workshop.svg" alt="" width="64" align="middle"/> | [`brand-workshop`](#brand-workshop) | Run a Discovery → Concept → Creation workshop and ship a brand strategy brief, tagline, and code-generated logo. | You need a real identity package for a product, app, or startup — not just a logo doodle. |
| <img src="assets/icons/validation-canvas.svg" alt="" width="64" align="middle"/> | [`validation-canvas`](#validation-canvas) | Interview a founder block-by-block and produce a rigorous Lean Canvas + Value Proposition Canvas with explicit Stress Tests. Adapts to founder experience via 3-question intake. | You need a beliefs artifact that holds up to scrutiny — *what do we believe?* — before designing tests, building the deck, or pitching. |
| <img src="assets/icons/riskiest-assumption-test.svg" alt="" width="64" align="middle"/> | [`riskiest-assumption-test`](#riskiest-assumption-test) | Convert canvas Stress Tests into falsifiable hypotheses with success/kill criteria and chosen test methods. Ships a 1-page test plan + interactive risk × impact matrix. | You have beliefs in your canvas and need to know *what to test first*, with the cheapest experiment that could falsify it. |
| <img src="assets/icons/pitch-deck.svg" alt="" width="64" align="middle"/> | [`pitch-deck`](#pitch-deck) | Structured narrative interview across the 10-slide investor arc; ships a self-contained HTML deck + speaker notes. Heavy gate on `riskiest-assumption-test` results. | An investor said "send me your deck" and you've already validated your top assumptions — now you need a shippable v1 this week. |
| <img src="assets/icons/startup-grill.svg" alt="" width="64" align="middle"/> | [`startup-grill`](#startup-grill) | Adversarially probe a startup with a panel of domain-aware grillers; ship a kill report ranked by severity × fixability with optional interactive defense. Includes an iteration-evidence check. | You want your idea / deck / canvas probed for what would actually kill it — not "thoughts to consider," a verdict you can act on. |
| <img src="assets/icons/startup-launch-kit.svg" alt="" width="64" align="middle"/> | [`startup-launch-kit`](#startup-launch-kit) | Opt-in umbrella orchestrator that sequences the five-step startup pipeline (brand → canvas → tests → pitch → grill) with shared state via `docs/startup-kit/kit-manifest.json`. Never bypasses gates; every individual skill stays independently invocable. | You're starting a new idea from scratch and want end-to-end coordination, OR you ran a few steps manually and want to absorb them into an orchestrated resume. |
| <img src="assets/icons/gtm.svg" alt="" width="64" align="middle"/> | [`gtm`](#gtm) **🚧 BETA** | Phased go-to-market for startup products. Builds a GTM playbook from upstream artifacts, produces multi-channel content, schedules cadenced tasks, enforces compliance, emits handoff events. Trust ramp P1 → P2 → P3. Project-local `.gtm/`. Architectural kill switch via HALT file. | The pitch deck is locked and you need to actually get users — multi-channel marketing motion with state, scheduling, compliance gates, and a kill switch you can trust. **Beta** — evals are structural-only; not yet dogfooded on a real founder workflow. |

Each skill lives under [`skills/`](skills/) with its own `README.md`, `SKILL.md`, and reference docs.

---

## How skills chain

Two pipelines the shelf is designed to support end-to-end.

### 🧭 Startup pipeline — identity → beliefs → tests → deck → grill → ship 🚧

```
brand-workshop ──▶ validation-canvas ──▶ riskiest-assumption-test ──▶ pitch-deck ──▶ startup-grill ──▶ gtm 🚧
 (identity kit)    (Lean Canvas + VPC)    (test plan + results)        (HTML deck)    (kill report)    (BETA — get users)
```

The sixth step (`gtm`) is **beta** — it slots in after `startup-grill` for founders who've graduated the pipeline and want to actually go acquire users. Evals validate structural reliability; real-world dogfooding is the next milestone before v1.

**Sequential by default. No one-shot orchestrator** — each skill is invocable independently, but composes through filesystem conventions. **Inter-step gates are weighted:** `brand-workshop` → `validation-canvas` is light; `validation-canvas` → `riskiest-assumption-test` is medium (RAT STOPs without canvas); `riskiest-assumption-test` → `pitch-deck` is **heavy** (pitch-deck STOPs without populated `## Results` for top-3 hypotheses; override with `[PRE-VALIDATION DRAFT]` watermark); `pitch-deck` → `startup-grill` is light. **Loop-back is first-class** — invalidated hypotheses route back to `validation-canvas` in update mode, not a pipeline restart. Pristine pipelines (no canvas revision after testing) are the actual yellow flag, which `startup-grill` checks for in its kill-report `## Iteration Evidence` section.

**The artifacts compound.** As of v2.2.0, every artifact lives under `docs/` (default `docs/<skill>/` solo, `docs/startup-kit/<skill>/` orchestrated; v1 layouts at cwd root still read via fallback). `brand-workshop` writes `docs/brand/DESIGN.md` ([Google Labs spec](https://github.com/google-labs-code/design.md), alpha) — `validation-canvas`, `riskiest-assumption-test`, and `pitch-deck` all pick it up automatically and extract tokens from the YAML front matter for consistent branding. `validation-canvas` writes `docs/canvas/validation-canvas.md` (Lean Canvas + VPC) — its Stress Tests section seeds `riskiest-assumption-test`'s assumption dump; `pitch-deck` reads it to seed slides 2, 3, 6 and cross-checks the Ask against the Stress Tests. `riskiest-assumption-test` writes `docs/rat/assumption-test-plan.md` + interactive `docs/rat/test-matrix.html` — `pitch-deck` reads `## Top 3 Hypotheses` and `## Results` to inform the Validation slide and Traction claims; `startup-grill` reads them for the iteration-evidence check. `startup-grill` reads everything as direct grilling ammunition and ships a `docs/grill/kill-report.md` with a verdict you can act on. You don't have to wire anything up; running them in order is the wiring.

**Pipeline philosophy:** validation is iterative, not a checklist. Each step's value is in the slow consideration it forces.

**Pipeline shortcut (v2.1.0+):** the optional `startup-launch-kit` skill is an *opt-in orchestrator* that sequences the five steps with shared state via `kit-manifest.json` (at `docs/startup-kit/kit-manifest.json` as of v2.2.0). It is **convenience, not replacement**: every individual skill remains independently invocable, every gate is honored (no silent bypass), and every step still surfaces its own prompts to the founder (no batching). The orchestrator preserves the philosophy by recording every gate override with a reason, by surfacing loop-back recommendations after RAT and grill (founder decides; never auto-routes), and by treating the manifest as a hint rather than truth (filesystem state always wins on reconciliation). Use it when you want end-to-end coordination without manual step-chaining; use the individual skills directly for any single-step or partial-pipeline work.

### 🛰 Delegation pipeline — discuss → build

```
team-composer ──▶ sub-agent-coordinator
 (3-round debate)   (parallel build with verification)
```

`team-composer`'s Phase 6 hands its conclusion, decisions, and role constraints to `sub-agent-coordinator`'s briefing patterns — so the discussion's context survives the handoff to the deliverable instead of evaporating mid-flight.

---

## Skill details

<a id="team-composer"></a>

### <img src="assets/icons/team-composer.svg" alt="" width="48" align="middle"/> &nbsp;`team-composer`

**What it does.** Assembles a virtual team of domain personas — across tech, health, fintech, climate, biotech, games, and beyond — runs a structured 3-round discussion (opening positions → rebuttals → synthesis), and returns a conclusion with recommendation, trade-offs, and prioritized next steps. Every role earns its seat via signal-based scoring; the discussion is designed to produce real disagreement rather than restated agreement.

**Reach for it when.** You have a decision, plan, or review that needs more than one lens, and you want the trade-offs surfaced explicitly instead of smoothed over. Good for new-product brainstorming, architecture reviews, regulated-domain gut-checks, and cross-functional planning sessions.

**Pairs well with.**
- [`sub-agent-coordinator`](#sub-agent-coordinator) — Phase 6 delegates deliverable production through its patterns.
- [`skill-evaluator`](#skill-evaluator) — audit team-composer (or any team-driven skill) for rules that get quietly skipped.
- [`tech-stack-recommendations`](#tech-stack-recommendations) — when the architect role needs an opinionated stack to anchor the debate.
- [`i18n-contextual-rewriting`](#i18n-contextual-rewriting) — when the `@i18n_specialist` is on the team and the output needs to ship in multiple locales.

**Try it.**
- "Bring a team together to review this mobile auth architecture before we ship."
- "Brainstorm a habit-tracker for teens — multi-perspective, no single viewpoint wins."
- "After team-composer concludes, hand Phase 6 deliverables to `sub-agent-coordinator` and fan out the architect / backend / frontend work in parallel."

---

<a id="sub-agent-coordinator"></a>

### <img src="assets/icons/sub-agent-coordinator.svg" alt="" width="48" align="middle"/> &nbsp;`sub-agent-coordinator`

**What it does.** Turns the primary agent into a coordinator: breaks work into parallelizable chunks, writes quick briefs, dispatches sub-agents through fan-out / pipeline / specialist patterns, and verifies results instead of blindly merging them. Strict about what *not* to do — no nested delegation, no overlapping file edits, no trust without verification.

**Reach for it when.** You're starting a multi-step task that's clearly bigger than fifteen minutes and at least partially parallelizable — debugging a flaky suite, auditing a codebase, landing a multi-file feature — and you don't want the coordinator to grind alone for an hour.

**Pairs well with.**
- [`team-composer`](#team-composer) — natural upstream: discussion finishes, deliverables fan out via coordinator patterns.
- [`skill-evaluator`](#skill-evaluator) — spawn evaluator sub-agents to stress-test other skills in parallel.

**Try it.**
- "Refactor all 14 React components from class to function — coordinate in parallel."
- "Debug our flaky CI suite: spawn a researcher, a fixer, and a reviewer with clear briefs."
- "After `team-composer` concludes, brief sub-agents to produce the per-role deliverables the conclusion assigned."

---

<a id="skill-evaluator"></a>

### <img src="assets/icons/skill-evaluator.svg" alt="" width="48" align="middle"/> &nbsp;`skill-evaluator`

**What it does.** Reads a target skill end-to-end (`SKILL.md` plus every referenced file), generates test prompts spanning happy paths, trigger edges, and rule-specific stress tests, then grades outputs against the rules — without letting the grader peek at the skill text. Classifies failures by fix layer (skill text / rubric / brief / fixture) and proposes targeted rule-text diffs.

**Reach for it when.** You just wrote a skill and want to stress-test it, or a skill has been "mostly working" and you suspect a rule is being quietly skipped. Also useful for vetting someone else's skill before you install it.

**Pairs well with.**
- **Every other skill on this shelf** — use it to audit any of them. The shelf is only as sharp as its weakest rule.
- [`sub-agent-coordinator`](#sub-agent-coordinator) — run evaluation variants in parallel (different prompt sets, different grader instances) and converge findings.

**Try it.**
- "Stress-test `team-composer` — does Round 2 actually produce rebuttals, or is it ceremonial?"
- "My onboarding skill has been 'mostly working.' Audit it and tell me which rules are getting skipped."
- "Use `sub-agent-coordinator` to fan out evaluator runs against three of our skills in parallel and converge the findings."

---

<a id="tech-stack-recommendations"></a>

### <img src="assets/icons/tech-stack-recommendations.svg" alt="" width="48" align="middle"/> &nbsp;`tech-stack-recommendations`

**What it does.** Names a single opinionated default stack — Bun + SvelteKit + Elysia + Neon + Drizzle + Clerk, with Tailwind + shadcn on top — and two alternates with clear triggers (Deno for edge-first / sandboxed, Node 22 LTS for ecosystem-heavy / Angular / NestJS). Covers the full vertical: runtime, monorepo layout, framework, hosting, database, auth, styling, mobile, i18n, icon system, AI assistant config. Topic guides load on demand with override factors named up front.

**Reach for it when.** You're starting a new TypeScript/JavaScript project, picking one layer (runtime, DB, auth, hosting, mobile, i18n), or migrating between stacks — and you want one clear default instead of a neutral grid where every cell reads "it depends."

**Pairs well with.**
- [`team-composer`](#team-composer) — when the architect role needs an anchor position to debate from.
- [`skill-evaluator`](#skill-evaluator) — audit the stack rules against your real constraints before committing.

**Try it.**
- "I'm starting a SaaS side-project. Give me one opinionated stack I don't have to second-guess."
- "We're migrating off Next.js on Vercel — recommend the path and name the trade-offs honestly."
- "Kick off a `team-composer` architecture review and load `tech-stack-recommendations` as the architect's anchor position."

---

<a id="handshake"></a>

### <img src="assets/icons/handshake.svg" alt="" width="48" align="middle"/> &nbsp;`handshake`

**What it does.** A brief mutual exchange that establishes the terms of subsequent collaboration — not a friendship, not an interview, a handshake. Three phases: (1) **show what I know** — surfaces the most relevant existing `user`-type memory entries (≤5) with filenames in brackets, so you can correct stale facts before anything new gets added; (2) **core calibration** — asks ≤4 high-leverage pill questions (expertise framing, default collaboration mode, output verbosity, one explicit collaboration norm) plus 1 free-text "what did past assistants get wrong about you?" question, each with a stated behavioral payoff; (3) **optional project overlay** — ≤6 scoped questions about the current project (goal, stage, stakeholders, constraints, past decisions, external resources), all skippable, written to `project`-type memory. Closes with a written-to-memory summary so memory stays transparent. Hard never-ask list mirrors the auto-memory PII rules.

**Reach for it when.** You want the agent to know how *you* prefer to collaborate before it starts giving generic answers. You've noticed memory accruing passively but never been shown what's on file. A new project is starting and `project`-type memory is empty. Or another skill suggests calibration because relevant memory is sparse.

**Pairs well with.**
- [`team-composer`](#team-composer) — when a team is about to be assembled and `user`-type memory is sparse, `team-composer` MAY suggest `/handshake` first so the team can be tailored to your collaboration style. Suggestion only; never auto-routes.
- [`brand-workshop`](#brand-workshop) — similar — may suggest `/handshake` for a personal-brand or solo-founder identity package. Suggestion only.
- [`validation-canvas`](#validation-canvas) / [`riskiest-assumption-test`](#riskiest-assumption-test) / [`pitch-deck`](#pitch-deck) — these read project state, not user state. May suggest `/handshake --project` at kickoff if `project`-type memory for the current work is empty. Suggestion only.
- `productivity:memory-management` *(if installed)* — `handshake` writes into the same two-tier `MEMORY.md` + `memory/` store. Capability-gated: defers to `productivity:memory-management`'s file-layout conventions when present, otherwise writes directly to the runtime's persistent memory.

**Try it.**
- "Calibrate how we work — I'm tired of generic answers."
- "Show me what you have on file about me, then ask the questions that would actually help."
- "Run `/handshake --project` for this repo before we start the next sprint."

---

<a id="i18n-contextual-rewriting"></a>

### <img src="assets/icons/i18n-contextual-rewriting.svg" alt="" width="48" align="middle"/> &nbsp;`i18n-contextual-rewriting`

**What it does.** Two halves. (1) File-handling discipline that refuses to rewrite a whole translation file — target affected lines only, reach for a script when the edit is genuinely bulk, never silently truncate. (2) A multi-role review pass that treats translation as contextual rewriting inside cultural reality, across 15+ locales and regional variants (including `zh-CN / zh-TW / zh-HK`, `ja`, `ko`, `th` with a Thai dialect variant `th-bupphe`, plus major European languages).

**Reach for it when.** You're editing a large i18n file (JSON / YAML / TS) without blowing token limits, adding a new locale, or producing Thai / Japanese / Chinese / European translations that shouldn't read as machine-converted English.

**Pairs well with.**
- [`team-composer`](#team-composer) — when `@i18n_specialist` is on the team, this skill executes the translation work the team's output needs.
- [`brand-workshop`](#brand-workshop) — localize the descriptions pack (taglines, bios, boilerplate) without losing voice.

**Try it.**
- "Translate this onboarding flow into Thai, Japanese, and Korean — cultural rewriting, not machine translation."
- "Edit three keys in a 4,000-line `zh-CN.json` without rewriting the whole file or blowing the token budget."
- "`brand-workshop` just shipped the descriptions pack — localize it into `th` and `ja` and keep the voice."

---

<a id="brand-workshop"></a>

### <img src="assets/icons/brand-workshop.svg" alt="" width="48" align="middle"/> &nbsp;`brand-workshop`

**What it does.** Assembles a virtual creative team, runs a Discovery → Concept → Creation workshop, and ships a launch-ready identity package: brand strategy brief (`.md`), tagline, code-generated logo (`.svg` rendered to `.png`), favicon pack with HTML install snippet, social banner set (OG / X / LinkedIn / Instagram), descriptions pack (bios + elevator pitch + boilerplate), and a starter `DESIGN.md` ([Google Labs spec](https://github.com/google-labs-code/design.md), alpha — tokens only) that downstream skills like `validation-canvas`, `riskiest-assumption-test`, and `pitch-deck` pick up automatically.

**Reach for it when.** You need a real identity package — positioning, voice, archetype, tagline, and mark all sharing the same rationale — not just a logo doodle. Skip the positioning and the logo is just a doodle.

**Pairs well with.**
- [`validation-canvas`](#validation-canvas) — suggested next step. Auto-applies brand tokens from the kit.
- [`riskiest-assumption-test`](#riskiest-assumption-test) — two steps downstream. Reads design tokens for the matrix HTML.
- [`pitch-deck`](#pitch-deck) — reads the brand design system (`docs/brand/DESIGN.md`) for consistent branding and owns the deck construction itself.
- [`i18n-contextual-rewriting`](#i18n-contextual-rewriting) — localize the descriptions pack while preserving tone.

**Try it.**
- "Run the full workshop for my meditation startup — identity, mark, voice, and design tokens."
- "I have a one-paragraph startup idea. Take me through Discovery → Concept → Creation and ship a launch-ready kit."
- "Brand-workshop first, then hand the kit to `validation-canvas` and `pitch-deck` so the whole startup artifact chain shares tokens."

---

<a id="validation-canvas"></a>

### <img src="assets/icons/validation-canvas.svg" alt="" width="48" align="middle"/> &nbsp;`validation-canvas`

**What it does.** Interviews a founder with **experience-adaptive intake** (3 calibration questions at invocation → Guided / Focused / Compressed-with-Challenge mode), then produces a combined **Lean Canvas (Maurya) + Value Proposition Canvas (Osterwalder)** as `validation-canvas.md` (canonical, editable, downstream-parseable) and `validation-canvas.html` (self-contained visual that prints cleanly to PDF). Runs a mandatory 7-question cross-block consistency pass + a VPC fit check. Ends with a Stress Tests section naming the 3–5 assumptions most likely to kill the business — which feeds directly into `riskiest-assumption-test` next.

**Replaces** the prior `business-model-canvas` skill. Lean Canvas is the right altitude for an idea-stage founder; the 9-block Osterwalder BMC is a Series-A operating-plan tool — wrong altitude. For board packets that explicitly need the 9-block grid, use `team-composer` with `@startup_strategist` for a discussion-grade fill.

**Reach for it when.** You need a beliefs artifact — *what do we believe?* — that holds up to scrutiny before testing assumptions, building the deck, or pitching. The intake adapts to your experience: first-timers get definitions and examples; repeat founders get push-back, not teaching.

**Pairs well with.**
- [`brand-workshop`](#brand-workshop) — upstream input; the canvas auto-applies brand tokens from the kit.
- [`riskiest-assumption-test`](#riskiest-assumption-test) — required next step (medium gate). Stress Tests seed the assumption dump; invalidated hypotheses loop back here in update mode.
- [`pitch-deck`](#pitch-deck) — two steps downstream. Reads canvas headings to seed slides 2, 3, 6 and cross-checks the Ask against Stress Tests.
- [`team-composer`](#team-composer) — when a block is contested, kick it to a full multi-role team for a focused session.
- [`startup-grill`](#startup-grill) — last step. Reads Stress Tests and un-relieved Pains as direct grilling ammunition.

**Try it.**
- "Build a validation canvas for my AI code-review tool."
- "I'm a 3rd-time founder pivoting into healthtech — run the canvas in compressed mode and challenge me hard."
- "`brand-workshop` is done — use the brand kit as input and generate the canvas with auto-styled tokens."

---

<a id="riskiest-assumption-test"></a>

### <img src="assets/icons/riskiest-assumption-test.svg" alt="" width="48" align="middle"/> &nbsp;`riskiest-assumption-test`

**What it does.** Reads the validation canvas (`docs/canvas/validation-canvas.md` or v1 `validation-canvas.md`), dumps every implicit belief categorized into desirability / viability / feasibility (Christensen), ranks them on a 3×3 risk × impact matrix, picks Top 3 from the high-impact corner, rewrites each as a falsifiable hypothesis ("We believe X. We'll know this is true if [measurable outcome] within [time]"), matches each to the cheapest test method (5-interview rule, landing page, fake-door, concierge MVP, Wizard of Oz, pre-sale, smoke test, or expert interview), and ships `docs/rat/assumption-test-plan.md` (canonical) plus `docs/rat/test-matrix.html` (interactive — drag to re-rank, click to expand, color-coded by category, prints cleanly).

**Reach for it when.** You have beliefs in your canvas but no proof. You need to know what to test first, with the cheapest experiment that could actually falsify it. Investors and advisors keep asking "what have you validated?" and you don't have a structured answer. Or: a previous test invalidated something — re-invoke this skill in update mode to revise the plan and pick the next top 3.

**Pairs well with.**
- [`validation-canvas`](#validation-canvas) — required upstream (medium gate). Loop-back target when hypotheses invalidate.
- [`pitch-deck`](#pitch-deck) — downstream (heavy gate). Pitch refuses to ship without populated `## Results` for top-3 hypotheses.
- [`startup-grill`](#startup-grill) — last step. Reads Results to check for iteration evidence.
- [`team-composer`](#team-composer) — discussion-grade alternative for multi-role validation strategy.

**Try it.**
- "I just shipped my validation canvas — what should I test first?"
- "Design a fake-door test for my new auto-AP feature."
- "My pre-sale failed — only 1 of 15 paid. Update my test plan and route me back to the canvas."

---

<a id="pitch-deck"></a>

### <img src="assets/icons/pitch-deck.svg" alt="" width="48" align="middle"/> &nbsp;`pitch-deck`

**What it does.** Runs a structured narrative interview across the 10-slide investor arc (Title → Problem → Solution → Market → Product → Business Model → Traction → Team → Competition → Ask) and ships three files: a single self-contained HTML deck (Reveal.js inlined, keyboard nav, AAA contrast, `?print-pdf` produces a clean slide-per-page PDF), speaker notes per slide, and a pre-send checklist. Refuses to ship with any of the four cardinal sins unfilled: TAM-only sizing, traction without a time axis, teamless team, vague ask.

**Reach for it when.** An investor said "send me your deck" and you need a shippable v1 this week with the actual content filled in — not a template waiting to be filled later.

**Pairs well with.**
- [`validation-canvas`](#validation-canvas) — two steps upstream. Reads the validation canvas (`docs/canvas/validation-canvas.md` or v1 `validation-canvas.md`) to seed slides 2/3/6 and cross-check the Ask.
- [`riskiest-assumption-test`](#riskiest-assumption-test) — required direct upstream (heavy gate). Reads the assumption-test plan (`docs/rat/assumption-test-plan.md` or v1 `rat/assumption-test-plan.md`) Top 3 + Results to inform the Validation slide and Traction claims; refuses to ship a clean deck without populated Results (override: `[PRE-VALIDATION DRAFT]` watermark).
- [`brand-workshop`](#brand-workshop) — reads the brand design system (`docs/brand/DESIGN.md`) for visuals.
- [`team-composer`](#team-composer) — when a slide claim is weak, spin up `@startup_strategist + @vc_partner + @senior_copywriter` to pressure-test it before shipping.
- [`startup-grill`](#startup-grill) — after this skill ships, run the grill to probe the deck adversarially before it lands in an investor's inbox.

**Try it.**
- "Investor wants my seed deck by Friday — start the structured interview."
- "Use the validation canvas and assumption-test plan to build the deck; refuse to ship with any cardinal sin."
- "I haven't tested anything yet but I want to see what the deck would look like — pre-validation draft mode."

---

<a id="startup-grill"></a>

### <img src="assets/icons/startup-grill.svg" alt="" width="48" align="middle"/> &nbsp;`startup-grill`

**What it does.** Adversarially probes a startup idea with a panel of domain-aware grillers — `@vc_partner`, `@growth_marketer`, `@startup_strategist`, `@ux_researcher`, plus a flexible fifth seat (`@senior_software_architect` for technical-execution-dominant startups, `@brand_strategist` for consumer-brand-dominant ones), plus 0–3 specialists injected from signals (legal, security, clinical, AI safety, game design, etc.). Runs three rounds — probe → forced steelman defense → verdict — and ships a structured kill report ranked across two axes: severity (lethal vs material) and fixability (fixable vs unfixable). Verdict label is one of four canonical labels: `Investable as-is`, `Investable with conditions`, `Pivot signal`, `Pass`. Refuses to ship a soft report — Round 1 must surface at least one lethal read or re-run with sharpened posture. Optional interactive defense mode lets the founder pick a weakness, bring new evidence, and have the relevant 1–2 panelists re-probe that line item only.

**Reach for it when.** You have a startup idea, deck, or business model and want it probed adversarially before you commit time, money, or a fundraise. You want a verdict you can act on, not "thoughts to consider." You want the lethal weakness named declaratively, with a falsifier attached, so you know exactly what evidence to bring.

**Pairs well with.**
- [`validation-canvas`](#validation-canvas) — upstream input. The Stress Tests section + un-relieved VPC Pains are direct grilling ammunition.
- [`riskiest-assumption-test`](#riskiest-assumption-test) — upstream input. The iteration-evidence check (`## Iteration Evidence` section in the kill report, added v2.0.0) yellow-flags pristine pipelines where the canvas wasn't updated after RAT testing.
- [`pitch-deck`](#pitch-deck) — upstream input. The deck's required-slot answers become starting probes.
- [`brand-workshop`](#brand-workshop) — upstream input when slot 5 = `@brand_strategist`; the panel reads `brand-brief.md`'s Positioning section.
- [`team-composer`](#team-composer) — instead of this skill when the user wants brainstorming or constructive review. After this skill when the kill report's `Suggested attack` lines need a multi-role workshop.
- [`skill-evaluator`](#skill-evaluator) — audit the verdict-vs-body consistency rule, the no-lethal-skip rule, the interactive-invitation rule.

**Try it.**
- "Grill my startup idea: a B2B SaaS for accounting firms — pre-seed, $4k MRR, two co-founders. What would kill us?"
- "I have the validation canvas, assumption-test plan, and pitch deck ready — run the grill with the deck as primary input."
- "Defending L1. We have a 6-month cohort retention curve at 87% logo retention. Re-probe."

---

<a id="startup-launch-kit"></a>

### <img src="assets/icons/startup-launch-kit.svg" alt="" width="48" align="middle"/> &nbsp;`startup-launch-kit`

**What it does.** Opt-in umbrella orchestrator that sequences the five-step startup pipeline (`brand-workshop` → `validation-canvas` → `riskiest-assumption-test` → `pitch-deck` → `startup-grill`) with shared state via `kit-manifest.json` at `docs/startup-kit/kit-manifest.json` (a thin JSON state journal: completed steps with mtimes, gate-override flags with reason+timestamp, founder-intake-answers cache, atomic writes). Calls each pipeline skill via the Skill tool — every skill runs as itself, surfaces its own prompts, ships its own artifacts under `docs/startup-kit/<skill>/`. The orchestrator manages the manifest, enforces gate transitions, and surfaces loop-back recommendations after RAT or grill (founder decides; never auto-routes). The 3-question intake fires once at orchestrator level; downstream skills read the cache and offer to confirm/update.

**Reach for it when.** You're starting a new idea from scratch and want end-to-end coordination through the whole pipeline; you're resuming a prior orchestrated session (manifest exists); or you ran a few steps manually and want to absorb them into an orchestrated resume.

**Hard constraints (preserved from v2.0.0 philosophy).** Every individual pipeline skill remains independently invocable — the orchestrator depends on the skills, the skills do not depend on the orchestrator. Gates are never silently bypassed (overrides require explicit founder reason ≥ 20 chars + acknowledgment, recorded in `gate_overrides[]`, surfaced in `startup-grill`'s `## Iteration Evidence` section). No batching — every step's prompts go to the founder. Loop-back is founder-driven; the orchestrator surfaces recommendations, never routes.

**Pairs well with.**
- All five pipeline skills above — the orchestrator calls them in order. Use them directly for any single-step or partial-pipeline work.
- [`team-composer`](#team-composer) — alternative for pipeline-strategy discussions, single-block deep dives, or work that doesn't fit the pipeline shape.

**Try it.**
- "Build my whole startup kit for [idea] — take me through everything."
- "I ran brand-workshop and validation-canvas manually last week. Pick up where I left off."
- "I want to ship a pre-validation draft of the deck for an advisor meeting Friday — record the override and proceed."

---

<a id="gtm"></a>

### <img src="assets/icons/gtm.svg" alt="" width="48" align="middle"/> &nbsp;`gtm` &nbsp;🚧&nbsp;**BETA**

> **Beta — read before relying on it.** Iteration-1 evals scored 100% with-skill (24/24 assertions) vs 27.8% baseline (7/24, +72pp), but those validate *structural* reliability — config files, helper-function pattern, handoff event vocabulary. They do **not** validate real founder workflows on a real startup project; that dogfooding is the next milestone. Breaking changes possible before v1. Treat outputs as drafts to review, not artifacts to ship.

**What it does.** Phased go-to-market for startup products — the sixth step in the startup pipeline, after `startup-grill`. Builds a GTM playbook from upstream artifacts (`validation-canvas.md`, `pitch-deck` content, `brand-workshop` `DESIGN.md`), produces multi-channel content via fan-out (X, TikTok, Reddit, blog/SEO, email, community/Discord), schedules cadenced tasks via the `schedule` skill (daily metrics pull, daily/weekly digests, 6-hour budget check), enforces compliance gates (CAN-SPAM, GDPR, FTC, COPPA, platform TOS), and emits structured handoff events (`lead.captured`, `content.needs_eng`, `crisis.detected`, etc.) to `.workspace/events/` so future workers (support, sales, eng) can plug in cleanly.

**One-way trust ramp — P1 → P2 → P3.** P1 ships read-only playbook + content drafts (no external API calls). P2 adds scheduled execution with state and digests. P3 adds autonomous-with-escalation once MCPs are configured. Skipping levels is a configured refusal — empirically, founders who skip the ramp burn an account, reputation, or several thousand dollars in ad spend within the first week.

**Architectural kill switch — never prompt-only.** `.gtm/HALT` file checked by a `require_active()` helper-function wrapper before every external action. Three layers (HALT file → `state.json` status → harness-killable schedule via the `schedule` skill). Honest about best-effort enforcement in a Claude harness — see `references/kill-switch-pattern.md`.

**Marketing skill orchestration with inline fallback.** When the `marketing:*` plugin is installed (default in Claude Cowork/Code), `gtm` dispatches per-channel content production via [`sub-agent-coordinator`](#sub-agent-coordinator). When not installed, falls back to inline prompts — lower quality, still functional. See `references/marketing-fallback.md`.

**Reach for it when.** The pitch deck is locked and you need to actually get users. You want multi-channel content with state, voice fidelity, compliance gates, and a kill switch you can trust. You have upstream artifacts (`validation-canvas.md`, `DESIGN.md`, pitch deck) and want them to flow into the next step automatically.

**Pairs well with.**
- [`brand-workshop`](#brand-workshop) — upstream input. `gtm` reads `DESIGN.md` for brand voice tokens. Wizard offers to invoke `brand-workshop` if no brand artifact exists.
- [`validation-canvas`](#validation-canvas) — upstream input. `gtm` reads ICP, positioning, channels, and Stress Tests for the playbook.
- [`pitch-deck`](#pitch-deck) — upstream input. `gtm` reads positioning and messaging from the deck content.
- [`startup-grill`](#startup-grill) — adjacent. After `gtm` ships its P1 playbook, the founder may grill it for blind spots before promoting to P2.
- [`sub-agent-coordinator`](#sub-agent-coordinator) — hard dispatch target. Multi-channel content fan-out runs through its patterns.
- [`i18n-contextual-rewriting`](#i18n-contextual-rewriting) — hard dispatch target. Non-English content drafts route through this skill for cultural adaptation.
- [`tech-stack-recommendations`](#tech-stack-recommendations) — when `gtm` emits a `content.needs_eng` event for a landing page and the founder has no chosen stack.

**Try it.**
- "My pitch deck is ready and I want to start getting users — set up GTM for this project."
- "kick off go-to-market for invoicy.app — B2C, US-only for now, freelance designer audience."
- "halt all my marketing automations right now — there's a PR fire on TikTok. Then later, walk me through how to resume safely."

---

## Design principles

These aren't rules for contributors — they're the taste I'm trying to keep on the shelf.

- **One job per skill.** Each skill on the shelf has a tight, named scope. A skill that tries to do five things does none of them well — so the bundle stays wide while each skill stays narrow.
- **Rules must land, not just exist.** A skill is a prompt dressed as policy. If the rules don't survive realistic prompts, the skill is decoration. Every skill here either has evals, or gets audited by one that does.
- **Boring and readable beats clever.** Skill text is read by humans and followed by models. Opaque indirection costs more than it saves.
- **Risk-blocking roles and checks are non-droppable.** Where a skill has explicit safety or compliance triggers, they're vetoes — not tiebreakers, not suggestions.
- **Narrow scope, named boundaries.** Every skill states what it *doesn't* do and when to reach for a different skill instead. Overlap is negotiated up front, not resolved mid-output.
- **Delegate to Anthropic's official shelf.** Where an Anthropic-shipped skill (`theme-factory`, `docx`, `pptx`, `canvas-design`, `skill-creator`, `web-artifacts-builder`, `mcp-builder`, `pdf`, `doc-coauthoring`) owns a primitive better than we do, we reference it rather than rebuild. Each SKILL.md spells out the hand-offs in its Cross-Skill Integration table.

## Status

`3.4.0` is the current release. Adds the **`gtm`** skill in **🚧 BETA** — sixth step in the startup pipeline, covering the missing post-pipeline step (actually getting users) after `startup-grill`. Iteration-1 evals scored 100% with-skill vs 27.8% baseline (+72pp across three test cases: first-run-with-artifacts, cold-start, kill-switch). Those evals validate structural reliability — config files, helper-function kill switch, handoff event vocabulary — but do **not** validate real founder workflows; that dogfooding is the next milestone before graduating to v1. Breaking changes possible before then.

Earlier in v3.2.0: refined the `handshake` skill following its pre-shipment audit — description triggers widened on three new phrases (`"tune in to me"`, `"set a working agreement"`, `"share my preferences"`) and narrowed via an explicit negative gate against codebase orientation, performance-review calibration, and content gathering. Two body fixes added (Phase 0 transition rule + Phase 1 voice rule).

Earlier in v3.1.0: added the `handshake` skill — a brief, opt-in collaboration calibration ritual that runs before the real work (slash-command-only at v1, two-mode design with core calibration + optional project overlay, hard never-ask list, single-user contract, capability-gated integration with the existing two-tier memory store).

Earlier in v3.0.0: `brand-workshop`'s starter design-system output migrated to the [Google Labs `DESIGN.md` format](https://github.com/google-labs-code/design.md) (alpha spec). The downstream startup-pipeline skills (`validation-canvas`, `riskiest-assumption-test`, `pitch-deck`) now read tokens directly from `colors.primary` in the YAML front matter. See [CHANGELOG.md](CHANGELOG.md) for full v3.4.0 + v3.2.0 + v3.1.0 + v3.0.0 entries and migration notes.

- **Primary target agent** — Claude (Claude Code, Cowork).
- **Other agents** — may come later, no promises yet.
- **Stability** — the skills I ship here I use myself; if one stops earning its place, it gets removed rather than left to rot.

## Feedback

Issues and suggestions are welcome via [GitHub](https://github.com/sorawit-w/agent-skills/issues). Not accepting code contributions right now — feel free to fork.

## License

MIT. See [LICENSE](LICENSE).
