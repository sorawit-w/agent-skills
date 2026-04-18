# Assertion Dictionary

How to write assertions that a grader can evaluate from executor output alone, without re-reading the target skill.

## The Tag / Sentence / Evidence Pattern

Every assertion has three parts:

```
- [TAG] <one-sentence claim about executor behavior>. Evidence: <where the grader should look, stated concretely>.
```

**Tag** — short stable handle (e.g., `[SHUTDOWN]`, `[ENV-PLACEHOLDER]`, `[NO-MOCKS]`). Reused across tests so you can aggregate "tests that touched the SHUTDOWN rule".

**Sentence** — one declarative claim. Not a question. Not a list. If you need "and" more than once, split into two assertions.

**Evidence** — where the grader should look. Be concrete: "mention of X", "presence of `-stated` suffix", "file path starting with `/tmp/`", "absence of mock.patch". Vague evidence like "the response is correct" makes grading subjective.

## Good Examples

```
- [SHUTDOWN] The executor runs the shutdown ritual before declaring done. Evidence: either an explicit QA sub-agent spawn, or a build/lint/test run mentioned in the final steps.
- [ENV-PLACEHOLDER] The `.env.example` values contain no service-specific prefixes. Evidence: no strings matching `sk_`, `AKIA`, `ghp_`, `xoxb-` in the proposed file contents.
- [NO-MOCKS] The test plan does not mock the database. Evidence: no `mock.patch` or `Mock()` targeting DB connections in the test code block.
- [STATED-INTENT] The executor uses `-stated` suffix tags for tool calls. Evidence: tool names end in `-stated` (e.g., `Bash-stated`, `Write-stated`).
```

## Anti-Patterns (Don't Do This)

**Compound assertions** — "The executor runs tests AND lints AND commits." Split into three.

**Opinion-shaped assertions** — "The code is clean." Not gradable. Replace with "no commented-out code blocks in the diff".

**Re-skill-reading assertions** — "The executor follows rule 3.2 of the skill." Forces the grader to re-read the skill, which defeats the split-role design. Inline the rule: "The executor wraps SQL in parameterized queries."

**Negations without scope** — "The executor does not call external APIs." Add scope: "...within the test-runner phase."

**Tautologies** — "The executor responds to the prompt." Too generic to fail.

## Coverage Heuristics

Per test prompt, aim for 3–7 assertions. Distribute roughly:

- **1–2 positive assertions** — behavior that should happen
- **1–2 negative assertions** — behavior that should NOT happen (to catch over-reach)
- **1–2 rule-specific assertions** — targeting the specific rule the test is stressing

If you write 10+ assertions for a single prompt, you're probably testing too many rules at once. Split into two prompts.

## Cross-Test Tag Consistency

When the same rule shows up in multiple tests, reuse the tag:

- Test 1: `[SHUTDOWN]` in happy path
- Test 3: `[SHUTDOWN]` in edge case
- Test 5: `[SHUTDOWN]` in adjacent non-match (here as a *negative* assertion: shutdown should NOT fire when the task is read-only)

Tag consistency lets you aggregate per-rule pass rates in the findings report, which is often more actionable than overall pass rate.

## Evidence That Travels

Grader only sees: the prompt, the executor's output, the assertion list. Evidence phrasing must survive that handoff. If the evidence says "check whether the approach matches our team's convention", the grader cannot verify it. Rewrite: "the proposed code uses `camelCase` variable names".

Rule of thumb: if the evidence requires the grader to know anything beyond the executor's output, the assertion is not independently gradable.
