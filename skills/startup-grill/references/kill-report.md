# Kill Report — Deliverable Contract

The kill report is the primary deliverable of `startup-grill`. It is **not** a
list of "concerns" — it is a structured verdict on what would kill this startup
if unaddressed, organized by what the founder can *do* about each weakness.

This document specifies the exact file shape. Deviating from it breaks
downstream readability and the interactive defense flow.

---

## Output path

```
grill/kill-report.md
```

If the working directory already has a `grill/kill-report.md` from a prior
session, **append** today's run as a new dated section at the top — never
overwrite. The defense log (if any) lives at `grill/defense-log.md` and follows
the same append rule.

---

## File structure

The report has **seven required sections** in this exact order (Section 7
added in v2.0.0):

```markdown
# Kill Report — [Startup name]
*Run: YYYY-MM-DD · Variant: [pre-seed | seed | Series A | other] · Panel: [N roles]*

## 1. Verdict
## 2. Lethal & Fixable
## 3. Lethal & Unfixable
## 4. Material & Fixable
## 5. Diligence Asks
## 6. Panel
## 7. Iteration Evidence
```

Sections 2 and 3 may be empty (state "None surfaced this run"); sections 1,
4, 5, 6, and 7 are mandatory and non-empty.

---

## Section 1 — Verdict

A **single paragraph, 3–6 sentences**, leading with the verdict label and
ending with the headline reason.

**Verdict labels** (pick exactly one):

| Label | Meaning |
|---|---|
| `Investable as-is` | No lethal weaknesses surfaced; standard diligence applies |
| `Investable with conditions` | Lethal-but-fixable issues; addressable inside one quarter |
| `Pivot signal` | Lethal-and-unfixable issues; the idea as-stated isn't fundable, but a related framing might be |
| `Pass` | Lethal-and-unfixable issues without a credible nearby framing |

After the label, name the **single most important reason** in plain language —
not VC-speak. The reason **MUST** cite a specific weakness from sections 2–4
by item number (e.g., "see L1") or by clear unambiguous reference (e.g., "the
GTM channel weakness"). Generic phrases like "five material gaps remain" or
"some risks need addressing" are forbidden — they sever the verdict from its
support and make the report uncheckable.

Example (passes):

> **Verdict: Investable with conditions.** The TAM math holds, the team
> credibility is there, and the wedge is sharp — but the GTM motion has not
> been tested with even five paying customers (see L2). This is fixable in
> 90 days and is the gating item for a seed conversation.

Example (fails — generic, no specific cite):

> **Verdict: Investable with conditions.** The team is credible and traction
> is real. Five material gaps remain but all are addressable in 90 days.

**Anti-patterns to refuse:**
- Hedged verdicts ("could be investable depending on…") — pick a label
- Verdicts that don't reference any specific weakness from sections 2–4 by
  item number or clear pointer
- Verdicts that aggregate weaknesses generically ("five gaps remain", "some
  risks", "needs work") without naming any specific item
- Verdicts that contradict the body (label says `Pass`, body has nothing
  lethal; or label says `Investable as-is` but body has lethal items)

---

## Section 2 — Lethal & Fixable

The weaknesses that would kill the company if unaddressed, **and** the founder
can do something about them.

**Format** — a numbered list, **2–3 items max** (more than 3 means the panel
diluted the bar — re-rank). Each item has this exact shape:

```markdown
### L1. [One-sentence weakness statement]

- **Who saw it:** @vc_partner, @ux_researcher
- **Severity:** Lethal — [why this kills the company if unaddressed]
- **Fixability:** Fixable in [time horizon] — [what changes]
- **What evidence would change our minds:** [specific, verifiable]
- **Suggested attack:** [concrete next move, not "do customer research"]
```

**Quality bar for "Suggested attack":** must name a *specific* action with a
*specific* artifact or signal as output. "Run discovery interviews" fails;
"Run 8 discovery calls with operations leads at logistics SMBs ($10–$50M
revenue) and report willingness-to-pay at $499/month" passes.

---

## Section 3 — Lethal & Unfixable

Weaknesses that would kill the company **and** the founder can't address
without abandoning or fundamentally pivoting the idea.

**Format** — same shape as Lethal & Fixable, with two changes:

- `Fixability:` always reads `Unfixable within current framing — [why]`
- Add a **`Pivot the founder might consider:`** line proposing a related
  framing where this weakness wouldn't apply. If no credible pivot exists,
  state that explicitly: "No credible pivot — this is a `Pass` signal."

**Cap at 2 items.** If the panel surfaces more than 2, that's not a startup —
that's a category problem. Surface it as a Verdict footnote and stop.

---

## Section 4 — Material & Fixable

Weaknesses that **wouldn't kill the company** but would meaningfully reduce
investability or execution velocity. The diligence ask list, essentially.

**Format** — numbered list, **3–5 items**, lighter shape:

```markdown
### M1. [Weakness statement]

- **Who saw it:** [role]
- **Why it matters:** [1–2 sentences, no padding]
- **Fix:** [concrete next move]
```

No `evidence-would-change-mind` line here — that's reserved for lethal items.

---

## Section 5 — Diligence Asks

The list of artifacts, data, or follow-up that an investor would request
before making a decision. **Numbered, prioritized, ≤7 items.**

```markdown
1. Cohort retention table (months 1–12) for the first 50 customers
2. Top-down + bottom-up TAM working with named source data
3. ...
```

Diligence asks are not the same as fix-actions in sections 2–4 — these are
*evidence requests*, not *change-the-business* actions. Don't double-count.

---

## Section 6 — Panel

A short reference table of who was in the room and what lens each carried.

```markdown
| Role | Lens |
|---|---|
| @vc_partner | Capital efficiency, defensibility, comparable deals |
| ... | ... |
```

If specialists were dropped due to the cap, name them and their unaddressed
concern in a one-line footnote: *"Cap forced @clinical_researcher out — clinical
evidence diligence is not covered in this run."*

---

## Section 7 — Iteration Evidence

A short read on whether the founder is closing the loop on what they learn.
Pulled from the iteration-evidence check in SKILL.md Phase 1 Step 1c.

This section is **always present** but its content scales with what the
working directory shows. Three states:

### State A — Full pipeline with evidence of iteration

```markdown
## 7. Iteration Evidence

✅ Pipeline shows iteration. `validation-canvas.md` was updated on
[YYYY-MM-DD], after RAT Result entries on [YYYY-MM-DD]. Specifically,
[block name] was revised in response to [hypothesis #N] being
[confirmed | invalidated]. The deck reflects the updated belief.

**Probe focus:** the founder is using the loop. Probes can assume the
canvas is current and focus on what hasn't yet been tested.
```

### State B — Pristine pipeline (yellow flag)

```markdown
## 7. Iteration Evidence

🟡 Pristine pipeline — `validation-canvas.md` was NOT updated after RAT
Results landed. Either every top-3 hypothesis was confirmed (rare; be
skeptical) or the founder is not closing the loop on what they're
learning. The deck currently reflects the pre-test canvas.

**Probe focus:** ask why no canvas update. If the answer is "everything
confirmed", probe each top-3 result individually for whether the
confirmation criterion was actually met. If the answer is "I haven't
gotten to it", treat the deck's Traction claims as belief, not evidence.
```

### State C — RAT missing entirely (large yellow flag)

```markdown
## 7. Iteration Evidence

🟠 No assumption testing in the pipeline — `rat/assumption-test-plan.md`
is missing. The pitch was built directly from the canvas with no
intervening validation step. **Treat every Traction-flavored claim as
belief, not evidence.**

**Probe focus:** for each major claim in the deck (Problem severity, UVP
fit, channel CAC, willingness to pay), ask: "what test confirms this
isn't your assumption?" Most answers will be vibes. Surface accordingly
in Lethal & Fixable.
```

### State D — Canvas missing (panel can't cross-check)

```markdown
## 7. Iteration Evidence

⚪ No `validation-canvas.md` in the working directory. Panel cannot
cross-check the deck's claims against documented Stress Tests. The kill
report is bounded by what the founder put in the brief or the deck
directly.

**Probe focus:** ask the founder for a one-paragraph problem and segment
description before grilling, or accept that the panel will probe with
less ammunition than usual.
```

This section is **light gate output** (informational, not a blocker — the
kill report is the terminal pipeline step). But it surfaces a pattern that
predicts startup outcomes well: founders who iterate beat founders who
ship clean pipelines without revision.

---

## Forbidden patterns

The skill must refuse to ship a kill report that:

1. **Has no Lethal section** but verdict is `Pass` or `Pivot signal` — the
   verdict has no support
2. **Has more than 3 Lethal & Fixable items** — re-rank, the bar drifted
3. **Lists a weakness in both Lethal & Fixable AND Material & Fixable** — pick
   one severity, don't hedge
4. **Stuffs Material into Diligence Asks** to avoid surfacing them as
   weaknesses — a fix-action and an evidence-ask are different things
5. **Uses qualifying language** in lethal-section weaknesses ("might
   potentially struggle", "could be a challenge") — lethal items are stated
   in declarative form or they don't belong in the lethal section

---

## Verifier checklist

Before shipping `grill/kill-report.md`, verify:

- [ ] All seven sections present in the exact order above
- [ ] Verdict label is one of the four canonical labels
- [ ] Verdict references at least one specific weakness from sections 2–4
- [ ] Lethal & Fixable has 2–3 items (no more, no fewer if `Investable with conditions`)
- [ ] Each lethal item has all five fields filled (no `[fill in]` slots)
- [ ] Suggested attacks are specific (named artifact / signal), not generic
- [ ] Diligence Asks are evidence requests, not change-the-business actions
- [ ] No weakness appears in two severity sections
- [ ] Panel table lists every role that contributed in Round 1
- [ ] Iteration Evidence section reflects actual state of working directory (full / pristine / no-RAT / no-canvas)

If any box is unchecked, fix before presenting the file.
