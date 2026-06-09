<p align="center">
  <img src="https://raw.githubusercontent.com/sorawit-w/agent-skills/main/assets/steer-li.svg" alt="steer — redirect a run mid-flight, without losing work" width="100%"/>
</p>

# steer

A Claude Code skill for **non-destructive mid-run steering**. Drop a message into a project inbox from a second terminal while Claude is working, and a `PreToolUse` hook injects it at the next tool-call boundary — so Claude reads your course-correction *before its next action*, without discarding completed work.

> **Interim primitive for a known capability gap** (tracked in [anthropics/claude-code#30492](https://github.com/anthropics/claude-code/issues/30492)). Expected to be retired if/when native real-time steering lands in Claude Code.

## Why this exists

While Claude is mid-run, typing into the session only *queues* your message until the turn boundary. The only way to intervene immediately is `Esc` — which is **destructive**: it cancels the running tool and the in-progress work with it.

There's no non-destructive channel to say "actually, pivot the approach" without throwing away what's already done. `steer` is that channel, built from two boring, readable pieces: a one-line shell script and a small `PreToolUse` hook. It's deliberately interim — a stopgap for a tracked gap, not a permanent feature.

## What it does

- **Delivers a message at the next tool-call boundary.** `./.claude/steer "…"` from a second terminal queues text; the hook injects it before Claude's next tool call, tagged as a course-correction.
- **Frames the message so work isn't abandoned.** The injected wrapper explicitly says *"treat as a course-correction to the CURRENT task, not a new task… do not discard completed work."* This is the highest-leverage detail — a competing tool (Codex) injects mid-turn without this framing and a known failure is that the model drops in-progress work and starts a fresh thread.
- **Concatenates multiple steers in order.** Two messages before one boundary are merged, not dropped (append-based inbox).
- **Stays near-free when idle.** Empty inbox → the hook exits on a single `stat`, before spawning anything.
- **Consumes exactly once.** Rename-based atomic consume means a parallel tool-call batch (the hook fires once per call) injects the message a single time — no re-injection on the following call.
- **Installs with confirmation, never at the plugin level.** `install` / `uninstall` / `status` sub-commands wire the script and hook into a user-chosen settings file, each behind a diff-and-confirm.

## What it doesn't do

- **No instant interrupt.** Messages land at the *next tool call*, not immediately. During a long pure-reasoning stretch with no tool calls, a steer waits. Good for tool-heavy runs; useless for pure-reasoning turns. To *stop right now*, use `Esc`.
- **Cooperative, not interrupting.** "Pivot the approach" works; "stop everything this instant" still needs `Esc`. The imminent tool call still completes — the steer influences the *next* decision, it does not cancel the current one.
- **No sub-agent steering (v1).** The hook lives in the main session, so it steers the lead. Redirecting an individual sub-agent mid-run is out of scope for v1.
- **No daemon, no watcher, no config framework.** It's a file and a hook. That's the whole design.

## When to use it

- A long, tool-heavy run is heading somewhere slightly wrong and you want to correct course without losing progress.
- You realize a constraint mid-run ("use the existing util, don't add a dep") and want Claude to pick it up at the next boundary.
- You'd otherwise hit `Esc` and re-explain everything — and the work-in-progress is worth keeping.

## When not to use it

- You need an immediate hard stop → use `Esc`.
- Claude is in a pure-reasoning/text stretch with no upcoming tool calls → the message would just wait.
- You want to steer a specific sub-agent → out of scope for v1.

## How it works

1. **`steer` script** (`./.claude/steer`) appends your text to `<project>/.claude/steer-inbox` via `O_APPEND` — ordered, nothing dropped. The inbox path is derived from the script's own location, so it works from any cwd in a second terminal.
2. **`PreToolUse` hook** (`steer-inject.sh`, matcher `*`) fires before every tool call:
   - empty/missing inbox → exit immediately (no-op);
   - non-empty → atomically `mv` the inbox aside (exactly-once under parallel batches), read it, and emit it as `hookSpecificOutput.additionalContext`, wrapped in the steering tag.

```
[STEERING — treat as a course-correction to the CURRENT task, not a new task. Adjust your approach and continue; do not discard completed work unless explicitly told.]
<your message>
```

## Design choices worth knowing

- **`PreToolUse` + `additionalContext`, JSON-only.** Verified against the live hook docs: `PreToolUse` does support `hookSpecificOutput.additionalContext`, and the injected text lands *next to the tool result*. Critically, **plain stdout on `PreToolUse` is debug-log-only** — invisible to the model — so the hook emits JSON, never `echo`. Getting this wrong fails silently, which is why it was verified rather than written from memory.
- **Rename-based consume is mandatory, not a nicety.** The hook runs once *per tool call*; Claude batches parallel tool calls, so N hook instances hit one inbox near-simultaneously. `mv` succeeds for exactly one — the rest find nothing and no-op. Read-then-truncate would double-inject.
- **Single-file append over a spool directory.** Concatenate-in-order with nothing dropped, portably, with no `flock` (which isn't on stock macOS). The trade-off — `O_APPEND` atomicity is bounded by `PIPE_BUF` (~4KB) and there's a microsecond-wide consume-race window — is negligible for one human typing short messages, and documented rather than engineered around.
- **Inbox resolution is project-root anchored.** The hook finds the inbox via `CLAUDE_PROJECT_DIR` (the canonical project root Claude Code passes to hooks), falling back to the tool-call `cwd`, then `PWD` — so it works regardless of which subdirectory the session is operating in, and stays aligned with where `./.claude/steer` writes.
- **The wrapper wording is a tunable, not a constant.** The "not a new task" framing is load-bearing; the exact phrasing is meant to be tuned with testing.
- **Two-terminal friction is the point's cost.** You type into a separate terminal, not the session. This is the core ergonomic price and the reason the skill is explicitly interim.

## Install

```
/agent-skills:steer install
```

Sets up the `./.claude/steer` command and registers the `PreToolUse` hook in a settings file you choose (default: project `.claude/settings.local.json`), each behind a diff-and-confirm. Requires `jq`. **Restart the session after install** — Claude Code loads hooks at session start, so the current session won't deliver steers until then.

Other sub-commands: `/agent-skills:steer status`, `/agent-skills:steer uninstall`, `/agent-skills:steer explain`.

## Cross-skill integration

| Skill | Relationship |
|-------|--------------|
| [`coding-rules`](../coding-rules/README.md) | Shares the hook-shipping + opt-in-install pattern (resolve path → pick settings file → diff → confirm → idempotent). `steer` is a lighter, single-hook instance of the same convention. The two are independent; both can be installed in one project. |

## Status and scope

- **Current release:** v4.8.0 (initial). Supported: lead-session steering on tool-heavy runs, via a single `PreToolUse` hook + project-local `steer` script.
- **Not supported:** sub-agent steering, instant interrupts (use `Esc`), pure-reasoning-turn delivery, Windows `cmd`/PowerShell (the scripts are POSIX `bash`; WSL/Git-Bash work).
- **Dependency:** `jq`.
- **Interim by design:** expected to be retired if/when native steering ships (#30492).

## Contributions

Not accepting external contributions right now.

## License

MIT
