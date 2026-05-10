#!/bin/bash
# Hook: Hard-block destructive git commands (data-loss guardrail)
# Type: PreToolUse on Bash
# Name: protect-git
# Exit 2 = block action, stderr shown to agent as feedback
#
# Blocks:
#   - git push --force / -f         (allows --force-with-lease)
#   - git push to a protected branch (main, master, dev, develop, staging, trunk, release/*)
#   - git reset --hard
#   - git clean -f / -fd / --force
#   - git branch -D / --delete --force
#   - git checkout . / git restore . / git checkout -- . (wholesale local discard)
#
# Allows targeted variants: `git checkout -- src/foo.ts`, `git restore --staged file`,
# `git push origin feature/foo`, `git clean -n` (dry run), etc.
#
# This hook is NOT disablable via CODING_RULES_HOOK_DISABLED.
# Data-loss-critical hooks cannot be toggled off by an env var.
# To bypass for a one-off, run the command yourself in a terminal.
# To remove permanently, delete the hook entry from .claude/settings.json
# (requires a deliberate file edit, not an ambient variable).

set -u

INPUT=$(cat)
CMD=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

if [[ -z "$CMD" ]]; then
  exit 0
fi

# Lowercase for case-insensitive matching.
LC=$(echo "$CMD" | tr '[:upper:]' '[:lower:]')

block() {
  echo "BLOCKED: $1" >&2
  echo "Reason: destructive git command — data loss is hard or impossible to undo." >&2
  echo "If you really need this, run it yourself in a terminal." >&2
  echo "See coding-rules guardrails (hooks/protect-git.sh)." >&2
  exit 2
}

# 1. Force push (but allow --force-with-lease, which checks remote state first).
if echo "$LC" | grep -qE '\bgit\b.*\bpush\b.*(--force\b|[[:space:]]-f\b|[[:space:]]-[a-z]*f[a-z]*\b)'; then
  if ! echo "$LC" | grep -qE -- '--force-with-lease'; then
    block "git push --force / -f"
  fi
fi

# 2. Push to a protected branch. Matches BOOTSTRAP.md branching list.
PROTECTED='(main|master|dev|develop|staging|trunk|release/[^[:space:]]+)'
if echo "$LC" | grep -qE "\bgit\b.*\bpush\b[^|;&]*\b${PROTECTED}\b"; then
  block "git push to a protected branch"
fi

# 3. Reset --hard
if echo "$LC" | grep -qE '\bgit\b.*\breset\b.*--hard\b'; then
  block "git reset --hard"
fi

# 4. Clean with force flag.
if echo "$LC" | grep -qE '\bgit\b.*\bclean\b.*(-[a-z]*f[a-z]*\b|--force\b)'; then
  block "git clean -f / --force"
fi

# 5. Branch -D / --delete --force
if echo "$LC" | grep -qE '\bgit\b.*\bbranch\b.*(-d[a-z]*[[:space:]]|-[a-z]*d[a-z]*[[:space:]]|--delete[[:space:]]+--force\b)'; then
  # Match -D (capital D) explicitly, since lowercased above. After tr, -D becomes -d.
  # Distinguish -d (safe delete) from -D (force delete). After lowercasing both look the same,
  # so re-check the original CMD for capital -D.
  if echo "$CMD" | grep -qE '\bgit\b.*\bbranch\b.*-D\b'; then
    block "git branch -D"
  fi
  if echo "$LC" | grep -qE '\bgit\b.*\bbranch\b.*--delete[[:space:]]+--force\b'; then
    block "git branch --delete --force"
  fi
fi

# 6. Wholesale local discard: checkout . / restore . / checkout -- .
# Matches when the pathspec is exactly "." (the whole working dir).
# Allows targeted pathspecs like `git checkout -- src/foo.ts`.
if echo "$LC" | grep -qE '\bgit\b.*\b(checkout|restore)\b([[:space:]]+--)?[[:space:]]+\.([[:space:]]|$)'; then
  block "git checkout . / git restore . (wholesale local discard)"
fi

exit 0
