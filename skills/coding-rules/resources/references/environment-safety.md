# Environment Safety — Prod vs Non-Prod Behavior

What must *behave differently* across environments, and the rule that governs crossing between them. This is the long-tail matrix; the always-on reflex lives in `BOOTSTRAP.md` § Environment Safety.

---

## The core rule

```
Non-prod must never produce prod-visible side effects.
A non-prod task must never run prod-affecting operations without explicit confirmation.
```

The danger is **direction of leak**, not "wrong setting":

- **Non-prod → prod** is the expensive direction (test data hitting real customers, a dev job mutating prod state). Often irreversible.
- **Prod running with non-prod safeguards** (live traffic in test mode) is usually reversible but still costs money/trust.

Treat any env-crossing action as a **human-validation zone** regardless of reversibility (`references/safety-mindset.md` § cost-of-error).

---

## Detect the active environment first

Before applying the matrix, establish where you are. In order of authority:

1. **Explicit env var** — `NODE_ENV`, `APP_ENV`, `RAILS_ENV`, `DJANGO_SETTINGS_MODULE`, `ENVIRONMENT`, framework equivalent.
2. **Config** — env-specific config files (`config/production.*`, `.env.production`), `agent-context.yaml`.
3. **Infer from host/target** — domain, DB host, deploy target. Lowest confidence; confirm before acting on it.

If the environment is ambiguous, **assume the more dangerous interpretation** (treat as prod-adjacent) and confirm.

---

## The matrix

Each row is a real incident class, not a hypothetical (reactive corollary — rules trace to failures).

| Concern | Non-prod must… | Incident it prevents |
|---|---|---|
| **Crawlers / SEO** | Serve `X-Robots-Tag: noindex` + `robots.txt` disallow on every non-prod web surface | Staging site indexed by Google, outranking prod / leaking unreleased pages |
| **Email / SMS / push** | Route to a sandbox, mail-catcher, or hard allowlist | Test campaign blasted to real customers |
| **Payments** | Use test mode / test keys only | Live charge (or refund) triggered from QA |
| **Analytics / tracking / pixels** | Disable or route to a separate property | Dev/CI traffic pollutes prod metrics and ad audiences |
| **Third-party APIs & webhooks** | Point at sandbox endpoints; never a partner's prod URL | Non-prod call mutates a partner's production system |
| **Background jobs / crons** | Disable destructive or outbound-effecting jobs | A cleanup cron runs against prod-shaped data |
| **Data** | Use seed/synthetic data; never a raw prod dump with real PII | PII exposed in a low-trust environment |
| **Rate limits / retry budgets** | Use env-appropriate values | A non-prod load test exhausts a shared third-party quota |
| **Feature flags** | Default risky flags off; promote per environment | Unfinished feature visible to real users |

Not exhaustive — when a new outbound or stateful integration appears, ask "what does this do if it fires from non-prod?" and add the safeguard.

---

## Where the mechanics live

- **What to externalize** (which values become env-driven): `references/validation.md` § hardcoded-value triggers.
- **Secrets boundary** (`.env` only, never app config): `references/guardrails.md` § Configuration vs. Secrets.
- **Feature-flag pattern** (typed, env-driven, default-off): `references/working-patterns.md`.
- **Cost-of-error / reversibility framing**: `references/safety-mindset.md`.
