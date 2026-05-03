# Ranking Matrix — Reference

Scoring rubrics and worked examples for the **risk × impact** ranking in
Phase 2. Read this before scoring assumptions — it surfaces the systematic
biases founders bring to the matrix and how to correct for them.

---

## The matrix

Score each assumption on two axes:

- **Risk** (likelihood the belief is wrong): **Low / Medium / High**.
- **Impact** (consequence if the belief is wrong): **Low / Medium / High**.

Plot mentally:

```
                Risk →
              Low   Med   High
              ┌─────┬─────┬─────┐
         High │  ○  │  ●  │  ★  │  ← test these first
              ├─────┼─────┼─────┤
Impact   Med  │  -  │  ○  │  ●  │
              ├─────┼─────┼─────┤
         Low  │  -  │  -  │  -  │  ← never test these first,
              └─────┴─────┴─────┘    even when High Risk

★ = Top 3 candidates (high impact + high risk)
● = Top 3 fillers (high impact + medium risk, or medium impact + high risk)
○ = Backlog
- = Don't bother
```

**The Top 3 rule:**
- Pick from the ★ corner first.
- If you have fewer than 3 ★s, fill from ● in this order: high-impact
  + medium-risk, then medium-impact + high-risk.
- **Never** include a low-impact assumption in the top 3 — even if it's
  high-risk. Confirming a low-impact belief doesn't move you forward.

---

## Risk scoring rubric

The question: *how likely is it that this belief is wrong?*

### High risk

The belief is largely **untested speculation** built on either:

- The founder's intuition without external corroboration.
- Limited evidence from a non-representative sample (your 3 friends; your
  Twitter audience; the one customer who asked for it).
- Pattern-matching from a different domain ("worked for Slack, will work
  here").
- A second-order assumption ("competitors must be solving this poorly
  because…").

**Examples:**
- "Customers will pay $99/mo for this" — when no one has been asked.
- "We can acquire customers via SEO at $30 CAC" — when no SEO content
  exists.
- "Healthcare buyers will tolerate a non-EMR-integrated tool" — when
  founder has no healthcare background.

### Medium risk

The belief has **some external evidence** but the evidence is partial:

- A handful of customer interviews (2–4) have nodded at the belief.
- Comparable companies have demonstrated the pattern, but in adjacent
  segments.
- The founder has direct domain experience that supports the belief, but
  no test in the specific segment.
- Quantitative data exists but is from a non-experimental source (industry
  reports, public benchmarks).

**Examples:**
- "Customers will pay $99/mo" — based on 3 interviews where 2 said "I
  could see paying that."
- "SEO at $30 CAC" — based on a competitor in an adjacent segment hitting
  similar numbers.

### Low risk

The belief has been **directly tested or has strong external support**:

- ≥ 5 customer interviews unprompted-confirmed the belief.
- A prior product or test of the same belief succeeded.
- The belief is a well-established industry constant (e.g., "stripe.com
  works as a payment processor").

**Examples:**
- "Customers will pay $99/mo" — 5 of 7 prospects in a pre-sale paid that
  exact price last quarter.
- "Stripe handles our payments correctly" — well-tested infrastructure.

---

## Impact scoring rubric

The question: *if this belief is wrong, what happens to the business?*

### High impact

If wrong, the business **does not work in its current shape**:

- The price is wrong → no path to break-even.
- The segment doesn't feel the problem → product has no buyers.
- The technology can't be built → no product to sell.
- The channel doesn't work → no path to scale.
- A regulatory pathway is closed → can't operate.

**Examples:**
- "Customers will pay $99/mo" — at $20/mo CAC, the unit economics close.
  At $39/mo, they don't.
- "VPs of Sales feel this pain" — if they don't, the product is a
  Slack-channel idea, not a SaaS company.

### Medium impact

If wrong, the business **needs a meaningful adjustment** but doesn't die:

- Pricing is wrong but a 30% adjustment fixes it.
- A secondary segment doesn't materialize but the primary still works.
- A channel underperforms but a fallback exists.
- A feature isn't valued but the core offering still is.

**Examples:**
- "Annual contracts will be the dominant deal shape" — if monthly wins,
  cash flow gets harder but the business still works.
- "We'll add a self-serve tier in Q2" — if self-serve doesn't convert,
  enterprise still pays.

### Low impact

If wrong, the business **adjusts a tactic**, no strategic change:

- Wrong color on the landing page.
- A specific copy variant underperforms.
- One marketing channel isn't optimal.
- A nice-to-have feature doesn't get used.

**Examples:**
- "The 'Get Started' button should be green" — change to blue, move on.
- "Sales reps will close deals 20% faster with feature X" — useful, but
  not strategic.

---

## Common scoring traps

### Trap 1: founders systematically under-rate desirability risk

You've talked yourself into the problem. You believe it's real because
you've been thinking about it for months. But the customer hasn't agreed
yet — and the customer is who decides.

**Correction:** if your only evidence for desirability is "I've thought
about this and it makes sense," score it **High Risk**. Always.

### Trap 2: founders systematically under-rate viability risk in B2B

"Of course they'll pay $X — look at what competitors charge!" But
competitors charge for products with logos, case studies, and references
you don't have. Your willingness-to-pay test is yours alone.

**Correction:** any pricing belief without ≥ 3 prospects who've explicitly
acknowledged the price is **High Risk** in B2B. The "just look at
competitors" reasoning is a sign you should test, not skip.

### Trap 3: founders over-rate feasibility risk for technology and under-rate it for distribution

Engineers especially: "Can we build it?" feels exciting, so it gets
attention. "Can we get anyone to know we exist?" feels boring, so it gets
hand-waved.

**Correction:** for any feasibility-flavored hypothesis, ask: "is this a
*build* feasibility or a *distribute* feasibility question?" Distribution
feasibility (the channel works at the cost we need) is almost always
under-tested.

### Trap 4: confusing "scary if true" with "high impact"

Some assumptions are scary because they're emotionally charged (a
co-founder might leave, a competitor might launch first), but their
strategic impact is moderate. Others are boring but lethal (the unit
economics are 20% off).

**Correction:** when scoring impact, ask: *"if this belief is wrong, what
specifically breaks?"* If you can name a structural break (margin, CAC,
runway, regulation), it's likely High Impact. If the answer is "we'd be
sad," it might be lower impact than it feels.

### Trap 5: over-scoring everything as High Risk + High Impact

Some founders feel bad scoring assumptions as Low Risk or Low Impact —
"aren't they all important?" No. The matrix is a forced ranking. If
everything is ★, the ranking has no information.

**Correction:** if more than ~3 of your assumptions land in the ★ corner,
re-score with sharper criteria. The Top 3 should be obvious — if not, the
matrix is muddy.

### Trap 6: ignoring assumptions with **explicit `[Unknown — …]`** in the canvas

Founders sometimes treat the explicit unknowns as "I'll figure it out
later" rather than "this is exactly what to test now." But the canvas
already flagged them — that's their value.

**Correction:** every `[Unknown — …]` in the canvas should automatically
appear in the assumption dump and get scored. If you find yourself omitting
one, ask why.

---

## A worked end-to-end example

**Setup:** a founder runs `validation-canvas` for a B2B SaaS targeting
"VPs of People at 200–1000 person tech companies" — the product is an
"AI coach for first-time managers." Here's a slice of the matrix:

| # | Assumption | Source | Risk | Impact | Reasoning |
|---|---|---|---|---|---|
| 1 | VPs of People feel acute pain about new-manager flameout | Stress Tests | High | High | Founder's intuition only; no interviews. If wrong, no buyer. **★** |
| 2 | New managers will use an AI coach 2+ times per week | Stress Tests | High | High | Engagement assumption — high churn product if wrong. **★** |
| 3 | Per-seat pricing at $25/mo will close | UVP block | High | High | No pricing tested. At $25 unit economics close; at $15 they don't. **★** |
| 4 | LinkedIn ads at < $200 CAC | Channels | Med | High | Comparable ed-tech tools hit $300–$400 CAC; founder hopes to beat. ● (filler if needed) |
| 5 | We can integrate with BambooHR / Workday in 4 weeks | Solution | Low | Med | Founder is ex-Workday eng; integration is well-understood. Backlog. |
| 6 | "Manager" is the right title to target (vs. "Lead", "Senior IC") | Customer Segments | Med | Low | Wrong title is fixable in 1 week of A/B; not strategic. |

**Top 3 selection:** assumptions 1, 2, 3 — all in the ★ corner. Backlog:
4, 5, 6.

**If only 2 ★s existed:** 4 would join (high impact + medium risk).
Assumption 6 would never make Top 3 (low impact).

---

## Output of Phase 2

The Phase 2 output (the `## Ranking Matrix` section in the Markdown plan)
includes every scored assumption, sorted by Top 3 first, then by impact +
risk. Reasoning column is required so the founder (and downstream
reviewers) can sanity-check the ranking.

Feed the Top 3 into Phase 3 (Hypothesis Rewriting) and Phase 4 (Test
Method Selection).
