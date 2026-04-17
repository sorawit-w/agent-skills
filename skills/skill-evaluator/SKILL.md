---
name: skill-evaluator
description: Audit a skill to see whether its rules actually land in practice. Use when you want to stress-test a skill, find gaps between what it says and what Claude does, validate rule adherence with a split-role eval harness, classify failures by fix layer (skill text / rubric / brief / fixture), and get proposed rule-text diffs. Triggers on "evaluate this skill", "audit a skill", "stress-test my skill", "does this skill actually work", "find gaps in this skill", "what's broken in this skill", "validate rule adherence", or uploading a SKILL.md and asking for a review of how it behaves. Complements `skill-creator` — use skill-creator to author/benchmark skills, use skill-evaluator to audit adherence and propose targeted fixes.
---

# Skill Evaluator

Audit a target skill to see whether its instructions actually land when Claude runs it. This skill does NOT benchmark skill-vs-no-skill (that's `skill-creator`'s job). This skill checks rule adherence under realistic prompts, classifies where failures come from, and proposes targeted fixes.

## Scope

**Good fit — v1 supports:**

- Workflow skills (sequences of steps, shutdown rituals, review passes)
- Rule-shaped skills (policies, conventions, constraints, checklists)
- Guideline skills (style guides, voice guides, design rules)

**Out of scope for v1 (say so explicitly if asked):**

- Creative-synthesis skills (brand voice, canvas design, algorithmic art) — rule-adherence framing does not apply cleanly to "is this output beautiful"
- Skills whose value is measured by end-user outcomes over time (engagement, retention)

If the user asks to evaluate a creative-synthesis skill, say the harness is not validated for that skill type and ask if they want to proceed anyway with a best-effort run. Do not silently pretend it works.

## Differentiation from skill-creator

| skill-creator | skill-evaluator |
|--|--|
| Authors new skills | Audits existing skills |
| Benchmarks skill-vs-baseline (A/B) | Measures rule adherence under realistic prompts |
| Asks "does the skill help?" | Asks "does the skill's text actually land?" |
| Outputs: a skill | Outputs: findings + rule-text diffs |

You can chain them: evaluator finds a gap → creator's conventions guide the rule-text fix.

## Dependencies

- **`skill-creator`** (Anthropic-shipped) — recommended. Used to enforce authoring conventions when you propose rule-text diffs. Suggest installation if the user doesn't have it.
- **User-authored orchestration skills** (e.g., `sub-agent-coordinator`) — not required. Opt-in only.

## Artifact policy

**Default: dry run.** The evaluator prints to chat and writes no files. This keeps the target skill's folder clean and the user's workspace untouched — especially important when the target skill lives inside the mounted workspace.

**Hard rules (no exceptions):**

1. **Never write inside the target skill's folder.** Not during the run, not for saving findings, not ever.
2. **Do not create directories at the workspace root by default.** No auto-created `_evaluation/` or similar folders. The workspace is the user's, not ours.
3. **Intermediate state lives in Claude's session sandbox only** — scratch space outside the user's workspace, cleared when the session ends. The user does not need to see or inspect it.
4. **Save only on explicit request.** If the user says "save the findings", "keep this report", or similar, write ONE file at the workspace root with a clear name: `skill-evaluation-{skill-name}-{YYYY-MM-DD}.md`. Never a folder. Never multiple files. Never inside the skill.
5. **Confirm the path before writing.** Example: "Saving to `skill-evaluation-coding-rules-2026-04-17.md` at your workspace root — confirm?"

**If the user also wants full traces** (executor output, grader output per test), treat it as a separate opt-in. Same filename convention: `skill-evaluation-{skill-name}-{YYYY-MM-DD}-traces.md`. Still one file, still at the workspace root.

**If no workspace is mounted:** tell the user, offer to keep the report inline so they can copy-paste it. Do not guess a save location.

## Workflow — 7 Phases

Run these phases in order. Do not skip Phase 2 even if the target skill looks obvious.

### Phase 1 — Read the target skill

Read the target `SKILL.md` in full. Then read every file it references (via `references/`, `assets/`, `scripts/`, or inline links). A skill's rules often live in reference files, not in SKILL.md itself — evaluating SKILL.md alone will miss 30-60% of the surface area.

Build a mental index:

- Purpose (from the description field and opening paragraph)
- Trigger phrases (from the description field)
- Rules / steps / constraints (the testable content)
- Explicit non-goals or "out of scope" sections

**Why this matters:** if you generate test prompts without reading the reference files, your assertions will miss rules that only live there. The evaluation will show false passes.

### Phase 2 — Clarify (≤3 questions, only if needed)

Ask the user targeted questions ONLY if the skill text does not make the following obvious:

1. **Purpose ambiguity** — what problem does this skill solve?
2. **Trigger ambiguity** — which kinds of requests should invoke it?
3. **Success criteria** — what does "working correctly" look like?

**Budget: 3 questions max.** If the skill text is clear on all three, skip this phase entirely.

**Why the budget:** fully autonomous evaluation compounds bad inference into bad tests → bad findings. Three questions is usually enough to avoid garbage-in-garbage-out without turning this into a workshop.

If the user gives a one-word skill name with no context and you cannot figure out the three items above from the skill text alone, ask all three at once (not sequentially).

### Phase 3 — Generate test prompts + assertions

Produce **5–10 test prompts** that span the skill's declared surface area:

- **Happy path** (2–3) — requests the skill's description directly matches
- **Edge cases** (2–3) — requests at the boundary of the trigger phrases
- **Adjacent non-matches** (1–2) — requests that *look like* they should trigger the skill but shouldn't, to check for over-triggering
- **Rule-specific stress tests** (1–2) — requests designed to make Claude violate a specific rule in the skill

For each test prompt, write **3–7 assertions** using the tag/sentence/evidence pattern (see `references/assertion-dictionary.md`). Every assertion must be independently gradable from the executor's output alone — no need for the grader to re-read the skill to judge it.

Output format:

```
test_N.md
---
## Prompt
<the user-facing prompt>

## Assertions
- [T1] The executor calls the shutdown ritual. Evidence: mention of "shutdown" or explicit QA sub-agent spawn.
- [T2] ...
```

### Phase 4 — Split-role evaluation

Run each test via two sub-agents with fresh context:

**Executor sub-agent**

- Receives: the test prompt + the target skill loaded
- Mode: **stated-intent** by default (describe tool calls with `-stated` suffix, don't actually execute). Switch to live-execute only if the skill under test is purely advisory (no side effects).
- Output: a single response showing reasoning, tool-call intents, and final deliverable

**Grader sub-agent**

- Receives: the test prompt, the executor's output, and the assertion list
- Does NOT receive the target skill's text (to avoid bias toward what the skill *says* over what the executor *did*)
- Output: per-assertion pass/fail with one-line evidence quote

**Why split roles:** having the same agent execute and grade introduces bias. Fresh grader context with only the assertion list forces evidence-based judgment. See `references/executor-brief.md` and `references/grader-brief.md` for the briefs.

### Phase 5 — Classify failures

For every failed assertion, classify the root cause using the four-layer fix taxonomy (see `references/fix-taxonomy.md`):

1. **Skill text** — the rule is missing, unclear, or contradicted elsewhere in the skill
2. **Rubric** — the assertion was wrong (unfair test, ambiguous criteria, or testing something the skill doesn't actually claim)
3. **Brief framing** — the test prompt itself was ambiguous or under-specified
4. **Fixture scaffolding** — the executor needed context (files, tool access) that wasn't provided

**Layers 2–4 are not skill failures.** A well-classified "this is a rubric problem" is useful — it means the skill is probably fine and the test needs rewriting. Don't reflexively attribute every failure to the skill text.

### Phase 6 — Produce findings report

Generate a single user-facing findings report using the template in `references/findings-report.md`. The report must include:

- Summary: X/Y assertions passed, per test
- Failed assertions grouped by fix layer (skill text first, since that's the actionable part)
- For each skill-text failure: proposed rule-text diff that follows `skill-creator`'s conventions (frontmatter preserved, imperative voice, explain-the-why, progressive disclosure)
- Rubric/brief/fixture items listed separately as "test-quality issues" (not skill issues)

**Format the report for terminal reading.** Readers will `cat` / `less` / `grep` this file as often as they open it in an IDE. Apply the rules in `references/terminal-ui.md` — ASCII status symbols, grep-friendly leading tags, ≤80-col prose, narrow tables, no emoji or box-drawing Unicode. One output, two readers — no separate "rich" mode.

**Deliver inline by default.** Print the report to chat. Do not write files. If the user asks to save, follow the rules in "Artifact policy" above: one file, workspace root, `skill-evaluation-{skill-name}-{YYYY-MM-DD}.md`.

### Phase 7 — Stop

Do not auto-iterate. Do not run round 2 on your own.

**Why:** the human should gate iteration. Each round surfaces calibration opportunities (re-scoping assertions, revising brief framing) that get buried if the loop runs itself. Hand the report to the user and wait.

---

## Assertions ≠ Scoring

This skill produces findings, not grades. A 95% pass rate can hide a single critical rule that never fires. A 60% pass rate with all misses in one rule area is actionable. Don't lead the report with a single headline number — lead with the failure classification.

## When to refuse

- Target skill is not a skill (SKILL.md missing or frontmatter malformed): refuse and point to `skill-creator`.
- Target skill has no testable rules (pure creative prompt with no constraints): warn the user this harness isn't designed for that; offer to proceed best-effort.
- User wants A/B benchmark (with-skill vs without-skill): point to `skill-creator`'s benchmark loop. That is not this skill's job.

## Reference files

- `references/assertion-dictionary.md` — tag/sentence/evidence pattern, examples, anti-patterns
- `references/executor-brief.md` — the executor sub-agent brief template
- `references/grader-brief.md` — the grader sub-agent brief template + independence rules
- `references/fix-taxonomy.md` — four-layer classification with examples
- `references/findings-report.md` — user-facing output template
- `references/terminal-ui.md` — lean-markdown output rules so reports read well in terminals and IDEs alike

Read these when the phase calls for them. Do not front-load all references at once.
