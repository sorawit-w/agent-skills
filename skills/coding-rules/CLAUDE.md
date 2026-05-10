# Coding-rule revisions

**This CLAUDE.md is for *editing the rules*. It is not the rules themselves — those live in `resources/BOOTSTRAP.md` and the `resources/workflows/` and `resources/references/` files, and apply to ordinary coding work. The skill entry point is `SKILL.md` at the repo root, which loads `resources/BOOTSTRAP.md` into a session.**

## Eval handoff

Evaluation of rule changes is handled by the `skill-evaluator` skill (separate repo). coding-rules does not ship its own eval harness — one tool, one job.

When the user asks to:
- "audit coding-rules"
- "evaluate my change to <rule>"
- "test this rule revision"
- "run an eval on the new directive"
- "does this rule actually change agent behavior"
- "would this rule do anything"
- any natural-language variant of "is this rule effective"

→ **STOP.** Do not analyze the rule inline in your response.

Correct response:
1. Tell the user this is skill-evaluator territory and name the skill:
   "This is a `/agent-skills:skill-evaluator` job — it runs a split-role audit harness that removes author bias. Want me to invoke it?"
2. Wait for consent before proceeding.
3. If the user insists on inline analysis, remind them that inline grading in the same agent that wrote the rule is exactly what skill-evaluator is designed to avoid, then proceed only with explicit user override.

**Forbidden output shapes in this response:**
- "Finding 1/2/3" sections
- "Assessment" tables with enforceability / observability / impact columns
- Rule-text diffs as a recommendation (that's skill-evaluator's output, not rule-editing's)
- Anything that reads like a graded report

The distinction matters: rule editing happens here, rule grading happens in skill-evaluator. Do not collapse them.

## Change classes

| Change | Eval required? |
|--------|----------------|
| Typo / formatting | No |
| New directive, new prohibition, threshold shift, removal | Yes — via skill-evaluator |
| Change to safety, commit discipline, protected-branch rules, or secrets-handling | Yes, at a higher bar — see skill-evaluator's rubric |

---

## Rule-cost gate (precheck)

Before handing a proposed new rule to skill-evaluator, run this cheap inline check first. It is a **cost gate, not a behavior gate** — skill-evaluator handles the latter. The two are complementary: the cost gate decides whether a rule is worth evaluating at all; skill-evaluator decides whether an evaluated rule actually changes agent behavior.

Every rule added to coding-rules has persistent input-token cost — it loads on every session that consumes it. Many proposed rules do not pay back that cost. Before adding, answer:

1. **Cost.** How many lines does this rule add? (Line count is a fair proxy for recurring input tokens.)
2. **Frequency.** How often does the failure this rule prevents actually happen? (Once a quarter, or every session?)
3. **Severity.** When the failure happens, how bad is it without the rule?
4. **Coverage.** Is this already covered — directly or by reasonable inference — by an existing rule?
5. **Testability.** Can the agent itself check whether the rule was followed, without a human in the loop?

**Reject the rule if:** it duplicates existing coverage, the failure is rare *and* low-severity, or the rule is purely aesthetic (sentence-length caps, punctuation prohibitions, em-dash bans). Aesthetic rules are testable only by humans, which means agents won't self-enforce them and they bloat context for no behavioral payoff.

**Accept the rule if:** the failure is frequent or severe, no existing rule covers it, and the rule is testable by the agent itself. *"Did you run quality gates?"* is testable; *"did you write punchy prose?"* is not.

If the rule passes this gate, *then* proceed to skill-evaluator per the change-class table above. Skipping this precheck is allowed for typo/formatting changes (the change-class table already exempts them from eval).

---

## Authoring style — methodology over scripts

When drafting a new rule, prefer **methodology** (the approach the agent should take) over **scripts** (hardcoded commands or fixed sequences). The agent adapts methodology to whatever project it's in; scripts don't travel.

- Methodology: *"Verify before claiming done — run the project's quality gates and read the full output."*
- Script: *"Run `npm test && npm run lint && npm run build` before every commit."*

The script version breaks the moment the project uses Bun, pnpm, Deno, or a custom gate. The methodology version survives. This isn't a rule in `BOOTSTRAP.md` — it's guidance for the humans editing rules, which is why it lives here in `CLAUDE.md`. Zero runtime token cost.

Not absolute: when a rule genuinely requires a specific command (e.g., `git` invocations in the branching section), use it. The test is whether the command is load-bearing for the rule's meaning, or just the author's habit.

---

## Compression check against compact reference packs

When adding or revising a rule, sanity-check it against the four-principle compression in `forrestchang/andrej-karpathy-skills` (Think Before Coding / Simplicity First / Surgical Changes / Goal-Driven Execution). If your new rule restates one of those four principles in more words, you're paying recurring input tokens for a familiar idea — either compress it to fit alongside the existing rule, or drop it.

This is opportunistic, not periodic — fire it at the moment a new rule is being authored, not as a scheduled audit. Coding-rules grows; the compression discipline keeps growth honest. Zero runtime token cost (this section lives in the rule-editing context, not in `BOOTSTRAP.md`).
