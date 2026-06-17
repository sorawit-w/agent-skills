#!/bin/bash
# Hook: Soft-warn when the agent READS a .env file (security awareness)
# Type: PreToolUse on Read matching .env
# Name: warn-env-read
# Exit 0 = allow action; stderr surfaced to the agent as feedback.
#
# This is the soft, behavioral counterpart to protect-env.sh (which HARD-blocks
# .env *edits*). Reading .env is legitimate (the agent often needs the var names
# to wire things up) — so this never blocks. It only reminds the agent not to
# print secret VALUES into the conversation.
#
# COVERAGE GAP (documented, not a bug): the Claude Code matcher fires on the
# `Read` tool only. An agent reading a .env via Bash (`cat .env`, `grep KEY .env`)
# is invisible to this hook. See references/threat-model.md — this rule is
# [enforced-partial]: Read tool only, not shell.
#
# Disable with: CODING_RULES_HOOK_DISABLED=warn-env-read

# Respect the disable list (non-security soft hook).
case ",${CODING_RULES_HOOK_DISABLED:-}," in
  *,warn-env-read,*) exit 0 ;;
esac

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // .tool_input.path // empty')

if [[ -z "$FILE_PATH" ]]; then
  exit 0
fi

if echo "$FILE_PATH" | grep -qE '\.env($|\.)'; then
  echo "NOTE (coding-rules): you may read this .env file, but never print its secret values into the conversation — mask to last-4 if you must reference one. See coding-rules guardrails." >&2
fi

exit 0
