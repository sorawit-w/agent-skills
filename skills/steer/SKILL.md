---
name: steer
description: >
  Install, uninstall, or check the status of `steer` — an interim, non-destructive
  mid-run steering channel for Claude Code. Lets you redirect a run in flight from a
  second terminal without `Esc` (which cancels the running tool) and without losing
  in-progress work: a `steer` script drops a message into a project inbox, and a
  `PreToolUse` hook injects it as `additionalContext` at Claude's next tool-call
  boundary. Invoke ONLY when the user explicitly mentions "steer", "/steer", mid-run
  steering, or asks to install/set-up/uninstall/check that channel. Sub-commands via
  the args parameter: `install` (default), `uninstall`, `status`, `explain`. Does NOT
  trigger on general coding tasks, on "steer the conversation" used figuratively, or
  on car/boat/navigation senses of the word.
instructions: |
  Load this skill when: the user wants to set up, remove, or inspect the steer mid-run
  steering channel, or asks how it works.
  Do NOT load this skill when: the user uses "steer" figuratively ("let's steer toward
  X"), or wants a different kind of interrupt (that's `Esc`, native to Claude Code).
tags:
  - claude-code
  - hooks
  - workflow
---

# steer — interim mid-run steering for Claude Code

`steer` is a small, non-destructive channel for redirecting Claude **mid-run without losing in-progress work**. Today the only immediate intervention while Claude is working is `Esc`, which cancels the running tool. `steer` adds a cooperative alternative: from a second terminal you run `./.claude/steer "…"`, and a `PreToolUse` hook injects that message at Claude's next tool-call boundary, so Claude reads it before deciding its next action.

> **Interim primitive for a known capability gap** (tracked in [anthropics/claude-code#30492](https://github.com/anthropics/claude-code/issues/30492)). Expected to be retired if/when native steering lands in Claude Code.

**The skill ships two boring, readable pieces** under `./resources/`:
- `resources/hooks/steer-inject.sh` — the `PreToolUse` hook (matcher `*`).
- `resources/.claude/steer` — the `steer` script, installed into the project as `./.claude/steer`.

`install` wires both into the user's project with per-step confirmation; nothing is registered at the plugin level.

---

## How it works (mechanism)

1. **`steer` script** — appends your text to `<project>/.claude/steer-inbox` (atomic-enough via `O_APPEND`; multiple steers before a boundary concatenate in order, nothing dropped). Run it from a second terminal while Claude works.
2. **`PreToolUse` hook** — fires before every tool call. If the inbox is empty it exits immediately (near-free no-op). If non-empty it **atomically consumes** the inbox (rename, so a parallel tool-call batch injects exactly once) and emits the message as `hookSpecificOutput.additionalContext`, wrapped in a tag that frames it as a course-correction to the current task — not a new one.

The injected wrapper:

```
[STEERING — treat as a course-correction to the CURRENT task, not a new task. Adjust your approach and continue; do not discard completed work unless explicitly told.]
<your message>
```

**Verified design note.** For `PreToolUse`, plain stdout is debug-log-only — the hook must emit the `additionalContext` JSON, never `echo`. The injected text lands *next to the tool result*: the imminent tool call still completes (steer is cooperative, not interrupting), and the message influences Claude's *next* decision.

---

## Locating the bundled scripts

The skill is self-contained — scripts live under `./resources/` relative to this SKILL.md. Resolve the absolute paths via the first method that succeeds:

1. **Glob discovery (preferred).** `Glob` for `**/skills/steer/resources/hooks/steer-inject.sh`. Common locations: `~/.claude/skills/steer/...` (global) or `<project>/.claude/skills/steer/...` (project-local). The `steer` script is the sibling at `**/skills/steer/resources/.claude/steer`.
2. **`STEER_DIR` env var.** If set, use `${STEER_DIR}/resources/...`.
3. **Ask the user.** If both fail: "Where is your steer install? (Could not auto-locate steer-inject.sh.)"

---

## Sub-command routing

Determine the sub-command from `args` (default `install` when empty). Natural language maps too: "set up steer" / "add steer to this project" → `install`; "remove steer" → `uninstall`; "is steer installed?" → `status`; "how does steer work?" → `explain`.

---

## `explain`

Summarize the mechanism (the "How it works" section above) and the limitations (see README), then offer to `install`. No file changes.

---

## `install`

Two independent, opt-in phases. **Both modify user files — never silently. Always show the diff and require confirmation. Either phase is independently skippable.** Run Phase 1 first, then ask whether to run Phase 2.

**Dependency check (before either phase):** confirm `jq` is available (`command -v jq`). The hook needs it to read stdin and emit JSON. If missing, tell the user to install `jq` first (`brew install jq` / `apt-get install jq`); the hook is a silent no-op without it.

### Phase 1 — the `steer` command

1. Resolve the bundled `steer` script path (per "Locating the bundled scripts").
2. Target is `<project>/.claude/steer`. If `<project>/.claude/` does not exist, ask before creating it.
3. If `<project>/.claude/steer` already exists, diff it against the bundled version; report `already installed` if identical, otherwise show the diff.
4. Show the user what will be copied. Ask: `Install the steer command to ./.claude/steer? [y/n]`
5. On `y`: copy the bundled `steer` script to `<project>/.claude/steer` and `chmod +x` it. On `n`: skip.
6. Recommend adding `/.claude/steer-inbox` to the project's `.gitignore` (the inbox is transient, machine-local state). Offer to append it, behind a confirmation.

### Phase 2 — the `PreToolUse` hook

After Phase 1, ask once:

> Register the `steer-inject` `PreToolUse` hook? It fires on every tool call (near-free when the inbox is empty) and injects any queued steer message at the next boundary. [y/n]

If `n`, end install — Phase 1 alone is not useful without the hook, so note that the channel won't deliver until the hook is registered.

If `y`:

1. **Resolve the absolute path** to `resources/hooks/steer-inject.sh` (Glob, else `${STEER_DIR}/resources/hooks/steer-inject.sh`, else ask). `chmod +x` it if needed.
2. **Pick the settings file**. Ask:
   > Where should the hook be registered?
   >   1. `~/.claude/settings.json` (global — every project)
   >   2. `<project>/.claude/settings.local.json` (this project, your machine only — gitignored)
   >   3. `<project>/.claude/settings.json` (this project, committed — teammates inherit)
   > Choose 1, 2, or 3. **Default: 2** (lowest blast radius, easiest to revert).
3. **Read or create the settings file.** If missing, create with `{}`. **If the JSON is malformed, STOP** and ask the user to fix it — never overwrite a file we couldn't parse.
4. **Build the hook entry** (matcher `*`, with a short `timeout` since it runs on every tool call):

   ```json
   {
     "matcher": "*",
     "hooks": [
       { "type": "command", "command": "<abs>/steer-inject.sh", "timeout": 5 }
     ]
   }
   ```

   Insert under `hooks.PreToolUse` (create the array if absent).
5. **Detect already-managed entries.** An entry is *steer-managed* iff its `command` ends in `steer-inject.sh` AND its path contains `/skills/steer/resources/hooks/`. Skip if present — install is idempotent.
6. **Show the full diff** of what will be added to the chosen settings file, including the resolved absolute path.
7. **Single final confirmation** — `Apply this diff? [y/n]`. On `n`, abort without modifying. On `y`, write the merged JSON back, preserving all unrelated keys exactly.
8. **Summarize**, then state plainly: the hook takes effect in **new** sessions — Claude Code loads hooks at session start, so the current session won't deliver steers until restarted.

### Quick how-to-use reminder (print after install)

> From a **second terminal**, while Claude is working:
> ```
> ./.claude/steer "pivot to the simpler approach — don't refactor the parser yet"
> ```
> It delivers at Claude's next tool call. Multiple steers before a boundary concatenate in order. It's cooperative — to *stop* a running tool immediately, use `Esc`.

---

## `uninstall`

Mirror of `install` — both phases opt-in and confirmed before any change.

### Phase 1 — the `steer` command
1. If `<project>/.claude/steer` exists and matches a steer-managed script (header line contains `steer — queue a mid-run steering message`), show it and ask: `Remove ./.claude/steer? [y/n]`.
2. On `y`, delete it. Offer to remove a leftover `./.claude/steer-inbox` if present.

### Phase 2 — the hook
1. Ask which settings file to clean (same three options; default 2).
2. Find every hook entry whose `command` ends in `steer-inject.sh` AND whose path contains `/skills/steer/resources/hooks/`. Show the matched entries.
3. Single confirmation — `Remove these entries? [y/n]`. On `y`, remove them, then run the cleanup chain: drop an empty `matcher` group → drop an empty `PreToolUse` array → drop an empty `hooks` key. Touch no other keys.
4. Summarize.

**Uninstall does NOT touch:** hand-written hook entries that don't match the steer path signature; the bundled scripts under `resources/`; or the current session (hooks unload only at next session start).

---

## `status`

1. Check whether `<project>/.claude/steer` exists and is executable.
2. Read the candidate settings files (`~/.claude/settings.json`, project `.claude/settings.json`, project `.claude/settings.local.json`) and look for a `PreToolUse` entry whose `command` matches the steer path signature.
3. Confirm `jq` availability.
4. Report:
   > **steer:** command `<installed|missing>` · hook `<registered in <file>|not registered>` · jq `<present|MISSING>`.

   If the hook is registered but the user reports it not working, remind them hooks load at session start — they must restart the session after install.

---

## What NOT to do

- **Do NOT auto-invoke this skill on general coding tasks** or figurative "steer" usage. It is opt-in only.
- **Do NOT register the hook at the plugin level.** No `hooks` field in the parent plugin's `plugin.json`. Activation stays skill-scoped and opt-in via Phase 2.
- **Do NOT silently modify user files.** Every copy, settings write, and `.gitignore` edit requires confirmation after showing the change.
- **Do NOT "simplify" the hook's `jq` emit to an `echo`.** On `PreToolUse`, plain stdout is invisible to Claude; only the `additionalContext` JSON reaches the model.
- **Do NOT replace the rename-based consume with read-then-truncate.** The hook fires once per tool call; a parallel batch runs it N times against one inbox, and only `mv` guarantees exactly-once consumption.
- **Do NOT promise the current session will deliver steers right after install.** Hooks load at session start — say so.
- **Do NOT claim a native-steering release date.** Positioning is conditional: retired *if/when* native steering ships (#30492), no roadmap commitment.
