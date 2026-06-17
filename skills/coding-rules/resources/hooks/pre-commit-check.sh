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

# Secret scan on staged files.
# NOTE: This block is intentionally not gated by CODING_RULES_HOOK_DISABLED.
# Secret scanning is a hard security rule; disabling it requires editing
# settings.json, not setting an env var.
#
# Prefer gitleaks if present — broader coverage than the built-in regex, and it
# respects a repo-local .gitleaks.toml allowlist for example/test keys. Fall back
# to the narrow regex when gitleaks is absent OR errors. Critically, distinguish a
# gitleaks FINDING (exit 1 -> hard-block) from a TOOL ERROR (exit >=2 / 127 ->
# fall through to regex). A naive "nonzero -> block" would let a gitleaks config
# crash phantom-block every commit, and the block is non-disablable.
# (trufflehog is a viable alternative scanner; not wired here to keep one external
# integration and one test surface.)
# Pick a scanner by BINARY presence, not vendor (capability-gated). Prefer
# betterleaks (gitleaks' feature-frozen successor, same author) when installed,
# else gitleaks, else the built-in regex floor below.
SECRET_SCAN_DONE=""
SCANNER=""
if command -v betterleaks >/dev/null 2>&1; then
  SCANNER=betterleaks
elif command -v gitleaks >/dev/null 2>&1; then
  SCANNER=gitleaks
fi
if [[ -n "$SCANNER" ]]; then
  # Scan the staged diff's ADDED lines via `stdin` mode — the version-stable
  # invocation that survives gitleaks' 8.19 CLI reorg (which deprecated `protect`
  # in favor of `git`) and works the same on betterleaks. Added-only (-U0 + a
  # leading-'+' filter) is deliberate: scanning context or REMOVED lines would
  # block the very commit that refactors a secret OUT into env vars.
  # --exit-code 7 gives a DISTINCT leak code: the scanners' default exit 1 means
  # "leaks OR error", so a malformed config or any tool error would otherwise
  # phantom-block this NON-disablable hook. 7 = finding; any other nonzero = tool
  # error -> fall through to the regex (so an uncooperative scanner degrades, not
  # wedges). Output is suppressed: the scanner prints the matched secret, which we
  # must not echo into the agent's context.
  git diff --cached --diff-filter=ACMR -U0 2>/dev/null \
    | grep -E '^\+[^+]' \
    | "$SCANNER" stdin --no-banner --exit-code 7 >/dev/null 2>&1
  GL_RC=$?
  if [[ "$GL_RC" -eq 7 ]]; then
    echo "WARNING: $SCANNER detected possible secrets in staged changes." >&2
    echo "Output suppressed so the secret isn't echoed here — inspect locally with '$SCANNER stdin --redact', or allowlist a false positive in the scanner's config." >&2
    echo "See coding-rules security guardrails." >&2
    exit 2  # Hard-block on findings
  elif [[ "$GL_RC" -eq 0 ]]; then
    SECRET_SCAN_DONE=1  # scanner ran clean; trust it, skip the narrower regex
  else
    # Any non-7, non-0 code = tool error (bad config, unsupported flag, exec
    # failure), NOT a finding. Fall through to the regex floor.
    echo "NOTE (coding-rules): $SCANNER exited $GL_RC (tool error, not a finding); using built-in secret regex." >&2
  fi
fi

if [[ -z "$SECRET_SCAN_DONE" ]]; then
  SECRETS_FOUND=$(git diff --cached --diff-filter=ACMR -G '(sk_live_|sk_test_|AKIA[A-Z0-9]{16}|-----BEGIN (RSA |EC |DSA )?PRIVATE KEY-----|password\s*=\s*["\x27][^\s]+)' --name-only 2>/dev/null)
  if [[ -n "$SECRETS_FOUND" ]]; then
    echo "WARNING: Possible secrets detected in staged files:" >&2
    echo "$SECRETS_FOUND" >&2
    echo "Review these files before committing. See coding-rules security guardrails." >&2
    exit 2  # Hard-block on potential secrets
  fi
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
