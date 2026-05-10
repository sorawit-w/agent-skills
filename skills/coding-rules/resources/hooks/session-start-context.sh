#!/bin/bash
# Hook: Inject project state context at session start
# Type: SessionStart
# Name: session-start-context
# Outputs context that Claude reads at the beginning of the session
#
# Disable with: CODING_RULES_HOOK_DISABLED=session-start-context
# See references/hooks.md for the env-var convention.

# Respect the disable list (non-security hooks only).
case ",${CODING_RULES_HOOK_DISABLED:-}," in
  *,session-start-context,*) exit 0 ;;
esac

# Check for project state files and surface them
echo "=== AI Playbook Active ==="
echo "Follow the 9-step workflow: ASSESS → CLARIFY → PLAN → IMPLEMENT → DELEGATE → VALIDATE → LOG → CHECKPOINT → STOP"
echo ""

if [[ -f ".ai/STATUS.md" ]]; then
  echo "=== Previous Session State (.ai/STATUS.md) ==="
  head -30 .ai/STATUS.md
  echo ""
  echo "[Read full STATUS.md for complete context]"
else
  echo "No .ai/STATUS.md found — this may be a fresh project or first session."
fi

echo ""

if [[ -f ".ai/memory.log" ]]; then
  echo "=== Recent Memory Log (last 10 entries) ==="
  tail -20 .ai/memory.log
else
  echo "No .ai/memory.log found."
fi

exit 0
