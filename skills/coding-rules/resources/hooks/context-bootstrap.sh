#!/bin/bash
# Hook: Bootstrap CONTEXT.md at project root on session start
# Type: SessionStart
# Name: context-bootstrap
# Outputs context that Claude reads at the beginning of the session.
#
# Behavior:
# - If agent-context.yaml has `context.enabled: false`, exits silently.
# - Otherwise, if CONTEXT.md at project root is missing, scaffolds it
#   from templates/CONTEXT.md.template (resolved via $CODING_RULES_DIR
#   or repo-relative fallback).
# - Never overwrites an existing CONTEXT.md.
#
# Disable with: CODING_RULES_HOOK_DISABLED=context-bootstrap
# See references/hooks.md for the env-var convention.

set -u

# Respect the disable list.
case ",${CODING_RULES_HOOK_DISABLED:-}," in
  *,context-bootstrap,*) exit 0 ;;
esac

# Opt-out check: context.enabled: false in agent-context.yaml disables.
# Default is enabled (any other value, or missing config, treated as on).
if [[ -f "agent-context.yaml" ]]; then
  if awk '
    /^context:[[:space:]]*$/ { in_block=1; next }
    in_block && /^[^[:space:]]/ { in_block=0 }
    in_block && /^[[:space:]]+enabled:[[:space:]]*false[[:space:]]*$/ { found=1 }
    END { exit found ? 0 : 1 }
  ' agent-context.yaml; then
    exit 0
  fi
fi

# Already exists — nothing to do. Never overwrite human-curated content.
if [[ -f "CONTEXT.md" ]]; then
  exit 0
fi

# Resolve template path. Prefer $CODING_RULES_DIR; fall back to script-relative.
SCRIPT_DIR="$( cd "$( dirname "${BASH_SOURCE[0]}" )" >/dev/null 2>&1 && pwd )"
TEMPLATE=""
if [[ -n "${CODING_RULES_DIR:-}" && -f "$CODING_RULES_DIR/resources/templates/CONTEXT.md.template" ]]; then
  TEMPLATE="$CODING_RULES_DIR/resources/templates/CONTEXT.md.template"
elif [[ -f "$SCRIPT_DIR/../templates/CONTEXT.md.template" ]]; then
  TEMPLATE="$SCRIPT_DIR/../templates/CONTEXT.md.template"
fi

if [[ -n "$TEMPLATE" ]]; then
  cp "$TEMPLATE" "CONTEXT.md"
  echo "=== Domain Glossary Bootstrapped ==="
  echo "Created CONTEXT.md from template."
  echo "Add domain terms as you encounter them. See references/domain-glossary.md."
  echo ""
else
  # Template not found — write a minimal stub so the file exists.
  cat > "CONTEXT.md" <<'EOF'
# Project Context

> Domain glossary and shared language. Use these terms in code, commits, and prose.

## Glossary

<!-- Add entries here as you encounter domain jargon. -->
EOF
  echo "=== Domain Glossary Bootstrapped ==="
  echo "Created CONTEXT.md (template not found; minimal stub used)."
  echo ""
fi

exit 0
