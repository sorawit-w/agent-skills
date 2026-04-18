<p align="center">
  <img src="https://raw.githubusercontent.com/sorawit-w/agent-skills/main/assets/sub-agent-coordinator-li.svg" alt="sub-agent-coordinator — many hands, one source of truth" width="100%"/>
</p>

# sub-agent-coordinator

A Claude Code skill for orchestrating multi-agent work — turns the primary agent into a coordinator that briefs, dispatches, and integrates parallel sub-agents instead of grinding through implementation alone.

## Why this exists

The default failure mode of an agent given a 90-minute task is to start coding immediately and stay in the editor for the next 90 minutes. Even when sub-agents are available, the easy path is "I'll just do it myself" — the briefing overhead feels heavier than the work, until it isn't.

By the time you notice, you've burned an hour on a task that three sub-agents could have done in twenty minutes in parallel, and the coordinator has lost track of the bigger picture.

This skill exists to flip that default. It gives the coordinator a small, opinionated set of patterns — when to delegate, how to brief, which coordination shape fits the work — and it's deliberately strict about what *not* to do (no nested delegation, no overlapping file edits, no blind trust without verification).

## What it does

- Defines the **coordinator vs. implementer mindset** — your job is breaking down work, briefing sub-agents, and verifying results, not grinding through every line yourself.
- Gives a **2-minute / 15-minute decision boundary** for delegating, plus seven concrete spawning signals (debugging, iterative work, multi-file features, dependency issues, test suites, multi-file docs, investigation).
- Provides **two briefing templates** — Quick Brief for complexity 1–5, Full Brief for 6+. Each comes with explicit scope, out-of-scope, tool budget, and success criteria so sub-agents don't drift.
- Codifies **four coordination patterns** — Fan-Out (parallel independent), Pipeline (producer→consumer), Specialist Domain Routing (skill-loaded sub-agents), Review/Validation (parallel verification).
- Encodes **eight coordination rules** — non-overlapping files, clear boundaries, trust-but-verify after each sub-agent, conflict resolution in the main agent, structured reporting, no nested sub-agents, unblock dependents promptly, shared-worktree-by-default ownership.
- Sets a **communication protocol** for both sides — sub-agents report progress proactively and unblock fast; the coordinator checks in on long-running work and verifies results immediately rather than batching.

## What it doesn't do

- **Spawn sub-agents itself.** This is a coordination *playbook*, not an executor. You still run the spawn calls — the skill just makes sure the brief, scope, and verification protocol are in place first.
- **Pretend sub-agents are humans.** A sub-agent is another instance of you, task-focused and context-limited. The skill is designed for that, not for delegating to teammates.
- **Allow nested delegation.** Sub-agents do not spawn their own sub-agents. All spawning happens at the coordinator level — that's a hard rule, not a suggestion.
- **Auto-iterate or auto-verify.** It tells you *when* and *how* to verify; it doesn't silently re-run gates. Trust the sub-agent's report when it's clean; re-run only when the report is missing, partial, suspicious, or about to land on a protected branch.
- **Force delegation on tightly coupled work.** Single-file edits, cross-cutting decisions, and architecture choices stay with the primary agent. Delegation overhead exceeds the benefit when the work needs unified judgment.

## When to use it

- You're starting a multi-step task that's clearly bigger than 15 minutes and at least partially parallelizable.
- You're scaffolding a monorepo, running large refactors across multiple files, or doing translation/i18n work where each chunk is independent.
- You've caught yourself thinking "this should be quick, I'll just do it" — that's the optimism-bias signal the skill is built to interrupt.
- You're routing work that needs specialist context (i18n, design systems, DevOps) and want a sub-agent with the right skill loaded.
- You want to run implementation and review in parallel rather than sequentially.

## When not to use it

- **Single-file edits or quick fixes (< 15 min).** The 2-minute rule says: handle directly. Briefing a sub-agent for a one-line config change is pure overhead.
- **Tightly coupled changes.** If A affects B affects C, sequential understanding wins — split it apart and you lose the thread.
- **The platform doesn't support sub-agents.** Then you're just a sequential implementer and the skill doesn't apply.
- **Architecture decisions or cross-cutting calls.** Those need a single owner and a unified mental model.

## How it works — the loop

1. **Decide whether to delegate.** Apply the 2-minute / 15-minute boundary and check the seven spawning signals. If you catch yourself optimistically estimating "this should be quick" on a non-trivial task — spawn anyway.
2. **Pick the coordination pattern.** Fan-Out for parallel independent. Pipeline for producer→consumer. Specialist Routing when domain skills matter. Review/Validation when you want a second pair of eyes in parallel.
3. **Brief the sub-agent.** Quick Brief for simple tasks, Full Brief for complex. Always include scope, out-of-scope, tool budget, success criteria, and a "files to read first" list.
4. **Spawn (in parallel if non-overlapping).** Multiple Agent calls in a single message run concurrently. Sequential only if there's a real dependency.
5. **Read the report when it returns.** Status, files modified, gate results, decisions, blockers. Trust clean reports; re-verify only when the report is incomplete, suspicious, or shared-file/protected-branch sensitive.
6. **Resolve conflicts in the main agent.** If two sub-agents touched the same code, integrate carefully and re-run gates after the merge.
7. **Unblock dependents.** Find tasks that depend on this one, move them to ready, and spawn the next batch.

## Design choices worth knowing

- **Coordinator-only spawning is non-negotiable.** Allowing nested delegation produces coordination chaos — too many places to track state, too easy to lose the thread. One coordinator, many hands.
- **Shared worktree by default.** When the coordinator is in a worktree, sub-agents share it. Sibling worktrees are an escalation when file conflicts repeatedly appear, not a default — they multiply branches and merge work.
- **Briefing depth matches task complexity.** Over-briefing simple tasks adds friction; under-briefing complex tasks causes wrong implementations. Quick vs. Full is a deliberate fork, not a sliding scale.
- **Trust the report, then verify only when warranted.** Reflexively re-running gates that just passed wastes parallel capacity. The skill names exactly when to re-verify (missing/partial report, shared-file changes, protected branches).
- **Tool budgets are guardrails, not goals.** ~15 calls for simple, ~30 for medium, ~50 for complex. A sub-agent approaching its budget should wrap up and report progress, not spiral into unbounded iteration.

## Install

This skill is distributed as a [Claude Code](https://docs.claude.com/en/docs/claude-code) plugin inside the [`sorawit-w/agent-skills`](https://github.com/sorawit-w/agent-skills) marketplace. From Claude Code or Cowork:

```
/plugin marketplace add sorawit-w/agent-skills
/plugin install sub-agent-coordinator@sorawit-w
```

Once installed, Claude picks the skill up automatically from the description in its `SKILL.md` frontmatter. Invocation triggers on phrases like "delegate this," "fan out the work," "spawn sub-agents," "coordinate this rollout," or any prompt where the work is clearly parallelizable across more than one file or domain.

## Status and scope

v0.1. Originally extracted from the coding-rules project (MIT). The scope is intentionally narrow:

- **Supported:** multi-step coding work, monorepo scaffolding, large refactors, translation/i18n batches, parallel implementation+review, specialist routing.
- **Not supported:** platforms without sub-agents, tightly coupled changes that need sequential understanding, architecture decisions that need a single owner.

If asked to coordinate work that doesn't fit the supported shapes, the skill says so explicitly rather than producing decorative orchestration that adds overhead without parallelism.

## Contributions

Not accepting external contributions right now. Feel free to fork.

## License

MIT — see the [LICENSE](https://github.com/sorawit-w/agent-skills/blob/main/LICENSE) file at the repo root.
