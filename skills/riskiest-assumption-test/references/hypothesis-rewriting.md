# Hypothesis Rewriting — Reference

Patterns for converting **vague beliefs** (the canvas's natural output) into
**falsifiable hypotheses** (what RAT requires for testable claims). Read
this before completing Phase 3.

The job: a hypothesis the founder can run a test against, where there is a
plausible result that would convince them they were wrong.

---

## The canonical pattern

```
We believe [specific assumption about a specific segment].
We'll know this is true if [specific measurable outcome] within [time bound].
```

**Three rules** the canonical pattern enforces:

1. **Specificity on both sides** — the belief names a specific segment AND
   a specific behavior; the outcome names a specific measurable signal AND
   a specific threshold.
2. **Time bound** — *when* does the test conclude? Without a time bound,
   the test never falsifies (you can always say "wait longer").
3. **Falsifiability** — the outcome must be observable. "They'll love it"
   is not observable. "≥ 4 of 10 will sign and pay" is observable.

---

## Anti-patterns: belief framings that aren't falsifiable

Rewrite these. Don't write tests for them.

### Anti-pattern 1: vague verbs

❌ *"Customers will **like** our product."*
❌ *"Users will **engage** with the feature."*
❌ *"The market will **support** this price."*

**Why it fails:** "like", "engage", "support" are unobservable. Two
people can disagree on whether something happened.

✅ Rewrite: *"≥ 4 of 10 ICP-matched users will return to the product
within 7 days of first use, without prompting."*

### Anti-pattern 2: missing specifics

❌ *"Customers will pay for this."*

**Why it fails:** which customers? How much? How often? Pay vs. say
they'd pay?

✅ Rewrite: *"≥ 3 of 10 VPs of Customer Support at 50–500 person SaaS
companies will sign a 6-month contract at $499/mo within 14 days of
first demo."*

### Anti-pattern 3: time-unbounded

❌ *"Eventually, the cohort retention curve will flatten."*
❌ *"Over time, organic word-of-mouth will be our primary channel."*

**Why it fails:** "eventually" / "over time" can never be falsified —
the founder can always wait longer.

✅ Rewrite: *"Cohort retention at month 6 will be ≥ 60% for the August
2026 cohort, measured by the November 2026 cohort report."*

### Anti-pattern 4: outcome too abstract

❌ *"The data will show product-market fit."*
❌ *"We'll see strong unit economics."*

**Why it fails:** PMF and "strong unit economics" are interpretive. Three
people will read the same data three ways.

✅ Rewrite: *"≥ 40% of week-1 users return in week 4 (Sean Ellis-style PMF
proxy)" + "LTV/CAC ≥ 3 across the August 2026 cohort by month 6."*

### Anti-pattern 5: confounded with multiple variables

❌ *"If we ship version 2, our metrics will improve."*

**Why it fails:** version 2 might change pricing, UI, marketing copy, AND
the feature set. Improvement could be from any of those — you learn
nothing about which.

✅ Rewrite: hold variables constant. Test ONE thing at a time. *"If we
add the new onboarding flow (only changing onboarding, not pricing or
copy), week-1 activation will increase from 38% to ≥ 50% in the next
30-day cohort."*

### Anti-pattern 6: confirmable-but-not-falsifiable

❌ *"There will be at least *some* interest from the target segment."*

**Why it fails:** "some" is non-disconfirmable — any non-zero result
confirms it. You haven't tested anything.

✅ Rewrite: name a threshold above which the result counts as
confirmation, and below which it counts as falsification. *"≥ 5% of 200
LinkedIn-targeted visitors will leave their email."*

### Anti-pattern 7: untestable in the available time/budget

❌ *"Within 6 months we'll know if we have a venture-scale business."*

**Why it fails:** the test is too expensive — the founder will burn
runway *during* the test. RAT is about cheap, fast falsification.

✅ Rewrite: pick a smaller, cheaper proxy that resolves in days or weeks.
*"Within 14 days, ≥ 4 of 10 paid-enterprise prospects will agree to a
2nd-meeting product demo (a leading indicator of pipeline velocity)."*

---

## Conversion patterns by category

### Desirability hypotheses

**Belief shape:** "Segment X cares about Problem P."

**Hypothesis shape:**
- *"≥ N of M [ICP-matched]] [segment] members will [observable engagement
  signal] within [time bound]."*
- *"Within [time], ≥ X% of [segment] visitors who see [specific UVP] will
  [conversion action]."*

**Worked examples:**

Belief: "VPs of Sales at 200-person SaaS companies feel pain about ramp
time for new AEs."

Hypothesis: *"In a 14-day window, ≥ 6 of 10 outreached VPs of Sales at
100–300 person SaaS companies will accept a 30-min call to discuss new-AE
ramp time, AND ≥ 4 of those 6 will describe the pain unprompted within
the first 5 minutes of the call."*

---

### Viability hypotheses

**Belief shape:** "Segment X will pay [price] for [offering]."

**Hypothesis shape:**
- *"≥ N of M prospects will [pay / sign / commit] at [exact price] within
  [time bound]."*
- *"Of [segment] prospects shown the offering at [price], ≥ X% will
  [conversion event]."*

**Worked examples:**

Belief: "Solo bookkeepers will pay $300/mo for an automated client report
service."

Hypothesis: *"Of 15 solo bookkeepers contacted in a 3-week window, ≥ 5
will sign a 3-month contract at $300/mo (paid up front via Stripe) for
the concierge MVP."*

Note the specifics: time bound, sample size, exact price, payment mechanic
(not "agree to pay" but "pay via Stripe"), commitment shape (not
month-to-month, 3-month).

---

### Feasibility hypotheses

**Belief shape:** "We can build/deliver [thing] at [cost/quality]."

**Hypothesis shape:**
- *"In a [time-bound] technical spike, [specific quality bar] will be
  achievable using [stated approach] — measured by [observable check]."*
- *"After [N] expert consultations, ≥ N of N experts confirm the approach
  is feasible at our scale and name no blocking constraint."*

**Worked examples:**

Belief: "We can deliver an AI coding assistant that saves engineers ≥ 30
min/day."

Hypothesis: *"In a 2-week Wizard of Oz with 5 engineers (humans
roleplaying the AI assistant), engineers will self-report ≥ 30 min/day of
saved time on ≥ 60% of usage days, AND will continue using the tool
unprompted into week 2."*

Note: this is a feasibility *and* a desirability hybrid — common with
Wizard of Oz tests. The hypothesis is split into two falsifiers (time
saved + continued use) so the test can fail either way.

---

## When the founder produces an unfalsifiable hypothesis: push back

The skill is allowed — and required — to refuse to write a test plan for
a hypothesis that fails the falsifiability bar. The push-back is direct:

> *"This hypothesis isn't falsifiable in its current form: there's no
> measurable outcome that would convince you the belief is wrong. Let's
> rewrite — what's the specific signal you'd accept as evidence the
> belief is incorrect?"*

Then walk through:
1. What does "yes, this is true" look like, observably? (Define success.)
2. What would convince you it's NOT true? (Define kill.)
3. What's the soonest you could observe this signal? (Time bound.)

If the founder can't answer any of these, the hypothesis is genuinely
ill-formed — escalate to either splitting it into smaller hypotheses or
moving it to the backlog.

---

## A complete worked example

**Founder's initial belief (from the canvas Stress Tests):**

> *"Designers want an AI tool that converts Figma to React."*

**Step 1 — Add specificity.**

What kind of designer? At what kind of company? At what stage of the
design-to-dev handoff?

Refined: *"Solo product designers at < 50 person startups want an AI tool
that converts a single Figma frame to a working React component."*

**Step 2 — Add a measurable outcome.**

"Want" how? Use it once? Use it weekly? Pay for it?

Refined: *"Solo product designers at < 50 person startups will use an AI
Figma-to-React tool ≥ 3 times in their first week and ≥ 2 times per week
in week 2."*

**Step 3 — Add a time bound and sample.**

Over how long, with how many?

Refined: *"In a 14-day window, of 10 solo product designers at < 50
person startups recruited via the Designer Hangout community, ≥ 6 will
use the AI Figma-to-React tool at least 3 times in their first week, and
≥ 4 of those 6 will use it ≥ 2 times in week 2."*

**Step 4 — State the kill criteria explicitly.**

When is this falsified?

Final hypothesis:

> *"We believe solo product designers at < 50 person startups will adopt
> an AI Figma-to-React tool. We'll know this is true if ≥ 6 of 10
> recruited designers use the tool ≥ 3 times in week 1, AND ≥ 4 of those
> ≥ 2 times in week 2 — measured 14 days from cohort start. Killed if
> < 4 use it ≥ 3 times in week 1, OR none of the week-1 users return in
> week 2."*

This hypothesis is now ready for Phase 4 (Test Method Selection — likely
a Wizard of Oz given feasibility + desirability mix).
