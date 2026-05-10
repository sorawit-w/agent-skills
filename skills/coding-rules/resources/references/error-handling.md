# Error Handling & Recovery

Use this reference when encountering build failures, test failures, dependencies issues, or blockers.

> **Note:** Examples below use `bun` commands. Adapt to your project's toolchain (`npm`, `yarn`, `pnpm`, `deno`, etc.). The patterns apply regardless of the package manager.

---

## Retry Budgets

Each error type has a maximum retry count and recovery strategy:

| Error Type | Max Attempts | Primary Strategy |
|------------|--------------|------------------|
| **Build failures** | 5 | Check logs, fix imports, reinstall deps, verify syntax |
| **Test failures** | 3 | Read output, fix logic, add logging, skip flaky tests |
| **Lint errors** | 5 | Auto-fix first, then adjust code or update config |
| **Dependency issues** | 5 | Clear cache, reinstall, check versions, try --force |
| **Schema validation** | 1 | Validate input — deterministic, either valid or not |

---

## Build Failures (5 attempts)

### Attempt 1-2: Check and Fix

1. Run build with verbose output:
   ```bash
   bun run build --verbose
   ```
2. Scan logs for obvious issues:
   - Missing imports or typos
   - Syntax errors in generated code
   - Circular dependencies
3. Fix the identified issue
4. Re-run build

### Attempt 3-4: Dependency and Cache Cleanup

1. Clear cache:
   ```bash
   bun pm cache rm
   ```
2. Reinstall dependencies:
   ```bash
   bun install --force
   ```
3. Re-run build

### Attempt 5: Deep Inspection

1. Check for platform-specific issues (native modules, OS-specific paths)
2. Verify generated code syntax (if code generation involved)
3. Check for circular dependencies manually
4. If still failing: mark BLOCKED, document in `.ai/BLOCKERS.md`

---

## Test Failures (3 attempts)

### Attempt 1: Understand the Failure

1. Run the test suite with verbose output:
   ```bash
   bun run test --verbose
   ```
2. Read the full test output carefully
3. Identify root cause: logic error, assertion, flakiness, or environment issue

### Attempt 2: Fix or Skip

If root cause is clear:
- **Logic error:** Fix the code
- **Wrong assertion:** Correct the test
- **Flaky test:** Add retry logic or skip with comment:
  ```typescript
  test.skip("flaky test — TODO: fix race condition");
  ```
- **Environment issue:** Check env vars, setup, teardown

### Attempt 3: Add Logging and Retest

If root cause is unclear:
1. Add detailed logging around the failing assertion
2. Run test again
3. If still failing after 3 attempts: mark BLOCKED, document in `.ai/BLOCKERS.md`

---

## Lint Errors (5 attempts)

### Attempt 1: Auto-Fix

```bash
bun run lint --fix
```

Many lint errors resolve automatically. Check the diff and commit.

### Attempt 2-3: Manual Fixes

If auto-fix doesn't resolve:
1. Read the linter error message
2. Adjust code to meet the rule
3. Re-run lint

### Attempt 4-5: Config or Disable

If a rule is too strict for your use case:
1. Disable rule with inline comment:
   ```typescript
   // biome-ignore lint/rule-name: <reason>
   const someCode = ...;
   ```
2. Document the exception in `.ai/memory.log`
3. If multiple files affected: update `biome.json` config instead

---

## Dependency Issues (5 attempts)

### Attempt 1-2: Clear and Reinstall

1. Clear package manager cache:
   ```bash
   bun pm cache rm
   ```
2. Remove lock file and node_modules:
   ```bash
   rm -rf bun.lockb node_modules
   bun install
   ```
3. Try again

### Attempt 3: Force Install

```bash
bun install --force
```

### Attempt 4: Check Versions

1. Review `.tool-versions` or `package.json` engines
2. Verify that all declared versions are compatible
3. Check if newer versions of problematic dependencies exist
4. Update if appropriate, re-run install

### Attempt 5: Platform-Specific Issues

1. Check if error is platform-specific (native modules, Windows vs Unix paths)
2. Look for known issues in dependency's GitHub repo
3. If unable to resolve: mark BLOCKED, document in `.ai/BLOCKERS.md`

---

## Schema Validation (1 attempt)

Schema validation is deterministic — either the input is valid or it isn't. No retry strategy.

If validation fails:
1. Verify the input matches the schema exactly
2. Check data types, required fields, format
3. If input is invalid: fix the data
4. If schema is wrong: update the schema definition
5. Re-validate

---

## When Retries Are Exhausted

### Document the Blocker

Create `.ai/BLOCKERS.md` with this format:

```markdown
## [blocker-id]: [short description]

**Severity**: Critical | High | Medium

**Category**: Build | Test | Dependencies | Auth | Other

**Description**: [Detailed explanation of what failed and why it matters]

**Error message**:
[Full error output, last 50 lines]

**Attempted solutions**:
- Attempt 1: [what was tried and result]
- Attempt 2: [what was tried and result]
- Attempt N: [what was tried and result]

**Suggested resolution**: [What a human needs to do to unblock]

**Affected tasks**: [List task IDs that depend on this]

**When it happened**: [ISO 8601 timestamp]
```

### Update STATUS.md

Add to `.ai/STATUS.md` under the Blockers section:

```
## Blockers

- [blocker-id]: [description] (severity: [level])
```

### Log in memory.log

Use the canonical format from `communication.md`:

```
[YYYY-MM-DDTHH:MM:SSZ]
Task: [task-id or description]
Action: Exhausted retry budget for [error type]
Files: [affected files]
Status: BLOCKED
Notes: Blocker=[blocker-id], Attempts=[N], Next=[awaiting human review / needs external action]
```

### Move On

- Skip the blocked task
- Look for other READY tasks (no unmet dependencies)
- Continue work on unblocked items
- Escalate blocker to human reviewer if task is critical

---

## Never Leave the Repo Broken

Before stopping work, ensure the main branch is in a buildable state.

### If Task Cannot Be Completed

1. Identify what changed that broke the build
2. Revert with:
   ```bash
   git revert HEAD
   ```
3. Or reset if not yet pushed:
   ```bash
   git reset --hard HEAD~1
   ```
4. Verify build passes:
   ```bash
   bun run build && bun run lint && bun run test
   ```
5. Document the failed attempt in `.ai/memory.log`

### If Task is Partially Complete

1. Commit what works
2. Create a separate branch for incomplete work (using standard branch convention):
   ```bash
   git checkout -b wip/[task-id]-incomplete
   git push -u origin wip/[task-id]-incomplete
   ```
3. Leave `main` clean and building
4. Document next steps in `.ai/memory.log`

---

## Error Triage Decision Tree

```
Error occurs
  ↓
Read error message carefully
  ↓
Match to error type (build|test|lint|dependency|schema)
  ↓
Run recovery strategy for that type
  ↓
Does it pass?
  ├─ YES → Commit and continue
  ├─ NO → Have retries remaining?
  │         ├─ YES → Increment attempt, retry strategy
  │         └─ NO → Exhausted, document blocker
  └─ UNCERTAIN → Add logging, run again
```
