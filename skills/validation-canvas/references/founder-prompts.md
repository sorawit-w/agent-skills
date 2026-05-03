# Founder Prompts — Reference

The interview questions to use during Phase 1 (Discovery). Two passes:

- **Pass 1: Lean Canvas** — 9 blocks in problem-and-customer-first order.
- **Pass 2: Value Proposition Canvas** — 6 blocks, right side (customer) first.

At most **3 questions per block** in Guided mode (less in Focused, often just
one in Compressed-with-Challenge). If you need more questions to get an answer,
either split the segment or mark the block `[Unknown]` and move on.

Prompts are deliberately concrete. A prompt like "Who are your customers?" is
too broad and gets category answers ("SMBs"). The prompts below force
specificity.

---

## Pass 1: Lean Canvas

### 1. Problem

1. What are the top 1–3 problems your customer experiences? Describe them in
   *their* words, not yours — what they would actually complain about.
2. For each problem, what does the customer use today to address it? Status
   quo, a competing product, a workaround, ignoring it? The current alternative
   is your real competition.
3. If you couldn't solve the most important problem on this list, would
   customers still buy something for the others? (If yes, you may have picked
   the wrong "most important.")

### 2. Customer Segments

1. Tell me about the most recent real person or company who'd want this. What
   do they do for a living, how many people are at their organization, and what
   city are they in?
2. Who's your *early adopter* — the segment you can actually reach in week 1
   (not the broader target you'd reach in year 3)? Name them by pattern, not
   demographics.
3. If you had to pick *one* segment for the next 12 months and ignore the
   others, which would it be, and what do you know about that segment that your
   competitors might not?

### 3. Unique Value Proposition

1. Complete this sentence in the segment's words: "Before using us, I [painful
   current state]. After using us, I [specific new state]."
2. Compress the above to one sentence — the UVP. Read it back to me as if you
   were one of the customers from segment 2. Does it land?
3. If a competitor copied your UVP word-for-word tomorrow, what would prevent
   them from winning your top segment? (This is a preview of the Unfair
   Advantage block, but answering now sharpens the UVP.)

### 4. Solution

1. What are the top 3 features that directly address the top 3 problems?
   Map them 1:1 to the Problems above.
2. Which one feature, if shipped alone, would prove the Problem ↔ Solution
   fit? That's your real MVP.
3. Are there features on this list that don't address a stated Problem? Either
   add the Problem they address, or cut the feature.

### 5. Channels

1. Where does your flagship segment spend attention when they're looking for
   solutions to this problem? Name a specific channel path, not "the internet."
2. What's the cheapest channel experiment you could run this quarter, and what
   would success look like in real numbers (CAC, signups, reply rate)?
3. If your primary channel's economics got 10× worse overnight (platform
   change, bidding war), what's your fallback?

### 6. Revenue Streams

1. How does money actually move? (Subscription monthly/annual, usage-based,
   transaction fee, licensing, marketplace take, ads, services.) What event
   triggers the charge?
2. What's the order-of-magnitude price per customer per month or per
   transaction? $10s, $100s, $1000s, $10Ks? Don't over-precise this — the
   range is enough.
3. What's the implied lifetime value? Rough math is fine — "$50/mo × 18 month
   avg retention = ~$900 LTV."

### 7. Cost Structure

1. Working from the Solution and Channels you just named — what are the real
   cost drivers of *this* business, not generic startup overhead?
2. Which costs are fixed (rent, base salaries), which are variable (cloud,
   support, payments), and at 10× customers which one scales worst?
3. What's your implied customer-acquisition cost (CAC), even at order of
   magnitude? Does CAC < LTV? If you don't know, that's a Stress Test.

### 8. Key Metrics

1. Name the 3–5 numbers that tell you whether the business is working. Not
   vanity (signups, downloads) — actionable (cohort retention, paid conversion
   rate, payback period).
2. For each metric, what's the rough target? "Activation = >50% of signups
   complete setup in first session" beats "monitor activation."
3. Which metric, if it dropped 50% next month, would tell you the business is
   broken? That's the canary.

### 9. Unfair Advantage

1. What do you have that a well-funded competitor would take 12+ months to
   replicate? (Insider info, distribution, audience, community ownership,
   engineering depth, network.)
2. Is your stated unfair advantage something you have *now*, or something
   you hope to develop? Be honest — hopes belong in Stress Tests, not in this
   block.
3. If you don't have a real unfair advantage yet, what's your *speed* moat —
   what can you do in 6 months that competitors won't see coming until you
   land it? (It's OK to leave this block partial in v1.)

---

## Pass 2: Value Proposition Canvas (run after Lean Canvas)

The VPC zooms into the Customer Segments ↔ UVP intersection. Right side first
(the customer's reality), then left side (your offering, mapped 1:1).

### 10. Customer Jobs

1. What functional jobs is the customer trying to get done? (e.g., "submit Q3
   sales tax", "onboard a new hire to the codebase").
2. What social jobs are at play? ("Look competent to my CFO", "be seen as
   on top of compliance".)
3. What emotional jobs? ("Not feel anxious during audit season", "feel in
   control of my finances".)

### 11. Customer Pains

1. What goes wrong, what's annoying, what they fear? Stay in customer
   experience, not in feature gaps.
2. Rank these pains by severity (mild annoyance / blocking obstacle / fear of
   bad outcome). Where's the high-intent pain?
3. For B2B: are these the *user's* pains, the *buyer's* pains, or both?
   The gap between user pain and buyer pain is where deals die.

### 12. Customer Gains

1. What outcomes does the customer want? Spread across required (table
   stakes), expected (industry norm), desired (what they'd say if asked),
   unexpected (delight).
2. Which gain would the customer brag about to a peer? That's the marketing
   angle.
3. Are any of these gains generic ("increased efficiency") that any product
   could claim? Sharpen them to be specific to this segment.

### 13. Products & Services

1. What's the actual offering today (not the roadmap)? Named features, named
   services, named support tiers.
2. Which is core, which is supporting? E.g., "core: AI contract review;
   supporting: redline export, audit log."
3. If you cut half of these, would you still relieve the top 3 Pains? If yes,
   which half is gold-plating?

### 14. Pain Relievers (mapped 1:1 to Pains above)

For *each* Pain on the customer side, ask:

1. How does the offering specifically reduce this pain? Describe the mechanism
   ("automatic daily reminders 3 days before deadline"), not just the outcome
   ("fixes the deadline problem").
2. Is the relief partial or complete? "Reduces from 4hr to 30min" is more
   credible than "eliminates."
3. **If a Pain has no Pain Reliever:** mark it explicitly as un-relieved.
   Un-relieved pains belong in Stress Tests.

### 15. Gain Creators (mapped 1:1 to Gains above)

For *each* Gain on the customer side, ask:

1. How does the offering specifically produce this gain? Describe the
   mechanism, not the outcome.
2. Is the gain a *required* outcome (table stakes) or *delight* (above the
   line)? Both belong, labelled.
3. **If a Gain has no Gain Creator:** mark it explicitly as un-created.
   Un-created gains belong in Stress Tests.

---

## Interview pacing

- **Guided mode:** ~60–90 min total. ~6–10 min per block.
- **Focused mode:** ~30–45 min total. ~3–5 min per block.
- **Compressed-with-Challenge mode:** ~15–20 min total. ~1–2 min per block,
  with sharp push-back on glib answers.

If you exceed the per-block budget, the block is too broad (split it) or the
founder doesn't know yet (mark `[Unknown — what-to-learn]` and move).

Take *one* pass through all blocks before going back to refine. Do not perfect
block 1 before starting block 2 — the later blocks will surface contradictions
that force block 1 revisions anyway.

## Mode-specific underweighted boxes

When you've inferred the founder's background, weight extra time on the boxes
they typically underweight:

- **Ex-engineers:** Channels and Cost Structure — engineers undervalue
  distribution and overestimate scaling efficiency.
- **Ex-designers:** Key Metrics and Customer Segments — designers think in
  craft, not in measurable activation/retention.
- **Ex-PMs:** Unfair Advantage and Problem — PMs are good at solutions, less
  practiced at naming why the customer feels the pain right now.
- **Ex-marketers / -salespeople:** Solution and Cost Structure — go-to-market
  folks tend to underweight what's actually shipped vs. promised.
- **First-time founders generally:** Unfair Advantage and Cost Structure —
  these are the blocks where wishful thinking shows up most.

## When the founder doesn't know

This happens. It's not a failure of the interview — it's a useful output.
Mark the block:

```markdown
### Revenue Streams

- [Unknown — pricing model not yet tested. Hypothesis: per-seat SaaS at
  ~$40/seat/mo.]
```

Then add a row to Stress Tests: "We don't yet know whether per-seat pricing
closes at $40. To find out: a 10-call sales sprint against the flagship ICP
in the next 2 weeks."

These Stress Tests then become the **direct seed for `riskiest-assumption-test`**
— the next step in the pipeline. The unknowns are the high-value assumptions
to test first.

A canvas with honest unknowns is far more useful than a canvas filled with
invented confidence.
