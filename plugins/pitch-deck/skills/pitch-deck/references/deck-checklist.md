# Deck Checklist — Template

The template for `pitch/deck-checklist.md`, the before-you-send gate. Write this file
last, after `deck.html` and `speaker-notes.md`. The checklist is the founder's own
final review — the deck doesn't go to investors until every item passes.

**Why it exists.** The skill gates on the four cardinal sins before rendering — but
even a rendered deck can fail in subtle ways (out-of-date date, wrong contact email,
a slide that reads fine to the founder but confusing to a stranger). The checklist
catches those.

---

## Template

```markdown
# Deck Checklist — {{company_name}}

Last updated: {{generated_date}}
Deck variant: {{variant: cold-email | warm-intro | demo-day | follow-up}}

---

## Cardinal gate (these block shipping)

- [ ] **Slide 4 (Market):** has TAM *and* SAM *and* SOM, with a bottom-up calculation
      and a source.
- [ ] **Slide 7 (Traction):** every number has a time axis. No "10,000 users" without
      a start date.
- [ ] **Slide 8 (Team):** every founder has a face (photo) and a one-line relevant
      prior experience.
- [ ] **Slide 10 (Ask):** amount + specific milestones + runway in months.

**If any box above is unchecked, do not send this deck.** Fix the slot, regenerate,
then re-check.

---

## Required slots filled

- [ ] Slide 1 Title: company name, tagline (≤10 words), founder names + roles,
      date, contact.
- [ ] Slide 2 Problem: named segment (not "SMBs"), customer-language pain, current
      workaround, why-now seed.
- [ ] Slide 3 Solution: one-sentence description, key insight, concrete outcome.
- [ ] Slide 4 Market: cardinal items above + sources named.
- [ ] Slide 5 Product: screenshot or demo artifact, 2–4 callouts, primary user
      action.
- [ ] Slide 6 Business Model: who pays, pricing model, price band, contract length.
- [ ] Slide 7 Traction: cardinal item above + trend direction + growth rate + named
      logos or cohort.
- [ ] Slide 8 Team: cardinal items above + unfair advantage named.
- [ ] Slide 9 Competition: visual (2×2 or table), at least 2 named competitors
      including status quo, honest trade-off acknowledged.
- [ ] Slide 10 Ask: cardinal items above + use-of-funds percentage breakdown summing
      to 100%, round type named.

---

## The 90-second read test

**What it is.** The founder reads the deck cold, front-to-back, in 90 seconds, out
loud if possible. Then answers three questions without looking at the deck:

1. What does this company do? (one sentence)
2. Why is now the right time? (one reason)
3. What are they asking for? (amount + the top milestone it buys)

If the founder stumbles on any of these, the deck isn't done.

- [ ] 90-second read completed
- [ ] Question 1 answered cleanly
- [ ] Question 2 answered cleanly
- [ ] Question 3 answered cleanly

**Next level.** Have someone outside the company do the same 90-second read. If
they can't answer the three questions, the deck isn't ready for cold-email send
(warm-intro can tolerate more, since you'll be there to answer).

---

## Cross-slide consistency

- [ ] Segment on slide 2 matches SAM on slide 4.
- [ ] Business model on slide 6 is consistent with traction metric on slide 7.
      (Subscription model → ARR/MRR traction; transaction model → GMV/take-rate.)
- [ ] Ask amount on slide 10 is realistically fundable by the milestones listed
      (no "raise $2M, do $6M of work").
- [ ] Team on slide 8 has the skills implied by the use-of-funds plan on slide 10.
- [ ] If `business-model.md` has a top-severity Stress Test, the deck addresses it
      (in Traction, Competition, or Ask) — not hidden in appendix.

---

## Rendering quality

- [ ] `deck.html` opens in a browser with no internet.
- [ ] Keyboard navigation works (←, →, Space, Esc).
- [ ] `?print-pdf` produces a clean slide-per-page PDF.
- [ ] AAA contrast for body text (≥ 7:1 on the projection background).
- [ ] AA contrast for accent text (≥ 4.5:1).
- [ ] Brand tokens applied if `brand-kit/design-system.md` is present; neutral
      defaults otherwise.
- [ ] No `<script src="https…">` or `<link rel="stylesheet" href="https…">` in the
      HTML.
- [ ] All images are base64-inlined or live in the `pitch/` folder as relative
      paths.

---

## Legal and disclosure

- [ ] "Confidential" or equivalent footer if the deck is shared under NDA.
- [ ] Forward-looking-statement disclaimer if projections or forecast numbers are
      shown. Template:
      > *This presentation contains forward-looking statements based on current
      > expectations. Actual results may differ materially.*
- [ ] CCPA/GDPR disclaimer if the deck references personal data (customer names,
      customer emails). Usually the customer logos + quotes are fine with permission.
- [ ] Customer quotes / named logos have explicit permission from the customer.
- [ ] No competitor logos without permission or fair-use basis.

---

## Final sanity

- [ ] Read date on slide 1 is current.
- [ ] Contact email on slide 1 is the right one (not a personal address if the
      company has a domain, unless deliberate).
- [ ] Spelling and grammar scanned (at least one read-through by someone other than
      the deck author).
- [ ] File size is reasonable (< 15MB for easy email attachment; < 25MB hard ceiling).
- [ ] Open `deck.html` on a phone — make sure body text is still readable. Investors
      open cold-email decks on phones first.
- [ ] Saved backup to `pitch/deck-v{{YYYY-MM-DD}}.html` so future edits don't
      overwrite the send-ready version.

---

## Overrides

If the founder chooses to ship despite a cardinal-gate failure (discouraged, but
their call), document here:

```
Override: {{which cardinal item is being shipped unfilled}}
Reason: {{why the founder is shipping anyway}}
Accepted risk: {{what the founder understands will happen if the slot is wrong}}
Date: {{YYYY-MM-DD}}
```

Without this override block, the deck is considered not ready.

---

## One-liner at the end

The final section of the checklist — the founder's own honest answer:

```
If I were the investor reading this cold, would I take the meeting?

[ ] Yes, because: ______________
[ ] No, because: ______________
```

A "no" with a named reason is a valid outcome — it tells the founder what to fix
before the next pass.
```

---

## Usage

- Save this file as `pitch/deck-checklist.md` with real values substituted.
- The checklist is for the founder to use, not for the skill to auto-check. The
  skill has already run its hard gates (cardinal slots, rendering validity). The
  checklist is the human-in-the-loop final review.
- Recommend the founder complete the checklist the *day before* sending, not
  immediately after generation — a night of distance catches typos, clichés, and
  optimism the founder didn't notice in the moment.
