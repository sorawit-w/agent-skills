#!/bin/bash
# Hook: Hard-block edits to .env files (security guardrail)
# Type: PreToolUse on Edit|Write matching .env
# Name: protect-env
# Exit 2 = block action, stderr shown to agent as feedback
#
# This hook is NOT disablable via CODING_RULES_HOOK_DISABLED.
# Security-critical hooks cannot be toggled off by an env var.
# To bypass, remove the hook from .claude/settings.json (requires
# a deliberate file edit, not an ambient variable).

INPUT=$(cat)
FILE_PATH=$(echo "$INPUT" | jq -r '.tool_input.file_path // .tool_input.path // empty')

if [[ -z "$FILE_PATH" ]]; then
  exit 0
fi

if echo "$FILE_PATH" | grep -qE '\.env($|\.)'; then
  echo "BLOCKED: Do not edit .env files directly. Use environment variables and document required vars in DEVELOPER_TODO.md. See coding-rules guardrails." >&2
  exit 2
fi

exit 0
