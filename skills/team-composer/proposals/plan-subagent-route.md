# Proposal: Phase 6.6 — Structural Plan Review via `Plan` subagent

**Status:** Draft, not merged into `SKILL.md`.
**Author:** drafted in conversation, 2026-04-26.
**Scope:** Add a narrow, optional route that hands `@staff_engineer`'s draft Structured Plan to the built-in `Plan` subagent for a *structural rigor pass*, then folds the critique back in for `@staff_engineer` to finalize. Mirrors the shape of Phase 6.5 (External Audit) so it slots in cleanly.

---

## Why a new phase, not a new Phase 6 trigger

Phase 6's existing rows are about **producing deliverable content** in parallel (architect → system design doc, backend → API spec). The plan-review case is different: the artifact already exists in draft, and we want a **structural critique** — not a parallel rewrite. Treating it as another Phase 6 row would muddle the "production vs. review" distinction.

Phase 6.5 already has the right shape for "fresh-context sub-agent reviews the team's output and returns a structured critique." This proposal is Phase 6.5's sibling: same shape, different review lens (plan rigor vs. blind-spot audit).

Keeping them separate lets each run independently — a high-stakes regulated build can trigger both; a routine high-complexity plan triggers only this one.

---

## Trigger conditions

Two-stage rollout. Ship conservatively, lower the threshold after observation.

**Stage 1 (launch):**

```
trigger Phase 6.6 if ALL of:
  - @staff_engineer is on the team (i.e., Phase 5 produced a Structured Plan)
  - scope in [planning, building]
  - complexity = high
  - Agent-tool sub-agent spawning is available  (same gate as Phase 6 / 6.5 fallback)
  - the Plan subagent type is registered in this runtime
```

**Stage 2 (after Plan-subagent cost/latency are proven in practice):** lower the floor to `complexity >= medium`. "Proven" means observed across enough real runs to confirm: median latency adds <30s to total run time, median tokens <2k per review, and at least 60% of runs surface ≥1 actionable finding. Until those signals hold, stay at Stage 1.

Optional opt-in trigger (lower threshold):

```
trigger Phase 6.6 if user explicitly says any of:
  "tighten the plan" / "is this plan rigorous?" / "stress-test the plan" /
  "make this agent-executable" / "Plan-review this"
```

Explicitly **do not** gate on "the orchestrator is Claude." It's neither necessary (Plan subagent works wherever the Agent tool is wired) nor reliably detectable from inside a skill. Gate on **capability**, not **vendor identity**.

### When NOT to trigger

- `complexity` ∈ {low, medium} — `@staff_engineer` in-context is enough; a sub-agent round-trip costs more than it returns.
- `scope` ∈ {discussion, review} — no Structured Plan exists to review.
- `@staff_engineer` is absent (Phase 2 chose not to seat them) — there's no plan-as-artifact to send.
- The team already triggered Phase 6 per-role fan-out AND total token budget for the run is constrained — defer to user opt-in instead of auto-firing.

---

## Phase placement in the run

```
Phase 4: Discussion
Phase 5: Conclude (writes Structured Plan via @staff_engineer)
Phase 6: Deliverable production fan-out  [if triggered]
Phase 6.5: External audit                [if triggered]
Phase 6.6: Structural Plan Review        [if triggered]   ← NEW
Final synthesis: present plan + audit findings + plan-review folded edits
```

6 → 6.5 → 6.6 ordering matters: Phase 6 may revise the plan with per-role specifics; Phase 6.5 may surface blind spots that change the plan; only after both does the plan stabilize enough to be worth sending to `Plan` for structural review. Running 6.6 too early wastes the call.

---

## What `Plan` is asked to do

`Plan` is **a reviewer with a fixed checklist**, not a co-author. The contract is asymmetric on purpose: `@staff_engineer` keeps authorship, `Plan` returns a structured critique.

### Brief template

```markdown
You are reviewing a Structured Plan authored by @staff_engineer for an agent-executable
implementation. Your job is to identify structural weaknesses that would cause an
executing agent to guess, drift, or stall. You are NOT rewriting the plan.

**Original user brief:**
[paste the original request verbatim]

**Team conclusion (Phase 5):**
- Recommendation: [paste]
- Decisions Made: [paste]
- Trade-offs Identified: [paste]

**Draft Structured Plan to review:**
[paste the full Structured Plan from Phase 5]

**Review against this checklist — return findings as a numbered list:**

1. **Decisions locked vs. deferred** — Is anything in "locked" actually still ambiguous?
   Is anything in "deferred" actually decidable from the discussion?
2. **Assumptions** — Are any load-bearing assumptions un-flagged? Any flagged assumption
   that has no verification step before phase 1?
3. **Phase boundaries** — Does each phase have a single, observable acceptance criterion?
   Flag criteria that are vague ("works correctly", "user-friendly") or untestable
   without human judgment.
4. **Files/modules** — Are concrete paths named, or only abstract areas? An executing
   agent should not have to guess which file to edit.
5. **Dependencies** — Any phase that depends on a deferred decision without a checkpoint?
   Any cycle (phase N depends on phase M output that depends on phase N)?
6. **Out-of-scope ring-fence** — Is the boundary tight enough to prevent drift, or so
   tight that a reasonable agent will hit a wall and stop?
7. **Risks flagged for human decision** — Any risk that should pause execution but is
   currently inline? Any "risk" that is actually a deferred decision in disguise?
8. **Agent-executability** — Could an agent (Claude Code, etc.) execute Phase 1
   end-to-end without a clarifying question? If not, name the specific gap.

**Output shape:**

For each finding:
- **Section:** [which Structured Plan section]
- **Issue:** [one sentence]
- **Why it matters:** [one sentence — what an executing agent would do wrong]
- **Suggested edit:** [concrete proposed text or change — not a rewrite of the section]
- **Severity:** blocker | major | minor

End with an overall verdict: `ready-to-execute` | `needs-tightening` | `needs-rewrite`.

Tool budget: ~8 calls. Read-only — do not modify the plan.
```

---

## Fold-back protocol

`Plan`'s critique returns to `@staff_engineer`, who:

1. **Triages each finding** by severity. Blockers must be addressed; majors should be addressed unless rejected with a recorded reason; minors are optional.
2. **Edits the Structured Plan in place.** No diff, no separate "v2" — the Structured Plan in the final output is the post-review version.
3. **Records rejections in the plan itself.** If `@staff_engineer` rejects a `Plan`-suggested edit, note it under a new bullet at the bottom of the Structured Plan: `**Plan-review notes:** [finding] rejected because [reason].` Auditability lives with the artifact — if the plan moves, the rationale moves with it. Rejected findings are visible to the user without prompting; the user-facing one-liner in the final output points to that section.
4. **Re-runs Post-Discussion Verification** (the existing checklist in `SKILL.md`). If the critique exposed a Phase 5 structural gap (e.g., missing trade-off section), fix that too.

The user-facing output **does not show `Plan`'s raw critique**. They see the finalized plan plus a one-line note: `Structural review by Plan subagent: <verdict>. <N> findings folded in.` If they want to see the raw critique, they can ask.

---

## Failure modes & guardrails

| Failure mode | Guardrail |
|---|---|
| `Plan` rewrites instead of critiquing | Brief explicitly says "you are NOT rewriting the plan." Output shape forces per-finding atomicity. If the response looks like a rewrite, discard and re-prompt once with the constraint repeated. |
| `Plan` returns trivial nits, hides real issues | Severity field forces ranking. If all findings are `minor`, accept verdict and move on. If all findings are `blocker`, flag for human review — `Plan` may have misunderstood the brief. |
| Token budget blowout from 6 + 6.5 + 6.6 all firing | Hard ordering (6 → 6.5 → 6.6) ensures each runs against a stable input. If overall run token budget is hit, 6.6 is the first to drop (blind-spot audits matter more than structural rigor for high-stakes work). |
| Runtime doesn't expose `Plan` subagent | Same fallback as Phase 6: skip the phase, note in output `Structural review skipped: Plan subagent not available in this runtime.` Do not synthesize a fake review in-context — that's confirmation bias. |
| User opts out mid-run | `Plan-review this` was opt-in; absence of the trigger means absence of the phase. No re-prompt needed. |

---

## What this changes in `SKILL.md`

If accepted, the merge is small and additive:

1. **New section after Phase 6.5**, titled `## Phase 6.6: Structural Plan Review (Plan Subagent)`. Mirrors 6.5's structure: trigger table, "How It Works" steps, brief template, fallback.
2. **One line in the Phase 6 trigger table cross-referencing 6.6**: `| Plan-review needed (see Phase 6.6) | Optional structural critique pass on @staff_engineer's draft, not a content fan-out |` — to prevent future contributors from confusing the two patterns.
3. **One line in `Cross-Skill Integration`**: `- **Plan subagent (built-in)**: Phase 6.6 hands the Structured Plan draft to the Plan subagent for structural review. Skipped if the Plan subagent type is not registered in the runtime.`
4. **No changes to Phases 1–5** — discussion, scoring, conclusion, and Structured Plan shape stay identical.
5. **No changes to `selection-algorithm.md` or `role-personas.md`** — `@staff_engineer` is still the in-context plan author; their persona, tensions, and signature phrases don't change.

Estimated diff: ~80 lines added to `SKILL.md`, no deletions, no edits to other files.

---

## Resolved decisions (2026-04-26)

1. **Rejected findings live in the plan itself** — see fold-back step 3 above. Not gated behind "ask to see it."
2. **Two-stage trigger threshold** — launch at `complexity=high`; lower to `complexity >= medium` once latency, token, and finding-yield criteria are met. See trigger conditions section for the gating signals.
3. **Phased-Launch Variant support is deferred.** The variant's structural shape (`Phase 1 (MVP) / Gating criteria → Phase 2 / Deferred`) would require a checklist tweak in the brief. Defer until a regulated/phased-launch run is observed in practice — premature support adds branching in the brief without evidence it's needed.
4. **Eval coverage is in scope.** Add cases to `evals/evals.json` (sketch below).

## Future enhancements (deferred)

- **Phased-Launch Variant review path.** Add a second brief template branch when the team produces the variant shape from Phase 5. Trigger when both Phase 6.6 fires AND the conclusion uses the variant. Defer until observed in real runs.
- **Stage 2 threshold lowering.** See trigger conditions — gated on observed cost/latency/yield from Stage 1 runs.

## Eval coverage

Add to `evals/evals.json`:

| Case | Setup | Assertion |
|---|---|---|
| `phase_6_6_fires_high_complexity_planning` | scope=planning, complexity=high, @staff_engineer present, Plan subagent registered | Phase 6.6 runs; final output includes the `Structural review by Plan subagent: <verdict>` one-liner |
| `phase_6_6_skips_low_complexity` | scope=planning, complexity=low | Phase 6.6 does NOT run; no review one-liner in output |
| `phase_6_6_skips_no_staff_engineer` | scope=building, complexity=high, @staff_engineer absent (e.g., trivial scope exception) | Phase 6.6 does NOT run |
| `phase_6_6_skips_no_plan_subagent` *(deferred — needs fixture support)* | scope=planning, complexity=high, Plan subagent NOT registered | Phase 6.6 is skipped with the documented fallback note. **Not shipped in evals.json**: the current eval format is prompt+assertion only, so simulating "Plan subagent unavailable" requires runtime fixture support that doesn't exist yet. Track as a manual test until fixtures land. |
| `phase_6_6_user_opt_in_lowers_threshold` | scope=planning, complexity=medium, user says "tighten the plan" | Phase 6.6 runs (opt-in path bypasses Stage-1 floor) |
| `rejected_finding_recorded_in_plan` | Phase 6.6 runs, @staff_engineer rejects ≥1 finding | The Structured Plan in final output contains a `**Plan-review notes:**` line with the rejection reason |
