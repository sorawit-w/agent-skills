# Hooks — Automated Enforcement

Hooks are shell commands or LLM prompts that run automatically at specific lifecycle points. They provide **deterministic enforcement** of playbook rules — the agent can't skip them.

> **Note:** Hooks are currently supported by Claude Code. Other agents will ignore the hooks configuration in frontmatter but should still follow the playbook's written instructions.

---

## Active Hooks

coding-rules ships with these hooks:

### SessionStart → Context Injection

**Script:** `hooks/session-start-context.sh`
**Strictness:** Informational (no blocking)

Runs at the start of every session. Injects:
- Reminder of the 9-step workflow
- Contents of `.ai/STATUS.md` (if it exists) — so the agent knows where the previous session left off
- Last entries from `.ai/memory.log` (if it exists) — recent decisions and context

This replaces the need for the agent to "remember" to read project state — it's surfaced automatically.

---

### SessionStart → Knowledge Bootstrap

**Script:** `hooks/knowledge-bootstrap.sh`
**Strictness:** Informational (no blocking)

Runs at the start of every session. Three jobs:

1. **Scaffold** `.ai/knowledge/KNOWLEDGE.md` from `templates/KNOWLEDGE.md.template` if the directory is missing. One-time, idempotent.
2. **Reindex** the AUTO-INDEX block in `KNOWLEDGE.md` from the title (frontmatter) and first body line of each entry file. Idempotent — only writes if content actually changed. Internally calls `knowledge-reindex.sh --force`.
3. **Stale scan** — scans entry files for `updated:` (or `created:` as fallback) and prints any older than 180 days, so the agent can flag them rather than treating them as authoritative.

Why reindex on session start instead of post-commit? `KNOWLEDGE.md` is read by agents at the start of each session — that's the only moment freshness matters. Aligning regen with the read avoids per-project git-hook installation entirely. (For the case where the agent writes a new entry mid-session, see "Mid-session updates" below.)

Opt-out per project via `agent-context.yaml`:

```yaml
knowledge:
  enabled: false
```

Defaults to enabled when the section is missing. Override the staleness window with `CODING_RULES_KNOWLEDGE_STALE_DAYS=90`.

The `KNOWLEDGE.md` written by this hook contains `<!-- AUTO-INDEX:START -->` / `<!-- AUTO-INDEX:END -->` markers — only the lines between those markers are rewritten. Custom intro text or extra sections elsewhere in the file are preserved. If markers are missing, the hook prints a warning and skips index regen.

**Mid-session updates.** When an agent writes a new knowledge entry during a session (after the proposal-then-approval flow in `references/knowledge-management.md`), it should run `bash "${CODING_RULES_DIR}/resources/hooks/knowledge-reindex.sh" --force` to refresh the index immediately rather than waiting for the next session. The script is safe to call ad-hoc — idempotent and side-effect-free if nothing changed.

---

### SessionStart → Context Bootstrap

**Script:** `hooks/context-bootstrap.sh`
**Strictness:** Informational (no blocking)

Runs at the start of every session. If `CONTEXT.md` is missing at project root, scaffolds it from `templates/CONTEXT.md.template`. Never overwrites an existing `CONTEXT.md` — human-curated content is treated as authoritative.

`CONTEXT.md` is the project's enduring domain glossary (see `references/domain-glossary.md`). It's read at session start as part of BOOTSTRAP step 2 and used in code, plans, and prose to keep terminology consistent.

Opt-out per project via `agent-context.yaml`:

```yaml
context:
  enabled: false
```

Defaults to enabled when the section is missing.

---

### PreToolUse → .env File Protection

**Script:** `hooks/protect-env.sh`
**Strictness:** Hard-block (exit 2)
**Matcher:** `Edit|Write` targeting `.env` files

Prevents the agent from editing `.env` files directly. This is a security guardrail — secrets should never be modified by an agent. If the agent needs environment variables set, it should document them in `DEVELOPER_TODO.md` instead.

---

### PreToolUse → .env Read Warning

**Script:** `hooks/warn-env-read.sh`
**Strictness:** Soft-warn (exit 0 with stderr note) — disablable
**Matcher:** `Read` targeting `.env` files

The behavioral counterpart to `protect-env`. Reading a `.env` is legitimate (the agent often needs the variable *names* to wire things up), so this never blocks — it only reminds the agent not to print secret *values* into the conversation. Disablable via `CODING_RULES_HOOK_DISABLED=warn-env-read`.

**Coverage gap (by design, not a bug):** the Claude Code matcher fires on the `Read` tool only. An agent reading a `.env` via Bash (`cat .env`, `grep KEY .env`) is invisible to this hook — that path stays a [behavioral] rule (`guardrails.md`: "never print a live secret"). See `references/threat-model.md` for why the in-context boundary can't be hook-enforced. Self-tested by `hooks/warn-env-read.test.sh`.

---

### PreToolUse → Pre-Commit Check

**Script:** `hooks/pre-commit-check.sh`
**Strictness:** Soft-warn (exit 0 with context) + Hard-block on secrets (exit 2)
**Matcher:** `Bash` running `git commit`

Two checks before every commit:
1. **Secret scan (hard-block)** — Capability-gated on the binary: prefers `betterleaks`, then `gitleaks`, if either is on `PATH` (broader coverage, respects the scanner's repo-local allowlist), scanning the staged *added* lines via the version-stable `stdin` mode (`git diff --cached -U0 | <scanner> stdin --exit-code 7`). Falls back to a built-in regex (`sk_live_`, `AKIA`, private keys, hardcoded passwords) when no scanner is present or it errors. A *finding* (distinct exit code 7) blocks the commit; a *tool error* (any other nonzero — their default exit 1 means "leaks OR error") falls through to the regex rather than phantom-blocking. Cannot be disabled via env var. Self-tested by `hooks/pre-commit-check.test.sh`. *(betterleaks is the gitleaks author's feature-frozen-gitleaks successor; the `stdin` invocation is what survives gitleaks' 8.19 reorg that deprecated `protect`.)*
2. **Quality gate reminder (soft-warn)** — Injects a reminder to run lint/test on changed files. Does NOT hard-block — this avoids trapping the agent on pre-existing lint errors from other developers.

---

### git post-commit → Knowledge Reindex (Optional)

**Script:** `hooks/knowledge-reindex.sh`
**Strictness:** Informational (no blocking)
**Trigger:** git's native `post-commit` hook (not Claude Code lifecycle)

**This hook is optional.** The SessionStart bootstrap above already keeps `KNOWLEDGE.md` fresh at the only moment it matters (session start). Wire post-commit only if you want index updates to land in the same commit as the entry changes that triggered them — useful for cleaner git history or shared-team conventions, unnecessary for solo workflows.

The script has two modes:

- **Default (no args)** — git-gated. Only regenerates if the just-made commit touched a `.ai/knowledge/*.md` file other than `KNOWLEDGE.md`. Requires being in a git work tree. This is what the post-commit hook below uses.
- **`--force`** — Always regenerates, no git checks. This is what `knowledge-bootstrap.sh` calls internally, and what the agent should call after writing a new entry mid-session.

Either way:

- **Initial commits work.** Uses `git diff-tree --root` so the very first commit triggers an index build.
- **Idempotent.** If regeneration produces no actual change, the file isn't touched (keeps `git status` clean).
- **The regenerated `KNOWLEDGE.md` is left UNSTAGED.** Auto-amending the commit was deliberately rejected — it would mutate history under your feet.
- **Marker-safe.** If `<!-- AUTO-INDEX:START -->` / `<!-- AUTO-INDEX:END -->` markers are missing, the script prints a one-line warning and exits without touching the file.
- **Same opt-out** as `knowledge-bootstrap` — `agent-context.yaml: knowledge.enabled: false` skips it.

To wire it as a per-project post-commit hook (one-paste, from the project's git root):

```bash
mkdir -p .git/hooks
cat > .git/hooks/post-commit <<EOF
#!/bin/bash
# Wired by coding-rules. Add other post-commit logic above or below.
"\${CODING_RULES_DIR:-\$HOME/dev/coding-rules}/resources/hooks/knowledge-reindex.sh"
EOF
chmod +x .git/hooks/post-commit
```

If your project already has a `post-commit` hook, append the script call to it instead of overwriting.

---

### Manual / git post-commit → Knowledge Integrity (Optional)

**Script:** `hooks/knowledge-lint.sh`
**Strictness:** Advisory (exit 0; `--strict` exits non-zero)
**Trigger:** Manual invocation, or git's native `post-commit` hook (not Claude Code lifecycle)

Two zero-dependency mechanical checks over `.ai/knowledge/` entries:

1. **Broken `related:` target** — an entry's `related:` frontmatter names a file that isn't in `.ai/knowledge/`. Fires only when a link is declared, so effectively no false positives.
2. **Supersede-without-pointer** — an entry has a `## Superseded` section whose body names no replacement entry (no `.md` token).

**Advisory by default** — prints findings, always exits 0. Pass `--strict` to exit 1 on any finding (for a git pre-push or CI gate). Deliberately **not** a SessionStart hook: integrity drifts slowly and shouldn't be re-checked every session. There is **no orphan check** — `related:` is optional, so "no inbound link" is a curation opinion, not a correctness error; that's [OpenKB](external-resources.md)'s semantic-lint job, not this floor's.

Same opt-out as the other knowledge hooks — `agent-context.yaml: knowledge.enabled: false`, or `CODING_RULES_HOOK_DISABLED=knowledge-lint`. Run it directly any time (`bash "${CODING_RULES_DIR}/resources/hooks/knowledge-lint.sh"`), or append the call to a project `post-commit` hook the same way as `knowledge-reindex.sh` above. Self-tested by `hooks/knowledge-lint.test.sh`.

---

### Stop → Quality Gate Verification

**Type:** Prompt hook (LLM evaluation)
**Strictness:** Soft-verify

When the agent finishes responding, a prompt hook checks whether quality gates (build, lint, test) were run during the turn. If the agent made code changes but skipped quality gates, it's flagged. This is advisory — it doesn't prevent the agent from stopping, but surfaces the gap.

---

### SessionEnd → Checkpoint Verification

**Type:** Prompt hook (LLM evaluation)
**Strictness:** Soft-verify

When the session ends, a prompt hook verifies that:
1. All code is committed (no uncommitted changes)
2. `.ai/STATUS.md` or `.ai/memory.log` was updated during the session

If the checkpoint is missing, the agent is reminded. This is advisory — it flags the gap but doesn't prevent session exit.

---

## Customizing Hooks

### Runtime Toggles (env vars)

Non-security hooks respect a single env var for ad-hoc disabling during a session:

```bash
# Disable one hook
CODING_RULES_HOOK_DISABLED=session-start-context

# Disable several (comma-separated, no spaces)
CODING_RULES_HOOK_DISABLED=session-start-context,pre-commit-check
```

Hook names match the `# Name:` header in each script. Current names:

| Name | Disablable? |
|------|-------------|
| `session-start-context` | Yes |
| `knowledge-bootstrap` | Yes (or per-project: `agent-context.yaml: knowledge.enabled: false`) |
| `knowledge-reindex` | Yes (same per-project opt-out as `knowledge-bootstrap`) |
| `knowledge-lint` | Yes (same per-project opt-out as `knowledge-bootstrap`) |
| `pre-commit-check` | Yes (disables soft reminder only — secret scan always runs) |
| `warn-env-read` | Yes (soft `.env`-read reminder) |
| `protect-env` | No — security-critical, edit `.claude/settings.json` to remove |
| `protect-git` | No — data-loss-critical, edit `.claude/settings.json` to remove |

**Rule:** security-critical hooks cannot be disabled via env var. This is intentional. An env var is too easy to set accidentally (shell rc, CI config, `.envrc`) for a rule that blocks secret leaks. To bypass, make a deliberate config edit.

`CODING_RULES_HOOK_PROFILE` is reserved for future use (named presets like `minimal` / `strict`). Not wired yet — use the disable list.

### Disabling Hooks (permanent)

If a hook is causing issues in your project, you can:
- Remove or modify the hooks in the skill's frontmatter
- Override with project-level settings in `.claude/settings.json`

### Adding Your Own Hooks

You can extend coding-rules' hooks by adding to your project's `.claude/settings.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "if": "Bash(rm -rf*)",
        "hooks": [
          {
            "type": "command",
            "command": "echo 'BLOCKED: Destructive command detected.' >&2 && exit 2"
          }
        ]
      }
    ]
  }
}
```

### Hook Strictness Levels

| Exit Code | Behavior | Use For |
|-----------|----------|---------|
| `0` | Success — stdout injected as context | Reminders, soft warnings |
| `2` | Blocking error — action prevented, stderr shown | Security violations, hard rules |
| Other | Non-blocking error — logged, action proceeds | Diagnostics, optional checks |

---

## How Hooks Map to the Playbook

| Playbook Rule | Enforcement Without Hooks | Enforcement With Hooks |
|--------------|--------------------------|----------------------|
| Read project state first | Agent must remember | SessionStart injects state automatically |
| Bootstrap `.ai/knowledge/` on first use | Agent must remember (often forgets) | SessionStart scaffolds + flags stale entries |
| Keep `KNOWLEDGE.md` index in sync with entries | Agent must remember on every entry change | SessionStart reindexes; agent calls `knowledge-reindex.sh --force` for mid-session updates |
| Never commit secrets | Agent must self-check | Hard-blocked before commit happens |
| Never edit .env files | Agent must self-check | Hard-blocked before edit happens |
| Run quality gates | Agent must remember | Soft-verified when agent stops |
| Create checkpoints | Agent must remember | Soft-verified at session end |

Hooks turn "the agent should do X" into "X happens automatically." The playbook's written instructions remain the source of truth — hooks enforce the most critical rules deterministically.
