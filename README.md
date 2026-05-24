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

- **What this is** — a single Claude Code plugin that installs a curated shelf of nineteen specialized skills in one go.
- **Who it's for** — anyone using Claude Code or Cowork who wants auto-triggering expertise for a specific job: founders pitching investors, PMs brainstorming with a team, engineers writing or auditing a skill, localizers rewriting inside cultural reality, founders who want their startup adversarially probed, anyone who wants the agent to know how *they* prefer to collaborate before the work starts, and anyone who wants to load one author's opinionated coding-discipline preamble at session start (read the caveat first).
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
| <img src="assets/icons/wear-the-hat.svg" alt="" width="64" align="middle"/> | [`wear-the-hat`](#wear-the-hat) | Pick one role from `team-composer`'s catalog and do the work in their voice — solo embodiment, no panel discussion. Auto-picks when you don't name a role; hands off to `team-composer` for multi-role tasks. | You want a specific lens (`@security_specialist`, `@dataviz_engineer`, `@accessibility_specialist`) applied to a task without convening a full panel. |
| <img src="assets/icons/skill-evaluator.svg" alt="" width="64" align="middle"/> | [`skill-evaluator`](#skill-evaluator) | Audit a skill to see whether its rules actually land when Claude runs it. | You just wrote a skill, or one has been "mostly working" and you suspect a rule is being skipped. |
| <img src="assets/icons/tech-stack-recommendations.svg" alt="" width="64" align="middle"/> | [`tech-stack-recommendations`](#tech-stack-recommendations) | Opinionated default TS/JS stack (Bun + SvelteKit + Elysia + Neon + Drizzle + Clerk), plus named alternates. | You're starting a new project, or picking one layer, and want a default instead of a neutral grid. |
| <img src="assets/icons/handshake.svg" alt="" width="64" align="middle"/> | [`handshake`](#handshake) | A brief opt-in calibration ritual that shows you what's on file, then asks ≤4 high-leverage collaboration questions (and optionally ≤6 scoped project questions). Writes to the existing memory store. | You want the agent to know *how* you prefer to collaborate before it starts giving generic answers, or you want a transparent moment to see and correct what's been captured about you. |
| <img src="assets/icons/whoami.svg" alt="" width="64" align="middle"/> | [`whoami`](#whoami) | A short conversational interview that profiles how you want to be collaborated with — six dials, an RPG class, a portable profile, and a self-contained HTML character sheet. | You want the agent to know who you are and how you work — broadly, across projects — or you're new to AI / switching vendors and want a profile you can carry. |
| <img src="assets/icons/coding-rules.svg" alt="" width="64" align="middle"/> | [`coding-rules`](#coding-rules) **⚠️ OPINIONATED** | Loads one author's operating system for agentic coding into the session — branching, commit cadence, verification gates, sub-agent triggers, ambiguity-before-cost, plus a per-project install for vendor agent-instruction files. | You've read `BOOTSTRAP.md` end-to-end, the rules match your taste (or you've forked them), and you want them to load reliably across sessions. **Not a neutral best-practice guide — fork before adopting if your judgment differs.** |
| <img src="assets/icons/i18n-contextual-rewriting.svg" alt="" width="64" align="middle"/> | [`i18n-contextual-rewriting`](#i18n-contextual-rewriting) | Surgical edits on large translation files, plus a role-based review that turns "translate" into cultural rewriting. | You're editing a big i18n file without blowing token limits, or producing translations that shouldn't read as machine-converted English. |
| <img src="assets/icons/brand-workshop.svg" alt="" width="64" align="middle"/> | [`brand-workshop`](#brand-workshop) | Run a Discovery → Concept → Creation workshop and ship a brand strategy brief, tagline, and code-generated logo. | You need a real identity package for a product, app, or startup — not just a logo doodle. |
| <img src="assets/icons/validation-canvas.svg" alt="" width="64" align="middle"/> | [`validation-canvas`](#validation-canvas) | Interview a founder block-by-block and produce a rigorous Lean Canvas + Value Proposition Canvas with explicit Stress Tests. Adapts to founder experience via 3-question intake. | You need a beliefs artifact that holds up to scrutiny — *what do we believe?* — before designing tests, building the deck, or pitching. |
| <img src="assets/icons/riskiest-assumption-test.svg" alt="" width="64" align="middle"/> | [`riskiest-assumption-test`](#riskiest-assumption-test) | Convert canvas Stress Tests into falsifiable hypotheses with success/kill criteria and chosen test methods. Ships a 1-page test plan + interactive risk × impact matrix. | You have beliefs in your canvas and need to know *what to test first*, with the cheapest experiment that could falsify it. |
| <img src="assets/icons/pitch-deck.svg" alt="" width="64" align="middle"/> | [`pitch-deck`](#pitch-deck) | Structured narrative interview across the 10-slide investor arc; ships a self-contained HTML deck + speaker notes. Heavy gate on `riskiest-assumption-test` results. | An investor said "send me your deck" and you've already validated your top assumptions — now you need a shippable v1 this week. |
| <img src="assets/icons/startup-grill.svg" alt="" width="64" align="middle"/> | [`startup-grill`](#startup-grill) | Adversarially probe a startup with a panel of domain-aware grillers; ship a kill report ranked by severity × fixability with optional interactive defense. Includes an iteration-evidence check. | You want your idea / deck / canvas probed for what would actually kill it — not "thoughts to consider," a verdict you can act on. |
| <img src="assets/icons/startup-launch-kit.svg" alt="" width="64" align="middle"/> | [`startup-launch-kit`](#startup-launch-kit) | Opt-in umbrella orchestrator that sequences the five-step startup pipeline (brand → canvas → tests → pitch → grill) with shared state via `docs/startup-kit/kit-manifest.json`. Never bypasses gates; every individual skill stays independently invocable. | You're starting a new idea from scratch and want end-to-end coordination, OR you ran a few steps manually and want to absorb them into an orchestrated resume. |
| <img src="assets/icons/gtm.svg" alt="" width="64" align="middle"/> | [`gtm`](#gtm) **🚧 BETA** | Phased go-to-market for startup products. Builds a GTM playbook from upstream artifacts, produces multi-channel content, schedules cadenced tasks, enforces compliance, emits handoff events. Trust ramp P1 → P2 → P3. Project-local `.gtm/`. Architectural kill switch via HALT file. | The pitch deck is locked and you need to actually get users — multi-channel marketing motion with state, scheduling, compliance gates, and a kill switch you can trust. **Beta** — evals are structural-only; not yet dogfooded on a real founder workflow. |
| <img src="assets/icons/ai-ux-review.svg" alt="" width="64" align="middle"/> | [`ai-ux-review`](#ai-ux-review) | Design-completeness review for AI products. Seven blocks (necessity → mental model → trust → feedback → errors → output integrity → success), six cross-block checks, explicit `[Gap — …]` markers. Ships MD + self-contained HTML. | You're about to ship an AI feature (or already did) and want a structured pre-launch review — not a vibe check, a forced walk through the decisions that quietly get skipped. Especially the gen-AI integrity surface (hallucination, provenance, prompt injection, agent autonomy). |
| <img src="assets/icons/ai-eval-review.svg" alt="" width="64" align="middle"/> | [`ai-eval-review`](#ai-eval-review) | Eval-design-completeness review for AI products — sibling to `ai-ux-review`. Seven blocks (necessity & success → ground truth → offline eval → online metrics → cohorts + disparate impact → adversarial + robustness → drift + monitoring), six cross-block checks plus regulatory lens. Ships MD + self-contained HTML. | You want a structured eval review for an AI product — not "we ran some tests," a forced walk through ground-truth quality, cohort breakdown, adversarial coverage, and drift detection. Especially when `ai-ux-review` Block 7 surfaced eval gaps that need to be made concrete. |
| <img src="assets/icons/pixel-art.svg" alt="" width="64" align="middle"/> | [`pixel-art`](#pixel-art) **🚧 BETA** | A pocket-sized hi-density pixel-art studio with a built-in design system (palette tokens, density specs, composition rules, font catalog, anti-pattern checklist). Two style modes — `hi-fi` (painterly hi-density) and `lo-fi` (scanlined warm-paper banner). Model-agnostic prompts route to any connected image-gen MCP (Z-image, Imagen, OpenAI Image, Midjourney, SDXL) or emit a copy-pasteable prompt brief. Title cards get a portable SVG path using VT323 by default. | You want hi-density pixel art (scenes, characters, buildings, nature, title cards) without re-specifying palette / density / composition / typography on every prompt — and you want it to work whether you have an image-gen MCP connected or not. |

Each skill lives under [`skills/`](skills/) with its own `README.md`, `SKILL.md`, and reference docs.

This repo treats skill authoring as **harness engineering** — designing the context, scaffolding, feedback loops, state, and eval discipline *around* an agent so it can do reliable work. See [`CLAUDE.md`](CLAUDE.md) → "Harness vocabulary" for the five primitives and where each shows up in the shelf.

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
- [`wear-the-hat`](#wear-the-hat) — when the task wants ONE specific lens applied, not a multi-role panel discussion. Inverse use case from this skill.
- [`skill-evaluator`](#skill-evaluator) — audit team-composer (or any team-driven skill) for rules that get quietly skipped.
- [`tech-stack-recommendations`](#tech-stack-recommendations) — when the architect role needs an opinionated stack to anchor the debate.
- [`i18n-contextual-rewriting`](#i18n-contextual-rewriting) — when the `@i18n_specialist` is on the team and the output needs to ship in multiple locales.
- [`ai-ux-review`](#ai-ux-review) / [`ai-eval-review`](#ai-eval-review) — discussion-grade alternative inverse. Use `team-composer` with `@ux_researcher` + `@ai_safety_specialist` (or `@data_scientist` + `@ai_safety_specialist` for eval) when you want a *narrow one-block discussion* rather than a full structured review artifact. Use the dedicated review skills when you want the persistent MD + HTML output.

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
- [`wear-the-hat`](#wear-the-hat) — sub-agent mode hands off a brief with `Role:` tag and persona context baked in; this skill's spawning protocol owns the rest.
- [`skill-evaluator`](#skill-evaluator) — spawn evaluator sub-agents to stress-test other skills in parallel.

**Try it.**
- "Refactor all 14 React components from class to function — coordinate in parallel."
- "Debug our flaky CI suite: spawn a researcher, a fixer, and a reviewer with clear briefs."
- "After `team-composer` concludes, brief sub-agents to produce the per-role deliverables the conclusion assigned."

---

<a id="wear-the-hat"></a>

### <img src="assets/icons/wear-the-hat.svg" alt="" width="48" align="middle"/> &nbsp;`wear-the-hat`

**What it does.** Triggers on deliberate role-lens signals (explicit `@role` tags, embodiment phrases like "act as" or "wear the hat of", lens framings like "from the X perspective"), picks one role (explicit if named, auto-picked via a small keyword/verb table otherwise), loads only perspective + signature phrases from `team-composer`'s catalog (NOT the role's blind spots or biases), and executes the work — inline for short analytical responses, sub-agent mode for tasks hitting `sub-agent-coordinator`'s spawning signals. Four-outcome auto-pick: clean match, multi-candidate (asks user), multi-role task (offers `team-composer` handoff with explicit confirmation, never silent), or fallback default. Catalog stays in `team-composer/references/role-personas.md` — no parallel taxonomy.

**Reach for it when.** You want one specific lens on a task — `@security_specialist` for an auth audit, `@dataviz_engineer` for a chart spec, `@accessibility_specialist` for a UI — without the panel ceremony of `team-composer`. Or you want a brief produced for a sub-agent with persona context baked in before handing off to `sub-agent-coordinator`.

**Pairs well with.**
- [`team-composer`](#team-composer) — owns the role catalog (`role-personas.md`). `wear-the-hat` consumes it. Multi-role tasks route here with explicit user confirmation.
- [`sub-agent-coordinator`](#sub-agent-coordinator) — sub-agent mode produces a brief with `Role:` tag and persona context, then hands off to coordinator's protocol; no duplicate spawning logic.
- [`coding-rules`](#coding-rules) — coding-task role embodiment composes naturally: `coding-rules` sets the engineering discipline; `wear-the-hat` applies the lens.
- [`brand-workshop`](#brand-workshop) — pure brand-identity packages route to `brand-workshop`; `wear-the-hat` redirects.

**Try it.**
- "Audit `middleware/auth.ts` for missing CSRF guards as `@security_specialist`."
- "Act as a data-viz engineer and review this chart spec."
- "Wear the hat of the accessibility specialist for this UI review."

---

<a id="skill-evaluator"></a>

### <img src="assets/icons/skill-evaluator.svg" alt="" width="48" align="middle"/> &nbsp;`skill-evaluator`

**What it does.** Reads a target skill end-to-end (`SKILL.md` plus every referenced file), generates test prompts spanning happy paths, trigger edges, and rule-specific stress tests, then grades outputs against the rules — without letting the grader peek at the skill text. Classifies failures by fix layer (skill text / rubric / brief / fixture) and proposes targeted rule-text diffs.

**Reach for it when.** You just wrote a skill and want to stress-test it, or a skill has been "mostly working" and you suspect a rule is being quietly skipped. Also useful for vetting someone else's skill before you install it.

**Heads up — token-hungry by design.** The split-role harness (executor + grader sub-agents, fresh context per test, no skill-text access for the grader) is what makes the findings independent. A 5-test run is ~10 sub-agent invocations plus a Phase 1 read pass through every reference file the target skill cites; 10 prompts with opt-in high-stakes mode (second-grader quorum) runs ~30. For a single-section rule edit, in-context adversarial review by the author surfaces ~80–90% of the value at ~10% of the cost — the skill's own README names when the full harness is worth it.

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

<a id="whoami"></a>

### <img src="assets/icons/whoami.svg" alt="" width="48" align="middle"/> &nbsp;`whoami`

**What it does.** Runs a short, conversational interview — review what's known → background questions → optional MBTI fast-path → gamified scenario questions — that scores six bipolar collaboration dials (Initiative, Depth, Breadth, Rationale, Warmth, Challenge) and converges memory, MBTI, and answers onto those six numbers. Derives an RPG-style class + subclass from a 12-class taxonomy (6 axes × 2 poles). Writes a portable `whoami-profile.md` source-of-truth file plus a runtime `user`-type memory entry, keeps dated snapshots, and emits a self-contained HTML character sheet (diverging-lollipop dials, trait meters, class card + portrait). Bare `/whoami` on an existing profile shows what's on file and offers correct / re-run / leave it; `/whoami rerun` re-runs the interview.

**Reach for it when.** You want the agent to know who you are and how you prefer to work — broadly, not project-scoped. You're new to AI tools, or switching agent vendors and want a profile you can carry over. You want tailored responses without re-explaining yourself each session — or you just want your collaboration character sheet.

**Pairs well with.**
- [`handshake`](#handshake) — sibling. `whoami` is the broad person-level profile; `handshake` calibrates one project and pre-fills its core questions from the whoami profile. `whoami` is upstream and one-directional.
- [`pixel-art`](#pixel-art) — `whoami` calls it (if an image generator is available) to generate the class character portrait; falls back to a bundled hi-density pixel-art PNG.
- `productivity:memory-management` *(if installed)* — `whoami` writes its profile as a standard `user`-type memory; capability-gated, defers to the runtime's memory conventions.

**Try it.**
- "Run `/whoami` — I want you to actually know how I like to work."
- "I just switched from another AI tool — here's my profile file, set me up."
- "`/whoami rerun` — my role changed and the profile's out of date."

---

<a id="coding-rules"></a>

### <img src="assets/icons/coding-rules.svg" alt="" width="48" align="middle"/> &nbsp;`coding-rules` &nbsp;⚠️&nbsp;**OPINIONATED**

> **Read this before installing.** This skill is **deliberately, aggressively opinionated.** It captures *one author's* personal taste and loads on every session that uses it (real input-token cost). It is **not** a neutral best-practice guide. Read [`resources/BOOTSTRAP.md`](skills/coding-rules/resources/BOOTSTRAP.md) end-to-end before adopting; **fork, edit, or skip rules that don't fit your taste**. The skill provides a frame; your judgment is what makes it useful.

**What it does.** Loads `resources/BOOTSTRAP.md` into the current session via the `Read` tool — Prime Directive (clarity over cleverness, safety over speed, never leave the repo broken), workflow routing by task type (`new-project` / `feature` / `bugfix` / `quick-task`), hard rules that apply on every task (branching, commit cadence, verification with fresh evidence, resource cleanup, manual-verification instructions, sub-agent delegation triggers, ambiguity-before-cost), and a reference index for the long tail. Five sub-commands via the `args` parameter: `load` (default), `reload` (re-inject BOOTSTRAP after compaction), `status` (check whether markers are present), `install` (two phases, both opt-in: Phase 1 appends one instruction line to your `CLAUDE.md` / `AGENTS.md` / `AI-CONTEXT.md` / `.cursorrules` with per-file confirmation; Phase 2 optionally registers six PreToolUse / SessionStart guardrail hooks in your chosen settings file — `~/.claude/settings.json`, project `.claude/settings.json`, or project `.claude/settings.local.json` — with a single full-diff confirmation), `uninstall` (mirror, both phases). **Activation stays skill-scoped — never plugin-wide.** No `hooks` field in the parent plugin's `plugin.json`; users who installed for a different skill never silently inherit these guardrails.

**Reach for it when.** You've read `BOOTSTRAP.md` end-to-end, the rules match your taste (or you've forked them), and you want them to load reliably across sessions in a project. You also want compaction-safety — long sessions can strip earlier context, and `args: status` + `args: reload` is the recovery path. **Don't reach for it** if you haven't read the rules, your team's conventions conflict (e.g., commit batching, work-on-`main`), or you want a neutral preamble — try a more general guide instead.

**Pairs well with.**
- [`skill-evaluator`](#skill-evaluator) — for evaluating rule changes. The skill's own `CLAUDE.md` enforces "no inline grading" — rule audits route to a fresh-context split-role harness to remove author bias.
- [`wear-the-hat`](#wear-the-hat) — coding-task role embodiment composes naturally: this skill sets the engineering discipline; `wear-the-hat` applies the specific lens (`@security_specialist`, `@dataviz_engineer`, etc.) for the task at hand.
- Project-local `CLAUDE.md` / `AGENTS.md` — per BOOTSTRAP's priority order (User > Project config > Agent context > Playbook), the project's own instructions always win over rules in this skill.
- `superpowers:*` *(if installed)* — overlap exists (TDD, brainstorming, verification-before-completion). Explicit user invocations win; otherwise this skill's BOOTSTRAP rules are the operating frame.

**Try it.**
- "Use the coding-rules skill to load my rules into this session."
- "Use the coding-rules skill with `args: install` for this project — I want CLAUDE.md to auto-load it."
- "Use the coding-rules skill with `args: status` — I want to check whether the rules are still in context after that long compaction."

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
- [`ai-ux-review`](#ai-ux-review) — for AI-flavored startups, the natural next step after the canvas is settled. This skill reads `validation-canvas.md` if present and skips business-model questions, focusing purely on the human-AI design layer.
- [`ai-eval-review`](#ai-eval-review) — sibling of `ai-ux-review`. When the AI product's eval rigor is the load-bearing question (regulated domain, classification with disparate-impact risk, drift-sensitive deployment), this is the measurement-side review.

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
- [`ai-ux-review`](#ai-ux-review) / [`ai-eval-review`](#ai-eval-review) — composition. When the Gap Summary from either AI-review skill surfaces an *assumption that needs testing* (not just deciding — e.g., "we assume voice-sample-based prompting matches user voice well enough"), hand it here to convert into a falsifiable hypothesis with success / kill criteria.

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

<a id="ai-ux-review"></a>

### <img src="assets/icons/ai-ux-review.svg" alt="" width="48" align="middle"/> &nbsp;`ai-ux-review`

**What it does.** Walks an AI product or feature through seven design-completeness blocks — necessity check (why AI here vs. a deterministic alternative), mental model, trust calibration, feedback + control, errors + graceful failure, output integrity (hallucination, provenance, prompt injection, multi-turn drift, agent autonomy — the gen-AI surface), and success + evaluation. Roles active: `@ux_researcher`, `@ai_safety_specialist`, `@lead_behavioral_scientist`, `@senior_product_designer`, `@senior_product_manager`. Specificity gate rejects category answers; gaps are first-class outputs marked `[Gap — …]`. Six mandatory cross-block checks. Ships `ai-ux-review.md` + a self-contained `ai-ux-review.html` (3+3+1 card grid with `[GAP]` chips, Gap Summary footer). Reads `validation-canvas.md` if present and skips business-model questions; reads `<brand-root>/DESIGN.md` for tokens.

**Reach for it when.** You're about to ship an AI feature and want a structured pre-launch design review — or you already shipped, and fluent-but-wrong outputs are surfacing. Especially when you suspect the output-integrity surface (hallucination, provenance, prompt injection, agent autonomy) was underdesigned. Or when a cofounder asked "how do we know this is responsible AI?" and the answer isn't yet structured enough to defend.

**Pairs well with.**
- [`validation-canvas`](#validation-canvas) — upstream for AI startups. When present, this skill skips business-model questions and audits UX execution only.
- [`brand-workshop`](#brand-workshop) — upstream when a brand identity exists. This skill reads `DESIGN.md` to style the HTML output.
- [`team-composer`](#team-composer) — alternative when the request is one narrow block (e.g., "let's debate trust calibration") rather than a full review. Discussion-grade, no artifact.
- [`riskiest-assumption-test`](#riskiest-assumption-test) — composition. If the Gap Summary surfaces design assumptions that need *testing* (not just deciding), hand the gaps to RAT.
- [`startup-grill`](#startup-grill) — adjacent. Adversarial pre-mortem with a verdict. Different mode from this skill's cooperative gap detection.

**Try it.**
- "Review the UX of our LLM email-draft feature before launch — focus on trust and output integrity."
- "We just shipped an agentic feature and fluent-but-wrong outputs are surfacing. Walk us through the review."
- "Review the AI feature in our app — `validation-canvas.md` is already in `docs/canvas/`; skip the business-model questions and audit the UX layer."

---

<a id="ai-eval-review"></a>

### <img src="assets/icons/ai-eval-review.svg" alt="" width="48" align="middle"/> &nbsp;`ai-eval-review`

**What it does.** Walks the **eval layer** of an AI product through seven design-completeness blocks — necessity & success definition (what does "good enough to ship" mean, what's the offline criterion), ground truth & label quality (where do labels come from, inter-annotator agreement, coverage gaps), offline eval design (eval set composition, distribution alignment, leakage protection, statistical power, baseline), online metrics & signal (success-tracking metric, failure signal independent of engagement, counter-metrics, per-cohort visibility), cohort breakdown & disparate impact (per-segment performance, fairness, harm distribution — the responsible-AI block), adversarial & robustness (red-team coverage, prompt injection, OOD, jailbreak resistance, distribution shift), and drift detection & monitoring (model / behavior / data drift, alerting, runbook). Roles active: `@data_scientist`, `@ai_system_architect`, `@ai_safety_specialist`, `@senior_product_manager`, `@legal_compliance_advisor`. Six mandatory cross-block checks plus a regulatory cross-cutting lens (EU AI Act / FDA SaMD / FTC). Specificity gate rejects "we measure accuracy" answers. Ships `ai-eval-review.md` + a self-contained `ai-eval-review.html` (3+3+1 card grid with adversarial-eval table in Block 6, gap chips, Gap Summary footer; teal accent — sibling to `ai-ux-review`'s warm orange). When `ai-ux-review.md` exists, reads its Block 7 (Success & Evaluation) gaps and seeds Block 1 here from them.

**Reach for it when.** You want a structured eval review for an AI product — pre-launch rigor check, post-launch eval gap audit, or follow-up to an `ai-ux-review` run where Block 7 surfaced eval-side gaps. Especially when the team treats labels as solved (Block 2 will surface debt), engagement as the success metric (Block 4's failure-signal check catches this), or aggregate accuracy as enough (Block 5's cohort breakdown surfaces the cases hidden in the mean). Also when regulatory context applies (EU AI Act high-risk, FDA SaMD, FTC-adjacent) and eval rigor needs to be proportional to risk class.

**Pairs well with.**
- [`ai-ux-review`](#ai-ux-review) — **sibling skill.** Same shape, same elicitation pattern, different subject. Run both for a complete AI product review.
- [`validation-canvas`](#validation-canvas) — upstream for AI startups. Block 5 (Cohort breakdown) reads Customer Segments.
- [`brand-workshop`](#brand-workshop) — upstream when a brand exists. HTML output styled from `DESIGN.md`.
- [`team-composer`](#team-composer) — alternative for one-block discussions (e.g., "let's debate ground-truth labeling strategy") rather than a full review artifact.
- [`riskiest-assumption-test`](#riskiest-assumption-test) — composition. Gap Summary entries that are *assumptions about evals* (e.g., "we assume single-annotator labels are accurate enough") become RAT hypotheses.
- [`startup-grill`](#startup-grill) — adjacent. Adversarial pre-mortem with verdict; different mode from this skill's cooperative gap detection.

**Try it.**
- "Review the eval setup for our classification model before launch — push hard on ground truth and cohort breakdown."
- "We have `ai-ux-review.md` with Block 7 gaps for our LLM feature. Walk through the eval review next, seeded from those gaps."
- "Eval review for our medical-imaging classifier — we're FDA SaMD class II, so apply regulatory rigor across Blocks 2, 5, and 6."

---

<a id="pixel-art"></a>

### <img src="assets/icons/pixel-art.svg" alt="" width="48" align="middle"/> &nbsp;`pixel-art` &nbsp;🚧&nbsp;**BETA**

**What it does.** A pocket-sized hi-density pixel-art studio. Takes a short brief — *"medieval harbor at dusk", "tavern interior with fireplace", "Whispers of the Flame title card in VT323"* — and returns either a finished image (when an image-gen MCP is connected) or a copy-pasteable, model-agnostic prompt brief (when none is). The style is encoded once as an internal design system in `references/` — palette tokens (5 hi-fi palettes + lo-fi banner anchors), density specs (pixel density + dithering rules per mode), composition rules (three-layer scenes, eye-line, focal point, light source), six lighting profiles (golden hour, candlelit, twilight, stormy, midday, dawn), a 5-font catalog (VT323 default + Pixelify Sans, Press Start 2P, Silkscreen, DotGothic16), and a 5-marker craft-marker checklist (hue shifts, cluster studies, banding avoidance, painterly mid-tones via dithering, clean edges) — so the user does not have to re-specify any of it on every prompt. Two style modes: `hi-fi` (default, painterly hi-density pixel art) and `lo-fi` (scanlined warm-paper banner aesthetic, matching this repo's banners). Five subject categories: scenes, characters, buildings, nature, title cards. Title cards additionally get a portable SVG path using VT323 with bold + inset-shadow styling — the "Whispers of the Flame" look — that renders without any image generator. IP guardrail mirrors `algorithmic-art` (no living-artist names; original compositions only).

**Reach for it when.** You want hi-density pixel art that is consistent across runs — not "vibey pixel art" that drifts from prompt to prompt. Especially good when: you have a preferred image generator (Z-image, Imagen / Nano Banana, OpenAI Image, Midjourney, SDXL — the prompt structure works in all of them); you want a portable prompt brief you can paste into the generator of your choice with no MCP setup; you need a title card with crisp typography (image models render text inconsistently — the SVG path solves this); or you want the agent-skills banner aesthetic (lo-fi mode) without re-inventing the scanlined-paper background.

**Pairs well with.**
- [`brand-workshop`](#brand-workshop) — logo / identity packages route there. `pixel-art` can produce pixel-art **banners** for a brand, but logos are a different deliverable.
- Anthropic's `algorithmic-art` — sibling skill. Algorithmic art uses p5.js (procedural, seeded); `pixel-art` uses image-gen models + structured prompts. Different toolchain, complementary scope.
- Anthropic's `canvas-design` — sibling skill. Canvas-design ships static raster / PDF via design-philosophy prose; `pixel-art` ships pixel-style raster via design-system tokens.
- [`team-composer`](#team-composer) — when the brief is cross-disciplinary (e.g., game splash + marketing copy), `team-composer` assembles roles and may hand the visual deliverable to `pixel-art`.
- Image-gen MCPs (Z-image Turbo, Imagen, OpenAI Image, etc.) — capability-gated dependency. Skill works without any MCP via the prompt brief; works better with at least one connected.

**Try it.**
- "Create a hi-fi pixel-art medieval harbor at dusk with a lighthouse and three ships."
- "Make a lo-fi pixel-art banner for my project — three-panel, scanlined paper, VT323 title."
- "Title card for 'Whispers of the Flame' in VT323, candlelit palette, bold + inset shadow."

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

`3.14.0` is the current release. Refines **`whoami`** in response to an external 6/10 review and adds a social-share clarity fix to the character sheet. The interview gains an **anti-patterns question** — it now asks what AI assistants most often get wrong and captures 2–3 named failure modes into the portable profile, the runtime memory entry, and the HTML sheet; profile `schema_version` bumps 1 → 2 with an additive `anti_patterns` field (`handshake`'s read contract is unaffected). Core Principle 4 is rewritten from passive ("hold the profile lightly") to **active drift-handling** — when live behavior contradicts a stored dial, follow the live behavior, flag the mismatch, and revise on confirmation. Out-of-scope routing is made explicit in `SKILL.md` and the README: per-task / per-mode calibration and the code definition-of-done go to `handshake` / `coding-rules`, correction-accrual to `feedback`-type memory; the per-mode-profile and chat-mining non-goals are recorded as deliberately declined. The character sheet gains a **header subtitle** ("An AI collaboration profile") and a **footer legend** ("Dials are collaboration preferences, not scores") so a sheet shared on social media isn't misread as a competence scorecard. Pre-shipment `skill-evaluator` audit: 33/33 assertions across 6 tests. MINOR — additive only, no breaking changes.

Earlier in v3.13.1: Replaces `whoami`'s 13 bundled class portraits with **hi-density pixel-art character portraits** — helmed, hooded, hatted, or bare-faced busts with shade ramps, dithered backgrounds, and a class emblem each, in six axis-family designs (high/low variant pairs) plus Wildcard. Each was generated with an AI image model from a reusable per-class prompt spec and ships at 512×512 PNG (~370 KB) so the base64-embedded HTML character sheet stays light. They replace the first release's coarse ~10-rectangle SVG emblems, which are removed — `class-map.md`, `SKILL.md`, and both READMEs now point at `.png`. Also folds in the batched `skill-evaluator` enhancement — a Step 4 in the findings-report Next-steps flow that capability-gates a `skill-creator` description-check handoff. PATCH — no breaking changes.

Earlier in v3.13.0: adds the **`whoami`** skill — a portable collaboration profile that calibrates how the agent works with each user. A short conversational interview scores six bipolar dials (Initiative, Depth, Breadth, Rationale, Warmth, Challenge), converges memory + MBTI + answers onto those six numbers, derives an RPG class + subclass from a 12-class taxonomy (6 axes × 2 poles), writes a portable `whoami-profile.md` + a runtime `user`-type memory entry, keeps dated snapshots, and emits a self-contained HTML character sheet that renders the dials as **diverging lollipops, not a radar** — every dial is bipolar, and a radar misreads a strong low preference as "weak." Sibling to `handshake`, which now reads the whoami profile to pre-fill its core questions. Capability-gated throughout. Ships `SKILL.md` + 8 references + 2 templates + command + README, banners + icon, and 13 default class-character SVGs. English-first MVP; `skill-evaluator` audit (24/24) and `skill-creator` triggering check (16/16) both run, two findings folded in. Additive only — no breaking changes.

Earlier in v3.12.0: adds an **opt-in HTML export** to `coding-rules` — on explicit request, the agent renders a Markdown document as a single self-contained, shareable HTML file (emailable, opens offline, prints to PDF cleanly). Markdown stays the canonical source; the HTML is a point-in-time snapshot written alongside the `.md`, never synced back. Two new files in `skills/coding-rules/resources/` — `references/html-export.md` (the convention: opt-in trigger only, what "self-contained" means, deterministic production via a bundled template, no UI-skill delegation) and `templates/html-export.html.template` (single-file wrapper + default document stylesheet, with `:root` custom properties as the `DESIGN.md` override surface) — plus two small edits wiring it into `BOOTSTRAP.md`'s Reference Index and `references/design-md.md`. Styling defers to `DESIGN.md` when the repo has one, else the bundled default. A mandatory "human docs → HTML" rule was rejected — it would force fuzzy human-vs-agent classification on every document; opt-in deletes the classification. No `SKILL.md` change, no new skill, no new sub-command. Additive only — no breaking changes.

Earlier in v3.11.0: hardens the `coding-rules` workflow boundaries to fix two stacked failure modes — agents over-applying full TDD + build + lint discipline to one-line copy changes (turning 30-second tasks into 5-minute ceremonies), and agents *under*-applying discipline by self-classifying a one-line edit to `auth/middleware.ts`, `migrations/`, `payments/`, or `terraform/` as quick-task because the LOC delta looked small. Five additions across four files in `skills/coding-rules/resources/`, no `SKILL.md` text changes, no new skill. **(1)** `workflows/quick-task.md` grows a hard `<fit_check>` block — no new files, no test logic, no schema/contract/type changes, no high-stakes paths, ≤~50 LOC, strings/copy/comments/config/data only — with a 2–4-line declaration template the agent states before starting. **(2)** A post-implementation `git diff --stat` scope-check in step 3a re-validates the declared fit; mismatch → STOP and escalate to `workflows/feature.md`. Trust-but-verify counterweight to self-classification. **(3)** `BOOTSTRAP.md` §3 adds a high-stakes path override that always routes to `feature.md` regardless of LOC for migrations / auth / payments / infra (Terraform / k8s / Dockerfile) / CI/CD / production-traffic-shaping constants — blast radius isn't bounded by LOC, so the discipline floor can't be either. **(4)** `references/quality-gates.md` adds a Formatter Scope section forbidding repo-wide `prettier --write .` / `eslint --fix .` / `biome check --apply .` / `black .` / `gofmt -w .` invocations; defers to `lint-staged` / `husky` / `pre-commit` / `lefthook` when detected; provides touched-files-only patterns per stack using `git diff --name-only ... | xargs -r` to avoid the zero-arg-means-format-everything trap. **(5)** `references/external-resources.md` adds a Transport reliability paragraph below the JetBrains MCP entry codifying **STDIO** preference for IDE-coupled MCP servers — three reasons (topology match: one server per IDE per developer; `sse` deprecated 2025-03-26 in favor of Streamable HTTP; corporate-network reality of buffered SSE / TLS-intercepted HTTP / idle-timeout drops). Vocabulary stayed deliberately native — no parallel "Tier 0 / 1 / 2" naming was introduced; the existing `quick-task` / `feature` / `bugfix` workflows are the tier system, and this release hardens their boundaries instead of inventing a parallel one. Additive only — no breaking changes.

Earlier in v3.10.2: Adherence patch on `pixel-art` from a pre-shipment `skill-evaluator` audit (4 tests, 17 assertions, 17/17 pass with two coverage gaps flagged) — folds two SKILL.md text findings and formally labels the skill **🚧 BETA**. **Finding A:** SKILL.md verification section said *"at least 4 of 5 craft markers"* while `references/anti-patterns.md` said *"at least 5 of 6"* after v3.10.1 added marker 6 (pixel scale matches the density anchor) — stale-after-patch inconsistency caught by the T1 executor sub-agent, not by the grader rubric. Now reconciled with the reference file authoritative and the SKILL.md mirror paragraph synced. **Finding B:** IP guardrail said *"Never reference a living artist by name"* — leaves deceased artists ambiguous under literal reading (e.g., Eyvind Earle, d. 2000, work still under copyright). Tightened to *"Never reference any specific named artist — living or deceased."* The **🚧 BETA** label mirrors `gtm`'s pattern: structural smoke-tests pass on the routing rule and IP guardrail and craft-marker discipline, but the skill has not yet been dogfooded across multiple subject categories (scenes-only smoke), multiple generators (Z-image only), or reference-image-supplied briefs. Pass-rate without coverage context is misleading — that's the framing `skill-evaluator`'s output enforces and v3.10.2 operationalizes. Coverage gaps left for a future round: author/auditor bias, untested Path-B-only-when-no-MCP, untested style-mode ambiguity, untested lo-fi generation, untested multi-MCP routing, untested reference-image briefs.

Earlier in v3.10.1: Adherence patch on the new `pixel-art` skill, folding in findings from the first end-to-end smoke test (medieval harbor at dusk via Z-image Turbo). The smoke test surfaced a real routing gap: Z-image scored 5/5 on the original craft-marker checklist while still failing the user's actual density target — Z-image caps at moderate density (Stardew / Octopath aesthetic) and cannot reach hi-density AI-pixel-art density via prompting alone, even with explicit density emphasis and a resolution bump. Four fixes folded in: (1) `references/density.md` replaces the "~96 pixels per character" numeric target with a named density-anchor table (8-bit / 16-bit / modern-indie / HD-pixel-game / AI-pixel-art-density) since image-gen models honor named aesthetics over numeric constraints; (2) `references/anti-patterns.md` adds a 6th craft marker — *"pixel scale matches the density anchor"* — raising the hi-fi pass bar from 4/5 to 5/6; markers 1–5 check *how* pixels behave, marker 6 checks *whether the pixels are the right size*; (3) `references/model-routing.md` sharpens Z-image's "Known weak spots" with the empirically-verified density ceiling, and adds a "Picking by density target" section mapping each anchor to the right generator; (4) `SKILL.md` Phase 3 gets a density-target pre-check that runs *before* the MCP-availability check — if the brief's anchor is HD-pixel-game-density or above, the skill skips Z-image and routes to Path B with a Midjourney `--niji 6` or SDXL + pixel-art LoRA prompt brief, even when Z-image is the only connected MCP. Adherence-pattern parallel to v3.6.1 / v3.5.1 (audit-driven patches). No new feature, no behavior change for moderate-density flows.

Earlier in v3.10.0: Adds the **`pixel-art`** skill — a pocket-sized hi-density pixel-art studio with a built-in design system in `references/` (5 hi-fi palettes + lo-fi banner anchors, per-mode density + dithering rules, three-layer composition rules, six lighting profiles, a 5-font catalog with VT323 default, a 5-marker craft-marker checklist), six prompt templates across five subject categories (scenes, characters, buildings, nature, title cards), and a portable SVG title-card template using VT323 with bold + inset-shadow styling. Two style modes: `hi-fi` (default, painterly hi-density) and `lo-fi` (scanlined warm-paper banner aesthetic, matching this repo's own banners). Capability-gated generation routing — Path A generates inline when an image-gen MCP is connected (Z-image, Imagen, OpenAI Image, Midjourney, SDXL); Path B emits a copy-pasteable, model-agnostic prompt brief with per-generator phrasing tweaks as a first-class deliverable. IP guardrail mirrors `algorithmic-art` (no living-artist names; original compositions only). Plus banners (LinkedIn + X) showing the skill's own design system as a three-panel layout (brief → palette/density/font → output mini-scene with lighthouse, ships, and dithered water/sky) and a 32×32 icon with a pixel-art lighthouse + warm-light reflection.

Earlier in v3.9.2: Adherence-only YAML frontmatter cleanup across 8 SKILL.md files to align with the cross-tool [SKILL.md standard](https://agentskills.io). Three skills (`coding-rules`, `pitch-deck`, `validation-canvas`) had plain-inline `description:` fields with `: ` colon-space sequences that broke YAML parsing — converted to `>` folded scalars (the style 9 other skills already use). Five skills (`handshake`, `sub-agent-coordinator`, `wear-the-hat`, `ai-ux-review`, `ai-eval-review`) had `instructions:` and/or `tags:` frontmatter keys outside Codex's documented optional-field allowlist — moved into the body as a `## When to use this skill` section + `**Tags:**` line. No description content changed, no behavior change for Claude; Codex now parses all 17 SKILL.md files. PyYAML strict-mode validation: 17/17 pass after patch (3 were invalid before). No README catalog changes.

Earlier in v3.9.1: Doc-only patch surfacing the token cost of `skill-evaluator`'s split-role harness. Adds a "What it costs to run" section to the skill's README (per-test cost breakdown — one executor + one grader sub-agent with fresh grader context, Phase 1 read pass through every reference file; ~10 sub-agent invocations for 5 prompts, ~30 with opt-in high-stakes mode) and a "Heads up — token-hungry by design" paragraph to the root README's `skill-evaluator` detail entry. Names when an in-context adversarial review by the author is the right substitute (single-section rule edits surface ~80–90% of the value at ~10% of the cost). No skill text or behavior changes. No breaking changes.

Earlier in v3.9.0: Adds the **§Diagnosis** hard rule to `coding-rules`' BOOTSTRAP.md. Closes the symptom-driven-fix failure mode — pattern-matching on error messages, stack traces, or "what a similar bug usually looks like" without reading the code that actually produced the failure. Generalizes the Iron Law from `references/debugging.md` to all coding work, not just bugfixes — feature-work failures (adding `*` to CORS allow-lists, wrapping in `try/catch` to silence errors, copy-pasting unverified snippets) are the same failure mode under a different name. Three bolded leads in the new section: "Diagnose with evidence, not symptoms" (scope: any code edit), "Cite the evidence in your response" (citation must be from code/logs/config actually read this session — not invented; citing a file you have not opened is a §Accuracy violation), and a STOP-and-surface-the-uncertainty escape valve (labeled hypothesis + verification path + 1–3 candidate fixes, with an anti-fabrication clause). Defines "reasonable effort" as at least 2-of-4 concrete actions. Sequences §When Stuck's "After 3 focused attempts" through the escape valve before marking BLOCKED. Pre-shipment in-context `skill-evaluator` audit surfaced six adherence gaps — three load-bearing (invented citations, "non-trivial edit" scope leak, error-message-as-evidence rationalization), three lower-risk — all folded into the shipped rule. No new skill; rule addition inside an existing one. No breaking changes — additive only.

Earlier in v3.8.0: Added the **`ai-eval-review`** skill — eval-design-completeness review for AI products, sibling to `ai-ux-review` (which shipped in 3.7.0). Seven elicitation blocks (necessity & success → ground truth → offline eval → online metrics → cohorts + disparate impact → adversarial + robustness → drift + monitoring), six mandatory cross-block checks plus a regulatory cross-cutting lens (EU AI Act / FDA SaMD / FTC AI guidance). Ships editable Markdown plus a self-contained HTML visualization (3+3+1 card grid in teal, sibling tone to `ai-ux-review`'s warm orange; Block 6 includes an adversarial-eval table). When `ai-ux-review.md` exists, reads Block 7 (Success & Evaluation) gaps and seeds Block 1 here from them — the two skills compose cleanly via `docs/ai-ux/`. Authored from first principles; informed by [HELM](https://github.com/stanford-crfm/helm) (Apache 2.0), [Anthropic's claude-cookbooks](https://github.com/anthropics/anthropic-cookbook) (MIT), [OpenAI Evals](https://github.com/openai/evals) (MIT), EU AI Act, FTC AI guidance, FDA SaMD eval expectations — none reproduced verbatim. Cross-link added bidirectionally to `ai-ux-review`. No breaking changes — additive only.

Earlier in v3.7.0: Added the **`ai-ux-review`** skill — design-completeness review for AI products. Seven elicitation blocks (necessity → mental model → trust → feedback → errors → output integrity → success), six mandatory cross-block checks, explicit `[Gap — …]` markers as first-class outputs. Ships editable Markdown plus a self-contained HTML visualization (3+3+1 card grid with `[GAP]` chips and Gap Summary footer). Block 6 (Output Integrity) is the gen-AI modernization layer — hallucination handling, output verifiability, provenance + citation, prompt-injection exposure, multi-turn drift, agent-autonomy levels — that pre-2022 frameworks under-cover. Inspired by Google's [People + AI Guidebook](https://pair.withgoogle.com/guidebook/) (CC BY-NC-SA 4.0) but **not a derivative work** — authored from first principles in its own voice; no Guidebook prose, worksheets, illustrations, or pattern names reproduced. See the skill's README → Influences for the full copyright-vs-license reasoning. Reads `validation-canvas.md` if present and skips business-model questions; reads `<brand-root>/DESIGN.md` for tokens.

Earlier in v3.6.3: Doc-only patch absorbing **harness engineering** vocabulary into `CLAUDE.md` and existing skills. No new skill, no rule changes — names the discipline that skill authoring in this repo was already doing partly by instinct (context engineering, progressive disclosure, observable feedback loops, state preservation, eval discipline), and points at `coding-rules` as the canonical implementation. Adds Design Principle 6 to `CLAUDE.md` ("Observable feedback loops over aspirational prose," with a reactive-constraint corollary), a "Harness lens" audit section to `skill-evaluator`, framing paragraphs to `sub-agent-coordinator` and `team-composer` Phase 6.6, and an `AGENTS.md` cross-vendor pointer to `CLAUDE.md`. An earlier draft added a `progress.md` continuity log + slash commands; both were removed when review confirmed `coding-rules`' `.ai/memory.log` + `.ai/STATUS.md` + session-start hooks are the sharper, working system.

Earlier in v3.6.2: Adherence-only documentation patch. The 3.6.0 release introduced the `wear-the-hat` skill but failed to update the root README's catalog sections (TL;DR count, "The shelf" table, "Skill details" entry) — the skill was registered in the plugin manifests but invisible to GitHub readers browsing the catalog. This patch fills those gaps and adds a new-skill catalog requirement to `CLAUDE.md`'s release ritual so future skill additions don't miss the catalog updates. Adjacent skills' "Pairs well with" lists now reference `wear-the-hat` bidirectionally.

Earlier in v3.6.1: Adherence-only patch from a pre-shipment `skill-evaluator` audit of the new `wear-the-hat` skill. Adds a **Role name authority** rule to Phase 2 (Load persona): use the exact role name from `team-composer/references/role-personas.md`; do not paraphrase or invent variants. Includes a graceful-degradation fallback when the auto-pick heuristic returns a role not present in the catalog. No other behavior change. All other audit findings across the three skills audited (`wear-the-hat`, `sub-agent-coordinator`, `team-composer`) classified as test-design issues, not skill issues. Overall pass rate 66/73 assertions (90.4%).

Earlier in v3.6.0: Consolidates sub-agent brief conventions into `sub-agent-coordinator` as the canonical home — three orthogonal axes for model selection (capability tier / reasoning effort / speed lane) with default mapping for coding work and generic fallback for non-coding; a Picking the Role section that reuses `team-composer`'s catalog as shared vocabulary; and a `BLOCKED_SCOPE_EXPANDED` status that lets sub-agents escalate scope expansion without breaking the hard no-nested-spawning rule. Adds the **`wear-the-hat`** skill for single-role embodiment — when you want one specific lens (`@security_specialist`, `@dataviz_engineer`, etc.) applied to a task without convening a multi-role panel. Updates `coding-rules` (Companion skills callout, BOOTSTRAP routing) and `team-composer` (Phase 6 Model Routing retires the "future enhancement" note). Additive only — no breaking changes.

Earlier in v3.5.1: Adherence-only patches surfaced during a `skill-evaluator` audit of the new `coding-rules` skill. Two doc/template-level changes: (1) tightens `skill-evaluator`'s executor-brief template so terse executors can't silently skip Trace/Reasoning sections; (2) clarifies the `coding-rules` README on how `load` and `install` differ in lifetime + adds explicit invocation examples for every sub-command. No external contract change to either skill.

Earlier in v3.5.0: adds the **`coding-rules`** skill — a session loader for one author's opinionated agentic-coding rules, ported from a separate working repo. Five sub-commands (`load` / `reload` / `status` / `install` / `uninstall`), per-project install with per-file confirmation across `CLAUDE.md` / `AGENTS.md` / `AI-CONTEXT.md` / `.cursorrules`, compaction-safe via `status` + `reload`. **The rules themselves are aggressively personal — read `BOOTSTRAP.md` end-to-end and fork before adopting.** No breaking changes; this is purely additive (`v0.1` skill).

Earlier in v3.4.0: adds the **`gtm`** skill in **🚧 BETA** — sixth step in the startup pipeline, covering the missing post-pipeline step (actually getting users) after `startup-grill`. Iteration-1 evals scored 100% with-skill vs 27.8% baseline (+72pp across three test cases: first-run-with-artifacts, cold-start, kill-switch). Those evals validate structural reliability — config files, helper-function kill switch, handoff event vocabulary — but do **not** validate real founder workflows; that dogfooding is the next milestone before graduating to v1. Breaking changes possible before then.

Earlier in v3.2.0: refined the `handshake` skill following its pre-shipment audit — description triggers widened on three new phrases (`"tune in to me"`, `"set a working agreement"`, `"share my preferences"`) and narrowed via an explicit negative gate against codebase orientation, performance-review calibration, and content gathering. Two body fixes added (Phase 0 transition rule + Phase 1 voice rule).

Earlier in v3.1.0: added the `handshake` skill — a brief, opt-in collaboration calibration ritual that runs before the real work (slash-command-only at v1, two-mode design with core calibration + optional project overlay, hard never-ask list, single-user contract, capability-gated integration with the existing two-tier memory store).

Earlier in v3.0.0: `brand-workshop`'s starter design-system output migrated to the [Google Labs `DESIGN.md` format](https://github.com/google-labs-code/design.md) (alpha spec). The downstream startup-pipeline skills (`validation-canvas`, `riskiest-assumption-test`, `pitch-deck`) now read tokens directly from `colors.primary` in the YAML front matter. See [CHANGELOG.md](CHANGELOG.md) for full v3.14.0 + v3.13.1 + v3.13.0 + v3.12.0 + v3.11.0 + v3.10.2 + v3.10.1 + v3.10.0 + v3.9.2 + v3.9.1 + v3.9.0 + v3.8.0 + v3.7.0 + v3.6.3 + v3.6.2 + v3.6.1 + v3.6.0 + v3.5.1 + v3.5.0 + v3.4.0 + v3.2.0 + v3.1.0 + v3.0.0 entries and migration notes.

- **Primary target agent** — Claude (Claude Code, Cowork).
- **Other agents** — may come later, no promises yet.
- **Stability** — the skills I ship here I use myself; if one stops earning its place, it gets removed rather than left to rot.

## Feedback

Issues and suggestions are welcome via [GitHub](https://github.com/sorawit-w/agent-skills/issues). Not accepting code contributions right now — feel free to fork.

## License

MIT. See [LICENSE](LICENSE).
