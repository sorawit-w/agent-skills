# Phase 3 findings — trigger-collision benchmark

**Status:** BLOCKED inside Cowork sandbox. Eval set + harness prepared for
local execution.

## What we tried

- Path A per matrix Q1 resolution: run `skill-creator`'s `run_eval.py` twice
  (once for `skill-evaluator`, once for `skill-creator`) against a stratified
  20-query eval set (6 evaluator-positives, 6 creator-positives, 4 ambiguous,
  4 unrelated), with mirrored labels to measure cross-firing.
- Harness: Anthropic's `run_eval.py` unchanged. Fake command file ➜ `claude
  -p` subprocess ➜ stream watch for `clean_name`.

## What happened

Both runs returned identical 14/20 pass-rate — but the pattern was
suspicious: every positive failed at 0/2, every negative passed at 0/2. A
diagnostic `claude -p` invocation from the sandbox revealed the actual
failure mode:

```
"apiKeySource": "none"
"Not logged in · Please run /login"
```

The nested `claude` subprocess has no credentials. Every eval invocation
returned an auth error before producing a single token, so `run_eval`
correctly observed "no skill triggered" for every single query. The 14/20
"passes" are entirely trivially-satisfied `should_trigger: false` labels.

**There is no real measurement in these results.**

## Root cause

Cowork mode's auth doesn't propagate to child `claude` processes, and
`skill-creator`'s eval assumes a stand-alone authenticated CLI. This is a
harness limit, not a description-quality issue.

## Confidence

High (0.95) — the stream log shows the auth error explicitly. The 0/2 across
all 40 queries matches what you'd see under total subprocess failure, and
there's no plausible alternative explanation (real model, real API, but never
triggers any of 14 skills on 20 varied queries).

## What we have to hand off

- `queries.md` — annotated 20-query corpus with labeling convention
- `queries.evaluator.json`, `queries.creator.json` — JSON eval sets ready for
  `run_eval.py`
- `RUN_LOCAL.md` — runbook for executing outside the sandbox
- `results.evaluator.{json,log}`, `results.creator.{json,log}` — the
  sandbox-invalid runs, kept as evidence of the auth failure (not data)

## Decision on Path B

Deferred. Two reasons:

1. **We don't have Path A data yet.** Path B is a ~40-line wrapper that
   extends `run_eval` to write both fake command files before spawning
   `claude -p`. That's valuable IFF Path A shows cross-firing between two
   isolated descriptions. Without Path A evidence, we'd be building a
   measurement tool for a problem we can't yet confirm exists.

2. **The matrix gate only requires Path A.** Matrix Q1 resolution
   specifically called Path A a "quick sanity check" and flagged Path B as a
   v2 capability. We should honor that sequencing.

**Recommended next step:** Kiang runs `RUN_LOCAL.md` on his local machine
(cost: ~$0.50–$1 of sonnet tokens, ~10 min wall time at 3 runs/query).
Evaluates the gate. Only if results surface real collisions (>15%) or the
description clearly under-triggers do we invest in Path B.

## Secondary finding — addressed by reasoning, not yet verified

The skill-evaluator description tightened in Phase 2.5 led with `Use ONLY
when the user has a shipped skill...`, which was hypothesized to over-restrict
triggering. Soft-revised in a follow-up commit (see git log) without running
the eval:

- Positive trigger list moved ABOVE the hard-boundary prose (front-loads the
  common phrasings "audit", "stress-test", "find gaps" so the classifier
  sees them first)
- "Use ONLY when" relaxed to "Use when"
- Added "review this skill end-to-end" to the positive list (matches one of
  the Group-A eval queries)
- Hard-boundary paragraph kept, but now lives below the trigger lists as
  defensive context rather than gating prose

**Still un-verified** — the local eval under `RUN_LOCAL.md` would confirm or
falsify. If anyone picks this up later, compare trigger rates on Group A
queries before/after this revision.

## README update note

When we write the Phase 4 README update, call out that eval tooling for our
skills requires running `claude` outside Cowork. Users evaluating
contributions won't hit this today because there's no CI harness — but we
should add it to CONTRIBUTING / docs/testing.md when that exists.
