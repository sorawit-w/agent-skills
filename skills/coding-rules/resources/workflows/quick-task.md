# Quick Task Workflow

For simple tasks — single-file edits, config changes, documentation updates, or fixes with obvious root cause (complexity 1–3).

**Branching:** quick-task stays in-place. Use a normal `git checkout -b` — worktree overhead is not justified for changes this small. Worktree default applies only to `workflows/feature.md` and `workflows/bugfix.md`. (If the task turns out to be more complex than expected, escalate to feature.md and create a worktree at that point.)

<do_it>
## Steps

1. **Read** — project conventions and recent history (you already did this in BOOTSTRAP.md step 2)
2. **Do** — implement the change, match existing patterns
3. **Check** — choose gate tier based on what you changed (see `references/quality-gates.md`):
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
