#!/bin/bash
# Self-test for knowledge-lint.sh — zero-framework, self-contained.
# Builds a temp fixture vault, runs the lint, asserts behavior, cleans up.
#
# Run from anywhere: bash knowledge-lint.test.sh
# Exit 0 = all assertions pass; non-zero = a failure (with FAIL line above).

set -u

SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
LINT="$SCRIPT_DIR/knowledge-lint.sh"

FAILS=0
pass() { echo "PASS: $1"; }
fail() { echo "FAIL: $1"; FAILS=$((FAILS + 1)); }

# --- Build fixture vault -----------------------------------------------------
TMP=$(mktemp -d)
trap 'rm -rf "$TMP"' EXIT
mkdir -p "$TMP/.ai/knowledge"
cd "$TMP" || { echo "FAIL: could not cd to temp dir"; exit 1; }

# Entry A: dangling related: target (points at a file that does not exist).
cat > .ai/knowledge/decision-broken.md <<'EOF'
---
title: Entry with a broken related link
type: decision
domain: [testing]
related: [context-does-not-exist.md]
confidence: high
created: 2026-01-01
---

## Decision
Points at a non-existent sibling.
EOF

# Entry B: ## Superseded section that names no replacement entry.
cat > .ai/knowledge/decision-bad-supersede.md <<'EOF'
---
title: Entry superseded with no pointer
type: decision
domain: [testing]
confidence: high
created: 2026-01-01
---

## Decision
Old approach.

## Superseded
This was reversed. We do it differently now.
EOF

# Entry C: clean — legitimately has NO related: field (the false-positive
# guard). An optional empty field must NEVER be flagged.
cat > .ai/knowledge/convention-clean.md <<'EOF'
---
title: Clean entry with no related field
type: convention
domain: [testing]
confidence: high
created: 2026-01-01
---

## Convention
Self-contained; references nothing.
EOF

# Entry D: a good supersede that DOES name a replacement (.md token present)
# — also must not be flagged.
cat > .ai/knowledge/decision-good-supersede.md <<'EOF'
---
title: Entry superseded with a proper pointer
type: decision
domain: [testing]
confidence: high
created: 2026-01-01
---

## Decision
Old approach.

## Superseded
Replaced by convention-clean.md after review.
EOF

# --- Assertions --------------------------------------------------------------
OUT=$(bash "$LINT"); RC=$?

# 1. Default mode exits 0 (advisory).
[[ "$RC" -eq 0 ]] && pass "default mode exits 0" || fail "default mode should exit 0 (got $RC)"

# 2. Broken-link finding present for entry A.
echo "$OUT" | grep -q "BROKEN-LINK: decision-broken.md" \
  && pass "reports broken related link" \
  || fail "missing BROKEN-LINK finding for decision-broken.md"

# 3. Supersede-no-pointer finding present for entry B.
echo "$OUT" | grep -q "SUPERSEDE-NO-POINTER: decision-bad-supersede.md" \
  && pass "reports supersede without pointer" \
  || fail "missing SUPERSEDE-NO-POINTER finding for decision-bad-supersede.md"

# 4. Clean no-related: entry is NEVER flagged (false-positive guard).
echo "$OUT" | grep -q "convention-clean.md" \
  && fail "clean no-related entry was flagged (false positive)" \
  || pass "clean no-related entry not flagged"

# 5. Good supersede (names a .md replacement) is NOT flagged.
echo "$OUT" | grep -q "decision-good-supersede.md" \
  && fail "good supersede entry was flagged (false positive)" \
  || pass "good supersede entry not flagged"

# 6. --strict exits 1 when findings exist.
bash "$LINT" --strict >/dev/null 2>&1; SRC=$?
[[ "$SRC" -eq 1 ]] && pass "--strict exits 1 on findings" || fail "--strict should exit 1 on findings (got $SRC)"

# 7. Clean vault: remove the two bad entries, expect silent exit 0 both modes.
rm .ai/knowledge/decision-broken.md .ai/knowledge/decision-bad-supersede.md
CLEAN_OUT=$(bash "$LINT"); CRC=$?
[[ "$CRC" -eq 0 && -z "$CLEAN_OUT" ]] \
  && pass "clean vault prints nothing, exits 0" \
  || fail "clean vault should be silent exit 0 (rc=$CRC, out='$CLEAN_OUT')"
bash "$LINT" --strict >/dev/null 2>&1; CSRC=$?
[[ "$CSRC" -eq 0 ]] && pass "--strict exits 0 on clean vault" || fail "--strict should exit 0 on clean vault (got $CSRC)"

# --- Summary -----------------------------------------------------------------
echo "---"
if [[ "$FAILS" -eq 0 ]]; then
  echo "All assertions passed."
  exit 0
else
  echo "$FAILS assertion(s) failed."
  exit 1
fi
