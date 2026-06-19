<p align="center">
  <img src="https://raw.githubusercontent.com/sorawit-w/agent-skills/main/assets/storm-li.svg" alt="storm — perspectives in, grounded Q&A, cited briefing out" width="100%"/>
</p>

# storm

A Claude Code skill for **perspective-driven, retrieval-grounded research**. Point it at a topic; it discovers the perspectives that matter, asks grounded questions from each, and returns a **cited briefing** where every factual line is either sourced or tagged `[unverified]`. An agent-native port of Stanford's [STORM](https://arxiv.org/abs/2402.14207).

## Why this exists

STORM's insight is that good research isn't one search — it's *many perspectives* each asking different questions, grounded in sources, then synthesized. The original is a Python pipeline; Nav Toor's popular version is a 4-prompt copy-paste chat workflow whose whole selling point ("5 minutes, no setup, just paste") only matters to a human pasting into a chat box.

Inside an agent, that framing is dead weight. The agent already holds retrieval — there's no setup to avoid and no reason to run un-grounded. `storm` ports the **mechanism** (perspective discovery → per-perspective grounded Q&A → cited synthesis) and drops the human-UI artifact. Grounded *is* the default.

It also fills a real gap in this repo: `team-composer` is a discuss-and-hand-off skill that deliberately doesn't do retrieval. When a panel needs sourced external knowledge it can't reason its way to, `storm` is the hand-off target — and it inherits the panel's roles as seed perspectives instead of re-discovering them.

## What it does

- **Discovers or accepts perspectives.** Standalone, it surveys adjacent material to find 3–4 genuinely distinct lenses on the topic. As a hand-off target, it uses the caller's supplied perspectives (e.g. `team-composer`'s active roles) verbatim.
- **Runs grounded Q&A per perspective.** Each lens asks the questions it would ask; each answer is backed by retrieval and carries its source. Bounded by two knobs — `max_perspectives` (4) and `max_turns_per_perspective` (3).
- **Synthesizes a cited briefing.** Decision-oriented by default: summary, findings ranked by reliability with supporting *and* challenging sources, the actionable insight, open questions. A longer `--report` form is opt-in.
- **Enforces honesty structurally.** A source→claim map is carried through synthesis, so a line with no source *cannot* render as verified — it's tagged `[unverified / reasoning-only]`. Remove retrieval entirely and the whole output is tagged.
- **Runs optional rigor passes** (on by default, `--no-rigor` to skip): a **contradiction map** (clashes / consensus / blind spots) and a **peer-review** pass that scores confidence by source-backing and hunts STORM's two self-flagged failure modes.

## What it doesn't do

- **Single-source-of-truth research.** One authoritative answer from source fan-out + adversarial verification is `deep-research`. storm is perspective-breadth, not source-breadth.
- **Opinion, critique, planning, or team assembly.** That's `team-composer`. storm produces sourced knowledge, not the panel's judgment.
- **Co-STORM.** No human-in-the-loop turn-by-turn collaboration — that's a separate, heavier paper.
- **A conversation-simulation engine.** The bounded Phase-2 Q&A is the whole loop; no agent-vs-agent dialogue beyond it.
- **Wikipedia articles by default.** Briefing is the default output; the long report is opt-in.
- **Un-grounded output presented as fact.** When retrieval comes up empty, it says so and labels the answer — it never dresses introspection as verified.

## When to use it

- "Research X." / "What's actually known about Y?" / "Survey the evidence on Z." / "Build me a grounded briefing on…"
- You want to understand a topic from *several* angles, with sources, not one authoritative answer.
- An upstream skill (usually `team-composer`) hits a grounding need and needs sourced external knowledge.

## When not to use it

- **You want the authoritative answer on one question, or to verify a single claim** → `deep-research`.
- **You want perspectives to *argue* and reach a decision** → `team-composer` (judgment, not sourced research).
- **There's no external-knowledge need** — let the normal skill stack handle it.

## How it works — the loop

1. **Perspectives in** — discovered by surveying adjacent material (standalone), or supplied by the caller (hand-off). Capped at `max_perspectives`.
2. **Grounded Q&A per perspective** — question → retrieve → answer, each answer sourced; capped at `max_turns_per_perspective`. Empty retrieval → `[unverified]`, never filler.
3. **Curate → outline** — cluster findings, dedupe sources, draft structure; the source→claim map rides through unchanged.
4. **Cited synthesis** — emit the briefing (or `--report`). Every line sourced or tagged.
5. **Optional rigor** — contradiction map + peer-review/confidence (`--no-rigor` to skip).

Procedural detail lives in [`references/loop-mechanics.md`](references/loop-mechanics.md); the honesty discipline in [`references/honesty-rubric.md`](references/honesty-rubric.md).

## Design choices worth knowing

- **Mechanism, not paper-fidelity.** Two knobs (`max_perspectives`, `max_turns_per_perspective`) — not the reference implementation's full knob-set. "Be faithful to the paper" is the over-build trap; the core loop is what earns its place.
- **Honesty is structural.** Confidence tracks source-backing, never fluency. The dry-run test (no retrieval ⇒ entirely `[unverified]`) is a *mechanical* check, not a prose reminder — it either passes or it doesn't.
- **Peer-review isn't cosmetic.** It exists to catch STORM's own flagged failures — *source-bias transfer* and *over-association of unrelated facts* — so the pass actively checks source concentration and whether *linked* facts have a sourced link.
- **Capability-gated retrieval.** Gates on "is a retrieval tool available?", not on which vendor/agent is running. Survives new platforms; degrades cleanly to labelled-unverified when no tool is present.
- **Distinct neighbor to `deep-research`.** Both end in a cited briefing, so the boundary is drawn sharply: source-of-truth fact-checking routes to `deep-research`; multi-perspective discovery routes here.

## Install

This skill is distributed as a [Claude Code](https://docs.claude.com/en/docs/claude-code) plugin inside the [`sorawit-w/agent-skills`](https://github.com/sorawit-w/agent-skills) marketplace. From Claude Code or Cowork:

```
/plugin marketplace add sorawit-w/agent-skills
/plugin install storm@sorawit-w
```

Also installable into any agent via [`npx skills`](https://github.com/vercel-labs/skills): `npx skills add sorawit-w/agent-skills --skill storm`.

Once installed, Claude picks the skill up automatically from the `description` in `SKILL.md`'s frontmatter. Invocation triggers on phrases like:

- "Research what's actually known about microplastics in drinking water."
- "Survey the evidence on four-day work weeks — give me a grounded briefing."
- "Build me a cited briefing on RAG vs. long-context for production agents."

Slash invocation also works:

```
/agent-skills:storm <topic>
/agent-skills:storm <topic> --report --max-perspectives 3
```

## Cross-skill integration

| Skill | Relationship |
|---|---|
| `deep-research` *(if installed)* | The distinct neighbor. It owns single-topic, source-of-truth research (fan-out → fetch → adversarial verify → one cited report); storm owns multi-perspective research. "Verify this claim" / "the authoritative answer on X" → `deep-research`; "what different lenses reveal about X" → storm. |
| [`team-composer`](https://github.com/sorawit-w/agent-skills/tree/main/skills/team-composer) | The primary caller. When a panel hits a grounding need ("verify the current state of X", "we're guessing here"), it hands off to storm with its active roles as seed perspectives; storm returns a cited briefing the panel folds into its conclusion. |
| [`sub-agent-coordinator`](https://github.com/sorawit-w/agent-skills/tree/main/skills/sub-agent-coordinator) | If per-perspective Q&A is heavy enough to parallelize, the coordinator owns the spawning/briefing. storm does not duplicate that logic. |

## Status and scope

v0.1. New skill in the agent-skills marketplace.

- **Supported:** standalone grounded research (`/storm <topic>`), `team-composer` hand-off with seeded perspectives, briefing (default) and report output, contradiction-map + peer-review rigor passes, capability-gated retrieval with clean degradation.
- **Not supported:** single-source-of-truth research (use `deep-research`), opinion/critique/planning (use `team-composer`), Co-STORM human-in-the-loop, conversation-simulation beyond the bounded Q&A.

The `team-composer` back-port (contradiction map into its Discuss phase, peer-review into its Audit phase) ships as a separate follow-up change.

## Contributions

Not accepting external contributions right now. Feel free to fork.

## License

MIT — see the [LICENSE](https://github.com/sorawit-w/agent-skills/blob/main/LICENSE) file at the repo root.
