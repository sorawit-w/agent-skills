#!/bin/bash
# Self-test for pre-commit-check.sh — zero-framework, self-contained.
# Exercises the gitleaks/regex secret-scan branches deterministically by stubbing
# `gitleaks` and controlling PATH, so results don't depend on gitleaks being
# installed on the test machine.
#
# Run from anywhere: bash pre-commit-check.test.sh
# Exit 0 = all assertions pass; non-zero = a failure.

set -u

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
HOOK="$SCRIPT_DIR/pre-commit-check.sh"

FAILS=0
pass() { echo "PASS: $1"; }
fail() { echo "FAIL: $1"; FAILS=$((FAILS + 1)); }

TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT

# --- Controlled PATHs: no scanner / stub gitleaks / stub betterleaks+gitleaks --
BIN_NO="$TMP/bin_no"   # tools only, NO scanner (forces regex fallback)
BIN_GL="$TMP/bin_gl"   # tools + stub gitleaks
BIN_BL="$TMP/bin_bl"   # tools + stub betterleaks AND stub gitleaks (precedence)
mkdir -p "$BIN_NO" "$BIN_GL" "$BIN_BL"
for t in bash git jq grep sed cat head tail env; do
  real="$(command -v "$t")" && ln -s "$real" "$BIN_NO/$t" && ln -s "$real" "$BIN_GL/$t" && ln -s "$real" "$BIN_BL/$t"
done
ARGS_FILE="$TMP/scanner_args"

# Each stub records "<name> <args>" then exits the code the test asked for via the
# named env var. Built line-by-line so $2/$3 expand now but $* / exit value don't.
mk_scanner_stub() { # $1=path  $2=scanner-name  $3=rc-env-var-name
  {
    echo '#!/bin/bash'
    echo "printf '$2 %s\\n' \"\$*\" >> \"\${SCANNER_ARGS_FILE:-/dev/null}\""
    echo "exit \"\${$3:-0}\""
  } > "$1"
  chmod +x "$1"
}
mk_scanner_stub "$BIN_GL/gitleaks"    gitleaks    GITLEAKS_STUB_RC
mk_scanner_stub "$BIN_BL/betterleaks" betterleaks BETTERLEAKS_STUB_RC
mk_scanner_stub "$BIN_BL/gitleaks"    gitleaks    GITLEAKS_STUB_RC

# --- Fixture git repo --------------------------------------------------------
REPO="$TMP/repo"
mkdir -p "$REPO"
git -C "$REPO" init -q

COMMIT_INPUT='{"tool_input":{"command":"git commit -m test"}}'

stage_clean() {
  echo "const port = 3000;" > "$REPO/app.js"
  git -C "$REPO" add app.js
}
stage_secret() {
  # A fake Stripe-style key the built-in regex matches.
  echo 'const k = "sk_live_ABCDEFG1234567890fake";' > "$REPO/secret.js"
  git -C "$REPO" add secret.js
}
reset_index() { git -C "$REPO" rm -r --cached -q -f . >/dev/null 2>&1 || true; rm -f "$REPO"/*.js; }

run_hook() { # $1=PATH  $2=gitleaks_rc(opt)  $3=betterleaks_rc(opt)
  ( cd "$REPO" && echo "$COMMIT_INPUT" | PATH="$1" \
      GITLEAKS_STUB_RC="${2:-0}" BETTERLEAKS_STUB_RC="${3:-0}" \
      SCANNER_ARGS_FILE="$ARGS_FILE" bash "$HOOK" >/dev/null 2>&1 )
}

# --- Assertions --------------------------------------------------------------

# A. gitleaks reports a finding (DISTINCT leak code 7) -> hard-block (exit 2).
reset_index; stage_clean; : > "$ARGS_FILE"
run_hook "$BIN_GL" 7; rc=$?
[[ "$rc" -eq 2 ]] && pass "gitleaks finding (exit 7) -> exit 2" || fail "gitleaks finding should exit 2 (got $rc)"

# A2. The hook MUST use the version-stable `stdin` mode (NOT the deprecated
#     `protect`) and request a DISTINCT leak code (default exit 1 = "leaks OR error").
grep -q 'gitleaks stdin' "$ARGS_FILE" \
  && pass "hook uses stdin mode (not deprecated protect)" \
  || fail "hook should call '<scanner> stdin' (args: $(cat "$ARGS_FILE"))"
grep -q -- '--exit-code 7' "$ARGS_FILE" \
  && pass "hook requests --exit-code 7" \
  || fail "hook must pass --exit-code 7 (args: $(cat "$ARGS_FILE"))"
grep -q 'protect' "$ARGS_FILE" \
  && fail "hook still uses deprecated 'protect' subcommand" \
  || pass "hook does not use deprecated 'protect'"

# B. scanner clean (rc 0) is TRUSTED -> regex skipped even with a secret staged -> exit 0.
reset_index; stage_secret
run_hook "$BIN_GL" 0; rc=$?
[[ "$rc" -eq 0 ]] && pass "gitleaks clean trusted, skips regex -> exit 0" || fail "gitleaks clean should exit 0 (got $rc)"

# C. NO scanner + staged secret -> regex fallback hard-blocks (exit 2).
reset_index; stage_secret
run_hook "$BIN_NO"; rc=$?
[[ "$rc" -eq 2 ]] && pass "no scanner + secret -> regex fallback exit 2" || fail "regex fallback should exit 2 (got $rc)"

# D. scanner ERROR returning the AMBIGUOUS default code 1 + clean staged ->
#    must be a TOOL ERROR (not a finding) -> fall back -> NOT blocked.
#    Codex P2 scenario: a malformed scanner config must not phantom-block.
reset_index; stage_clean
run_hook "$BIN_GL" 1; rc=$?
[[ "$rc" -eq 0 ]] && pass "gitleaks exit 1 (error, not leak) + clean -> exit 0 (no phantom block)" || fail "exit-1 error+clean should exit 0 (got $rc)"

# E. scanner ERROR (rc 1) + staged secret -> fall back to regex -> exit 2.
reset_index; stage_secret
run_hook "$BIN_GL" 1; rc=$?
[[ "$rc" -eq 2 ]] && pass "gitleaks error (exit 1) + secret -> regex fallback exit 2" || fail "error+secret should exit 2 (got $rc)"

# E2. A different error code (2) + clean -> also falls back, not blocked.
reset_index; stage_clean
run_hook "$BIN_GL" 2; rc=$?
[[ "$rc" -eq 0 ]] && pass "gitleaks exit 2 (error) + clean -> exit 0 (no phantom block)" || fail "exit-2 error+clean should exit 0 (got $rc)"

# G. betterleaks present -> its finding (exit 7) hard-blocks, and the hook called
#    BETTERLEAKS (not gitleaks). Proves the new scanner is actually wired.
reset_index; stage_clean; : > "$ARGS_FILE"
run_hook "$BIN_BL" 0 7; rc=$?   # gitleaks_rc=0, betterleaks_rc=7
[[ "$rc" -eq 2 ]] && pass "betterleaks finding (exit 7) -> exit 2" || fail "betterleaks finding should exit 2 (got $rc)"
grep -q 'betterleaks stdin' "$ARGS_FILE" \
  && pass "hook invoked betterleaks (not gitleaks)" \
  || fail "hook should have called betterleaks (args: $(cat "$ARGS_FILE"))"

# H. PRECEDENCE: with BOTH installed, betterleaks wins. betterleaks=clean(0),
#    gitleaks=would-block(7) -> result 0 proves gitleaks was never consulted.
reset_index; stage_clean
run_hook "$BIN_BL" 7 0; rc=$?   # gitleaks_rc=7 (ignored), betterleaks_rc=0
[[ "$rc" -eq 0 ]] && pass "betterleaks takes precedence over gitleaks" || fail "betterleaks should win over gitleaks (got $rc)"

# F. Non-commit command exits 0 early (no scan).
reset_index; stage_secret
rc=0; ( cd "$REPO" && echo '{"tool_input":{"command":"git status"}}' | PATH="$BIN_NO" bash "$HOOK" >/dev/null 2>&1 ) || rc=$?
[[ "$rc" -eq 0 ]] && pass "non-commit command exits 0 early" || fail "non-commit should exit 0 (got $rc)"

# --- Summary -----------------------------------------------------------------
echo "---"
if [[ "$FAILS" -eq 0 ]]; then
  echo "All assertions passed."
  exit 0
else
  echo "$FAILS assertion(s) failed."
  exit 1
fi
