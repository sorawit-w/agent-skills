# Signal Extraction

The Stage 1a sweep. Read the codebase for **deterministic business signal**. This
is extraction, not judgment — every signal is tagged with the file/path it came
from, and that tag becomes the provenance pointer the inference layer (Phase 2)
requires. No provenance, no claim.

A codebase is a frozen record of business decisions. The job here is to read
business intent from technical artifacts, cheaply and precisely.

---

## Capability lane

- **SocratiCode MCP present** (`mcp__socraticode__codebase_index` /
  `codebase_search` / `codebase_symbols` / `codebase_about`) → index once, then
  query for the source categories below. Best for large / unconventional repos.
- **Absent** → glob/grep fallback over the high-signal files named below. Proven
  sufficient for conventional repos. Record which lane ran (the dossier states it).

**Secret-redaction rule (hard, applies to every extractor):** capture key *names
/ presence* only — never values. `STRIPE_SECRET_KEY=` in `.env.example` is signal
that Stripe is wired; never read or record a real secret value. If one is
encountered, record `<redacted secret present>` and move on.

---

## Universal source taxonomy (descending signal density)

Run these for every repo regardless of ecosystem. The per-ecosystem section maps
each to concrete files.

| # | Source | Business signal it carries |
|---|---|---|
| 1 | **Dependency manifests** | Monetization (payment SDK + *which*), auth, email/CRM, analytics, LLM SDKs, multi-tenancy/SSO. Highest density. |
| 2 | **Data model / schema** | The domain ontology. Entity names *are* the business (`Org/Team/Seat` → B2B; `Listing/Booking/Payout` → marketplace; `Patient/Claim` → regulated health). |
| 3 | **Routes / pages / API surface** | Product surface + ICP. `/admin`, `/billing`, `/team/invite`, public `/api/v1` (→ developer/platform), marketing pages (`/pricing`, `/enterprise`). |
| 4 | **Auth & tenancy** | Single-user vs team vs org → B2C / B2B / B2B2C. |
| 5 | **`.env(.example)`** | First-class extractor — enumerates the entire third-party + region/compliance surface in a few lines. Highest signal-to-effort. |
| 6 | **Money code** | Revenue model precisely: subscription vs usage vs seat vs take-rate; webhooks (`invoice.paid`), metering, plan tiers, `free`/`pro` enums. |
| 7 | **README / docs / marketing copy** | The *claimed* story — to diff against built reality. Parse roadmap markers ("Future", "Coming soon", "Roadmap"). |
| 8 | **Commit recency / contributors** | Team size, velocity, maturity, abandonment (last commit > 12mo → likely dead). |

`.env(.example)` (source 5) is the cheapest high-precision win — read it first.

---

## JS / TS extractors

- **Manifests:** `package.json` (root + every `apps/*` / `packages/*` workspace),
  `bun.lock` / `pnpm-lock.yaml` / `yarn.lock`. Read `dependencies` +
  `devDependencies` + `description` + `workspaces`.
- **Schema:** Drizzle (`*.ts` with `pgTable(` / `sqliteTable(` / `mysqlTable(`),
  Prisma (`schema.prisma` → `model X {`), TypeORM (`@Entity()`), Sequelize models,
  raw SQL migrations.
- **Routes:** SvelteKit (`src/routes/**/+page.svelte`, `+server.ts`), Next
  (`app/**/page.tsx`, `pages/**`), Remix (`app/routes/**`), Express/Elysia/Hono
  route registrations.
- **Money code:** grep `stripe` / `paddle` / `lemonsqueezy`, `invoice` /
  `subscription` / `checkout` / `webhook` / `price` / `plan` / `tier` / `seat` /
  `metering`, plan enums (`'free' | 'pro'`).
- **`.env.example`:** key names → integration map (see decoder below).

## Python extractors

- **Manifests:** `requirements.txt`, `pyproject.toml` (`[project.dependencies]` /
  poetry), `Pipfile`, `setup.py`/`setup.cfg`.
- **Schema:** SQLAlchemy (`class X(Base):` + `__tablename__`), Django models
  (`class X(models.Model)`), Alembic migrations (`versions/`), Pydantic models.
- **Routes:** FastAPI (`@app.get` / `@router.post` / `APIRouter`), Django
  (`urls.py` `urlpatterns`), Flask (`@app.route`).
- **Money code:** grep `stripe` / `braintree`, `Subscription` / `Invoice` /
  `Plan` / `webhook`, Django `PaymentSettings`, usage-metering helpers.
- **`.env` / settings:** `.env.example`, Django `settings.py` third-party keys,
  `os.environ.get(...)` calls.

## Generic fallback (any other stack)

When the ecosystem isn't JS/TS or Python, degrade honestly — yield is lower, and
the dossier says so:

- Any package/dependency manifest present (`go.mod`, `Gemfile`, `composer.json`,
  `Cargo.toml`, `pom.xml`, `*.csproj`) → list declared deps; map the recognizable
  ones (Stripe, auth, analytics, LLM SDKs) via the decoder below.
- Any `.env` / `.env.example` / `config.*` → key-name decoder.
- `README` / `docs/` → claimed story.
- `Dockerfile` / `docker-compose.yml` / IaC (`*.tf`, `k8s/`) → infra → Cost
  Structure + scale intent.
- Schema: any `migrations/` dir or `*.sql` → entity names.

Mark generic-fallback signals at most `inferred` confidence unless the signal is
unambiguous (e.g. a literal `STRIPE_SECRET_KEY` → Stripe is `observed`).

---

## `.env` key-name decoder (high-precision, ecosystem-agnostic)

| Key pattern | Signal |
|---|---|
| `STRIPE_*`, `PADDLE_*`, `LEMONSQUEEZY_*` | Monetized. `STRIPE_PRICE_ID` (singular) → likely one flat price; multiple price IDs / `STRIPE_*_PRICE` → tiered. |
| `CLERK_*`, `AUTH0_*`, `NEXTAUTH_*`, `COGNITO_*`, `SUPABASE_*`(auth) | Has accounts (not anonymous). Dual keys (`CLERK_ADMIN_*`) → admin surface. |
| `WORKOS_*`, `SAML_*`, `SCIM_*`, `OKTA_*` | Enterprise B2B (SSO/SCIM). |
| `SENDGRID_*`, `RESEND_*`, `POSTMARK_*`, `CUSTOMERIO_*`, `LOOPS_*` | Lifecycle / transactional email → retention motion. |
| `SEGMENT_*`, `POSTHOG_*`, `AMPLITUDE_*`, `MIXPANEL_*`, `GA_*` | Product analytics → Key Metrics signal; what they track reveals the north-star. |
| `OPENAI_*`, `ANTHROPIC_*`, `OPENROUTER_*`, `REPLICATE_*`, `HUGGINGFACE_*` | **AI feature** → set the AI-feature flag (routes to `ai-ux-review` / `ai-eval-review`). |
| `NEON_*`, `DATABASE_URL`, `PLANETSCALE_*`, `MONGODB_*` | Datastore → Cost Structure. |
| `R2_*`, `S3_*`, `CLOUDINARY_*`, `UPLOADTHING_*` | Object storage → user uploads / media product. |
| `SENTRY_*`, `DATADOG_*` | Ops maturity. |
| `*_REGION`, `GDPR_*`, `HIPAA_*`, locale/i18n keys | `is_international` / `is_regulated` signals. |

---

## Output of this phase

A structured **signal set** (held internally for Phase 2), where each signal is:

```
{ source: "<file:path or symbol>", signal: "<what was found>", category: "<taxonomy #>" }
```

Example (from a real dry-run): `{ source: "apps/api/src/db/schema/index.ts:122",
signal: "users.stripeCustomerId + subscriptionId + subscriptionPeriodEnd",
category: "money code" }` → feeds `Revenue Streams = observed` in Phase 2.

The `source` field is non-negotiable — it is the provenance pointer the inference
layer needs to render any claim.
