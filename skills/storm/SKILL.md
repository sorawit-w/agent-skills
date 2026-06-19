---
name: storm
description: >
  Research a topic from multiple perspectives, grounded in retrieval, and return a cited
  briefing — an agent-native port of Stanford's STORM. Discovers (or accepts) diverse
  perspectives, runs grounded question-asking per perspective with retrieval at each step,
  and curates findings into a source-attributed synthesis. Every claim is cited or tagged
  [unverified]. Runs standalone (`/storm <topic>`) or as a hand-off target for `team-composer`,
  inheriting the panel's active roles as seed perspectives. Triggers on "research X", "what's
  known about Y", "survey the evidence on Z", "build a grounded briefing on…", or an upstream
  skill needing sourced external knowledge. Does NOT trigger on single-source-of-truth
  fact-checking or one authoritative report — that's `deep-research`; nor on opinion, critique,
  planning, or assembling a team — that's `team-composer`. Perspective-breadth, not source-breadth.
metadata:
  tier: draft
tags:
  - research
  - retrieval-grounded
  - cited-briefing
  - perspectives
  - storm
  - hand-off-target
---

# storm

Research a topic the way Stanford's STORM does its pre-writing: **discover the perspectives that matter, ask grounded questions from each, and synthesize the answers into a cited briefing.** The wedge is *breadth of perspectives* — what different lenses surface about a topic — not breadth of sources on a single question.

This is an **agent-native port of the STORM mechanism**, not Nav Toor's 4-prompt chat workflow. The agent already holds retrieval, so grounded *is* the default — there is no un-grounded mode.

---

## Phase 0 — Boundary gate

Activate `storm` when the request wants **sourced external knowledge across perspectives**. Route away otherwise:

| Request shape | Skill |
|---|---|
| "Research X", "what's known about Y", "survey the evidence on Z", "grounded briefing on…" | **storm** |
| An upstream skill (e.g. `team-composer`) needs sourced knowledge it can't reason to | **storm** (hand-off) |
| Single-source-of-truth fact-check, one authoritative report, "verify this claim" | `deep-research` |
| Opinion, critique, planning, "assemble a team", "review my plan" | `team-composer` |
| General agent loop / build work | the harness / `cerby` |

The `deep-research` line is the load-bearing one: it owns *source-breadth* (fan-out, fetch, adversarially verify into one report). `storm` owns *perspective-breadth*. If the request wants the ground truth on one question, it's `deep-research`. If it wants what several lenses reveal about a topic, it's `storm`.

---

## Phase 1 — Perspectives in

Two paths:

- **Seeded (hand-off).** A caller supplied perspectives (e.g. `team-composer` passes its active roles). Use them verbatim as the perspective set — they are already domain-relevant lenses. Do not re-discover.
- **Discovered (standalone).** No seed. *Discover* perspectives by surveying adjacent material on the topic (STORM's move): a quick retrieval pass to find the recurring stakeholder/expert/angle framings, then name 3–4 distinct ones. A fixed generalist set is one possible seed, never the only option.

Bound it: **`max_perspectives` (default 4)**. Stated up front so the user can correct it.

---

## Phase 2 — Grounded Q&A per perspective

For each perspective, generate questions that lens would ask, and **answer them via retrieval**. Bound: **`max_turns_per_perspective` (default 3)** — at most `max_perspectives × max_turns` retrieval cycles total.

- Every answer **carries its source(s)**. Keep a source→claim map from here forward — synthesis depends on it (see `references/honesty-rubric.md`).
- Retrieval is **capability-gated**: use whatever retrieval the runtime holds (web search/fetch, a `*_search` MCP, drive search). Do not assume a specific tool name.
- If a question's retrieval comes up empty, record the answer as `[unverified / reasoning-only]` — do not pad it with confident introspection.

Mechanics (question generation, dedup, the contradiction-map pass) live in `references/loop-mechanics.md`.

---

## Phase 3 — Curate → outline

Cluster findings across perspectives, **dedupe sources**, and draft a structure. This is where overlap collapses and the shape of the briefing emerges. Carry the source→claim map through unchanged.

---

## Phase 4 — Cited synthesis

Emit the output. **Every factual line is either source-attributed or tagged `[unverified / reasoning-only]`** — no exceptions. The honesty rule is structural: because the source→claim map is carried through Phases 2–3, a line with no mapped source *cannot* be presented as verified.

**Output formats:**

- **`briefing` (default)** — decision-oriented: a one-paragraph summary, findings ranked by reliability (each with supporting *and* challenging sources), the actionable insight, and open questions. Each claim cited.
- **`report` (`--report`)** — a longer sourced write-up (closer to STORM's article form) for when breadth matters more than turnaround.

---

## Phase 5 — Optional rigor passes (flagged on; `--no-rigor` to skip)

Cheap, on by default, off with `--no-rigor`. Both are specified in `references/honesty-rubric.md`:

- **Contradiction map** — where perspectives clash, what they all agree on, and what *none* addressed (blind spots).
- **Peer review / confidence** — a confidence score per finding **tied to source-backing** (not fluency), the weakest link, a bias check, and the missing perspective. This pass exists primarily to catch STORM's two self-flagged failure modes — **source-bias transfer** and **over-association of unrelated facts** — so it is not cosmetic.

---

## Inputs / outputs contract

**Standalone:**

```
/storm <topic> [--report] [--no-rigor] [--max-perspectives N] [--max-turns N]
```

No seed perspectives → Phase 1 discovers them.

**`team-composer` hand-off:**

- **In:** the research question + `team-composer`'s active roles, passed as the seed perspectives.
- **Out:** a cited briefing returned to the panel, which folds it back into its conclusion.

**Invariant:** no claim ships without a source or an explicit `[unverified / reasoning-only]` tag. With retrieval unavailable, the *entire* output is tagged — the honesty invariant holds by construction, not by reminder.

---

## Capability-gated retrieval & graceful degradation

Gate on "is a retrieval tool available in this runtime?" — not on which agent or vendor is running (a brittle check). If none is available, **do not refuse silently and do not fabricate**: produce the perspective structure and reasoning, label every line `[unverified / reasoning-only]`, and state plainly that retrieval was unavailable so the output is ungrounded.

---

## What this skill is NOT

- **Not single-source-of-truth research.** One authoritative report from source fan-out is `deep-research`. storm is multi-perspective.
- **Not a panel.** Opinion, critique, planning, team assembly → `team-composer`.
- **Not Co-STORM.** No human-in-the-loop turn-by-turn collaboration (separate, heavier paper).
- **Not a conversation-simulation engine.** The bounded Phase-2 Q&A is the whole loop; no agent-vs-agent dialogue beyond it.
- **Not a Wikipedia-article generator by default.** Briefing is the default; the long report is opt-in.

---

## Cross-skill integration

| Skill | Relationship |
|---|---|
| `deep-research` *(if installed)* | The distinct neighbor. `deep-research` owns single-topic, source-of-truth research (fan-out → fetch → adversarial verify → one cited report). storm owns multi-perspective research. Route "verify this claim" / "give me the authoritative answer on X" there; route "what do different lenses reveal about X" here. |
| [`team-composer`](https://github.com/sorawit-w/agent-skills/tree/main/skills/team-composer) | The primary caller. When a panel hits a grounding need ("verify the current state of X", "survey what's known about Y", "we're guessing here"), team-composer hands off to storm with its active roles as the seed perspectives; storm returns a cited briefing the panel folds into its conclusion. The team-composer-side routing — a storm row in its Cross-Skill table + a grounding-need trigger, plus the contradiction-map and peer-review lenses storm seeded — is wired as of team-composer v5.4.0. |
| [`sub-agent-coordinator`](https://github.com/sorawit-w/agent-skills/tree/main/skills/sub-agent-coordinator) | If per-perspective Q&A is heavy enough to parallelize, the coordinator owns the spawning/briefing — storm does not duplicate that logic. |

---

## Slash invocation

```
/agent-skills:storm <topic>
/agent-skills:storm <topic> --report
/agent-skills:storm <topic> --no-rigor --max-perspectives 3
```

Equivalent to the natural-language trigger, just unambiguous.

---

## Status

v0.1 — new skill. Ports the STORM *mechanism* (perspective discovery → grounded per-perspective Q&A → cited synthesis), bounded by two knobs (`max_perspectives`, `max_turns_per_perspective`). The `team-composer` back-port (the grounding-need hand-off row + the contradiction-map lens in its Discuss phase + peer-review/confidence in its Audit phase) shipped in team-composer v5.4.0.

## When to use this skill

Load this skill when:
- The user wants grounded research across perspectives on a topic ("research X", "what's known about Y", "survey the evidence on Z", "build me a grounded briefing on…").
- An upstream skill needs sourced external knowledge it can't reason its way to.

Do NOT load this skill when:
- The user wants the authoritative answer on a single question or to verify one claim → `deep-research`.
- The user wants opinion, critique, planning, or a team assembled → `team-composer`.
- There's no external-knowledge need — let the normal skill stack handle it.

**Tags:** research, retrieval-grounded, cited-briefing, perspectives, storm, hand-off-target
