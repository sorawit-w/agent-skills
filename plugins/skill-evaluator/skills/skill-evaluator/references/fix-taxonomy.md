# Fix Taxonomy

Every failed assertion gets classified into one of four layers. The layer determines what to fix — and whether the skill itself actually failed.

## The Four Layers

### 1. Skill text

The skill's rules are missing, unclear, contradicted, or buried. This is the only layer where "the skill failed".

**Signals:**

- The skill does not state the rule the assertion is testing
- The skill states the rule but in a place the executor wouldn't naturally reach (deep in a reference file with no pointer from SKILL.md)
- Two parts of the skill disagree
- The rule is stated but without *why*, so executors skip it when it feels inconvenient
- The rule is conditional ("if complexity is high, run shutdown") and the condition is gameable

**Fix shape:** a rule-text diff. Add, clarify, move, or remove the relevant text in SKILL.md or references/.

**Example:**

> Assertion: `[ENV-PLACEHOLDER] .env.example contains no service-specific prefixes`
> Executor output: `STRIPE_SECRET_KEY=sk_test_placeholder`
> Classification: skill text. The skill did not state the placeholder policy explicitly.
> Fix: add an explicit `.env.example` policy block with allowed/disallowed shapes.

### 2. Rubric

The assertion itself was wrong. The executor did the right thing; the test was unfair.

**Signals:**

- The assertion tests something the skill does not actually claim
- The evidence clause is vague enough that reasonable graders would disagree
- The assertion bundles multiple checks into one line (should have been split)
- The assertion requires the grader to re-read the skill

**Fix shape:** rewrite the assertion in `test_N.md`. Do not edit the skill.

**Example:**

> Assertion: `[CLEAN-CODE] The code is clean and maintainable`
> Classification: rubric. "Clean" is not gradable from output alone.
> Fix: replace with specific assertions like `[NO-DEAD-CODE] No commented-out code blocks in the diff`.

### 3. Brief framing

The test prompt itself was ambiguous. The executor reasonably went a different direction than the assertion expected.

**Signals:**

- The prompt had two plausible interpretations and the executor picked the other one
- The prompt was missing context the skill normally assumes (e.g., "review this PR" with no PR linked)
- The prompt accidentally triggered an adjacent skill instead

**Fix shape:** rewrite the prompt. Add missing context or disambiguate.

**Example:**

> Prompt: "Write some tests for my code."
> Executor: wrote unit tests.
> Assertion expected: integration tests.
> Classification: brief framing. The prompt did not say which kind.
> Fix: rephrase as "Write integration tests (not unit tests) for the `UserService`."

### 4. Fixture scaffolding

The executor needed something to exist — a file, a directory structure, tool access — that wasn't provided. It failed because the environment was incomplete, not because the skill's rules were wrong.

**Signals:**

- Executor said "I need to see X first" and stopped
- Executor hallucinated file contents because the file wasn't given
- Executor tried to use a tool that wasn't in its allowed set

**Fix shape:** add fixture context to the test brief — include the file, describe the directory, enumerate available tools.

**Example:**

> Prompt: "Run the shutdown ritual on this project."
> Executor: "I don't see a test runner configured. Please confirm how tests are run."
> Classification: fixture scaffolding. No project files were attached.
> Fix: include a minimal sample project structure in the brief.

## Classification decision order

When a failure is hard to classify, run this order:

1. **Did the prompt itself cause the detour?** → brief framing
2. **Did the executor lack needed context?** → fixture scaffolding
3. **Is the assertion itself defensible?** → if no, rubric
4. **If all three above are clean, it's the skill.** → skill text

Do not default to "skill text" without first ruling out 2–4.

## Why this matters

**Layer 1 failures are the only actionable skill problems.** The other three layers are test-quality issues. Treating them as skill problems leads to over-editing the skill with rules that try to compensate for bad tests — bloat, not clarity.

A useful findings report often shows something like:

- 4 skill-text failures (actionable, propose diffs)
- 3 rubric issues (rewrite assertions, don't touch skill)
- 2 brief-framing issues (rewrite prompts, don't touch skill)
- 1 fixture issue (add sample data, don't touch skill)

This separation is the main reason the harness is worth running. Without it, every failure looks like a skill failure and the skill grows into a sprawling rulebook that contradicts itself.

## Recording the classification

In the findings report, each failed assertion gets one of: `[SKILL]`, `[RUBRIC]`, `[BRIEF]`, `[FIXTURE]`. Propose fixes only for `[SKILL]` — the others list the recommended test-quality action in one sentence.
