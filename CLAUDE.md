# CLAUDE.md — Working in the agent-skills repo

This file is your onboarding when working on **skill authoring in this repo**. It captures conventions, design principles, and environment quirks that took investigation to discover and are worth surfacing up-front instead of relearning each session.

**Scope:** how to author, edit, version, and ship skills inside `sorawit-w/agent-skills`. NOT general agentic-coding discipline — for that, see the external [`kerby`](https://github.com/sorawit-w/kerby) skill (formerly `coding-rules` in this repo, now its own repo).

**Authority:** when this file conflicts with a specific skill's own `SKILL.md` or `README.md`, the skill wins (its conventions may have evolved). This file is the *default* for new skills and the *checklist* for repo-wide changes.

---

## Quick reference

| What you need | Where it lives |
|---|---|
| New skill files | `skills/<skill-name>/` |
| Banner SVGs (LinkedIn + X formats) | `assets/<skill-name>-li.svg`, `assets/<skill-name>-x.svg` |
| Icon SVG | `assets/icons/<skill-name>.svg` |
| Skill registration | Claude Code: `.claude-plugin/plugin.json` **AND** `.claude-plugin/marketplace.json`. Codex: `.codex-plugin/plugin.json` (`"skills": "./skills/"`) **AND** `.agents/plugins/marketplace.json`. All four required — Claude and Codex schemas collide on the `skills`/`source` keys, so they cannot share one file. |
| Plugin version | `.claude-plugin/plugin.json` + `.claude-plugin/marketplace.json` + `.codex-plugin/plugin.json` + `CHANGELOG.md` top entry + `README.md` Status section (**5 version-bearing files**; `.agents/plugins/marketplace.json` carries no version). `scripts/check-skill-compat.py` asserts parity across them. |
| Release notes | `CHANGELOG.md` — Keep-a-Changelog format |
| Repo-wide architectural context | Root `README.md` |
| Skill knowledge graph (nodes + edges + audience buckets) | `docs/skill-graph.md` |
| Shared role catalog | `skills/team-composer/references/role-personas.md` |
| Sub-agent brief conventions | `skills/sub-agent-coordinator/SKILL.md` |
| Coding-task discipline (opt-in) | external [`kerby`](https://github.com/sorawit-w/kerby) repo (formerly `coding-rules` here) |
| Skill audit harness | `skills/skill-evaluator/` |
| Cross-platform frontmatter checker | `scripts/check-skill-compat.py` (Codex `SKILL.md` rules) |

---

## Harness vocabulary

Skill authoring in this repo is **harness engineering** — the discipline of designing everything *around* an agent that determines whether it succeeds: context, scaffolding, feedback, state, evaluation. We already do most of this; naming the primitives lets future edits be deliberate instead of accidental.

The five primitives, with one concrete repo pointer each:

| Primitive | What it means here | Repo example |
|---|---|---|
| **Context engineering** | Organize information so the agent can reason over it. Repo-local, versioned, not in chat threads. | `SKILL.md` frontmatter `description` + `instructions` — what the agent sees before it decides to invoke. |
| **Progressive disclosure** | Load detail on demand instead of front-loading everything. The harness pattern behind `references/`. | `team-composer/references/role-personas.md` — read lazily when the skill body cites it. |
| **Observable feedback loops** | Prefer machine-checkable signal over aspirational prose. Linters, audits, structured reviewers beat "be careful." | `skill-evaluator` (rule-adherence audit) + `team-composer` Phase 6.6 (Plan-subagent structural review). |
| **State preservation** | Carry useful context across session boundaries. Skill authoring sessions are short; project work isn't. | The external `kerby` skill's `.ai/memory.log` (append-only session log) + `.ai/STATUS.md` (current state) + `.ai/knowledge/` (curated wiki). Canonical implementation — see the [`kerby`](https://github.com/sorawit-w/kerby) repo. |
| **Eval discipline** | Decide what "working" means before shipping. | Pre-shipment audit ritual: `skill-evaluator` + `skill-creator` description check before version bump. |

**Canonical implementation:** the external [`kerby`](https://github.com/sorawit-w/kerby) skill (formerly `coding-rules` in this repo, now extracted). The five primitives above are vocabulary; `kerby` is the working machinery — `BOOTSTRAP.md` for context, `references/` for progressive disclosure, hooks like `pre-commit-check.sh` for feedback loops, `.ai/memory.log` + `.ai/STATUS.md` + `.ai/knowledge/` for state preservation, `references/quality-gates.md` for eval discipline. When this vocabulary cites a primitive abstractly, the `kerby` repo shows it implemented concretely.

**External reading:** Anthropic ([effective harnesses for long-running agents](https://www.anthropic.com/engineering/effective-harnesses-for-long-running-agents), [harness design for long-running apps](https://www.anthropic.com/engineering/harness-design-long-running-apps)); OpenAI ([harness engineering](https://openai.com/index/harness-engineering/)); the [`AGENTS.md`](https://agents.md/) convention.

**How to use this vocabulary.** When you propose a new rule or skill change, ask: *which primitive is this serving?* If you can't answer, the change is probably speculative. When you debug a skill that "just isn't working," ask: *is the environment underspecified (context, scaffolding, feedback) or is the prompt wrong?* Most agent failures are environment failures wearing a prompt-failure mask.

### Control loop (loop engineering)

Prompt engineering optimizes a single forward pass. **Loop engineering** optimizes the trajectory across many passes: the agent acts, observes a result (test output, build error, screenshot), and that observation re-enters context and shapes the next action. It is the runtime-control-flow half of harness engineering — the harness is the static scaffolding, the loop is what drives it over time.

The external `kerby` skill (formerly `coding-rules` here) implements the loop primitives. This table is the map so the spine is legible in one place; each row points to where the primitive is enforced — the "Lives in" paths below are in the [`kerby`](https://github.com/sorawit-w/kerby) repo.

| Primitive | One-line meaning | Lives in |
|---|---|---|
| Inner / outer check split | cheap check while coding, full gate at the boundary | `resources/workflows/feature.md` (iteration-check tiers vs commit check) |
| Termination condition | what must be true to exit the loop | `resources/references/validation.md` (Iron Law: no claim without fresh evidence) |
| Retry budget / circuit breaker | bounded retries per failure type, then escalate | `resources/references/error-handling.md` (build 5 / test 3 / lint 5 → BLOCKED) |
| Bounded search | cap the hypothesis count so the loop can't flail | `resources/references/debugging.md` (max 3 hypotheses) |
| State across iterations | what carries forward so the loop has no amnesia | `.ai/memory.log`, `.ai/STATUS.md`, checkpoint-before-context-fills |
| Iteration cost is the speed limit | a faster loop buys more hypotheses | `resources/references/debugging.md` (assess the feedback loop first) |
| Parallel loops (fan-out) | independent iterations run concurrently | `resources/references/sub-agent-delegation.md` (vertical slices, blind lenses) |

These are the runtime expression of the harness primitives above, not a second taxonomy: *State across iterations* is *State preservation* applied mid-task, and the two check rows are *Observable feedback loops* applied per-iteration. The rest (termination, retry budget, bounded search, fan-out) are loop-specific. When in doubt about which table owns a concern, the harness table is the noun and this one is the verb.

Lives in the authoring context, not `kerby`'s `BOOTSTRAP.md` — zero cost for `kerby` *consumers* (this table does load for sessions working in this repo, so keep it tight).

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
| `skills/<name>/CLAUDE.md` | optional | Skill-internal authoring rules (rare; the external `kerby` skill has one) |
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
  What it does, when it triggers, when it does NOT trigger. This gets read by
  Claude to decide whether to invoke the skill, so be explicit about anti-triggers
  ("does NOT trigger on X, Y, Z") — but keep it ≤1024 characters (see the
  cross-platform contract below); overflow detail belongs in `instructions`/body.
instructions: |
  Load this skill when: ...
  Do NOT load this skill when: ...
tags:
  - <topic-tag-1>
  - <topic-tag-2>
---
```

`name` and `description` are required; `instructions` and `tags` are recommended for discoverability.

#### Cross-platform frontmatter contract — keep skills loadable on Codex too

Claude Code imposes no length limit on `description`, but **OpenAI Codex silently skips any skill whose `SKILL.md` violates its frontmatter rules** — no error in the loop, the skill just never appears. Because `description` is a *single shared field* (Codex has no per-platform override at the frontmatter level — the `interface` block in `.codex-plugin/plugin.json` is plugin-level UI metadata, not per-skill triggering), every skill here must satisfy the stricter Codex contract. We prioritize Claude's triggering quality *within* that ceiling — keep the trigger phrases and the load-bearing disambiguation boundaries, and push genuinely overflowing detail into `instructions` (still read by Claude) or the body, never drop a real boundary to save characters.

| Field | Codex rule (violation ⇒ skill skipped) |
|---|---|
| `description` | **1–1024 in length, measured as Unicode _characters_** (Codex's Rust loader uses `value.chars().count()` against `MAX_DESCRIPTION_LEN = 1024`). The earlier byte-counting bug ([openai/codex#7730](https://github.com/openai/codex/issues/7730)) is **fixed** — current Codex counts characters, and there is **no** `<`/`>` restriction. |
| `name` | matches `^[a-z0-9]+(-[a-z0-9]+)*$`, ≤64 bytes (no leading/trailing/double hyphen). Codex's own rule is laxer (`^[a-zA-Z0-9_-]+$`), so our lowercase-hyphen house style is a safe subset. |
| entry file | named exactly `SKILL.md` (all caps). |

**Enforced by `scripts/check-skill-compat.py`** — run it after any frontmatter edit and before a version bump. It fails (exit 1) on any hard violation and warns at a 1000-character soft cap to keep headroom before the 1024 wall. It also asserts version parity across the release manifests. This is the observable feedback loop (principle #6) for the constraint; don't hand-count characters.

> **History:** through v4.14.0 this checker enforced 1024 *bytes* + a `<`/`>` ban, mirroring Codex's behavior at the time of the #7730 report. v4.15.0 corrected it to characters and dropped the angle-bracket ban to match current Codex; the byte-strict version drove an unnecessary trim in v4.11.0. If you ever need to support a *pre-#7730* Codex, byte-strictness is the thing to restore.

#### Codex marketplace discovery — known limitation (we are Claude-first)

**Codex's plugin marketplace only discovers plugins in a `./plugins/<name>/` subdirectory** (each self-contained with its own `.codex-plugin/plugin.json` + `skills/`), per [the Codex build docs](https://developers.openai.com/codex/plugins/build). Our **root layout** — `.claude-plugin/plugin.json` + `./skills/` at the repo root, which Claude Code needs — is therefore **not discoverable by Codex's `/plugin marketplace add`**. Verified empirically: neither `"path": "."` nor `"./"` in `.agents/plugins/marketplace.json` resolves; Codex shows nothing.

**Decision (2026-06-18): Claude-first, park Codex.** We do not contort the working root layout for Codex — Claude Code is the priority. The `.agents/plugins/marketplace.json` + `.codex-plugin/plugin.json` stay **dormant/forward-compat** (still version-synced so `check-skill-compat.py` parity holds), and **`npx skills add <owner/repo>`** remains the working cross-platform install path — it reads `SKILL.md` directly, no marketplace needed. The Codex *frontmatter* contract above still matters for that `npx` path. A both-worlds layout (skills moved under `plugins/<name>/skills/`, both manifests pointing there) is achievable but adds path depth and risks the Claude layout — declined unless Codex parity becomes a hard requirement. So "All four required" in the registration row above is true for *file presence + parity*, not for Codex marketplace discovery.

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

### Version bumping — 5 files, every time

A version bump touches exactly these five version-bearing files. Miss one and `scripts/check-skill-compat.py` fails the parity check:

1. `.claude-plugin/plugin.json` — `version` field
2. `.claude-plugin/marketplace.json` — `version` field (same value)
3. `.codex-plugin/plugin.json` — `version` field (same value; Codex-native manifest)
4. `CHANGELOG.md` — new entry at the top using `## [<version>] — <YYYY-MM-DD>` heading
5. `README.md` Status section — update the one-line **Current release** blurb (new version number + a one-sentence summary of what's newest). The Status section carries only the current-release pointer; full per-version history lives in `CHANGELOG.md`.

(`.agents/plugins/marketplace.json` — the Codex marketplace — carries no version field, so it's not in the parity set, but keep its plugin metadata in sync when other manifest fields change.)

### When the release ADDS a new skill — root README needs two more touches

The Status bump is not enough on its own. A new skill must also appear in the README's routing and the skill graph, or it stays invisible to readers browsing the repo:

5. **Start-here grouped section** — add the skill to its **primary group** (the group matching its primary-audience column in `docs/skill-graph.md`). Each entry is: one reader-facing one-liner faithful to the skill's Purpose in `skill-graph.md` (tighten the catalog text for voice, but don't drop load-bearing terms or introduce new claims — the graph is the source of meaning, the README is the punchier register) plus **up to two example prompts** that teach its trigger phrasing, each on its own nested bullet. Single-mode skills may use one prompt; two is the ceiling. Place next to thematically-related skills. A cross-listed skill gets a full entry in exactly ONE primary group; elsewhere it's a bare "see also" link with no description and no prompts. Authoring/meta skills (e.g. `skill-evaluator`) go under "Building on the shelf" instead of a Start-here group, reachable via the one-line authoring pointer in the grouped section. The Startup group keeps a pipeline *flow line* on top (`brand-workshop → … → startup-grill`) above its per-skill entries, and tags the off-pipeline skills inline (`startup-launch-kit` orchestrator, `gtm` after-the-pipeline, `startup-audit` already-built) — otherwise it's the same per-skill menu shape as the other groups.
6. **Skill graph** (`docs/skill-graph.md`) — add a node row (name, purpose, audience, status, bucket) and any new edges to the Mermaid graph. This is the canonical map **and** the one-liner source for item 5.

No skill-count number to bump anywhere — the README and `skill-graph.md` deliberately avoid a hardcoded "N skills" count (it drifts, and `ls skills/` over-counts non-skill dirs like `gtm-workspace`; the authoritative count is `plugin.json`'s skills array). Don't reintroduce one.

**Per-skill detail — usage, `Pairs well with`, the full example-prompt set — lives ONLY in the skill's own `README.md`. Never copy it into the root README.** The grouped section routes; the skill README explains. (This is the rule whose violation bloated the README to ~590 lines before the 4.10.1 presentation reorg, which deleted the old per-skill "Skill details" section and the flat "The shelf" table.)

Skipping any of these is the failure mode caught after shipping `wear-the-hat` in 3.6.0 — the skill was registered in the plugin manifest but invisible in the README routing. The grouped-section entry and the skill-graph node are permanent; the Status-section mention is demoted at the next release.

**Optional polish for new skills:** keep cross-references bidirectional in each skill's own `Pairs well with` block (that lives in the skill READMEs now, not the root README). Treat as nice-to-have, not blocker.

### Semver — what counts as what

- **MAJOR** (`X.0.0`): breaking changes to existing skills' triggers, output shapes, or contracts. Users would need to migrate.
- **MINOR** (`3.X.0`): new skill added, new feature within an existing skill, backwards-compatible additions.
- **PATCH** (`3.5.X`): bug fixes, doc tweaks, adherence-only patches — no behavior change.

Recent precedent: adding a new skill = MINOR; fixing executor-brief template gaps = PATCH; consolidating sub-agent conventions across existing skills (additive only) = MINOR.

### Pre-shipment audit ritual

For changes to a `SKILL.md` (rule text or trigger description), run the audit *before* bumping:

1. Run `python3 scripts/check-skill-compat.py` — the mechanical gate. Any frontmatter edit can push `description` over Codex's 1024-character wall (or trip the `name` rule); this catches it before the skill silently stops loading on Codex, and also asserts version parity across the release manifests. Cheap, deterministic, always run it.
2. Run `skill-evaluator` on the changed skill **in the main loop** — then `skill-creator`'s description-check on the frontmatter description.

A pure description-length trim (no change to trigger phrases or boundaries) clears step 1 mechanically; step 2's value is confirming the *compressed* description still triggers as well as the long one, which is best done in a separate session (outer-bias insulation, below).

**Run it in the main loop, not as a sub-agent.** `skill-evaluator`'s bias removal *is* its Phase 4: it spawns fresh-context executor + grader sub-agents (the grader never sees the skill text). That only works where it can spawn sub-agents — the main loop. Dispatch `skill-evaluator` *itself* as a sub-agent and no-nested-sub-agents silently collapses Phase 4 into in-context simulation — you get a confident-looking verdict with the bias removal gone. (This bit us in v4.5.0; `skill-evaluator` now emits a `DEGRADED` banner instead of simulating silently — but don't rely on the banner, invoke it right.)

**Two bias levels.** *Inner* (execute-vs-grade) is removed by Phase 4's split — you get this for free in the main loop. *Outer* (the author orchestrates the audit and reads the verdict) is not removed by running the skill; for outer insulation when you just wrote the skill, run it in a **separate session**, never by nesting. Self-review by the same agent that wrote the changes reliably misses rule-adherence bugs.

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

## Library conventions

Authoring a *single* skill — draft → test → iterate → optimize the description — is owned by Anthropic's `skill-creator`. Use it; reference it; do not restate it here. This section covers only what `skill-creator` doesn't: how a skill behaves **inside a growing library**. Two failure modes never show up in single-skill evaluation (which scores against a no-skill baseline, in isolation) — they appear only once skills co-load.

### The library gate — run before merging a new or changed skill

- **Routing regression — does the new skill steal triggering from a neighbor?** Keep a small trigger-eval set per skill under `.eval/triggers/<skill>.json` (the existing `.eval/` shape — an array of `{ "query": ..., "should_trigger": true|false }`, with at least one *neighbor-steal* case for skills that have adjacent siblings). Before merging skill N, read the *existing* sets **together with** N present, not one at a time. If a previously-passing skill now mis-fires, the descriptions overlap — sharpen the "does NOT trigger on…" boundary (the cross-platform `description`, then `instructions`/body) before merge. This is the one net-new mechanism: `skill-creator` and `skill-evaluator` both audit a skill *alone*, so neither sees a cross-skill collision.
- **Co-load token budget — is the body lean enough to ride alongside 5–15 active skills?** No new rule — this is already enforced by progressive disclosure (push detail to `references/`), prose economy (Design principle #7), and `skill-evaluator`'s harness lens. Quick test before merge: "would this body still be fine loaded next to the busiest skills?"

This gate stays **manual prose** by design — see "Don't start with meta-skills" below.

### Authority tiers — annotate every skill

Every `SKILL.md` carries `metadata.tier` in frontmatter. This is a **review convention**, not runtime-enforced.

```yaml
metadata:
  tier: draft   # read-only | draft | act
```

- `read-only` — fetches, queries, or describes; never produces a mutable artifact or mutates state.
- `draft` — produces content for human review; cannot send or commit. **Default for this repo** — nearly every skill here is a content-producer.
- `act` — performs irreversible operations.

**Graduation rule:** anything new — *including anything an agent drafts for you* — enters at `draft`. It earns `act` only after it has run clean across several real uses **and** you've eyeballed its tool *trajectory*, not just its final output (the right answer reached via a wrong sequence of tool calls is the failure that bites at `act`-tier). Where the runtime honors it, pair an `act` skill with a tightly scoped `allowed-tools`.

### Supply-chain hygiene

This repo's standing practice is **cross-reference, don't vendor**: we point at external skills and we absorb *ideas with citation* (precedent: `GoogleChrome/modern-web-guidance` and `nidhinjs/prompt-master`, both cited in `skill-evaluator/references/`), but we do not copy external skill *code* into the tree — all skills here are first-party. When you absorb an idea, cite the source and license inline where it lands.

Dormant rule for if we ever *do* vendor an external skill: a skill is code that runs in your context. Trust tier (first-party vendor > your own/org > community; treat community as audit-before-adopt); read its `scripts/` before installing (no unscanned deps, no hardcoded secrets or absolute paths); **pin** the commit you vendored and record where it came from (a `SOURCE` note or a README line).

### Don't start with meta-skills

Keep the library gate manual until it has caught a real regression at least once. A self-improving `library-regression-checker` *meta-skill* built on weak evals quietly degrades the library while reporting that it's improving. The shift-left instinct (`docs/skills-policy.md`) argues for a script — defer it; the gate's job first is to prove it catches a boundary that prose review missed.

> **See also** `docs/skills-policy.md` — the canonical global skills policy (skill vs. always-on context, write-software-not-rules, the mental model). Its skill-vs-passive-context point overlaps this repo's harness vocabulary ("Context engineering" / "Progressive disclosure") — that doc owns the global-settings framing, this file owns the in-repo authoring framing. Point, don't restate.

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

Skills that need any of this reference the relevant section in coordinator. `team-composer` is the existing thin-pointer example (the external `kerby` skill is another).

### Other shared things to be aware of

- The external [`kerby`](https://github.com/sorawit-w/kerby) skill — opinionated agentic-coding rules (`BOOTSTRAP.md`). Opt-in; formerly `coding-rules` in this repo.
- `team-composer` Phase 6 — references `sub-agent-coordinator` for model routing / role-picking / deliverable fan-out.
- `skill-evaluator` — the split-context audit harness for SKILL.md rule-adherence reviews. Run it in the **main loop** (its executor/grader sub-agents — the actual bias removal — only spawn there; nesting collapses them). See "Pre-shipment audit ritual".

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

**Example:** the sub-agent-coordinator coding-work mapping (10 rows) started in `coding-rules` (now the external `kerby` skill) as an "opinionated overlay." On review, 9 of 10 rows were universal defaults, not personal taste — they got promoted to coordinator's `Default Mapping (Coding Work)`. It became a thin pointer.

**Why:** the temptation is to draw the framework/opinion line along skill boundaries (coordinator = framework; coding-rules = opinion). The real line is along *actual taste* — and most calibration matrices have more defensible defaults than they look like at first.

### 6. Observable feedback loops over aspirational prose

Prefer constraints the harness can *check* over rules only a careful human reviewer can verify. Aspirational prose ("be rigorous", "consider edge cases") drifts on contact with real runs; structured reviewers, linters, and audit rituals do not.

**Examples in this repo:**
- `team-composer` Phase 6.6 — a `Plan` subagent reviews the draft Structured Plan and returns ranked findings. The check happens; "be rigorous" is reified.
- `skill-evaluator` — split-context audit that asks "does the text land?" instead of trusting self-review.
- Pre-shipment audit ritual — `skill-evaluator` + description check run before every version bump that touches SKILL.md.
- The five-file version bump in this CLAUDE.md — concrete checklist beats "remember to update the manifest," and `check-skill-compat.py`'s parity assertion turns the checklist into an enforced gate.

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
| General agentic-coding discipline | external `kerby` skill (opt-in) |
| SKILL.md rule-adherence auditing | `skill-evaluator` skill |
| Skill creation walkthrough | Anthropic's `skill-creator` skill |
| Banner pixel-art examples | Existing `assets/<skill>-li.svg` files |
| Cross-skill integration patterns | Each skill's `## Cross-skill integration` section |

When in doubt, **read an existing skill as a template** rather than guessing. The conventions are mostly observable. This file is the shortcut, not the whole map.

---

*Maintenance note:* if you change a convention in the repo (visual style, file structure, release ritual, etc.), update this file as part of the same change. A stale CLAUDE.md is worse than no CLAUDE.md — readers will follow incorrect instructions.

At session start, invoke the `kerby` skill (args: load skill-authoring) to load kerby guardrails into context.
