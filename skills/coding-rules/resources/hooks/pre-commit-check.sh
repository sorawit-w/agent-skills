#!/bin/bash
# Hook: Soft-warn if lint/test haven't been run before committing
# Type: PreToolUse on Bash matching git commit
# Name: pre-commit-check
# Exit 0 = allow action, stdout injected as context for the agent
#
# This does NOT hard-block commits. It checks if lint/test commands
# were run recently in this session and reminds the agent if not.
# This avoids blocking on pre-existing lint errors from other developers.
#
# Disable the soft reminder with: CODING_RULES_HOOK_DISABLED=pre-commit-check
# The secret scan below cannot be disabled via env var — it is a
# security guardrail. To bypass, remove the hook from settings.json.

INPUT=$(cat)
COMMAND=$(echo "$INPUT" | jq -r '.tool_input.command // empty')

# Only check git commit commands
if ! echo "$COMMAND" | grep -qE '^git commit'; then
  exit 0
fi

# Check for unstaged secret patterns in staged files
# NOTE: This block is intentionally not gated by CODING_RULES_HOOK_DISABLED.
# Secret scanning is a hard security rule; disabling it requires editing
# settings.json, not setting an env var.
SECRETS_FOUND=$(git diff --cached --diff-filter=ACMR -G '(sk_live_|sk_test_|AKIA[A-Z0-9]{16}|-----BEGIN (RSA |EC |DSA )?PRIVATE KEY-----|password\s*=\s*["\x27][^\s]+)' --name-only 2>/dev/null)

if [[ -n "$SECRETS_FOUND" ]]; then
  echo "WARNING: Possible secrets detected in staged files:" >&2
  echo "$SECRETS_FOUND" >&2
  echo "Review these files before committing. See coding-rules security guardrails." >&2
  exit 2  # Hard-block on potential secrets
fi

# Respect the disable list for the soft reminder only.
case ",${CODING_RULES_HOOK_DISABLED:-}," in
  *,pre-commit-check,*) exit 0 ;;
esac

# Soft reminder — injected as context, does not block
cat <<'EOF'
REMINDER (coding-rules): Before committing, ensure you have:
1. Run the project's lint command on your changed files
2. Run the project's test suite
3. Verified the build passes
If any of these are failing due to YOUR changes, fix them before committing.
Pre-existing failures from other code are acceptable — do not block on them.
EOF

exit 0
