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

## When Gates Fail

→ See `error-handling.md` for retry budgets (per-error-type limits), recovery strategies, blocker documentation format, and the escalation path when retries are exhausted.

**Key rule:** Do not leave the repo broken. If you can't fix a failing gate, revert the change and document the blocker.
