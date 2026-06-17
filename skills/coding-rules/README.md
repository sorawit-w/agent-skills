<p align="center">
  <img src="https://raw.githubusercontent.com/sorawit-w/agent-skills/main/assets/coding-rules-li.svg" alt="coding-rules — one author's operating system for agentic coding" width="100%"/>
</p>

# coding-rules

A Claude Code skill that loads **one specific person's** operating system for agentic coding into your session — branching discipline, commit cadence, verification gates, sub-agent delegation triggers, ambiguity-before-cost rules, and a small amount of taste about how rules themselves should be written.

> ⚠️ **Read this before installing.** This skill is **deliberately, aggressively opinionated.** It captures *one author's* personal taste, accumulated from years of breaking and fixing things while pairing with agents. It is **not** a "best-practice" guide or a neutral default. The choices are personal, sometimes contrarian, and load on every session that uses them — there is a real input-token cost. **Read `resources/BOOTSTRAP.md` end-to-end before adopting. Fork, edit, or skip rules that don't fit your taste.** The skill provides a frame; your judgment is what makes it useful.

## Why this exists

Most "agent coding" advice is either too vague to land (*"be careful with git"*) or too project-specific to travel (*"run `npm test && npm run lint`"*). What survives across projects, stacks, and teammates is **methodology** — the *shape* of how an agent should approach work.

This skill packages one person's methodology as a loadable session preamble:

- A **Prime Directive** — clarity over cleverness, safety over speed, never leave the repo broken.
- **Hard rules** that apply on every task — branching, commit discipline, verification, resource cleanup, manual-verification instructions, sub-agent delegation, ambiguity-before-cost.
- **Routed workflows** — the agent reads the right workflow file (`new-project`, `feature`, `bugfix`, `quick-task`) instead of guessing from memory.
- **A reference index** for the long tail of decisions — debugging, error handling, vendor adapters, knowledge-base maintenance, design tokens, multi-tool support across Claude Code / Codex / Cursor.
- **A meta-rule** about adding rules — every proposed new rule passes a cost gate (line count, frequency, severity, coverage, testability) before it earns its place.

If your taste matches, the skill will feel like an extension of how you already think. If it doesn't, please **fork and adapt** rather than installing as-is.

## Companion skills

Skills you'll likely want alongside `coding-rules` — all ship in this same marketplace. Brief overview here; deeper integration notes in [Cross-skill integration](#cross-skill-integration) below.

| Skill | Use it for |
|---|---|
| [`team-composer`](https://github.com/sorawit-w/agent-skills/tree/main/skills/team-composer) | Multi-role discussion *before* coding — "monolith vs services?", "which DB?", "is this refactor worth it?" Surfaces trade-offs the rules can't. |
| [`sub-agent-coordinator`](https://github.com/sorawit-w/agent-skills/tree/main/skills/sub-agent-coordinator) | Coordination patterns *during* execution — fan-out, pipeline, specialist routing, briefing templates. The natural sibling to BOOTSTRAP's `sub-agent-delegation` reference. |
| [`wear-the-hat`](https://github.com/sorawit-w/agent-skills/tree/main/skills/wear-the-hat) | When you want one specific lens applied to a task without convening a full panel — `@security_specialist` on auth code, `@dataviz_engineer` on a chart, `@accessibility_specialist` on a UI. Single-role embodiment. |
| [`skill-evaluator`](https://github.com/sorawit-w/agent-skills/tree/main/skills/skill-evaluator) | Auditing rule changes via split-context review — never grade rules in the same agent that wrote them. |
| [`tech-stack-recommendations`](https://github.com/sorawit-w/agent-skills/tree/main/skills/tech-stack-recommendations) | Picking a runtime / framework / database / hosting target on a new project or migration. Pairs with `workflows/new-project.md`. |

None are required — `coding-rules` works on its own. They sharpen the edges where it deliberately stays thin (multi-role planning, sub-agent coordination, rule evaluation, stack selection).

## What it does

- **Loads `resources/BOOTSTRAP.md`** into the current session via the `Read` tool, so the rules enter conversation context as a tool result (not a paraphrase).
- **Seven sub-commands** routed via the `args` parameter: `load` (default), `reload`, `status`, `install`, `uninstall`, `prepare`, `audit`.
- **Per-project install** appends a single instruction line to your `CLAUDE.md` / `AGENTS.md` / `AI-CONTEXT.md` / `.cursorrules` so future sessions auto-invoke `coding-rules` at start. **Per-file confirmation required — never silent.**
- **Compaction-safe.** Long sessions can strip earlier context; `args: status` checks whether BOOTSTRAP markers are still present, `args: reload` re-injects them.

## What it doesn't do

- **Auto-trigger on general coding tasks.** This is opt-in only — the user must explicitly mention `coding-rules`, `/coding-rules`, or ask to load/install/check it. The rules are a meta-system, not a fix for individual bugs.
- **Modify your code.** The rules govern *how* the agent works; they don't ship code edits.
- **Silently change vendor files.** `install` and `uninstall` ask per-file before touching `CLAUDE.md` etc. If you say no, nothing happens.
- **Replace your judgment.** Every rule has a stated reason; if the reason doesn't apply to your project, the rule shouldn't either.
- **Pretend to be evaluated.** Rule changes route to a separate skill ([`skill-evaluator`](https://github.com/sorawit-w/agent-skills/tree/main/skills/skill-evaluator)) for a split-context audit. Inline grading by the same agent that wrote the rule is exactly what the evaluator is designed to avoid.

## When to use it

- You're working with Claude Code, Codex, Cursor, or another agent and you want a **shared frame** the agent will follow without you re-typing it every session.
- You've already fork-and-edited the rules so they reflect *your* taste — and want them to load reliably across sessions in a project.
- You want a **compaction-safe loader**: even if a long session strips earlier context, a one-line reload restores the rules.
- You want per-project install hygiene that touches one line in your vendor agent-instruction file and stops there.

## When not to use it

- **You haven't read `resources/BOOTSTRAP.md`.** Loading rules you haven't read defeats the purpose. The cost is paid in tokens on every session; the value is paid out only when the rules match your judgment.
- **The rules conflict with your team's conventions.** Branching and commit discipline rules are not universal. If your team batches commits or works on `main`, this skill will fight you. Fork and adapt.
- **You want a neutral, "best-practice" preamble.** This isn't that. Try a more general guide instead.
- **You're trying to fix a specific bug.** The skill governs how tasks are done — it doesn't *do* the task. Use a debugging skill (e.g., [`engineering:debug`](https://github.com/anthropics/skills) or [`anthropic-skills:diagnose`](https://github.com/anthropics/skills)) for that.

## Sub-commands

The skill is invoked via `Skill` tool with `args: <sub-command>`. Defaults to `load` if `args` is empty.

| Sub-command | What it does |
|---|---|
| `load` (default) | Locate `resources/BOOTSTRAP.md`, read it via `Read` so it enters context as a tool result, confirm to user. |
| `reload` | Same as `load`, but with a "BOOTSTRAP refreshed" confirmation. Useful after Claude Code compacts the conversation. |
| `status` | Scan recent context for BOOTSTRAP signatures (e.g., `Prime Directive`, `<hard_rules>`, distinctive headers). Report loaded / not loaded. |
| `install` | **Phase 1** — append the session-start instruction to your vendor agent-instruction files (`CLAUDE.md` / `AGENTS.md` / `AI-CONTEXT.md` / `.cursorrules`), per-file confirmation. **Phase 2 (optional)** — register `coding-rules`' Claude Code lifecycle hooks (`PreToolUse` + `SessionStart`) in your chosen settings file. Both phases are independently skippable; both show a diff and require explicit confirmation. |
| `uninstall` | Mirror — Phase 1 removes the install line from vendor files; Phase 2 removes coding-rules-managed hook entries from your chosen settings file. Both phases optional, both confirmed. |
| `prepare` | Onboard an **existing repo**: populate (and refresh) the artifacts BOOTSTRAP reads at session start — `agent-context.yaml`, `CONTEXT.md`, `.ai/knowledge/`, `.ai/STATUS.md`, `.ai/memory.log` — from your real code and git history. Tiered by inferability; **diff-and-confirm on every write**; refresh never clobbers human-curated content. The existing-code counterpart to greenfield `new-project` setup. The `.ai/knowledge/` candidate pass auto-runs on first onboarding (empty knowledge dir) and is opt-in once entries exist — force it with `args: prepare:knowledge` / `prepare --knowledge` (or "force the knowledge pass"). Forcing only controls whether the pass runs; drafts stay `confidence: low` with per-entry diff-and-confirm, and `confidence: high` entries stay frozen. |
| `audit` | **Read-only** static conformance audit of a real-coding project against the *current* rule corpus → self-contained HTML report under `.ai/audits/` (git-excluded). `audit [--full] [<dimension> ...]` — incremental by default, dimensions `security`/`quality`/`data`/`git-hygiene`/`docs`. Derived + classifier-anchored: only checks rules that leave durable artifacts, names what it can't statically see in a coverage banner. Never edits/commits/merges. NOT a bug review (`/code-review`) or a SKILL.md audit (`skill-evaluator`); redirects to the latter on a skill repo. |

`install`, `uninstall`, and `prepare` are idempotent — re-running is safe. (`prepare` re-derives only agent-owned content and is a diffs-only near-no-op on an already-onboarded repo.) `audit` is read-only and re-runnable — it writes a timestamped report and never mutates the repo.

### How to invoke

Slash command (recommended — unambiguous):

```bash
/agent-skills:coding-rules               # default sub-command: load
/agent-skills:coding-rules load          # explicit
/agent-skills:coding-rules reload        # after compaction
/agent-skills:coding-rules status        # check whether rules are still loaded
/agent-skills:coding-rules install       # persistent per-project setup
/agent-skills:coding-rules uninstall     # mirror — both phases
/agent-skills:coding-rules prepare       # onboard an existing repo (populate context)
/agent-skills:coding-rules prepare:knowledge  # prepare + force the .ai/knowledge candidate pass
/agent-skills:coding-rules audit         # conformance audit → HTML report (incremental)
/agent-skills:coding-rules audit --full security  # whole-repo, security dimension only
```

If no other installed plugin defines a `coding-rules` skill, the short form `/coding-rules` also resolves. The namespaced form is always unambiguous and recommended.

Or in natural language — Claude will route correctly:

- "load coding-rules"
- "install coding-rules in this project"
- "are coding-rules still loaded?"
- "reload coding-rules — they seem to have stopped applying"
- "uninstall coding-rules"
- "onboard this repo into coding-rules" / "make this repo coding-rules-ready" / "prepare this repo"
- "prepare this repo and force the knowledge pass" (forces the opt-in `.ai/knowledge/` candidate pass)
- "audit this repo against coding-rules" / "run a coding-rules conformance audit" / "audit the security dimension"

### `load` vs `install` — they're independent

The two most-used sub-commands have different lifetimes. Worth understanding before you reach for either.

- **`load`** reads `BOOTSTRAP.md` into the **current session's** context. The rules are active now and only now — when the session ends or context is compacted, they're gone.
- **`install`** appends one instruction line to your project's vendor agent-instruction files (and, optionally, registers hooks) so **future sessions** auto-invoke `load` at session start. It does NOT touch the current session's BOOTSTRAP state.

Neither command requires the other. Typical patterns:

```bash
# One-off in this session only — no persistence
/agent-skills:coding-rules load

# Persistent setup for future sessions — no immediate effect on this session
/agent-skills:coding-rules install

# First time in a project: persist AND activate now
/agent-skills:coding-rules install
/agent-skills:coding-rules load
```

**Subtle gotcha:** right after running `install` for the first time, BOOTSTRAP is **not** yet active in the current session — `install` only edited a file, it didn't load anything. Either run `load` manually in the same turn, or start a fresh session (where the install line in `CLAUDE.md` etc. will auto-fire `load`).

After `install` is applied to a project, every future session in that project auto-loads via the install line — you shouldn't need to type anything. Exceptions:

- **Mid-session compaction** stripped BOOTSTRAP → `/agent-skills:coding-rules reload` (or run `status` first to confirm).
- **You want to verify** the rules are still active → `/agent-skills:coding-rules status`.

## What `install` actually does — two independent phases

This is the most surface-area part of the skill, so the contract is laid out explicitly:

### Phase 1 — vendor agent-instruction files (one-line append)

For each detected file (`CLAUDE.md`, `AGENTS.md`, `AI-CONTEXT.md`, `.cursorrules`), the skill asks per-file before appending:

```
At session start, invoke the `coding-rules` skill (args: load) to load coding-rules guardrails into context.
```

Skipping a file leaves it untouched. Already-installed files are detected and skipped silently. No other content is modified.

### Phase 2 — Claude Code lifecycle hooks (settings.json registration, optional)

After Phase 1 completes, the skill asks once whether to register hooks. **Not required** — Phase 2 can be skipped entirely, and the skill still works (BOOTSTRAP load + reload + status are independent of hooks).

If accepted, the skill:

1. **Resolves the absolute path** to the bundled hooks directory at `<install-root>/resources/hooks/`. Discovery order: BOOTSTRAP-relative path (from `load`) → Glob match → `${CODING_RULES_DIR}` env var → ask the user.
2. **Asks where to register**:
   - `~/.claude/settings.json` (global — applies to every project)
   - `<project>/.claude/settings.local.json` (project, gitignored — your machine only) — **default**
   - `<project>/.claude/settings.json` (project, committed — teammates also inherit)
3. **Builds six hook entries** with absolute paths to the resolved scripts:

   | Event | Matcher | Script | What it does |
   |---|---|---|---|
   | `PreToolUse` | `"Edit\|Write"` | `protect-env.sh` | Hard-block edits to `.env` files (security — not env-var disablable) |
   | `PreToolUse` | `"Bash"` | `protect-git.sh` | Hard-block destructive git (`reset --hard`, `push --force` to protected branches, `clean -f`, etc.) — security, not env-var disablable |
   | `PreToolUse` | `"Bash"` | `pre-commit-check.sh` | Soft-warn on missing quality gates before `git commit`; hard-block on detected secrets in staged files |
   | `SessionStart` | `""` | `session-start-context.sh` | Inject `.ai/STATUS.md` head + recent `.ai/memory.log` so the agent resumes with state |
   | `SessionStart` | `""` | `knowledge-bootstrap.sh` | Scaffold `.ai/knowledge/KNOWLEDGE.md` if missing; reindex AUTO-INDEX block; flag entries older than 180 days |
   | `SessionStart` | `""` | `context-bootstrap.sh` | Scaffold `CONTEXT.md` (project domain glossary) if missing; never overwrites |

4. **Shows the full diff** of the merged settings.json. Single y/n confirmation. On `n`, nothing is written.
5. **Idempotent** — re-running detects already-managed entries by their absolute path signature (`/skills/coding-rules/resources/hooks/<script>.sh`) and skips them.

`uninstall` mirrors symmetrically, removing only entries that match the path signature. Hand-written hook entries with the same script names but different paths are left alone.

### Disabling individual hooks at runtime

Once hooks are registered, three soft hooks (non-security) can be temporarily disabled via the `CODING_RULES_HOOK_DISABLED` env var (comma-separated, no spaces):

```bash
# Disable one hook for the current shell
export CODING_RULES_HOOK_DISABLED=session-start-context

# Disable several
export CODING_RULES_HOOK_DISABLED=session-start-context,pre-commit-check,knowledge-bootstrap
```

Disablable: `session-start-context`, `knowledge-bootstrap`, `context-bootstrap`, `pre-commit-check` (soft reminder only — secret scan still runs).
**Not disablable** (security / data-loss critical): `protect-env`, `protect-git`. To bypass these, edit your settings file and remove the entry — a deliberate config edit, not an ambient variable.

### Plugin-level activation is intentionally NOT supported

Hooks are never auto-registered at plugin install time. Specifically: the parent plugin's `plugin.json` carries no `hooks` field, and there is no `hooks/hooks.json` at the plugin root. This is by design — users who installed the parent plugin for a different skill (`team-composer`, `pitch-deck`, etc.) must not silently inherit guardrails they didn't ask for. Activation stays skill-scoped, opt-in via Phase 2 of `install`.

## What's inside `resources/`

The rules themselves live under `resources/`, bundled with the skill:

- **`BOOTSTRAP.md`** — the loader entry point. Prime Directive, project-state detection, workflow routing, hard rules, when-stuck, context-save, reference index. ~230 lines.
- **`workflows/`** — task-shape playbooks: `new-project.md`, `feature.md`, `bugfix.md`, `quick-task.md`. Each wires the relevant references in the right order.
- **`references/`** — long-tail topic guides (~25 files): working patterns, quality gates, error handling, debugging, communication, git worktrees, guardrails, validation, context management, sub-agent delegation, vendor adapters, knowledge management, roadmap, hooks, multi-tool support, safety mindset, design-token authority, domain glossary.
- **`templates/`** — starter files: `agent-context.yaml`, `STATUS.md`, `KNOWLEDGE.md`, `CONTEXT.md`.
- **`hooks/`** — optional shell hooks for projects that want enforcement at git/session boundaries: `pre-commit-check.sh`, `protect-env.sh`, `protect-git.sh`, `session-start-context.sh`, `knowledge-bootstrap.sh`, `knowledge-reindex.sh`, `knowledge-lint.sh` (advisory `.ai/knowledge/` integrity check — manual or git post-commit, not SessionStart; `--strict` to fail on findings), `context-bootstrap.sh`. Not installed automatically — copy what you want into your project's `.git/hooks/` or session-start config.
- **`scripts/validate-agent-context.ts`** — Bun/Node script to validate `agent-context.yaml` against the bundled JSON Schema. Optional.
- **`agent-context.schema.yaml`** — JSON Schema for the per-project `agent-context.yaml` contract.

## A note on opinionation

The rules in `BOOTSTRAP.md` reflect specific choices that may not match your judgment:

- **Worktree-default for feature work** (with a 3-question gate to skip when overhead isn't justified). If your repo is npm-heavy or tiny, you may want `git checkout -b` everywhere.
- **Commit after every completed piece of work**, not at the end of the session. Some teams prefer squashed commits and a clean history; this rule fights that.
- **No completion claims without fresh evidence.** Some workflows are exploratory and "should work" is fine. Not here.
- **Manual verification instructions in every completion report.** Reasonable for shipped features; overkill for one-line typo fixes.
- **`DESIGN.md` as design-token authority** when present. Opinionated wiring into the [Google Labs spec](https://github.com/google-labs-code/design.md), alpha.
- **Methodology over scripts.** Hardcoded commands (`npm test`) lose to project-detected commands (`{test_command}`).

These choices have stated reasons in the rule files. Read the reasons; keep the ones that match your work; **delete or rewrite the ones that don't.** The skill loads whatever is in `resources/BOOTSTRAP.md` — the easiest way to make it yours is to fork the repo and edit BOOTSTRAP directly.

## Editing the rules

`CLAUDE.md` at the skill root (not the project's `CLAUDE.md`) governs **rule edits** — change-class table, rule-cost gate, authoring style notes. If you fork to adapt the rules, read it before adding rules; many proposed rules don't pay back their token cost.

For rule **evaluation** (does this rule actually change agent behavior?), use the [`skill-evaluator`](https://github.com/sorawit-w/agent-skills/tree/main/skills/skill-evaluator) skill — split-context audit removes author bias.

## Install

This skill is distributed as part of the [`sorawit-w/agent-skills`](https://github.com/sorawit-w/agent-skills) plugin marketplace. From Claude Code or Cowork:

```
/plugin marketplace add sorawit-w/agent-skills
/plugin install agent-skills@sorawit-w
```

Once the plugin is installed, the skill is available system-wide. Then, in any project where you want the rules to auto-load on session start:

```
> Use the coding-rules skill with args: install
```

The skill will detect your vendor agent-instruction files and ask per-file before adding the one-line invocation.

## Cross-skill integration

| Skill | Relationship |
|---|---|
| [`skill-evaluator`](https://github.com/sorawit-w/agent-skills/tree/main/skills/skill-evaluator) | Use for evaluating rule changes — never inline-grade in the same agent that wrote the rule. The skill's own `CLAUDE.md` enforces this. |
| `superpowers:*` *(if installed)* | Some superpowers skills overlap with the BOOTSTRAP rules (TDD, brainstorming, verification-before-completion). User instructions and explicit invocations win — see Phase 0.5 in `team-composer`'s docs for a pattern. |
| Project-local `CLAUDE.md` / `AGENTS.md` | Per the BOOTSTRAP priority order (User > Project config > Agent context > Playbook), the project's own instructions always win over rules in this skill. |

## Status

`v0.1` — ported from a separate working repo. The rules have been used and refined over time but the skill packaging in this marketplace is new. **Treat as alpha** — feedback on the loader behavior welcome via [issues](https://github.com/sorawit-w/agent-skills/issues). Rule-content feedback should generally take the shape of *fork-and-edit*, not feature-request.

## Contributions

Not accepting external contributions to the rule content — these are personal taste, and "everyone's opinion in one BOOTSTRAP.md" is not the goal. Bug reports on the loader (path resolution, install/uninstall edge cases) are welcome.

Feel free to fork.

## License

MIT — see the [LICENSE](https://github.com/sorawit-w/agent-skills/blob/main/LICENSE) file at the repo root.
