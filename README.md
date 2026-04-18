<p align="center">
  <img src="assets/hero.svg" alt="agent-skills — a personal shelf of Claude Code plugins" width="100%"/>
</p>

<h1 align="center">agent-skills</h1>

<p align="center">
  <em>A personal shelf of Claude Code plugins. Hand-crafted, one skill at a time.</em>
</p>

<p align="center">
  <a href="#install"><img alt="install" src="https://img.shields.io/badge/install-%2Fplugin%20marketplace%20add%20sorawit--w%2Fagent--skills-1f2937?style=flat-square"></a>
  <a href="LICENSE"><img alt="MIT license" src="https://img.shields.io/badge/license-MIT-6b7280?style=flat-square"></a>
  <a href="https://docs.claude.com/en/docs/claude-code"><img alt="built for claude code" src="https://img.shields.io/badge/built%20for-Claude%20Code%20%7C%20Cowork-c2410c?style=flat-square"></a>
</p>

---

## What this is

A single Claude Code plugin that bundles a curated shelf of narrow skills — each scoped tight, designed deliberately, and tested against its own eval set before landing on the shelf.

One install, one update, one source of truth. Pick up the whole shelf — the individual skills still auto-trigger only when their own description matches.

## Install

Add the marketplace and install in one go:

```bash
/plugin marketplace add sorawit-w/agent-skills
/plugin install agent-skills@sorawit-w
```

That's it. You get every skill below, each triggering on its own description — no extra wiring, no per-skill install step.

Works from both [Claude Code](https://docs.claude.com/en/docs/claude-code) and Cowork.

When the plugin updates, refresh once and reinstall:

```bash
/plugin marketplace update sorawit-w
/plugin install agent-skills@sorawit-w
```

Claude Code caches the marketplace index locally — new skills and fixes only appear after an explicit refresh.

## On the shelf

| Skill | What it does | Reach for it when |
|---|---|---|
| [`team-composer`](skills/team-composer) | Assemble the right virtual team and run a 3-round discussion that produces real disagreement — not restated agreement. | You want multi-perspective planning/review across tech, health, fintech, climate, games, biotech, and beyond, with a conclusion you can act on. |
| [`sub-agent-coordinator`](skills/sub-agent-coordinator) | Orchestrate multi-agent work through fan-out, pipeline, and specialist patterns — briefing templates, coordination rules, and a spawning/verification protocol. | You're starting a multi-step task that's clearly bigger than 15 minutes and at least partially parallelizable, and you want delegation that doesn't drift. |
| [`skill-evaluator`](skills/skill-evaluator) | Audit a skill to see whether its rules actually land when Claude runs it, and propose targeted rule-text fixes when they don't. | You just wrote a skill and want to stress-test it, or a skill has been "mostly working" but you suspect a rule is being silently skipped. |
| [`tech-stack-recommendations`](skills/tech-stack-recommendations) | Opinionated default tech stack (Bun + SvelteKit + Elysia + Neon + Drizzle + Clerk), two alternates (Deno / Node), and topic guides loaded on demand — with override factors named up front. | You're starting a new TypeScript/JavaScript project or picking one layer (runtime, frontend, DB, auth, hosting, mobile, i18n) and want one clear default instead of a neutral grid. |
| [`i18n-contextual-rewriting`](skills/i18n-contextual-rewriting) | Surgical edits on large translation files (JSON / YAML / TS) plus a multi-role review that turns "translate" into contextual rewriting inside cultural reality, across 15+ locales and variants. | You're editing a big i18n file without blowing past token limits, adding a new locale, or producing Thai / Japanese / Chinese / European translations that shouldn't read as machine-converted English. |
| [`brand-workshop`](skills/brand-workshop) | Assemble a virtual creative team, run a Discovery → Concept → Creation workshop, and ship a brand strategy brief, tagline, and code-generated logo. | You need a real identity package for a product, app, or startup — not just a logo doodle — with the positioning, tagline, and mark all sharing the same rationale. |
| [`business-model-canvas`](skills/business-model-canvas) | Interview a founder block-by-block and produce a rigorous 9-block Osterwalder canvas — as editable Markdown and a self-contained visual HTML — with explicit Stress Tests on the 3–5 assumptions most likely to kill the business. | You need a business model that holds up to scrutiny before building the deck, the product, or the hire plan — and want customer-first reasoning order and specificity gates enforced, not assumed. |
| [`pitch-deck`](skills/pitch-deck) | Run a structured narrative interview across the 10-slide investor arc (Title → Ask) and ship a single self-contained HTML deck + speaker notes + pre-send checklist — refusing to ship if any of the four cardinal sins (TAM-only, traction without time, teamless team, vague ask) are unfilled. | An investor said "send me your deck" and you need a shippable v1 this week with the actual content filled in, not a template waiting to be filled later. |

Each skill lives under [`skills/`](skills/) with its own `README.md`, `SKILL.md`, and reference docs.

## Design principles

These aren't rules for contributors — they're the taste I'm trying to keep on the shelf.

- **One job per skill.** Each skill on the shelf has a tight, named scope. A skill that tries to do five things does none of them well — so the bundle stays wide while each skill stays narrow.
- **Rules must land, not just exist.** A skill is a prompt dressed as policy. If the rules don't survive realistic prompts, the skill is decoration. Every skill here either has evals, or gets audited by one that does.
- **Boring and readable beats clever.** Skill text is read by humans and followed by models. Opaque indirection costs more than it saves.
- **Risk-blocking roles/checks are non-droppable.** Where a skill has explicit safety or compliance triggers, they're vetoes — not tiebreakers, not suggestions.
- **Narrow scope, named boundaries.** Every skill states what it doesn't do and when to reach for a different skill instead. Overlap is negotiated up front, not resolved mid-output.

## Status

`1.0.0` marks the structural shape — a single `agent-skills` plugin with narrow skills under `skills/`. Interface-level breaking changes will still be called out; expect active iteration on individual skills.

- **Primary target agent:** Claude (Claude Code, Cowork).
- **Other agents:** may come later — no promises yet.
- **Stability:** the skills I ship here I use myself; if one stops earning its place, it gets removed rather than left to rot.

## Feedback

Issues and suggestions are welcome via [GitHub](https://github.com/sorawit-w/agent-skills/issues). Not accepting code contributions right now — feel free to fork.

## License

MIT. See [LICENSE](LICENSE).
