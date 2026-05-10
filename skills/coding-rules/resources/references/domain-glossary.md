# Domain Glossary (CONTEXT.md)

A `CONTEXT.md` at project root is the **shared domain language** for the project. It captures vocabulary that humans and agents use to talk about the codebase — concepts that take a paragraph to describe and a noun to name.

Without it, agents (and devs) burn tokens explaining the same concept five different ways: *"the problem when a lesson inside a section of a course is made real"* instead of *"materialization cascade."*

This is distinct from:
- `.ai/knowledge/` — decisions, conventions, lessons (see `references/knowledge-management.md`)
- `.ai/STATUS.md` — current session state
- `agent-context.yaml` — project metadata (runtime, stack, paths)

`CONTEXT.md` is **enduring vocabulary**, edited deliberately, read on every session.

---

## When agents read it

`CONTEXT.md` is part of the project-state read list in BOOTSTRAP step 2. Read it at session start (or after `/clear`) before planning or implementing.

## How agents use it

- **Use the glossary terms in code, plans, commit messages, and prose.** If `CONTEXT.md` names a concept, the name beats a description.
- **Name new code consistently with the glossary** — variables, functions, files, modules.
- **If a "why" question is in the glossary, don't ask it.**

## When agents propose additions

After completing a task, scan your changes. Propose adding a glossary entry when:

1. **A new domain concept was introduced** and used 2+ times (or is intended to be).
2. **An existing concept was renamed** — both the old and new term should be reconcilable.
3. **A new top-level module** was created that becomes shared vocabulary.

**Do not add:**
- Session-ephemeral terms — those go in `.ai/STATUS.md` or `memory.log`.
- Implementation trivia (*"the for-loop in `parseRow`"*).
- Technology names already obvious from `package.json` / `agent-context.yaml`.
- Decisions or lessons — those belong in `.ai/knowledge/`.

**Always propose, never silently edit.** Same rule as knowledge entries: surface the proposed term + definition, get the user's go-ahead, then write.

## Bootstrap and lifecycle

- **Scaffold if missing.** The `context-bootstrap` SessionStart hook scaffolds `CONTEXT.md` at project root from `templates/CONTEXT.md.template` on first session. It never overwrites an existing file.
- **Update at task wrap-up.** The Finish steps of `workflows/feature.md`, `workflows/bugfix.md`, and `workflows/new-project.md` include a glossary check.
- **Opt-out.** Set `context.enabled: false` in `agent-context.yaml` to disable bootstrapping. The rule itself still applies if `CONTEXT.md` exists.

## Maintenance

- Keep entries one or two sentences. The point is the *name*, not an encyclopedia entry.
- Optional pointer to where the concept lives in code (`src/billing/cascade.ts`).
- When a term is retired, mark it as superseded with the replacement; don't delete.
- Aim for a glossary that fits on one screen. If it grows beyond ~40 entries, split by domain (`CONTEXT.md` + `CONTEXT-billing.md`, etc.) and add a top-level pointer.
