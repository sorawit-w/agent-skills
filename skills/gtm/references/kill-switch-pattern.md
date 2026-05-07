# Kill Switch Pattern

The architectural enforcement layer for stopping GTM from acting. Prompt-only
kill switches don't work — agents rationalize past them under task-completion
pressure, especially when running unattended on schedules. The pattern below
is the *only* enforcement layer GTM relies on.

## Three layers, in order of reliability

### Layer 1 — `.gtm/HALT` file (per-project)

A file in the project's `.gtm/` folder. Its presence means "no external
actions, period." Optional contents: a single text line with a reason.

**Check happens before every external call** via `require_active()` helper.
The agent does not decide whether to honor it; the helper enforces.

**To halt:** founder writes the file. Three ways:

```bash
# Option A — touch
touch .gtm/HALT

# Option B — touch with reason
echo "PR fire on TikTok account" > .gtm/HALT

# Option C — via gtm convenience command (writes the file)
gtm halt --reason "PR fire on TikTok account"
```

**To resume:** founder removes the file. `rm .gtm/HALT` or `gtm resume`.

**Why a file:** simple, visible (shows up in `git status`), readable from
outside the agent's context. The founder can halt by editing in any text
editor, even on mobile if the project is in a synced folder.

### Layer 2 — `state.json#status` (in-band but checked by helper)

Soft pause — finish in-flight work but no new actions.

```json
{
  "status": "active | paused | halted",
  "...": "..."
}
```

`require_active()` checks `status` after `HALT` file. If `status != "active"`,
no new external action fires. In-flight actions (e.g., a multi-step content
fan-out that's already started) finish; new ones don't start.

**To pause:** `gtm pause` writes `status: "paused"` to state.json. Useful
when the founder wants to stop new work but let current cycle finish cleanly.

### Layer 3 — Harness-killable scheduled tasks

The most reliable layer because it's outside the agent's blast radius
entirely. Scheduled tasks are registered via the `schedule` skill, which
the harness manages. The founder can disable scheduled tasks from the
Cowork (or Claude Code) scheduling UI even if the agent inside the run is
misbehaving.

This means: even if a hypothetical bug prevented the HALT file from
working, the founder still controls *whether the agent runs at all* via
the harness UI.

## The `require_active()` helper

The contract is small and load-bearing:

```python
def require_active(gtm_root: Path) -> tuple[bool, str | None]:
    """
    Returns (True, None) if external actions may proceed.
    Returns (False, reason) if any kill-switch layer says no.
    Wrappers MUST call this before any external action.
    """
    halt_file = gtm_root / "HALT"
    if halt_file.exists():
        reason = halt_file.read_text().strip() or "HALT file present"
        return False, f"halted: {reason}"

    state_path = gtm_root / "state.json"
    if not state_path.exists():
        return False, "halted: missing state.json (uninitialized)"

    state = json.loads(state_path.read_text())
    if state.get("status") != "active":
        return False, f"halted: state.status={state.get('status')}"

    return True, None
```

The helper itself is short and audit-friendly. The agent doesn't *decide*
whether to honor it — the helper enforces, and any code path that calls an
external API without going through the helper is a skill bug.

## Other gating helpers

`require_active()` is one of five gates. The full chain for any external
action:

```python
ok, reason = require_active(gtm_root)
if not ok:
    log_refusal(reason); return

ok, reason = check_dry_run(state, action)  # respects mode=p1 + dry-run config
if not ok:
    log_skip(reason); return

ok, reason = check_budget(config, category, cost)
if not ok:
    escalate(reason); return

ok, reason = check_compliance(config, content)  # CAN-SPAM/GDPR/FTC/TOS
if not ok:
    escalate_and_refuse(reason); return

ok, reason = check_first_use_gate(state, channel)
if not ok:
    queue_for_human_review(reason); return

execute(action)
log_event(action)
```

Each helper is small, testable, and refuses by default. The chain order
matters: HALT first (cheapest check, hardest stop), then dry-run (next
cheapest), then budget, then compliance, then first-use gate.

## What the agent MUST NOT do

1. **Bypass the helpers.** Any external API call must pass through the
   gating chain. Direct API calls without `require_active()` are a skill
   bug, caught in code review of any contribution.

2. **Argue with HALT.** When `require_active()` returns False, the only
   acceptable behavior is log + return. Not "let me check why," not "this
   action is harmless," not "the founder probably forgot to remove the
   file." Just stop.

3. **Use prompt-text as a kill switch.** "If user says stop, stop" in the
   prompt is theater. The helper-function pattern is the only enforcement.

4. **Persist past HALT.** A scheduled task that fires while HALT is
   present must check HALT and exit cleanly without producing any output.
   It does not retry, does not "wait for HALT to clear" — it simply exits.

## What the agent MAY do under HALT

1. **Read state and respond to the founder.** "Yes, GTM is halted because
   X." Reading is not an external action.

2. **Plan in dry-run mode.** "If we resumed, here's what cycle would
   produce" — no external action fires, no events logged. Useful for the
   founder deciding whether to clear HALT.

3. **Exit cleanly.** Logging "halted: <reason>" once per invocation is
   the only side effect.

## Audit trail

Every refusal logs to `.gtm/state.json#refusal_log[]`:

```json
{
  "refusal_log": [
    {
      "timestamp": "2026-05-05T12:34:56Z",
      "gate": "require_active | check_dry_run | check_budget | check_compliance | check_first_use_gate",
      "reason": "halted: PR fire on TikTok",
      "action_skipped": {
        "type": "post_to_x",
        "draft_id": "draft_..."
      }
    }
  ]
}
```

The log is append-only, capped at 1000 entries (oldest pruned), and
surfaced in the next digest. Auditing why GTM didn't act is as important
as auditing why it did.

## Honest limitations

This is a Claude-based skill running in a Claude Code or Cowork harness.
The agent has the same tools the founder has. The architectural pattern
is **best-effort enforcement**, not perfect sandboxing. What we can do:

1. Make the helper-function chain very explicit in the SKILL.md
2. Have the harness's schedule UI be the actually-killable layer
3. Surface "actions taken since last digest" in every digest so drift is
   visible
4. Recommend the founder not run unattended for >24h until P3 trust is
   established

What we cannot do:

1. Prevent a future skill bug from skipping the chain (caught in review,
   but not at runtime)
2. Stop the agent from emitting prose claiming it would have acted
   (it can talk; it just can't *act* without going through the helpers)

This limitation is documented honestly so founders set expectations
correctly. P3 (autonomous) is appropriate only after observing the trust
ramp work end-to-end.
