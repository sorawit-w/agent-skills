#!/bin/bash
# Hook: inject a pending steer message as additionalContext (interim mid-run steering)
# Type: PreToolUse, matcher "*"
# Name: steer-inject
# Exit 0 on every path — this hook must NEVER error the session.
#
# Emits JSON additionalContext ONLY when the inbox is non-empty. On PreToolUse,
# plain stdout is debug-log-only and is NOT shown to Claude — the
# hookSpecificOutput.additionalContext JSON is the ONLY channel to the model.
# Do not "simplify" the jq emit to an echo; it would silently stop working.
#
# Disable with: STEER_HOOK_DISABLED=steer-inject

# Respect the disable list.
case ",${STEER_HOOK_DISABLED:-}," in
  *,steer-inject,*) exit 0 ;;
esac

INPUT=$(cat)

# Resolve the project root. Prefer CLAUDE_PROJECT_DIR (canonical root Claude Code sets for
# hooks); fall back to the hook input's cwd, then PWD. This keeps the hook's inbox aligned
# with where ./.claude/steer writes even when the session cwd is a subdirectory.
DIR="${CLAUDE_PROJECT_DIR:-}"
[ -z "$DIR" ] && DIR=$(printf '%s' "$INPUT" | jq -r '.cwd // empty' 2>/dev/null)
[ -z "$DIR" ] && DIR="$PWD"
INBOX="$DIR/.claude/steer-inbox"

# Empty / missing inbox: near-free no-op (acceptance criterion: no measurable overhead).
[ -s "$INBOX" ] || exit 0

# Atomic consume: the hook fires once per tool call, so a parallel tool-call batch
# runs N instances near-simultaneously against one inbox. `mv` succeeds for exactly
# one of them; the rest find nothing and no-op. This guarantees consumed-exactly-once.
# Never read-then-truncate — that double-injects.
CLAIM="$INBOX.consuming.$$"
mv "$INBOX" "$CLAIM" 2>/dev/null || exit 0
MSG=$(cat "$CLAIM" 2>/dev/null)
rm -f "$CLAIM"

# Whitespace-only inbox: no-op, no injection.
[ -z "$(printf '%s' "$MSG" | tr -d '[:space:]')" ] && exit 0

# Frame the message as a course-correction to the CURRENT task, not a new task.
# This negative instruction is load-bearing: without it, models tend to abandon
# in-progress work and treat the steer as a fresh thread. Tune the wording, but
# keep the "not a new task" / "do not discard completed work" intent.
WRAP="[STEERING — treat as a course-correction to the CURRENT task, not a new task. Adjust your approach and continue; do not discard completed work unless explicitly told.]
$MSG"

jq -n --arg ctx "$WRAP" \
  '{hookSpecificOutput:{hookEventName:"PreToolUse",additionalContext:$ctx}}'
exit 0
