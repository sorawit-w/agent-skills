---
name: skill-evaluator
description: >
  Audit an existing SKILL.md for rule adherence — does the text actually land when Claude runs
  it? Use when the user wants a behavioral review of a shipped skill. Outputs: failure
  classification by fix layer (skill text / rubric / brief / fixture) and targeted rule-text
  diffs. Trigger ON: "audit this skill", "stress-test my skill", "does this skill actually
  work", "find gaps in this skill", "what's broken in this skill", "validate rule adherence",
  "review this skill end-to-end", or uploading a SKILL.md for behavior review. Do NOT trigger
  on: "build a skill", "create a skill from scratch", "benchmark this skill", "evaluate skill
  quality", "compare versions", "optimize trigger phrases", or "measure variance" — those are
  all `skill-creator`. If the request mixes both, start with `skill-creator` and chain here.
  Hard boundary: `skill-creator` builds, benchmarks, measures variance, and optimizes
  triggering; this skill does NONE of those — it asks "does the text land?".
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

## Harness lens — what to audit beyond rule adherence

Rule-adherence audits catch *whether the agent follows what the skill says*. The **harness lens** catches a different class of failure: *whether the skill is shaped right in the first place*. Run these eight questions in addition to (not instead of) the standard adherence checks. They're cheap; one or two will usually surface a real issue.

1. **Does the skill name its primitives?** A well-shaped skill is explicit about which of the five harness primitives it serves: context engineering, progressive disclosure, observable feedback loops, state preservation, eval discipline. If the skill mixes all five implicitly, it probably has a scope problem. Flag: "Skill doesn't name what kind of work it's doing for the agent."
2. **Progressive disclosure or front-loaded?** Is the SKILL.md body trying to be the encyclopedia, or is it a map that points to `references/` for detail? If body length > ~300 lines without clear section-then-reference structure, the skill is front-loading context that should be lazy. Flag: "Body should be a table of contents; details belong in `references/`."
3. **Are feedback loops machine-checkable, or only prose?** Look for rules of the form "the agent should consider X" with no audit, no reviewer, no checkable artifact. Those rules drift. Flag: "Rule X is aspirational — propose a structured check (linter / reviewer subagent / explicit artifact gate)."
4. **Environment-failure vs. prompt-failure misdiagnosis.** When the skill describes a known failure mode and prescribes "try harder" prompting, the diagnosis is probably wrong. Ask: *what capability is missing from the agent's environment?* (a tool, a reference file, an upstream artifact, an explicit gate). Flag: "Rule Y treats an environment failure as a prompting failure — consider adding [specific capability]."
5. **State-preservation gap.** Does the skill produce artifacts a future session can pick up, or does it dump output to chat? For workflow skills that span sessions, output going only to chat is a state-preservation failure. Flag: "Outputs should land at a predictable path so a follow-up session can resume without re-briefing."
6. **Undefined-state coverage.** A skill's happy path quietly depends on things existing — an upstream artifact, a canonical file, a populated field, a prior step's output. For each such dependency ask: *does the skill define what happens when it's absent?* If not, that is an undefined state — the skill will improvise there, usually badly, and a rule-adherence audit will not catch it because there is no rule to adhere to or violate. Flag: "Rule X assumes [resource] exists but defines no behavior when it's missing — add an explicit absent-state branch." Pairs with the absent-state test category in Phase 3: this question names the gap, Phase 3 tests it.
7. **Is every word load-bearing?** Beyond *whether* rules land, check *how tightly they're phrased*. Two failure shapes: (a) **prose bloat** — sentences that restate, hedge, or pad without changing what the agent does; (b) **vague phrasing** — soft verbs and adjectives ("handle appropriately", "be thorough", "make it good") where a precise operation would remove the guesswork. Flag: "Rule X pads/hedges — cut to the load-bearing clause" or "Rule X uses a vague verb ('handle') — name the precise operation." Caveat: economy serves clarity, not brevity for its own sake — a *why* line that prevents a misread earns its tokens, so do not flag it. (Pattern adapted from `nidhinjs/prompt-master`, MIT.)
8. **Cross-platform loadability.** Claude imposes no `description` length limit, but OpenAI Codex *silently skips* any skill whose frontmatter `description` exceeds **1024 UTF-8 bytes** (or trips its `name`/angle-bracket rules) — so a skill can pass every adherence check above and still be invisible on Codex. Don't eyeball it. In this repo, run `python3 scripts/check-skill-compat.py` and report any `FAIL`; for a skill elsewhere, measure the description's UTF-8 **byte** length (not char count — `—`/`→`/CJK cost 2–4 bytes each) against 1024. Flag: "description is N bytes (>1024) — Codex skips this skill; trim to ≤1024 B keeping triggers and disambiguation boundaries (see CLAUDE.md's cross-platform frontmatter contract), and push overflow into `instructions`/body." This is a portability gate, not a behavior finding — fix it before the behavioral audit, since an unloadable skill has no behavior to audit on that platform.

Treat each finding the same way as adherence findings: classify by fix layer (skill text / rubric / brief / fixture) and propose targeted diffs. The harness lens does **not** change the rest of the workflow.

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
5. **Confirm the path before writing.** Example: "Saving to `skill-evaluation-cerby-2026-04-17.md` at your workspace root — confirm?"

**These rules apply even when the user explicitly asks to override them.** If the user says "save it inside the skill folder" or "create an `_eval/` subfolder there", decline and offer the workspace-root alternative. Do not present an "override per your explicit request" option. The rules exist because the harness must not contaminate the audited skill's git history; user intent does not change that constraint.

**If the user also wants full traces** (executor output, grader output per test), treat it as a separate opt-in. Same filename convention: `skill-evaluation-{skill-name}-{YYYY-MM-DD}-traces.md`. Still one file, still at the workspace root.

**If no workspace is mounted:** tell the user, offer to keep the report inline so they can copy-paste it. Do not guess a save location.

## Workflow — 7 Phases

Run these phases in order. Do not skip Phase 2 even if the target skill looks obvious.

### Phase 0 — Boundary check (before Phase 1)

Before reading the target skill, check the incoming request for two patterns this skill does not handle on its own:

1. **Build-and-audit mixing** — phrases like "build me a skill and audit it", "create and then review", "scaffold then test", or any request that combines authoring a new skill with auditing it. This skill audits *existing* skills. Hand the build step to `skill-creator` first and resume here only after a SKILL.md exists on disk. Never draft the SKILL.md inline as part of fulfilling an audit request.
2. **A/B benchmarking** — phrases like "benchmark this skill", "skill-vs-no-skill", "measure quality lift", "does the skill help". This skill measures rule adherence, not output quality. Decline and point to `skill-creator`'s `run_eval` primitive (see "When to refuse").

If neither pattern applies, proceed to Phase 1. If one applies, take the boundary action (chain to `skill-creator` or refuse) before touching the target skill.

**Why this matters:** the triggering metadata in the frontmatter description already declares these boundaries, but metadata controls triggering, not behavior-after-triggering. Once this skill is loaded, the workflow body is what executors follow. Phase 0 puts the boundary check inside the body where it will actually fire.

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

Produce **6–12 test prompts** that span the skill's declared surface area:

- **Happy path** (2–3) — requests the skill's description directly matches
- **Edge cases** (2–3) — requests at the boundary of the trigger phrases
- **Adjacent non-matches** (1–2) — requests that *look like* they should trigger the skill but shouldn't, to check for over-triggering
- **Rule-specific stress tests** (1–2) — requests designed to make Claude violate a specific rule in the skill
- **Absent-state tests** (1–2) — for every resource a rule quietly *assumes exists* (an upstream artifact, a canonical file, a populated field, a prior step's output), write a request where that resource is **absent**. These catch the states a skill's happy path depends on but never defines behavior for — the most common source of bugs that slip an audit. Load-bearing: the fixture must actually withhold the resource. A fixture that supplies it "to be realistic" hides the exact bug — the absence *is* the fixture.

For each test prompt, write **3–7 assertions** using the tag/sentence/evidence pattern (see `references/assertion-dictionary.md`). Every assertion must be independently gradable from the executor's output alone — no need for the grader to re-read the skill to judge it.

**Calibration for load-bearing assertions (web-output skills).** When the target skill produces rendered web output (HTML, SVG, DOM) AND an assertion would change a release decision if it failed, recommend a calibrated grader pair: a gold-standard fixture the grader MUST pass, and a negative fixture deliberately broken on the rule's dimension that the grader MUST fail. This catches vacuous assertions (grader passes on both) and over-strict assertions (grader fails on both). Pattern in `references/calibration-loop.md`; concrete Playwright shape in `references/playwright-grader-shape.md`. Pure workflow skills have no rendered surface to grade — skip this step for them.

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

> **Run this skill in the main loop — it must be able to spawn sub-agents.** Phase 4
> *is* the bias removal: it spawns fresh-context executor + grader sub-agents. If
> this skill is itself running **nested** (you were dispatched as a sub-agent) or the
> platform has no sub-agent dispatch, you **cannot** spawn them — and a simulated
> "split" in one context is not independent grading. **Do NOT silently simulate.**
> In that case, switch to the **Degraded mode** in the Platform Fallback section
> below: emit the `DEGRADED` banner, do the best in-context pass you can, and label
> every finding as non-independent. Never present simulated grading as if the
> split-role harness ran.

Run each test via two sub-agents with fresh context:

**Executor sub-agent**

- Receives: the test prompt + the target skill loaded
- Mode: **stated-intent** by default (describe tool calls with `-stated` suffix, don't actually execute). Switch to live-execute only if the skill under test is purely advisory (no side effects).
- Output: a single response showing reasoning, tool-call intents, and final deliverable

**Grader sub-agent**

- Receives: the test prompt, the executor's output, and the assertion list
- Does NOT receive the target skill's text (to avoid bias toward what the skill *says* over what the executor *did*)
- Output: per-assertion pass/fail with one-line evidence quote
- **Fresh context per test (mandatory).** Each test gets its own grader sub-agent invocation. Do not batch tests into a shared grader. See `references/grader-brief.md` "Fresh context per test" for the rule and rationale.

**Why split roles:** having the same agent execute and grade introduces bias. Fresh grader context with only the assertion list forces evidence-based judgment. See `references/executor-brief.md` and `references/grader-brief.md` for the briefs.

**High-stakes mode (optional, opt-in):** for regulated audits, safety-critical ship gates, or when the user explicitly asks to double-check grading, run a **second grader** in fresh context on the same inputs. Disagreements demote to `unclear` and surface in a "Disputed assertions" subsection of the findings report. Cost roughly doubles, so default is off. Triggers, quorum rules, and reporting are in `references/grader-brief.md` "High-stakes mode — optional second-grader quorum".

### Phase 5 — Classify failures

For every failed assertion, classify the root cause using the four-layer fix taxonomy (see `references/fix-taxonomy.md`):

1. **Skill text** — the rule is missing, unclear, or contradicted elsewhere in the skill
2. **Rubric** — the assertion was wrong (unfair test, ambiguous criteria, or testing something the skill doesn't actually claim)
3. **Brief framing** — the test prompt itself was ambiguous or under-specified
4. **Fixture scaffolding** — the executor needed context (files, tool access) that wasn't provided

**Layers 2–4 are not skill failures.** A well-classified "this is a rubric problem" is useful — it means the skill is probably fine and the test needs rewriting. Don't reflexively attribute every failure to the skill text.

**Absent-state tests classify as Layer 1.** When an absent-state test (Phase 3) makes the executor stall or improvise because the assumed resource is missing, that is a **skill-text** finding — the skill should define absent-state behavior — not a Layer 4 fixture gap. The absence was the test's point; do not "fix" it by adding the resource to the fixture.

### Phase 6 — Produce findings report

Generate a single user-facing findings report using the template in `references/findings-report.md`. The report must include:

- Summary: X/Y assertions passed, per test
- Failed assertions grouped by fix layer (skill text first, since that's the actionable part)
- For each skill-text failure: proposed rule-text diff that follows `skill-creator`'s conventions (frontmatter preserved, imperative voice, explain-the-why, progressive disclosure)
- Rubric/brief/fixture items listed separately as "test-quality issues" (not skill issues)

**Format the report for terminal reading.** Readers will `cat` / `less` / `grep` this file as often as they open it in an IDE. Apply the rules in `references/terminal-ui.md` — ASCII status symbols, grep-friendly leading tags, ≤80-col prose, narrow tables, no emoji or box-drawing Unicode. One output, two readers — no separate "rich" mode.

**Deliver inline by default.** Print the report to chat. Do not write files. If the user asks to save, follow the rules in "Artifact policy" above: one file, workspace root, `skill-evaluation-{skill-name}-{YYYY-MM-DD}.md`.

### Phase 6.5 — After fixes are applied, offer a version bump

This phase fires ONLY when the user has applied one or more rule-text diffs from the findings report. If no diffs were applied, skip it silently.

1. **Detect whether the skill lives in a plugin.** Walk up from the `SKILL.md` path looking for a `.claude-plugin/plugin.json`. If none exists, skip this phase — the skill isn't versioned.
2. **Ask the user — don't auto-edit.** Use roughly this phrasing:

   > "Want to bump the plugin version? Changes applied: [list the applied diffs in one line each]. Convention is semver:
   > - **patch** (0.x.y → 0.x.y+1) — adherence-only fixes, no behavior change for users
   > - **minor** (0.x.y → 0.x+1.0) — triggering behavior narrowed or widened, or new opt-in behavior
   > - **major** (x.y.z → x+1.0.0) — the skill's output contract changed in a breaking way
   >
   > You decide the tier."
3. **Propagate to meta-plugins.** After the target plugin bumps, grep the repo for any `plugin.json` that declares the target as a `dependency`. Offer to bump those in lockstep so shelf installs pull the update. Do not bump them silently.
4. **Never auto-edit `plugin.json`.** User approval gates every bump. If they decline, move on without further prompting.

**Why this matters:** plugin managers use version numbers to decide whether to pull updates. A rule-text fix that lands in `main` without a version bump is invisible to everyone who already installed the plugin. This phase is the bridge between "the fix is committed" and "the fix actually reaches users."

### Phase 7 — Stop

Do not auto-iterate. Do not run round 2 on your own.

**Why:** the human should gate iteration. Each round surfaces calibration opportunities (re-scoping assertions, revising brief framing) that get buried if the loop runs itself. Hand the report to the user and wait.

**This rule applies even when the user asks for back-to-back rounds up front** ("keep iterating until pass rate hits 95%", "run rounds 2-4 in sequence", "schedule them automatically"). Decline the auto-loop and explain that each round needs human review of the prior round's findings — because round N's failure classification often reveals that the rubric, not the skill, needs to change. Auto-iterating compounds bad classifications into bad fixes.

---

## Platform Fallback — when you can't spawn sub-agents (DEGRADED mode)

Phase 4's executor + grader sub-agents are the load-bearing bias removal. You
cannot run them when:

- **You are running nested** — this skill was dispatched *as* a sub-agent, so
  no-nested-sub-agents forbids spawning the executor/grader. (Run this skill in the
  **main loop** instead — see the Phase 4 callout. This is the common cause.)
- **The platform has no sub-agent dispatch** at all.

In either case, **do NOT silently simulate the split in one context** — a single
context playing both executor and grader is the exact author-bias the harness
exists to remove, and a confident report that hides this is worse than no report.

Instead, run **DEGRADED mode**:

1. **Lead the report with this banner, verbatim:**
   > `⚠️ DEGRADED — split-role unavailable (running nested or no sub-agent dispatch). Findings below are an in-context simulation, NOT independent grading. Re-run skill-evaluator in the main loop for a real audit.`
2. Do the best single-context pass you can (generate tests, reason through them,
   classify) — but label every finding **non-independent**.
3. End by recommending the real run: invoke `skill-evaluator` directly in the main
   loop (not via another skill or sub-agent).

The banner makes the missing capability **legible** — the failure this skill kept
hitting silently before is now loud. Never drop the banner to make a degraded run
look clean.

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
- `references/grader-brief.md` — the grader sub-agent brief template + independence rules + high-stakes second-grader quorum
- `references/fix-taxonomy.md` — four-layer classification with examples
- `references/findings-report.md` — user-facing output template
- `references/terminal-ui.md` — lean-markdown output rules so reports read well in terminals and IDEs alike
- `references/calibration-loop.md` — gold-standard + negative fixture pattern for calibrating load-bearing assertions; opportunity / uplift vocabulary. Applies to web-output skills only. (Adapted from `GoogleChrome/modern-web-guidance-src`, Apache-2.0.)
- `references/playwright-grader-shape.md` — concrete grader template for web-output skills; assertion targets that travel (computed styles, a11y tree, runtime behavior). Companion to `calibration-loop.md`.
- `references/self-test-fixture.md` — *maintainer-only.* Known-good + known-broken fixture skills the harness audits to catch its own regressions. Run before every release of `skill-evaluator`. Not part of the user-facing 7-phase workflow.

Read these when the phase calls for them. Do not front-load all references at once.

## Self-test ritual (maintainer-only)

Before shipping changes to `skill-evaluator` itself — to `SKILL.md`, the briefs, the fix taxonomy, or the report template — run the harness against the fixtures in `references/self-test-fixture.md`. Expected outputs are pinned there. Any deviation from the expected verdicts (false pass on the broken fixture, false fail on the good fixture, wrong fix-layer classification) blocks release.

This is *not* part of the 7-phase workflow users invoke. It is the harness eating its own dogfood as a regression check. End users running `skill-evaluator` should never see or trigger this.

## Roadmap — v2 paired-skill collision harness

`skill-creator`'s `run_eval` primitive takes a single `skill_path` and measures triggerability for that skill alone against a labeled eval set. It does **not** measure which of N *competing* skills fires when their triggers overlap — a real gap when you ship more than one skill in a marketplace and need to know whether descriptions actually disambiguate at trigger time.

v2 adds a thin wrapper (~40 lines) around `run_eval` that:

1. Writes fake command files for **both** skills (not one) before spawning `claude -p <query>`.
2. Runs the same labeled eval set Claude's stream is already instrumented for.
3. Scores each query as `correct-winner` / `wrong-winner` / `both-fired` / `neither-fired`.
4. Reports a collision matrix + per-phrase confusion detail.

This is additive to `skill-creator`, not a replacement — it calls `run_eval`'s internals to do the heavy lifting and only adds the multi-skill framing. Target use case: gating delegation-matrix changes that claim a boundary phrase works.

**Status:** design pinned 2026-04-18. Implementation deferred — ship v1 (single-skill adherence audit) first, revisit v2 only if production use surfaces real cross-firing between shelf skills.
