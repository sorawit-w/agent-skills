# Working Patterns

Detailed guidance on task approach, complexity routing, code standards, and commit discipline.

---

## Task Approach

For every task:

1. **Clarify before assuming** — If the request is ambiguous, ask 1–2 targeted questions before starting. You may state a tentative assumption alongside the question (*"Assuming X — confirm or correct?"*); do not proceed on the assumption until acknowledged. Don't silently guess — wrong assumptions waste more time than a quick question.
2. **Restate the problem** — Confirm you understand what's being asked
3. **Identify affected files** — Scope the change before editing
4. **Check dependencies** — Will this change break anything downstream?
5. **Search before creating** — Before writing a new utility, helper, or module-level function, grep for the responsibility. If similar code exists, propose a refactor or note in the commit body why divergence is intentional. If code only *looks* similar, verify it's the same responsibility before consolidating — duplication beats premature abstraction.
6. **Implement incrementally** — Small, reviewable changes over large rewrites
7. **Verify after each change** — use tiered gates: lint-only for config/docs, full build+lint+test for logic changes (see `quality-gates.md`)
8. **Commit with intent** — One logical change per commit

---

## IDE-Aware Tools (when available)

When the agent's environment exposes IDE-native tools via MCP — most commonly **JetBrains MCP** (IntelliJ IDEA, PyCharm, WebStorm, GoLand, Rider, PhpStorm, Android Studio; bundled in 2025.2+) — **prefer them over generic file/grep tools** for the actions below. The IDE understands type hierarchies, language semantics, and project structure; grep doesn't. The gap matters most for typed languages (Java, Kotlin, Scala, Swift, C#, TypeScript).

You don't need to "check" availability. If the JetBrains MCP tools are connected, they appear in your tool list. If they're not, fall back to the generic tools silently — no commentary needed.

| Action | Preferred (JetBrains MCP) | Fallback (generic) |
|---|---|---|
| Find a file by name | `find_files_by_name_substring` | `Glob` |
| Search code content | `search_in_files_content` (uses the IDE index — much faster on large repos) | `Grep` |
| Find usages of a symbol | `find_usages` (semantic — knows type hierarchy, polymorphism) | `Grep` (textual; expect false positives in typed code) |
| Go to definition / declaration | `go_to_declaration` (semantic) | `Grep` for the symbol name |
| Rename a symbol across the project | `rename_refactoring` (atomic, handles imports + cross-file references) | `Edit` per file (error-prone for symbols with many references) |
| Get the currently open file (mid-session context) | `get_open_in_editor_file_text` | Ask the developer |
| Run project tests / a specific config | `execute_run_configuration` (uses the IDE's defined run config) | Infer command from `package.json` / build file |
| List available run configurations | `get_run_configurations` | Read project files |
| Get inspections, errors, or warnings on a file | `get_project_problems` (uses IntelliJ inspections) | Run lint + parse output |
| Replace text in a file | `replace_text_in_file` | `Edit` |
| List project dependencies | `get_project_dependencies` | Read manifest files |

**When NOT to prefer the IDE tool:**

- **Project not indexed.** If an IDE tool returns "no project loaded" or similar, the IDE doesn't have the project open. Fall back to generic tools and continue.
- **Dynamic-heavy code where the indexer can't help.** For heavily-dynamic Python, JS with runtime introspection, or codegen-driven symbols, the IDE's `find_usages` / `go_to_declaration` may miss callers grep would catch. If results look incomplete, follow up with `Grep`.
- **Sanity check disagreements.** If the MCP tool's output is ambiguous, run grep too and reconcile — but don't *default* to grep just because it's familiar.

**Setup and the authoritative tool list:** see the JetBrains MCP entry in `references/external-resources.md`. Tool names above are accurate as of JetBrains 2025.2; the [JetBrains YouTrack MCP-Available-Tools article](https://youtrack.jetbrains.com/articles/SUPPORT-A-2156/MCP-Available-Tools) keeps the authoritative list.

---

## Think in Code, Not Data Processing

When you need to extract a value from many files, **write a script that prints only the value** rather than reading all the files into your context. Tool calls that dump raw content into context burn through the model's window for data the model doesn't need to see.

**Failure mode this prevents:** reading N files to count occurrences, find a maximum, list distinct values, or compute any aggregate — when a 5-line script could print the answer.

**Heuristic:** if your next move is to read >3 files just to extract or compute something, stop and write a script instead. Use `bash` for filesystem queries, the project's runtime (`node`, `python`, `bun`) for parsing or aggregation, or IDE tools (`search_in_files_content`) when the question is "find references."

**Exception:** when the model genuinely needs file content for *reasoning* (reviewing logic, refactoring, summarizing prose, learning a new codebase), reading is correct — scripting can't substitute for understanding. The rule fires when the goal is *extraction or computation*, not comprehension.

**Source:** absorbed from `mksglu/context-mode` (2026-05-09); their "stop treating the LLM as a data processor, treat it as a code generator" framing is the load-bearing insight. The full context-mode runtime (MCP server + hooks + FTS5) is intentionally NOT adopted — see `external-resources.md` for the why.

---

## Complexity Routing

| Complexity   | Indicators                                 | Approach                          | Model Routing |
|--------------|-----------------------------------------------|-----------------------------------|---------------|
| Low (1–3)    | Single file, config change, typo fix        | Handle directly                   | Fastest available model |
| Med (4–6)    | Multiple related files, moderate logic      | Plan first, then implement. Self-check when done. | General-purpose model |
| High (7–8)   | Multi-file, design decisions, new patterns  | Write plan, get approval. QA sub-agent when done. | Best reasoning model |
| Critical (9–10) | Cross-cutting, architectural, breaking    | Plan + approval + staged rollout. QA sub-agent when done. | Best reasoning or specialized model |

**Model routing:** If the agent has access to multiple models, route sub-agent tasks to a model that matches the complexity. Don't waste a top-tier reasoning model on a config change; don't trust a fast model with an architectural decision.

---

## Test-Driven Development

**Prefer TDD when a test framework is already configured in the project.** Writing the test first forces you to understand the requirement before writing the implementation — and gives you an immediate verification signal when you're done.

### The RED-GREEN-REFACTOR Cycle

1. **RED** — Write a minimal failing test that describes the expected behavior
2. **GREEN** — Write the simplest code that makes the test pass
3. **REFACTOR** — Clean up the code while keeping the test green

### When to Use TDD

- **Always use** when: fixing a bug (write a test that reproduces it first), adding a pure function or utility, implementing a well-defined API endpoint, the project already has a test suite
- **Prefer but don't force** when: prototyping or exploratory work, UI components where visual testing is more appropriate, the codebase has no test infrastructure at all
- **Skip TDD** when: the task is configuration only, you're writing documentation, the project explicitly doesn't use tests

### Characterization Tests for Untested Code

When changing code that has no existing test, **write a characterization test that captures current behavior before modifying.** Run it once against the current code (it should pass), then make your change — a now-failing test means your change altered behavior, intended or not. Skip only if the area is genuinely untestable (config files, vendor dirs, build scripts, generated code) and note why in the commit body.

This is especially common when adopting `coding-rules` into a project that predates the test-first discipline — characterization tests are the bridge into the change-comfort regime the rest of these rules assume.

### Relationship to Quality Gates

TDD is *in addition to* quality gates, not a replacement. After your test passes, still run the full gate: `{build_command} && {lint_command} && {test_command}`. A passing unit test doesn't guarantee the build works or lint passes.

---

## Autonomous Iteration

When working on multi-step tasks — especially unattended or long-running ones — use a structured iteration loop instead of a single-pass attempt.

### Define "Done" Before Starting

Before implementing anything, write explicit completion criteria:

```
Done when:
  ✅ All tests pass (0 failures)
  ✅ Build succeeds with no warnings
  ✅ Lint passes with no errors
  ✅ [Feature-specific criterion 1]
  ✅ [Feature-specific criterion 2]
```

These criteria are the loop's exit condition. If you can't define "done" clearly, clarify with the developer first.

### The Iteration Cycle

```
┌→ Pick next incomplete task (one at a time)
│    ↓
│  Implement it
│    ↓
│  Run quality gates
│    ↓
│  Pass? → Commit + mark task done → loop back ┐
│  Fail? → Debug systematically → loop back     │
│                                                │
│  All tasks done + all criteria met? → Exit ────┘
```

**One task at a time.** Don't batch multiple tasks into one iteration — it creates large diffs, makes failures harder to attribute, and complicates rollback. Each iteration should produce one commit.

### Circuit Breaker

Don't loop forever. Stop and escalate when:

| Condition | Action |
|---|---|
| **3 consecutive iterations with no progress** | Stop. You're stuck in a loop. Document what you tried and escalate. |
| **Same error appears 3+ times** | Stop. The fix isn't working. Step back and re-hypothesize (see `debugging.md`). |
| **Retry budget exhausted** | Stop. Follow the escalation path in `quality-gates.md`. |

"No progress" means: no new tests passing, no new tasks completed, no meaningful code changes committed. If you're changing code but nothing improves, that's not progress — that's churn.

### Progress Tracking

Use `.ai/STATUS.md` as your iteration state file. After each successful iteration:

1. Mark the completed task
2. Note what's next
3. Commit the status update alongside the code change

This lets the next iteration (or the next session) pick up exactly where you left off.

### When to Use Autonomous Iteration

- **Multi-task implementation** — working through a plan with 5+ discrete tasks
- **Bug-fixing sweeps** — fixing multiple test failures or lint errors
- **Refactoring campaigns** — systematic changes across many files
- **Unattended work** — overnight builds, batch processing

### When NOT to Use It

- **Subjective decisions** — design choices, UX direction, architecture trade-offs need human judgment
- **Single-task work** — one bug fix, one feature addition — just do it directly
- **Exploratory work** — prototyping, research, investigation — the loop assumes you know what "done" looks like

---

## Code Standards

- **Prefer boring, readable solutions** over clever abstractions
- **Match existing patterns** in the codebase (naming, structure, style)
- **Treat the next reader and downstream caller as your primary user** — code is consumed before it's run; naming, line-of-sight, and consistency are DX, not aesthetics
- **Make trade-offs explicit** — comment *why*, not *what*
- **Handle edge cases** — null checks, empty arrays, network failures
- **Log on error paths and key state transitions** — for application code, include enough context (correlation ID, request shape, decision branch) to diagnose without reproducing. Lighter-weight cousin of the platform-code logging discipline in Scope Discipline below.
- **No dead code in your touched scope** — Remove unused imports, commented blocks, and orphaned files *that your changes made dead*. Don't sweep pre-existing dead code unless explicitly asked — janitorial sweeps inflate the diff and add unrelated risk.
  - **Platform-code caveat:** in libraries, SDKs, and published packages, exported symbols that look unused may have external callers you can't see. Treat unused *exports* as live unless you've verified no downstream consumer depends on them — removing them is a semver-breaking change, not dead-code cleanup.

Dead-code-scope qualifier source: same as Scope Discipline below.

---

## Schema-Migration Coupling

When a task changes an ORM model (Prisma schema, Drizzle table definition, Django model, ActiveRecord, SQLAlchemy declarative model, etc.), the same task must also include the corresponding migration. Do not split model change and migration into separate tasks — they ship together or not at all.

**Why:** a model change without a migration is a deploy-time failure — production fails to start, or worse, silently runs against an out-of-date schema. The two are conceptually one change; splitting them defers risk to the worst point in the pipeline.

**Self-check before commit:** if the diff touches a model file, scan the diff for a corresponding migration file (`migrations/`, `prisma/migrations/`, `drizzle/`, `alembic/`, `db/migrate/` — depends on stack). If absent, generate the migration and include it in the same commit.

**Exception:** model-file edits that produce no schema change (renaming a TypeScript type alias, reorganizing a model file, adding documentation comments) need no migration — but the diff should make this obvious. When in doubt, run the migration generator and let the diff show "no changes" rather than skipping the check.

**Source:** absorbed from `gsd-build/get-shit-done` (2026-05-09); their schema-drift detection at task boundaries is the load-bearing insight.

---

## Feature Flags for Incomplete or Risky Work

Gate incomplete or rollback-prone features behind a typed env-driven boolean (e.g., `FEATURE_X_ENABLED`). Default off in `.env.example`, flip on per environment — typically dev on, QA opt-in, prod off until promoted. For *what* to externalize see the hardcoded-value triggers in `validation.md`; for the secrets boundary see `guardrails.md`. **Stack-agnostic:** if the project already uses a flag service (LaunchDarkly, GrowthBook, Unleash, in-house), use that instead of inventing a parallel mechanism — check `agent-context.yaml` and existing imports before reaching for an env var.

---

## Reusable UI Components — Story-First

When a project has Storybook installed (`storybook` in `package.json`), every reusable UI component ships with a colocated-or-conventional stories file.

**Reusable** = lives in a shared dir (`components/`, `ui/`, `lib/`) AND is imported by ≥2 call sites. Both conditions required — directory placement is intent, multi-import is evidence.

**Hard requirement (commit gate):** a `*.stories.*` file exists exporting ≥1 story for the component.

**Soft guidance (judgment, not enforcement):**

- Cover meaningful states: default, loading (if async), error (if it can fail), empty (if list-shaped)
- Use the component's actual prop types — no parallel mock types that drift from real usage
- Prefer one-state-per-story over many-states-in-one

**When Storybook is not installed:** see `recommendations.md` — surface the suggestion once when a component crosses the ≥2-consumers threshold; do not enforce.

*Future expansion (out of scope for V1): Histoire (Vue) and Ladle (lightweight React) follow the same methodology and could be added once the base rule is bedded in.*

---

## Component Tests via Storybook

Builds on the Reusable UI Components rule above. When Storybook is installed AND `@storybook/test-runner` is in `package.json`, every story becomes a render-smoke test via headless Playwright.

**Hard requirement:** if `@storybook/test-runner` is installed, it runs as part of the project's `test_command`. Failures block merge per the existing quality-gates discipline (no new gate — leverage the existing one).

**Soft guidance:**

- Stateful or interactive components (dropdowns, modals, forms, toggles) include a `play()` function exercising the primary interaction
- Use `@storybook/test`'s `expect`/`userEvent` — not separate test files
- Investigate flakes within one sprint or delete the offending `play()` — skipped flaky `play()`s lie about coverage

**Out of scope:** cross-page user flows (auth, payment, destructive actions). Those require E2E coverage and may be addressed by a separate future rule.

**Setup suggestion (Storybook installed but test-runner is not):** see `recommendations.md` — surface the suggestion once when a component crosses the ≥2-consumers threshold. Inform the developer; do NOT autonomously add the dependency. Developer chooses whether to install.

---

## Scope Discipline

Implement exactly what was asked — with one qualifier: the *audience* shapes what "asked" means. Platform code (libraries, SDKs, frameworks, public APIs) carries higher implicit standards than application code (scripts, internal CRUD, prototypes).

**Treat the file as platform code if any of the following match:**

- **Path:** `lib/`, `libs/`, `sdk/`, `pkg/` (Go), `packages/*` (monorepo workspaces)
- **Manifest:** `package.json` has `"exports"`, `"main"`, or `"types"` AND lacks `"private": true`; or `pyproject.toml` `[project]`; or `Cargo.toml` `[lib]`; or `go.mod` at a non-`internal/` path
- **Tags:** file has `@public` JSDoc, `export *` re-exports, or appears in a package's `"exports"` map
- **Domain:** auth/authz, persistence layer, public HTTP endpoints, anything published to a registry (npm, PyPI, crates, Maven)
- **Caller boundary:** the function accepts data from an untrusted caller (network, user input, third-party)

**Treat as application code if:** path is `scripts/`, `tools/`, `examples/`, `demos/`, `bin/`, or inside an `internal/` package or a `"private": true` workspace.

**If unsure:** treat as platform and ask — the cost of one clarifying question is lower than shipping a thin public API.

**For platform code,** the implicit ask includes: input validation, typed error variants, retry on transient failures, edge-case handling, structured logging with correlation IDs and PII redaction, threat-modeling the boundary (untrusted callers, output encoding, timing-safe comparisons where applicable), and observability hooks. These are table stakes, not extras.

**For application code,** default to minimal: log on error paths, don't commit secrets, validate input at entry. Don't impose platform discipline on throwaway scripts.

**No silent additions in either case.** If you spot a likely-needed addition outside the inferred scope, surface it as a question — don't silently add, don't silently skip. *"I notice this SDK call has no retry — want that, or intentional?"*

**When to ask vs. follow conventions:** ask only when the addition would meaningfully change diff size or risk profile *and* the answer isn't inferable from existing code style, file location, or framework conventions. Otherwise, follow the observed convention and note it in the commit body.

**Validation pass:** after the change, scan the diff. Every modified line should trace to either the user's explicit request or the audience's implicit standards. If a line doesn't, justify it (one inline comment) or remove it.

This is the agent-side complement to the Anti-Rationalization rule below: anti-rationalization catches you skipping discipline you should follow; scope discipline catches you doing extra work you weren't asked to do. Both are scope failures, opposite directions.

Source: distilled from `forrestchang/andrej-karpathy-skills` (2026-04-19, MIT) — itself derived from Andrej Karpathy's public X post on common LLM coding failures — with platform-audience qualifier, indicator checklist, and surface-as-question protocol added in a 2026-04-20 revision after the original wording was found to overshoot for platform/library/SDK contexts.

---

## Source-Driven Framework Claims

When stating how a framework, library, or runtime behaves (React hook rules, Bun APIs, AWS SDK semantics, etc.), cite the official docs or verify against them. Flag unverified claims explicitly. "I think it works this way" is not evidence; `npm docs`, framework websites, and source code are.

- If you're confident, link the source: "Per the React docs on rules of hooks, hooks must be called at the top level."
- If you're unsure, say so: "I think Bun's `Bun.serve` returns a Server instance, but verify against the docs before relying on this."
- When the user is about to act on framework knowledge, verify first — don't guess.

This rule applies most strongly when you're recommending an approach the developer will execute. Speculation is fine for brainstorming; once it influences a decision or a commit, it needs evidence.

Source: distilled from `addyosmani/agent-skills` (2026-04-19, MIT).

---

## Anti-Rationalization

Common excuses agents (and humans) reach for to skip discipline, with the rebuttal that should kill the excuse:

- *"I'll add tests later."* → Later is a decision to accept regressions now. Write the test or open the ticket before merging.
- *"This is throwaway code."* → Throwaway code has a way of surviving. Write it the same way.
- *"The linter is wrong here."* → Often, but prove it before disabling. An `eslint-disable` without a justifying comment is debt.
- *"It works on my machine."* → Not evidence. Reproduce in CI or a clean environment before claiming it works.
- *"I'll clean this up in a follow-up PR."* → Follow-up PRs are the slowest PRs. Clean up now, or open the ticket before merging.
- *"This is a one-off, no need for a test."* → One-offs become two-offs. If it's worth writing, it's worth a smoke test.

When you catch yourself reaching for one of these, stop and do the thing properly — or surface the trade-off explicitly so the developer can decide. The harm isn't the excuse; it's making the excuse silently.

Source: distilled from `addyosmani/agent-skills` (2026-04-19, MIT).

---

## Pushback Protocol

When the user pushes back — *"find more"*, *"look harder"*, *"are you sure?"*, *"is that really it?"* — do not defend the prior answer without re-running the relevant checks. The pushback is data: the user has a reason to suspect more, even if they can't articulate it.

Before disagreeing:

1. **Walk fresh checklists end-to-end.** Re-run the relevant quality gates. Re-grep for the bug class. Re-read the diff. Open files you didn't read the first time.
2. **Document the negatives.** Note what you checked and what came up empty — *"Grepped for X across `src/`, no other instances. Re-ran test suite, all passing. Re-read auth path, no other unprotected endpoints."*
3. **Then respond** — with what you tried and what you found (or didn't). The user gets to see your work, not just your conclusion.

The failure mode this prevents: dismissing pushback because the prior answer felt complete. Anti-Rationalization above catches you skipping discipline you should follow; Pushback Protocol catches you defending a prior answer instead of re-verifying. Opposite directions, same root: refusing to do the work a second time.

**Source:** absorbed from `elementalsouls/Claude-BugHunter` (2026-05-27); their Pushback Protocol (user says "find more" → walk additional checklists end-to-end, document negatives before disagreeing) is security-framed, but the trust-and-thoroughness logic is general.

---

## Checkpoints

Checkpoints are your safety net. They let you (and the developer) recover from mistakes, resume after crashes, and hand off work between sessions. Think of them as **save points** — create them early and often.

### Three Layers of Checkpoints

| Layer | What It Saves | How | When |
|-------|--------------|-----|------|
| **Agent-level** | File snapshots within the session | Automatic (e.g., Claude Code creates these before each edit) | Every edit — no action needed |
| **Git-level** | Committed code on a branch | `git commit` + `git push` | After every logical milestone |
| **Session-level** | Progress state, decisions, next steps | Update `.ai/STATUS.md` + `.ai/memory.log` | After significant progress or before context fills |

All three layers work together. Agent-level checkpoints protect against mid-task mistakes (undo/rewind). Git-level checkpoints protect against session crashes and make work reviewable. Session-level checkpoints enable handoff between sessions — the next agent (or the same agent in a new session) picks up exactly where you left off.

### Git-Level Checkpoints

Don't accumulate a session's worth of changes in a single commit at the end. **Commit after every logical milestone** — a completed function, a passing test suite, a config change that works.

- **Crash recovery** — If the session ends unexpectedly (token limit, network drop, timeout), committed work is safe. Uncommitted work is lost.
- **Easier review** — Smaller commits are easier for humans to review and revert if needed.
- **Clear history** — Each commit tells a story: what changed and why.

**Rule of thumb:** If you've made a change that builds and passes tests, commit it. Don't wait.

**Push after committing** — In multi-session work, push your commits to the remote branch after each logical milestone. A local commit protects against session crashes, but a pushed commit protects against machine crashes and lets other agents or developers pick up where you left off.

### Session-Level Checkpoints

When you've made significant progress or the conversation is getting long, create a session-level checkpoint:

1. **Commit and push** all current work (git-level checkpoint)
2. **Update `.ai/STATUS.md`** — current position, what's done, what's next, key decisions
3. **Update `.ai/memory.log`** — detailed session summary with rationale and open questions
4. **Compact or hand off** — trigger conversation compaction if available, or tell the developer a fresh session can resume from this checkpoint

See `context-management.md` for full session checkpoint and resumption workflow.
