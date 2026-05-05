# Speaker Notes — Format Reference

The format for `<pitch-root>/speaker-notes.md`. One section per slide in the deck, in
deck order. Each section has three required parts and one optional part.

**Purpose.** Speaker notes are not a teleprompter. They are a compressed rehearsal
artifact — the 15–30 second version of the slide's message, the pushback you should
expect, and the data to pull up if pushback goes deeper. A founder who can deliver
the 30-second version cold, and field the expected pushback, has internalized the
slide.

---

## Per-slide format

```markdown
## Slide N — {{Slide Title}}

**Spoken (15–30 sec):**
{{The actual spoken version. First person, conversational, ≤75 words. Must fit in
30 seconds at normal speaking pace — read it aloud with a stopwatch to verify.}}

**Likely pushback:**
{{The most common VC objection to this slide. Stated as the VC might state it —
direct, maybe slightly hostile. One-line response that addresses it without getting
defensive.}}

**Deep-dive redirect (optional):**
{{If the pushback turns into a 5-minute tangent, where do you take them?
Specifically: "Appendix slide X" or "the validation result in the assumption-test plan" or
"pull up the metrics dashboard at [url]."}}
```

---

## Example — Slide 2 (Problem)

```markdown
## Slide 2 — The Problem

**Spoken (15–30 sec):**
Single-location dental practices run scheduling out of spreadsheets and a lot of
phone tag. The office manager spends about 12 hours a week on it, which is a
third of their job. We talked to 47 practices in California — all 47 said this
is their #1 operations pain, and 32 pay a combined $800/month across three tools
that don't talk to each other.

**Likely pushback:**
*"Isn't this a solved problem? What about Dentrix or Open Dental?"*
Those are practice-management suites — they own billing and charting, and
scheduling is bolted on. Office managers hate the scheduling UX so much they build
workarounds in Google Sheets. We're the workaround, productized.

**Deep-dive redirect:**
Appendix slide "Competitive landscape detail" shows the four incumbents by module
— scheduling is everyone's weakest feature.
```

---

## Per-slide guidance

### Slide 1 — Title

**Spoken:** Introduce yourself and the company in under 15 seconds. "I'm {{name}},
founder of {{company}}. We {{tagline}}." Don't over-explain — the next 9 slides do
that.

**Likely pushback:** usually none on the title itself. If the tagline is unclear, the
pushback comes immediately on slide 2 — so treat the tagline as a pre-stressed
element of slide 2.

### Slide 2 — Problem

**Spoken:** who hurts, how much, why it matters. Lead with a customer quote or
specific number. Do not lead with market size — that's slide 4.

**Likely pushback:** "is this a pain, or a nice-to-have?" Answer with the customer
quote and current workaround cost.

### Slide 3 — Solution

**Spoken:** one sentence on what you do, one sentence on why this approach works now.
Keep the sentences short. If you can't say it in two sentences, the solution isn't
crisp enough yet.

**Likely pushback:** "how is this different from {{adjacent product}}?" Answer:
describe one specific thing you do that they structurally can't.

### Slide 4 — Market

**Spoken:** the bottom-up SOM, not the top-down TAM. "We think we can reach $X in 3
years by closing Y customers at Z ACV." TAM is backdrop; SOM is what you're selling.

**Likely pushback:** "your SOM feels optimistic" OR "where does your TAM source come
from?" For the first, lead with your current conversion rate from pilots. For the
second, name the source and the specific data point you used.

### Slide 5 — Product

**Spoken:** "here's what the user sees, and here's what they do 80% of the time."
Don't walk through every screen — the investor can see them.

**Likely pushback:** "how technical is this? what's the moat?" The product slide
itself doesn't have to answer moat — but be ready to.

**Deep-dive redirect:** Product slide is where demos happen. If the investor wants
to see more, offer to share your login and walk through in a follow-up, or play a
60-second recorded demo.

### Slide 6 — Business Model

**Spoken:** one sentence each on who pays, how often, how much. If gross margin is
strong, name it. If not, skip it (you'll be asked).

**Likely pushback:** "why this pricing model and not {{alternative}}?" Usually a
test of whether you've thought about alternatives. Answer: describe the alternative
you rejected and why.

### Slide 7 — Traction

**Spoken:** the single most impressive number + the time axis + the trend direction.
"We're at $X ARR, up 22% MoM for the last 6 months, with 0 paid marketing." If
pre-revenue, substitute: "X companies in pilot, Y signed LOIs, waitlist at Z
growing 15% WoW."

**Likely pushback:** "how durable is this growth?" Answer: retention cohort data.
If you don't have it yet, say so and name when you will.

**Deep-dive redirect:** always prep a cohort retention table in the appendix.
Traction + retention is the most-asked follow-up.

### Slide 8 — Team

**Spoken:** one sentence per founder on why they are uniquely qualified for *this*
problem. Not "10 years at Google" — "built Gmail's anti-spam filter, then ran the
dental vertical at Square for 4 years."

**Likely pushback:** "what's missing from the team?" Answer honestly — naming the
gap (e.g., "we need a VP Sales by Q3") builds trust.

### Slide 9 — Competition

**Spoken:** name 2–3 real competitors (including status quo), state the one axis
where you're better, acknowledge where they're stronger. Honesty here wins more
investor respect than any other slide.

**Likely pushback:** "what happens when {{big incumbent}} builds this?" Answer:
usually a combination of (a) they're optimized for a different segment, (b) they've
had X years and haven't, (c) we'd be acquired before they ship. Pick the truthful
one.

### Slide 10 — Ask & Use of Funds

**Spoken:** amount, round type, top 3 milestones, runway in months. End with "we'd
love to talk about {{specific next step}}" — a clear next action beats "thoughts?"

**Likely pushback:** "why this amount?" Answer: the milestones it buys and the
runway it produces. The number should feel bounded by the plan, not arbitrary.

---

## Optional prefatory section

If the deck includes a warning slide at position 0 (cardinal slots unfilled), the
speaker notes should begin with:

```markdown
## ⚠️ Slide 0 — Deck is not ready to send

Unfilled cardinal slots:
- {{missing_slot_1}}
- {{missing_slot_2}}

**Do not share this deck with investors until these are filled.** See
`deck-checklist.md` for the full gate.
```

Remove this section when the slots are filled.

---

## Length discipline

The full `speaker-notes.md` file should be readable in under 15 minutes. If it's
longer, the slides are carrying too much. Each slide's section should fit on one
screen without scrolling — if it doesn't, cut.

A speaker-notes file that's longer than the deck is a signal that the deck is too
short and too much is living in spoken narrative. Investors in a cold-email context
never hear the spoken version.
