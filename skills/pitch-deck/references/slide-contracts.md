# Slide Contracts — Reference

Per-slide required slots, anti-patterns, and the investor-read-test question each
slide must pass. Read this before writing any slide.

A **required slot** is content the deck cannot render without. If it's not filled,
either the founder answers it or the slot blocks shipping via a warning slide at
position 0 (see SKILL.md §Phase 3 Step 2).

A **cardinal slot** is a required slot whose absence is one of the four cardinal
sins. Cardinal slots are hard gates — the deck is not shippable without them.

---

## Slide 1 — Title

**Core question:** What is this company and who's pitching?

**Required slots:**
- Company name
- One-line tagline (≤10 words, ≤80 characters, plain language)
- Founder name(s) + role(s)
- Date of deck (month/year at minimum)
- Contact: email or scheduling link

**Cardinal slots:** company name, tagline.

**Anti-patterns:**
- Tagline is a mission statement ("democratizing X") instead of what the product does
- Tagline uses three buzzwords in a row ("AI-powered, blockchain-enabled, decentralized")
- No contact info — investor has to dig to follow up

**Investor-read-test question:** *In five seconds, can I explain to a colleague what
this company does?* If not, the tagline is too abstract.

---

## Slide 2 — Problem

**Core question:** Who hurts, how much, and why hasn't it been solved?

**Required slots:**
- Named customer segment (not "SMBs" — a specific kind of SMB, e.g., "single-location
  dental practices with 3–5 operatories")
- The pain, in the customer's own language (quote a real customer if you have one)
- The current workaround — what they're doing today to cope (spreadsheets, hiring
  someone, living with it)
- Why the pain is bigger now than 5 years ago (the "why now" seed)

**Cardinal slots:** named segment, pain described in customer language.

**Anti-patterns:**
- "There's no good solution" — there always is; it's usually the status quo the
  customer already pays for
- Pain described in founder-speak, not customer-speak ("leveraging fragmented data
  silos" vs "I have to copy-paste between 4 tools every Monday")
- Solving a "nice to have" disguised as a "must have" — if the workaround works OK,
  the pain is not urgent

**Investor-read-test question:** *Would a customer in this segment, reading this
slide, nod and say "yes, exactly"?*

---

## Slide 3 — Solution

**Core question:** What do we do, in one sentence?

**Required slots:**
- One-sentence description of the solution (≤25 words)
- The key insight or unlock — why this approach works now when prior attempts didn't
- One concrete outcome in customer terms (time saved, revenue gained, risk reduced)

**Cardinal slots:** one-sentence description, concrete outcome.

**Anti-patterns:**
- Solution described as a feature list rather than an outcome
- "AI-powered" or "ML-driven" without specifying what the AI/ML actually does
- Solution doesn't obviously connect to the pain on slide 2

**Investor-read-test question:** *Does this solution read as an obviously-better
response to the pain on the previous slide?*

---

## Slide 4 — Market

**Core question:** How big is this, credibly, with SAM and SOM — not just TAM?

**Required slots:**
- **TAM** (total addressable market) — global or broad, with a source
- **SAM** (serviceable addressable market) — the subset you could reach with the
  current product and channels
- **SOM** (serviceable obtainable market) — the realistic share in years 1–3
- Bottom-up calculation showing how SOM was derived (e.g., "10,000 dental practices
  × $4,800 ARR × 2% capture = $960K ARR year 3")
- Source(s) for the numbers (industry report, public data, primary research)

**Cardinal slots:** TAM, SAM, SOM, bottom-up SOM calculation. **Missing SAM or SOM
(or both) is cardinal sin #1 — refuse to ship.**

**Anti-patterns:**
- TAM only, no SAM/SOM — looks lazy and overclaims
- TAM = "$X trillion global software market" — too wide to be meaningful
- Bottom-up calculation that multiplies a tiny conversion rate by a huge universe to
  hit an arbitrary target
- Sources are consulting-firm press releases without underlying methodology

**Investor-read-test question:** *If I stopped reading here and had to tell my
partner "this is X big and here's how they get there," could I?*

---

## Slide 5 — Product

**Core question:** What does it actually do?

**Required slots:**
- Screenshot or short product demo (static image, animated GIF, or short embedded
  video link — but link preferred over embed for deck portability)
- 2–4 labeled callouts that map each product surface to a user outcome
- The primary user action (the one thing the user does 80% of the time)

**Cardinal slots:** screenshot or demo artifact, primary user action.

**Anti-patterns:**
- Architecture diagram instead of a product screenshot — investors care what the user
  sees, not your infrastructure
- Multiple screenshots with no annotations — investor has to guess what's important
- "Coming soon" or mockups presented as if live — say mockup explicitly if it's one

**Investor-read-test question:** *Can I visualize a real user using this?*

---

## Slide 6 — Business Model

**Core question:** Who pays, how, how often, at what price band?

**Required slots:**
- Who pays (if different from who uses — e.g., B2B2C, where the buyer is not the user)
- Pricing model (subscription, usage-based, transactional, one-time, freemium with
  upgrade path)
- Price band (rough ACV, ARPU, or transaction size — not a full pricing page)
- Contract length or revenue cadence (monthly / annual / per-transaction)
- Gross margin range (if known; mark [Unknown] if not)

**Cardinal slots:** who pays, pricing model, price band.

**Anti-patterns:**
- Pricing described as "TBD" or "depends on the customer" (signals the founder hasn't
  talked to enough customers)
- Multi-sided model described without naming the paying side clearly
- Freemium with no stated upgrade trigger

**Investor-read-test question:** *Can I compute a rough ACV and gross margin from
this slide?*

---

## Slide 7 — Traction

**Core question:** What evidence do you have that this works?

**Required slots:**
- A chart or table with numbers and a **time axis** (monthly is best; quarterly
  acceptable; annual only if company is >3 years old)
- The metric that matters most for this stage (revenue, logos, retention, active
  users, NPS, LOIs — pick the strongest one, don't dilute with 5 charts)
- Trend direction + growth rate (e.g., "+22% MoM for the last 6 months")
- Named logos or customer types if B2B; cohort retention if B2C/consumer SaaS
- Pre-launch exception: if pre-revenue, traction = validation proxies (waitlist
  size with growth curve, LOIs, pilot contracts, design partners). Mark clearly as
  pre-revenue.

**Cardinal slots:** chart/table with time axis, the strongest metric for stage. **A
number without a time axis is cardinal sin #2 — refuse to ship.**

**Anti-patterns:**
- "10,000 users" with no time axis — could be over 10 years or 10 days
- Cumulative charts presented as growth charts (always-up visual lies about velocity)
- Cherry-picked window (3 good weeks after a marketing push, presented as "trend")
- Vanity metrics (pageviews, signups) stacked in place of revenue or retention
- **Future-dated pilots, planned launches, or projected revenue plotted on the
  traction curve.** That's pipeline, not traction. Move it to the Ask slide as
  use-of-funds milestones.

### Pre-revenue traction (no historical revenue yet)

The time axis is REQUIRED but the metric changes:

- Use validation proxies with **past dates only**: signed LOIs, design-partner
  agreements, completed pilots (with end date), waitlist growth curve,
  referenceable users
- A "planned pilot Q3 2026" is **not** traction — it's pipeline. Either move
  it to the Ask slide as a milestone, or omit it.
- If you have ZERO historical traction, **replace this slide with "Why Now"**
  (timing thesis + insight) and disclose the absence on the Title slide
  preamble. Do not fake a traction slide with future-dated bars.

**Investor-read-test question:** *Is this growth real, and at what rate?*

---

## Slide 8 — Team

**Core question:** Why this team for this problem?

**Required slots:**
- Faces (photos) of the founders and any key hires
- For each founder: name, role, one-line prior experience most relevant to this problem
- Any unfair advantage the team has (domain expertise, prior startup, relevant network,
  academic credibility — name it explicitly)

**Cardinal slots:** faces, per-founder relevant prior experience. **Team slide with
no faces or no relevant experience is cardinal sin #3 — refuse to ship.**

**Anti-patterns:**
- Logos of prior employers with no context about role or duration
- "MIT alum" without saying what they actually did
- Advisors listed as if they were team members — separate them visually
- Headshots that look like LinkedIn thumbnails on a plain background (investors will
  still read the slide but a clear, consistent photo set signals professionalism)

**Investor-read-test question:** *Would I bet on these specific humans to solve this
specific problem?*

---

## Slide 9 — Competition

**Core question:** Who are you really competing with, and how are you different?

**Required slots:**
- A visual (2×2 positioning, feature comparison table, or quadrant) — not a bullet list
- At least 2 named competitors (even if they're indirect — the customer's status quo
  always counts)
- The one axis where you are clearly better, stated explicitly
- Acknowledgment of where competitors are stronger (honest trade-off)

**Cardinal slots:** visual, at least 2 named competitors.

**Anti-patterns:**
- "We have no competition" — the real competitor is always the customer's current
  workaround; claiming no competition means you haven't looked
- All competitors painted as strictly worse on every dimension — honest trade-offs
  build credibility; painting competitors as uniformly bad signals blind spots
- Feature checklists with only your checkmarks filled in

**Investor-read-test question:** *Does this deck acknowledge real competitive
pressure without whining about it?*

---

## Slide 10 — Ask & Use of Funds

**Core question:** What are you raising, what will it buy, and how long does it run?

**Required slots:**
- **Amount** (e.g., "Raising $3.5M seed")
- **Round type** (pre-seed / seed / Series A / bridge)
- **Specific milestones** the raise will buy (3–5 milestones, each with a metric or
  date — "ship v2 by Q3" is weaker than "reach $1M ARR by Q3")
- **Runway** in months at the new burn rate
- **Use of funds** percentage breakdown (engineering, sales, marketing, ops, etc.)
- Optional but strong: named lead investor if one is committed, or the terms target
  if not

**Cardinal slots:** amount, specific milestones, runway. **A vague ask ("raising
capital to grow the business") is cardinal sin #4 — refuse to ship.**

**Anti-patterns:**
- Milestones that are activities, not outcomes ("hire 10 engineers" vs "ship mobile app
  to 10k DAU")
- Runway that implies unrealistic efficiency (e.g., 36-month runway on a $2M seed with
  $150K burn — the math doesn't hold)
- Use-of-funds breakdown that sums to more or less than 100%
- No round type specified — makes it hard for investors to categorize the deal

**Investor-read-test question:** *If I wrote the check, would I know exactly what I
bought?*

---

## Optional slides (add only if founder has real content)

### Why Now

**Core question:** What changed in the world that makes this possible/necessary now?

**Required slots:** a specific shift (technology, regulation, market behavior, cost
curve) with a source; why this unlock matters for *your* approach specifically.

**Anti-pattern:** "AI is changing everything" without specifying which AI advance and
how it maps to your approach.

### Vision

**Core question:** What does the world look like if you win?

**Required slots:** a 3–5 year view of what the company becomes; the adjacent markets
you expand into; why winning this segment gives you access to those adjacencies.

**Anti-pattern:** vision that's unrelated to the current product ("we start with
dental, end with curing cancer").

### Appendix

**What belongs:** cohort retention tables, unit economics detail, cap table, legal
structure, customer testimonials with names, GTM org chart.

**What doesn't belong:** anything you were too afraid to put in the main deck. If
it's material, it goes in the main flow or gets cut.

---

## Cross-slide consistency checks

Before rendering, verify:

- **Segment (slide 2) matches SAM (slide 4).** If the problem is "single-location
  dental practices" but SAM is "all healthcare," the deck has a bait-and-switch.
- **Business model (slide 6) is consistent with traction (slide 7).** If the model
  is subscription, traction should show ARR or MRR, not GMV.
- **Ask milestones (slide 10) are fundable by the ask amount.** If you're raising
  $2M but milestones imply $6M of work, the numbers don't hold.
- **Team (slide 8) has the skills to execute the ask (slide 10).** If the ask buys
  "10 sales hires" but the team has no GTM leader, flag it.
- **If the validation canvas Stress Tests identify a critical assumption, the deck
  either addresses it (ideally in Traction) or acknowledges it in the Ask.**
- **If the assumption-test plan has confirmed any top-3 hypothesis, surface
  the result on Traction (or on a dedicated Validation slide before Traction).
  If any top-3 hypothesis was invalidated, the canvas MUST have been updated and
  the deck MUST reflect the updated belief — otherwise the deck is built on a
  belief the founder already knows is wrong.**

**Single-slide rework:** when the user asks to rework only one slide, these
same consistency checks apply against that slide's named adjacencies — see
SKILL.md §Single-slide rework mode for the adjacency table. A Competition
rework must still line up with Problem and Solution; a Market rework must
still line up with Problem's segment and Business Model's ACV math. An
isolated rework is how a single-slide edit quietly breaks the rest of the deck.
