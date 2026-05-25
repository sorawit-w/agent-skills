# CLAUDE.md — Working in the agent-skills repo

This file is your onboarding when working on **skill authoring in this repo**. It captures conventions, design principles, and environment quirks that took investigation to discover and are worth surfacing up-front instead of relearning each session.

**Scope:** how to author, edit, version, and ship skills inside `sorawit-w/agent-skills`. NOT general agentic-coding discipline — for that, invoke the `coding-rules` skill (it's opt-in via `/agent-skills:coding-rules` or natural-language).

**Authority:** when this file conflicts with a specific skill's own `SKILL.md` or `README.md`, the skill wins (its conventions may have evolved). This file is the *default* for new skills and the *checklist* for repo-wide changes.

---

## Quick reference

| What you need | Where it lives |
|---|---|
| New skill files | `skills/<skill-name>/` |
| Banner SVGs (LinkedIn + X formats) | `assets/<skill-name>-li.svg`, `assets/<skill-name>-x.svg` |
| Icon SVG | `assets/icons/<skill-name>.svg` |
| Skill registration | `.claude-plugin/plugin.json` **AND** `.claude-plugin/marketplace.json` (both required) |
| Plugin version | `plugin.json` + `marketplace.json` + `CHANGELOG.md` top entry + `README.md` Status section (4 files total) |
| Release notes | `CHANGELOG.md` — Keep-a-Changelog format |
| Repo-wide architectural context | Root `README.md` |
| Skill knowledge graph (nodes + edges + audience buckets) | `docs/skill-graph.md` |
| Shared role catalog | `skills/team-composer/references/role-personas.md` |
| Sub-agent brief conventions | `skills/sub-agent-coordinator/SKILL.md` |
| Coding-task discipline (opt-in) | `skills/coding-rules/` |
| Skill audit harness | `skills/skill-evaluator/` |

---

## Harness vocabulary

Skill authoring in this repo is **harness engineering** — the discipline of designing everything *around* an agent that determines whether it succeeds: context, scaffolding, feedback, state, evaluation. We already do most of this; naming the primitives lets future edits be deliberate instead of accidental.

The five primitives, with one concrete repo pointer each:

| Primitive | What it means here | Repo example |
|---|---|---|
| **Context engineering** | Organize information so the agent can reason over it. Repo-local, versioned, not in chat threads. | `SKILL.md` frontmatter `description` + `instructions` — what the agent sees before it decides to invoke. |
| **Progressive disclosure** | Load detail on demand instead of front-loading everything. The harness pattern behind `references/`. | `team-composer/references/role-personas.md` — read lazily when the skill body cites it. |
| **Observable feedback loops** | Prefer machine-checkable signal over aspirational prose. Linters, audits, structured reviewers beat "be careful." | `skill-evaluator` (rule-adherence audit) + `team-composer` Phase 6.6 (Plan-subagent structural review). |
| **State preservation** | Carry useful context across session boundaries. Skill authoring sessions are short; project work isn't. | The `coding-rules` skill's `.ai/memory.log` (append-only session log) + `.ai/STATUS.md` (current state) + `.ai/knowledge/` (curated wiki). Canonical implementation in this repo — see `skills/coding-rules/SKILL.md`. |
| **Eval discipline** | Decide what "working" means before shipping. | Pre-shipment audit ritual: `skill-evaluator` + `skill-creator` description check before version bump. |

**Canonical implementation in this repo:** the [`coding-rules`](skills/coding-rules/SKILL.md) skill. The five primitives above are vocabulary; `coding-rules` is the working machinery — `BOOTSTRAP.md` for context, `references/` for progressive disclosure, hooks like `pre-commit-check.sh` for feedback loops, `.ai/memory.log` + `.ai/STATUS.md` + `.ai/knowledge/` for state preservation, `references/quality-gates.md` for eval discipline. When this vocabulary cites a primitive abstractly, `coding-rules/SKILL.md` shows it implemented concretely.

**External reading:** Anthropic ([effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), [harness design for long-running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps)); OpenAI ([harness engineering](https://openai.com/index/harness-engineering/)); the [`AGENTS.md`](https://agents.md/) convention.

**How to use this vocabulary.** When you propose a new rule or skill change, ask: *which primitive is this serving?* If you can't answer, the change is probably speculative. When you debug a skill that "just isn't working," ask: *is the environment underspecified (context, scaffolding, feedback) or is the prompt wrong?* Most agent failures are environment failures wearing a prompt-failure mask.

---

## Skill anatomy

A complete skill ships with the files below. Existing skills are templates by example — read at least one before creating a new one (`sub-agent-coordinator`, `team-composer`, and `wear-the-hat` are recent and consistent).

| File | Required | Purpose |
|---|---|---|
| `skills/<name>/SKILL.md` | yes | YAML frontmatter + skill body |
| `skills/<name>/README.md` | yes | User-facing docs — banner at top, then standard sections |
| `skills/<name>/references/*.md` | optional | Long-tail topic guides loaded by the skill body. This is **progressive disclosure** — the harness pattern of loading detail on demand instead of front-loading everything into `SKILL.md`. |
| `skills/<name>/templates/*` | optional | Starter files the skill emits |
| `skills/<name>/commands/*.md` | optional | Slash-command entry points |
| `skills/<name>/CLAUDE.md` | optional | Skill-internal authoring rules (rare; coding-rules has one) |
| `assets/<name>-li.svg` | yes | LinkedIn banner — `viewBox="0 0 1200 627"` |
| `assets/<name>-x.svg` | yes | X/Twitter banner — `viewBox="0 0 1600 467"` |
| `assets/<name>-li.png` | optional | PNG rasterization — some skills have it, some don't |
| `assets/<name>-x.png` | optional | PNG rasterization — same |
| `assets/icons/<name>.svg` | yes | 32×32 icon, pixel-art, ink + warm accent |

### SKILL.md frontmatter

```yaml
---
name: skill-name
description: >
  What it does, when it triggers, when it does NOT trigger. Long-form prose
  is fine — this gets read by Claude to decide whether to invoke the skill.
  Be explicit about anti-triggers ("does NOT trigger on X, Y, Z").
instructions: |
  Load this skill when: ...
  Do NOT load this skill when: ...
tags:
  - <topic-tag-1>
  - <topic-tag-2>
---
```

`name` and `description` are required; `instructions` and `tags` are recommended for discoverability.

### README structure

Match the convention from `sub-agent-coordinator/README.md`, `team-composer/README.md`, or `wear-the-hat/README.md`. Order:

1. Banner image (`<p align="center"><img src=".../assets/<name>-li.svg" ...></p>`)
2. `# <skill-name>`
3. **Why this exists** — the friction this skill addresses
4. **What it does** — concrete capabilities, bulleted
5. **What it doesn't do** — anti-scope, bulleted
6. **When to use it** — situational triggers
7. **When not to use it** — when to pick a different skill
8. **How it works** — phase flow / loop / steps
9. **Design choices worth knowing** — non-obvious decisions, opinionated bits
10. **Install** — slash command sequence
11. **Cross-skill integration** — table of related skills and the relationship
12. **Status and scope** — version, what's supported / not
13. **Contributions** — "not accepting external contributions right now"
14. **License** — MIT

Length: 80–200 lines is normal. Past 250 lines, ask whether the long bits belong in a `references/*.md` instead.

---

## Release ritual

### Version bumping — 4 files, every time

A version bump touches exactly these four files. Miss one and the manifest is inconsistent:

1. `.claude-plugin/plugin.json` — `version` field
2. `.claude-plugin/marketplace.json` — `version` field (same value)
3. `CHANGELOG.md` — new entry at the top using `## [<version>] — <YYYY-MM-DD>` heading
4. `README.md` Status section — update the one-line **Current release** blurb (new version number + a one-sentence summary of what's newest). The Status section carries only the current-release pointer; full per-version history lives in `CHANGELOG.md`.

### When the release ADDS a new skill — root README needs five more touches

The Status section bump is not enough on its own. A new skill must also appear in the root README's catalog and navigation, plus the skill graph, or it stays invisible to readers browsing the repo:

5. **TL;DR count** (~line 22) — the "a curated shelf of N specialized skills" line. Increment `N`.
6. **"The shelf" table** — add a row: icon image, skill name linked to its own README (`skills/<name>/README.md`), and a "What it's for" one-liner. Three columns — match the existing structure exactly. Place the row next to thematically-related skills (e.g., role/delegation skills cluster near `team-composer` and `sub-agent-coordinator`).
7. **"Skill details" section** — add a trimmed detail entry: anchor `<a id="skill-name"></a>`, H3 with icon image and the skill name **linked to its README** (`skills/<name>/README.md`), then a `**Pairs well with**` block (bulleted, each link pointing to another skill's README) and a `**Try it**` block (3 example prompts). No "What it does" / "Reach for it when" prose — that lives in the skill's own README. Place near related skills in the same order as the shelf table.
8. **"Start here" audience map** (README) — add the new skill to ≥1 job-to-be-done row of the `## Start here` section. One link entry into the skill's Skill-details anchor; do **not** re-describe the skill (the row is a link index, not a second catalog). Every skill must appear in at least one audience row.
9. **Skill graph** (`docs/skill-graph.md`) — add a node row to the table (name, purpose, audience, status, bucket) and any new relationship edges to the Mermaid graph. This is the canonical map the README's "Start here" and "Building on the shelf" sections point at.

Skipping any of these is the failure mode caught after shipping `wear-the-hat` in 3.6.0 — the skill existed and was registered in the plugin manifest, but was invisible in the root README catalog. Status section mentions only persist until the next release demotes them; the catalog is permanent.

**Optional polish for new skills:** update the `**Pairs well with**` bullets in adjacent skills' detail entries so cross-references are bidirectional (e.g., when adding `wear-the-hat`, mention it under `team-composer` and `sub-agent-coordinator`'s "Pairs well with" lists too). Treat as nice-to-have, not blocker.

### Semver — what counts as what

- **MAJOR** (`X.0.0`): breaking changes to existing skills' triggers, output shapes, or contracts. Users would need to migrate.
- **MINOR** (`3.X.0`): new skill added, new feature within an existing skill, backwards-compatible additions.
- **PATCH** (`3.5.X`): bug fixes, doc tweaks, adherence-only patches — no behavior change.

Recent precedent: adding a new skill = MINOR; fixing executor-brief template gaps = PATCH; consolidating sub-agent conventions across existing skills (additive only) = MINOR.

### Pre-shipment audit ritual

For changes to a `SKILL.md` (rule text or trigger description), run the audit *before* bumping:

1. Invoke `skill-evaluator` on the changed skill — split-context audit removes author bias.
2. Invoke `skill-creator`'s description-check on the SKILL.md frontmatter description.

Self-review by the same agent that wrote the changes reliably misses rule-adherence bugs. The audit catches gaps that self-review can't.

The audit is required for SKILL.md *text* changes. Pure doc additions (CHANGELOG, README, banner edits, reference-file additions) don't require it.

### CHANGELOG entry shape

Each release entry follows Keep-a-Changelog format:

```markdown
## [<version>] — <YYYY-MM-DD>

<One-paragraph summary of what the release does.>

### Added
- <thing added>

### Changed
- <thing changed>

### Why
<Multi-paragraph context for non-obvious decisions. Capture reasoning, not just changes.>

### Notes
- <Migration notes, gotchas, compat statements>
```

Not every section is required for every release. `Added` / `Changed` / `Fixed` / `Removed` / `Deprecated` are the standard buckets; use what fits.

---

## Visual style

All banners and icons follow a consistent pixel-art aesthetic. Match the existing work; don't introduce a new visual language for a new skill.

### Banner format

- `-li.svg` dimensions: `viewBox="0 0 1200 627"`. Title centered at top.
- `-x.svg` dimensions: `viewBox="0 0 1600 467"`. Title top-left.
- **Background:** scanlined warm paper via an SVG `<pattern>` of `#f5efe6` rows with `#eadfcf` 2px stripes every 6px.
- **Typography:** `font-family="ui-monospace, SFMono-Regular, Menlo, monospace"` throughout. Title 38–44px bold; subtitle 18–20px regular; chapter markers 11–13px with `letter-spacing` 3–4px.
- **Composition:** three-panel layout is the standard — left card (context/input), center card (the skill's signature move, often colored warm accent), right card (output). Pixel-art arrows between cards in `#6b7280` (entering) → `#c2410c` (exiting). Chapter markers in a row below the cards.
- **Pixel crispness:** `shape-rendering="crispEdges"` plus `style="image-rendering: pixelated; image-rendering: crisp-edges;"` on every banner.
- **Accessibility:** include `role="img"`, `aria-label`, `<title>`, `<desc>` on every SVG.

### Icon format

- `viewBox="0 0 32 32"`.
- 2-color palette: `#1f2937` (ink) + `#c2410c` (warm accent). Third colors are rare (e.g., skill-evaluator's `#0d7c3c` check).
- Pixel-art, no antialiasing (`shape-rendering="crispEdges"`).
- `aria-label`, `<title>` required.

### Canonical color palette

Match these exact hex codes — don't introduce a new palette for a new skill.

| Token | Hex | Use |
|---|---|---|
| Paper | `#f5efe6` | Banner background base |
| Paper edge | `#eadfcf` | Scanlines, ground lines |
| Card paper (warm) | `#f3e7c9`, `#fdf7ea` | Card backgrounds |
| Card border (wood) | `#b79a5c`, `#c9b58a` | Card edges, rack bars |
| Ink | `#1f2937` | Primary text, icon outlines, dark fills |
| Warm accent | `#c2410c` | Arrows, highlights, attention markers, hatband |
| Yellow chip | `#fde68a`, `#fbbf24` | Status chips, warnings, hardhat dome |
| Blue chip | `#bae6fd`, `#0e7490` | Information chips, sub-agent tiles |
| Green pass | `#15803d`, `#dcfce7`, `#0d7c3c` | DONE seals, check marks, validation |
| Red flag | `#b91c1c`, `#fecaca` | OUT-of-scope markers, errors, beret |
| Muted | `#6b7280`, `#9ca3af` | Secondary text, placeholder bars |
| Wood / leather | `#8b6f3c`, `#92400e` | Wooden rack bars, hardhat outlines |

---

## Shared resources — don't fork, extend in place

Some assets are deliberately shared across skills. When you need them, **reference the canonical source — don't copy** into your new skill.

### Role catalog

`skills/team-composer/references/role-personas.md` is the canonical role vocabulary for the repo. Three consumers reference it: `team-composer` (panel assembly + discussion), `sub-agent-coordinator` (optional `Role:` tag in briefs), `wear-the-hat` (single-role embodiment).

When you need a new role or want to refine an existing one, edit `role-personas.md` *in place*. The change propagates to all three consumers. Do NOT create parallel role taxonomies inside other skills.

### Sub-agent brief conventions

`skills/sub-agent-coordinator/SKILL.md` is the canonical home for:

- Spawning signals (when to delegate)
- Briefing templates (Quick Brief / Full Brief)
- Coordination patterns (fan-out, pipeline, specialist, review)
- Model selection axes (capability tier × reasoning effort × speed lane)
- Picking the role guidance
- `BLOCKED_SCOPE_EXPANDED` escalation protocol

Skills that need any of this reference the relevant section in coordinator. `coding-rules` and `team-composer` are the existing thin-pointer examples.

### Other shared things to be aware of

- `coding-rules/resources/BOOTSTRAP.md` — opinionated agentic-coding rules. Opt-in via the coding-rules skill.
- `team-composer` Phase 6 — references `sub-agent-coordinator` for model routing / role-picking / deliverable fan-out.
- `skill-evaluator` — the split-context audit harness for SKILL.md rule-adherence reviews.

If you're tempted to copy from one skill into another, first check whether the source is meant to be shared. Almost always: reference, don't copy.

---

## Design principles

These principles emerged across multiple skill designs in this repo. Apply them by default when designing new skills or extending existing ones. They're defaults, not laws — name them explicitly when proposing alternatives so the trade-off is visible.

### 1. Capability-gated routing, not vendor-gated routing

Gate on "is the tool / sub-agent / skill available in this runtime?" — NOT on "is the agent Claude / Cowork / Claude Code?" Vendor identity is brittle and often undetectable from inside a skill.

**Why:** new platforms emerge constantly. A skill that hardcodes "if Claude Code, do X; if Cowork, do Y" rots when a third platform appears. A skill that gates on "if `sub-agent-coordinator` is loaded, hand off; otherwise fall back to sequential" survives.

### 2. Asymmetric reviewer / author contracts

When adding a sub-agent reviewer to an artifact already authored by an in-context persona, the reviewer returns a *structured critique*. The original author keeps authorship and final-edit rights. Do not add a co-author — it produces two competing voices and no clear final.

**Why:** the Phase 6.6 Plan-subagent route in `team-composer` is the canonical example. The Plan subagent reviews; `@staff_engineer` authors. If both authored, the output is a forest of design docs instead of one executable plan.

### 3. Staged rollout with conservative initial trigger

New sub-agent routes or auto-trigger thresholds ship gated on the most conservative trigger first (e.g., `complexity=high`), with an explicit second-stage threshold-lowering plan gated on observed cost / latency / value-yield criteria.

**Why:** lowering a trigger threshold after observing real usage is easy. Raising one after users built expectations on it is hard. Ship conservative, observe, then expand.

### 4. Orthogonal axes over flat ladders

When designing tier / role / capability taxonomies, prefer multiple independent axes over compound flat ladders.

The sub-agent-coordinator Model Selection precedent: capability tier (low/std/high) + reasoning effort (off/on) + speed lane (flex/std/priority) shipped as three orthogonal axes, NOT as one 4- or 5-rung ladder. Flat ladders mash dimensions together, hide useful configs ("standard tier + thinking on" disappears when thinking-on becomes a tier above standard), and break across vendors.

**Why:** orthogonal axes preserve composability. A flat ladder forces every consumer to accept the merged dimensions; orthogonal axes let each consumer pick independently.

### 5. Framework vs. opinion test (corollary to #4)

When drafting an "opinionated overlay" on top of a framework, row-by-row ask: "would any thoughtful team converge here?" If yes, it's a defensible default, not taste — promote it to the framework layer. The overlay should contain only what's genuinely opinionated.

**Example:** the sub-agent-coordinator coding-work mapping (10 rows) started in `coding-rules` as an "opinionated overlay." On review, 9 of 10 rows were universal defaults, not personal taste — they got promoted to coordinator's `Default Mapping (Coding Work)`. coding-rules became a thin pointer.

**Why:** the temptation is to draw the framework/opinion line along skill boundaries (coordinator = framework; coding-rules = opinion). The real line is along *actual taste* — and most calibration matrices have more defensible defaults than they look like at first.

### 6. Observable feedback loops over aspirational prose

Prefer constraints the harness can *check* over rules only a careful human reviewer can verify. Aspirational prose ("be rigorous", "consider edge cases") drifts on contact with real runs; structured reviewers, linters, and audit rituals do not.

**Examples in this repo:**
- `team-composer` Phase 6.6 — a `Plan` subagent reviews the draft Structured Plan and returns ranked findings. The check happens; "be rigorous" is reified.
- `skill-evaluator` — split-context audit that asks "does the text land?" instead of trusting self-review.
- Pre-shipment audit ritual — `skill-evaluator` + description check run before every version bump that touches SKILL.md.
- The four-file version bump in this CLAUDE.md — concrete checklist beats "remember to update the manifest."

**Reactive corollary.** Every line of a good rule traces to a specific past failure. If you can't name the failure you're preventing, the rule is speculative — it belongs in `docs/` or a `references/` file until a real incident promotes it.

**Why:** harness engineering literature converges on this — "the fix is almost never *try harder*; it's *make the missing capability legible and enforceable.*" Prose rules ask the agent to try harder. Feedback loops give the agent (or auditor) something to check against.

### 7. Prose economy — every word load-bearing

When authoring SKILL.md rule text, cut any word that doesn't change what the agent does. Two failure shapes: **prose bloat** (restating, hedging, padding) and **vague phrasing** (soft verbs/adjectives — "handle appropriately", "be thorough" — where a precise operation removes the guesswork).

**Caveat:** economy serves clarity, not brevity for its own sake — a *why* line that prevents a misread earns its tokens. This is the reactive corollary (#6) applied to prose: cut what prevents nothing, keep what prevents a misread.

**Why:** the SKILL.md body is context the agent reloads before every decision, so bloat there is paid on every run. `skill-evaluator`'s harness lens checks this at audit time (question 7); this principle is the authoring-time version. Pattern adapted from `nidhinjs/prompt-master` (MIT).

---

## What's NOT here

For depth on topics this file deliberately skims:

| Topic | Where |
|---|---|
| Full release notes per version | `CHANGELOG.md` |
| Repo architecture and philosophy | Root `README.md` |
| General agentic-coding discipline | `coding-rules` skill (opt-in) |
| SKILL.md rule-adherence auditing | `skill-evaluator` skill |
| Skill creation walkthrough | Anthropic's `skill-creator` skill |
| Banner pixel-art examples | Existing `assets/<skill>-li.svg` files |
| Cross-skill integration patterns | Each skill's `## Cross-skill integration` section |

When in doubt, **read an existing skill as a template** rather than guessing. The conventions are mostly observable. This file is the shortcut, not the whole map.

---

*Maintenance note:* if you change a convention in the repo (visual style, file structure, release ritual, etc.), update this file as part of the same change. A stale CLAUDE.md is worse than no CLAUDE.md — readers will follow incorrect instructions.
