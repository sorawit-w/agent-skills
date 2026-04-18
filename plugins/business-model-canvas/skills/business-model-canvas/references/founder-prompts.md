# Founder Prompts — Reference

The interview questions to use during Phase 1 (Discovery). Go in **customer-first
reasoning order** (not grid order). At most **3 questions per block** — if you need
more, either split the segment or mark the block as `[Unknown]` and move on.

Prompts are deliberately concrete. A prompt like "Who are your customers?" is too
broad and gets category answers ("SMBs"). The prompts below force specificity.

---

## 1. Customer Segments

1. Tell me about the most recent real person or company who'd want this. What do
   they do for a living, how many people are at their organization, and what city
   are they in?
2. When that person hits the problem you solve, what do they currently do instead?
   (If the answer is "nothing" — why hasn't this been a business?)
3. If you had to pick *one* segment for the next 12 months and ignore the others,
   which would it be, and what do you know about that segment that your competitors
   might not?

## 2. Value Propositions

1. For your flagship segment, complete this sentence in their words: "Before using
   us, I [painful current state]. After using us, I [specific new state]."
2. What does the segment currently use instead? What does your offering do 10× better
   than that — not 10% — and how would you prove it?
3. If the product vanished tomorrow, what specifically would the segment lose? (If
   the answer is abstract — "they'd lose efficiency" — dig.)

## 3. Channels

1. Where does your flagship segment spend attention when they're looking for
   solutions to this problem? Name a specific channel path, not "the internet."
2. What's the cheapest channel experiment you could run this quarter, and what
   would success look like in real numbers (CAC, signups, reply rate)?
3. If your primary channel's economics got 10× worse overnight (platform change,
   bidding war), what's your fallback?

## 4. Customer Relationships

1. How does your flagship segment expect to interact post-signup — self-serve,
   humans in the loop, dedicated account team, community?
2. Does the expected relationship match your price point? A $29/mo product usually
   can't support dedicated account management; enterprise won't accept pure self-serve.
3. What's the intended retention mechanism — switching cost, community stickiness,
   workflow lock-in, habit? Be specific.

## 5. Revenue Streams

1. How does money actually move? (Subscription monthly/annual, usage-based,
   transaction fee, licensing, marketplace take, ads, services.) What event
   triggers the charge?
2. What's the order-of-magnitude price per customer per month or per transaction?
   $10s, $100s, $1000s, $10Ks? Don't over-precise this — the range is enough.
3. Which revenue assumption is least validated so far — price level, willingness
   to pay, billing cadence, or contract structure?

## 6. Key Resources

1. What are the 3–5 resources this business can't function without? Distinguish
   between what you own (IP, data, brand) and what you rent (cloud, APIs).
2. Which resource is hardest to acquire — the one that bounds how fast you can grow?
3. What resource would take a well-funded competitor 18+ months to replicate? If
   nothing, the moat is speed — say so plainly.

## 7. Key Activities

1. What are the 3–5 activities this business must do well to make its model work?
   Tie each one to a Value Proposition or a Revenue Stream.
2. Which activity, if paused for 30 days, would kill the business?
3. Are any activities duplicating work a Key Partner could do better — or are any
   outsourced to a partner in a way that creates fragile dependency?

## 8. Key Partners

1. Name the 3–5 partners that de-risk, accelerate, or reduce the cost of a Key
   Activity. For each: what specific role do they play?
2. What happens if each critical partner walks, gets acquired, or changes terms
   tomorrow?
3. Which partner is most overrated on the current list? (It's often the one with
   the biggest logo and the least actual value delivered.)

## 9. Cost Structure

1. Working from the Key Activities and Resources you just named — what are the
   real cost drivers of *this* business, not generic startup overhead?
2. Which costs are fixed (rent, base salaries), which are variable (cloud,
   support, payments), and at 10× customers which one scales worst?
3. Are you operating cost-driven (commodity, minimize costs) or value-driven
   (accept higher costs for premium position)? Your Cost Structure should reflect
   the choice, not hedge it.

---

## Interview pacing

- Total time for a good interview: **45–75 minutes** for a first-pass canvas.
- If you exceed 15 minutes on a single block, the block is too broad (split it)
  or the founder doesn't know yet (mark `[Unknown — what-to-learn]` and move).
- Take *one* pass through all nine blocks before going back to refine. Do not
  perfect block 1 before starting block 2 — the later blocks will surface
  contradictions that force block 1 revisions anyway.

## When the founder doesn't know

This happens. It's not a failure of the interview — it's a useful output. Mark the
block:

```markdown
## Revenue Streams

- [Unknown — pricing model not yet tested. Hypothesis: per-seat SaaS at ~$40/seat/mo.]
```

Then add a row to Stress Tests: "We don't yet know whether per-seat pricing closes
at $40. To find out: a 10-call sales sprint against the flagship ICP in the next 2
weeks."

A canvas with honest unknowns is far more useful than a canvas filled with invented
confidence.
