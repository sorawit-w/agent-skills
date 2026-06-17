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

# --- Controlled PATHs: one without gitleaks, one with a stub gitleaks ---------
BIN_NO="$TMP/bin_no"      # tools only, NO gitleaks (forces regex fallback)
BIN_GL="$TMP/bin_gl"      # tools + stub gitleaks (exit code via GITLEAKS_STUB_RC)
mkdir -p "$BIN_NO" "$BIN_GL"
for t in bash git jq grep sed cat head tail env; do
  real="$(command -v "$t")" && ln -s "$real" "$BIN_NO/$t" && ln -s "$real" "$BIN_GL/$t"
done
cat > "$BIN_GL/gitleaks" <<'EOF'
#!/bin/bash
exit "${GITLEAKS_STUB_RC:-0}"
EOF
chmod +x "$BIN_GL/gitleaks"

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

run_hook() { # $1=PATH $2=stub_rc(optional)
  ( cd "$REPO" && echo "$COMMIT_INPUT" | PATH="$1" GITLEAKS_STUB_RC="${2:-0}" bash "$HOOK" >/dev/null 2>&1 )
}

# --- Assertions --------------------------------------------------------------

# A. gitleaks reports a finding (rc 1) -> hard-block (exit 2), regardless of content.
reset_index; stage_clean
run_hook "$BIN_GL" 1; rc=$?
[[ "$rc" -eq 2 ]] && pass "gitleaks finding -> exit 2" || fail "gitleaks finding should exit 2 (got $rc)"

# B. gitleaks clean (rc 0) is TRUSTED -> regex skipped even with a secret staged -> exit 0.
reset_index; stage_secret
run_hook "$BIN_GL" 0; rc=$?
[[ "$rc" -eq 0 ]] && pass "gitleaks clean trusted, skips regex -> exit 0" || fail "gitleaks clean should exit 0 (got $rc)"

# C. gitleaks ABSENT + staged secret -> regex fallback hard-blocks (exit 2).
reset_index; stage_secret
run_hook "$BIN_NO"; rc=$?
[[ "$rc" -eq 2 ]] && pass "no gitleaks + secret -> regex fallback exit 2" || fail "regex fallback should exit 2 (got $rc)"

# D. gitleaks ERROR (rc 2) + clean staged -> fall back to regex -> NOT phantom-blocked.
reset_index; stage_clean
run_hook "$BIN_GL" 2; rc=$?
[[ "$rc" -eq 0 ]] && pass "gitleaks tool-error + clean -> exit 0 (no phantom block)" || fail "tool-error+clean should exit 0 (got $rc)"

# E. gitleaks ERROR (rc 2) + staged secret -> fall back to regex -> exit 2.
reset_index; stage_secret
run_hook "$BIN_GL" 2; rc=$?
[[ "$rc" -eq 2 ]] && pass "gitleaks tool-error + secret -> regex fallback exit 2" || fail "tool-error+secret should exit 2 (got $rc)"

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
