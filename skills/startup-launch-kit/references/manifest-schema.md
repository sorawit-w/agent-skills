# Manifest Schema — `kit-manifest.json`

The canonical schema for the orchestrator's state journal at the
working-directory root. Read this before reading or writing the manifest.

**Contract:**

- Single JSON file at `<founder-working-directory>/kit-manifest.json`.
- Versioned from day one (`manifest_version: 1`).
- Atomic writes: write `kit-manifest.json.tmp`, then rename. Never leave a
  partial-write file in the half-state.
- The orchestrator owns the manifest's lifecycle (creation, deletion). Each
  pipeline skill reads it if present and appends/updates its own entry, but
  no pipeline skill creates the manifest if absent.
- Read failures (corrupt JSON, missing required fields) are non-fatal — log
  the issue inline and proceed as if no manifest exists.
- The manifest is a hint, not truth. Filesystem state always wins. See
  [`state-detection.md`](state-detection.md) for the reconciliation rules.

---

## Schema (v1)

```json
{
  "manifest_version": 1,
  "created": "ISO-8601 timestamp",
  "updated": "ISO-8601 timestamp",

  "intake_answers": {
    "founding_history": "yes-with-revenue | yes-no-revenue | no",
    "domain_experience": "yes | no",
    "customer_segment_experience": "yes | no",
    "inferred_mode": "guided | focused | compressed-with-challenge"
  },

  "steps": [
    {
      "skill": "brand-workshop | validation-canvas | riskiest-assumption-test | pitch-deck | startup-grill",
      "status": "pending | in-progress | completed | blocked | failed",
      "mtime": "ISO-8601 timestamp (set when status transitions to completed/in-progress/failed)",
      "iterations": "integer (incremented on update-mode runs; defaults to 1 on first completion)",
      "blocked_by": "string (only present when status=blocked; names the gate or upstream artifact missing)"
    }
  ],

  "gate_overrides": [
    {
      "gate": "string identifier (e.g., 'pitch-deck-pre-validation')",
      "timestamp": "ISO-8601 timestamp",
      "reason": "string (min 20 chars; founder-provided rationale)",
      "founder_acknowledged": "boolean (must be true for the override to be honored)"
    }
  ]
}
```

### Field semantics

| Field | Required | Notes |
|---|---|---|
| `manifest_version` | yes | Currently `1`. Increment on breaking schema changes; document the migration. |
| `created` | yes | Set by the orchestrator on first write. Never changes. |
| `updated` | yes | Updated on every write (orchestrator OR called skill). |
| `intake_answers` | optional | Populated by the orchestrator at Phase 1. Pipeline skills read it as a default; never silently skip their own intake. |
| `steps[]` | yes | Always five entries, in pipeline order. Status transitions are `pending → in-progress → completed`, with `blocked` or `failed` as side-paths. |
| `steps[].iterations` | yes once `completed` | Incremented when a skill is re-run in update mode. Useful signal for the iteration-evidence check in `startup-grill`. |
| `gate_overrides[]` | yes (may be empty) | Append-only. Once recorded, an override is honored on subsequent invocations until the founder explicitly revokes it (set `founder_acknowledged: false` or remove the entry). |

### Field validation rules

- `reason` in `gate_overrides[]` must be ≥ 20 characters. The orchestrator
  rejects shorter reasons — "ok" or "fine" don't constitute consent.
- `founder_acknowledged` must be explicitly `true`. The orchestrator never
  defaults it; the founder must affirm the override.
- `iterations` must be a positive integer; default `1` on first completion.
- `mtime` should match the most recent mtime of the artifact this skill
  produces. If the artifact is updated outside the orchestrator (manual
  edit), the next orchestrator invocation should detect the discrepancy
  during state-detection reconciliation.

---

## Example 1 — Fresh start (just after Phase 1 intake)

```json
{
  "manifest_version": 1,
  "created": "2026-05-04T17:30:00Z",
  "updated": "2026-05-04T17:32:00Z",
  "intake_answers": {
    "founding_history": "no",
    "domain_experience": "yes",
    "customer_segment_experience": "no",
    "inferred_mode": "focused"
  },
  "steps": [
    { "skill": "brand-workshop",          "status": "pending" },
    { "skill": "validation-canvas",       "status": "pending" },
    { "skill": "riskiest-assumption-test", "status": "pending" },
    { "skill": "pitch-deck",              "status": "pending" },
    { "skill": "startup-grill",           "status": "pending" }
  ],
  "gate_overrides": []
}
```

The orchestrator just asked the 3-question intake, mapped it to *focused*
mode, and is about to invoke `brand-workshop`. No artifacts exist yet.

---

## Example 2 — Mid-pipeline, blocked on RAT-empty-results gate

```json
{
  "manifest_version": 1,
  "created": "2026-05-04T17:30:00Z",
  "updated": "2026-05-08T11:15:00Z",
  "intake_answers": {
    "founding_history": "yes-with-revenue",
    "domain_experience": "yes",
    "customer_segment_experience": "yes",
    "inferred_mode": "compressed-with-challenge"
  },
  "steps": [
    { "skill": "brand-workshop",          "status": "completed", "mtime": "2026-05-04T18:45:00Z", "iterations": 1 },
    { "skill": "validation-canvas",       "status": "completed", "mtime": "2026-05-05T10:20:00Z", "iterations": 1 },
    { "skill": "riskiest-assumption-test", "status": "completed", "mtime": "2026-05-06T15:30:00Z", "iterations": 1 },
    {
      "skill": "pitch-deck",
      "status": "blocked",
      "blocked_by": "rat-results-empty-for-top-3-hypotheses",
      "mtime": "2026-05-08T11:15:00Z"
    },
    { "skill": "startup-grill", "status": "pending" }
  ],
  "gate_overrides": []
}
```

A repeat founder ran through the first three skills, then hit the heavy
gate on `pitch-deck`: their RAT has top-3 hypotheses but no populated
`## Results`. The orchestrator paused here. The founder can resolve by
running their tests and updating Results, then re-invoking the orchestrator;
or by accepting an override (which would record an entry in
`gate_overrides[]` per [`gate-override-protocol.md`](gate-override-protocol.md)).

---

## Example 3 — Complete, with one recorded override

```json
{
  "manifest_version": 1,
  "created": "2026-05-04T17:30:00Z",
  "updated": "2026-05-12T16:42:00Z",
  "intake_answers": {
    "founding_history": "no",
    "domain_experience": "no",
    "customer_segment_experience": "yes",
    "inferred_mode": "focused"
  },
  "steps": [
    { "skill": "brand-workshop",          "status": "completed", "mtime": "2026-05-04T19:15:00Z", "iterations": 1 },
    { "skill": "validation-canvas",       "status": "completed", "mtime": "2026-05-07T14:30:00Z", "iterations": 3 },
    { "skill": "riskiest-assumption-test", "status": "completed", "mtime": "2026-05-09T10:20:00Z", "iterations": 2 },
    { "skill": "pitch-deck",              "status": "completed", "mtime": "2026-05-11T13:00:00Z", "iterations": 1 },
    { "skill": "startup-grill",           "status": "completed", "mtime": "2026-05-12T16:42:00Z", "iterations": 1 }
  ],
  "gate_overrides": [
    {
      "gate": "pitch-deck-pre-validation",
      "timestamp": "2026-05-11T12:30:00Z",
      "reason": "Friendly advisor meeting Friday — want directional feedback on narrative shape before validation completes for hypothesis 3.",
      "founder_acknowledged": true
    }
  ]
}
```

A first-timer founder iterated the canvas three times (loop-back from RAT
results), iterated RAT twice, accepted one pre-validation-draft override
for an early advisor meeting, and shipped the grill report. The recorded
override surfaces in the kill-report's `## Iteration Evidence` section as
something for the panel to probe — not a hidden bypass.

---

## What the manifest does NOT store

- **Founder content.** Decisions, canvas blocks, hypothesis text, slide
  copy, and grill probes all live in their respective artifact files
  (canvas markdown, RAT plan markdown, deck HTML, kill-report markdown).
  The manifest is a state journal, not a content store.
- **Long decision logs.** Per the v2.1.0 plan, the manifest scope is
  artifact-tracking + intake-answer cache. Decision-log journaling
  ("founder decided X on date Y for reason Z") was deliberately excluded
  to keep the privacy surface small and to avoid duplicating content the
  artifacts already capture.
- **Per-skill internal state.** Each pipeline skill has its own state
  semantics (e.g., `validation-canvas`'s update mode, `pitch-deck`'s
  single-slide rework mode). Those are managed inside the skill, not
  surfaced in the manifest.
- **Anything that would make the file > ~2KB on a typical run.** If a
  field starts to grow that large, it probably belongs in an artifact, not
  in the manifest.
