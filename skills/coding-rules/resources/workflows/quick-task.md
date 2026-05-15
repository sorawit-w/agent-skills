# Quick Task Workflow

For simple tasks — single-file edits, config changes, documentation updates, or fixes with obvious root cause (complexity 1–3).

**Branching:** quick-task stays in-place. Use a normal `git checkout -b` — worktree overhead is not justified for changes this small. Worktree default applies only to `workflows/feature.md` and `workflows/bugfix.md`. (If the task turns out to be more complex than expected, escalate to feature.md and create a worktree at that point.)

<fit_check>
## Fit Check (before you start)

The quick-task path is appropriate only when ALL of these hold. If even one fails, switch to `workflows/feature.md` from step 2 (Clarify) — no exceptions.

- **No new files** — you're editing existing files only, not adding modules
- **No test logic changes** — tests may *run* during checks, but you're not modifying assertions, test scaffolding, or fixtures
- **No schema, contract, or public-type changes** — no DB migrations, no exported type/interface shape changes, no public API edits
- **No high-stakes paths** — auth, payments, migrations, infra, CI/CD, production-traffic-shaping constants (see BOOTSTRAP.md §3 "High-stakes path override")
- **Diff stays ≤ ~50 LOC** — rough budget; if you're approaching it, the change isn't a quick task
- **Change is strings, copy, comments, config values, data, or formatting** — not new logic, not refactoring, not behavior change

**Why this is hard-floored, not advisory:** quick-task skips overhead because the risk surface is bounded. Violating any criterion means the risk surface is no longer bounded — at that point the savings are illusory and the discipline of `feature.md` is the cheaper path overall.

**State your fit check before starting**, in 2–4 lines:

```
Quick-task fit:
- Files: <list>
- Estimated LOC: <number>
- Type of change: <strings / config / comments / docs / formatting>
- No new files / tests / schema / contracts / high-stakes paths: confirmed
```

If you can't state it cleanly, the task doesn't fit. Switch workflows.
</fit_check>

<do_it>
## Steps

1. **Read** — project conventions and recent history (you already did this in BOOTSTRAP.md step 2)
2. **Do** — implement the change, match existing patterns
3. **Scope-check, then quality-check** — first verify the actual diff stayed within fit criteria; then run the appropriate quality gate:

   **3a. Scope-check (diff vs. declared fit):**
   ```bash
   git diff --stat
   ```
   Compare actual diff to your declared fit check. If ANY of these now hold, STOP and escalate to `workflows/feature.md`:
   - Diff exceeds ~50 LOC across the change
   - Diff introduces a new file you didn't declare
   - Diff touches a test file, schema/migration file, contract/type file, or a high-stakes path (per BOOTSTRAP.md §3)
   - You found yourself changing behavior or logic mid-implementation, not just strings/config

   Escalation is not a setback — it's the system working. Do NOT commit a Tier-mismatched diff to escape the workflow change.

   **3b. Quality-check (only if 3a passed):** choose gate tier based on what you changed (see `references/quality-gates.md`):
   - Config, docs, comments, formatting → `{lint_command}` only
   - Logic changes → `{lint_command}` + related tests
   - Then **always run full gates before committing:**
     ```bash
     {build_command} && {lint_command} && {test_command}
     ```
4. **Commit:**
   ```bash
   git add <specific-files>
   git commit -m "<type>(<scope>): <description>"
   ```
5. **Log** — append to `.ai/memory.log`
6. **Tell the developer how to verify:**
   ```markdown
   ## How to Verify
   1. [What to check]
   ```
</do_it>

<escalate>
## If It's Not Simple

If the task turns out to be more complex than expected (touching multiple files, unexpected failures, unclear requirements), switch to the full feature workflow:

Read `workflows/feature.md` and start from step 2 (Clarify).
</escalate>
