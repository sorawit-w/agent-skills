# Nine Blocks — Reference

Deep definitions for each Business Model Canvas block. Each entry has four parts:
**Definition**, **What "good" looks like**, **Common failure modes**, and **Stress tests**.
Read this before drafting — it's what turns a template fill-in into a rigorous artifact.

The nine blocks are filled in **customer-first reasoning order**, not grid order:

1. [Customer Segments](#1-customer-segments)
2. [Value Propositions](#2-value-propositions)
3. [Channels](#3-channels)
4. [Customer Relationships](#4-customer-relationships)
5. [Revenue Streams](#5-revenue-streams)
6. [Key Resources](#6-key-resources)
7. [Key Activities](#7-key-activities)
8. [Key Partners](#8-key-partners)
9. [Cost Structure](#9-cost-structure)

---

## 1. Customer Segments

**Definition:** The distinct groups of people or organizations the business serves.
Distinct means they need different value propositions, reach through different channels,
or have materially different willingness-to-pay.

**What good looks like:**
- Specific enough that the founder can name real candidates. Not "SMBs" — "5–25 person
  legal-tech firms in the US northeast that currently use paper intake forms."
- Segments are *separable*. If you'd pitch them identically, they're one segment.
- At most 3 segments in v1. More than that and the business is trying to be everything.

**Common failure modes:**
- "Everyone who [broad need]." No, that's a total market, not a segment.
- Segments defined by demographics when behavior is what matters. "Millennials" rarely
  explains purchase behavior; "people who switched from X to Y in the last 12 months"
  often does.
- Confusing *user* (who uses the product) with *buyer* (who pays). For B2B this
  distinction is usually load-bearing.

**Stress tests:**
- If you had to pick only one segment for the next 12 months, which would it be and why?
- What does this segment currently use instead? If the answer is "nothing," they
  probably don't feel the pain strongly enough to switch.

---

## 2. Value Propositions

**Definition:** The bundle of products/services that creates value for a specific
segment. Value = problem solved OR job done better/cheaper/faster/safer than the
alternative.

**What good looks like:**
- Written in the *segment's language*, not the founder's. If your segment wouldn't
  say "orchestrating agentic workflows," neither should the value prop.
- Names the pain, not just the solution. "Saves 4 hours a week of manual contract
  redlining" beats "AI-powered contract review platform."
- Maps 1:1 or 1:many to Customer Segments. Every segment has at least one VP; every
  VP serves at least one segment.

**Common failure modes:**
- Feature list masquerading as a value prop ("we have real-time dashboards, SSO,
  integrations, mobile apps…"). Features aren't value.
- Same VP for three different segments. If it really works for all of them, the
  segments probably aren't distinct.
- Comparatives with no basis. "10× faster than competitors" without a source is
  marketing, not a claim.

**Stress tests:**
- What does the segment currently do instead, and why is this 10× better (not 10%)?
- If the product disappeared tomorrow, what specifically would the segment lose?

---

## 3. Channels

**Definition:** How the business reaches, communicates with, and delivers to each
Customer Segment. Includes awareness, evaluation, purchase, delivery, and post-sale.

**What good looks like:**
- Concrete channel *paths*, not channel categories. "Paid LinkedIn ads targeting the
  'VP of Ops' title at 50–200 person SaaS companies" beats "digital marketing."
- Different channels for different segments, because segments live in different places.
- Owned vs. partner channels are distinguished (owned = direct control; partner =
  leverage their distribution).

**Common failure modes:**
- "SEO and content marketing" with no specific topic, keyword, or funnel mapped out.
- Assuming the channel that worked for a well-known competitor will work here. It
  often won't — their moat is often *on the channel*, not in the product.
- Single-channel dependence with no acknowledgment of platform risk.

**Stress tests:**
- What's the cheapest channel to test this quarter, and what would success look like
  in real numbers?
- If the primary channel's unit economics 10×'d worse (bidding war, algorithm change,
  platform policy), what's the fallback?

---

## 4. Customer Relationships

**Definition:** The kind of relationship the business establishes with each segment.
Spans self-serve, automated, personal assistance, dedicated account, communities,
co-creation.

**What good looks like:**
- Matches the segment's expectations. Enterprise buyers expect dedicated humans;
  prosumer SaaS users expect self-serve.
- Matches the price point. A $29/mo product cannot economically support dedicated
  account management.
- Matches the retention goal. High-churn segments need community or switching-cost
  mechanisms; low-churn enterprise can lean on account teams.

**Common failure modes:**
- "Great customer service" as a relationship type. That's a quality bar, not a
  relationship model.
- White-glove onboarding attached to a self-serve price point (unit economics
  don't close).
- Community as a checkbox. Building and moderating a real community is a full-time
  job and belongs in Key Activities if it's load-bearing.

**Stress tests:**
- For the flagship segment: is the relationship type economically viable at the
  current price point?
- How does the relationship change when you 10× the number of customers? Does anything
  break?

---

## 5. Revenue Streams

**Definition:** The cash the business generates from each Customer Segment. Structural,
not quantitative — how money flows, not how much.

**What good looks like:**
- Named payment *mechanic*: subscription (monthly/annual), usage-based, transactional
  (per-X), licensing, marketplace take rate, ads, services.
- Clear trigger: what event causes the charge (signed contract, first usage, renewal
  anniversary, transaction close).
- Price order-of-magnitude: $10s, $100s, $1000s, $10Ks per month/transaction. Not a
  precise number — a range that keeps the unit economics honest.

**Common failure modes:**
- "Freemium" with no path from free to paid. Who upgrades, when, why?
- Two revenue streams that compete with each other (e.g., usage-based and unlimited-flat
  for the same segment — one cannibalizes the other).
- Revenue from Customer Segment A being subsidized by unrelated Segment B without
  anyone noticing.

**Stress tests:**
- If the top segment pays you nothing for the first 6 months (trial, pilot), can the
  business survive?
- Which revenue stream has the least price discovery done? That's the one most likely
  wrong.

---

## 6. Key Resources

**Definition:** The most important assets required to make the business model work.
Physical, financial, intellectual (IP, brand, data, proprietary methods), human.

**What good looks like:**
- Resources that *specifically* enable the Key Activities and Value Propositions.
  Generic lists ("a great team", "funding") are not resources, they're wishes.
- Named scarcity: which resource is hardest to acquire? That's the one that bounds
  the business's growth.
- Distinction between resources you own vs. resources you rent (cloud, API partners,
  contract labor).

**Common failure modes:**
- Listing every possible resource instead of the 3–5 that actually matter.
- Conflating resources with activities. "Marketing" is an activity; a "proprietary
  audience of 50K newsletter subscribers" is a resource.
- Missing the most important one because it's obvious to the founder (e.g., founder's
  personal brand, personal network, accumulated domain knowledge).

**Stress tests:**
- If you lost the founder's network on day one, what else would carry the business?
- What's the resource that would take a well-funded competitor 18+ months to replicate?
  (If there isn't one, the moat is speed-based — name that honestly.)

---

## 7. Key Activities

**Definition:** The most important things the business must *do* to make its model
work. Production, problem-solving, platform/network operation, distribution.

**What good looks like:**
- Activities tied directly to delivering the Value Propositions and running the
  Channels. Not a to-do list of everything the team does.
- Prioritized. If forced to do only 2, which 2 are they?
- Distinction between *product* activities (what the customer perceives) and
  *business* activities (what keeps the lights on) — both belong, labelled.

**Common failure modes:**
- "Build a great product" as an activity. That's the outcome, not the activity —
  what specific engineering / research / design / ops work does it require?
- Activities that imply resources the Key Resources block doesn't have.
- Ignoring non-product activities that the business secretly depends on (sales ops,
  regulatory filings, supply chain, community moderation).

**Stress tests:**
- Which activity, if paused for 30 days, would kill the business? That's the one
  worth automating or hiring against first.
- Are any activities duplicated by a Key Partner? If so, why do both in-house?

---

## 8. Key Partners

**Definition:** The network of suppliers, partners, and allies that make the business
model work. Not a logo collection — each partner earns its seat by de-risking, reducing
cost, or enabling an activity the business can't do alone.

**What good looks like:**
- Named role per partner. "AWS — infrastructure supplier" is fine; "strategic
  partnership with Acme Corp" is not (strategic how?).
- Partner dependencies that are *intentional* (e.g., Stripe handles payments because
  building your own PSP is 3 years of work).
- Named failure mode per critical partner: what happens if they walk, get acquired,
  change terms?

**Common failure modes:**
- Listing partners the business doesn't actually have yet as if they were signed.
- Missing the partner whose API or platform the business secretly depends on.
- Treating a supplier with a generic, easily-replaced offering (e.g., a commodity
  cloud provider) as a "strategic partner."

**Stress tests:**
- If the top 3 partners each 2×'d their price, does the business still work?
- Is any Key Activity fully outsourced to a single partner with no alternative?
  That's platform risk — name it.

---

## 9. Cost Structure

**Definition:** The costs incurred to operate the business model. Structural, not
quantitative — what drives costs, not what they sum to.

**What good looks like:**
- Driven from the Key Activities and Resources blocks. A cost in this block should
  trace back to a specific activity or resource.
- Fixed vs. variable distinction, labelled.
- Named 1–2 *cost drivers* — the things that scale cost non-linearly (e.g., "support
  cost per customer", "cloud spend per active user").
- Cost-driven (minimize costs, commoditized offering) vs. value-driven (accept higher
  costs for premium positioning) orientation stated.

**Common failure modes:**
- Generic startup cost list: "salaries, rent, marketing, legal." True of every business
  — doesn't illuminate anything.
- Ignoring variable costs that scale with customers (support, infra, compliance) and
  assuming a SaaS gross margin that doesn't actually hold.
- Missing regulatory or compliance costs in regulated domains.

**Stress tests:**
- At 10× customers, which cost line scales worst? That's the bottleneck on margin.
- Is there a Key Activity that's expensive but doesn't clearly enable a Value
  Proposition or Revenue Stream? That's a candidate to cut.

---

## How the blocks talk to each other

The **Consistency Check** in Phase 2 of SKILL.md enforces these relationships:

- Every **Customer Segment** ↔ at least one **Value Proposition** (in segment's language)
- Every **Value Proposition** ↔ at least one **Revenue Stream** (or explicit loss-leader note)
- Every **Channel** is plausible for the **Segment** it reaches
- Every **Key Activity** has the **Key Resources** it needs
- **Cost Structure** reflects the cost drivers of the **Key Activities**
- Every **Key Partner** de-risks or accelerates at least one **Key Activity**

If any of these fails, the canvas is internally inconsistent. Revise, don't rationalize.
