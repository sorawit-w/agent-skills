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

- **What this is** — a single Claude Code plugin that installs a curated shelf of nine specialized skills in one go.
- **Who it's for** — anyone using Claude Code or Cowork who wants auto-triggering expertise for a specific job: founders pitching investors, PMs brainstorming with a team, engineers writing or auditing a skill, localizers rewriting inside cultural reality, and founders who want their startup adversarially probed.
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
| <img src="assets/icons/i18n-contextual-rewriting.svg" alt="" width="64" align="middle"/> | [`i18n-contextual-rewriting`](#i18n-contextual-rewriting) | Surgical edits on large translation files, plus a role-based review that turns "translate" into cultural rewriting. | You're editing a big i18n file without blowing token limits, or producing translations that shouldn't read as machine-converted English. |
| <img src="assets/icons/brand-workshop.svg" alt="" width="64" align="middle"/> | [`brand-workshop`](#brand-workshop) | Run a Discovery → Concept → Creation workshop and ship a brand strategy brief, tagline, and code-generated logo. | You need a real identity package for a product, app, or startup — not just a logo doodle. |
| <img src="assets/icons/business-model-canvas.svg" alt="" width="64" align="middle"/> | [`business-model-canvas`](#business-model-canvas) | Interview a founder block-by-block and produce a rigorous Osterwalder canvas with explicit Stress Tests. | You need a business model that holds up to scrutiny before building the deck, the product, or the hire plan. |
| <img src="assets/icons/pitch-deck.svg" alt="" width="64" align="middle"/> | [`pitch-deck`](#pitch-deck) | Structured narrative interview across the 10-slide investor arc; ships a self-contained HTML deck + speaker notes. | An investor said "send me your deck" and you need a shippable v1 this week — content filled, not a template. |
| <img src="assets/icons/startup-grill.svg" alt="" width="64" align="middle"/> | [`startup-grill`](#startup-grill) | Adversarially probe a startup with a panel of domain-aware grillers; ship a kill report ranked by severity × fixability with optional interactive defense. | You want your idea / deck / business model probed for what would actually kill it — not "thoughts to consider," a verdict you can act on. |

Each skill lives under [`skills/`](skills/) with its own `README.md`, `SKILL.md`, and reference docs.

---

## How skills chain

Two pipelines the shelf is designed to support end-to-end.

### 🧭 Startup pipeline — identity → model → deck → grill

```
brand-workshop ──▶ business-model-canvas ──▶ pitch-deck ──▶ startup-grill
 (identity kit)       (9-block model)          (HTML deck)     (kill report)
```

The artifacts compound. `brand-workshop` writes `brand-kit/design-system.md` — `business-model-canvas` and `pitch-deck` both pick it up automatically for consistent tokens. `business-model-canvas` writes `business-model.md` — `pitch-deck` seeds slides 2, 3, 6, and 7 from it and cross-checks the Ask against the Stress Tests. `startup-grill` reads all three (Stress Tests, slide-contract anti-patterns, brand positioning) as direct grilling ammunition and ships a `grill/kill-report.md` with a verdict you can act on. You don't have to wire anything up; running them in order is the wiring.

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

**What it does.** Assembles a virtual creative team, runs a Discovery → Concept → Creation workshop, and ships a launch-ready identity package: brand strategy brief (`.md`), tagline, code-generated logo (`.svg` rendered to `.png`), favicon pack with HTML install snippet, social banner set (OG / X / LinkedIn / Instagram), descriptions pack (bios + elevator pitch + boilerplate), and a starter `design-system.md` (tokens only) that downstream skills like `pitch-deck` and `business-model-canvas` pick up automatically.

**Reach for it when.** You need a real identity package — positioning, voice, archetype, tagline, and mark all sharing the same rationale — not just a logo doodle. Skip the positioning and the logo is just a doodle.

**Pairs well with.**
- [`business-model-canvas`](#business-model-canvas) — auto-applies brand tokens from the kit.
- [`pitch-deck`](#pitch-deck) — reads `brand-kit/design-system.md` for consistent branding and owns the deck construction itself.
- [`i18n-contextual-rewriting`](#i18n-contextual-rewriting) — localize the descriptions pack while preserving tone.

**Try it.**
- "Run the full workshop for my meditation startup — identity, mark, voice, and design tokens."
- "I have a one-paragraph startup idea. Take me through Discovery → Concept → Creation and ship a launch-ready kit."
- "Brand-workshop first, then hand the kit to `business-model-canvas` and `pitch-deck` so the whole startup artifact chain shares tokens."

---

<a id="business-model-canvas"></a>

### <img src="assets/icons/business-model-canvas.svg" alt="" width="48" align="middle"/> &nbsp;`business-model-canvas`

**What it does.** Interviews a founder block-by-block (customer-first reasoning order, at most three questions per block, total ~45–75 minutes for a first pass) and produces two files: `business-model.md` (canonical, editable, deck-parseable) and `business-model.html` (self-contained Osterwalder-grid canvas that prints cleanly to PDF). Runs a mandatory cross-block consistency pass, and ends with an explicit Stress Tests section naming the 3–5 assumptions most likely to kill the business.

**Reach for it when.** You need a business model that holds up to scrutiny before building the deck, the product, or the hire plan — with specificity gates that refuse category answers ("SMBs", "the internet") and customer-first reasoning enforced, not assumed.

**Pairs well with.**
- [`brand-workshop`](#brand-workshop) — upstream input; the canvas auto-applies brand tokens from the kit.
- [`pitch-deck`](#pitch-deck) — downstream: `business-model.md` seeds slides 2, 3, 6, 7 and the Ask gets cross-checked against the Stress Tests.
- [`team-composer`](#team-composer) — when a block is contested, kick it to a full multi-role team for a focused session.
- [`startup-grill`](#startup-grill) — after the canvas is done, run the grill to attack the Stress Tests with an adversarial panel.

**Try it.**
- "Interview me block-by-block and produce a BMC for my AI code-review tool."
- "`brand-workshop` is done — use `brand-kit/` as input and generate the canvas with auto-styled tokens."
- "Build the canvas; when we're done, hand it to `pitch-deck` to seed slides 2/3/6/7 and cross-check the Ask."

---

<a id="pitch-deck"></a>

### <img src="assets/icons/pitch-deck.svg" alt="" width="48" align="middle"/> &nbsp;`pitch-deck`

**What it does.** Runs a structured narrative interview across the 10-slide investor arc (Title → Problem → Solution → Market → Product → Business Model → Traction → Team → Competition → Ask) and ships three files: a single self-contained HTML deck (Reveal.js inlined, keyboard nav, AAA contrast, `?print-pdf` produces a clean slide-per-page PDF), speaker notes per slide, and a pre-send checklist. Refuses to ship with any of the four cardinal sins unfilled: TAM-only sizing, traction without a time axis, teamless team, vague ask.

**Reach for it when.** An investor said "send me your deck" and you need a shippable v1 this week with the actual content filled in — not a template waiting to be filled later.

**Pairs well with.**
- [`business-model-canvas`](#business-model-canvas) — reads `business-model.md` to seed slides and cross-check the Ask.
- [`brand-workshop`](#brand-workshop) — reads `brand-kit/design-system.md` and `brand-kit/deck/pitch-template.html` for visuals.
- [`team-composer`](#team-composer) — when a slide claim is weak, spin up `@startup_strategist + @vc_partner + @senior_copywriter` to pressure-test it before shipping.
- [`startup-grill`](#startup-grill) — after this skill ships, run the grill to probe the deck adversarially before it lands in an investor's inbox.

**Try it.**
- "Investor wants my seed deck by Friday — start the structured interview."
- "Use `business-model.md` and `brand-kit/` to build the deck; refuse to ship with any cardinal sin."
- "After v1 ships, kick it to `team-composer` (`@startup_strategist` + `@vc_partner` + `@senior_copywriter`) to pressure-test the Market slide."

---

<a id="startup-grill"></a>

### <img src="assets/icons/startup-grill.svg" alt="" width="48" align="middle"/> &nbsp;`startup-grill`

**What it does.** Adversarially probes a startup idea with a panel of domain-aware grillers — `@vc_partner`, `@growth_marketer`, `@startup_strategist`, `@ux_researcher`, plus a flexible fifth seat (`@senior_software_architect` for technical-execution-dominant startups, `@brand_strategist` for consumer-brand-dominant ones), plus 0–3 specialists injected from signals (legal, security, clinical, AI safety, game design, etc.). Runs three rounds — probe → forced steelman defense → verdict — and ships a structured kill report ranked across two axes: severity (lethal vs material) and fixability (fixable vs unfixable). Verdict label is one of four canonical labels: `Investable as-is`, `Investable with conditions`, `Pivot signal`, `Pass`. Refuses to ship a soft report — Round 1 must surface at least one lethal read or re-run with sharpened posture. Optional interactive defense mode lets the founder pick a weakness, bring new evidence, and have the relevant 1–2 panelists re-probe that line item only.

**Reach for it when.** You have a startup idea, deck, or business model and want it probed adversarially before you commit time, money, or a fundraise. You want a verdict you can act on, not "thoughts to consider." You want the lethal weakness named declaratively, with a falsifier attached, so you know exactly what evidence to bring.

**Pairs well with.**
- [`business-model-canvas`](#business-model-canvas) — upstream input. The Stress Tests section is direct grilling ammunition.
- [`pitch-deck`](#pitch-deck) — upstream input. The deck's required-slot answers become starting probes.
- [`brand-workshop`](#brand-workshop) — upstream input when slot 5 = `@brand_strategist`; the panel reads `brand-brief.md`'s Positioning section.
- [`team-composer`](#team-composer) — instead of this skill when the user wants brainstorming or constructive review. After this skill when the kill report's `Suggested attack` lines need a multi-role workshop.
- [`skill-evaluator`](#skill-evaluator) — audit the verdict-vs-body consistency rule, the no-lethal-skip rule, the interactive-invitation rule.

**Try it.**
- "Grill my startup idea: a B2B SaaS for accounting firms — pre-seed, $4k MRR, two co-founders. What would kill us?"
- "I have `business-model.md` and `pitch/deck.html` ready — run the grill with the deck as primary input."
- "Defending L1. We have a 6-month cohort retention curve at 87% logo retention. Re-probe."

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

`1.0.0` marks the structural shape — a single `agent-skills` plugin with narrow skills under `skills/`. Interface-level breaking changes will still be called out; expect active iteration on individual skills.

- **Primary target agent** — Claude (Claude Code, Cowork).
- **Other agents** — may come later, no promises yet.
- **Stability** — the skills I ship here I use myself; if one stops earning its place, it gets removed rather than left to rot.

## Feedback

Issues and suggestions are welcome via [GitHub](https://github.com/sorawit-w/agent-skills/issues). Not accepting code contributions right now — feel free to fork.

## License

MIT. See [LICENSE](LICENSE).
