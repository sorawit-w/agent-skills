# Communication & Resumability

Commit conventions, session logging, status tracking, external board sync, developer TODO lists, and branch naming.

---

## Conventional Commits

```
<type>[optional scope]: <description>
<type>[optional scope]: [<issue-id>] <description>    ← with issue/ticket reference

<body — explain why>
```

**Type is required; scope is optional.** `fix: handle null user` is valid; a bare `handle null user` (no type) is not. Add a scope when it adds a useful locator (`fix(auth): …`); omit it for repo-wide changes — never drop the type to avoid an awkward scope.

| Type     | When                                    |
|----------|-----------------------------------------|
| feat     | New feature or capability               |
| fix      | Bug fix                                 |
| refactor | Code restructuring, no behavior change  |
| test     | Adding or updating tests                |
| docs     | Documentation only                      |
| chore    | Build, CI, dependency updates           |

Examples:
- `feat(api): add rate limiting to public endpoints`
- `fix(auth): [#142] resolve token refresh race condition`

Include the issue/ticket ID when the task is tracked in an external system (Linear, Jira, GitHub Issues, etc.). This links commits to their context and makes tracing decisions easier.

---

## Session Logging

**This is the canonical format for `.ai/memory.log`.** All other references point here. Append after every significant action (create if missing):

```
[YYYY-MM-DDTHH:MM:SSZ]
Task: [task-id or description]
Action: [what you did]
Files: [modified files]
Commit: [SHA]
Status: DONE | BLOCKED
Notes: [decisions, next steps]
Observations: [optional — neutral facts noticed during the task, e.g. "Build took 47s",
  "npm audit shows 3 moderate vulnerabilities", "Test suite: 312 tests, 2 skipped"]
```

**Observations are facts, not suggestions.** Record what you noticed — build times, warnings, skipped tests, deprecation notices, audit results. Do NOT recommend actions or suggest improvements. The developer decides what to act on.

---

## Status Tracking

Maintain `.ai/STATUS.md` (create if missing) with:
- Current position (phase, milestone, branch)
- Progress (Done / In Progress / Blocked / Ready counts)
- Recent completions (task, commit, date)
- Next up (prioritized task queue)
- Blockers (what's stuck and why)

Only create `.ai/BLOCKERS.md` when there is an actual blocker. Track using: project issue tracker > `.ai/` files > commit messages.

---

## Knowledge Base

Maintain `.ai/knowledge/` for curated project knowledge — architecture decisions, domain context, conventions, and lessons learned. Unlike `memory.log` (append-only session logs) or `STATUS.md` (ephemeral state), the knowledge base is edited and organized like a wiki.

- Index: `.ai/knowledge/KNOWLEDGE.md` — agents read this to find relevant context
- Entries: markdown files with YAML frontmatter (`title`, `type`, `domain`, `confidence`, `created`)
- Types: `decision`, `context`, `convention`, `reference`, `lesson`

**Propose entries when decisions or lessons emerge. Always ask before writing.**

→ Full details: `knowledge-management.md`

---

## External Board Sync

When a project uses an external tracker (Linear, Jira, Asana, GitHub Issues, etc.) and the agent has MCP access to it:

1. **Check the board before starting** — Look for existing tickets related to your task. Don't create duplicates.
2. **Update ticket status as you work** — Move tickets to "In Progress" when you start, "Done" when complete, "Blocked" when stuck.
3. **Create new tickets for discovered work** — If you find bugs or tasks outside your scope, create tickets rather than fixing them silently.
4. **Link commits to tickets** — Use the `[#issue-id]` pattern in commit messages.
5. **Keep the board in sync** — The board should reflect reality. If a task took longer than expected or was split into smaller pieces, update accordingly.

The agent has PM authority to manage tickets — create, update, re-prioritize — as long as it serves the current task and keeps the board accurate.

---

## Developer TODO List

Some tasks require human action that an agent cannot perform — external service signups, API key generation, cloud resource provisioning, app store submissions, DNS changes, etc.

When your implementation depends on something only a human can do:

1. **Create a `DEVELOPER_TODO.md`** file in the project root (or append to it if it exists)
2. **Document each action** the developer needs to take:

```markdown
## Developer Action Required

### [Category]: [Short description]
- **What:** [Exactly what needs to be done]
- **Why:** [Which part of the implementation depends on this]
- **How:** [Step-by-step instructions or link to docs]
- **Where to put the result:** [e.g., "Add to .env as `STRIPE_SECRET_KEY`"]
- **Blocked tasks:** [What can't proceed until this is done]
```

**Common categories:**
- **API Keys** — Third-party service credentials (Stripe, SendGrid, Auth0, etc.)
- **Cloud Resources** — Database provisioning, storage buckets, CDN setup
- **External Services** — OAuth app registration, webhook configuration, domain verification
- **Secrets** — Encryption keys, signing certificates, JWT secrets
- **Manual Approvals** — App store review, DNS propagation, SSL certificate issuance
- **Account Setup** — Service accounts, team invitations, permission grants

Never hard-code placeholder secrets or skip integration steps silently. If the implementation can't work without a human action, document it clearly and move on to the next available task.

---

## Branch Conventions

**Never work directly on protected branches** — main, master, dev, develop, staging, release/*, or trunk — unless explicitly told.

### Branch Naming

```
<type>/<issue-id>-<short-description>   # with issue/ticket
<type>/<short-description>              # without issue/ticket
```

**Types** (aligned with conventional commits, but use full words for readability):

| Type     | When                                    |
|----------|-----------------------------------------|
| feature  | New feature or capability               |
| fix      | Bug fix                                 |
| refactor | Code restructuring, no behavior change  |
| test     | Adding or updating tests                |
| docs     | Documentation only                      |
| chore    | Build, CI, dependency updates           |
| wip      | Incomplete work parked for later        |

**Rules:**
- Description: kebab-case, 2–5 words
- Before creating: check `git branch --list` to avoid collisions

---

## Pull Requests

Prefer **small PRs scoped to one feature or fix** and **squash-merge for linear history**. If a PR grows past your team's review-fatigue threshold, split it before requesting review — two reviewed PRs are healthier than one un-reviewed one.

A small PR:
- Has a single, statable purpose (can be summarized in one sentence without "and")
- Touches a coherent slice of the codebase, not a scattergun
- Is reviewable in one sitting by one person

Source: principle distilled from `shanraisshan/claude-code-best-practice` (2026-04-19, MIT). Numeric line-count anchors from the original were intentionally omitted — teams set their own.

### PR Title & Body

**The PR title follows the commit convention** — `<type>[optional scope]: <description>`. Under squash-merge (the strategy above) the title becomes the squashed commit's subject on the base branch, so a freeform title silently breaks the conventional-commit history the per-commit rule protects. When a PR squashes to a single commit, reuse that commit's subject verbatim.

**Body — minimal but present. Use these two headings verbatim** (keeps PR bodies greppable and lets a reviewer reuse the §Manual Verification block; ad-hoc sections like Summary/Changes/Testing defeat that consistency):

```
## What & why
<one-paragraph summary: the problem and the chosen approach>

## How to verify
<steps a reviewer runs to confirm it works — reuse the §Manual Verification block from the workflow>
```

Link a tracked task with a closing keyword (`Closes #142`, `Fixes PROJ-12`) so the merge auto-closes it. Keep the body proportional to the diff — a one-line fix does not need a four-section essay.
