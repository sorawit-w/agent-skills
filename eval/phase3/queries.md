# Phase 3 trigger-collision eval set

Stratified 20-query corpus to measure cross-firing between our `skill-evaluator`
and Anthropic's `skill-creator`. Scored independently by `run_eval.py` against
each skill (queries.evaluator.json and queries.creator.json have the same
queries with mirrored labels).

## Group A — skill-evaluator positives (6)

A1. "Can you audit my pptx skill for rule adherence?"
A2. "Stress-test this SKILL.md and find gaps between what it says and how Claude actually behaves."
A3. "Does this skill actually work the way its description claims? I want a behavioral audit."
A4. "I need you to validate rule adherence in my docx skill — show me where the rules and behavior diverge."
A5. "Find what's broken in this skill — it's not triggering reliably and I don't know why."
A6. "Review my skill end-to-end and tell me what's wrong with how it actually behaves vs the rules I wrote."

## Group B — skill-creator positives (6)

B1. "Help me create a new skill from scratch for PDF annotation."
B2. "I want to optimize my skill's description for better triggering accuracy."
B3. "Build me a skill that summarizes Slack threads."
B4. "Can you benchmark my skill and report variance across multiple runs?"
B5. "Run an eval on my skill to measure trigger performance."
B6. "Make a new skill for processing CSV files into reports."

## Group C — ambiguous (4)

C1. "My skill isn't working right — can you help?"
C2. "I want to improve my skill."
C3. "Check this SKILL.md."
C4. "Make my skill better at triggering."

## Group D — unrelated (4)

D1. "Translate this UI string set to Thai."
D2. "Write a blog post about AI alignment trends."
D3. "Debug this Python traceback for me."
D4. "What's on my calendar today?"

## Labeling convention

For `queries.evaluator.json`:
- Group A → `should_trigger: true`
- Groups B, C, D → `should_trigger: false`

For `queries.creator.json`:
- Group B → `should_trigger: true`
- Groups A, C, D → `should_trigger: false`

A "collision" surfaces as: a Group B query that fires skill-evaluator (false positive
in evaluator eval) OR a Group A query that fires skill-creator (false positive in
creator eval). Group C/D are pure precision tests — neither skill should fire.
