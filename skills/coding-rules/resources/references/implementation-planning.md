# Implementation Planning Guide

**Only read this file for multi-session projects with 5+ tasks.** For single tasks, `working-patterns.md` is sufficient.

Use this reference to structure multi-session, multi-file projects into phases, milestones, and tasks.

> **Note:** Examples below use `bun` commands. Adapt to your project's toolchain (`npm`, `yarn`, `pnpm`, `deno`, etc.).

> **See also:** `references/roadmap.md` — the lighter-weight feature inventory at project root (`ROADMAP.md`). Implementation plans are spawned from complex roadmap items (typically complexity ≥ 7) and collapse back into a `[x]` checkbox when the plan completes. Use the roadmap for the menu; use this guide only when an item needs phased multi-session execution.

---

## When to Use Structured Planning

**Use this when:**
- Work spans multiple sessions or context windows
- 5+ files or components are affected
- New project scaffolding required
- Work needs to be resumable after interruptions
- Multiple independent tasks exist (parallelism opportunity)

**Skip when:**
- Single file fix or small refactor
- Fewer than 5 tool calls to complete
- Exploratory or research work
- Already in mid-execution (use only at session start)

---

## Core Principles

1. **Phased execution** — Progress through defined phases with clear gates
2. **Milestone delivery** — Each milestone produces verifiable outcomes
3. **Dependencies** — Tasks declare what must complete first
4. **Verification** — Every task must pass build, lint, test
5. **Resumability** — Document state so work survives interruptions
6. **Parallelism** — Independent tasks run concurrently via sub-agents
7. **Right-sized delegation** — Match complexity to execution model

---

## Phases

Six phases organize all work from conception to production:

| Phase | Focus | Exit Criteria |
|-------|-------|---------------|
| **Planning** | Requirements, architecture, design | agent-context.yaml approved, schema designed |
| **Setup** | Scaffolding, dependencies, CI | Monorepo/app structure in place, CI green |
| **Foundation** | Database, auth, shared packages | Schema and migrations work, auth functional |
| **Implementation** | Feature development | Features complete, unit tests pass |
| **Integration** | Cross-app flows, E2E testing | E2E tests pass |
| **Deployment** | Infrastructure, staging, production | Apps deployed, health checks pass |

### Phase Gates

Before moving to the next phase, run:

```bash
bun run build && bun run lint && bun run test
```

All three must pass. If any fails, stay in current phase and fix.

---

## Milestones

Milestones are goal-oriented checkpoints within a phase. Each milestone:
- Delivers a verifiable outcome
- Contains 5-15 tasks
- Has clear success criteria

### Milestone ID Format

Use semantic prefixes that indicate the phase:

```
plan-requirements      # Planning phase
setup-monorepo        # Setup phase
foundation-auth       # Foundation phase
impl-user-api         # Implementation phase
int-auth-flow         # Integration phase
deploy-staging        # Deployment phase
```

Example milestone definition:

```yaml
milestone:
  id: "setup-monorepo"
  phase: "setup"
  goal: "Monorepo scaffolded with all apps and CI configured"
  tasks: [setup-001, setup-002, setup-003, ...]
  verification:
    - "bun install succeeds"
    - "bun run build passes"
    - "bun run test passes"
    - "CI workflow runs"
```

---

## Tasks

Atomic units of work. One task = one focused session, testable outcome.

### Task ID Format

Use phase prefix + sequential number or descriptive suffix:

```
setup-001            # Sequential
setup-init-repo      # Descriptive
auth-middleware      # Feature-based
```

### Task Schema

```yaml
task:
  id: "setup-scaffold-web"
  name: "Scaffold SvelteKit web app"
  phase: "setup"
  milestone: "setup-monorepo"
  area: "web"
  depends_on: ["setup-init-repo"]
  complexity: 4
  description: |
    Create SvelteKit app in apps/web using Bun.
    Configure Tailwind and svelte-adapter-bun.
  acceptance_criteria:
    - "apps/web exists with SvelteKit structure"
    - "bun run dev starts without errors"
    - "Build passes"
    - "Lint passes"
```

### Plan-Fits-Fresh-Context Heuristic

Each plan should be small enough that an agent could execute it in a fresh context window — no accumulated session state required. If executing the plan would need >40% of the model's context for the plan + relevant code + verification output, the plan is too large; split it.

**Why:** large plans accumulate context decay during execution. A plan that "barely fits" starts strong and ends sloppy as the model loses earlier reasoning. Plans sized to leave headroom (~60% of context for actual work) preserve quality through the last task.

**Practical check:** if a plan has >15 tasks, or any single task's acceptance criteria span >5 files, the plan likely violates this heuristic regardless of model. Split before executing.

**Source:** absorbed from `gsd-build/get-shit-done` (2026-05-09); their framing "small enough to execute in a fresh context window" is the load-bearing insight.

---

### Complexity Scale

| Score | Scope | Who | When |
|-------|-------|-----|------|
| **1-3** | Single file, config change, trivial fix | You | Direct |
| **4-6** | Multiple related files, moderate logic | Sub-agent | With clear spec |
| **7-8** | Complex multi-file, design decisions | Sub-agent | With plan approval |
| **9-10** | Architectural, cross-cutting concerns | Sub-agent | With detailed plan + review |

### Task Types

| Type | Description |
|------|-------------|
| `coding` | Implementation, bug fixes, refactoring |
| `research` | Investigation, analysis, comparison |
| `architecture` | Design decisions, schema, API design |
| `testing` | Writing tests, E2E flows |
| `documentation` | Docs, READMEs, API docs |
| `coordination` | Task breakdown, planning, review |

---

## Task States

| State | Meaning |
|-------|---------|
| `TODO` | Not started |
| `BLOCKED` | Waiting on dependencies |
| `IN_PROGRESS` | Currently being worked on |
| `DONE` | Completed and verified |
| `FAILED` | Attempted but failed |

State transitions:
- `TODO` → `IN_PROGRESS` (start work)
- `TODO` → `BLOCKED` (if dependencies unmet)
- `IN_PROGRESS` → `DONE` (if all checks pass)
- `IN_PROGRESS` → `FAILED` (if retries exhausted)
- `BLOCKED` → `TODO` (when dependencies complete)
- `FAILED` → `TODO` (retry after fix)

---

## Task Dependencies

Tasks declare what must complete before they start:

```yaml
task:
  id: "foundation-shared-types"
  depends_on: ["setup-scaffold-api", "foundation-db-schema"]
```

Rules:
- Tasks with no dependencies start immediately
- A task is **BLOCKED** until all dependencies are **DONE**
- No circular dependencies allowed

---

## Plan Approval (Complexity >= 7)

For complex tasks, require plan approval before implementation:

1. Task enters read-only exploration mode
2. Produce implementation plan:
   - Files to modify (with rationale)
   - Approach description
   - Risk assessment
   - Test strategy
3. Coordinator reviews and approves
4. If approved: proceed with implementation
5. If rejected: revise based on feedback

Require approval for:
- Complexity 7-8 (complex, multi-file)
- Complexity 9-10 (architectural)
- Any change touching shared types or database schema

---

## Quality Gates

Automated checks that run after each task. Task is NOT DONE until all gates pass.

### Standard Gate (every task)

```bash
bun run build && bun run lint && bun run test
```

### Extended Gate (after milestone)

```bash
bun run build && bun run lint && bun run test && bun run test:e2e
```

### Enforcement

| Check | When | Failure Action |
|-------|------|----------------|
| **Build** | Every task | Block, fix required |
| **Lint** | Every task | Block, fix required |
| **Unit test** | Every task | Block, fix required |
| **E2E test** | After milestone | Flag, may not block |
| **Type check** | Tasks touching shared types | Block, fix required |

---

## Plan Document Format

Create `implementation-plan.yaml` at project root:

```yaml
project: "My Project"
phases:
  - id: "planning"
    milestones:
      - id: "plan-requirements"
        goal: "Requirements and scope documented"
        tasks:
          - id: "plan-001"
            name: "Define core features"
            complexity: 3
            depends_on: []
          - id: "plan-002"
            name: "Design database schema"
            complexity: 5
            depends_on: ["plan-001"]

  - id: "setup"
    milestones:
      - id: "setup-monorepo"
        goal: "Monorepo scaffolded and building"
        tasks:
          - id: "setup-001"
            name: "Initialize Bun monorepo"
            complexity: 4
            depends_on: ["plan-001", "plan-002"]
          # ... more tasks
```

---

## Completion Checklist

A task is **DONE** when ALL of these pass:

1. ✅ Acceptance criteria met
2. ✅ `bun run build` passes
3. ✅ `bun run lint` passes
4. ✅ `bun run test` passes
5. ✅ No regressions in other tests

If any fail, the task is NOT done. Fix and re-verify.

---

## Commits

Use Conventional Commits format:

```
<type>(<scope>): [<issue-id>] <description>

<body>
```

Types: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`

Examples:

```
feat(api): [TASK-001] add user authentication endpoint
fix(web): resolve form validation race condition
chore(setup): initialize monorepo structure
```

---

## Logging Progress

After each task, update `.ai/memory.log` using the canonical format from `communication.md`. Example:

```
[2025-02-09T10:30:00Z]
Task: setup-001 (Initialize Bun monorepo)
Action: Scaffolded monorepo with workspaces and build scripts
Files: package.json, bunfig.toml, apps/, packages/
Commit: abc123def
Status: DONE
Notes: Duration ~45min. Configured workspaces, added build scripts.
```

---

## Execution Modes

### Solo (< 5 tasks)

Execute directly without delegation:
1. Read plan
2. Find next READY task
3. Execute
4. Verify
5. Commit
6. Mark DONE
7. Repeat

### Sub-Agents (5-15 tasks)

Use sub-agents for parallelism:
1. Identify independent task clusters
2. Route tasks by complexity
3. Spawn sub-agents for independent tasks
4. Monitor progress
5. Verify and integrate results
6. Unblock dependent tasks

### Agent Team (15+ tasks)

Full team coordination with native teammates (if available).

---

## Resumability

If session may end, document state for resumption:

| File | Record |
|------|--------|
| `.ai/STATUS.md` | Current phase, milestone, next task |
| `.ai/memory.log` | Session summary, blockers |
| `implementation-plan.yaml` | Task states, progress |

At session end:
1. Commit all work
2. Update `STATUS.md`
3. Log session end in `memory.log`
4. Ensure build passes
5. Document blockers in `.ai/BLOCKERS.md`

At session resume:
1. Read `STATUS.md`
2. Read recent `memory.log` entries
3. Find next READY task
4. Verify build
5. Continue
