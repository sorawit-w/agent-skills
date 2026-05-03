# Gate Override Protocol

How a founder accepts a gate override, how the orchestrator records it, and
how downstream skills (especially `startup-grill`) read it. The whole point
of the override protocol is that **bypasses are visible and audited** —
silent bypasses defeat the pipeline philosophy.

---

## What a gate override is

A **gate override** is an explicit, recorded founder decision to advance
past a pipeline gate that would normally STOP. Each pipeline gate has its
own override semantics:

| Gate | Severity | Override available? | Override identifier |
|---|---|---|---|
| `brand-workshop → validation-canvas` | light | n/a (informational suggestion only, not a STOP) | — |
| `validation-canvas → riskiest-assumption-test` | medium | NO — the medium gate STOPs without canvas. Founder must run canvas; no override path. | — |
| `riskiest-assumption-test → pitch-deck` | heavy | YES — `[PRE-VALIDATION DRAFT]` watermark | `pitch-deck-pre-validation` |
| `pitch-deck → startup-grill` | light | n/a (grill works on minimum input) | — |

Only the pitch-deck heavy gate has a documented override path in v2.1.0.
Future gates should follow the same protocol if they admit overrides.

---

## When an override is requested

The founder explicitly declares the override intent. Examples for the
`pitch-deck-pre-validation` override:

- *"This is a pre-validation draft."*
- *"I'm pitching for early feedback, not for funding."*
- *"I haven't tested yet — show me what the deck would look like."*
- *"Skip the gate; I know I should validate first but I want to see the
  shape."*

The orchestrator (or `pitch-deck` directly when invoked manually) recognizes
these as override-intent and proceeds to the recording step below.

---

## Recording an override (atomic + auditable)

Every override is appended to `kit-manifest.json`'s `gate_overrides[]`
array as a structured entry:

```json
{
  "gate": "pitch-deck-pre-validation",
  "timestamp": "2026-05-11T12:30:00Z",
  "reason": "Friendly advisor meeting Friday — want directional feedback on narrative shape before validation completes for hypothesis 3.",
  "founder_acknowledged": true
}
```

**Required fields and validation:**

- `gate`: the canonical gate identifier from the table above.
- `timestamp`: ISO-8601, set at the moment of override.
- `reason`: founder-provided rationale. **Minimum 20 characters.** "ok",
  "fine", "later" do NOT constitute consent. The orchestrator rejects
  shorter reasons and re-prompts: *"That's not a reason. Why specifically
  are you overriding the gate? (At least 20 chars.)"*
- `founder_acknowledged`: must be explicitly `true`. The orchestrator never
  defaults this; the founder must affirm.

**Atomic write:** the manifest update follows the standard atomic-write
discipline (write `.tmp`, then rename). This prevents a half-written
override entry on crash.

---

## How downstream skills honor an override

Once recorded, an override is **persistent and active** until the founder
explicitly revokes it. On every subsequent invocation:

### `pitch-deck` Phase 0.0 — Override-flag special case

- Reads `kit-manifest.json` if present.
- Checks `gate_overrides[]` for an entry with `gate:
  "pitch-deck-pre-validation"` AND `founder_acknowledged: true`.
- If found: honor the override silently (proceed with `[PRE-VALIDATION
  DRAFT]` watermark per Phase 0.2) but surface a one-line acknowledgment:
  > *"Manifest records a [PRE-VALIDATION DRAFT] override from [date] —
  > reason: [reason]. Proceeding with watermark."*
- If not found: enforce the heavy gate normally (STOP if RAT Results are
  empty for top-3 hypotheses).

### `startup-grill` Step 1c — Iteration-evidence reads overrides

- Reads `kit-manifest.json` if present.
- Surfaces every override in the kill-report's `## Iteration Evidence`
  section as a signal worth probing:
  > *"This pipeline used 1 gate override:
  > `pitch-deck-pre-validation` on [date] (reason: [reason]). The deck
  > carries a `[PRE-VALIDATION DRAFT]` watermark. Probe whether the
  > untested hypotheses materially affect the deck's claims."*
- The panel uses recorded overrides as direct grilling ammunition. An
  override is not a hidden bypass — it's a deliberate decision the
  founder made to ship something un-validated, and it deserves probing.

This is the audit chain: **override → recorded → surfaced → probed**.

---

## Revoking an override

The founder can revoke an active override two ways:

1. **Explicit revocation:** founder says *"revoke the pre-validation
   override"* or *"the deck is now validated, remove the watermark"*. The
   orchestrator updates the entry to set `founder_acknowledged: false` (or
   removes the entry; either is acceptable per the schema).
2. **Implicit revocation via gate satisfaction:** if the founder runs RAT
   in update mode and populates `## Results` for all top-3 hypotheses, the
   underlying condition that prompted the override is resolved. The
   orchestrator surfaces: *"RAT Results are now populated. The
   `pitch-deck-pre-validation` override is no longer needed — revoke it
   so future deck runs ship without watermark?"* Founder confirms.

Revocation is **not retroactive**: a deck that shipped with the override
still has its `[PRE-VALIDATION DRAFT]` watermark in its rendered HTML
(the watermark is in the artifact itself, not driven by the manifest).
Re-rendering the deck after revocation produces a clean version.

---

## What the override protocol does NOT permit

- **No silent bypass.** If a founder doesn't explicitly acknowledge with a
  minimum-length reason, no override is recorded and the gate STOPs
  normally.
- **No retroactive override.** Overrides apply going forward. A deck
  shipped under an override keeps its watermark; the watermark is the
  audit trail in the artifact.
- **No transferable override.** Each override applies to a specific gate.
  An override on `pitch-deck-pre-validation` does NOT carry over to (e.g.)
  a hypothetical future `validation-canvas-skip-stress-tests` gate.
- **No anonymous override.** Every override has a `reason`. The orchestrator
  rejects empty or trivially-short reasons.
- **No override of the medium gate.** `validation-canvas → RAT` is the
  medium gate. There is no override path; the founder must run
  `validation-canvas` first. (The medium gate exists because RAT cannot
  meaningfully operate without a canvas to extract beliefs from.)

---

## Why this protocol exists

The pipeline's value is in its discipline. Founders who skip steps and
ship anyway are not learning anything from the pipeline; they're using it
as a checklist of artifacts to produce. The gates exist to surface that
skipping has consequences (a pitch built on un-validated beliefs IS sales
theater, per the heavy gate).

Sometimes the founder has a legitimate reason to skip — an early advisor
meeting where directional feedback matters more than validation, an
internal narrative-shape exercise, a sandbox run. The override protocol
honors those legitimate cases by:

1. Forcing the founder to articulate the reason (≥ 20 chars).
2. Recording the override with timestamp + reason + acknowledgment.
3. Surfacing the override later (especially in `startup-grill`'s
   iteration-evidence check) so the panel and the founder both see the
   override as a deliberate decision worth probing.

The result: **legitimate overrides are preserved**, illegitimate ones get
extra scrutiny, and silent bypasses don't exist.
