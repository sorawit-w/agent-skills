# Feature / Enhancement / Refactor Workflow

You are implementing a new feature, enhancement, or refactoring task. Follow these steps in order.

<pre_work>
## 1. Pre-Work

You MUST complete these before writing any code:

1. Read `references/working-patterns.md` — task approach, code standards
2. Read `references/communication.md` — commit format, logging, branch naming
3. Read project conventions — linter config, formatter config, existing code patterns
4. **Answer the Worktree Gate** (see BOOTSTRAP.md — 3 questions). If the gate → worktree, create it; else create an in-place branch.

   Worktree path (gate → yes):
   ```bash
   git worktree add .worktrees/<branch-name> -b <type>/<short-description>
   cd .worktrees/<branch-name>
   {package_manager} install    # bun install, pnpm install, etc.
   ```
   In-place path (gate → no, or npm fallback):
   ```bash
   git checkout -b <type>/<short-description>
   ```
   Ensure `.worktrees/` is in `.gitignore` before using worktrees. See `references/git-worktrees.md` for npm detection and fallback rules.
5. **Baseline check** — confirm you're starting from a clean state:
   - If you just created this worktree or in-place branch from a known-good base (main/develop passed CI): **skip baseline gates**
   - If `git status` shows a clean working tree and the last commit's gates passed: **skip baseline gates**
   - Otherwise, run full gates to establish baseline:
     ```bash
     {build_command} && {lint_command} && {test_command}
     ```
     If the baseline is broken, fix it first or flag it to the user.
</pre_work>

<clarify>
## 2. Clarify

If the request is ambiguous, ask 1–2 targeted questions. State your assumptions explicitly. Don't silently guess.

Check the knowledge base (`.ai/knowledge/`) for relevant decisions, conventions, or lessons that apply to this task. If the knowledge base answers a "why" question, use it instead of guessing or asking.
</clarify>

<plan>
## 3. Plan

1. Restate the problem — confirm you understand what's being asked
2. Identify affected files — scope the change before editing
3. Check dependencies — will this change break anything downstream?
4. **If the feature introduces a new third-party vendor** (auth, db, payments, mailer, etc.), consult `references/vendor-adapters.md` for the ports/adapters pattern. Define the port from consumer needs; add the adapter under `adapters/<vendor>/`.
5. Rate complexity (1–10):

| Complexity | Approach |
|-----------|----------|
| Low (1–3) | Handle directly. Self-review when done. |
| Med (4–6) | Write a brief plan, then implement. Self-check when done. |
| High (7–8) | Write plan, get user approval before starting. QA sub-agent when done. |
| Critical (9–10) | Plan + approval + staged rollout. QA sub-agent when done. |

For complexity 6+, read `references/implementation-planning.md` for structured planning.
</plan>

<delegate_check>
## 4. Check: Should You Delegate?

**Before implementing, check the delegation signals below.** If ANY signal matches, you MUST read `references/sub-agent-delegation.md` and spawn sub-agents instead of implementing everything yourself.

| Signal | Match? |
|--------|--------|
| Task touches 3+ files | → Delegate |
| Task involves iterative debugging/fixing | → Delegate |
| Multiple independent sub-tasks exist | → Delegate in parallel |
| You catch yourself thinking "this should be quick" | → Delegate |
| Task estimated at >15 minutes of focused work | → Delegate |

If NO signals match (single-file change, trivial fix), proceed to implement yourself.

**If your agent platform does not support spawning sub-agents** (e.g., Cursor, Windsurf, Copilot), skip delegation and implement sequentially using the task loop below. The loop still applies — commit after each piece of work.

If you delegate, brief each sub-agent with: task + scope + files + done-when + constraints. Use quick briefs for complexity ≤5, full briefs for 6+. See `references/sub-agent-delegation.md` for templates.
</delegate_check>

<implement>
## 5. Implement — Task Loop

Whether you implement yourself or coordinate sub-agents, repeat this loop for each piece of work:

```
┌─→ 1. PICK   — Choose the next task or sub-task
│              If tracked in ROADMAP.md, flip [ ] → [~]
│   2. DO     — Implement (prefer TDD: failing test → minimal code → pass)
│   3. CHECK  — Iteration check (fast feedback):
│              Choose tier based on what you changed (see below)
│   4. COMMIT — Commit check (full gates) + commit:
│              {build_command} && {lint_command} && {test_command}
│              git add <specific-files>
│              git commit -m "<type>(<scope>): <description>"
│              If commit completes a ROADMAP feature, flip [~] → [x]
│              and sweep to ## Shipped (immediately or in batches)
│   5. LOG    — Append to .ai/memory.log (see BOOTSTRAP.md section 4 for format)
│   6. PUSH   — In multi-session work: git push
└─── 7. REPEAT — Go to step 1 for the next task
```

### Iteration Check Tiers (step 3)

Pick the tier that matches your change. See `references/quality-gates.md` for details.

| Changed... | Iteration check | Why |
|-----------|----------------|-----|
| Config, docs, comments, formatting only | `{lint_command}` | No logic changed — lint catches typos/format |
| Logic in 1–2 files | `{lint_command}` + related tests only | Fast feedback on what you just touched |
| 3+ files, cross-cutting, or dependency changes | Full: `{build_command} && {lint_command} && {test_command}` | Too risky to skip — run everything |

**"Related tests only"** = run the test file(s) that cover the module you changed. If unsure which tests are related, run the full suite.

### Commit Check (step 4)

**Always run full gates before committing — no exceptions.** The iteration check is for fast feedback during coding. The commit check is your safety net.

```bash
{build_command} && {lint_command} && {test_command}
```

If gates fail, fix the issue and re-run before committing.

**Rules for this loop:**
- Do NOT batch commits at the end. Each piece of completed work gets its own commit.
- Do NOT skip the commit check. Full gates must pass before every commit.
- If stuck after 3 attempts on one task, log what you tried, mark BLOCKED, move to the next task.
- If a ROADMAP item is blocked mid-loop, flip `[~]` → `[!]` with a one-line reason and continue. Resume by flipping back to `[~]` when the blocker clears.
- Match existing patterns in the codebase — consistency over local optimization.
- **Debug systematically** — reproduce → hypothesize (max 3) → fix. No trial-and-error. Details: `references/debugging.md`
</implement>

<validate>
## 6. Validate

After all tasks in the loop are complete, perform final validation:

| Complexity | Validation |
|-----------|-----------|
| Low (1–3) | Self-review: run gates, re-read diff, confirm it does what was asked |
| Med (4–6) | Self-check: spec compliance check + run gates fresh |
| High (7+) | Spawn QA sub-agent for two-stage review: spec compliance then code quality |

**No completion claims without fresh verification evidence.** Never say "should work" or "probably passes" — run the check, read the output, state the result.

Details: `references/validation.md`
</validate>

<finish>
## 7. Finish

Complete ALL of these before declaring done:

1. **Final quality gates pass:**
   ```bash
   {build_command} && {lint_command} && {test_command}
   ```
2. **All changes committed and pushed:**
   ```bash
   git status  # must show clean working tree
   git worktree list  # verify no other worktrees have uncommitted work
   ```
3. **Memory log updated** — session summary appended to `.ai/memory.log`
4. **STATUS.md updated** — `.ai/STATUS.md` reflects current state
5. **`ROADMAP.md` self-check** — completed features flipped to `[x]` and swept to `## Shipped`; new in-scope items added if scope expanded mid-task. The flips should already have happened in the COMMIT step of the loop; this is the verification
6. **Manual verification instructions provided** — tell the developer how to test:
   ```markdown
   ## How to Verify
   1. [Step-by-step instructions]
   2. [What to look for]
   3. [Edge cases to test]
   4. [Environment setup if needed]
   ```
7. **DEVELOPER_TODO.md created** if any human actions are needed (API keys, cloud resources, etc.)
8. **Project knowledge artifacts** — propose additions before writing; skip if nothing applies:
   - **`.ai/knowledge/` entry** for a new decision, convention, or lesson
   - **`CONTEXT.md` update** for new domain terms used 2+ times. See `references/domain-glossary.md`.
9. **Branch finalization — pick one of four options** (ask the user if unclear):

   | Option | When to use | Action |
   |--------|-------------|--------|
   | **Open PR** (default) | Work is ready for human review | Push branch; open PR; keep worktree until PR is merged |
   | **Merge locally** | Solo project, fast-path, or approved | `git checkout <base>`, merge, then `git worktree remove .worktrees/<name>` |
   | **Preserve branch** | More work expected later | Keep worktree; note branch + reason in `.ai/memory.log` |
   | **Discard** | Work is a dead-end or spike | Requires explicit "discard" confirmation from user; then `git worktree remove --force .worktrees/<name>` |

   If using an in-place branch (npm fallback), skip worktree cleanup — only option 1 or 2 applies.

10. **Do NOT merge to a protected branch without explicit user instruction** — leave option 1 (PR) as the default.

Details: `references/context-management.md`, `references/git-worktrees.md`
</finish>
