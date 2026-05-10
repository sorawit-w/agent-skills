# Multi-Tool Support

coding-rules is a playbook. The hook scripts happen to target Claude Code, but the *rules themselves* — the prime directive, hard rules, workflows, and references — are vendor-independent and should work wherever an AI coding agent reads a project context file.

This document defines how to expose the playbook to multiple agent runtimes without duplicating content.

---

## Vendor-Independent Default

The canonical context file is **`AI-CONTEXT.md`** at the project root.

- Any agent that doesn't know about vendor-specific names can be pointed at `AI-CONTEXT.md`
- It is a symlink (or a thin pointer file) to `coding-rules/BOOTSTRAP.md` or your project's `CLAUDE.md`
- Prefer a symlink — keeps one source of truth

```bash
# At project root
ln -s coding-rules/BOOTSTRAP.md AI-CONTEXT.md
```

If your platform doesn't handle symlinks cleanly (Windows, some CI), use a one-line pointer file:

```markdown
# AI Context

See `coding-rules/BOOTSTRAP.md` for the operating rules.
```

---

## Vendor-Specific Files

When a runtime expects a specific filename, add a symlink. The rule: **only two supported vendors** — Claude Code and Codex. Other tools fall back to `AI-CONTEXT.md`.

| Runtime | Expected file | How to wire |
|---------|---------------|-------------|
| Claude Code | `CLAUDE.md` | `ln -s coding-rules/BOOTSTRAP.md CLAUDE.md` |
| Codex (OpenAI) | `AGENTS.md` | `ln -s coding-rules/BOOTSTRAP.md AGENTS.md` |
| Other agents | `AI-CONTEXT.md` | Same symlink — the fallback |

**Why only these two:** the maintenance cost of vendor-specific tweaks is non-zero. Supporting N vendors means N matrices to keep synchronized and eval. Claude Code + Codex is the smallest set that covers the current team's daily use.

Cursor, OpenCode, and others are not explicitly supported, but will still read `AI-CONTEXT.md` or `CLAUDE.md` if configured to do so. The rules apply; the delivery is best-effort.

---

## Hook Behavior Across Runtimes

Hooks are shell scripts triggered by Claude Code's lifecycle events (`SessionStart`, `PreToolUse`, etc.). They are currently **Claude Code only** in terms of automatic invocation.

Consequences for other runtimes:

- **Codex** does not invoke `hooks/*.sh` automatically. The rules in `BOOTSTRAP.md` and `references/*.md` still apply — the agent is expected to follow them manually.
- **Cursor** likewise. `.cursorrules` can be a symlink to `BOOTSTRAP.md` if you want Cursor's rule-injection to see the playbook.
- The text rules are the source of truth. Hooks are *enforcement scaffolding*, not the rules themselves.

If you need a hook-equivalent in Codex, write it as a shell command in Codex's configuration and have it invoke the same script in `coding-rules/hooks/`. The scripts are plain bash and don't depend on Claude Code internals beyond the JSON input format (which you can mock for Codex via a thin wrapper).

---

## Keeping Multiple Context Files in Sync

The symlink approach makes this automatic. If you chose pointer files instead (e.g., for Windows), add a check to your CI or a pre-commit hook that compares SHAs:

```bash
# In a repo hook or CI step
canonical=$(sha256sum coding-rules/BOOTSTRAP.md | cut -d' ' -f1)
for f in CLAUDE.md AGENTS.md AI-CONTEXT.md; do
  [[ -f "$f" ]] || continue
  if ! grep -q "$canonical" "$f" 2>/dev/null; then
    echo "Drift: $f does not reference the canonical BOOTSTRAP.md SHA"
  fi
done
```

This is advisory. The symlink path avoids it entirely.

---

## Why This Shape

An earlier absorb-vs-switch review considered pulling in a larger framework (`everything-claude-code`) with full cross-tool adapter infrastructure. The decision was to borrow the *idea* of cross-tool parity — not the implementation — because:

- A symlink convention is auditable in minutes; an adapter layer is not
- The playbook's value is its rules, not its delivery mechanism
- Two supported vendors is the smallest set that covers the team; more than two demands a real eval matrix

Cross-tool behavior is a candidate eval surface for `skill-evaluator`: does the same rule produce the same agent behavior under Claude Code vs Codex? If not, that's a signal the rule is over-specified for one runtime.
