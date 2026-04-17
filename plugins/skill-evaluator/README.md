# skill-evaluator

A Claude Code skill for auditing other skills — checks whether a skill's rules actually land when Claude runs it, and proposes targeted fixes when they don't.

## Why this exists

Skills are prompts dressed up as policy. You write rules, ship the skill, and hope Claude follows them. Usually most of the rules land. Sometimes the one that matters most doesn't — a risk-blocking role gets pruned, a required boundary check gets acknowledged but skipped, a "scrappy" framing in the user prompt silently compresses the team.

You don't find these failures by reading the skill. You find them by running it against prompts designed to expose the gaps, then grading the output against the rules — independently, without letting the grader peek at the skill text.

That's what this does.

## What it does

- Reads the target skill end-to-end — `SKILL.md` plus every file it references. A lot of rules live in reference files, and auditing `SKILL.md` alone misses 30–60% of the surface area.
- Generates 5–10 test prompts spanning happy paths, trigger edges, adjacent non-matches (to catch over-triggering), and rule-specific stress tests.
- Runs each test through a split-role harness: one sub-agent executes the skill; a separate sub-agent grades the output against a pre-written assertion list, without seeing the skill's text.
- Classifies every failure by fix layer: skill text, rubric, prompt framing, or fixture gap. Not every failure is the skill's fault, and conflating them leads to bad rewrites.
- Produces a findings report with proposed rule-text diffs for actual skill-text failures, formatted to read well in a terminal.
- Stops. Does not auto-iterate. The human decides what to land.

## What it doesn't do

- **A/B benchmark** (skill vs. no skill). That's what `skill-creator` is for.
- **Grade creative output.** "Is this logo beautiful?" is not a rule-adherence question.
- **Measure long-horizon outcomes** like engagement or retention.
- **Write files by default.** Everything renders in chat unless you explicitly ask to save — and then it's one file at the workspace root, never inside the skill folder.
- **Run round 2 on its own.** Each round surfaces calibration opportunities that get buried if the loop runs itself.

## When to use it

- You just wrote a skill and want to stress-test it before shipping.
- A skill has been "mostly working" but you suspect a rule is being silently skipped.
- You patched a skill and want a regression check on the failure mode you thought you fixed.
- You want to know whether a failure is a skill problem, a bad test, or a missing fixture — before rewriting anything.

## When not to use it

- You want a skill-vs-no-skill benchmark → use `skill-creator`.
- The skill has no testable rules (pure creative generation). The harness will run, but the findings will be noise.
- You need live execution with real side effects — proceed carefully. Default mode is stated-intent; switch to live-execute only for advisory skills with no destructive actions.

## How it works — 7 phases

1. **Read the target skill.** All of it, including every reference file.
2. **Clarify (≤3 questions).** Only if purpose, triggers, or success criteria aren't obvious from the skill text. Budget caps the workshop.
3. **Generate tests.** 5–10 prompts spanning happy/edge/adjacent/stress. 3–7 assertions per test, each independently gradable from the executor output alone.
4. **Split-role evaluation.** Executor runs the skill in fresh context. Grader judges the output in fresh context without seeing the skill text. This is the bias-avoidance design — the grader judges what Claude *did*, not what the skill *said to do*.
5. **Classify failures.** Four layers: skill text / rubric / brief framing / fixture scaffolding. Layers 2–4 are test-quality issues, not skill failures.
6. **Produce findings.** Grouped by fix layer, skill-text failures first. Proposed diffs follow `skill-creator`'s authoring conventions.
7. **Stop.** Hand the report to the human.

## What the output looks like

A single findings report, formatted for terminal reading — ASCII status symbols, grep-friendly leading tags, ≤80-column prose, no emoji or box-drawing Unicode. The report leads with a failure classification, not a headline pass rate. A 95% pass rate can hide the one critical rule that never fires.

For every skill-text failure, you get a proposed rule-text diff — not a vague "the skill should be clearer here," but specific before/after text you can land.

## Relationship to `skill-creator`

| skill-creator | skill-evaluator |
|---|---|
| Authors new skills | Audits existing skills |
| Benchmarks skill-vs-baseline (A/B) | Measures rule adherence under realistic prompts |
| Asks "does the skill help?" | Asks "does the skill's text actually land?" |
| Outputs: a skill | Outputs: findings + rule-text diffs |

The two chain naturally: evaluator finds a gap → creator's conventions guide the rule-text fix. `skill-creator` (Anthropic-shipped) is a recommended dependency; this skill works without it but will suggest installation when proposing diffs.

## Design choices worth knowing

- **Dry run by default.** The evaluator writes no files unless you ask. If the target skill lives in your mounted workspace, you can audit it without the harness ever touching the folder.
- **Split-role eval is non-negotiable.** If the same agent executes and grades, the grader is biased toward rewarding intent over behavior. Fresh grader context with only the assertion list forces evidence-based judgment.
- **Assertions ≠ scoring.** The report leads with failure classification, not a percentage. A pass rate is a weak signal; a classified failure list is an actionable one.
- **Layer-aware fix taxonomy.** Reflexively attributing every failure to the skill text produces over-written skills full of band-aids for test problems. Forcing the classification prevents that.

## Install

This skill is distributed as a [Claude Code](https://docs.claude.com/en/docs/claude-code) plugin inside the [`sorawit-w/agent-skills`](https://github.com/sorawit-w/agent-skills) marketplace. From Claude Code or Cowork:

```
/plugin marketplace add sorawit-w/agent-skills
/plugin install skill-evaluator@sorawit-w
```

Once installed, Claude picks the skill up automatically from the description in its `SKILL.md` frontmatter. Invocation triggers on phrases like "evaluate this skill," "audit a skill," "stress-test my skill," or "does this skill actually work."

## Status and scope

v1. The scope is intentionally narrow:

- **Supported:** workflow skills, rule-shaped skills, guideline skills.
- **Not supported:** creative-synthesis skills (brand voice, canvas design), skills whose value is measured by long-horizon user outcomes.

If asked to evaluate an out-of-scope skill, the evaluator says so explicitly and asks whether to proceed best-effort. It does not silently pretend to work.

## Contributions

Not accepting external contributions right now. Feel free to fork.

## License

MIT — see the [LICENSE](https://github.com/sorawit-w/agent-skills/blob/main/LICENSE) file at the repo root.
