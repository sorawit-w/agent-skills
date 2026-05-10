# Bug Fix Workflow

You are fixing a bug. Follow these steps in order.

<pre_work>
## 1. Pre-Work

You MUST complete these before writing any code:

1. Read `references/debugging.md` — systematic debugging approach
2. Read `references/communication.md` — commit format, logging
3. **Answer the Worktree Gate** (see BOOTSTRAP.md — 3 questions). If the gate → worktree, create it; else create an in-place branch.

   Worktree path (gate → yes):
   ```bash
   git worktree add .worktrees/<branch-name> -b fix/<short-description>
   cd .worktrees/<branch-name>
   {package_manager} install
   ```
   In-place path (gate → no, or npm fallback):
   ```bash
   git checkout -b fix/<short-description>
   ```
   See `references/git-worktrees.md` for npm detection and fallback rules.
4. **Baseline check** — establish which tests already fail vs. which are yours:
   - If you just created this worktree or in-place branch from a known-good base: **skip full gates** — run only `{test_command}` to note any pre-existing failures
   - If `git status` shows a clean working tree and the last commit's gates passed: **skip full gates**
   - Otherwise, run full gates:
     ```bash
     {build_command} && {lint_command} && {test_command}
     ```
   Note which tests fail — these are your baseline (not caused by your fix).
</pre_work>

<reproduce>
## 2. Reproduce

Before fixing anything, reproduce the bug:

1. Identify the exact steps or input that trigger the bug
2. Confirm you can see the failure (test failure, error message, wrong output)
3. If you cannot reproduce, ask the user for more details — do not guess at a fix

Document the reproduction: what you did, what happened, what should have happened.
</reproduce>

<diagnose>
## 3. Diagnose

Follow the systematic debugging process:

1. **Hypothesize** — form up to 3 hypotheses for the root cause
2. **Test each hypothesis** — narrow down with targeted checks (logs, breakpoints, assertions)
3. **Identify the root cause** — not just the symptom

Do NOT apply trial-and-error fixes. If 3 hypotheses fail, document what you tried, mark BLOCKED, and ask for help.

Check the knowledge base (`.ai/knowledge/`) — a similar bug or lesson may already be documented.
</diagnose>

<delegate_check>
## 4. Check: Should You Delegate?

If the fix touches 3+ files, involves iterative debugging cycles, or will take >15 minutes, read `references/sub-agent-delegation.md` and delegate. If your platform does not support sub-agents, implement sequentially but still follow the commit gate in section 5.
</delegate_check>

<fix>
## 5. Fix — Commit Gate

Execute these steps in order. Do NOT skip the commit.

1. Write a failing test that captures the bug (the test MUST fail before your fix)
2. Apply the minimal fix — don't refactor unrelated code
3. **Iteration check** — run the failing test + related tests to confirm the fix works. This is fast feedback, not full verification.
4. **Commit check** — run full quality gates before committing:
   ```bash
   {build_command} && {lint_command} && {test_command}
   ```
5. Confirm no regressions — all tests that passed before still pass
6. **COMMIT now:**
   ```bash
   git add <specific-files>
   git commit -m "fix(<scope>): <description>"
   ```
7. Append to `.ai/memory.log`

If the fix requires multiple changes, repeat steps 1–7 for each change. Each completed fix gets its own commit. See `references/quality-gates.md` for gate tier details.
</fix>

<finish>
## 6. Finish

Complete ALL of these before declaring done:

1. **Quality gates pass** — all tests green, no regressions
2. **All changes committed and pushed:**
   ```bash
   git status  # must show clean working tree
   git worktree list  # verify no other worktrees have uncommitted work
   ```
3. **Memory log updated** — what the bug was, what caused it, how you fixed it
4. **STATUS.md updated**
5. **Manual verification instructions provided:**
   ```markdown
   ## How to Verify
   1. [Steps to reproduce the original bug — should no longer occur]
   2. [Steps to verify the fix works correctly]
   3. [Related areas to spot-check for regressions]
   ```
6. **Project knowledge artifacts** — propose additions before writing; skip if nothing applies:
   - **`.ai/knowledge/` lesson** if this bug reveals an operational lesson worth keeping
   - **`CONTEXT.md` update** if a new domain term was introduced or renamed. See `references/domain-glossary.md`.
7. **Branch finalization — pick one of four options** (same as feature workflow):
   - **Open PR** (default) — push branch; open PR; keep worktree until PR is merged
   - **Merge locally** (solo project / approved hotfix) — merge, then `git worktree remove .worktrees/<name>`
   - **Preserve branch** (more work expected) — keep worktree; note reason in `.ai/memory.log`
   - **Discard** (requires explicit user confirmation) — `git worktree remove --force .worktrees/<name>`
   
   If using an in-place branch (npm fallback), only options 1 or 2 apply.

8. **Do NOT merge to a protected branch without explicit user instruction.**

Full worktree lifecycle details: `references/git-worktrees.md`
</finish>
