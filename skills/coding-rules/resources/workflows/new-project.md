# New Project Setup Workflow

You are setting up a new project from scratch. Follow these steps in order.

<pre_work>
## 1. Pre-Work

You MUST read these before starting:

1. Read `references/workflows.md` — project setup procedures
2. Read `references/communication.md` — commit format, logging, branch naming
3. Read `references/recommendations.md` — gap detection, tool suggestions
</pre_work>

<branch>
## 2. Create Working Branch

```bash
git checkout -b feature/initial-setup
```

Confirm you are on the branch:
```bash
git branch --show-current  # must NOT be main, master, dev, etc.
```
</branch>

<scaffold>
## 3. Scaffold

1. Fill `agent-context.yaml` at project root — project name, description, runtime, stack, entry points (this file is versioned and shared with teammates)
2. Create project structure based on requirements:
   - Infer platforms from the user's description (web, mobile, API, etc.)
   - Choose runtime and framework — ask user if ambiguous
   - Set up build tooling, linter, formatter
   - **Scaffold vendor-adapter structure** under the project source root: empty `ports/`, `adapters/`, and `composition.ts` (or stack-equivalent paths). Adapters are added when a vendor enters the project — see `references/vendor-adapters.md`.
3. Install dependencies
4. **Create `ROADMAP.md` at project root** from requirements. Group items by phase if multi-phase (`### Phase 1: MVP`, `### Phase 2`, etc.). See `references/roadmap.md` for shape and legends.
5. Verify the scaffold works:
   ```bash
   {build_command} && {lint_command}
   ```
6. Commit the scaffold:
   ```bash
   git add -A
   git commit -m "feat: initial project scaffold"
   ```
</scaffold>

<configure>
## 4. Configure

1. Create `.env.example` if environment variables are needed (never commit actual secrets)
2. Set up `.gitignore` appropriate for the stack
3. Configure testing framework
4. Set up CI if requested
5. Commit configuration:
   ```bash
   git add <specific-files>
   git commit -m "chore: project configuration"
   ```
</configure>

<detect_gaps>
## 5. Detect Missing Tools

Scan the project for signals and suggest missing tools:

1. Check what's needed — auth, database, file storage, email, payments, etc.
2. Read `references/external-resources.md` for vetted recommendations
3. Search the MCP registry for anything else
4. Create `DEVELOPER_TODO.md` for any services requiring human setup (API keys, cloud resources, etc.)
</detect_gaps>

<finish>
## 6. Finish

Complete ALL of these before declaring done:

1. **Build passes:**
   ```bash
   {build_command} && {lint_command}
   ```
2. **All changes committed and pushed:**
   ```bash
   git push -u origin $(git branch --show-current)
   ```
3. **`.ai/memory.log` created** with session summary
4. **`.ai/STATUS.md` created** with project state
5. **`CONTEXT.md` filled** with the project's core domain terms — at least 3 entries. The `context-bootstrap` hook scaffolds the file; you fill it before declaring done. See `references/domain-glossary.md`.
6. **`ROADMAP.md` populated** from requirements — not just the empty bootstrap header. Active items reflect the planned scope; phase grouping if multi-phase.
7. **Vendor-adapter structure scaffolded** — `ports/`, `adapters/`, and `composition.ts` exist under the source root, even if empty (adapters added per vendor on demand).
8. **Manual verification instructions provided:**
   ```markdown
   ## How to Verify
   1. [How to install dependencies]
   2. [How to run the dev server]
   3. [What to expect in the browser/terminal]
   4. [Any required environment setup]
   ```
9. **DEVELOPER_TODO.md created** if human actions are needed
10. **Do NOT merge** — leave for human review
</finish>
