# Findings Report Template

The user-facing output of an evaluation. Produce exactly one report per evaluation run.

**Delivery:** the report is printed inline to chat by default (no file write). If the user explicitly asks to save, write it to `skill-evaluation-{skill-name}-{YYYY-MM-DD}.md` at the workspace root — one file, never inside the target skill's folder, never a new directory. See "Artifact policy" in `SKILL.md` for the full rules.

**Before emitting the report, apply the rules in `references/terminal-ui.md`** — width budget, ASCII status symbols, grep-friendly leading tags, narrow tables. The template below already complies; if you customize, keep it terminal-clean.

## Structure

```markdown
# Skill Evaluation — {{skill name}}

Target:     {{path/to/SKILL.md}}
Tests run:  {{N}}
Mode:       {{stated-intent | live-execute}}
Date:       {{YYYY-MM-DD}}

## Summary

{{N_pass}}/{{N_total}} assertions passed across {{N_tests}} tests.

| Test           | Pass | Fail | ? |
|----------------|-----:|-----:|--:|
| 1. {{short…}}  |    x |    y | z |
| ...            |      |      |   |

### By fix layer

- [SKILL]   {{count}} failures  (actionable — skill-text diffs below)
- [RUBRIC]  {{count}}
- [BRIEF]   {{count}}
- [FIXTURE] {{count}}

Actionable skill fixes: {{skill_text_count}} (others are test-quality issues).

## Skill text findings (actionable)

One block per finding. Highest-priority first (by breadth of impact, not alphabetical).

---

### FINDING {{N}} — {{short title}}

Affected tests:  {{list of test numbers with the same tag}}
Tag:             [TAG]
Failure pattern: {{one sentence — what the executor did wrong, or what the skill didn't enforce}}
Root cause:      {{one sentence — why the skill text didn't land}}

Proposed rule-text diff:

File: `references/{{filename}}.md` (or `SKILL.md`)

```diff
  {{surrounding context lines}}
- {{line to remove or replace}}
+ {{new line}}
  {{surrounding context lines}}
```

Why this wording: {{one sentence — why the new text should produce different behavior. Tie to the observed failure.}}

---

## Test-quality issues (not skill problems)

Items here mean the test needs rework, not the skill.

### [RUBRIC]

- [TAG] (test {{N}}): {{one-sentence rewrite recommendation}}

### [BRIEF]

- Test {{N}}: {{one-sentence prompt-rewrite recommendation}}

### [FIXTURE]

- Test {{N}}: {{one-sentence context-to-add recommendation}}

## What passed well

Short paragraph or bulleted list. Call out tag-clusters where the skill performed reliably — this is useful to prevent regressions when editing the skill.

## Uncovered surface area

If the test set did not exercise some rules in the skill (and you noticed during Phase 1), list them here so the user knows this evaluation's coverage boundary.

## Next steps

1. Apply the proposed skill-text diffs (review each — they are suggestions, not mandates).
2. Rewrite the flagged rubric/brief/fixture items.
3. Re-run the evaluation (manually — skill-evaluator does not auto-iterate).
```

## Authoring guidance

### Lead with classification, not a single score

A headline like "skill passed 92%" hides the fact that all 8% of misses were on one critical rule. Structure the summary so the reader sees the fix-layer breakdown immediately.

### Diffs should follow `skill-creator` conventions

If `skill-creator` is available, follow its authoring rules when proposing diffs:

- Preserve frontmatter (`name`, `description`)
- Imperative voice ("Run the shutdown ritual" not "The shutdown ritual should be run")
- Explain the why (at least one sentence per rule)
- Keep SKILL.md under ~500 lines; push detail into `references/`

If `skill-creator` is NOT available, still apply these conventions — they're reasonable defaults even without the skill loaded.

### One finding per tag cluster

If `[SHUTDOWN]` failed in three different tests, produce ONE finding covering all three — not three separate findings. The skill text fix is the same; repeating inflates the report without adding signal.

### Keep the report one file

Do not split into multi-file output. The user should be able to skim the whole thing in one sitting. Aim for 500–1500 words depending on finding count.

### Do not recommend "add more rules"

If the skill's problem is that a rule is ignored, the fix is almost never "add another rule". It's usually "make the existing rule harder to skip" — move it earlier, add why, remove conditional escape hatches, inline the enforcement into a named checklist. Over-adding rules is how skills become bloated and self-contradicting.

### Mark low-confidence findings

If the failure pattern could plausibly be a rubric issue instead of a skill-text issue, say so. Give the user enough information to overrule your classification.

## Report anti-patterns

- **Pass-rate-only summaries.** Useless without the fix-layer breakdown.
- **"The skill should be clearer."** Not a diff. Propose specific text.
- **Listing every passing assertion.** Noise. Call out clusters, not individual passes.
- **Auto-iterating.** Stop after the report. Human gates round 2.
