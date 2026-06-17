#!/bin/bash
# Self-test for protect-git.sh — verifies destructive git commands are blocked
# (exit 2) and that legitimate / targeted variants are allowed (exit 0).
#
# Run from anywhere: bash protect-git.test.sh
# Exit 0 = all assertions pass; non-zero = a failure.

set -u

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
HOOK="$SCRIPT_DIR/protect-git.sh"

FAILS=0
pass() { echo "PASS: $1"; }
fail() { echo "FAIL: $1"; FAILS=$((FAILS + 1)); }

run() { # $1 = command string -> sets RC
  printf '{"tool_input":{"command":%s}}' "$(printf '%s' "$1" | jq -R .)" | bash "$HOOK" >/dev/null 2>&1
  RC=$?
}

# --- Must BLOCK (exit 2) -----------------------------------------------------
BLOCK=(
  "git push --force origin feature/x"
  "git push -f origin feature/x"
  "git push origin main"
  "git push origin master"
  "git push origin develop"
  "git reset --hard HEAD~1"
  "git clean -fd"
  "git clean --force"
  "git branch -D oldfeature"
  "git checkout ."
  "git restore ."
  "git checkout -- ."
)
for cmd in "${BLOCK[@]}"; do
  run "$cmd"
  [[ "$RC" -eq 2 ]] && pass "blocks: $cmd" || fail "should block (got $RC): $cmd"
done

# --- Must ALLOW (exit 0) -----------------------------------------------------
ALLOW=(
  "git push --force-with-lease origin feature/x"
  "git push origin feature/foo"
  "git checkout -- src/foo.ts"
  "git restore --staged src/foo.ts"
  "git clean -n"
  "git branch -d oldfeature"
  "git status"
  "git commit -m wip"
)
for cmd in "${ALLOW[@]}"; do
  run "$cmd"
  [[ "$RC" -eq 0 ]] && pass "allows: $cmd" || fail "should allow (got $RC): $cmd"
done

# Empty command -> exit 0.
printf '{"tool_input":{"command":""}}' | bash "$HOOK" >/dev/null 2>&1
[[ "$?" -eq 0 ]] && pass "empty command exits 0" || fail "empty command should exit 0"

echo "---"
if [[ "$FAILS" -eq 0 ]]; then
  echo "All assertions passed."
  exit 0
else
  echo "$FAILS assertion(s) failed."
  exit 1
fi
