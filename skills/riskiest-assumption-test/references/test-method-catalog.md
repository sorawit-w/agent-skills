# Test Method Catalog — Reference

The eight standard early-stage validation test methods, with **when to use**,
**when not to use**, **cost estimate**, **success-signal pattern**, and a
worked example for each. Read this before completing Phase 4 (Test Method
Selection).

The job of these methods is **cheap, fast falsification** — not statistical
significance, not optimization. The goal is to learn whether you should
invest more in the idea, not to A/B-test the precise CTA copy.

---

## 1. The 5-Interview Rule (customer interviews)

**Best for:** Desirability hypotheses. Specifically: *"the customer feels
this problem strongly enough to switch from their current alternative."*

**When to use:**
- You're early — pre-product or pre-pricing.
- The problem itself is uncertain (not just the solution).
- You can plausibly reach the segment in days, not months.

**When NOT to use:**
- The hypothesis is about willingness to pay (interviews are notoriously
  bad at predicting actual purchase behavior).
- The customer is hard to reach (e.g., regulated buyer, enterprise CISO) —
  the time cost balloons.
- You're really looking for confirmation (then it's not a test, it's
  theater).

**Cost:** 5–10 hours total (5 × 30–60 min interviews + scheduling +
synthesis).

**Success-signal pattern:**
- ≥ 4 of 5 interviewees confirm the problem unprompted (you describe the
  context but not the problem; they name the pain themselves).
- ≥ 3 of 5 describe a current workaround they actively dislike.
- ≥ 2 of 5 ask what you're building or when they can use it.

**Kill pattern:**
- ≤ 1 of 5 describes the problem unprompted.
- All 5 say "interesting, but…" with no follow-up energy.

**Worked example.**
*Hypothesis: "Solo legal-tech founders with $10K–$50K MRR feel the pain
of reconciling Stripe + bank statements monthly enough to pay $79/mo for
automation."*
*Method: 5-interview rule. Sample: 5 founders sourced via Indie Hackers and
the SaaS founders Slack. Format: 30-min Zoom, scripted but conversational.
Success: ≥ 4 confirm reconciliation pain unprompted; ≥ 2 ask about pricing.
Kill: ≤ 1 confirms unprompted, all describe "I just spend an hour at
month-end."*

**Common trap:** leading questions. *"Do you find reconciliation painful?"*
will get yes from anyone polite. *"Walk me through your last month-end
close — start to finish, what did you do?"* will get the truth.

---

## 2. Landing Page + Email Capture

**Best for:** Desirability hypotheses with a measurable conversion signal —
*"the segment is interested enough to leave their email."*

**When to use:**
- You can drive ~200–500 ICP-matched visitors cheaply (community,
  newsletter, paid ad to a tight segment).
- The UVP is testable in a single page (you can describe the offer in 2–3
  sentences without losing the gist).
- You're OK with email capture being a soft signal — it's not purchase
  intent.

**When NOT to use:**
- You can't drive targeted traffic. A landing page with no traffic teaches
  you nothing.
- The offer is genuinely complex (enterprise, regulated, multi-stakeholder).
- You're testing a price (use pre-sale instead).

**Cost:** 4–10 hours (page build + ad/email/community setup) + $50–$300 in
ad spend if going paid.

**Success-signal pattern:**
- ≥ 5–10% email-capture conversion among ICP-matched visitors (lower
  bound for "real interest" varies by industry; ≥ 5% is a useful baseline).
- ≥ 30% of email captures reply substantively when you follow up with one
  open question.

**Kill pattern:**
- < 1–2% conversion among ICP-matched visitors.
- Captures don't reply to follow-ups.

**Worked example.**
*Hypothesis: "VPs of Customer Support at 50–500 person SaaS companies want
an AI tool that auto-classifies inbound tickets by intent, urgency, and
required team."*
*Method: landing page with the 3-sentence UVP, 1 screenshot, "Get early
access" email form. Drive 300 visitors via LinkedIn ads targeted at the
title + industry. Success: ≥ 5% (15 emails) capture; ≥ 3 of those reply
with a one-line "what does it cost?" or "when can I try it?". Kill: < 1%
capture or zero substantive replies.*

**Common trap:** measuring capture without follow-up. Email capture is a
weak signal; the follow-up reply is what tells you whether intent is real.

---

## 3. Fake-Door Test

**Best for:** Desirability + early viability — *"the segment cares enough
about this specific feature to click 'buy' or 'sign up.'"*

**When to use:**
- The feature is well-defined and you want to test demand before building.
- You have an existing surface (current product, large mailing list, active
  community) to host the fake door.
- You can plausibly fulfill demand if the test surprises you (concierge
  fulfillment for the first 5–10 customers).

**When NOT to use:**
- You'd be lying without a real fallback. Showing a "Buy now" button and
  hard-redirecting to a 404 is unethical and damages trust.
- Your audience is small enough that the "got fooled" experience leaks.

**Cost:** 2–8 hours (button + post-click landing + email collection +
manual response template).

**Success-signal pattern:**
- ≥ 5–10% of users who see the fake door click it.
- ≥ 50% of clickers who enter the post-click flow leave their email or
  schedule a follow-up.

**Kill pattern:**
- < 1% click-through.
- High click but zero post-click engagement (people clicked out of
  curiosity, not intent).

**Worked example.**
*Hypothesis: "Existing users of our note-taking app want a one-click
'turn this note into a Slack post' integration enough to upgrade to the
$10/mo paid tier."*
*Method: add a "Send to Slack" button to the export menu. On click, show
"Coming soon — get notified" with email capture. Run for 7 days. Success:
≥ 5% of users who see the menu click; ≥ 50% of clickers leave email. Kill:
< 1% click or no email leaves.*

**Common trap:** running too short or with too small a pool. < 200 unique
viewers and the signal is noise.

---

## 4. Concierge MVP

**Best for:** Viability + feasibility hypotheses — *"the segment will pay
for the outcome, AND we can deliver it manually before automating."*

**When to use:**
- You can deliver the outcome by hand for the first 3–10 customers.
- The price is high enough that manual fulfillment is sustainable for the
  test (typically B2B with ACV ≥ $500/mo or transactional pricing ≥ $50).
- You want to learn what customers *actually* care about by being in the
  loop personally.

**When NOT to use:**
- The product is genuinely hard to deliver manually (search engine,
  real-time collaboration, etc.).
- You can't charge real money for ethical or regulatory reasons.
- The hypothesis is feasibility-only (use a Wizard of Oz instead).

**Cost:** 1–4 weeks of founder time, real money charged (the founder's
wage is "free" but bounded — > 10 customers and you need to automate).

**Success-signal pattern:**
- ≥ 3 of 5 first prospects pay full price.
- Customers re-purchase or refer (organic pull).
- The manual workflow surfaces 1–2 unexpected steps that change the
  product spec.

**Kill pattern:**
- ≤ 1 of 5 prospects pays.
- Customers cancel or churn after first delivery.
- The manual workflow surfaces that the value isn't actually deliverable.

**Worked example.**
*Hypothesis: "Solo bookkeepers will pay $300/mo for a service that
delivers their monthly client report (P&L + cash position + AR aging)
formatted to their template, with a 24hr turnaround."*
*Method: concierge MVP. Sell to 5 bookkeepers via direct outreach. Deliver
manually using a spreadsheet workflow. Success: ≥ 3 sign and pay first
month; ≥ 2 sign for month 2. Kill: ≤ 1 sign, or all churn after month 1.*

**Common trap:** under-pricing because "we're just testing." Real prices
test real demand. Discounts test how cheap something needs to be.

---

## 5. Wizard of Oz

**Best for:** Feasibility hypotheses — *"customers will use this thing if
the AI / automation / matching algorithm worked perfectly."*

**When to use:**
- You don't yet know if the *underlying technology* is feasible at
  acceptable quality, but you can fake it manually.
- You want to test product-shape and UX before investing in the engineering.
- The interaction is asynchronous or low-volume enough that humans can
  pretend to be the algorithm.

**When NOT to use:**
- The interaction is real-time + high-volume (chat at scale, search at
  scale).
- The hypothesis is desirability or viability — those need a real product
  signal, not a demo.

**Cost:** 3–10 hours setup (UI shell + manual fulfillment workflow) +
ongoing manual labor during the test window.

**Success-signal pattern:**
- Users return after first use without prompting.
- Users describe the experience as if it were real ("the AI is great at
  X but missed Y") — they're engaging with the simulated product, not the
  illusion.
- Manual fulfillment surfaces that the *real* technology only needs to
  hit a specific, achievable bar.

**Kill pattern:**
- Users don't return.
- Users describe the experience as confusing, slow, or off-target.
- Manual fulfillment surfaces that even with humans the output isn't useful
  — meaning the AI can't help either.

**Worked example.**
*Hypothesis: "Designers will use an AI tool that converts a Figma frame to
a working React component well enough to pay $20/mo."*
*Method: Wizard of Oz. Build a Figma plugin that "sends to AI" and silently
emails the founder. Founder writes the React by hand and emails it back
within 1hr. Run for 10 designers. Success: ≥ 6 of 10 use it more than once;
≥ 2 ask if they can pay. Kill: ≤ 2 use it more than once.*

**Common trap:** running the Wizard so long that the cost exceeds the
test value. > 2 weeks of human-as-AI fulfillment is a sign you should be
building or killing.

---

## 6. Pre-Sale

**Best for:** Viability hypotheses — *"the segment will pay [price] before
the product exists."*

**When to use:**
- The offering is concrete enough to describe in a one-pager.
- The price is high enough to matter ($500+ for B2B, $20+ for B2C — too
  low and the test isn't really validating willingness to pay).
- You have legal/refund clarity if the product doesn't ship.

**When NOT to use:**
- You can't legally or ethically take pre-payment (regulated industries).
- The price is so low that "yes I'll pay $9" is meaningless signal.
- The product is ill-defined (you'd be selling vapor).

**Cost:** 2–8 hours (one-pager + checkout / Stripe link + outreach
template) + the discomfort of asking for money.

**Success-signal pattern:**
- ≥ 3 of 10–20 prospects sign and pay full price (not deposit).
- Buyers ask "when does it ship?" and engage with the timeline.

**Kill pattern:**
- ≤ 1 of 20 buys at full price.
- Buyers want a 90% discount or only a 10% deposit.

**Worked example.**
*Hypothesis: "Engineering managers at 50–200 person companies will pay
$1500 upfront for a 6-week 'shipping habits' coaching cohort."*
*Method: pre-sale. One-pager describing the cohort syllabus, the coach,
and the start date. Stripe checkout link. Outreach to 30 EMs via LinkedIn.
Success: ≥ 5 sign and pay full price within 14 days. Kill: ≤ 2 sign or
"can I pay just $200 for now?"*

**Common trap:** discounting to "make the test work." A pre-sale that
required a 50% discount tells you the product can't sustain its target
price.

---

## 7. Smoke Test (Social-Media Pulse)

**Best for:** Early desirability hypotheses — *"the segment will react to
this concept publicly."* Lowest-cost test in the catalog.

**When to use:**
- You're earliest stage and want a directional read in days.
- You have an audience (yours or a community's) to post into.
- The concept is simple enough to communicate in a tweet / LinkedIn post /
  Reddit thread.

**When NOT to use:**
- The signal needs to be quantified rigorously (use landing page or
  fake-door instead).
- Your audience isn't your segment (e.g., posting a B2B accounting tool
  to a maker community gets you the wrong signal).

**Cost:** 30 min – 2 hours.

**Success-signal pattern:**
- Substantive comments (not "this is great") — questions about pricing,
  use cases, or "when?".
- DMs from ICP-shaped accounts asking for early access.
- ≥ 50% engagement rate (likes + comments / impressions) above your
  baseline for that channel.

**Kill pattern:**
- Polite likes, no substantive comments.
- "This already exists, look at X" with X being a credible competitor
  you didn't know about.
- DMs only from non-ICP accounts.

**Worked example.**
*Hypothesis: "Indie devs are interested in a CLI tool that auto-detects
unused dependencies and opens a PR to remove them."*
*Method: smoke test. Tweet thread with screenshots from a hand-built demo,
"who would use this?" call to action. Success: ≥ 5 substantive replies
from indie-dev accounts asking for the link or pricing. Kill: only
generic likes, no DMs.*

**Common trap:** treating likes as validation. Likes are vanity. Replies
asking "where can I buy?" are signal.

---

## 8. Expert Interview

**Best for:** Feasibility hypotheses in domains the founder doesn't deeply
know — *"this is technically/regulatorily/operationally possible at our
target cost and quality."*

**When to use:**
- The risk is *can we even build/deliver this*, not *do customers want it*.
- You can identify and reach 1–2 credible domain experts (former employees
  of incumbents, regulators, niche consultants).
- You can compensate the expert for their time (often $150–$500 for a 60
  min consult).

**When NOT to use:**
- The expert has incentive to discourage you (they sell a competing
  product, they're a defensive incumbent).
- The hypothesis is desirability — experts can't tell you whether
  customers want it.

**Cost:** 1–3 hours per interview + $150–$500 per expert.

**Success-signal pattern:**
- Expert names ≥ 2 specific paths to feasibility you hadn't considered.
- Expert validates the cost / quality target with reasoning, not just
  agreement.
- Expert names the 1–2 hardest sub-problems and they match your existing
  understanding.

**Kill pattern:**
- Expert names a regulatory or technical blocker you can't reasonably
  address.
- Expert says "you'd need a team of 10 and 18 months" when your plan was
  "one engineer in 3 months."
- Expert defers ("I don't really know") on the specific question — wrong
  expert, find another.

**Worked example.**
*Hypothesis: "We can deliver patient-record summarization for primary care
clinics in a way that meets HIPAA Business Associate Agreement
requirements without becoming a covered entity ourselves."*
*Method: expert interview. Two consults: (1) ex-Athenahealth privacy
counsel ($300 for 60 min), (2) practicing primary-care physician who has
deployed similar tools ($200 for 45 min). Success: both confirm BAA
pathway is feasible at our scale; physician names 2 specific use cases.
Kill: counsel names a regulatory blocker; or physician says "no clinic
would adopt this without [feature you can't build]."*

**Common trap:** confusing expert opinion with customer demand. Experts
predict what's possible; only customers tell you what they'll buy.

---

## How to pick the right method

| If your hypothesis is about… | Cheapest path |
|---|---|
| Whether the problem is real | 5-interview rule |
| Whether the segment will engage | landing page + email capture, or smoke test |
| Whether they'll click "buy" | fake-door |
| Whether they'll actually pay | pre-sale or concierge MVP |
| Whether the product can be built | Wizard of Oz, then technical spike |
| Whether we can navigate domain risk | expert interview |
| Whether a feature is missed in the current product | fake-door inside the existing surface |

**General rule:** if you can choose between a method that costs hours and
one that costs weeks, choose hours. The job is to *find out fast*, not to
*be thorough*.

---

## What this catalog deliberately does NOT include

- **Statistical A/B testing.** That's optimization, not validation.
  Out of scope at this stage.
- **Conjoint analysis / Van Westendorp / large surveys.** Too much
  apparatus for too little signal at idea-stage.
- **Customer-development sprints.** Lean methodology framework — useful
  but bigger than a single test method.
- **Full Lean Startup / Build-Measure-Learn cycles.** This skill plans
  ONE test at a time. The cycle is implicit (loop-back via
  `validation-canvas` update mode).
