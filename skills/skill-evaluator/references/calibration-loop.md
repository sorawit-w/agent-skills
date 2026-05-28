# Calibration loop — gold-standard + negative pair

Pattern adapted from [`GoogleChrome/modern-web-guidance-src`](https://github.com/GoogleChrome/modern-web-guidance-src) (Apache-2.0). Their eval harness uses it to prove that a grader actually tests the rule it claims to test, not a vacuous side effect. The same pattern transfers to skill audits.

## When this applies

Use when the target skill produces a **gradable artifact** — rendered output, generated file, structured response — and you want to prove that an assertion is non-vacuous before treating it as evidence. Examples in this repo: `pixel-art`, `pitch-deck`, `validation-canvas`, `ai-ux-review` and `ai-eval-review` HTML output, any future skill that emits HTML/SVG/JSON.

Does NOT apply to pure workflow skills (`team-composer`, `skill-evaluator` itself, `handshake`, `whoami`) — there is no rendered artifact to grade.

## The pattern

Every assertion the audit relies on is paired with two fixtures:

1. **Gold-standard fixture** — the artifact the skill is supposed to produce when it follows the rule correctly. Grader MUST pass.
2. **Negative fixture** — the same artifact deliberately broken on exactly the dimension the rule constrains. Grader MUST fail.

If the grader passes on the gold fixture AND fails on the negative, the assertion is calibrated — it actually tests the rule. If the grader passes on both (false-positive), the assertion is vacuous. If it fails on both, the assertion is wrong. Either failure mode is a Layer 2 (rubric) finding, not a Layer 1 (skill text) finding.

## Why this matters for adherence audits

Phase 3 of the workflow asks for 3–7 assertions per test. Without calibration, an assertion like "the executor produces accessible output" can pass on anything because the grader has no anti-example to disambiguate. With a negative fixture (e.g., the same artifact with `alt` attributes stripped), the grader has a clear discriminating signal.

The cost is real — each assertion needs a paired negative artifact — so the rule is **calibrate the rules you're treating as load-bearing**, not every assertion. Calibrate the assertion whose failure would change a release decision.

## Opportunity and uplift (measurement-only frame)

Modern Web Guidance also surfaces two metrics worth knowing about even though they're outside this skill's scope:

- **Opportunity** = `100% - unguided-pass-rate`. How much room there is for the skill to add value. Low opportunity = the model already does this well; the skill is not high-leverage.
- **Uplift** = `guided-pass-rate − unguided-pass-rate`. How much the skill actually improved the outcome.

This skill **does not measure** opportunity or uplift — that's `skill-creator`'s `run_eval` primitive. Surface the vocabulary in findings only when the user is debating whether a skill is worth its tokens; otherwise it's noise.

## Failure modes

| Failure | Symptom | Fix |
|---|---|---|
| Vacuous assertion | Grader passes on both gold and negative | Tighten assertion language or pick a different discriminator |
| Over-strict assertion | Grader fails on the gold fixture | Loosen — the assertion is testing more than the rule actually requires |
| Negative fixture too broken | Grader fails for the wrong reason | Break only the dimension the rule constrains; keep everything else valid |
| Calibration drift | Gold passes today, fails next month | Fixture pinned to a stale convention — refresh fixture, not the rule |

## Attribution

Pattern, terminology (gold-standard / negative / opportunity / uplift), and closed-loop validation framing adapted from `GoogleChrome/modern-web-guidance-src` — see their root `README.md` "Evals to prove this works well" section. Apache-2.0. Re-expressed here for skill-adherence audits rather than web-platform agent benchmarking; concrete authoring is this repo's own.
