#!/bin/bash
# Self-test for warn-env-read.sh — zero-framework, self-contained.
#
# Run from anywhere: bash warn-env-read.test.sh
# Exit 0 = all assertions pass; non-zero = a failure.

set -u

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
HOOK="$SCRIPT_DIR/warn-env-read.sh"

FAILS=0
pass() { echo "PASS: $1"; }
fail() { echo "FAIL: $1"; FAILS=$((FAILS + 1)); }

run() { # $1=json input ; sets RC and ERR
  ERR=$(echo "$1" | bash "$HOOK" 2>&1 >/dev/null); RC=$?
}

# 1. Read of a .env file -> exit 0 + a stderr note.
run '{"tool_input":{"file_path":"/proj/.env"}}'
[[ "$RC" -eq 0 ]] && pass ".env read exits 0" || fail ".env read should exit 0 (got $RC)"
echo "$ERR" | grep -q "never print its secret values" \
  && pass ".env read emits the secret-print warning" \
  || fail ".env read should warn (got: '$ERR')"

# 2. Variant .env name (.env.local) also warns.
run '{"tool_input":{"file_path":".env.local"}}'
echo "$ERR" | grep -q "coding-rules" && pass ".env.local warns" || fail ".env.local should warn"

# 3. Non-.env read -> exit 0, silent.
run '{"tool_input":{"file_path":"src/app.ts"}}'
[[ "$RC" -eq 0 && -z "$ERR" ]] \
  && pass "non-.env read silent exit 0" \
  || fail "non-.env read should be silent exit 0 (rc=$RC, err='$ERR')"

# 4. Disabled via env var -> silent even for a .env read.
ERR=$(echo '{"tool_input":{"file_path":".env"}}' | CODING_RULES_HOOK_DISABLED=warn-env-read bash "$HOOK" 2>&1 >/dev/null); RC=$?
[[ "$RC" -eq 0 && -z "$ERR" ]] \
  && pass "disabled -> silent exit 0" \
  || fail "disabled should be silent (rc=$RC, err='$ERR')"

# 5. Empty/missing path -> exit 0, silent.
run '{"tool_input":{}}'
[[ "$RC" -eq 0 && -z "$ERR" ]] \
  && pass "missing path silent exit 0" \
  || fail "missing path should be silent exit 0 (rc=$RC, err='$ERR')"

echo "---"
if [[ "$FAILS" -eq 0 ]]; then
  echo "All assertions passed."
  exit 0
else
  echo "$FAILS assertion(s) failed."
  exit 1
fi
