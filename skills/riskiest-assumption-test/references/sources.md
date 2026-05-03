# Sources — Bibliography

Full citations for the canonical sources referenced in
[`test-method-catalog.md`](test-method-catalog.md). The catalog uses inline
surname-only citations (e.g., *"per Maurya"*, *"following Fitzpatrick"*) plus
per-method "Further reading" lines; this file is the authoritative pointer
when those abbreviations leave you wanting more.

The five primary sources cover the bulk of the catalog. The two secondary
sources extend specific methods. The "cited but not primary" entry covers
Steve Blank's framing without adopting his (now-dated) Customer Development
stage vocabulary.

---

## Primary

**Maurya, Ash.** *Running Lean: Iterate from a Plan That Works to a Business
That Works.* 3rd edition. O'Reilly Media, 2022. ISBN 978-1098108779.
- Ch. 1–3: Lean Canvas mechanics (the upstream artifact this skill consumes).
- Ch. 8–10: Customer interview rigor (the 5-interview rule with mom-test
  alignment).
- Ch. 11–13: Validation experiments — concierge MVP, Wizard of Oz, pre-sale,
  smoke tests, and the "riskiest assumption first" sequencing this skill
  operationalizes.
- Ch. 14: Pricing validation (informs Pre-Sale and LOI thresholds).

**Ries, Eric.** *The Lean Startup: How Today's Entrepreneurs Use Continuous
Innovation to Create Radically Successful Businesses.* Crown Business, 2011.
ISBN 978-0307887894.
- Ch. 6: MVP definitions (concierge MVP via the Food on the Table case).
- Ch. 7: Wizard of Oz (the IMVU and Aardvark cases).
- Ch. 8: Pivot triggers — directly relevant to the loop-back protocol
  documented in [`folder-contract.md`](../../validation-canvas/references/folder-contract.md).
- Ch. 9–10: Validated learning + innovation accounting (informs the
  "results are evidence, not vibes" discipline of Phase 5 RAT outputs).

**Fitzpatrick, Rob.** *The Mom Test: How to Talk to Customers and Learn If
Your Business Is a Good Idea When Everyone Is Lying to You.* CreateSpace,
2013. ISBN 978-1492180746.
- Ch. 1: The three sins of customer interviews — opinion questions,
  future-tense questions, hypothetical scenarios. (Directly cited in the
  5-Interview Rule and Expert Interview entries.)
- Ch. 3: Asking about past behavior, not future intent.
- Ch. 5: Commitment and advancement currencies — the framework behind
  Pre-Sale's success-signal pattern (real money is the only commitment
  currency that scales).
- Ch. 7: When to keep talking and when to stop (informs the n=5 cutoff).

## Secondary

**Savoia, Alberto.** *The Right It: Why So Many Ideas Fail and How to Make
Sure Yours Succeed.* HarperOne, 2019. ISBN 978-0062884657.
- Ch. 6: Pretotyping techniques — fake-door, Mechanical Turk, pinocchio,
  fake-by-day. (Source for the Fake-Door Test entry's framing.)
- Ch. 7: "Market Interest Assessment" (MIA) — the canonical rationale for
  why fake-door clicks count as evidence (binary commitment under realistic
  conditions).
- Ch. 9: YODA principle ("Your Own Data Always" beats third-party reports).

**Hall, Erika.** *Just Enough Research.* 2nd edition. A Book Apart, 2019.
ISBN 978-1937557102.
- Ch. 4: Interview techniques — script structure, sample sizing rationale,
  interpreting non-answers. (Cited in the 5-Interview Rule and Expert
  Interview entries.)
- Ch. 6: When expert > customer (and when not).
- Ch. 8: Synthesis — turning 5–10 interviews into actionable signal without
  over-fitting.

## Cited but not primary

**Blank, Steve.** *The Four Steps to the Epiphany.* 2nd edition. K&S Ranch,
2013. ISBN 978-0989200509.
- Cited for: (1) the "get out of the building" framing in the catalog
  intro, and (2) Letter of Intent (LOI) as a B2B viability signal in
  Method 6.
- **Not used for:** Blank's full four-stage Customer Development vocabulary
  (Discovery / Validation / Creation / Building). The stages are right; the
  language is dated for 2026 founders and overlaps confusingly with this
  catalog's own terms ("validation", "discovery"). This skill operationalizes
  Blank's posture without adopting his vocabulary.

---

## Notes on conflicts and defaults

Where sources disagree, the catalog states the conflict and picks a default
for the **idea-stage founder** (the catalog's target reader):

- **Sample size for customer interviews.** Maurya: n=5 (the "5-interview
  rule"). Hall: n≈8–12 for synthesis confidence. Fitzpatrick: "until you
  stop hearing new things." **Default:** n=5 as the floor for a single
  hypothesis; expand if the first 5 give noisy/conflicting signal. Maurya's
  number is right for cost-cheapness; Hall's is right for synthesis; the
  floor lets you stop early when the signal is loud.
- **Concierge vs. Wizard of Oz boundary.** Ries treats them interchangeably
  in early chapters; Maurya separates them sharply. **Default:** Maurya's
  separation. Concierge = test viability (will they pay for the outcome
  delivered manually?). Wizard of Oz = test feasibility/desirability of
  the *experience* (would they use it if the tech worked?). Different
  hypotheses, different methods.
- **Pre-Sale price thresholds.** Maurya: B2B ≥ $500/yr ARR equivalent,
  B2C ≥ $20 one-time. Ries: "any real money beats survey data." **Default:**
  Maurya's thresholds for the catalog's "Cost / Success-signal" sections;
  Ries's framing as the underlying rationale.

---

## How to extend this list

When the catalog adds inline citations to a new source, add it here with
the same shape: full bibliographic entry + 3–5 chapter pointers indicating
what the catalog draws from. Keep this file under ~80 lines total — it's a
pointer, not a textbook.
