<p align="center">
  <img src="https://raw.githubusercontent.com/sorawit-w/agent-skills/main/assets/wear-the-hat-li.svg" alt="wear-the-hat — one hat per task, no panel needed" width="100%"/>
</p>

# wear-the-hat

A Claude Code skill for **single-role embodiment**. Put on one role's hat — `@security_specialist`, `@dataviz_engineer`, `@accessibility_specialist`, whichever the task wants — and do the work in their voice. No panel discussion, no worker fan-out. One role, one task, one deliverable.

## Why this exists

`team-composer` is a panel. The minimum useful team is seven roles in a structured three-round discussion. That's the right shape when you want multi-perspective tension surfaced before deciding — but it's heavy ceremony for "have the security specialist look at this auth flow."

`sub-agent-coordinator` is the wrong shape too. Its `Role:` tag is for briefing a *worker* — the orchestrator delegates to a sub-agent that acts as the role. It doesn't help when the orchestrator itself wants to wear the hat for inline work.

Today's workaround is to invoke `team-composer` and let someone in the assembled team work on the task. Five steps to do what should be two:

1. Type the task → 2. Pick one role → 3. Wear the hat → 4. Do the work → 5. Done.

That's what this skill collapses. One step picks the role (auto, with disclosure); the work happens in that voice immediately.

## What it does

- **Triggers on deliberate role-lens signals** — explicit `@role` tags, embodiment phrases ("act as", "wear the hat of", "from the X perspective"), or hat-metaphor framings. Does NOT trigger greedily on tasks that don't ask for a role lens.
- **Reuses `team-composer`'s role catalog** (`role-personas.md`) as the canonical role vocabulary. No duplicate taxonomy. ~30 personas from product, engineering, design, compliance, behavioral science, clinical, creative, naming, localization, data, contemplative, and humor lenses.
- **Auto-picks the role** when the user didn't name one — via a small keyword/verb table (~25–30 rows), not an ML classifier. Four possible outcomes: clean match, multi-candidate (ask user), multi-role (offer team-composer handoff), no match (defaulted fallback).
- **Loads only what's useful from the persona** — perspective + signature phrases. Does NOT load blind spots or biases (the skill applies the lens, not the role's authentic weaknesses).
- **Decides between inline and sub-agent execution** — inline for short analytical responses, sub-agent for tasks that hit `sub-agent-coordinator`'s spawning signals (3+ files, iterative debug, > 2 min). Announces the choice.
- **Hands off to `sub-agent-coordinator`** when sub-agent mode is picked — no duplicate spawning or coordination logic. The brief carries `Role:` + `Persona context:` lines; coordinator owns the lifecycle from there.
- **Stops when the task is intrinsically multi-role** ("create a slide deck from this URL" — needs HTML + content + narrative) and offers a clean handoff to `team-composer` *with your confirmation*. Never silently pretends one role nails a multi-role task.

## What it doesn't do

- **Open a panel discussion.** One role per invocation. For multi-role tension, use `team-composer`.
- **Spawn parallel workers.** One brief, one role. For N workers in parallel, use `sub-agent-coordinator`.
- **Maintain its own role taxonomy.** The catalog is `team-composer/references/role-personas.md`. wear-the-hat consumes it and stops there.
- **Enforce the role's biases.** A `@senior_product_manager` is naturally biased toward "ship fast." wear-the-hat loads the perspective + signature phrases — not the bias. The skill applies what's useful, not what would be authentic-but-counterproductive.
- **Silently route to another skill.** Multi-role tasks stop, present options, and ask for confirmation before handing off to `team-composer`. No autopilot.
- **Trigger greedily.** A task that *could* benefit from a role lens but doesn't ask for one (e.g., "audit middleware/" with no role framing) does NOT trigger this skill. Coding-rules and the engineering review skills handle that case.

## When to use it

- You want one specific lens applied to a task — `@security_specialist` on auth code, `@dataviz_engineer` on a chart spec, `@accessibility_specialist` on a UI.
- The task is too small or too focused to justify convening a panel — but you don't want the orchestrator to default to a generic voice either.
- You want consistency across multiple invocations of the same role (call wear-the-hat for `@security_specialist` three times, get three responses with the same perspective and vocabulary).
- You want a brief produced for a sub-agent with the persona baked in — wear-the-hat composes the brief, `sub-agent-coordinator` spawns from it.

## When not to use it

- **Multi-role decisions.** "Should we use Postgres or Cassandra?" with input from architect, lead engineer, and PM — use `team-composer`.
- **Parallel implementation.** Five independent tasks, five workers — use `sub-agent-coordinator` directly. wear-the-hat is for one role per invocation.
- **Multi-role deliverables.** Slide decks, landing pages with copy+design+CTA, end-to-end features. wear-the-hat will detect these and route to `team-composer` with your confirmation.
- **Brand identity work.** Logo + tagline + brief is `brand-workshop`'s job. wear-the-hat will redirect.
- **You don't actually want a role lens.** If your task didn't ask for a specific role, just run the normal stack — wear-the-hat shouldn't activate.

## How it works — 4 phases

1. **Trigger gate.** Activate only on explicit `@role` tags, embodiment phrases ("act as", "wear the hat"), hat metaphors, lens framings ("from the X perspective"), or verb-led role assignments. Skip otherwise.
2. **Pick the role.** Use the explicit role if given. Otherwise auto-pick against the keyword/verb table in `references/auto-pick-heuristic.md` — four outcomes (clean / multi-candidate / multi-role / no-match), each with a defined response shape.
3. **Load persona.** Read the role's block from `team-composer/references/role-personas.md`. Extract perspective + signature phrases only. Skip blind spots, biases, tensions.
4. **Mode select + execute.** Inline for short analytical work; sub-agent for tasks hitting `sub-agent-coordinator`'s spawning signals. Announce the choice. Inline: respond in the role's voice. Sub-agent: produce a brief with `Role:` + `Persona context:` and hand off to coordinator.

The full protocol — including the exact wording for each outcome and the auto-pick decision tree — lives in `SKILL.md` and `references/`.

## Design choices worth knowing

- **Role taxonomy lives in `team-composer`, not here.** Two consumers (team-composer's own panel-assembly, sub-agent-coordinator's `Role:` tag) already share that catalog. wear-the-hat becomes a third consumer. Maintaining a parallel set of role labels would duplicate naming and rot in the gap. Reuse > fork.
- **Selection algorithm is local, not borrowed from team-composer.** team-composer's signal-based scoring picks N panelists for one decision. wear-the-hat picks 1 worker for one task — different shape, different math. The local heuristic is a small keyword/verb table; it stays simple deliberately.
- **Four outcomes for auto-pick, not two.** "Clean match OR fallback" is too binary. The multi-role outcome (where the task intrinsically spans 3+ roles) gets its own branch — the skill stops, presents single-role escapes AND a team-composer handoff, and asks the user to choose. No silent picking.
- **Multi-role handoff to team-composer requires confirmation.** wear-the-hat detects when it's the wrong tool and offers a clean handoff, but the handoff fires only with the user's explicit consent. Silent routing erodes skill identity.
- **Mode selection is announced.** Inline vs sub-agent always discloses ("inline mode — single-encoding question", "sub-agent mode — task hits 3+ files signal"). The user can override either way.
- **Persona biases stay un-loaded.** Loading only perspective + signature phrases keeps the role useful without enforcing the role's authentic weaknesses on the work. If you want the full persona-with-biases experience, use `team-composer` — that's where the tension between role biases is the point.

## Install

This skill is distributed as a [Claude Code](https://docs.claude.com/en/docs/claude-code) plugin inside the [`sorawit-w/agent-skills`](https://github.com/sorawit-w/agent-skills) marketplace. From Claude Code or Cowork:

```
/plugin marketplace add sorawit-w/agent-skills
/plugin install wear-the-hat@sorawit-w
```

Also installable into any agent via [`npx skills`](https://github.com/vercel-labs/skills): `npx skills add sorawit-w/agent-skills --skill wear-the-hat`.

> **Standalone install?** `wear-the-hat` embodies roles defined in the `team-composer` skill (`skills/team-composer/references/role-personas.md`). Install `team-composer` alongside it — `npx skills add sorawit-w/agent-skills --skill wear-the-hat --skill team-composer` — or grab the full set, so the role personas resolve. Without it, role embodiment falls back to generic interpretation.

Once installed, Claude picks the skill up automatically from the `description` in `SKILL.md`'s frontmatter. Invocation triggers on phrases like:

- "act as `@security_specialist` and audit middleware/"
- "wear the hat of the architect and review this design"
- "from the data-viz perspective, how should this chart encode?"
- "have the copywriter rewrite this paragraph"
- "embody `@accessibility_specialist` for this review"

Slash invocation also works:

```
/agent-skills:wear-the-hat audit middleware/ for missing CSRF guards
/agent-skills:wear-the-hat as @security_specialist <task>
```

## Cross-skill integration

| Skill | Relationship |
|---|---|
| [`team-composer`](https://github.com/sorawit-w/agent-skills/tree/main/skills/team-composer) | Owns the canonical role catalog (`role-personas.md`). wear-the-hat consumes it. For multi-role panel discussion of one decision, route to team-composer directly. wear-the-hat will hand off (with your confirmation) when the task is intrinsically multi-role. |
| [`sub-agent-coordinator`](https://github.com/sorawit-w/agent-skills/tree/main/skills/sub-agent-coordinator) | Owns sub-agent spawning, briefing templates, model-selection axes, and a `Role:` tag for briefing workers. wear-the-hat's sub-agent mode produces a brief and hands off — no duplicate logic. |
| [`cerby`](https://github.com/sorawit-w/cerby) *(if installed)* | Lists wear-the-hat in its Companion skills callout. For coding-task role embodiment, the two compose: cerby sets the engineering discipline; wear-the-hat applies the lens. |
| [`brand-workshop`](https://github.com/sorawit-w/agent-skills/tree/main/skills/brand-workshop) | For brand identity deliverables (logo + tagline + strategy brief), wear-the-hat redirects. Brand identity is multi-role + multi-deliverable; the dedicated skill is correct. |

## Status and scope

v0.1. New skill in the agent-skills marketplace.

- **Supported:** single-role embodiment for analytical reviews, audits, lens-based critiques, focused implementation in a specific role's voice, and brief composition for `sub-agent-coordinator` with persona context baked in.
- **Not supported:** panel discussion (use `team-composer`), parallel worker fan-out (use `sub-agent-coordinator`), brand identity packages (use `brand-workshop`), or maintaining a parallel role taxonomy (the catalog lives in `team-composer`).

The auto-pick heuristic in `references/auto-pick-heuristic.md` is intentionally a small keyword/verb table, not an ML classifier — calibrate by editing rows as real tasks expose gaps.

## Contributions

Not accepting external contributions right now. Feel free to fork.

## License

MIT — see the [LICENSE](https://github.com/sorawit-w/agent-skills/blob/main/LICENSE) file at the repo root.
