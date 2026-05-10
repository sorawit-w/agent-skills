#!/bin/bash
# Hook: Regenerate .ai/knowledge/KNOWLEDGE.md AUTO-INDEX block
# Name: knowledge-reindex
#
# Two trigger modes:
#   (default) — git post-commit: only regen if the just-made commit
#               touched a .ai/knowledge/*.md file (excluding KNOWLEDGE.md).
#               Requires being inside a git work tree.
#   --force   — Always regen, no git checks. Used by knowledge-bootstrap.sh
#               on session start, and safe for the agent to call directly
#               after writing a new entry.
#
# The default (post-commit) mode is OPTIONAL — knowledge-bootstrap.sh
# (SessionStart) already calls this script with --force, so a per-project
# post-commit hook is only needed if you want index changes to land in the
# same commit as entry changes (cleaner git history). See references/hooks.md.
#
# Behavior either way:
# - The regenerated KNOWLEDGE.md is left UNSTAGED. Review and commit
#   when convenient. (Auto-amending the just-made commit would mutate
#   git history under your feet — explicitly avoided.)
# - Only the block between AUTO-INDEX:START and AUTO-INDEX:END is
#   rewritten. Everything else in KNOWLEDGE.md is preserved. If those
#   markers are missing, the script prints a warning and exits without
#   touching the file.
#
# Disable with: CODING_RULES_HOOK_DISABLED=knowledge-reindex

set -u

FORCE=0
if [[ "${1:-}" == "--force" ]]; then
  FORCE=1
fi

case ",${CODING_RULES_HOOK_DISABLED:-}," in
  *,knowledge-reindex,*) exit 0 ;;
esac

# Opt-out check (same shape as knowledge-bootstrap.sh).
if [[ -f "agent-context.yaml" ]]; then
  if awk '
    /^knowledge:[[:space:]]*$/ { in_block=1; next }
    in_block && /^[^[:space:]]/ { in_block=0 }
    in_block && /^[[:space:]]+enabled:[[:space:]]*false[[:space:]]*$/ { found=1 }
    END { exit found ? 0 : 1 }
  ' agent-context.yaml; then
    exit 0
  fi
fi

if [[ "$FORCE" == "0" ]]; then
  # Default mode: only fire on a relevant commit.
  if ! git rev-parse --git-dir >/dev/null 2>&1; then
    exit 0
  fi

  # What changed in the just-made commit, scoped to entry files.
  # --root makes the initial commit (no parent) diff against the empty tree
  # instead of returning nothing.
  CHANGED=$(git diff-tree --no-commit-id --name-only -r --root HEAD -- .ai/knowledge 2>/dev/null \
    | grep -v '^\.ai/knowledge/KNOWLEDGE\.md$' || true)

  if [[ -z "$CHANGED" ]]; then
    exit 0
  fi
fi

INDEX=".ai/knowledge/KNOWLEDGE.md"
if [[ ! -f "$INDEX" ]]; then
  echo "knowledge-reindex: $INDEX missing; skipping." >&2
  exit 0
fi

if ! grep -q 'AUTO-INDEX:START' "$INDEX" || ! grep -q 'AUTO-INDEX:END' "$INDEX"; then
  echo "knowledge-reindex: AUTO-INDEX markers not found in $INDEX." >&2
  echo "  Add <!-- AUTO-INDEX:START --> and <!-- AUTO-INDEX:END --> markers" >&2
  echo "  to enable index regeneration. Skipping for now." >&2
  exit 0
fi

# Build the new index block.
TMP_BLOCK=$(mktemp)
shopt -s nullglob
for f in .ai/knowledge/*.md; do
  base=$(basename "$f")
  [[ "$base" == "KNOWLEDGE.md" ]] && continue

  # Extract title from frontmatter; fall back to filename stem.
  TITLE=$(awk '
    /^---[[:space:]]*$/ { fm++; next }
    fm == 1 && /^title:[[:space:]]*/ {
      sub(/^title:[[:space:]]*/, "")
      gsub(/^["\047]|["\047]$/, "")
      print
      exit
    }
    fm >= 2 { exit }
  ' "$f")
  if [[ -z "$TITLE" ]]; then
    TITLE="${base%.md}"
  fi

  # First non-blank, non-heading line of the body becomes the hook.
  # Files with no frontmatter (fm stays 0) still get scanned from the top.
  HOOK=$(awk '
    BEGIN { fm=0; saw_fm=0 }
    /^---[[:space:]]*$/ { fm++; saw_fm=1; next }
    saw_fm && fm < 2 { next }    # inside frontmatter, skip
    /^[[:space:]]*$/ { next }
    /^#/ { next }
    { print; exit }
  ' "$f")
  HOOK=$(echo "$HOOK" | tr -s '[:space:]' ' ' | sed 's/^ //;s/ $//')
  # Truncate the line so the index entry stays under ~120 chars.
  if [[ ${#HOOK} -gt 90 ]]; then
    HOOK="${HOOK:0:87}..."
  fi

  if [[ -n "$HOOK" ]]; then
    echo "- [$TITLE]($base) — $HOOK" >> "$TMP_BLOCK"
  else
    echo "- [$TITLE]($base)" >> "$TMP_BLOCK"
  fi
done
shopt -u nullglob

# Sort entries alphabetically by title for stable ordering (case-fold).
sort -f -o "$TMP_BLOCK" "$TMP_BLOCK"

# Splice the new block in between the markers.
TMP_OUT=$(mktemp)
awk -v block_file="$TMP_BLOCK" '
  /AUTO-INDEX:START/ {
    print
    while ((getline line < block_file) > 0) print line
    close(block_file)
    in_block=1
    next
  }
  /AUTO-INDEX:END/ { in_block=0 }
  !in_block { print }
' "$INDEX" > "$TMP_OUT"

# Only overwrite if the content actually changed (keeps git status clean).
if ! cmp -s "$TMP_OUT" "$INDEX"; then
  mv "$TMP_OUT" "$INDEX"
  echo "knowledge-reindex: regenerated $INDEX (now unstaged; commit when ready)."
else
  rm -f "$TMP_OUT"
fi

rm -f "$TMP_BLOCK"
exit 0
