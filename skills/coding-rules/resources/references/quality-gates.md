# Quality Gates & Error Recovery

Non-negotiable checks and retry strategies for when things go wrong.

---

## Quality Gates

**Non-negotiable — but scaled to the change.**

Not every change needs the full gate. Match verification effort to the risk of the change:

### Gate Tiers

| Tier | When to Use | What Runs |
|------|------------|-----------|
| **Quick** | Single-file edits, config, docs, comments, formatting | `{lint_command}` only |
| **Standard** | Multi-file changes, logic changes, new functions | `{build_command} && {lint_command} && {test_command}` |
| **Full** | Cross-cutting changes, dependency updates, public API changes | Standard + E2E (if applicable) + manual spot-check |

### Choosing the Right Tier

```
Is it config-only, docs, or formatting?  → Quick
Does it change logic or touch 2+ files?  → Standard
Does it cross module boundaries or change dependencies?  → Full
```

**When in doubt, use Standard.** Quick is an optimization for obviously low-risk changes — if there's any chance the change affects behavior, run Standard.

### At Commit Time

Regardless of which tier you used during development, **always run Standard gates before committing.** A Quick-tier check during iteration is fine, but no commit goes out without build+lint+test passing.

Run the project's existing test suite **before AND after** your changes. Don't assume your changes are isolated.

---

## Formatter Scope

**Never run repo-wide formatters or auto-fixers.** Format and auto-fix only files you touched this turn.

The failure mode this prevents: running `prettier --write .`, `eslint --fix .`, `biome check --apply .`, or `black .` reformats files unrelated to your change, balloons the diff, hides the actual edit, and can revert formatting a teammate's IDE or pre-commit hook applied for valid reasons. The diff stops being reviewable.

**Detection — defer to pre-commit infrastructure if present:**

If the project uses `lint-staged` + `husky` (or any equivalent that auto-formats staged files), do nothing manually. The hook handles touched-files-only formatting at commit time. Detect via:

- `package.json` has a `lint-staged` key
- `.husky/pre-commit` exists
- `.pre-commit-config.yaml` exists (Python projects)
- `.lefthook.yml` / `lefthook.yml` exists

Running formatters manually duplicates that hook's work and may conflict with its config.

**If no pre-commit infrastructure is present, format touched files only:**

```bash
# Compute touched files once
TOUCHED=$(git diff --name-only HEAD --diff-filter=ACMR)

# Prettier (JS/TS/JSON/MD/CSS/YAML)
echo "$TOUCHED" | grep -E '\.(ts|tsx|js|jsx|json|md|css|scss|yml|yaml)$' | xargs -r prettier --write

# ESLint --fix (JS/TS)
echo "$TOUCHED" | grep -E '\.(ts|tsx|js|jsx)$' | xargs -r eslint --fix

# Biome (JS/TS, integrated linter + formatter — pass file paths, NOT `.`)
echo "$TOUCHED" | xargs -r biome check --apply

# Black (Python)
echo "$TOUCHED" | grep '\.py$' | xargs -r black

# gofmt (Go)
echo "$TOUCHED" | grep '\.go$' | xargs -r gofmt -w

# rustfmt (Rust)
echo "$TOUCHED" | grep '\.rs$' | xargs -r rustfmt
```

The `xargs -r` (or `xargs --no-run-if-empty`) is important — if `TOUCHED` is empty for a given extension, the formatter will not be invoked with zero args, which on most formatters means "format the whole repo" (the failure mode we're avoiding).

**Forbidden invocations:**

```bash
prettier --write .         # NO
prettier --write **/*      # NO
eslint --fix .             # NO
biome check --apply .      # NO
black .                    # NO
gofmt -w .                 # NO
rustfmt --recursive .      # NO
```

**Exception — explicit normalization passes.** If the user asks for "format the whole repo" / "normalize formatting" / "apply the new formatter config," repo-wide IS the correct scope. Announce the scope before running it: `Running prettier --write . across the full repo per request — diff will be large.` so the developer sees the intent and isn't surprised by a 200-file diff.

---

## When Gates Fail

→ See `error-handling.md` for retry budgets (per-error-type limits), recovery strategies, blocker documentation format, and the escalation path when retries are exhausted.

**Key rule:** Do not leave the repo broken. If you can't fix a failing gate, revert the change and document the blocker.
