#!/bin/bash
# Hook: Bootstrap .ai/knowledge/ on session start; surface stale entries
# Type: SessionStart
# Name: knowledge-bootstrap
# Outputs context that Claude reads at the beginning of the session.
#
# Behavior:
# - If agent-context.yaml has `knowledge.enabled: false`, exits silently.
# - Otherwise, if `.ai/knowledge/` is missing, scaffolds the directory
#   from templates/KNOWLEDGE.md.template (resolved via $CODING_RULES_DIR
#   or repo-relative fallback).
# - Scans existing entries for staleness (default: > 180 days since
#   `updated:` or `created:`) and prints them so the agent can flag.
#
# Disable with: CODING_RULES_HOOK_DISABLED=knowledge-bootstrap
# Override staleness threshold: CODING_RULES_KNOWLEDGE_STALE_DAYS=90
# See references/hooks.md for the env-var convention.

set -u

# Respect the disable list.
case ",${CODING_RULES_HOOK_DISABLED:-}," in
  *,knowledge-bootstrap,*) exit 0 ;;
esac

# Opt-out check: knowledge.enabled: false in agent-context.yaml disables.
# Default is enabled (any other value, or missing config, treated as on).
if [[ -f "agent-context.yaml" ]]; then
  # Find the `knowledge:` block, then within it look for `enabled: false`.
  # Tolerates indentation and surrounding whitespace.
  if awk '
    /^knowledge:[[:space:]]*$/ { in_block=1; next }
    in_block && /^[^[:space:]]/ { in_block=0 }
    in_block && /^[[:space:]]+enabled:[[:space:]]*false[[:space:]]*$/ { found=1 }
    END { exit found ? 0 : 1 }
  ' agent-context.yaml; then
    exit 0
  fi
fi

# Resolve sibling paths. Prefer $CODING_RULES_DIR; fall back to script-relative.
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
TEMPLATE=""
REINDEX=""
if [[ -n "${CODING_RULES_DIR:-}" && -f "$CODING_RULES_DIR/resources/templates/KNOWLEDGE.md.template" ]]; then
  TEMPLATE="$CODING_RULES_DIR/resources/templates/KNOWLEDGE.md.template"
elif [[ -f "$SCRIPT_DIR/../templates/KNOWLEDGE.md.template" ]]; then
  TEMPLATE="$SCRIPT_DIR/../templates/KNOWLEDGE.md.template"
fi
if [[ -n "${CODING_RULES_DIR:-}" && -x "$CODING_RULES_DIR/resources/hooks/knowledge-reindex.sh" ]]; then
  REINDEX="$CODING_RULES_DIR/resources/hooks/knowledge-reindex.sh"
elif [[ -x "$SCRIPT_DIR/knowledge-reindex.sh" ]]; then
  REINDEX="$SCRIPT_DIR/knowledge-reindex.sh"
fi

# Scaffold .ai/knowledge/ if missing.
if [[ ! -d ".ai/knowledge" ]]; then
  mkdir -p ".ai/knowledge"
  if [[ -n "$TEMPLATE" ]]; then
    cp "$TEMPLATE" ".ai/knowledge/KNOWLEDGE.md"
    echo "=== Knowledge Base Bootstrapped ==="
    echo "Created .ai/knowledge/KNOWLEDGE.md from template."
    echo "Add entries as <type>-<short-description>.md alongside the index."
    echo ""
  else
    # Template not found — write a minimal index so the dir isn't empty.
    cat > ".ai/knowledge/KNOWLEDGE.md" <<'EOF'
# Knowledge Base Index

Project knowledge — decisions, context, conventions, lessons.

## Entries

<!-- AUTO-INDEX:START -->
<!-- AUTO-INDEX:END -->
EOF
    echo "=== Knowledge Base Bootstrapped ==="
    echo "Created .ai/knowledge/KNOWLEDGE.md (template not found; minimal stub used)."
    echo ""
  fi
fi

# Reindex KNOWLEDGE.md from current entry files. Idempotent — only writes
# if content actually changed. Failure here must NOT break session start,
# so any non-zero exit is swallowed.
if [[ -n "$REINDEX" && -d ".ai/knowledge" ]]; then
  "$REINDEX" --force || true
fi

# Staleness scan — only for entry files (NOT KNOWLEDGE.md).
STALE_DAYS="${CODING_RULES_KNOWLEDGE_STALE_DAYS:-180}"
if [[ ! "$STALE_DAYS" =~ ^[0-9]+$ ]]; then
  STALE_DAYS=180
fi

# Compute threshold date (portable: try BSD `date -v` first, fall back to GNU).
THRESHOLD=""
if THRESHOLD=$(date -v-"${STALE_DAYS}"d +%Y-%m-%d 2>/dev/null); then
  :
elif THRESHOLD=$(date -d "${STALE_DAYS} days ago" +%Y-%m-%d 2>/dev/null); then
  :
else
  THRESHOLD=""  # neither flavor of `date` worked — skip staleness check
fi

if [[ -n "$THRESHOLD" && -d ".ai/knowledge" ]]; then
  STALE_LIST=""
  shopt -s nullglob
  for f in .ai/knowledge/*.md; do
    base=$(basename "$f")
    [[ "$base" == "KNOWLEDGE.md" ]] && continue

    # Pull `updated:` if present, else `created:`. Frontmatter only (between first --- and second ---).
    DATE_STR=$(awk '
      /^---[[:space:]]*$/ { fm++; next }
      fm == 1 {
        if (match($0, /^updated:[[:space:]]*/)) { sub(/^updated:[[:space:]]*/, ""); upd=$0 }
        else if (match($0, /^created:[[:space:]]*/)) { sub(/^created:[[:space:]]*/, ""); cre=$0 }
      }
      fm >= 2 { exit }
      END { print (upd != "" ? upd : cre) }
    ' "$f")

    # Strip whitespace and quotes.
    DATE_STR="${DATE_STR//\"/}"
    DATE_STR="${DATE_STR//\'/}"
    DATE_STR=$(echo "$DATE_STR" | tr -d '[:space:]')

    [[ -z "$DATE_STR" ]] && continue
    # Compare lexically — works for ISO 8601 YYYY-MM-DD.
    if [[ "$DATE_STR" < "$THRESHOLD" ]]; then
      STALE_LIST+="  - $base (last touched $DATE_STR)"$'\n'
    fi
  done
  shopt -u nullglob

  if [[ -n "$STALE_LIST" ]]; then
    echo "=== Stale Knowledge Entries (older than ${STALE_DAYS} days) ==="
    printf "%s" "$STALE_LIST"
    echo "Review for accuracy before relying on these. Update or mark superseded."
    echo ""
  fi
fi

exit 0
