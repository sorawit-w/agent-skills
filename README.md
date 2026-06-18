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
  <a href="#install"><img alt="npx skills" src="https://img.shields.io/badge/any%20agent-npx%20skills%20add%20sorawit--w%2Fagent--skills-c2410c?style=flat-square"></a>
  <a href="LICENSE"><img alt="MIT license" src="https://img.shields.io/badge/license-MIT-6b7280?style=flat-square"></a>
  <a href="https://docs.claude.com/en/docs/claude-code"><img alt="built for claude code" src="https://img.shields.io/badge/built%20for-Claude%20Code%20%7C%20Cowork-c2410c?style=flat-square"></a>
</p>

---

## TL;DR

- **What this is** — a single Claude Code plugin that installs a curated, growing shelf of specialized skills in one go.
- **Who it's for** — anyone on Claude Code or Cowork who wants auto-triggering expertise for a specific job. [**Start here**](#start-here) to find yours.
- **How to start** — run the two-line install below. Each skill triggers on its own description when you describe the job — you don't have to memorize them.

## Install

**Claude Code (recommended)** — installs the full plugin: every skill, slash-command entry points, and one-step updates.

```bash
/plugin marketplace add sorawit-w/agent-skills
/plugin install agent-skills@sorawit-w
```

That's it — every skill below is now on the shelf. Works from [Claude Code](https://docs.claude.com/en/docs/claude-code), Cowork, and [OpenAI Codex](https://developers.openai.com/codex/plugins) (≥ 0.133.0) — the same `/plugin marketplace add` + `/plugin install` commands run on Codex, then `/reload-plugins`. The repo ships native manifests for both: `.claude-plugin/` for Claude Code and `.codex-plugin/plugin.json` + `.agents/plugins/marketplace.json` for Codex.

**When the plugin updates**, refresh once and reinstall:

```bash
/plugin marketplace update sorawit-w
/plugin install agent-skills@sorawit-w
```

> Claude Code caches the marketplace index locally — new skills and fixes only appear after an explicit refresh.

**Any agent — via [`npx skills`](https://github.com/vercel-labs/skills).** Works with Cursor, opencode, Claude Code, and any tool that reads `SKILL.md` files — no plugin system required.

```bash
npx skills add sorawit-w/agent-skills                          # the whole shelf
npx skills add sorawit-w/agent-skills --list                   # browse, don't install
npx skills add sorawit-w/agent-skills --skill team-composer    # just one
```

This copies the skill folders — `SKILL.md` plus their `references/`, `templates/`, and `hooks/` — into your agent's skills directory. It does **not** carry the Claude Code plugin wiring: slash-command entry points and MCP/hook *registration* come only via the marketplace path above.

> Most skills are self-contained and install cleanly on their own. A few share resources — `define` uses `i18n`'s locale data; `startup-grill`, `sub-agent-coordinator`, and `wear-the-hat` use `team-composer`'s role personas. `startup-audit` goes further: it has **hard dependencies** on `team-composer`, `validation-canvas`, and `riskiest-assumption-test` and will refuse to run if they're absent — install the full set for it. Install shared skills alongside their sibling (or just grab everything) so the references resolve.

---

<a id="start-here"></a>

## Start here — by what you're doing

New here? Find your job and jump in. The complete map is in
[`docs/skill-graph.md`](docs/skill-graph.md); each skill links to its own README
for the full usage, design notes, and cross-skill pairings.

### Building & validating a startup
*Idea to investor-ready — and each step runs standalone, so jump in anywhere.*

`brand-workshop` → `validation-canvas` → `riskiest-assumption-test` → `pitch-deck` → `startup-grill`

full chain in [How skills chain](#how-skills-chain).

[`brand-workshop`](skills/brand-workshop/README.md) — Discovery → Concept → Creation: ships a brand identity package (logo, tagline, brief, DESIGN.md tokens).

*Try:*
  - "Run the full brand workshop for my meditation startup."
  
[`validation-canvas`](skills/validation-canvas/README.md) — interview block-by-block into a rigorous Lean Canvas + Value Proposition Canvas.

*Try:*
  - "Build a validation canvas for my AI code-review tool."
  
[`riskiest-assumption-test`](skills/riskiest-assumption-test/README.md) — turn the canvas's stress-tests into falsifiable hypotheses with a risk×impact matrix + test plan.

*Try:*
  - "I just shipped my validation canvas — what should I test first?"

[`pitch-deck`](skills/pitch-deck/README.md) — structured interview → investor-ready self-contained HTML deck.

*Try:*
  - "Investor wants my seed deck by Friday — start the structured interview."
  
[`startup-grill`](skills/startup-grill/README.md) — adversarial panel → kill report with an Investable / Pivot / Pass verdict.

*Try:*
  - "Grill my startup idea: a B2B SaaS for accounting firms — what would kill us?"
  
[`startup-launch-kit`](skills/startup-launch-kit/README.md) — **orchestrator (opt-in):** runs the five steps above end-to-end with shared state.

*Try:*
  - "Build my whole startup kit for [idea] — take me through everything."
  
[`gtm`](skills/gtm/README.md) **🚧 BETA** — **after the pipeline:** phased go-to-market playbook, content, and scheduling.

*Try:*
  - "My pitch deck is ready and I want users — set up GTM for this project."
  
[`startup-audit`](skills/startup-audit/README.md) — **already built?** point at a codebase/URL → fast Continue / Pivot / Kill verdict + R/A/G band, grounded in a build-vs-claim diff.

*Try:*
  - "Grill my startup from this repo — continue, pivot, or kill?"

### Reviewing a product or AI feature
Multi-perspective critique and design-completeness checks.

[`team-composer`](skills/team-composer/README.md) — assemble a virtual team and run a 3-round discussion that forces real disagreement.

*Try:*
  - "Bring a team together to review this mobile auth architecture before we ship."
  - "Brainstorm a habit-tracker for teens — multi-perspective, no single viewpoint wins."

[`ai-ux-review`](skills/ai-ux-review/README.md) — human-AI design-completeness review; seven blocks, explicit gap markers.

*Try:*
  - "Review the UX of our LLM email-draft feature before launch — focus on trust."
  - "We shipped an agentic feature and fluent-but-wrong outputs are surfacing — walk us through the review."

[`ai-eval-review`](skills/ai-eval-review/README.md) — the eval-design sibling of `ai-ux-review`, plus a regulatory lens.

*Try:*
  - "Review the eval setup for our classification model — push on ground truth and cohort breakdown."
  - "Eval review for our medical-imaging classifier — we're FDA SaMD class II, apply regulatory rigor."

[`gamification-fit`](skills/gamification-fit/README.md) — restraint-first: finds the few places play honestly fits, refuses the rest.

*Try:*
  - "Where should I add gamification to my habit-tracker so users log 4+ days a week?"
  - "Should we gamify our expense-report flow? Goal is 90% on-time."

See also: [`validation-canvas`](skills/validation-canvas/README.md) and [`startup-audit`](skills/startup-audit/README.md) (under Startup) both double as review tools.

### Writing & shipping code
Discipline, stack choices, and parallel work.

[`cerby`](https://github.com/sorawit-w/cerby) *(external)* — opinionated agentic-coding guardrails (clarity over cleverness, safety over speed, nothing unproven passes the gate). Formerly `coding-rules` in this repo; now its own repo.

[`tech-stack-recommendations`](skills/tech-stack-recommendations/README.md) — opinionated default TS/JS stack, with named alternates.

*Try:*
  - "Starting a SaaS side-project — give me one opinionated stack I don't have to second-guess."
  - "We're migrating off Next.js on Vercel — recommend the path and name the trade-offs."

[`sub-agent-coordinator`](skills/sub-agent-coordinator/README.md) — orchestrate parallel sub-agents without drift.

*Try:*
  - "Refactor all 14 React components from class to function — coordinate in parallel."
  - "Debug our flaky CI: spawn a researcher, a fixer, and a reviewer with clear briefs."

[`wear-the-hat`](skills/wear-the-hat/README.md) — do a task in one expert's voice, solo, no panel.

*Try:*
  - "Audit `middleware/auth.ts` for missing CSRF guards as `@security_specialist`."
  - "Wear the accessibility specialist's hat for this UI review."

[`screenwright`](skills/screenwright/README.md) — paints one self-contained HTML surface, then renders it via the Playwright MCP and fixes it against an axe + fidelity gate until it passes (needs the Playwright MCP).

*Try:*
  - "Build this dashboard card to match the mockup and verify it's accessible."
  - "This component looks off on mobile — screenwright it and check the render."

### Calibration & personal voice
Make the agent yours, and write as yourself.

[`whoami`](skills/whoami/README.md) — profile how you want the agent to collaborate with you (six dials, an RPG class, a portable sheet)

*Try:*
  - "Run /whoami — I want you to actually know how I like to work."
  - "/whoami rerun — my role changed and the profile's out of date."

[`handshake`](skills/handshake/README.md) — a brief calibration ritual before real work begins.

*Try:*
  - "Calibrate how we work — I'm tired of generic answers."
  - "Run /handshake --project for this repo before the next sprint."

[`ghostwriter`](skills/ghostwriter/README.md) — draft messages in your own voice, zero AI tells.

*Try:*
  - "Reply to this email from my manager — keep it short."
  - "Tell my teammate on Slack the deploy slipped to Thursday, style=friend."

### Language & visuals

[`i18n`](skills/i18n/README.md) — surgical edits on large translation files, plus cultural rewriting.

*Try:*
  - "Translate this onboarding flow into Thai, Japanese, and Korean — cultural rewriting, not machine translation."
  - "Edit three keys in a 4,000-line `zh-CN.json` without rewriting the whole file."

[`define`](skills/define/README.md) — the true in-context meaning of a word or phrase, with a learner gloss.

*Try:*
  - "What does ออเจ้า mean in 'ออเจ้าจักไปไหน'? Give me the register and why."

[`pixel-art`](skills/pixel-art/README.md) **🚧 BETA** — a pocket pixel-art studio with a built-in design system.

*Try:*
  - "Create a hi-fi pixel-art medieval harbor at dusk with a lighthouse and three ships."
  - "Make a lo-fi pixel-art banner — three-panel, scanlined paper, VT323 title."

### Authoring & auditing skills
Building skills for this shelf? [`skill-evaluator`](skills/skill-evaluator/README.md)
audits whether a SKILL.md's rules actually land when Claude runs it — pair it with
[`team-composer`](skills/team-composer/README.md) to design and
[`sub-agent-coordinator`](skills/sub-agent-coordinator/README.md) to build. Full
authoring guide in [Building on the shelf](#building-on-the-shelf).

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

## Building on the shelf

Writing your own skill, or forking one of these? Skill authoring here is **harness engineering** — designing the context, scaffolding, and feedback loops around the agent. Start with:

- **Conventions & skill anatomy** — [`CLAUDE.md` → Skill anatomy](CLAUDE.md#skill-anatomy) (file structure, SKILL.md frontmatter, README shape, visual style).
- **The five harness primitives** — [`CLAUDE.md` → Harness vocabulary](CLAUDE.md#harness-vocabulary): context engineering, progressive disclosure, observable feedback loops, state preservation, eval discipline. The external [`cerby`](https://github.com/sorawit-w/cerby) skill is the canonical implementation.
- **The skill map** — [`docs/skill-graph.md`](docs/skill-graph.md): every skill, its audience, and how they relate.
- **Release ritual** — [`CLAUDE.md` → Release ritual](CLAUDE.md#release-ritual): the 4-file version bump + pre-shipment audit.
- **Audit a skill** — [`skill-evaluator`](skills/skill-evaluator/README.md) checks whether a skill's rules actually land when Claude runs them.

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

**Current release: `4.22.0`.** Extracted **`coding-rules`** out of this bundle into its own repo — [`sorawit-w/cerby`](https://github.com/sorawit-w/cerby) — where it ships and versions independently as **`cerby`** ("the gate guardian for agentic coding"). Existing users: switch from `/coding-rules` to the external `cerby` skill (install: `/plugin marketplace add sorawit-w/cerby`). No other skills changed. Full version history is in [CHANGELOG.md](CHANGELOG.md).

- **Primary target agent** — Claude (Claude Code, Cowork). Triggering and depth are tuned for Claude first.
- **Other agents** — skills also load on OpenAI Codex (and other `SKILL.md` consumers); `description` fields satisfy Codex's 1024-byte frontmatter limit, enforced by `scripts/check-skill-compat.py`.
- **Stability** — the skills I ship here I use myself; if one stops earning its place, it gets removed rather than left to rot.

## Feedback

Issues and suggestions are welcome via [GitHub](https://github.com/sorawit-w/agent-skills/issues). Not accepting code contributions right now — feel free to fork.

## License

MIT. See [LICENSE](LICENSE). Patterns and vocabulary adapted from third-party projects are credited in [NOTICE](NOTICE) (consolidated index) and inline in the file where each adaptation lives (authoritative).
