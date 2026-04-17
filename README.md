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

A small, curated marketplace of Claude Code plugins. Each plugin bundles exactly one skill — narrow in scope, deliberate in design, tested against its own eval set before it lands on the shelf.

No mega-plugins, no loose bags of helpers. Pick up the skills you want, one at a time, and leave the rest.

## Install

Add the marketplace once:

```bash
/plugin marketplace add sorawit-w/agent-skills
```

Then either install a single plugin by name:

```bash
/plugin install <plugin-name>@sorawit-w
```

…or grab the whole shelf in one command:

```bash
/plugin install agent-skills@sorawit-w
```

The `agent-skills` plugin is a meta-plugin — it ships no skill of its own, just lists every other plugin in this marketplace as a dependency. Installing it pulls them all in. Pin a specific version of `agent-skills` if you want a frozen set.

Works from both [Claude Code](https://docs.claude.com/en/docs/claude-code) and Cowork.

If a newly-added plugin isn't showing up, refresh the marketplace:

```bash
/plugin marketplace update sorawit-w
```

Claude Code caches the marketplace index locally and doesn't re-fetch on every command — new plugins appear only after an explicit refresh.

## On the shelf

| Plugin | What it does | Reach for it when |
|---|---|---|
| [`brand-workshop`](plugins/brand-workshop) | Assemble a virtual creative team, run a Discovery → Concept → Creation workshop, and ship a brand strategy brief, tagline, and code-generated logo. | You need a real identity package for a product, app, or startup — not just a logo doodle — with the positioning, tagline, and mark all sharing the same rationale. |
| [`team-composer`](plugins/team-composer) | Assemble the right virtual team and run a 3-round discussion that produces real disagreement — not restated agreement. | You want multi-perspective planning/review across tech, health, fintech, climate, games, biotech, and beyond, with a conclusion you can act on. |
| [`skill-evaluator`](plugins/skill-evaluator) | Audit a skill to see whether its rules actually land when Claude runs it, and propose targeted rule-text fixes when they don't. | You just wrote a skill and want to stress-test it, or a skill has been "mostly working" but you suspect a rule is being silently skipped. |
| [`sub-agent-coordinator`](plugins/sub-agent-coordinator) | Orchestrate multi-agent work through fan-out, pipeline, and specialist patterns — briefing templates, coordination rules, and a spawning/verification protocol. | You're starting a multi-step task that's clearly bigger than 15 minutes and at least partially parallelizable, and you want delegation that doesn't drift. |

Each plugin lives under [`plugins/`](plugins/) with its own `README.md` at the root, plus a `SKILL.md`, reference docs, and evals inside `skills/<name>/`.

## Design principles

These aren't rules for contributors — they're the taste I'm trying to keep on the shelf.

- **One skill per plugin.** Composable, inspectable, easy to uninstall. A skill that tries to do five things does none of them well.
- **Rules must land, not just exist.** A skill is a prompt dressed as policy. If the rules don't survive realistic prompts, the skill is decoration. Every skill here either has evals, or gets audited by one that does.
- **Boring and readable beats clever.** Skill text is read by humans and followed by models. Opaque indirection costs more than it saves.
- **Risk-blocking roles/checks are non-droppable.** Where a skill has explicit safety or compliance triggers, they're vetoes — not tiebreakers, not suggestions.
- **Narrow scope, named boundaries.** Every skill states what it doesn't do and when to reach for a different skill instead. Overlap is negotiated up front, not resolved mid-output.

## Status

Early-stage. Versions stay below `1.0.0` while interfaces stabilize. Breaking changes are possible but will be called out.

- **Primary target agent:** Claude (Claude Code, Cowork).
- **Other agents:** may come later — no promises yet.
- **Stability:** the skills I ship here I use myself; if one stops earning its place, it gets removed rather than left to rot.

## Feedback

Issues and suggestions are welcome via [GitHub](https://github.com/sorawit-w/agent-skills/issues). Not accepting code contributions right now — feel free to fork.

## License

MIT. See [LICENSE](LICENSE).
