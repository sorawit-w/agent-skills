# State Detection — Manifest + Filesystem Reconciliation

When the orchestrator (or any pipeline skill) reads `kit-manifest.json`
(at `<kit-root>/kit-manifest.json` — default
`docs/startup-kit/kit-manifest.json` in v2.2.0+, with legacy
`./kit-manifest.json` as a backward-compat fallback), the manifest may
disagree with the filesystem. Real artifacts can appear without manifest
entries (manual run between orchestrator invocations); manifest entries can
reference artifacts that have been deleted. **Filesystem state always
wins**; the manifest is a hint that gets reconciled to match reality.

This document defines the reconciliation rules. Apply them at every
orchestrator Phase 0 (after manifest discovery) and at every pipeline
skill's Step 0.0 (manifest awareness).

---

## The four states

For each of the five pipeline skills, there are four possible combinations of
manifest-says vs. filesystem-says:

| # | Manifest says | Filesystem says | Action |
|---|---|---|---|
| 1 | completed | artifact present, mtime matches | trust manifest; proceed |
| 2 | completed | artifact present, mtime > 30 days older than now | surface stale-artifact warning; offer refresh |
| 3 | completed | artifact missing | mark step as `failed`; recommend re-run |
| 4 | pending / missing entry | artifact present | absorb into manifest with `status: completed` and the artifact's mtime; assume manual run |

These cover the reconciliation cases. The orchestrator handles each silently
(no founder intervention needed for absorption) except case 2, where the
founder is asked whether to refresh.

---

## Detailed rules

### Rule 1 — Trust filesystem on artifact presence/absence

The manifest's `steps[].status` is a hint about the *last known state*. The
filesystem is the ground truth. If they disagree, the filesystem wins.

- Manifest says `completed`, file exists → trust manifest.
- Manifest says `completed`, file gone → mark `failed`; the manifest is
  out of date; the founder probably deleted the artifact intentionally or
  unintentionally. Recommend re-run rather than silently restoring.
- Manifest says `pending`, file exists → absorb into manifest (case 4).
  Likely the founder ran the skill manually between orchestrator
  invocations.
- Manifest entry missing entirely, file exists → same as above; absorb.

### Rule 2 — Stale-artifact threshold (30 days)

If the manifest says `completed` and the file's mtime is more than 30 days
older than the current time, surface a one-line warning:

> *"Manifest says you ran [skill] on [date], 35 days ago. Update mode
> (refresh from current state), keep as-is, or skip?"*

This is non-blocking — the founder can choose to keep the stale artifact.
The threshold is an opinion (validation work older than a month is usually
worth refreshing); founders working on long-cycle ideas can override.

### Rule 3 — Mtime mismatch (file edited outside the orchestrator)

If the manifest's recorded mtime is *older* than the file's actual mtime
(but the file still exists), the artifact was edited outside the
orchestrator's awareness. Two sub-cases:

- **Slight drift (< 1 hour):** likely the founder made a small in-place
  edit. Update the manifest's mtime silently to match the file. No prompt.
- **Significant drift (≥ 1 hour):** likely a manual update mode run
  outside the orchestrator. Surface a one-liner: *"Looks like you updated
  [artifact] on [new mtime] outside the orchestrator. I'll mark this as
  iteration #[N+1]."* Increment `iterations` counter; update mtime.

Mtime mismatch never blocks — it just gets recorded.

### Rule 4 — Intake-answers cache reconciliation

The `intake_answers` cache is a hint, not truth. On every orchestrator
invocation:

- If `intake_answers` is present, surface them: *"Manifest says: [founding
  history], [domain], [customer experience] → [mode]. Confirm or update?"*
- The founder can confirm (no change) or update any field. On update,
  re-run the mode-mapping logic and rewrite the cache.
- On a fresh run with no cache, ask all three questions per Phase 1.

The cache is *never* silently trusted across sessions — the founder's
self-assessment may have changed (especially after a successful
loop-back).

### Rule 5 — Gate-override reconciliation

The `gate_overrides[]` array is **append-only and persistent**. Once
recorded, an override is honored on subsequent invocations until the
founder explicitly revokes it (sets `founder_acknowledged: false` or
removes the entry).

The orchestrator surfaces each active override on resume:

> *"Manifest records 1 active gate override:
> `pitch-deck-pre-validation` (from 2026-05-11, reason: 'Friendly advisor
> meeting'). Still in effect — confirm to proceed, or revoke?"*

The founder can confirm or revoke. Revocation removes the entry; the
gate becomes binding again on the next downstream invocation.

### Rule 6 — Status `blocked` requires explicit unblocking

When a step's status is `blocked` (with `blocked_by` set), the orchestrator
does not silently re-attempt the step on resume. It first surfaces:

> *"Step `[skill]` was blocked on [date] by `[blocked_by]`. Has that been
> resolved?"*

Then either:
- **Founder says yes:** clear the `blocked` status, set to `pending`,
  re-attempt the step.
- **Founder says no:** keep blocked; surface what needs to happen
  (typically: re-run the upstream skill in update mode, or accept an
  override).

This protects against silent retries that would just hit the same gate
again.

---

## Pseudo-code: reconciliation loop

```
function reconcile(manifest, working_dir):
  for step in manifest.steps:
    artifact_path = expected_path_for(step.skill, working_dir)
    artifact_exists = file_exists(artifact_path)
    artifact_mtime = artifact_exists ? stat(artifact_path).mtime : null

    case (step.status, artifact_exists):
      ("completed", true):
        if artifact_mtime > step.mtime + 1_hour:
          step.iterations += 1
          step.mtime = artifact_mtime
          notify_founder("manual update detected")
        elif now() - artifact_mtime > 30_days:
          ask_founder("stale artifact — refresh?")
        # else: trust manifest

      ("completed", false):
        step.status = "failed"
        notify_founder("artifact missing — recommend re-run")

      ("pending" or missing, true):
        step.status = "completed"
        step.mtime = artifact_mtime
        step.iterations = 1
        notify_founder("absorbed manual run")

      ("pending" or missing, false):
        # nothing to do; step is genuinely pending

      ("blocked", _):
        # do not touch; explicit unblocking required (Rule 6)

      ("in-progress", _):
        # likely a crashed previous run; ask founder how to proceed

      ("failed", true):
        step.status = "completed"
        step.mtime = artifact_mtime
        notify_founder("artifact reappeared — marking completed")

      ("failed", false):
        # nothing to do; step needs re-run

  for override in manifest.gate_overrides:
    if override.founder_acknowledged:
      surface_active_override(override)
    # revoked overrides are skipped silently
```

---

## What state detection does NOT do

- **Auto-recover from corrupt manifest.** If the JSON fails to parse, the
  orchestrator logs the issue and proceeds as if no manifest exists. It
  does NOT attempt to repair the file. (The founder may have intentionally
  edited it; auto-repair would clobber their changes.)
- **Resolve content disagreements.** If the manifest's `intake_answers`
  cache says "repeat founder" but the canvas's content reads as
  first-timer, the orchestrator does not flag this. Content
  reconciliation is downstream skills' job.
- **Migrate older manifest versions.** v1 is the only supported
  `manifest_version` in v2.1.0. If a future version exists in the working
  directory (downgrade scenario), the orchestrator refuses to proceed and
  asks the founder how to handle it.
- **Lock the manifest.** No file locking. The orchestrator and called
  skills coordinate via atomic-write discipline (write `.tmp`, rename),
  not via locks. If two orchestrator invocations race, the second one's
  state-detection pass will absorb whatever the first one wrote.
