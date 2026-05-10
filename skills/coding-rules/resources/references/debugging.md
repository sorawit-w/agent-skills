# Systematic Debugging

**Iron Law: No fixes without root cause investigation first.**

Trial-and-error debugging — changing things until the error disappears — is the single biggest time sink for agents. It creates phantom fixes, introduces new bugs, and wastes retry budgets. This reference enforces a structured alternative.

---

## The 3-Step Method

### Step 1: Reproduce

Before anything else, confirm you can reliably trigger the bug.

1. **Read the error message completely** — stack trace, exit code, log context. Don't skim.
2. **Reproduce the failure** — Run the exact command or test that fails. If you can't reproduce it, you can't verify a fix.
3. **Isolate the scope** — Is this one test? One file? One endpoint? Narrow the blast radius.

If you cannot reproduce: add logging, check environment differences, verify you're on the right branch. Do NOT guess at a fix.

### Step 1.5: Tighten the Loop

Before iterating on hypotheses, **assess your feedback loop**. The speed and reliability of reproduction is your speed limit — every hypothesis test pays the loop's cost.

- **Deterministic > flaky.** A 30-second flaky loop is barely better than no loop. A 2-second deterministic loop is a debugging superpower.
- **If the loop is slow or flaky, fix the loop before fixing the code.** Add a focused test, narrow the input, mock external calls, or extract the failing path into a smaller harness.
- **State your loop explicitly** before the first hypothesis test: e.g., *"Reproduces in ~3s, deterministic"* or *"~45s, flaky 1-in-3"*. The latter is a signal to invest in tightening before guessing further.

A tight loop multiplies hypothesis throughput. Skipping this step pays for itself within ~5 hypotheses.

### Step 2: Hypothesize (Max 3)

Based on what you observed, form **at most 3 hypotheses** for the root cause. For each:

```
Hypothesis: [what you think is wrong]
Evidence for: [what supports this]
Evidence against: [what contradicts this]
Test: [how to confirm or eliminate this hypothesis]
```

**Test hypotheses one at a time.** Don't change multiple things simultaneously — you won't know which change mattered.

Priority order for hypotheses:
1. **What changed recently?** — Check `git diff` and `git log`. Most bugs are caused by recent changes.
2. **What does the error message actually say?** — Read it literally, not interpretively.
3. **What assumptions am I making?** — State them explicitly. Wrong assumptions are a top root cause.

### Step 3: Fix and Verify

Once you've identified the root cause (not before):

1. **Make the minimal fix** — Change only what's necessary to address the root cause
2. **Verify the original failure is resolved** — Run the exact reproduction from Step 1
3. **Check for regressions** — Run the full quality gate suite, not just the failing test
4. **Explain why the fix works** — If you can't explain it, you haven't found the root cause

---

## Anti-Patterns

| Anti-Pattern | Why It Fails | Do This Instead |
|---|---|---|
| Changing code before reading the error | You're guessing, not debugging | Read the full error first |
| Changing multiple things at once | Can't attribute which change fixed it | One change per hypothesis test |
| "Let me try restarting" as first step | Masks the problem, doesn't solve it | Reproduce first, restart only if hypothesis supports it |
| Fixing the symptom, not the cause | Bug will resurface in a different form | Trace to root cause |
| Spending >15 min without new information | You're stuck in a loop | Step back, add logging, form new hypothesis |
| "It works now" without understanding why | Phantom fix — it'll break again | Explain the fix or it's not a fix |

---

## When to Escalate

If after 3 hypotheses you still can't identify root cause:

1. **Document what you know** — reproduction steps, hypotheses tested, evidence gathered
2. **Mark as BLOCKED** — with the debugging context attached
3. **Move on** — don't burn more retry budget on speculation

This is not failure — it's efficient triage. Some bugs require domain knowledge or history that the agent doesn't have.

---

## Integration with Retry Budgets

Systematic debugging operates *within* the retry budgets defined in `quality-gates.md`. Each hypothesis test counts as one attempt. If you exhaust your retry budget during debugging, follow the escalation path above.

The difference is how you spend those attempts: structured investigation vs. random trial-and-error. Three focused attempts with hypothesis testing beats five blind retries.
