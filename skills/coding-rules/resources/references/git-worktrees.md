# Git Worktrees — Isolated Parallel Branches

Worktrees enable physical isolation of branches within a single repository, eliminating branch-switching overhead and keeping the repo state clean across parallel work.

---

## When to Use

| Workflow | Use Worktree? | Reason |
|----------|---|---|
| Feature/bugfix with parallel sub-agents OR multi-session (>1 day) | Yes | Physical isolation pays off |
| Feature/bugfix, solo serial, single-session | No | Install tax + lost build cache outweigh benefit; use `git checkout -b` in-place |
| Quick single-file tasks (`quick-task.md`) | No | Context switch overhead not justified |
| Sub-agent delegation with parallel branches | Yes — shared coordinator worktree | Avoids context collisions |
| One-off edits on main | No | Checkout, edit, checkout out — no isolation needed |

See the "Worktree gate" in `BOOTSTRAP.md` for the 3-question check the agent must answer before creating one.

---

## Package Manager Detection

Worktree safety depends on whether the project duplicates dependencies per worktree or shares them globally.

| Lockfile | Manager | Worktree Safety |
|----------|---------|---|
| `bun.lockb` | Bun | worktree-default ✓ |
| `pnpm-lock.yaml` | pnpm | worktree-default ✓ |
| `.pnp.cjs` or `.pnp.js` | Yarn Berry PnP | worktree-default ✓ |
| `yarn.lock` (no `.pnp`) | Yarn 1.x | worktree-default ✓ |
| `deno.lock` | Deno | worktree-default ✓ |
| `pyproject.toml` | Python | worktree-default ✓ |
| `Cargo.toml` | Rust | worktree-default ✓ |
| `go.mod` | Go | worktree-default ✓ |
| `package-lock.json` | npm | Fall back silently (see note below) |
| (no lockfile) | (no install) | worktree-default ✓ |

**npm fallback note (silent):** When npm is detected, silently use in-place branch instead of worktree to avoid `node_modules` duplication. If `node_modules/ > 500MB` or `package.json` has `>50` direct dependencies, also fall back silently and note to user: "npm detected; using in-place branch to avoid node_modules duplication."

---

## Creation

Create a new worktree with a clean branch:

```bash
git worktree add .worktrees/<branch-name> -b <type>/<description>
```

Example:

```bash
git worktree add .worktrees/feature-auth -b feature/auth
```

Then install and verify:

```bash
cd .worktrees/feature-auth
{package_manager} install    # bun install, pnpm install, etc.
{build_command} && {test_command}
```

The final `build && test` is a baseline verification — confirms the repo is clean before you start work. Pre-existing failures here are not your responsibility.

---

## Editor Workflow

After creation and install, open the worktree in your editor. Recommended approaches (do not mandate):

- **VS Code:** `code .worktrees/<name>`
- **Cursor:** `cursor .worktrees/<name>`
- **JetBrains (IntelliJ, PyCharm, Rust Rover):** File → Open → `.worktrees/<name>`
- **Current editor:** Refresh file tree and navigate — no new window required

The worktree behaves like a normal git repo directory. Editor choice is user preference.

---

## Cleanup & Lifecycle

After work is complete:

| Outcome | Action |
|---------|--------|
| Merged locally | `git worktree remove .worktrees/<name>` |
| PR opened | Keep worktree until PR merged; then `git worktree remove .worktrees/<name>` |
| Preserve for later | Keep worktree, note reason/branch in `.ai/memory.log` |
| Explicit discard | `git worktree remove --force .worktrees/<name>` (requires intent) |

**Before discarding:** Verify with `git branch -v` that all work is pushed or committed to a safe location.

---

## Inspection & Status

List all active worktrees:

```bash
git worktree list
```

Output shows path, branch, commit SHA, and detach state. Use this to verify no stale or orphaned worktrees before concluding "repo is clean."

**Cross-worktree discipline:** `git status` in one worktree shows only that worktree's state. Always run `git worktree list` and spot-check each active worktree before concluding the repo is clean.

---

## Failure Modes & Recovery

| Issue | Recovery |
|-------|----------|
| "Worktree is locked" | `git worktree unlock .worktrees/<name>` |
| Directory deleted externally | `git worktree prune` (removes stale entries) |
| Branch already checked out in another worktree | Git prevents duplicate; use existing worktree instead |
| Orphaned worktree entries (`.git/worktrees/`) | `git worktree prune` cleans up dangling references |

---

## Migration from In-Place Branches

If you're already on a traditional in-place branch when adopting worktrees:

- Finish the current branch normally (via existing checkout)
- Apply worktrees only to new branches going forward
- Do not retroactively convert old branches — it adds complexity and risk

---

## Prerequisites

Before creating your first worktree:

1. Ensure `.worktrees/` is in `.gitignore`
2. If not present, add it and commit:

```bash
echo ".worktrees/" >> .gitignore
git add .gitignore
git commit -m "chore: add .worktrees to gitignore"
```

Run this once per repo — it blocks accidental commits of worktree metadata.

---

Worktree tactical patterns adapted from obra/superpowers (MIT).
