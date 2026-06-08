# Signal Extraction — the feature/action inventory

Phase 1's sweep. Read the resource set for the **user-facing actions** the product
affords — these are the subjects the fit-test judges. This is extraction, not
judgment: every action is tagged with the source it came from, and that tag becomes
the provenance pointer the fit-test requires. **No provenance, no candidate.**

A codebase is a frozen record of what users can *do*; docs and URLs state what the
product *claims* they do; analytics state what they *actually* do. The job is to
read the action surface from all three, cheaply and precisely, and tag each action
with whether it is **repeatable** and whether the data behind it is **captured** —
the two properties the fit-test leans on hardest.

---

## Capability lane (code)

- **SocratiCode MCP present** (`mcp__socraticode__codebase_index` /
  `codebase_search` / `codebase_symbols`) → index once, then query for the source
  categories below. Best for large / unconventional repos.
- **Absent** → glob/grep fallback over the high-signal files named below. Record
  which lane ran (the report states it).

**Secret- & PII-redaction rule (hard, applies to every extractor):** capture key
*names / presence* and *aggregate counts* only — never values, never user-level
rows. `STRIPE_SECRET_KEY=` is signal that Stripe is wired; never read its value. An
analytics export's `login` event with a count is signal; an individual user's row
is not. Encounter a secret → record `<redacted secret present>` and move on.

---

## What an "action" is

A candidate is a **repeatable, user-initiated action tied to a goal** — not a
screen, not an entity. `POST /entries` (log a habit), "complete a lesson", "invite
a teammate", "submit an expense report" are actions. `users` table, `/settings`
page, a config flag are *not* actions. The fit-test needs verbs, not nouns.

For each action capture:

```
{ source: "<file:path | url | export-name>",
  action: "<the user-facing verb>",
  category: "<taxonomy # below>",
  repeatable: <observed | inferred | unknown>,   // is it done repeatedly?
  data_captured: <yes | no | unknown> }           // is the event/state stored?
```

`repeatable` is `observed` only when an analytics export shows recurrence, or the
schema makes it structural (a `streak`/`logged_at` column, a join table of repeated
events). Otherwise `inferred` (the action *looks* repeatable) or `unknown`. **Never
upgrade `inferred` to `observed` without an export.**

---

## Source taxonomy (descending signal density)

| # | Source | What it reveals |
|---|---|---|
| 1 | **Routes / handlers / pages** | The action surface. Mutating routes (`POST`/`PUT`/`PATCH`), form actions, RPC/mutations, event handlers = the verbs users perform. |
| 2 | **Data model / schema** | Which actions are *repeated and stored* — the strongest repeatability signal. `logged_at`, `streak`, `completed_count`, a join table of events → structural repeatability. |
| 3 | **Analytics exports** (if provided) | The only source that *grounds* repeat-usage. Event names + counts + per-user frequency distributions → `repeatable: observed`. PII-redacted: counts and event names only. |
| 4 | **Docs / README / PDFs** | The *claimed* feature set + the stated goal/roadmap. Parse for the intended user behavior ("users build a daily habit", "teams collaborate on…"). |
| 5 | **Live URL** (if provided) | Marketing + onboarding copy → the behavior the product *wants* (the goal), and the headline actions it surfaces. |
| 6 | **Domain events / queues / webhooks** | Background reactions to actions — sometimes the action worth reinforcing is the event, not the click. |

---

## Code extractors

**JS / TS**
- **Routes / actions:** SvelteKit (`+page.server.ts` actions, `+server.ts`), Next
  (`app/**/route.ts`, server actions, `app/**/page.tsx` forms), Remix
  (`app/routes/**` `action`/`loader`), Express/Elysia/Hono route registrations.
  Grep mutating verbs: `\.post(`, `\.put(`, `\.patch(`, `action:`, `mutation`.
- **Schema (repeatability):** Drizzle (`pgTable(`/`sqliteTable(`), Prisma
  (`model X {`), TypeORM (`@Entity()`). Grep recurrence columns: `streak`,
  `logged_at`, `completed_at`, `count`, `last_seen`, `_at` timestamps, join tables.
- **Events:** queue/job definitions, `emit(`, webhook handlers.

**Python**
- **Routes / actions:** FastAPI (`@app.post`/`@router.*`), Django (`urls.py` +
  views with `POST`), Flask (`@app.route(..., methods=["POST"])`).
- **Schema:** SQLAlchemy (`class X(Base)` + recurrence columns), Django models,
  Alembic migrations.

**Generic fallback (any other stack)** — degrade honestly; yield is lower and the
report says so. Any route/controller layer → list mutating endpoints; any
`migrations/` or `*.sql` → entity + recurrence columns. Mark generic-fallback
actions at most `repeatable: inferred` unless a schema column is unambiguous.

---

## Docs / PDF / URL extractors

- **README / docs / PDFs:** extract the *stated goal* (feeds the Phase 2 cascade)
  and the *claimed* action list. Parse roadmap markers ("Coming soon", "Future").
  A claimed action with no code behind it is `data_captured: no` — a fit-test SKIP
  unless the user plans to build it.
- **Live URL:** read onboarding + marketing copy for the target behavior and the
  hero actions. Treat as *claimed*, not *built* — diff against the code surface.

---

## Analytics extractors (when an export is provided)

Read PostHog/GA/Amplitude/Mixpanel exports (CSV/JSON) for **event names, total
counts, and per-event frequency** (how many users do it how often). These promote
an action's `repeatable` tag to `observed` and feed the report's confidence tier.

**Hard:** aggregate only. Never read, join, or echo a `distinct_id`, email, IP, or
any user-level row. If the export is row-level, aggregate it in-memory to
event-count form and treat the rows as `<redacted PII>`.

---

## Output of this phase

A provenance-pinned **inventory** (held internally for the fit-test). Triage by
goal-relevance × repeatability and carry the **top candidates** (aim ≤ ~12) — state
how many were found vs. carried. The `source` field is non-negotiable: it is the
provenance pointer every downstream recommendation must cite.

Example: `{ source: "src/routes/entries/+page.server.ts:14 + schema entries.logged_at",
action: "log a daily journal entry", category: "1+2", repeatable: "inferred",
data_captured: "yes" }` → a strong fit candidate (repeatable + captured); upgrades
to `repeatable: observed` if an analytics export shows recurring `entry_logged`.
