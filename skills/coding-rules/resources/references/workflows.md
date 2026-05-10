# Project Entry Workflows

Unified workflow for bootstrapping new projects and continuing existing ones.

> **Note:** Examples below use `bun` commands. Adapt to your project's toolchain (`npm`, `yarn`, `pnpm`, `deno`, etc.).

---

## Project State Detection

Before proceeding, determine which workflow applies:

**New project:**
- No `agent-context.yaml` file, or it has an empty `project.name` field
- No `package.json`, `deno.json`, or `pyproject.toml`
- No git history or minimal history (< 5 commits)

**Existing project:**
- `agent-context.yaml` exists with a filled `project.name`
- Runtime config file present (`package.json`, `deno.json`, `pyproject.toml`)
- Code structure already in place

---

## New Project Flow

### 1. Read Core Guidelines

Load `guidelines/core.md` to understand platform inference and runtime selection. Determine:
- **Platforms:** mobile, web, or both
- **Runtime:** Bun (default), Deno, or Node
- **Framework:** SvelteKit, Next.js, Elysia, etc.

### 2. Create Working Branch

Follow the branch naming convention from `communication.md`:

```bash
git checkout -b <type>/<short-description>
```

Examples:
- `chore/project-setup`
- `feature/initial-scaffold`
- `feat/142-user-auth`

### 3. Initialize agent-context.yaml

Create from template with:
- `project.name` and `project.description`
- `runtime.primary` (bun, node, deno)
- `runtime.language` (typescript, python, etc.)
- `runtime.target` (nextjs, sveltekit, elysia, etc.)
- `entryPoints` — main source files
- `directories` — source, public, distribution paths

### 4. Install Dependencies

```bash
bun install  # or npm install, deno cache
```

Use `--force` flag if needed. Clear cache on failure:

```bash
bun pm cache rm
```

### 5. Create Missing Files

| File | Purpose |
|------|---------|
| `package.json` | Runtime manifest (if not exists) |
| `.env.example` | Environment variable template |
| `.gitignore` | Standard template for stack |
| `.editorconfig` | Formatting rules |

#### `.env.example` placeholder policy

`.env.example` is a **committed, distributed** file. Secret-pattern
scanners (truffleHog, GitGuardian, etc.) read it and flag values whose
shape looks like a real credential. This creates real CI friction, so
treat `.env.example` placeholders with the same strictness as source
code.

**Allowed placeholder shapes:**

```bash
STRIPE_SECRET_KEY=                                     # empty
STRIPE_SECRET_KEY=your_stripe_test_secret_key          # descriptive
STRIPE_SECRET_KEY=<your-secret-key>                    # angle-bracketed
STRIPE_SECRET_KEY=REPLACE_ME                           # flag token

# Prefix belongs in a comment, not the value:
# STRIPE_SECRET_KEY format: sk_test_* (development) / sk_live_* (production)
STRIPE_SECRET_KEY=your_stripe_secret_key
```

**Disallowed placeholder shapes:**

```bash
STRIPE_SECRET_KEY=sk_test_your_secret_key_here         # prefix in value
STRIPE_SECRET_KEY=sk_test_51AbcDef...                  # real-looking
AWS_SECRET_ACCESS_KEY=AKIA...                          # real-looking
GITHUB_TOKEN=ghp_placeholder                           # prefix in value
```

The rule: a placeholder value MUST NOT carry a service-specific secret
prefix (`sk_`, `pk_live_`, `AKIA`, `ghp_`, `xoxb-`, etc.) even when
paired with obvious filler text. Put the prefix in a comment on the
line above if you need to document the key format.

### 6. Setup Linter + Formatter

For Bun projects, use Biome:

```bash
bunx @biomejs/biome init
```

Recommended `biome.json`:

```json
{
  "$schema": "https://biomejs.dev/schemas/1.9.4/schema.json",
  "organizeImports": { "enabled": true },
  "linter": { "enabled": true, "rules": { "recommended": true } },
  "formatter": { "enabled": true, "indentStyle": "space", "indentWidth": 2, "lineWidth": 120 }
}
```

Add scripts to `package.json`:

```json
{
  "scripts": {
    "lint": "biome lint .",
    "format": "biome format --write .",
    "check": "biome check --write ."
  }
}
```

Skip if project already uses ESLint/Prettier.

### 7. Create Agent Context File

Add a file for your IDE/agent:

| Tool | File |
|------|------|
| Claude Code | `CLAUDE.md` |
| Cursor | `.cursorrules` |
| Windsurf | `.windsurfrules` |
| Aider | `AIDER.md` |
| GitHub Copilot | `COPILOT.md` |

### 8. Commit Setup

```bash
git commit -m "chore: setup development environment"
```

### 9. Next Decision

- **Simple task (<1 hour, single file):** Skip planning, proceed to implementation
- **Complex task (multi-day, multiple files):** Proceed to `implementation-planning.md`

---

## Existing Project Flow

### 1. Load Project Context

Read in order:

1. `agent-context.yaml` — runtime, framework, conventions, entry points
2. `README.md` — project purpose, quick start
3. `.ai/memory.log` — recent actions, blockers (last 20 entries)
4. `.ai/knowledge/KNOWLEDGE.md` — knowledge base index (if it exists). Scan for relevant entries.
5. Agent context file (`.cursorrules`, `CLAUDE.md`, etc.)
6. `package.json` / `deno.json` — verify runtime and dependencies

### 2. Assess Current State

Check for:
- Incomplete implementations (TODO comments, partial features)
- Technical debt or blockers documented in `.ai/BLOCKERS.md`
- Failed tests or builds
- Missing dependencies
- Missing linter/formatter

### 3. Add Linter + Formatter (if missing)

If the project lacks formatting tooling:

```bash
bunx @biomejs/biome init
```

Add scripts to `package.json` and commit:

```bash
git commit -m "chore: add Biome linter and formatter"
```

### 4. Route to Appropriate Workflow

Based on user request:

| Need | Workflow |
|------|----------|
| Plan new feature or refactor | `implementation-planning.md` |
| Execute defined tasks | `execution.md` |
| Fix errors or blockers | `error-handling.md` |
| Detect gaps in tooling | `recommendations.md` |

---

## Common Steps (Both Workflows)

After project entry, verify the environment works:

```bash
# Try to build
bun run build

# Try to lint
bun run lint

# Try to run tests
bun run test
```

Document the results in `.ai/memory.log` (see `communication.md` for base format). For project entry, include:

```
[YYYY-MM-DDTHH:MM:SSZ]
Task: Project entry — [project name]
Action: Assessed project state and verified environment
Files: agent-context.yaml, .ai/memory.log
Status: DONE
Notes: State=[new|existing], Stack=[runtime, framework, tools], Build=[pass|fail], Next=[planning|execution|error handling]
```

---

## Context File Management

### When to Create

- **`agent-context.yaml`** — at project start (new project workflow, step 3)
- **`.ai/memory.log`** — at session start (first entry: project name, stack, current state)
- **`.ai/STATUS.md`** — before multi-phase work (implementation planning)
- **`.ai/BLOCKERS.md`** — when a task fails after retry budget exhausted
- **`.ai/knowledge/KNOWLEDGE.md`** — bootstrapped automatically by the `knowledge-bootstrap` hook at session start (default on). If hooks aren't wired for this project, copy `templates/KNOWLEDGE.md.template` manually when the first entry is approved. See `references/knowledge-management.md` and `references/hooks.md`.

### When to Update

| File | When |
|------|------|
| `agent-context.yaml` | After major architectural decisions or stack changes |
| `memory.log` | After every session or task completion |
| `STATUS.md` | After every phase completion or major milestone |
| `BLOCKERS.md` | After documenting a blocker; remove when resolved |
| `knowledge/` | When a decision, convention, or lesson emerges. Propose to user first. |

### Memory Log Format

Use the canonical format from `communication.md`. All entries follow the same structure — see that file for the definitive schema.

---

## Quick Reference

### New Project: Full Setup

1. Read `guidelines/core.md`
2. Create branch (`<type>/<short-description>`)
3. Fill `agent-context.yaml`
4. Install dependencies
5. Setup Biome
6. Create agent context file
7. Commit
8. Decide: simple task (skip planning) or complex (go to planning)

### Existing Project: Resume

1. Read `agent-context.yaml`
2. Read `.ai/memory.log` (last 20 lines)
3. Check build/lint/test status
4. Route to appropriate workflow

### Verification Commands

```bash
# Test everything works (adjust for your stack)
bun run build && bun run lint && bun run test

# Start development
bun run dev

# Format before commit
bun run format
```
