# Canvas Blocks — Reference

Deep definitions for each block in the **Lean Canvas (Maurya)** and the **Value
Proposition Canvas (Osterwalder)**. Each entry has four parts: **Definition**,
**What "good" looks like**, **Common failure modes**, and **Stress tests**.
Read this before drafting — it's what turns a template fill-in into a rigorous
artifact.

This skill ships *both* canvases as a single artifact. They overlap deliberately:
the VPC re-asks Customer Segments + UVP from the customer's perspective, which
surfaces gaps the Lean Canvas alone misses.

---

## Part 1 — Lean Canvas (9 blocks, problem-and-customer-first order)

1. [Problem](#1-problem)
2. [Customer Segments](#2-customer-segments)
3. [Unique Value Proposition](#3-unique-value-proposition)
4. [Solution](#4-solution)
5. [Channels](#5-channels)
6. [Revenue Streams](#6-revenue-streams)
7. [Cost Structure](#7-cost-structure)
8. [Key Metrics](#8-key-metrics)
9. [Unfair Advantage](#9-unfair-advantage)

---

### 1. Problem

**Definition:** The top 1–3 problems the customer faces that the business is
positioned to solve. *Existing alternatives* (what they currently use) belong
here too — the alternative is your real competitor, not "no one does this."

**What good looks like:**
- 1–3 problems max, each in the customer's language ("we lose 4 hours a week
  reconciling invoices manually"), not the founder's frame ("inefficient AP
  process").
- Each problem paired with a current alternative — what they do today,
  how it fails them.
- Problems the customer *would describe unprompted* — not problems the founder
  has decided they should care about.

**Common failure modes:**
- "There's no good solution" without saying what people use today. Status quo
  is always an alternative — even paper, even a spreadsheet, even ignoring the
  problem.
- Problems described in solution language ("they need an AI tool to…") instead
  of customer language ("they spend 4 hours a week on…").
- Listing 7+ problems. Three is the cap; if you can't pick three, the segment
  isn't focused.

**Stress tests:**
- Could you walk into a room of 10 candidate customers and have them confirm
  these are their top 3 problems? Or are these the top 3 *you* would care about
  if you were them?
- For each problem, what is the customer paying (in time, money, or attention)
  to live with it today? If the answer is "not much," the problem isn't
  expensive enough to switch from.

---

### 2. Customer Segments

**Definition:** The distinct groups of people or organizations the business
serves. Distinct means they need different value propositions, reach through
different channels, or have materially different willingness-to-pay. Lean
Canvas asks you to name **target customers** AND **early adopters** — they're
not the same.

**What good looks like:**
- Specific enough that the founder can name real candidates. Not "SMBs" — "5–25
  person legal-tech firms in the US northeast that currently use paper intake
  forms."
- Early adopters named separately from target customers. Early adopters are
  who you can actually reach in week 1.
- At most 3 segments in v1. More than that and the business is trying to be
  everything.

**Common failure modes:**
- "Everyone who [broad need]." That's a total market, not a segment.
- Segments defined by demographics when behavior is what matters.
- Confusing *user* (who uses the product) with *buyer* (who pays). For B2B this
  distinction is usually load-bearing.
- No early-adopter sub-segment named. Without one, the canvas hides the question
  "who can we get to month one?"

**Stress tests:**
- If you had to pick only one segment for the next 12 months, which would it be?
- Who's the *first 10 paying customers*? Name them by pattern, even if not
  individually.

---

### 3. Unique Value Proposition

**Definition:** A single, clear, compelling message that turns an unaware visitor
into an interested prospect. It states *why you are different* AND *worth
paying attention to*. Lean Canvas keeps this to one statement — not a list.

**What good looks like:**
- One sentence. Maximum two.
- Written in the *segment's language*, not the founder's.
- Names a specific outcome the customer cares about, not a feature list.
- Pairs nicely with a "high-concept pitch" sub-line (e.g., "Flickr for video"),
  which is optional but useful.

**Common failure modes:**
- Feature list masquerading as a UVP ("we have real-time dashboards, SSO,
  integrations, mobile apps…"). Features aren't value.
- Comparatives with no basis. "10× faster than competitors" without a source
  is marketing, not a claim.
- Different UVPs implied for different segments without explicit acknowledgment
  — usually means the segments aren't truly distinct.

**Stress tests:**
- Read the UVP cold to someone in the segment. Do they understand it without
  asking a follow-up?
- If the product disappeared tomorrow, what specifically would the segment lose?
  That's the real UVP.

---

### 4. Solution

**Definition:** The top 3 features that address the top 3 problems — directly
mapped, 1:1. Not a product roadmap. Not a feature list. The minimum that proves
the UVP.

**What good looks like:**
- 1–3 features, each tied to a specific Problem above.
- Described as outcomes (what the customer can now do), not implementations.
- Sized to be testable in weeks, not quarters. Lean Canvas is about the
  smallest thing that proves the model.

**Common failure modes:**
- Long feature lists ("real-time, multi-tenant, enterprise-grade…") — that's
  the gold-plating problem.
- Solutions with no matching Problem. If a feature doesn't address a stated
  problem, it doesn't belong here yet.
- Implementation-language solutions ("a Postgres-backed FastAPI service") that
  the customer doesn't care about.

**Stress tests:**
- Could you ship just the top 1 feature and still test the Problem ↔ Solution
  fit? If yes, that's your real MVP.
- Is any feature here addressing a Problem you didn't list? Either add the
  Problem, or cut the feature.

---

### 5. Channels

**Definition:** How the business reaches, communicates with, and delivers to
each Customer Segment. In Lean Canvas, this is *more skewed toward distribution*
than BMC's broader Channels block — the question is "how do customers
**discover** you?"

**What good looks like:**
- Concrete channel *paths*, not channel categories. "Paid LinkedIn ads
  targeting the 'VP of Ops' title at 50–200 person SaaS companies" beats
  "digital marketing."
- Different channels for different segments.
- Owned vs. partner channels distinguished (owned = direct control; partner =
  leverage their distribution).
- Free channels (community, content, SEO) named alongside paid — early-stage
  startups usually can't afford only paid.

**Common failure modes:**
- "SEO and content marketing" with no specific topic, keyword, or funnel.
- Assuming the channel that worked for a well-known competitor will work here
  — their moat is often *on the channel*, not in the product.
- Ignoring distribution as a separate skill — "we'll figure out marketing
  later" is a death sentence at this stage.

**Stress tests:**
- What's the cheapest channel to test this quarter, with what success metric?
- If the primary channel went away (algorithm change, platform policy), what's
  the fallback?

---

### 6. Revenue Streams

**Definition:** The cash the business generates from each Customer Segment.
Structural, not quantitative — *how money flows*, not *how much*. Lean Canvas
asks you to name pricing model AND lifetime-value (LTV) order-of-magnitude.

**What good looks like:**
- Named payment *mechanic*: subscription (monthly/annual), usage-based,
  transactional (per-X), licensing, marketplace take rate, ads, services.
- Clear trigger: what event causes the charge.
- Price order-of-magnitude: $10s, $100s, $1000s, $10Ks per month/transaction.
  Not a precise number — a range that keeps the unit economics honest.
- Implied LTV. If avg customer pays $50/mo and stays 18mo, LTV ~$900.

**Common failure modes:**
- "Freemium" with no path from free to paid.
- Two revenue streams that cannibalize each other.
- Price points that imply unit economics the cost structure can't sustain.
- "We'll figure out monetization later." For a Lean Canvas, that's a Stress
  Test, not a placeholder.

**Stress tests:**
- If the top segment pays you nothing for the first 6 months, can the business
  survive?
- At your stated price, how many customers do you need to break even? Is that
  realistic in your market?

---

### 7. Cost Structure

**Definition:** The costs incurred to operate the business. Structural, not
quantitative — *what drives costs*, not what they sum to. In Lean Canvas, this
is paired conceptually with Revenue to surface unit economics.

**What good looks like:**
- Driven from Solution + Channels — a cost should trace to a specific feature
  or distribution effort.
- Fixed vs. variable distinction, labelled.
- Named 1–2 *cost drivers* — things that scale cost non-linearly (e.g.,
  "support cost per customer", "API spend per active user").
- Customer-acquisition cost (CAC) order-of-magnitude. If you don't know CAC,
  Stress Tests should call that out.

**Common failure modes:**
- Generic startup cost list: "salaries, rent, marketing, legal." True of every
  business — doesn't illuminate anything.
- Ignoring variable costs that scale with customers.
- CAC ≥ LTV without anyone noticing. Lean Canvas's job is to make this
  arithmetic visible.

**Stress tests:**
- At 10× customers, which cost line scales worst? That's the bottleneck on
  margin.
- Is your implied CAC < implied LTV? If not, the model doesn't close.

---

### 8. Key Metrics

**Definition:** The key activities you measure to know if the business is
working. Pirate metrics (AARRR — Acquisition, Activation, Retention, Revenue,
Referral) is one common framing; pick the 3–5 numbers that actually tell you
something.

**What good looks like:**
- 3–5 metrics max. More than that and you're not measuring, you're cataloguing.
- Each metric tied to a specific stage (top of funnel, activation, retention,
  monetization).
- Each metric has an implied target ("activation = >50% of signups complete
  setup in first session").
- Distinguish *vanity metrics* (cumulative signups, page views) from
  *actionable metrics* (cohort retention, paid conversion rate).

**Common failure modes:**
- Vanity metrics dressed as KPIs (signups, downloads, social followers).
- Metrics with no target — "monitor MRR" doesn't tell you if it's working.
- Output metrics (revenue) without input metrics (the activities that drive
  revenue). Both belong.

**Stress tests:**
- Which metric, if it dropped 50% next month, would tell you the business is
  broken?
- Are any metrics impossible to measure with the current product? Add the
  instrumentation work to your Solution if so.

---

### 9. Unfair Advantage

**Definition:** Something that **cannot be easily copied or bought**. "We work
harder" is not an unfair advantage. Real unfair advantages are rare; many
canvases legitimately leave this block partial in v1 — *and that's data.*

**Examples of real unfair advantages:**
- Insider information (you worked in the segment for 10 years).
- The right "expert" endorsements (proprietary distribution).
- A dream team with deep domain ties.
- Personal authority (a founder with an audience the segment trusts).
- A large network already connected to the segment.
- Community ownership (you built and run the gathering place for this segment).
- An existing customer base you're moving to a new offering.
- Engineering depth that competitors lack (if it's truly hard, not "we use
  Rust").
- A patent (rare, often weak, but counts when real).
- SEO ranking that took years to build.

**What good looks like:**
- Something a well-funded competitor would take 12+ months to replicate.
- Honest about whether the advantage is *speed* (we'll outrun them), *moat*
  (they can't catch us), or *empty* (we don't have one yet).

**Common failure modes:**
- "Great team" / "first-mover advantage" / "patent pending" — these are
  cliches, not advantages.
- Naming an advantage that the founder doesn't actually have.
- Confusing a "hard" thing with an "unfair" one. Lots of things are hard;
  unfair means competitors can't get there.

**Stress tests:**
- If a Series-B-funded competitor copied your product tomorrow, what would
  prevent them from winning your top segment?
- Is your stated unfair advantage something you have *now*, or something you
  hope to develop? Be honest — hopes belong in Stress Tests.

---

## Part 2 — Value Proposition Canvas (6 blocks, two sides)

The VPC zooms into the **Customer Segments ↔ UVP** intersection from Lean
Canvas. Right side first (the customer's reality); then left side (your
offering, mapped 1:1 to the right).

10. [Customer Jobs](#10-customer-jobs)
11. [Customer Pains](#11-customer-pains)
12. [Customer Gains](#12-customer-gains)
13. [Products & Services](#13-products--services)
14. [Pain Relievers](#14-pain-relievers)
15. [Gain Creators](#15-gain-creators)

---

### 10. Customer Jobs

**Definition:** The tasks the customer is trying to get done — functional,
social, and emotional. "Jobs to be done" framing (Christensen).

**What good looks like:**
- Mix of functional ("file my taxes correctly"), social ("look competent to
  my CFO"), and emotional ("not feel anxious during audit season") jobs.
- Stated from the customer's perspective in the customer's language.
- Sized appropriately — "run my business" is too broad; "submit Q3 sales tax"
  is right.

**Common failure modes:**
- Only functional jobs listed. Social and emotional drive a lot of B2C and
  much of B2B; ignoring them undersells the offering.
- Jobs that are really features in disguise ("use our dashboard" — that's not
  a job).
- "Save time / save money" as a job. Those are gains, not jobs.

**Stress tests:**
- If the customer woke up tomorrow and the job were already done magically,
  what would they actually do with that time/headspace?
- Which job is the *currently most painful* — the one that would tip a switch
  to a new tool?

---

### 11. Customer Pains

**Definition:** Bad outcomes, risks, and obstacles the customer encounters
related to the jobs. "What goes wrong, what's annoying, what they fear."

**What good looks like:**
- Specific, observed pains — not pains the founder *imagines* customers have.
- Mix of severity (mild annoyance → blocking obstacle → fear of bad outcome).
- Pains expressed as *experiences*, not as missing features ("I'm afraid I'll
  miss a deadline" not "no calendar reminders").

**Common failure modes:**
- All pains are at the same severity (usually all "moderately annoying").
- Pains framed as feature gaps in your product instead of customer-side
  experiences.
- Pains the customer would not actually name unprompted.

**Stress tests:**
- Which pain causes the customer to *do something about it* (search, complain,
  switch)? That's the high-intent pain.
- Are any of these pains actually pains *for the buyer*, while the user has
  different ones? In B2B this gap is often where deals die.

---

### 12. Customer Gains

**Definition:** Outcomes and benefits the customer wants — required, expected,
desired, or unexpected.

**What good looks like:**
- Spread across all four levels: required (must work), expected (industry
  norm), desired (what they'd say if asked), unexpected (delight).
- Quantifiable where possible ("20% faster close" not "faster close").
- Not just inverses of the Pains — gains often include things customers
  wouldn't think to ask for.

**Common failure modes:**
- Only expected/desired gains listed. The required ones (table stakes) get
  ignored — and missing table stakes kills deals.
- Gains that are really features ("our API is RESTful"). Customers don't
  desire technical implementations.
- Generic gains ("increased efficiency") that any product could claim.

**Stress tests:**
- If you delivered every gain on this list, would the customer actually pay
  the price you're charging? If not, the gains aren't worth what you think.
- Which gain would the customer brag about to a peer? That's the marketing
  angle.

---

### 13. Products & Services

**Definition:** The offering — what the customer hires to do the jobs. List
products, services, support, related deliverables.

**What good looks like:**
- Concrete: named features, named services, named support tiers.
- Sized to MVP, not to the full vision. VPC is about today's offering, not
  the roadmap.
- Distinguishes core from supporting (e.g., "core: AI contract review;
  supporting: redline export, audit log").

**Common failure modes:**
- Vision-language ("a platform for…") rather than concrete deliverables.
- Listing the roadmap, not the current offering.
- Bundling so loosely that the offering doesn't relieve any specific pain.

**Stress tests:**
- For each product/service listed: is it actually delivered today, or
  aspirational?
- Could you cut half of these and still relieve the top 3 Pains?

---

### 14. Pain Relievers

**Definition:** **For each Pain on the right side, name how the offering
relieves it.** This is the explicit 1:1 mapping that surfaces gaps. If a
Pain has no Reliever, the offering doesn't address it — that's a red flag.

**What good looks like:**
- Each Pain Reliever maps to a specific Pain by name.
- Reliever describes *how* the pain reduces, not just that it does ("automatic
  daily reminders 3 days before deadline" not "fixes the deadline problem").
- Honest about partial relief — "reduces from 4hr to 30min" is more credible
  than "eliminates."

**Common failure modes:**
- Generic relievers ("makes it easier") that don't tie to a specific pain
  mechanism.
- Relievers that imply unbuilt features.
- Pain Relievers without corresponding Pains. If you have a reliever for a pain
  you didn't list, either add the pain or cut the reliever.

**Stress tests (mandatory fit check):**
- For every Pain on the right side, name the specific Pain Reliever. Pains
  without Relievers are red flags — they belong in Stress Tests.
- For every Pain Reliever on the left side, name the specific Pain it
  addresses. Relievers without Pains are gold-plating.

---

### 15. Gain Creators

**Definition:** **For each Gain on the right side, name how the offering
produces it.** Same 1:1 mapping rule as Pain Relievers.

**What good looks like:**
- Each Gain Creator maps to a specific Gain by name.
- Creator describes *the mechanism*, not the outcome.
- Honest about which gains are *required* (table stakes) vs. *delight*
  (above the line).

**Common failure modes:**
- Generic gain creators ("delivers better outcomes").
- Gain Creators implying unbuilt features.
- Creators without corresponding Gains, or vice versa.

**Stress tests (mandatory fit check):**
- For every Gain on the right side, name the specific Gain Creator. Gains
  without Creators are red flags — they belong in Stress Tests.
- For every Gain Creator on the left side, name the specific Gain it
  addresses.

---

## How the blocks talk to each other

The **Consistency Check** in Phase 2 of SKILL.md enforces these relationships:

**Lean Canvas:**
- Every **Problem** ↔ at least one **Customer Segment** that genuinely feels it
- Every **UVP** is written in the **Customer Segments**' language
- Every **Solution** feature ↔ a stated **Problem**
- Every **Channel** is plausible for the **Customer Segment** it reaches
- **Revenue Streams** ↔ value the **UVP** creates
- **Cost Structure** reflects the cost drivers of **Solution + Channels**

**VPC fit:**
- Every **Pain** ↔ a **Pain Reliever** (or explicitly marked as un-relieved)
- Every **Gain** ↔ a **Gain Creator** (or explicitly marked as un-created)

**Cross-canvas:**
- The Lean Canvas's UVP should compress to a single sentence that the VPC
  Pain Relievers + Gain Creators would, taken together, produce.

If any of these fails, the canvas is internally inconsistent. Revise, don't
rationalize.

---

## What this skill explicitly does NOT include

- **9-block Osterwalder BMC.** Wrong altitude — that's a Series-A operating
  plan tool. Use `team-composer` with `@startup_strategist` for that.
- **SWOT / Porter's Five Forces / Wardley Mapping.** Wrong altitude / wrong
  stage / overlap with `startup-grill`. Competitive analysis lives in the
  grill, not in the canvas.
- **Financial projections.** Revenue Streams and Cost Structure here are
  *structural*. P&L, cohort modeling, and sensitivity analysis are downstream.
