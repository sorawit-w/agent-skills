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

Each skill links to its own README — the full doc with usage, design notes, and cross-skill integration.

|  | Skill | What it's for |
|:---:|:---|:---|
| <img src="assets/icons/team-composer.svg" alt="" width="64" align="middle"/> | [`team-composer`](skills/team-composer/README.md) | Assemble the right virtual team and run a 3-round discussion that forces real disagreement. |
| <img src="assets/icons/sub-agent-coordinator.svg" alt="" width="64" align="middle"/> | [`sub-agent-coordinator`](skills/sub-agent-coordinator/README.md) | Orchestrate multi-agent work — briefing, coordination, and verification that don't drift. |
| <img src="assets/icons/wear-the-hat.svg" alt="" width="64" align="middle"/> | [`wear-the-hat`](skills/wear-the-hat/README.md) | Pick one role from `team-composer`'s catalog and do the work in their voice — solo embodiment, no panel discussion. |
| <img src="assets/icons/skill-evaluator.svg" alt="" width="64" align="middle"/> | [`skill-evaluator`](skills/skill-evaluator/README.md) | Audit a skill to see whether its rules actually land when Claude runs it. |
| <img src="assets/icons/tech-stack-recommendations.svg" alt="" width="64" align="middle"/> | [`tech-stack-recommendations`](skills/tech-stack-recommendations/README.md) | Opinionated default TS/JS stack (Bun + SvelteKit + Elysia + Neon + Drizzle + Clerk), plus named alternates. |
| <img src="assets/icons/handshake.svg" alt="" width="64" align="middle"/> | [`handshake`](skills/handshake/README.md) | A brief opt-in calibration ritual that shows you what's on file, then asks a few high-leverage collaboration questions. |
| <img src="assets/icons/whoami.svg" alt="" width="64" align="middle"/> | [`whoami`](skills/whoami/README.md) | A short conversational interview that profiles how you want to be collaborated with — six dials, an RPG class, a portable profile, and an HTML character sheet. |
| <img src="assets/icons/coding-rules.svg" alt="" width="64" align="middle"/> | [`coding-rules`](skills/coding-rules/README.md) **⚠️ OPINIONATED** | Loads one author's operating system for agentic coding into the session — branching, commit cadence, verification gates, sub-agent triggers. |
| <img src="assets/icons/i18n-contextual-rewriting.svg" alt="" width="64" align="middle"/> | [`i18n-contextual-rewriting`](skills/i18n-contextual-rewriting/README.md) | Surgical edits on large translation files, plus a role-based review that turns "translate" into cultural rewriting. |
| <img src="assets/icons/brand-workshop.svg" alt="" width="64" align="middle"/> | [`brand-workshop`](skills/brand-workshop/README.md) | Run a Discovery → Concept → Creation workshop and ship a brand strategy brief, tagline, and code-generated logo. |
| <img src="assets/icons/validation-canvas.svg" alt="" width="64" align="middle"/> | [`validation-canvas`](skills/validation-canvas/README.md) | Interview a founder block-by-block and produce a rigorous Lean Canvas + Value Proposition Canvas with explicit Stress Tests. |
| <img src="assets/icons/riskiest-assumption-test.svg" alt="" width="64" align="middle"/> | [`riskiest-assumption-test`](skills/riskiest-assumption-test/README.md) | Convert canvas Stress Tests into falsifiable hypotheses with success/kill criteria. Ships a 1-page test plan + interactive risk × impact matrix. |
| <img src="assets/icons/pitch-deck.svg" alt="" width="64" align="middle"/> | [`pitch-deck`](skills/pitch-deck/README.md) | Structured narrative interview across the 10-slide investor arc; ships a self-contained HTML deck + speaker notes. |
| <img src="assets/icons/startup-grill.svg" alt="" width="64" align="middle"/> | [`startup-grill`](skills/startup-grill/README.md) | Adversarially probe a startup with a panel of domain-aware grillers; ship a kill report ranked by severity × fixability. |
| <img src="assets/icons/startup-launch-kit.svg" alt="" width="64" align="middle"/> | [`startup-launch-kit`](skills/startup-launch-kit/README.md) | Opt-in umbrella orchestrator that sequences the five-step startup pipeline (brand → canvas → tests → pitch → grill) with shared state. |
| <img src="assets/icons/gtm.svg" alt="" width="64" align="middle"/> | [`gtm`](skills/gtm/README.md) **🚧 BETA** | Phased go-to-market for startup products — GTM playbook, multi-channel content, cadenced scheduling, compliance gates, kill switch. |
| <img src="assets/icons/ai-ux-review.svg" alt="" width="64" align="middle"/> | [`ai-ux-review`](skills/ai-ux-review/README.md) | Design-completeness review for AI products — seven blocks, six cross-block checks, explicit `[Gap — …]` markers. Ships MD + HTML. |
| <img src="assets/icons/ai-eval-review.svg" alt="" width="64" align="middle"/> | [`ai-eval-review`](skills/ai-eval-review/README.md) | Eval-design-completeness review for AI products — sibling to `ai-ux-review`. Seven blocks plus a regulatory lens. Ships MD + HTML. |
| <img src="assets/icons/pixel-art.svg" alt="" width="64" align="middle"/> | [`pixel-art`](skills/pixel-art/README.md) **🚧 BETA** | A pocket-sized hi-density pixel-art studio with a built-in design system. Two style modes; model-agnostic prompts; portable SVG title cards. |

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

Each entry below is a quick reference — example prompts and which skills it pairs with. Click any skill heading for its full README.

<a id="team-composer"></a>

### <img src="assets/icons/team-composer.svg" alt="" width="48" align="middle"/> &nbsp;[`team-composer`](skills/team-composer/README.md)

**Pairs well with.**
- [`sub-agent-coordinator`](skills/sub-agent-coordinator/README.md) — Phase 6 delegates deliverable production through its patterns.
- [`wear-the-hat`](skills/wear-the-hat/README.md) — when the task wants ONE specific lens applied, not a multi-role panel discussion. Inverse use case from this skill.
- [`skill-evaluator`](skills/skill-evaluator/README.md) — audit team-composer (or any team-driven skill) for rules that get quietly skipped.
- [`tech-stack-recommendations`](skills/tech-stack-recommendations/README.md) — when the architect role needs an opinionated stack to anchor the debate.
- [`i18n-contextual-rewriting`](skills/i18n-contextual-rewriting/README.md) — when the `@i18n_specialist` is on the team and the output needs to ship in multiple locales.
- [`ai-ux-review`](skills/ai-ux-review/README.md) / [`ai-eval-review`](skills/ai-eval-review/README.md) — discussion-grade alternative inverse. Use `team-composer` with `@ux_researcher` + `@ai_safety_specialist` (or `@data_scientist` + `@ai_safety_specialist` for eval) when you want a *narrow one-block discussion* rather than a full structured review artifact. Use the dedicated review skills when you want the persistent MD + HTML output.

**Try it.**
- "Bring a team together to review this mobile auth architecture before we ship."
- "Brainstorm a habit-tracker for teens — multi-perspective, no single viewpoint wins."
- "After team-composer concludes, hand Phase 6 deliverables to `sub-agent-coordinator` and fan out the architect / backend / frontend work in parallel."

---

<a id="sub-agent-coordinator"></a>

### <img src="assets/icons/sub-agent-coordinator.svg" alt="" width="48" align="middle"/> &nbsp;[`sub-agent-coordinator`](skills/sub-agent-coordinator/README.md)

**Pairs well with.**
- [`team-composer`](skills/team-composer/README.md) — natural upstream: discussion finishes, deliverables fan out via coordinator patterns.
- [`wear-the-hat`](skills/wear-the-hat/README.md) — sub-agent mode hands off a brief with `Role:` tag and persona context baked in; this skill's spawning protocol owns the rest.
- [`skill-evaluator`](skills/skill-evaluator/README.md) — spawn evaluator sub-agents to stress-test other skills in parallel.

**Try it.**
- "Refactor all 14 React components from class to function — coordinate in parallel."
- "Debug our flaky CI suite: spawn a researcher, a fixer, and a reviewer with clear briefs."
- "After `team-composer` concludes, brief sub-agents to produce the per-role deliverables the conclusion assigned."

---

<a id="wear-the-hat"></a>

### <img src="assets/icons/wear-the-hat.svg" alt="" width="48" align="middle"/> &nbsp;[`wear-the-hat`](skills/wear-the-hat/README.md)

**Pairs well with.**
- [`team-composer`](skills/team-composer/README.md) — owns the role catalog (`role-personas.md`). `wear-the-hat` consumes it. Multi-role tasks route here with explicit user confirmation.
- [`sub-agent-coordinator`](skills/sub-agent-coordinator/README.md) — sub-agent mode produces a brief with `Role:` tag and persona context, then hands off to coordinator's protocol; no duplicate spawning logic.
- [`coding-rules`](skills/coding-rules/README.md) — coding-task role embodiment composes naturally: `coding-rules` sets the engineering discipline; `wear-the-hat` applies the lens.
- [`brand-workshop`](skills/brand-workshop/README.md) — pure brand-identity packages route to `brand-workshop`; `wear-the-hat` redirects.

**Try it.**
- "Audit `middleware/auth.ts` for missing CSRF guards as `@security_specialist`."
- "Act as a data-viz engineer and review this chart spec."
- "Wear the hat of the accessibility specialist for this UI review."

---

<a id="skill-evaluator"></a>

### <img src="assets/icons/skill-evaluator.svg" alt="" width="48" align="middle"/> &nbsp;[`skill-evaluator`](skills/skill-evaluator/README.md)

**Pairs well with.**
- **Every other skill on this shelf** — use it to audit any of them. The shelf is only as sharp as its weakest rule.
- [`sub-agent-coordinator`](skills/sub-agent-coordinator/README.md) — run evaluation variants in parallel (different prompt sets, different grader instances) and converge findings.

**Try it.**
- "Stress-test `team-composer` — does Round 2 actually produce rebuttals, or is it ceremonial?"
- "My onboarding skill has been 'mostly working.' Audit it and tell me which rules are getting skipped."
- "Use `sub-agent-coordinator` to fan out evaluator runs against three of our skills in parallel and converge the findings."

---

<a id="tech-stack-recommendations"></a>

### <img src="assets/icons/tech-stack-recommendations.svg" alt="" width="48" align="middle"/> &nbsp;[`tech-stack-recommendations`](skills/tech-stack-recommendations/README.md)

**Pairs well with.**
- [`team-composer`](skills/team-composer/README.md) — when the architect role needs an anchor position to debate from.
- [`skill-evaluator`](skills/skill-evaluator/README.md) — audit the stack rules against your real constraints before committing.

**Try it.**
- "I'm starting a SaaS side-project. Give me one opinionated stack I don't have to second-guess."
- "We're migrating off Next.js on Vercel — recommend the path and name the trade-offs honestly."
- "Kick off a `team-composer` architecture review and load `tech-stack-recommendations` as the architect's anchor position."

---

<a id="handshake"></a>

### <img src="assets/icons/handshake.svg" alt="" width="48" align="middle"/> &nbsp;[`handshake`](skills/handshake/README.md)

**Pairs well with.**
- [`team-composer`](skills/team-composer/README.md) — when a team is about to be assembled and `user`-type memory is sparse, `team-composer` MAY suggest `/handshake` first so the team can be tailored to your collaboration style. Suggestion only; never auto-routes.
- [`brand-workshop`](skills/brand-workshop/README.md) — similar — may suggest `/handshake` for a personal-brand or solo-founder identity package. Suggestion only.
- [`validation-canvas`](skills/validation-canvas/README.md) / [`riskiest-assumption-test`](skills/riskiest-assumption-test/README.md) / [`pitch-deck`](skills/pitch-deck/README.md) — these read project state, not user state. May suggest `/handshake --project` at kickoff if `project`-type memory for the current work is empty. Suggestion only.
- [`whoami`](skills/whoami/README.md) — sibling. `whoami` is the broad person-level profile; `handshake` calibrates one project and pre-fills its core questions from the whoami profile.
- `productivity:memory-management` *(if installed)* — `handshake` writes into the same two-tier `MEMORY.md` + `memory/` store. Capability-gated: defers to `productivity:memory-management`'s file-layout conventions when present, otherwise writes directly to the runtime's persistent memory.

**Try it.**
- "Calibrate how we work — I'm tired of generic answers."
- "Show me what you have on file about me, then ask the questions that would actually help."
- "Run `/handshake --project` for this repo before we start the next sprint."

---

<a id="whoami"></a>

### <img src="assets/icons/whoami.svg" alt="" width="48" align="middle"/> &nbsp;[`whoami`](skills/whoami/README.md)

**Pairs well with.**
- [`handshake`](skills/handshake/README.md) — sibling. `whoami` is the broad person-level profile; `handshake` calibrates one project and pre-fills its core questions from the whoami profile. `whoami` is upstream and one-directional.
- [`pixel-art`](skills/pixel-art/README.md) — `whoami` calls it (if an image generator is available) to generate the class character portrait; falls back to a bundled hi-density pixel-art PNG.
- `productivity:memory-management` *(if installed)* — `whoami` writes its profile as a standard `user`-type memory; capability-gated, defers to the runtime's memory conventions.

**Try it.**
- "Run `/whoami` — I want you to actually know how I like to work."
- "I just switched from another AI tool — here's my profile file, set me up."
- "`/whoami rerun` — my role changed and the profile's out of date."

---

<a id="coding-rules"></a>

### <img src="assets/icons/coding-rules.svg" alt="" width="48" align="middle"/> &nbsp;[`coding-rules`](skills/coding-rules/README.md) &nbsp;⚠️&nbsp;**OPINIONATED**

> **Deliberately, aggressively opinionated** — one author's personal taste, loaded on every session that uses it. Not a neutral best-practice guide. Read [`resources/BOOTSTRAP.md`](skills/coding-rules/resources/BOOTSTRAP.md) end-to-end and fork before adopting. Full caveat in the [skill README](skills/coding-rules/README.md).

**Pairs well with.**
- [`skill-evaluator`](skills/skill-evaluator/README.md) — for evaluating rule changes. The skill's own `CLAUDE.md` enforces "no inline grading" — rule audits route to a fresh-context split-role harness to remove author bias.
- [`wear-the-hat`](skills/wear-the-hat/README.md) — coding-task role embodiment composes naturally: this skill sets the engineering discipline; `wear-the-hat` applies the specific lens (`@security_specialist`, `@dataviz_engineer`, etc.) for the task at hand.
- Project-local `CLAUDE.md` / `AGENTS.md` — per BOOTSTRAP's priority order (User > Project config > Agent context > Playbook), the project's own instructions always win over rules in this skill.
- `superpowers:*` *(if installed)* — overlap exists (TDD, brainstorming, verification-before-completion). Explicit user invocations win; otherwise this skill's BOOTSTRAP rules are the operating frame.

**Try it.**
- "Use the coding-rules skill to load my rules into this session."
- "Use the coding-rules skill with `args: install` for this project — I want CLAUDE.md to auto-load it."
- "Use the coding-rules skill with `args: status` — I want to check whether the rules are still in context after that long compaction."

---

<a id="i18n-contextual-rewriting"></a>

### <img src="assets/icons/i18n-contextual-rewriting.svg" alt="" width="48" align="middle"/> &nbsp;[`i18n-contextual-rewriting`](skills/i18n-contextual-rewriting/README.md)

**Pairs well with.**
- [`team-composer`](skills/team-composer/README.md) — when `@i18n_specialist` is on the team, this skill executes the translation work the team's output needs.
- [`brand-workshop`](skills/brand-workshop/README.md) — localize the descriptions pack (taglines, bios, boilerplate) without losing voice.

**Try it.**
- "Translate this onboarding flow into Thai, Japanese, and Korean — cultural rewriting, not machine translation."
- "Edit three keys in a 4,000-line `zh-CN.json` without rewriting the whole file or blowing the token budget."
- "`brand-workshop` just shipped the descriptions pack — localize it into `th` and `ja` and keep the voice."

---

<a id="brand-workshop"></a>

### <img src="assets/icons/brand-workshop.svg" alt="" width="48" align="middle"/> &nbsp;[`brand-workshop`](skills/brand-workshop/README.md)

**Pairs well with.**
- [`validation-canvas`](skills/validation-canvas/README.md) — suggested next step. Auto-applies brand tokens from the kit.
- [`riskiest-assumption-test`](skills/riskiest-assumption-test/README.md) — two steps downstream. Reads design tokens for the matrix HTML.
- [`pitch-deck`](skills/pitch-deck/README.md) — reads the brand design system (`docs/brand/DESIGN.md`) for consistent branding and owns the deck construction itself.
- [`i18n-contextual-rewriting`](skills/i18n-contextual-rewriting/README.md) — localize the descriptions pack while preserving tone.

**Try it.**
- "Run the full workshop for my meditation startup — identity, mark, voice, and design tokens."
- "I have a one-paragraph startup idea. Take me through Discovery → Concept → Creation and ship a launch-ready kit."
- "Brand-workshop first, then hand the kit to `validation-canvas` and `pitch-deck` so the whole startup artifact chain shares tokens."

---

<a id="validation-canvas"></a>

### <img src="assets/icons/validation-canvas.svg" alt="" width="48" align="middle"/> &nbsp;[`validation-canvas`](skills/validation-canvas/README.md)

**Pairs well with.**
- [`brand-workshop`](skills/brand-workshop/README.md) — upstream input; the canvas auto-applies brand tokens from the kit.
- [`riskiest-assumption-test`](skills/riskiest-assumption-test/README.md) — required next step (medium gate). Stress Tests seed the assumption dump; invalidated hypotheses loop back here in update mode.
- [`pitch-deck`](skills/pitch-deck/README.md) — two steps downstream. Reads canvas headings to seed slides 2, 3, 6 and cross-checks the Ask against Stress Tests.
- [`team-composer`](skills/team-composer/README.md) — when a block is contested, kick it to a full multi-role team for a focused session.
- [`startup-grill`](skills/startup-grill/README.md) — last step. Reads Stress Tests and un-relieved Pains as direct grilling ammunition.
- [`ai-ux-review`](skills/ai-ux-review/README.md) — for AI-flavored startups, the natural next step after the canvas is settled. This skill reads `validation-canvas.md` if present and skips business-model questions, focusing purely on the human-AI design layer.
- [`ai-eval-review`](skills/ai-eval-review/README.md) — sibling of `ai-ux-review`. When the AI product's eval rigor is the load-bearing question (regulated domain, classification with disparate-impact risk, drift-sensitive deployment), this is the measurement-side review.

**Try it.**
- "Build a validation canvas for my AI code-review tool."
- "I'm a 3rd-time founder pivoting into healthtech — run the canvas in compressed mode and challenge me hard."
- "`brand-workshop` is done — use the brand kit as input and generate the canvas with auto-styled tokens."

---

<a id="riskiest-assumption-test"></a>

### <img src="assets/icons/riskiest-assumption-test.svg" alt="" width="48" align="middle"/> &nbsp;[`riskiest-assumption-test`](skills/riskiest-assumption-test/README.md)

**Pairs well with.**
- [`validation-canvas`](skills/validation-canvas/README.md) — required upstream (medium gate). Loop-back target when hypotheses invalidate.
- [`pitch-deck`](skills/pitch-deck/README.md) — downstream (heavy gate). Pitch refuses to ship without populated `## Results` for top-3 hypotheses.
- [`startup-grill`](skills/startup-grill/README.md) — last step. Reads Results to check for iteration evidence.
- [`team-composer`](skills/team-composer/README.md) — discussion-grade alternative for multi-role validation strategy.
- [`ai-ux-review`](skills/ai-ux-review/README.md) / [`ai-eval-review`](skills/ai-eval-review/README.md) — composition. When the Gap Summary from either AI-review skill surfaces an *assumption that needs testing* (not just deciding — e.g., "we assume voice-sample-based prompting matches user voice well enough"), hand it here to convert into a falsifiable hypothesis with success / kill criteria.

**Try it.**
- "I just shipped my validation canvas — what should I test first?"
- "Design a fake-door test for my new auto-AP feature."
- "My pre-sale failed — only 1 of 15 paid. Update my test plan and route me back to the canvas."

---

<a id="pitch-deck"></a>

### <img src="assets/icons/pitch-deck.svg" alt="" width="48" align="middle"/> &nbsp;[`pitch-deck`](skills/pitch-deck/README.md)

**Pairs well with.**
- [`validation-canvas`](skills/validation-canvas/README.md) — two steps upstream. Reads the validation canvas (`docs/canvas/validation-canvas.md` or v1 `validation-canvas.md`) to seed slides 2/3/6 and cross-check the Ask.
- [`riskiest-assumption-test`](skills/riskiest-assumption-test/README.md) — required direct upstream (heavy gate). Reads the assumption-test plan (`docs/rat/assumption-test-plan.md` or v1 `rat/assumption-test-plan.md`) Top 3 + Results to inform the Validation slide and Traction claims; refuses to ship a clean deck without populated Results (override: `[PRE-VALIDATION DRAFT]` watermark).
- [`brand-workshop`](skills/brand-workshop/README.md) — reads the brand design system (`docs/brand/DESIGN.md`) for visuals.
- [`team-composer`](skills/team-composer/README.md) — when a slide claim is weak, spin up `@startup_strategist + @vc_partner + @senior_copywriter` to pressure-test it before shipping.
- [`startup-grill`](skills/startup-grill/README.md) — after this skill ships, run the grill to probe the deck adversarially before it lands in an investor's inbox.

**Try it.**
- "Investor wants my seed deck by Friday — start the structured interview."
- "Use the validation canvas and assumption-test plan to build the deck; refuse to ship with any cardinal sin."
- "I haven't tested anything yet but I want to see what the deck would look like — pre-validation draft mode."

---

<a id="startup-grill"></a>

### <img src="assets/icons/startup-grill.svg" alt="" width="48" align="middle"/> &nbsp;[`startup-grill`](skills/startup-grill/README.md)

**Pairs well with.**
- [`validation-canvas`](skills/validation-canvas/README.md) — upstream input. The Stress Tests section + un-relieved VPC Pains are direct grilling ammunition.
- [`riskiest-assumption-test`](skills/riskiest-assumption-test/README.md) — upstream input. The iteration-evidence check (`## Iteration Evidence` section in the kill report, added v2.0.0) yellow-flags pristine pipelines where the canvas wasn't updated after RAT testing.
- [`pitch-deck`](skills/pitch-deck/README.md) — upstream input. The deck's required-slot answers become starting probes.
- [`brand-workshop`](skills/brand-workshop/README.md) — upstream input when slot 5 = `@brand_strategist`; the panel reads `brand-brief.md`'s Positioning section.
- [`team-composer`](skills/team-composer/README.md) — instead of this skill when the user wants brainstorming or constructive review. After this skill when the kill report's `Suggested attack` lines need a multi-role workshop.
- [`skill-evaluator`](skills/skill-evaluator/README.md) — audit the verdict-vs-body consistency rule, the no-lethal-skip rule, the interactive-invitation rule.

**Try it.**
- "Grill my startup idea: a B2B SaaS for accounting firms — pre-seed, $4k MRR, two co-founders. What would kill us?"
- "I have the validation canvas, assumption-test plan, and pitch deck ready — run the grill with the deck as primary input."
- "Defending L1. We have a 6-month cohort retention curve at 87% logo retention. Re-probe."

---

<a id="startup-launch-kit"></a>

### <img src="assets/icons/startup-launch-kit.svg" alt="" width="48" align="middle"/> &nbsp;[`startup-launch-kit`](skills/startup-launch-kit/README.md)

**Pairs well with.**
- All five pipeline skills above — the orchestrator calls them in order. Use them directly for any single-step or partial-pipeline work.
- [`team-composer`](skills/team-composer/README.md) — alternative for pipeline-strategy discussions, single-block deep dives, or work that doesn't fit the pipeline shape.

**Try it.**
- "Build my whole startup kit for [idea] — take me through everything."
- "I ran brand-workshop and validation-canvas manually last week. Pick up where I left off."
- "I want to ship a pre-validation draft of the deck for an advisor meeting Friday — record the override and proceed."

---

<a id="gtm"></a>

### <img src="assets/icons/gtm.svg" alt="" width="48" align="middle"/> &nbsp;[`gtm`](skills/gtm/README.md) &nbsp;🚧&nbsp;**BETA**

> **Beta** — evals validate structural reliability, not real founder workflows on a real project. Breaking changes possible before v1; treat outputs as drafts to review. Full caveat in the [skill README](skills/gtm/README.md).

**Pairs well with.**
- [`brand-workshop`](skills/brand-workshop/README.md) — upstream input. `gtm` reads `DESIGN.md` for brand voice tokens. Wizard offers to invoke `brand-workshop` if no brand artifact exists.
- [`validation-canvas`](skills/validation-canvas/README.md) — upstream input. `gtm` reads ICP, positioning, channels, and Stress Tests for the playbook.
- [`pitch-deck`](skills/pitch-deck/README.md) — upstream input. `gtm` reads positioning and messaging from the deck content.
- [`startup-grill`](skills/startup-grill/README.md) — adjacent. After `gtm` ships its P1 playbook, the founder may grill it for blind spots before promoting to P2.
- [`sub-agent-coordinator`](skills/sub-agent-coordinator/README.md) — hard dispatch target. Multi-channel content fan-out runs through its patterns.
- [`i18n-contextual-rewriting`](skills/i18n-contextual-rewriting/README.md) — hard dispatch target. Non-English content drafts route through this skill for cultural adaptation.
- [`tech-stack-recommendations`](skills/tech-stack-recommendations/README.md) — when `gtm` emits a `content.needs_eng` event for a landing page and the founder has no chosen stack.

**Try it.**
- "My pitch deck is ready and I want to start getting users — set up GTM for this project."
- "kick off go-to-market for invoicy.app — B2C, US-only for now, freelance designer audience."
- "halt all my marketing automations right now — there's a PR fire on TikTok. Then later, walk me through how to resume safely."

---

<a id="ai-ux-review"></a>

### <img src="assets/icons/ai-ux-review.svg" alt="" width="48" align="middle"/> &nbsp;[`ai-ux-review`](skills/ai-ux-review/README.md)

**Pairs well with.**
- [`validation-canvas`](skills/validation-canvas/README.md) — upstream for AI startups. When present, this skill skips business-model questions and audits UX execution only.
- [`brand-workshop`](skills/brand-workshop/README.md) — upstream when a brand identity exists. This skill reads `DESIGN.md` to style the HTML output.
- [`team-composer`](skills/team-composer/README.md) — alternative when the request is one narrow block (e.g., "let's debate trust calibration") rather than a full review. Discussion-grade, no artifact.
- [`riskiest-assumption-test`](skills/riskiest-assumption-test/README.md) — composition. If the Gap Summary surfaces design assumptions that need *testing* (not just deciding), hand the gaps to RAT.
- [`startup-grill`](skills/startup-grill/README.md) — adjacent. Adversarial pre-mortem with a verdict. Different mode from this skill's cooperative gap detection.
- [`ai-eval-review`](skills/ai-eval-review/README.md) — sibling skill. This audits the human-AI design surface; `ai-eval-review` audits the measurement layer behind it. Block 7 gaps here seed Block 1 there.

**Try it.**
- "Review the UX of our LLM email-draft feature before launch — focus on trust and output integrity."
- "We just shipped an agentic feature and fluent-but-wrong outputs are surfacing. Walk us through the review."
- "Review the AI feature in our app — `validation-canvas.md` is already in `docs/canvas/`; skip the business-model questions and audit the UX layer."

---

<a id="ai-eval-review"></a>

### <img src="assets/icons/ai-eval-review.svg" alt="" width="48" align="middle"/> &nbsp;[`ai-eval-review`](skills/ai-eval-review/README.md)

**Pairs well with.**
- [`ai-ux-review`](skills/ai-ux-review/README.md) — **sibling skill.** Same shape, same elicitation pattern, different subject. Run both for a complete AI product review.
- [`validation-canvas`](skills/validation-canvas/README.md) — upstream for AI startups. Block 5 (Cohort breakdown) reads Customer Segments.
- [`brand-workshop`](skills/brand-workshop/README.md) — upstream when a brand exists. HTML output styled from `DESIGN.md`.
- [`team-composer`](skills/team-composer/README.md) — alternative for one-block discussions (e.g., "let's debate ground-truth labeling strategy") rather than a full review artifact.
- [`riskiest-assumption-test`](skills/riskiest-assumption-test/README.md) — composition. Gap Summary entries that are *assumptions about evals* (e.g., "we assume single-annotator labels are accurate enough") become RAT hypotheses.
- [`startup-grill`](skills/startup-grill/README.md) — adjacent. Adversarial pre-mortem with verdict; different mode from this skill's cooperative gap detection.

**Try it.**
- "Review the eval setup for our classification model before launch — push hard on ground truth and cohort breakdown."
- "We have `ai-ux-review.md` with Block 7 gaps for our LLM feature. Walk through the eval review next, seeded from those gaps."
- "Eval review for our medical-imaging classifier — we're FDA SaMD class II, so apply regulatory rigor across Blocks 2, 5, and 6."

---

<a id="pixel-art"></a>

### <img src="assets/icons/pixel-art.svg" alt="" width="48" align="middle"/> &nbsp;[`pixel-art`](skills/pixel-art/README.md) &nbsp;🚧&nbsp;**BETA**

> **Beta** — structural smoke-tests pass, but the skill is not yet dogfooded across all subject categories and generators. Full caveat in the [skill README](skills/pixel-art/README.md).

**Pairs well with.**
- [`brand-workshop`](skills/brand-workshop/README.md) — logo / identity packages route there. `pixel-art` can produce pixel-art **banners** for a brand, but logos are a different deliverable.
- Anthropic's `algorithmic-art` — sibling skill. Algorithmic art uses p5.js (procedural, seeded); `pixel-art` uses image-gen models + structured prompts. Different toolchain, complementary scope.
- Anthropic's `canvas-design` — sibling skill. Canvas-design ships static raster / PDF via design-philosophy prose; `pixel-art` ships pixel-style raster via design-system tokens.
- [`team-composer`](skills/team-composer/README.md) — when the brief is cross-disciplinary (e.g., game splash + marketing copy), `team-composer` assembles roles and may hand the visual deliverable to `pixel-art`.
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

**Current release: `3.15.3`.** Root README restructured into a lean table-of-contents — the shelf links straight to each skill's README, Skill-details entries trimmed to examples + pairings, the Status section slimmed; six skill READMEs gained or completed their cross-skill sections. Full version history, with the reasoning behind each release, is in [CHANGELOG.md](CHANGELOG.md).

- **Primary target agent** — Claude (Claude Code, Cowork).
- **Other agents** — may come later, no promises yet.
- **Stability** — the skills I ship here I use myself; if one stops earning its place, it gets removed rather than left to rot.

## Feedback

Issues and suggestions are welcome via [GitHub](https://github.com/sorawit-w/agent-skills/issues). Not accepting code contributions right now — feel free to fork.

## License

MIT. See [LICENSE](LICENSE).
