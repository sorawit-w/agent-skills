# Knowledge Base

A curated, project-level knowledge base that gives AI agents the context they need to make better decisions. Unlike `memory.log` (append-only session logs) or `STATUS.md` (ephemeral state), the knowledge base is **edited, organized, and maintained** — more like a wiki than a log.

> **Glossary lives elsewhere.** Domain vocabulary — names of concepts used repeatedly across the project — belongs in `CONTEXT.md` at project root, not here. See `references/domain-glossary.md`. The knowledge base captures decisions, conventions, lessons, and references; it isn't a thesaurus.

---

## What Goes in the Knowledge Base

| Type | Examples | Why It Matters |
|------|----------|---------------|
| `decision` | "Why we chose Postgres over DynamoDB", "Why we use event sourcing for billing" | Prevents agents from re-litigating settled decisions or making contradictory choices |
| `context` | "Billing module handles EU VAT edge cases", "The legacy auth middleware is being replaced in Q3" | Gives agents domain and project background they can't infer from code alone |
| `convention` | "We use kebab-case for API endpoints", "All dates are stored as UTC, displayed in user's timezone" | Prevents agents from introducing inconsistencies |
| `reference` | "Production database credentials are in 1Password vault 'Engineering'", "CI/CD pipeline docs are at [URL]" | Points agents to external resources without duplicating content |
| `lesson` | "We discovered that batch inserts over 10k rows cause timeouts on our Neon tier", "The Stripe webhook retry window is 72 hours — design idempotency around that" | Captures hard-won operational knowledge that saves future debugging time |

**What does NOT belong here:**
- Session logs → `memory.log`
- Current progress/state → `STATUS.md`
- User preferences and working style → auto-memory (`MEMORY.md`)
- Code patterns discoverable by reading the codebase
- Git history or who-changed-what → `git log` / `git blame`

---

## Directory Structure

```
.ai/knowledge/
├── KNOWLEDGE.md              ← Index file (agents read this first)
├── architecture-postgres.md
├── convention-api-naming.md
├── context-billing-eu-vat.md
├── decision-event-sourcing.md
├── lesson-batch-insert-limit.md
└── ...
```

### File Naming

```
<type>-<short-description>.md
```

Types: `decision`, `context`, `convention`, `reference`, `lesson`
Description: kebab-case, 2-5 words

---

## Entry Schema

Every knowledge entry is a markdown file with YAML frontmatter:

```markdown
---
title: Why we chose Postgres over DynamoDB
type: decision
domain: [database, infrastructure]
related: [context-billing-eu-vat.md, convention-api-naming.md]
confidence: high
created: 2025-11-15
updated: 2026-01-20
---

## Context

We needed a primary database for the billing and user management modules.
The main candidates were Postgres (via Neon) and DynamoDB.

## Decision

Postgres via Neon, with connection pooling through their serverless driver.

## Rationale

- Billing requires complex joins across invoices, line items, tax rules, and subscriptions.
  DynamoDB's single-table design would make these queries awkward and expensive.
- The team has deep Postgres expertise. DynamoDB would require retraining.
- Neon's branching feature lets us create database branches for preview deployments.

## Trade-offs

- We lose DynamoDB's automatic scaling for write-heavy workloads.
  Mitigated by Neon's autoscaling and our current traffic level.
- We take on connection pooling complexity.
  Mitigated by Neon's built-in pooler.

## Revisit When

- Write volume exceeds 10k ops/sec sustained
- We need global multi-region with single-digit-ms latency
```

### Frontmatter Fields

| Field | Required | Description |
|-------|----------|-------------|
| `title` | Yes | Human-readable title. Be specific — "Why we chose X" is better than "Database decision" |
| `type` | Yes | One of: `decision`, `context`, `convention`, `reference`, `lesson` |
| `domain` | Yes | List of topic tags. Free-form but keep consistent within the project |
| `related` | No | List of other knowledge files this entry connects to (filename only, not path) |
| `confidence` | Yes | `high` (human-verified), `medium` (agent-drafted, seems right), `low` (agent-drafted, unverified) |
| `created` | Yes | ISO date when the entry was first written |
| `updated` | No | ISO date of last meaningful update |

---

## KNOWLEDGE.md Index

The index is the agent's entry point. It lists all knowledge entries with a one-line summary so the agent can decide which to read without loading them all.

```markdown
# Knowledge Base Index

Project knowledge — architecture decisions, domain context, conventions, and lessons learned.
Read this index to find relevant context before planning or implementing.

## Entries

- [Why we chose Postgres over DynamoDB](knowledge/architecture-postgres.md) — billing needs complex joins; team has Postgres expertise
- [EU VAT handling in billing](knowledge/context-billing-eu-vat.md) — reverse charge, MOSS, and threshold rules
- [API naming conventions](knowledge/convention-api-naming.md) — kebab-case endpoints, camelCase bodies, plural resource names
- [Batch insert limit on Neon](knowledge/lesson-batch-insert-limit.md) — keep under 10k rows per transaction
```

**Rules:**
- One line per entry, under 120 characters
- Format: `- [Title](path) — one-line hook`
- Keep alphabetical within each type, or group by domain — pick one and be consistent
- Lines after 100 will be truncated by agents, so keep the index lean

---

## When to Create Knowledge Entries

### Agents Should Propose Entries When:

1. **An architecture or technology decision is made** — capture the rationale before it's forgotten
2. **A non-obvious convention is established** — if the agent had to ask or guess, future agents will too
3. **A debugging session reveals operational knowledge** — "this timeout happens because X" is a lesson worth recording
4. **Domain-specific context comes up** — if the user explains how their industry works, capture it
5. **A "why" question gets answered** — if someone explains why code is structured a certain way, that's a decision entry

### Agents Should NOT Create Entries For:

- Things obvious from reading the code
- Temporary state or in-progress work (use STATUS.md)
- Session-level notes (use memory.log)
- User preferences (use auto-memory)

### The Proposal Workflow

1. Agent identifies knowledge worth capturing
2. Agent drafts the entry with `confidence: medium` or `confidence: low`
3. Agent tells the user: "I've drafted a knowledge entry about [topic]. Want me to add it to the knowledge base?"
4. If approved, agent writes the entry file and runs `bash "${CODING_RULES_DIR}/resources/hooks/knowledge-reindex.sh" --force` to refresh the AUTO-INDEX block in `KNOWLEDGE.md`. (If the hook isn't available — e.g., on a platform without `coding-rules` wired — the agent updates `KNOWLEDGE.md` by hand, adding one line in the format `- [Title](filename.md) — one-line summary` between the AUTO-INDEX markers.)
5. Human can later promote `confidence` to `high` after review

**Never write knowledge entries silently.** Always tell the user what you're proposing and why.

---

## When to Query the Knowledge Base

Agents should check the knowledge base at these points:

1. **Session start (Step 1: ASSESS)** — read `KNOWLEDGE.md` index to understand project context
2. **Before planning (Step 3: PLAN)** — search for relevant decisions, conventions, and lessons before designing an approach
3. **When encountering a "why" question** — before asking the user, check if the answer is already documented
4. **Before making architecture decisions** — check for existing decisions in the same domain

### Retrieval Strategy

For most projects (under ~100 entries):
1. Read `KNOWLEDGE.md` index
2. Identify entries relevant to the current task by title and summary
3. Read the full content of relevant entries (typically 2-5)
4. Follow `related` links if the entries reference other useful context

The LLM reading the index IS the semantic search engine. No embeddings or vector DB required.

---

## Maintenance

### Staleness

Knowledge entries can become outdated. Agents should treat entries with appropriate skepticism:

- Check `updated` date — entries older than 6 months may be stale
- If an entry conflicts with current code, **trust the code** and flag the entry for update
- Entries with `confidence: low` should be verified before acting on them

### Retiring Entries

When a decision is reversed or a convention changes:
1. Update the entry (don't delete it — the history is valuable)
2. Add a section: `## Superseded` with what replaced it and why
3. Update `KNOWLEDGE.md` index to reflect the change

### Keeping the Index Clean

- Remove entries that are no longer relevant
- Merge entries that overlap significantly
- Split entries that cover too many topics
- Aim for entries that are 50-200 lines each — long enough to be useful, short enough to read quickly

### Keeping the Root Context File Lean

The knowledge base relies on the root context file (`CLAUDE.md` / `AGENTS.md` / `AI-CONTEXT.md` — whichever this project uses) staying an **index and pointer**, not a dumping ground. Durable content belongs in `.ai/knowledge/`; current state in `STATUS.md`; session history in `memory.log`. The root file should mostly *point* at those.

It still drifts upward over time — dated "Session Notes" sections, completed-work blurbs, and one-off decisions accrete. Unlike the index (≤100 lines) and entries (50–200 lines), nothing here caps the root file, so it silently inflates the input-token cost of **every** session.

- **Set a soft cap** (~250–300 lines is a sane default) and check it during maintenance passes. Line count is a fair proxy for recurring input tokens.
- **When over the cap, archive — don't delete.** Move dated/completed sections (e.g., "Session Notes (DATE)" older than ~7 days, "Completed" blocks) to a sibling archive file (`CLAUDE-Archive.md` or `.ai/knowledge/`), leaving a one-line pointer behind.
- **Never archive load-bearing sections** — project approach/philosophy, structure, key references, and active conventions stay in the root file permanently.

This is agent-checkable: count the lines, flag when over, propose the archive move (never silently). It complements the index/entry size disciplines above rather than duplicating them — different file, different failure mode.

Source: cap-and-archive pattern distilled from `EliaAlberti/cpr-compress-preserve-resume` (2026-06-07, MIT) `/preserve` command — its 280-line CLAUDE.md cap + `CLAUDE-Archive.md` move is the one idea in that repo not already covered by coding-rules' `.ai/` state-preservation machinery.

### Built-in automation: bootstrap + index regeneration

One hook ships with `coding-rules` to remove the most-forgotten chores:

- **`knowledge-bootstrap`** (SessionStart) — creates `.ai/knowledge/KNOWLEDGE.md` from the template on first use, regenerates the AUTO-INDEX block in `KNOWLEDGE.md` from current entry files, and flags entries older than 180 days so agents treat them with appropriate skepticism. No per-project setup beyond wiring SessionStart in your agent's settings.

A second script, **`knowledge-reindex`**, is what `knowledge-bootstrap` calls internally for the index regeneration. It can also be called directly:
- By the agent, with `--force`, immediately after writing a new entry mid-session (so the index reflects the change without waiting for the next session).
- As an optional git post-commit hook (without `--force`), if you want index updates to land in the same commit as entry changes.

Default-on. Opt out per project with `agent-context.yaml: knowledge.enabled: false`. See `references/hooks.md` for wiring details.

The proposal workflow above still applies — the hook handles scaffolding and indexing, not entry creation. Agents must still propose entries to you before writing them.

### Optional: Heavier automated compilation

If you outgrow the built-in reindexing — for example, you want cross-link validation, contradiction sweeps, or embedding-based search — the `.ai/knowledge/` directory can be compiled by [OpenKB](external-resources.md) (see Knowledge Base Tools). OpenKB is opt-in; the doctrine here works the same whether it's installed or not.
