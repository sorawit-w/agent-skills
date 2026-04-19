# Phase 3 Path A — local execution runbook

## Why this needs to run outside Cowork

Anthropic's `skill-creator` eval (`scripts/run_eval.py`) spawns a subprocess
`claude -p` and watches its stream. Inside Cowork mode the nested `claude`
process resolves `apiKeySource: "none"` and exits with `Not logged in · Please
run /login` before producing any token. Every subprocess returns "not
triggered" and the eval results carry no signal.

To get real data, run this on your laptop where `claude` is logged in.

## Prerequisites

```bash
# Verify claude is authenticated
claude -p "say hi"   # should produce a real reply, not an auth error
```

## Run

```bash
cd ~/path/to/agent-skills    # adjust to your local clone

# Make sure the Anthropic skill-creator scripts dir is on your machine.
# It typically ships at ~/.claude/skills/skill-creator/
SKILL_CREATOR=~/.claude/skills/skill-creator
cd "$SKILL_CREATOR"

# Eval 1 — does our skill-evaluator description discriminate correctly?
python3 -m scripts.run_eval \
  --eval-set ~/path/to/agent-skills/eval/phase3/queries.evaluator.json \
  --skill-path ~/path/to/agent-skills/skills/skill-evaluator \
  --num-workers 8 --timeout 60 --runs-per-query 3 --verbose \
  > ~/path/to/agent-skills/eval/phase3/results.evaluator.json

# Eval 2 — does Anthropic's skill-creator description discriminate correctly?
python3 -m scripts.run_eval \
  --eval-set ~/path/to/agent-skills/eval/phase3/queries.creator.json \
  --skill-path "$SKILL_CREATOR" \
  --num-workers 8 --timeout 60 --runs-per-query 3 --verbose \
  > ~/path/to/agent-skills/eval/phase3/results.creator.json
```

## Reading the results

Each result file has a `results` array. Cross-firing = collision evidence:

| Pattern | Interpretation |
|---|---|
| Group A query (audit ask) fires `skill-creator` | skill-creator over-claims audit territory |
| Group B query (build ask) fires `skill-evaluator` | skill-evaluator over-claims creator territory |
| Group C query (ambiguous) fires either | aggressive triggering on edge cases — note which |
| Group D query (unrelated) fires either | precision bug — should be 0 |

Matrix gate: collision rate (false-positives across A+B = 12 queries) **< 15%**
→ skill-evaluator is sufficiently differentiated to ship beside the official
shelf without further description surgery.

## If the gate fails

Most likely fix is on `skill-evaluator/SKILL.md` frontmatter:
- Tighten the trigger phrase list further
- Add explicit anti-triggers ("Do NOT trigger on …")
- Move the strongest hard-boundary line above the trigger list

Don't loosen `skill-creator` — it's Anthropic's, we don't own it.

## Path B (paired-skill wrapper) — if needed

If Path A passes precision (no false positives) but recall is poor (true
positives don't fire either), description is too restrictive, not too
collision-prone. A v2 wrapper that writes both fake commands before spawning
`claude -p` and scores `correct-winner / wrong-winner / both / neither` is the
proper measurement — see `skills/skill-evaluator/SKILL.md` "Roadmap — v2
paired-skill collision harness" for the spec.
