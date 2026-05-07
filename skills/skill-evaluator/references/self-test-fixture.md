# Self-Test Fixture (maintainer-only)

A pair of tiny fixture skills — one known-good, one known-broken — that the harness audits before every release of `skill-evaluator`. The point is to catch regressions in the harness itself: false passes, false fails, wrong fix-layer classifications, drift in the briefs.

This is not part of the user-facing 7-phase workflow. End users should never see or run this. It's the harness eating its own dogfood.

## When to run

- Before bumping `skill-evaluator`'s plugin version
- Before merging changes to any of: `SKILL.md`, `references/executor-brief.md`, `references/grader-brief.md`, `references/fix-taxonomy.md`, `references/findings-report.md`
- After any change to the assertion-dictionary tag vocabulary
- Whenever a real audit produces a finding that "feels wrong" — re-run the fixtures to confirm the harness still calibrates

## How to run

Treat each fixture as an ordinary target skill. Invoke `skill-evaluator` against it the same way a user would. Compare the resulting findings report to the expected verdicts pinned below. Any deviation blocks release.

Run both fixtures. Do not stop after the known-good passes — half the regressions only show up on the broken one.

## Fixture A — known-good

A minimal skill with one unambiguous, gradable rule. The harness should classify all assertions as `pass`.

### Fixture skill text

```markdown
---
name: list-formatter
description: >
  Format a sequence of items as either a bullet list or inline prose, depending on count.
  Trigger ON: "format these items", "turn this into a list", "should this be bullets".
---

# List Formatter

When asked to format a sequence of items:

- **3 or more items** → render as a bullet list, one item per line, each line starting with `- `.
- **2 or fewer items** → render inline as prose using "and" between the last two items.
  Example: "apples and oranges" — never `- apples\n- oranges`.

The count rule is hard. Never bullet a 2-item list. Never inline a 4-item list.
```

### Test prompts to generate

The harness should generate prompts including at least:

1. **Happy (3+ items):** "Format these items: red, green, blue, yellow."
   Expected executor output uses bullets.
2. **Happy (2 items):** "Format these: cats, dogs."
   Expected executor output: "cats and dogs" — inline prose, no bullets.
3. **Edge (exactly 3):** "Format these: a, b, c."
   Expected: bullets (3 is the threshold).
4. **Adjacent non-match:** "Should I use bullets in my essay?"
   Expected: skill should NOT trigger (it's about formatting *given* items, not advice).

### Expected harness verdict

- All assertions: `pass`
- Failure classification section: empty
- No `unclear` results
- Findings report does NOT propose any rule-text diffs

**If the harness reports any failures on Fixture A, the harness is broken.** Most likely culprits: grader saw the skill text and over-interpreted, or the assertion dictionary regressed.

## Fixture B — known-broken

The same skill, but with one rule deliberately contradicted in a reference file. The harness should detect the contradiction and classify it as a **skill-text** failure.

### Fixture skill text

```markdown
---
name: list-formatter-broken
description: >
  Format a sequence of items as either a bullet list or inline prose, depending on count.
  Trigger ON: "format these items", "turn this into a list", "should this be bullets".
---

# List Formatter (broken fixture)

When asked to format a sequence of items:

- **3 or more items** → render as a bullet list, one item per line.
- **2 or fewer items** → render inline as prose using "and" between the last two items.

See `references/style.md` for additional formatting rules.
```

### Fixture reference file (`references/style.md`)

```markdown
# Style notes

For consistency across the product, **always use bullet lists regardless of item count**. Two-item lists should also be bulleted to keep visual rhythm uniform.
```

### The planted bug

`SKILL.md` says "2 or fewer items → inline prose, never bullets." The reference file says "always bullet, including 2-item lists." The two contradict. An executor reading both will be inconsistent depending on which it weights more.

### Test prompts to generate

Same as Fixture A. The 2-item case is the discriminator.

### Expected harness verdict

- 2-item happy-path assertion: `fail` OR `unclear` (depending on which rule the executor weighted)
- Failure classification: **skill-text layer** (not rubric, not brief, not fixture)
- Proposed rule-text diff: should resolve the contradiction — either delete the conflicting line in `references/style.md`, or strengthen `SKILL.md` to declare itself canonical when references conflict

**If the harness misclassifies this as a rubric failure** ("the assertion was wrong"), the fix taxonomy in `references/fix-taxonomy.md` has regressed. Skill-text contradictions are the load-bearing case for the taxonomy.

**If the harness reports `pass` on the 2-item case**, the grader is being too lenient or the executor is silently dropping the contradiction. Re-check `references/grader-brief.md` independence rules and the executor's specificity requirement.

## Pinned verdicts (do not edit casually)

| Fixture | Total assertions | Expected pass | Expected fail | Expected unclear | Expected fix-layer |
|---------|-----------------:|--------------:|--------------:|-----------------:|--------------------|
| A (good) | ≥12 (across 5–10 prompts × 3–7 assertions) | all | 0 | 0 | (none) |
| B (broken) | ≥12 | most | ≥1 (the 2-item case) | 0–1 | skill-text |

These are tolerances, not exact counts — the test-prompt generator is non-deterministic. The signal you watch for is the *shape*: A clean, B fails on the planted contradiction with skill-text classification.

## When the fixtures themselves drift

If real-world audits keep finding bug shapes the fixtures don't cover, expand the fixtures. Likely directions:

- A second known-broken fixture for **rubric-layer** false-positive (an assertion that *looks* like a skill bug but isn't) — confirms the taxonomy doesn't over-blame the skill
- A fixture for **brief-framing** layer (ambiguous test prompt) — confirms the harness can tell "the test was bad" from "the skill was bad"
- A fixture for **fixture-scaffolding** layer (executor needed context that wasn't provided)

Add these only when a real audit surfaces the shape — don't pre-build them. Premature fixtures rot.

## What this fixture deliberately does NOT cover

- **Creative-synthesis skills.** v1 of `skill-evaluator` declares those out of scope; the fixtures match.
- **Cross-skill collisions.** That's the v2 paired-skill collision harness (deferred per `SKILL.md` roadmap), not v1.
- **Live-execute mode.** Both fixtures are advisory and run in stated-intent. Adding a live-execute fixture would require sandboxed side effects — out of scope for v1.
