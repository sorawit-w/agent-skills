---
name: sub-agent-coordinator
description: >
  Orchestrate multi-agent work through fan-out, pipeline, and specialist patterns.
  Use this skill when delegating focused tasks to parallel sub-agents, coordinating
  iterations, or architecting complex workflows. Load this whenever you need
  spawning signals, briefing templates, coordination patterns, or communication protocols.
instructions: |
  Load this skill when:
  - Delegating work to sub-agents (fan-out parallel tasks, pipelines, specialist routing)
  - You need briefing templates (quick vs. full) for sub-agent spawn commands
  - Architecting coordination patterns (fan-out, pipeline, specialist domain, review/validation)
  - Resolving coordination issues (file conflicts, communication, nested delegation)
  - Designing workflow checkpoints and quality gates
  
  Do NOT load this if:
  - Your platform does not support sub-agents (use sequential implementation instead)
  - The task is trivial (<2 minutes) or single-file
  - You need only basic delegation signals (the fallback stub covers this)

tags:
  - coordination
  - delegation
  - orchestration
  - sub-agents
  - parallelization
  - workflow
---

# Sub-Agent Coordinator

Orchestrate focused work across multiple sub-agents using proven patterns. This skill handles briefing, spawning, communication, and verification when delegating complex tasks.

Use this skill to **parallelize independent work, avoid conflicts, and maintain coordination state** across sub-agents.

---

## What Are Sub-Agents

Sub-agents are separate agent instances that handle a scoped piece of work. They:
- Work independently on assigned tasks
- Operate within defined constraints and boundaries
- Report back with structured results
- Can be spawned in parallel for independent tasks

A sub-agent is not a human teammate — it is another instance of you, task-focused and context-limited, designed to parallelize work that would otherwise be sequential.

---

## Coordinator vs. Implementer

When you are orchestrating work, adopt the **coordinator mindset**:

| **Your Job (Coordinator)** | **NOT Your Job** |
|----------------------------|------------------|
| Break down tasks | Write every line of code yourself |
| Brief and spawn sub-agents | Debug iteratively for 20+ minutes |
| Review work before committing | Grind through boilerplate |
| Integrate results and resolve conflicts | Spend >2 min on implementation when you could delegate |
| Unblock stuck sub-agents | Ignore sub-agent status updates |
| Keep the board and status files current | Let coordination state go stale |

**The 2-Minute Rule (decision boundary, not absolute):**

| Estimated task time | Guidance |
|--------------------|----------|
| < 2 min | Handle directly — delegation overhead exceeds the work itself |
| 2–15 min | Judgment call — delegate if independent/parallelizable; handle directly if tightly coupled |
| > 15 min | Delegate unless the work is tightly coupled and requires sequential understanding |

Your time as coordinator is better spent on orchestration — breaking down tasks, verifying quality, unblocking dependencies, and maintaining project state.

This doesn't mean you never write code. Trivial fixes, config tweaks, and one-line changes are fine to handle directly. The point is: don't get absorbed in implementation when sub-agents can do it in parallel while you coordinate.

---

## Spawning Signals — When to Delegate Immediately

These signals mean "spawn a sub-agent now, don't attempt it yourself":

| Signal | Why |
|--------|-----|
| 🐛 Debugging / fixing errors | Iterative fix-test cycles are time-consuming and benefit from focused attention |
| 🔧 Iterative work (multiple attempts) | Styling, performance tuning, API integration — likely needs multiple rounds |
| 🏗️ Feature implementation (3+ files) | Multi-file features are sub-agent work |
| 📦 Dependency issues | Cache clearing, lock file regeneration, version conflicts — tedious and scoped |
| ✅ Testing / verification (suites, not single tests) | Writing comprehensive test suites across multiple files is parallelizable and well-scoped. A single unit test is typically below the 2-minute threshold — handle directly. |
| 📝 Documentation (>1 file) | Updating docs across multiple locations |
| 🔍 Investigation / research | Exploring unfamiliar codebase areas or third-party APIs |

**Heuristic: "This should be quick" → Spawn anyway.** Optimism bias in task estimation is real. If you catch yourself thinking a task is trivial, that's often the moment to delegate it.

---

## When to Delegate

Use sub-agents to parallelize work and reduce total execution time.

| Scenario | Why Delegate | Benefit |
|----------|-------------|---------|
| **Parallel independent tasks** | Tasks 1, 2, 3 don't depend on each other | Spawn all 3 at once, finish in 1/3 the time |
| **Specialized domain work** | Task needs specific expertise (i18n, design systems, DevOps) | Route to agent with relevant skills loaded |
| **Large refactoring** | Multiple files in different areas affected | Parallelize file-by-file refactoring |
| **Research + implementation** | Research findings feed implementation | Spawn researcher while you start implementation |
| **Feature review/validation** | Implement feature, have second agent validate | Double-check work in parallel |
| **Monorepo scaling** | 3+ apps being scaffolded | Scaffold api, web, admin in parallel |

---

## When NOT to Delegate

Some work should stay with the primary agent.

| Scenario | Why NOT Delegate |
|----------|------------------|
| **Tightly coupled changes** | Changes in File A affect File B affect File C | Sequential understanding required |
| **Single-file edits** | 1-2 files, quick fix | Overhead of delegation exceeds benefit |
| **Cross-cutting decisions** | Decision made in Task A affects Task B | Needs unified judgment |
| **Architecture decisions** | Core design that all tasks depend on | Needs single owner |
| **Tasks < 15 minutes** | Quick tasks | Delegation overhead > actual work |

---

## Briefing Templates

Match briefing depth to task complexity. Over-briefing simple tasks adds overhead; under-briefing complex tasks causes wrong implementations.

### Quick Brief (Complexity 1–5)

For straightforward, well-scoped tasks. Three sections, keep it tight:

```
Task: [what to do]
Scope: [which files/components to touch]
  - [file 1]
  - [file 2]
  Out of scope: [what NOT to touch]
Budget: ~[N] tool calls
Done when:
  ✅ [criterion 1]
  ✅ [criterion 2]
  ✅ Quality gates pass (build + lint + test)
```

**Tool budget guidelines:** Set a budget proportional to complexity. ~15 calls for simple tasks (1–3), ~30 for medium (4–5), ~50 for complex (6+). If a sub-agent approaches its budget without finishing, it should wrap up and report what's done vs. what remains — not spiral into unbounded iteration.

The sub-agent reads the project's existing config and conventions on its own. Only add explicit constraints if they deviate from the project's defaults.

### Full Brief (Complexity 6+)

For complex, multi-file, or high-risk tasks.

#### Context Section

```
Project: [project-name]
Branch: [branch-name or "main"]
State: [description of what's already done]
Phase: [current phase]
Milestone: [current milestone]
```

#### Task Section

```
Task ID: [task-id]
Name: [task-name]
Complexity: [1-10]
Acceptance Criteria:
  - [criterion 1]
  - [criterion 2]
  - [criterion 3]
```

#### Scope Section

```
Scope: Exactly which files/components you'll work on:
  - [file or component 1]
  - [file or component 2]

Out of scope (do NOT touch):
  - [system/component to avoid]
  - [area not part of this task]
```

#### Constraints Section

```
Constraints:
- Do not modify [shared file] — other tasks depend on it
- Follow [naming convention] for consistency
- Use [library/pattern] established in the codebase
- Do not commit to main — leave on working branch
- Tool budget: ~[N] calls (wrap up and report if approaching limit)
```

#### Success Criteria Section

```
Done when:
  ✅ Acceptance criteria met
  ✅ {build_command} passes
  ✅ {lint_command} passes
  ✅ {test_command} passes
  ✅ No regressions in other tests
```

#### Files to Read First

```
Start by reading these files to understand the context:
  1. [file 1] — architecture overview
  2. [file 2] — conventions used
  3. [file 3] — types or utilities you'll reference
```

#### Reporting Section

```
When done, provide:
  - Task status: DONE | FAILED | BLOCKED
  - Files modified: [list of files]
  - Tests added: [list of test files]
  - Verification results: build pass/fail, lint pass/fail, test pass/fail
  - Any notes or decisions made during implementation
  - Any blockers encountered
```

---

## Coordination Patterns

Match the coordination pattern to your work structure.

### Fan-Out: Parallel Independent Tasks

Use when you have multiple independent tasks that don't depend on each other.

```
Task A (setup-api)      ──────┐
Task B (setup-web)      ──────┼─→ Wait for all → Verify → Next round
Task C (setup-admin)    ──────┘
```

Example:
- Spawn setup-api, setup-web, setup-admin in parallel
- Each sub-agent works independently
- When all complete, run quality gates
- Unblock dependent tasks (setup-shared, setup-tailwind, etc.)

### Pipeline: Producer → Consumer

Use when one task produces output that another consumes.

```
Task A (foundation-schema) → Task B (foundation-types) → Task C (foundation-auth)
```

Example:
- Spawn Task A (schema design)
- Wait for completion
- Spawn Task B (type generation from schema)
- Wait for completion
- Spawn Task C (auth implementation using types)

### Specialist Domain Routing

Use when delegating to agents with specific skills loaded.

```
Standard agent       → General coding tasks
Agent + i18n skill   → Localization and translation
Agent + design skill → Design system updates
Agent + DevOps skill → CI/CD and infrastructure
```

### Review/Validation

Use when you want parallel verification of completed work.

```
You: Implement feature X (in-progress)
Sub-agent: Review feature X from Task A (in parallel)
Merge results: Integrate review feedback
```

---

## Coordination Rules

Follow these rules to avoid conflicts and maintain coherence:

1. **Non-overlapping files** — Each sub-agent works on different files. If two tasks touch the same file, execute sequentially, not in parallel.

2. **Clear boundaries** — Define exactly which files each sub-agent will modify. Include "out of scope" section in briefing.

3. **Trust-but-verify after each sub-agent** — Read the sub-agent's verification report. Only re-run quality gates yourself if:
   - The report is missing or incomplete (no gate results provided)
   - The report shows warnings or partial failures
   - The sub-agent touched shared files or public APIs
   - You're about to merge into a protected branch
   
   If the report shows clean passes with evidence, accept it and move on. Don't redundantly re-run gates that just passed.

4. **Resolve conflicts in main agent** — If two sub-agents touch the same code, the main agent integrates and resolves conflicts. **Always run gates after conflict resolution** — merging can introduce issues that neither sub-agent's individual run would catch.

5. **Structured reporting** — Each sub-agent reports back with:
   - Status (DONE, FAILED, BLOCKED)
   - Files modified
   - Test results
   - Any decisions made during implementation
   - Any blockers

6. **No nested sub-agents** — Sub-agents do not spawn their own sub-agents. All spawning is done by the coordinating agent.

7. **Unblock dependent tasks** — After a sub-agent completes, immediately evaluate which downstream tasks are now unblocked and can be spawned next.

8. **Worktree ownership — shared by default** — When the coordinator is working in a worktree (the default for feature and bugfix workflows), sub-agents operate within the *same* worktree. This keeps coordination simple: one branch, one directory, one source of truth. Rely on rule 1 (non-overlapping files) to prevent conflicts. Only create sibling worktrees for sub-agents if file-conflict problems are observed repeatedly with the shared approach — treat it as an escalation, not a default.

---

## Communication Protocol

Delegation doesn't end at spawning. Active coordination prevents stuck sub-agents and wasted time.

**Sub-agents should:**
- Report progress proactively, especially on long-running tasks
- Ask the coordinator immediately when blocked — don't guess or work around constraints silently
- On completion, report with the structured format from the briefing template (status, files, tests, decisions, blockers)

**The coordinator should:**
- Check in on long-running sub-agents at ~30-minute intervals for tasks estimated at >1 hour
- Respond to unblocking requests promptly — a stuck sub-agent wastes parallel capacity
- Verify results immediately after sub-agent reports back (don't batch verification)
- Maintain a mental model of what each sub-agent is working on and when it should finish

---

## Example Scenarios

### Scenario 1: Setting Up a New Monorepo (Fan-Out)

**Main task:** Setup phase, setup-monorepo milestone

**Parallel tasks:**
- setup-001: Initialize Bun monorepo (complexity 4)
- setup-002: Scaffold API (complexity 3)
- setup-003: Scaffold web app (complexity 3)
- setup-004: Scaffold admin app (complexity 3)
- setup-005: Create shared package (complexity 2)

**Execution:**
1. Execute setup-001 directly (primary agent)
2. Wait for setup-001 to complete (DONE)
3. Spawn sub-agents for setup-002, setup-003, setup-004, setup-005 in parallel
4. Each sub-agent works on separate directory:
   - Sub-agent A: `apps/api`
   - Sub-agent B: `apps/web`
   - Sub-agent C: `apps/admin`
   - Sub-agent D: `packages/shared`
5. Wait for all to complete
6. Run quality gates: `{build_command} && {lint_command} && {test_command}`
7. Proceed to next round of tasks (setup-tailwind, setup-drizzle, setup-ci)

**Benefit:** 4 independent 30-minute tasks run in parallel instead of sequentially, reducing total time from 120 minutes to ~40 minutes.

---

### Scenario 2: Large Translation Work (Specialist Routing)

**Main task:** Implementation phase, feature milestone for multi-language support

**Parallel tasks:**
- impl-i18n-001: Extract strings from codebase (complexity 5)
- impl-i18n-002: Translate to Spanish (complexity 4)
- impl-i18n-003: Translate to French (complexity 4)
- impl-i18n-004: Translate to German (complexity 4)

**Execution:**
1. Execute impl-i18n-001 directly (extract strings)
2. Wait for completion
3. Spawn sub-agents for impl-i18n-002, impl-i18n-003, impl-i18n-004 with i18n skill loaded:
   - Sub-agent A + i18n skill: Spanish translation
   - Sub-agent B + i18n skill: French translation
   - Sub-agent C + i18n skill: German translation
4. Each works on translation/[language].json file
5. Wait for all to complete
6. Merge translations
7. Run E2E tests with all languages

**Benefit:** 3 translation tasks run in parallel. Each sub-agent has context-specific i18n skills, producing better translations.

---

### Scenario 3: Feature Implementation + Validation (Parallel Review)

**Main task:** Implement user authentication feature

**Setup:**
- Main agent: Implements auth feature (impl-auth)
- Sub-agent: Reviews implementation (impl-auth-review)

**Execution:**
1. Main agent starts impl-auth (still in-progress)
2. Spawn sub-agent with previous task context to:
   - Review API security
   - Check error handling
   - Validate JWT implementation
   - Suggest improvements
3. Sub-agent completes review while main agent is still coding
4. Main agent finishes implementation
5. Integrate review feedback
6. Run quality gates

**Benefit:** Review happens in parallel with implementation, providing feedback immediately after first draft.

---

## Spawning Checklist

Before spawning a sub-agent, verify:

- [ ] Task is independent (no same-file conflicts with other in-progress tasks)
- [ ] Task has clear acceptance criteria
- [ ] Task has < 30 minutes of estimated work (or is a natural checkpoint)
- [ ] Briefing template is complete (context, scope, constraints, success criteria)
- [ ] All dependencies are DONE (no BLOCKED tasks)
- [ ] Files to read are identified
- [ ] Constraints are explicit ("do not modify X")
- [ ] Reporting format is clear

---

## After Sub-Agent Returns

1. **Read the report** — Status, files modified, test results
2. **Run quality gates** — Build, lint, test immediately
3. **Review code** — If time permits, quick scan of changes
4. **Resolve conflicts** — If overlaps occurred, merge carefully
5. **Mark task DONE or FAILED** — Update task state based on report
6. **Unblock dependents** — Find tasks that depend on this one and move to READY
7. **Log result** — Record with sub-agent's notes
8. **Spawn next batch** — If multiple tasks ready, spawn next parallel batch

---

## Common Mistakes to Avoid

- **Overlapping file edits** — Two sub-agents modifying the same file → conflicts. Use fan-out only for non-overlapping work.
- **Insufficient briefing** — Sub-agent lacks context → wrong implementation. Include "files to read first" and "conventions to follow".
- **Tight coupling** — Task A depends on Task B, but you spawn both in parallel → Task B has no context. Only parallelize truly independent tasks.
- **Blind trust OR blind re-verification** — Read the sub-agent's verification report. Accept clean results; re-run gates only when the report is missing, incomplete, or suspicious.
- **No structured reporting** — Sub-agent comes back with prose → hard to verify. Require status, files, tests, pass/fail.
- **Nested delegation** — Sub-agent spawns another sub-agent → coordination chaos. All spawning happens at coordinator level.

---

Originally part of the coding-rules project (MIT).
