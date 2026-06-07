---
description: Run skill-evaluator on every SKILL.md changed on this branch, sequentially in the main loop
argument-hint: "[base-ref | skill-name ...]"
---

Audit the skills whose `SKILL.md` changed on the current branch, using the
`skill-evaluator` skill (`skills/skill-evaluator/SKILL.md`).

## Resolve the target set

- **No argument** — compute changed skills from git:
  `git diff --name-only main... -- 'skills/**/SKILL.md'`
  (use the merge-base against `main`; this is the set of skills whose rule text
  changed on this branch).
- **A base ref** (e.g. `origin/main`, a tag, a SHA) — diff against that instead of
  `main`.
- **One or more skill names** — skip the diff and audit exactly those skills.

If the resolved set is empty, say so and stop — nothing to audit.

## Run each audit — SEQUENTIALLY, in the MAIN loop

For each `SKILL.md` in the set, run `skill-evaluator` on it **here, in the main
loop, one at a time.** Wait for each to finish before starting the next.

**Do NOT fan out — this is the load-bearing rule.** Do not dispatch one
`skill-evaluator` per skill as parallel sub-agents (Agent/Task tool). `skill-evaluator`'s
bias removal *is* its Phase 4, which spawns its own executor + grader sub-agents;
wrapping it in a sub-agent triggers no-nested-sub-agents and silently collapses
that split into in-context simulation (skill-evaluator will emit a `⚠️ DEGRADED`
banner). Sequential main-loop runs keep each audit's split-role intact. The
trade-off is wall-clock time, not rigor — accept it.

(The fan-out you *can* do is internal: each `skill-evaluator` run spawns its own
executor/grader sub-agents. That nesting level is the one the skill owns — you
don't add another above it.)

## Collect

After all runs, present one summary: per-skill verdict + headline findings. If any
run came back `⚠️ DEGRADED`, surface it loudly at the top — that means an audit did
not actually run independently and must be re-run in the main loop.
