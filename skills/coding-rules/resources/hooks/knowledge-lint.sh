#!/bin/bash
# Hook: Lint .ai/knowledge/ for mechanical integrity drift
# Type: manual + optional git post-commit
# Name: knowledge-lint
#
# Two zero-dependency correctness checks over .ai/knowledge/ entries:
#   1. BROKEN-LINK     — a `related:` frontmatter target that names a file
#                        which does not exist in .ai/knowledge/.
#   2. SUPERSEDE-NO-POINTER — an entry with a `## Superseded` section whose
#                        body names no replacement entry (no `.md` token).
#
# These are pure mechanical checks — no LLM, no API key. They are the
# always-on integrity floor. The heavier semantic lint (contradiction,
# orphan, stale) is OpenKB's job; see references/external-resources.md.
# Kept separate from knowledge-reindex.sh on purpose — different failure
# mode (integrity vs indexing). Do not fold the two together.
#
# Behavior:
# - If agent-context.yaml has `knowledge.enabled: false`, exits silently.
# - If `.ai/knowledge/` is missing, prints nothing and exits 0.
# - Default (advisory): prints findings to stdout, always exits 0.
# - `--strict`: exits 1 if any finding, else 0.
#
# Disable with: CODING_RULES_HOOK_DISABLED=knowledge-lint
# See references/hooks.md for the env-var convention.

set -u

STRICT=0
if [[ "${1:-}" == "--strict" ]]; then
  STRICT=1
fi

# Respect the disable list.
case ",${CODING_RULES_HOOK_DISABLED:-}," in
  *,knowledge-lint,*) exit 0 ;;
esac

# Opt-out check: knowledge.enabled: false in agent-context.yaml disables.
# Default is enabled (any other value, or missing config, treated as on).
# Same shape as knowledge-bootstrap.sh / knowledge-reindex.sh.
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

# Nothing to lint if the vault doesn't exist yet.
[[ -d ".ai/knowledge" ]] || exit 0

FINDINGS=""

shopt -s nullglob
for f in .ai/knowledge/*.md; do
  base=$(basename "$f")
  [[ "$base" == "KNOWLEDGE.md" ]] && continue

  # --- Check 1: broken related: targets -----------------------------------
  # Capture the `related:` field from frontmatter (handles both inline
  # `related: [a.md, b.md]` and block-list forms), then pull out .md tokens.
  REL_BLOB=$(awk '
    /^---[[:space:]]*$/ { fm++; next }
    fm == 1 {
      if (in_rel) {
        if ($0 ~ /^[[:space:]]/) { print; next }   # continuation of block list
        else { in_rel = 0 }
      }
      if ($0 ~ /^related:/) { print; in_rel = 1; next }
    }
    fm >= 2 { exit }
  ' "$f")

  if [[ -n "$REL_BLOB" ]]; then
    # Filenames are recorded without path (schema: "filename only").
    while IFS= read -r target; do
      [[ -z "$target" ]] && continue
      if [[ ! -f ".ai/knowledge/$target" ]]; then
        FINDINGS+="BROKEN-LINK: $base → related: $target (no such entry)"$'\n'
      fi
    done < <(echo "$REL_BLOB" | grep -oE '[A-Za-z0-9._-]+\.md' | sort -u)
  fi

  # --- Check 2: supersede without pointer ----------------------------------
  # A `## Superseded` section must name the replacement entry (a .md token).
  SUPERSEDE=$(awk '
    /^##[[:space:]]+Superseded([[:space:]]|$)/ { insec = 1; found = 1; next }
    insec && /^##[[:space:]]/ { insec = 0 }
    insec { body = body $0 "\n" }
    END {
      if (!found) { print "NONE"; exit }
      if (body ~ /[A-Za-z0-9._-]+\.md/) print "OK"; else print "NOPOINTER"
    }
  ' "$f")

  if [[ "$SUPERSEDE" == "NOPOINTER" ]]; then
    FINDINGS+="SUPERSEDE-NO-POINTER: $base has ## Superseded but names no replacement entry"$'\n'
  fi
done
shopt -u nullglob

if [[ -n "$FINDINGS" ]]; then
  COUNT=$(printf "%s" "$FINDINGS" | grep -c .)
  echo "=== knowledge-lint: $COUNT integrity finding(s) in .ai/knowledge/ ==="
  printf "%s" "$FINDINGS"
  echo "Advisory — fix the broken links or name the replacement entry. Run with --strict to fail on findings."
  [[ "$STRICT" == "1" ]] && exit 1
fi

exit 0
