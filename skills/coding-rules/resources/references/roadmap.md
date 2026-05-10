# Roadmap — Living Feature Inventory

A curated, project-level inventory of features and major changes — what's planned, in progress, blocked, and shipped. Lives at the project root as `ROADMAP.md` so humans see it first; agents read it natively without an MCP integration.

> **Sibling to `references/knowledge-management.md`.** The knowledge base captures *why* (decisions, conventions, lessons). The roadmap captures *what's next* and *what shipped*. Two files, two jobs.

This doctrine targets **solo and small-team projects with AI agents in the loop.** Multi-stakeholder external roadmaps usually live in Jira, Linear, Asana, or similar — those tools win for that use case. `ROADMAP.md` exists because agents can read markdown in-repo natively, and because solo work needs a single source of truth that survives across sessions without external dependencies.

---

## File Location

`ROADMAP.md` at project root — not `.ai/`. Humans need it more visible than agents do.

---

## Shape

A flat list at the top with status legends, plus a `## Shipped` archive section. That's it.

```markdown
# Roadmap

> Status: `[ ]` todo • `[~]` in progress • `[x]` done • `[!]` blocked

- [~] User auth (Clerk integration)
- [!] Tax calculation (blocked: legal review)
- [ ] Billing module — Stripe integration
- [ ] Invoice PDF generation
- [ ] Multi-tenant support

## Shipped

- [x] CI/CD pipeline — 2026-04-20
- [x] Initial project setup — 2026-04-15
```

### Status legends

| Legend | Meaning |
|--------|---------|
| `[ ]` | Todo |
| `[~]` | In progress |
| `[x]` | Done |
| `[!]` | Blocked — always include a one-line reason |

> **GFM caveat.** GitHub renders `[ ]` and `[x]` as visual checkboxes. `[~]` and `[!]` render as plain text in most viewers. They're agent-parseable and human-readable, but won't show as visual indicators in rendered Markdown. The convention is local — that's fine.

### Ordering = priority

Top of list = sooner, bottom = later. **No `## Now` / `## Next` / `## Later` headers.** The legends and ordering already carry that signal — adding sections would duplicate information and create drift.

`## Shipped` is the only horizon-style section and it earns its keep as an archive: without it, completed items pile up and drown the active list after a few months.

### Optional: group by feature area

When a project has clear modules, group active items under sub-headings (`### Auth`, `### Billing`, etc.). This is more useful than horizon for navigation and emerges naturally from the codebase structure. Optional — flat works for small projects.

### Sub-features

Nest sub-bullets where features have meaningful sub-work:

```markdown
- [~] Billing module
  - [x] Stripe integration
  - [ ] Invoice PDF generation
  - [!] Tax calculation (blocked: legal review)
```

The parent's status reflects the rollup: any sub-item `[~]` makes the parent `[~]`, any `[!]` surfaces the block, all sub-items `[x]` flips the parent.

---

## What Goes In (and What Doesn't)

`ROADMAP.md` is for **features and major changes** — not every commit.

| Goes in | Stays in `.ai/memory.log` / git history |
|---------|------------------------------------------|
| New features (auth, billing, dashboard) | Bug fixes |
| Major refactors that change capability | Chores (dep bumps, formatting) |
| Architectural changes users will notice | Minor refactors |
| Externally visible behavior changes | Internal-only cleanups |

**Rule of thumb:** items rated complexity ≥ 4 (per the 1–10 scale in `workflows/feature.md`) belong in `ROADMAP.md`. Below that stays in commit history. If unsure, ask: *would a future contributor want to know we did this?*

---

## Item Format

Minimum: `- [x] User auth`

Recommended: `- [x] User auth (Clerk) — shipped 2026-04-15, [PR #42](url)`

For blocked items, the blocker reason is required: `- [!] Tax calculation (blocked: legal review pending)`

Don't over-prescribe — agents and humans can extend with their own annotations (target dates, owners, links to specs in `.ai/knowledge/`).

---

## Bootstrap (Existing Projects)

When a project doesn't yet have `ROADMAP.md`, **the agent proposes; the human confirms.** Never bootstrap silently — agent guesses become false history that's expensive to unwind later.

1. Agent scans the codebase, `git log`, `README.md`, and `package.json` (or equivalent) to infer existing features
2. Agent drafts `## Shipped` entries with a header note marking the source:
   ```markdown
   > Bootstrapped from codebase scan on YYYY-MM-DD — verify and edit.
   ```
3. Agent presents the draft to the human: "I've drafted N items. Want me to commit this, or do you want to edit first?"
4. Only after explicit confirmation does the agent write the file
5. After the human verifies and prunes, the bootstrap header note can be removed

**For large or unfamiliar codebases** (>~50 source files, multi-package, or unknown stack), intensify step 1 with parallel sub-agent mapping. Dispatch four sub-agents in parallel, each with a fresh context and a focused brief:

1. **Stack & dependencies** — runtime, framework, build tools, key libraries, package manifests
2. **Architecture & boundaries** — directory layout, module/package boundaries, entry points, layer separation
3. **Conventions & style** — naming patterns, file organization, test patterns, lint config, formatter config
4. **Concerns & risks** — TODOs, FIXMEs, deprecation notices, recent bug-fix commits, areas with high churn

Each sub-agent writes a short summary (~100 lines max) into `.ai/knowledge/` as a `bootstrap-{facet}.md` entry. The coordinating agent reads the four summaries to draft `## Shipped` entries — usually richer and more accurate than a serial scan because each sub-agent goes deeper on its facet without context dilution.

For small or familiar codebases, the serial scan in step 1 is sufficient — parallel mapping isn't worth the orchestration overhead.

**Source:** absorbed from `gsd-build/get-shit-done` (2026-05-09); `/gsd-map-codebase` runs parallel agents per facet — the methodology absorbs cleanly; the `.planning/research/` artifact does not (use `.ai/knowledge/` instead).

For **new projects**, the agent populates `ROADMAP.md` from the requirements as part of `workflows/new-project.md` — features can be grouped by phase (`### Phase 1: MVP`, `### Phase 2`) inside the active list. No bootstrap note needed since the items aren't inferred from prior code.

---

## Update Discipline (Or the File Dies)

`ROADMAP.md` only earns its keep if it stays current. The intended pattern is to wire updates into the feature-workflow commit loop alongside the existing `.ai/memory.log` discipline:

| Action | Update |
|--------|--------|
| Picking up a `[ ]` item | Flip to `[~]` |
| Hitting a blocker | Flip to `[!]`, add a one-line reason |
| Resuming after a block clears | Flip `[!]` back to `[~]`, remove the blocker note |
| Completing | Flip to `[x]`, sweep to `## Shipped` (immediately or in batches when the active list gets crowded) |
| Cancelling/descoping | Delete the line, note the decision in `.ai/memory.log` |

A finishing-checklist self-check ("`ROADMAP.md` reflects the work just shipped") closes the loop. Without this, the file silently drifts and stops being trustworthy within a few sprints.

---

## Relationship to Other Docs

- **`references/implementation-planning.md`** — when a `ROADMAP.md` item is complex enough to need a phased multi-session execution plan, spawn an implementation plan as a separate doc. The roadmap item stays as a single line; the plan doc handles the detail. Collapse back to `[x]` on the roadmap when the plan completes.
- **`.ai/knowledge/`** — captures *why* a feature was built a certain way. Roadmap captures *what* is built or planned. Cross-reference from a roadmap item to a knowledge entry when the design rationale matters (e.g., `- [x] Auth (Clerk) — see [decision-auth.md](.ai/knowledge/decision-auth.md)`).
- **`.ai/STATUS.md`** — ephemeral session state ("currently working on X, blocked on Y"). Roadmap is durable across sessions; STATUS.md is reset/overwritten as work moves.
- **`.ai/memory.log`** — append-only session log. Roadmap is curated and edited.

---

## When NOT to Use This

- **Multi-stakeholder roadmaps** where horizons (Now/Next/Later) matter for external communication → Jira, Linear, Asana, or similar wins.
- **Projects without AI agents in the loop** where the team already has a tracker → external tracker wins; markdown-in-repo is redundant.
- **Throwaway scripts or one-off tools** with no future feature pipeline → not worth the overhead. A few lines in the README cover it.

If you're using an external tracker AND want agents to see roadmap state, the right answer is an MCP integration to that tracker — not a duplicate `ROADMAP.md`. Two sources of truth always drift.
