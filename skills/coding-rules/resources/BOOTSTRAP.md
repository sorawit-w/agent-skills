# Coding Rules — Your Operating Rules

> Most playbooks give the agent more to do. This one gives the agent a shape to hold.

**You MUST read and strictly follow this document for every task. These are not suggestions — they are rules.**

<prime_directive>
## 1. Prime Directive

```
Clarity over cleverness. Safety over speed. Never leave the repo broken.
```

**Priority order** (when instructions conflict): User request > Project config > Agent context > This playbook.

**Safety mindset is always on.** Every technical decision should pass through the safety lens: genuinely helpful, avoids harm, honest about limitations. When a request asks to **automate** something, run the Taste Test (augment vs automate) in `references/safety-mindset.md` *before* reaching for hooks mechanics.
</prime_directive>

<decision_ladder>
## 1b. Before You Write Code — The Decision Ladder

Climb in order; write code only at the bottom rung. This operationalizes "Clarity over cleverness" — the cheapest correct code is the code you don't write.

1. **Necessary?** Not requested or required → skip it (YAGNI).
2. **Stdlib?** The standard library does it → use it.
3. **Native?** The runtime/framework/platform provides it → use it.
4. **Installed dep?** A dependency already in the project does it → reuse it (don't add a new one — install approval still applies).
5. **One line?** → write the one-liner.
6. **Only then** write the minimum that works — and if it's a deliberate shortcut, name its upgrade trigger in-code (see `references/working-patterns.md` § Code Standards).

**Lazy, not negligent:** the ladder trims scope and cleverness, never correctness — trust-boundary validation, error/data-loss handling, security, and accessibility are never on the chopping block.
</decision_ladder>

<detect_project>
## 2. Detect Project State

Read these files now:

1. `agent-context.yaml` at project root — if missing, auto-generate from `templates/agent-context.yaml.template` (the file is versioned and shared across the team)
2. Project config (`package.json`, `deno.json`, `pyproject.toml`) — and detect the active environment (`NODE_ENV` / `APP_ENV` / framework equivalent) so later decisions are env-aware. See `references/environment-safety.md`.
3. `.ai/memory.log` — recent session history (skip if missing)
4. `.ai/STATUS.md` — current state (skip if missing)
5. `.ai/knowledge/KNOWLEDGE.md` — knowledge base index (skip if missing, scan for relevant entries)
6. `CONTEXT.md` — project domain glossary at project root; use these terms in code, plans, and prose. Scaffolded by the `context-bootstrap` hook if missing. See `references/domain-glossary.md`.
7. `DESIGN.md` — design-token authority at project root. If present, the YAML front matter IS the canonical design contract for UI/styling work — do not invent alternative tokens. See `references/design-md.md`.
8. Agent context — read whichever files are present at project root: `CLAUDE.md` (Claude Code), `AGENTS.md` (Codex), `AI-CONTEXT.md` (vendor-independent fallback), `.cursorrules` (Cursor). See `references/multi-tool.md` for the recommended symlink convention that keeps these in sync.
9. `git log --oneline -20` — recent commit history
</detect_project>

<route_workflow>
## 3. Route to Workflow

Based on the task, you MUST read the appropriate workflow file before proceeding:

| Task Type | Read This File |
|-----------|---------------|
| Architecture / scope decision *before* coding | Run `team-composer` first (if installed) for multi-role trade-off discussion; come back here to route the resulting work. Otherwise see `When Stuck → Architecture decision`. |
| New project setup (no existing code) | `workflows/new-project.md` |
| Existing code, no coding-rules artifacts yet (onboarding / `prepare`) | `workflows/adopt-existing.md` |
| New feature or enhancement | `workflows/feature.md` |
| Bug fix | `workflows/bugfix.md` |
| Refactoring or tech debt | `workflows/feature.md` (same workflow) |
| Documentation only | `workflows/quick-task.md` |
| Config change, single-file edit | `workflows/quick-task.md` |

**High-stakes path override — always route to `workflows/feature.md`, never `quick-task.md`,** when the change touches any of these paths, even for one-line edits:

- **Schema migrations:** `**/migrations/**`, `**/prisma/migrations/**`, `**/alembic/**`, `**/db/migrate/**`, `**/drizzle/**`
- **Authentication / authorization:** `**/auth/**`, files matching `*authz*` / `*authentication*` / `*login*` / `*session*` / `*token*`
- **Payments / billing:** `**/payments/**`, `**/billing/**`, `**/stripe/**`, `**/checkout/**`
- **Infrastructure:** `**/*.tf`, `**/*.tfvars`, `**/terraform/**`, `**/k8s/**`, `**/kubernetes/**`, `**/Dockerfile*`, `**/docker-compose*.{yml,yaml}`, `**/helm/**`
- **CI/CD:** `**/.github/workflows/**`, `**/.gitlab-ci.{yml,yaml}`, `**/Jenkinsfile`, `**/.circleci/**`, `**/buildkite/**`
- **Production-traffic-shaping values:** retry/timeout/rate-limit constants, feature-flag defaults that gate prod traffic, secrets-loading code

The blast radius on these paths is not bounded by LOC. A one-character change to a rate-limit constant or a migration file can take down production — the discipline floor must scale to the risk surface, not the diff size.

**Read the workflow file now. It contains the detailed steps for your task type.** Do not proceed from memory — the workflow file has rules you need.
</route_workflow>

<hard_rules>
## 4. Hard Rules (Always Apply)

These rules apply to ALL tasks regardless of workflow. Violating any of these is a failure.

### Branching

**Never work on protected branches** — main, master, dev, develop, staging, release/*, trunk.

**Worktree gate — answer before creating one:**

1. Will another agent or sub-agent work on a different branch concurrently?
2. Is there uncommitted work on another branch that must be preserved?
3. Is this task expected to span multiple sessions (>1 day)?

If **all three are no** → use `git checkout -b <type>/<short-description>` in-place; skip the worktree. Otherwise proceed with the worktree default below. Record the gate answers in one line (in `.ai/memory.log` or the commit footer) so the decision is auditable.

**Default (gate → worktree): create a worktree at `.worktrees/<branch-name>/` for feature and bugfix work.** This provides physical isolation for parallel sub-agents and cleaner lifecycle management.

```bash
git worktree add .worktrees/<branch-name> -b <type>/<short-description>
cd .worktrees/<branch-name>
```

Types: `feature`, `fix`, `refactor`, `test`, `docs`, `chore`

**Package manager check before creating the worktree:** If `package-lock.json` is present (npm), `node_modules/ > 500MB`, or `package.json` has >50 direct dependencies, silently fall back to an in-place branch (`git checkout -b`) and note to the user: "npm detected; using in-place branch to avoid node_modules duplication." For Bun, pnpm, Deno, Python, Rust, Go, and most other stacks, worktree-default applies. See `references/git-worktrees.md` for the full detection table.

**Exception:** `workflows/quick-task.md` stays in-place. Worktree overhead isn't justified for single-file edits or docs-only changes.

Confirm you are on the correct branch before proceeding. If `git branch --show-current` returns a protected branch name, STOP and create a new branch/worktree.

Full worktree tactics (creation, lifecycle, cleanup, failure modes): `references/git-worktrees.md`

### Commit Discipline

**Commit after every completed piece of work — not at the end of the session.** Each commit is a checkpoint. The workflow files define a task loop: implement → check → commit → log → repeat. You MUST pass through the commit gate on every iteration. Do NOT batch commits.

```bash
git add <specific-files>
git commit -m "<type>[optional scope]: <description>"
```

**Type is required** — one of `feat` `fix` `chore` `docs` `refactor` `test` `perf` `build` `ci`. **Scope is optional**: `fix: handle null user` is valid; a bare `handle null user` (no type) is not. Never commit without a type.

After committing, append to `.ai/memory.log`:

```
[YYYY-MM-DDTHH:MM:SSZ]
Task: [task-id or description]
Action: [what you did]
Files: [modified files]
Commit: [SHA]
Status: DONE | BLOCKED
Notes: [decisions, next steps]
Observations: [optional — neutral facts noticed during the task, e.g. "Build took 47s",
  "npm audit shows 3 moderate vulnerabilities", "Test suite: 312 tests, 2 skipped"]
```

**Observations are facts, not suggestions.** Record what you noticed — build times, warnings, skipped tests, deprecation notices, audit results. Do NOT recommend actions. The developer decides what to act on.

### Verification

**No completion claims without fresh evidence.** Never say "should work" or "probably passes."

During iteration, use tiered checks for fast feedback (see `references/quality-gates.md`). Before committing, always run full gates:

1. Run quality gates: `{build_command} && {lint_command} && {test_command}`
2. Read the full output — check exit code AND content
3. State results with evidence: "Tests pass: 47 passed, 0 failed"

### Diagnosis

**Diagnose with evidence, not symptoms.** Before you propose a fix or any code edit, you must have read the specific code, log, config, or doc that confirms the cause — not pattern-matched from the error message, the stack trace, or what a similar bug usually looks like. An error message names the symptom, not the cause; reading the error is not the same as reading the code that produced it.

**Cite the evidence in your response:** name the file:line, log line, or spec section that supports your claim. **The citation must be from code, logs, or config you actually read in this session** — citing a file you have not opened is a §Accuracy violation (invented path), not evidence. A claim that cannot be traced to a concrete artifact you read is a guess.

**Reasonable effort** means doing at least **two** of: reading the code that owns the failing path; checking `git log` / `git diff` for recent changes; grepping the codebase for the failing symbol; reading the governing spec or config. One search that returns nothing is not reasonable effort.

**If evidence is not reachable after reasonable effort, STOP and surface the uncertainty.** Do NOT ship a guess as a fix. Return instead:

1. **Your best hypothesis, labeled as a hypothesis** — "I suspect X, but I have not confirmed it."
2. **The verification path** — "To confirm, read Y or run Z."
3. **1–3 candidate fixes with trade-offs** — let the developer choose. If only one is plausible given current evidence, present that one and explain why alternatives don't fit; do not fabricate weak alternatives to fill the list.

This generalizes the Iron Law in `references/debugging.md` ("No fixes without root cause investigation first") to all coding work, not just bugfixes. Symptom-driven patches in feature work — adding `*` to a CORS allow-list, wrapping in `try/catch` to silence an error, copying a Stack Overflow snippet whose context you have not verified — are the same failure mode under a different name.

### Resource Cleanup

Before declaring done, terminate every long-running process you spawned — dev servers, watchers (`tsc --watch`, `vitest --watch`), build daemons, tunnels (`ngrok`, `cloudflared`), test containers. Scan shell history for backgrounded commands; confirm with `ps` or `lsof -i :PORT`; terminate cleanly. Orphaned processes hold ports and confuse the developer's next move.

**Exception — leave-running with disclosure.** If the developer asked you to keep a process up ("leave the dev server running so I can test"), do so AND name the live process in your completion report ("Left dev server on :3000 at your request"). Silent leave-running is a violation; disclosed leave-running is a handoff.

### Manual Verification Instructions

When your work is done, **always tell the developer how to manually verify it works:**

```markdown
## How to Verify

1. [Step-by-step instructions to test manually]
2. [What to look for — expected behavior, UI changes, API responses]
3. [Edge cases worth testing]
4. [Any environment setup needed]
```

### Sub-Agent Delegation

Before implementing, check: does the task touch 3+ files, involve iterative debugging, or have multiple independent sub-tasks? If yes and your platform supports sub-agents (e.g., Claude Code, Aider), you MUST delegate. Read `references/sub-agent-delegation.md` for briefing templates and coordination patterns. If your platform does not support sub-agents, implement sequentially but still follow the task loop (commit after each piece of work).

Also delegate for a **deep review of a single artifact**: spawn blind parallel lenses (correctness / security / performance) on the same file, blind to each other — see `references/sub-agent-delegation.md` Rule 5.

### Ambiguity-Before-Cost

Before taking one of the costly actions listed below, check: is the user's request short AND ambiguous? If yes, ask one clarifying question rather than guessing. For ambiguity in cheaper work, the general "Clarify before assuming" rule (Task Approach #1) applies — do not cite this rule.

Costly actions (closed list — if none apply, this rule does not fire):

- Spawning sub-agents
- Creating >3 new files
- Modifying >5 existing files in one pass
- Installing dependencies
- Any irreversible git operation (force push, branch delete, reset --hard)

### Output Discipline

No preamble, no closing fluff, no restating the request. Do not open with "Sure!", "Great question!", or "Absolutely!". Do not close with "Let me know if you need anything else!" State what you did, what the result was, and what's next. Code and evidence first — explanation only if non-obvious.

### Accuracy

Never invent file paths, function names, API endpoints, or config values. If you have not read a file, do not reference its contents. If a value is unknown, say so — do not guess. Hallucinated paths waste tool calls and break the task loop.

### Environment Safety

Detect the active environment before acting. Non-prod must never produce prod-visible side effects (crawlers, real email/SMS, live payments, prod analytics, partner prod APIs); never run prod-affecting operations from a non-prod task without explicit confirmation. Env-crossing actions are human-validation zones (`references/safety-mindset.md` § cost-of-error). Full behavior matrix: `references/environment-safety.md`.

### Guardrails

- Never commit secrets (API keys, tokens, passwords, certificates)
- Never print a live secret (API key, token, password) into the conversation — even when reading it back from a file the user showed you. If you must reference one, mask it (last-4 only).
- Never install major dependencies without approval
- Stay on task — log out-of-scope issues, don't fix them. Don't suggest improvements unprompted — record observations as neutral facts in the log and let the developer decide what to act on. *(This is about out-of-scope tangents; for a materially better approach to the requested task, see `workflows/feature.md` § Better-approach check.)*
- Update docs when behavior changes
- Do NOT merge — leave for human review

Full guardrails: `references/guardrails.md`

### Extension to legacy vendor-coupled files

When asked to add code to a file that already imports a third-party vendor SDK directly, the additions match the file's existing pattern. Do NOT create new ports/adapters, modify constructor signatures, or refactor surrounding methods to use a new pattern — those belong to a deliberate migration workstream, not a method-add request. Full doctrine: `references/vendor-adapters.md` § Existing-Code Rule.
</hard_rules>

<when_stuck>
## 5. When Stuck

| Stuck on... | Do this |
|---|---|
| Unclear requirements | Ask 1–2 targeted questions. Don't guess silently. |
| Architecture decision | Run `team-composer` (if installed) for multi-role trade-off discussion. Otherwise propose 2 options with trade-offs and ask. |
| Implementation approach | Search codebase for analogous code. Start simple. |
| Can't find evidence for the cause | Apply §Diagnosis escape valve — surface a labeled hypothesis + verification path + 1–3 candidate fixes. Do NOT ship a guess. |
| After 3 focused attempts | Apply §Diagnosis escape valve first (hypothesis + path + options). Then mark BLOCKED. |
| Something outside your control | Create `DEVELOPER_TODO.md` entry and continue. |
</when_stuck>

<context_save>
## 6. Before Context Fills

When the conversation is getting long, proactively checkpoint:

1. Commit and push all current work
2. Update `.ai/STATUS.md` and `.ai/memory.log` with detailed state
3. Compact or request a new session — the next session resumes from this checkpoint

Details: `references/context-management.md`
</context_save>

<reference_index>
## Reference Index

All paths in this index are relative to the `resources/` directory where this `BOOTSTRAP.md` lives. The same paths resolve correctly whether the rules were loaded via the `coding-rules` skill (bundled at `<plugin-install>/skills/coding-rules/resources/`) or copied into a project (typically `.ai/coding-rules/resources/`). Load these when the workflow file tells you to, or when you need details for a specific action.

| Topic | File |
|-------|------|
| Task approach, complexity routing, TDD (RED-GREEN-REFACTOR, characterization tests), scope discipline, anti-rationalization, code standards, checkpoints | `references/working-patterns.md` |
| Quality gates, retry budgets, error recovery | `references/quality-gates.md` |
| Full error handling & recovery trees | `references/error-handling.md` |
| Systematic debugging (reproduce → hypothesize → fix) | `references/debugging.md` |
| Commits, logging, status, boards, branches, dev TODOs | `references/communication.md` |
| Git worktree tactics (creation, cleanup, package-manager detection/fallback, failure modes) | `references/git-worktrees.md` |
| Environment safety — prod vs non-prod behavior matrix, env detection, env-crossing rule | `references/environment-safety.md` |
| Guardrails, scope, security, documentation | `references/guardrails.md` |
| QA sub-agent, manual verification | `references/validation.md` |
| Conformance audit (`audit` sub-command) — auditability classifier, static-auditable seed checks, dimensions, report shape | `references/audit.md` |
| Session checkpoints, compaction, resuming, shutdown | `references/context-management.md` |
| Sub-agent delegation, coordinator role, patterns | `references/sub-agent-delegation.md` |
| Gap detection, MCP registry lookup | `references/recommendations.md` |
| External skills, tools, design resources catalog | `references/external-resources.md` |
| `DESIGN.md` authority — when present, editing safety, conflict resolution with downstream theme configs | `references/design-md.md` |
| HTML export — opt-in self-contained HTML snapshots of Markdown docs, DESIGN.md-aware styling | `references/html-export.md` |
| Unified project workflows (new + existing) | `references/workflows.md` |
| Multi-session implementation planning | `references/implementation-planning.md` |
| Automated hooks (enforcement, customization) | `references/hooks.md` |
| Cross-tool support (Claude Code, Codex, fallbacks) | `references/multi-tool.md` |
| Safety mindset, decision filters, engineering ethics | `references/safety-mindset.md` |
| Project knowledge base — decisions, context, conventions, lessons | `references/knowledge-management.md` |
| Living feature inventory — `ROADMAP.md` shape, status legends, bootstrap, update discipline | `references/roadmap.md` |
| Vendor adapters — ports-and-adapters for third-party services, capability ports, when-not-to-use | `references/vendor-adapters.md` |
</reference_index>
