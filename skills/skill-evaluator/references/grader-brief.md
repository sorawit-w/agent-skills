# Grader Brief Template

The grader sub-agent evaluates the executor's output against the assertion list. The grader must NOT have access to the target skill's text — only the prompt, the executor output, and the assertions.

## Why independence matters

If the grader sees the skill's text, it will grade "did the executor follow the skill" instead of "does the executor's output satisfy the assertions". Those sound similar but diverge in practice:

- Skill text says "prefer simple solutions" → grader might pass a complex solution because "it's still allowed under the skill"
- Assertion says "the code uses a loop, not recursion" → grader judges this on the executor's output alone, no skill interpretation

The assertion is the rubric. The skill is not.

<!-- Future: this is tier=standard work (literal-match grading against assertions, no creative synthesis). When opt-in cost-tier routing lands, this brief is a one-line target for Haiku-class. Do NOT downgrade silently — surface as opt-in config per the cross-skill model-routing policy. -->

## The Brief

```
You are a grader sub-agent in a skill-evaluation harness. Your job: for each assertion, judge whether the executor's output satisfies it, based only on the output itself.

## Inputs

### Test prompt

{{the user-facing prompt, verbatim}}

### Executor output

{{the executor's full response, verbatim — include reasoning, tool-call intents, deliverable}}

### Assertions

{{assertion list from test_N.md, one per line}}

## Grading rules

1. Judge each assertion independently. Prior assertion results do not influence later ones.
2. Evidence must come from the executor's output. Do not infer based on what you think the skill says.
3. Pass requires affirmative evidence matching the assertion's evidence clause. Absence of counter-evidence is not pass.
4. If evidence is genuinely ambiguous, mark `unclear` and explain in one sentence. Do not guess.
5. You do NOT have access to the target skill's text. If an assertion references a skill rule you don't know, grade based on the assertion's literal claim, not on what you guess the rule says.

## Output format

For each assertion, output exactly one line:

```
[TAG] {pass | fail | unclear} — "<≤12-word evidence quote from executor output>"
```

Then a summary line:

```
TOTAL: <pass_count>/<total> pass, <fail_count> fail, <unclear_count> unclear
```

No other prose. No recommendations. Just the grades.
```

## Anti-instructions for the grader

- Do NOT propose fixes — that's for Phase 5, not the grader
- Do NOT re-grade if the executor "was close" — assertions are binary pass/fail/unclear
- Do NOT upgrade `unclear` to `pass` to be nice — unclear is a signal the assertion needs sharpening

## Handling `unclear` results

`unclear` is valuable. It usually means:

- The assertion evidence clause was vague (fix in rubric layer)
- The executor output was silent on the point (fix in brief-framing layer)
- The executor did the thing but implicitly (fix by making the assertion check for implicit signals too)

Never aggregate `unclear` into pass or fail in the summary counts. Report the three counts separately.

## Fresh context per test (mandatory)

Each test gets its own grader sub-agent invocation with fresh context. Do NOT batch multiple tests into a single grader run, and do NOT reuse a grader sub-agent across tests.

**Why:** when the same grader runs many tests in a row, drift sets in (getting stricter or looser over time), and prior assertions contaminate later judgments. The split-role design only delivers its bias-avoidance guarantee when each grading event is independent.

This invariant mirrors the executor's "one prompt, one executor" rule. If the orchestrator cannot guarantee fresh context per test (e.g., platform constraint), say so explicitly in the findings report rather than silently sharing context.

## High-stakes mode — optional second-grader quorum

A second grader is **opt-in**, not the default. Cost roughly doubles when enabled (2× grading invocations per test), so reserve it for cases where a single grader's judgment is load-bearing.

**Trigger when ANY of these apply:**

- User explicitly requests ("high-stakes audit", "double-check the grading", "verify findings", "second-grader pass")
- The audited skill gates a release in a regulated domain (finance, health, children, etc.)
- A failed assertion would block ship/merge of safety-critical work
- ≥30% of grader-1's verdicts came back `unclear` on first pass — signal that judgment is brittle

**How it works:**

1. Run grader-1 normally per the brief above.
2. Spawn grader-2 with the SAME inputs (test prompt, executor output, assertion list), fresh context, no knowledge of grader-1's verdicts. Same brief, same anti-instructions.
3. Compare per-assertion judgments:
   - **Both agree (pass+pass or fail+fail)** → take the agreed verdict.
   - **One `pass` + one `fail`** → demote to `unclear`. Surface both evidence quotes in the findings report under a "Disputed assertions" section so the human can adjudicate.
   - **One verdict + one `unclear`** → take the `unclear`. Disagreement signals the assertion is too fuzzy (rubric-layer fix in Phase 5).
   - **Both `unclear`** → `unclear` stands.
4. Do NOT add a third grader as tiebreaker. Disagreement IS the signal that the rubric needs sharpening, not that we need more graders. A 2-of-3 majority would launder a fuzzy assertion as confidently `pass`/`fail` and defeat the purpose.

**What changes in the brief itself:** nothing. Both graders run the exact same brief in fresh context. The asymmetry is at the orchestrator, not in the grader's instructions.

**Reporting:** findings report adds a "Grading mode: single | quorum" line near the top, and a "Disputed assertions" subsection if any disagreements arose. If single-mode was used despite a trigger condition firing, surface that as a process note so the user knows the cheaper path was taken.
