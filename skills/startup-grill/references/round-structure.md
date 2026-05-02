# Round Structure

The skill runs in **two modes**:

- **One-shot mode** (default) — three rounds, ends with a kill report. The
  founder is not in the room during grilling.
- **Interactive defense mode** (opt-in, after one-shot completes) — the
  founder picks a weakness number, defends it; the relevant 1–2 panelists
  re-probe; the verdict on that line item updates.

This document specifies both. Read it whole — the modes share Round 1 and 2
logic; only Round 3 and the post-shipment loop differ.

---

## One-shot mode

### Round 1 — Probe (panel-only)

Each panelist contributes **one probe per startup-axis they own**, in this
order:

1. `@vc_partner` — capital, defensibility, comparable deals
2. `@growth_marketer` — distribution, CAC, channel reality
3. `@startup_strategist` — wedge, narrative, founder-market fit
4. `@ux_researcher` — actual user behavior vs. reported user behavior
5. **Slot 5** — technical DD or brand positioning (per Phase C of
   `panel-resolution.md`)
6. **Specialists** (in priority order from Phase F of `panel-resolution.md`)

**Per-probe shape** — each panelist outputs:

```markdown
**@role_tag (Round 1):**
- **Probe:** [the question or claim being tested]
- **What I'm looking for:** [the specific signal that would pass or fail]
- **My read:** [pass | material | lethal-fixable | lethal-unfixable]
- **Falsifier:** [evidence that would change the read]
```

**Per-probe length cap:** 60–100 words. Anything longer gets cut — grilling
is dense, not verbose.

**Round 1 quality bar:**
- At least 2 panelists must mark a probe as `lethal-fixable` or
  `lethal-unfixable` for the round to be meaningful. If every probe is
  `material` or `pass`, **the panel was too soft** — re-run with sharper
  posture or note explicitly that no lethal weaknesses surfaced.
- No probe may end in a question without a falsifier. Probes without
  falsifiers are rhetoric, not grilling.

### Round 2 — Forced defense (panel-internal)

The skill itself responds *as the founder would*, using whatever evidence the
brief contained, to each lethal probe from Round 1. This is the
"steelman pass" — the panel must hear the strongest version of the founder's
defense before issuing a verdict.

**Per-defense shape:**

```markdown
**Steelman defense to L#:** [strongest possible response using brief evidence]
**Defense gap:** [what evidence the brief doesn't contain that the defense
needs]
```

**Downgrade rule — read this carefully, it's the most-violated rule in this skill:**

The downgrade decision is **binary** and **driven entirely** by whether the
brief contains the defense:

- **Brief contains the defense** → probe gets downgraded (lethal → material,
  or material → drop). The defense retired the risk.
- **Brief does NOT contain the defense** → probe **stays at its Round 1
  severity**. The defense gap becomes the `What evidence would change our
  minds:` line in the kill report.

**The forbidden middle path:** writing a steelman that explicitly names a
defense gap (e.g., "the brief does not contain X" / "no measured Y" / "no
documented Z") AND THEN downgrading the probe anyway. This is contradictory.
A defense gap means the brief did not credibly answer — by definition, the
probe stands.

**Hard rule:** if your steelman text contains the phrases "defense gap:",
"the brief does not", "no [evidence type]", "not yet [verb]ed", or any
equivalent phrasing that names missing evidence, the probe **MUST** stay at
its Round 1 severity. Do not downgrade. The kill report's `What evidence
would change our minds:` line captures exactly that gap.

This rule exists because Claude has a natural pull toward synthesis and
closure — wanting to "resolve" probes by softening them. That instinct
produces empty Lethal sections and over-optimistic verdicts. The downgrade
rule keeps the lethal bar where it belongs.

**Round 2 quality bar:**
- Every Round 1 probe marked `lethal-*` must get a steelman defense. No
  silent skips.
- Steelmen must use *only* evidence the founder actually included in the
  brief. Inventing favorable facts is forbidden — that defeats the purpose.
- Steelmen that name a defense gap must NOT downgrade the probe. Downgrades
  are for steelmen with NO defense gap (the brief credibly answered).

### Round 3 — Synthesis (panel + report assembly)

`@startup_strategist` synthesizes the panel's reads into the four kill-report
sections (Lethal & Fixable, Lethal & Unfixable, Material & Fixable, Diligence
Asks) per `kill-report.md`.

`@vc_partner` writes Section 1 — the verdict — in 3–6 sentences leading with
one of the four canonical labels.

The other panelists do not contribute new probes in Round 3. If they
disagree with the synthesis, they record dissent as a single bullet in the
verdict's footnote: *"@role dissents: [reason]."*

### Output

After Round 3, the skill writes `grill/kill-report.md` per the spec in
`kill-report.md` and presents the file to the user.

The response **closes with the interactive-mode invitation** (next section).

---

## Interactive defense mode

### Invitation (always shown after one-shot ships)

After the kill report is presented, the response must end with this exact
block (or a close variant):

```markdown
---

**Defend any weakness?**

Pick a weakness number (e.g., `L1`, `M2`) and tell me why we got it wrong.
Bring evidence — a metric, a customer quote, a teardown, a working
artifact. Vibes don't move the verdict.

I'll re-probe that line with the relevant 1–2 panelists and update the
verdict on that item only. Other items stay frozen.
```

The invitation is **non-optional** — even when the verdict is `Investable
as-is`, the founder may want to defend a `Material` finding or a
`Diligence Ask`. Interactive mode is opt-in but always offered.

### Defense round (when founder responds)

When the founder picks a weakness number and provides defense:

1. **Identify the relevant panelists.** If the weakness was authored by ≤ 2
   panelists, re-engage those panelists. If 3+, pick the lead author plus
   the panelist most affected by the defense's evidence type (e.g., a
   retention-curve defense engages the @vc_partner most).

2. **Run a single defend-and-reprobe cycle.** Format:

   ```markdown
   **Founder defense to L#:** [the founder's response, quoted or summarized]

   **@role re-probe:**
   - **What you brought:** [name the evidence]
   - **What it does prove:** [what's now retired]
   - **What it doesn't prove:** [what's still open, if anything]
   - **Updated read:** [pass | material | lethal-fixable | lethal-unfixable | acknowledged | partially addressed]
   ```

3. **Append to `grill/defense-log.md`** with the dated defense round and the
   updated read. Format mirrors the kill report's lethal-item shape.

4. **Update the kill report's verdict line item only.** Find the matching
   weakness in `grill/kill-report.md`, update its severity / read in place,
   and add a one-line `**Defended on YYYY-MM-DD — see defense-log.md**`
   pointer.

5. **Do NOT regenerate the entire report.** Only the affected line item
   moves. Frozen items stay frozen.

### Defense round quality bar

- The defense must include *new information* (a metric, a quote, an
  artifact). Vibes-only defenses are rejected with the response: *"You
  pushed back, but I didn't see new evidence. The verdict stands until
  there's data to weigh."*
- Re-probes follow the same falsifier rule as Round 1 probes — every
  re-probe ends with a falsifier or it doesn't ship.
- A single weakness can be defended at most **3 times in one session**
  before the skill returns: *"This weakness has been defended three times
  without a verdict change. The panel's read stands. Consider whether the
  underlying assumption needs to be revisited rather than this finding."*

### When to refuse a defense round

The skill refuses to enter interactive mode if:

- The founder argues with the *verdict* rather than picking a weakness
  number. Response: *"Verdicts roll up from weaknesses. Pick a specific
  weakness to defend — `L1`, `M2`, etc. — and we'll re-probe that line."*
- The founder tries to defend > 1 weakness in a single message. Response:
  *"One at a time — they each need their own evidence. Which weakness
  first?"*
- The founder asks the panel to "be nicer" or "soften the report". The
  report is what it is; softening it would defeat the purpose of grilling.

---

## Round-budget targets (word counts)

| Round | One-shot mode | Interactive mode |
|---|---|---|
| Round 1 | 600–900 words (5 core × ~80 + N specialists × ~50) | — |
| Round 2 | 250–400 words (one defense per lethal probe) | — |
| Round 3 + verdict | 200–300 words | — |
| Kill report file | 800–1500 words depending on lethal count | — |
| Defense round | — | 150–300 words per defense |

If a run trends over the upper bound, cut the weakest probe / defense first
rather than trim every contribution. Density beats balance.

---

## Anti-patterns (refuse all)

- **Round 2 echoing Round 1.** If the steelman defense restates the probe
  rather than answering it, that's a defective Round 2 — re-author the
  defense using brief evidence or, if the brief is silent, leave the probe
  standing at Round 1 severity (do NOT downgrade).
- **Steelman gap + downgrade.** Writing "Defense gap: brief does not contain
  X" and then downgrading the probe to material in the same breath. This is
  the most common Round 2 failure mode and is explicitly forbidden — a
  defense gap means the probe stands. If you find yourself typing both, stop
  and re-classify: the probe stays.
- **Round 3 introducing new probes.** Synthesis only. New probes mean Round
  1 was incomplete — go back and add the probe there, not in synthesis.
- **Skipping the interactive invitation.** Even when verdict is `Pass`, the
  founder may want to defend a Diligence Ask or contest a finding. The
  invitation always ships.
- **Auto-engaging interactive mode without a defend message.** Interactive
  is opt-in. Don't simulate defenses on the founder's behalf after the
  kill report ships.
