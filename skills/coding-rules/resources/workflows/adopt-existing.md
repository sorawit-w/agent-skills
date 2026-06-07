# Adopt Existing Project Workflow

You are onboarding an **existing repo** (real code, git history, conventions) into coding-rules by populating — and refreshing — the artifacts BOOTSTRAP's `detect_project` step reads. This is the `prepare` sub-command's procedure.

**This is to an existing repo what `new-project.md` is to greenfield:** it produces the same ready-state, but derived from *what is already built* (code + git history) rather than from requirements.

> **Not the resume flow.** `references/workflows.md` → "Existing Project Flow" *reads* these artifacts and routes to work, assuming they exist. This workflow is the *first-time populate* that creates them. After `prepare`, future sessions use the resume flow.

---

<core_principles>
## Core principles — read before touching any file

1. **Tier population by inferability-from-code.** What the code reliably tells you (stack, entry points) is auto-filled. What it hints at (domain vocabulary) is proposed. What lives only in people's heads (the *why* behind decisions) is drafted as low-confidence candidates, never asserted.
2. **Diff-and-confirm every write.** Show the proposed file (or the proposed addition) and get a yes before writing. Same consent discipline as `install`. Never write silently.
3. **Never clobber human-curated content.** Refresh re-derives only agent-owned material. Anything a human wrote or verified is frozen. Per-tier refresh rules below.
4. **Never write secret contents.** When a scan surfaces `.env`-like or credential files, record *paths only*, never the values inside them.
</core_principles>

---

<pre_work>
## 1. Pre-Work

Read these before starting:

1. `references/workflows.md` — the resume "Existing Project Flow" this complements
2. `references/communication.md` — canonical `memory.log` format, commit format
3. `references/knowledge-management.md` — knowledge entry schema, `confidence` tiers, proposal workflow
4. `references/domain-glossary.md` — what belongs in `CONTEXT.md`
</pre_work>

---

<assess>
## 2. Assess the existing code

Build the raw material for population. **Read-only — no writes in this step.**

1. **Capability gate — structure indexing.** If a SocratiCode / codegraph MCP is connected, use it for the WHAT: module map, symbols, dependency graph (`codebase_index`, `codebase_symbols`, `codebase_graph_*`). It is an **accelerator, never a dependency** — if absent, fall back to `find`/`grep`/manifest parsing. Your value-add is the WHY and the curation, not reinventing the index.

2. **Manifests & stack** (feeds `agent-context.yaml`): parse whichever exist — `package.json`, `deno.json`, `pyproject.toml`, `go.mod`, `Cargo.toml`, etc. Derive runtime, language, target/framework, tools, entry points, source/dist directories. Map dependencies → frameworks/tools.

3. **Recurring vocabulary** (feeds `CONTEXT.md`): frequency-analyze domain identifiers across the source tree (class/module/function names), filtering framework noise. Pull recurring terms from `README.md`. Note top-level source dirs for the module map.

4. **Decision/lesson signal** (feeds `.ai/knowledge/`): scan `git log` bodies for recurring rationale, look for `docs/adr/` or design docs, note major dependency choices and large refactors (decision candidates) and recurring fix patterns (lesson candidates). Capture *pointers*, not conclusions — you draft these in step 3.

5. **Current branch** (feeds `STATUS.md` stub): `git branch --show-current`.
</assess>

---

<populate>
## 3. Populate — tiered, each behind diff-and-confirm

Work top-down through the tiers. Each artifact: build the proposed content, **show it**, get a yes, then write.

### High inferability — `agent-context.yaml` (auto-fill)

Fill the mechanical fields from step 2 against `templates/agent-context.yaml.template`: `project.name/description/type`, `runtime.*`, `stack.*`, `entryPoints`, `directories`. Leave `agentNotes`, `ai`, and `preferences` as the human's to fill. Show the proposed file; confirm; write.

### Medium inferability — `CONTEXT.md` (propose)

If `CONTEXT.md` is missing, start from `templates/CONTEXT.md.template`. Propose:
- **Glossary:** the recurring domain terms from step 2 — aim for ≥3 real entries, each a one/two-line definition with a code pointer.
- **Module map:** one line per top-level source dir.

These are *proposals* — present them, let the human cut/correct, then write under the template's markers.

### Low inferability — `.ai/knowledge/` (draft candidates)

**First-run detection:** if `.ai/knowledge/` has no entry files (only `KNOWLEDGE.md`, or the dir is absent) → run this pass **automatically**. If entry files already exist → it is **opt-in**: ask *"Draft candidate decision/lesson entries from your git history for review?"* and skip on no.

When the pass runs, draft entries from the step-2 signal using the `knowledge-management.md` schema, with two hard constraints:
- **`confidence: low`** on every drafted entry (agent-inferred, unverified).
- **Hedged prose** — "appears to…", "inferred from commit history…" — so a reviewer can tell agent-drafted from human-verified at a glance. Do **not** assert rationale the code doesn't prove.

Show each candidate; confirm each individually (per the never-write-knowledge-silently rule). After writing approved entries, run:
```bash
bash "${CODING_RULES_DIR}/resources/hooks/knowledge-reindex.sh" --force
```
(or update the `AUTO-INDEX` block in `KNOWLEDGE.md` by hand if the hook isn't wired).

### Stub only — `.ai/STATUS.md`

Create from `templates/STATUS.md.template` as an **honest onboarding stub**: phase `Onboarded`, current branch, no active tasks ("freshly onboarded, no active work"). Do not invent progress, milestones, or a task queue for a repo you just met. Confirm; write.

### Stub only — `.ai/memory.log`

Append one onboarding entry in the canonical `communication.md` format (Task: "Project onboarding via prepare", Action, Files, Status: DONE, Notes: stack summary + what was populated). Append-only; create if missing.
</populate>

---

<refresh>
## 4. Refresh rules (re-running `prepare` on an already-onboarded repo)

`prepare` is idempotent — re-running is a **diffs-only near-no-op**. Per tier:

- **`agent-context.yaml`** — re-derive mechanical fields only; show the diff; confirm. **Never touch `agentNotes`, `ai`, `preferences`, or any human-edited field.**
- **`CONTEXT.md`** — **append only**. Propose newly-discovered terms under the existing markers. Never rewrite or reorder existing glossary entries.
- **`.ai/knowledge/`** — re-draft **only entries still tagged `confidence: low`**. Any entry promoted to `confidence: high` (or `medium` after human review) is frozen — leave it untouched.
- **`.ai/STATUS.md`** — leave an existing STATUS alone; it belongs to live work now, not onboarding.

If nothing changed since the last run, say so and write nothing.
</refresh>

---

<finish>
## 5. Finish

Complete before declaring done:

1. **`agent-context.yaml`** populated (mechanical fields), confirmed before write.
2. **`CONTEXT.md`** has ≥3 real glossary terms + a module map, confirmed.
3. **`.ai/knowledge/`** candidates drafted (auto on first run, opt-in after) as `confidence: low`, each confirmed; index regenerated.
4. **`.ai/STATUS.md`** honest onboarding stub created.
5. **`.ai/memory.log`** onboarding entry appended.
6. **Tell the human what's now agent-drafted and needs review** — especially the `confidence: low` knowledge entries and proposed glossary terms.
</finish>

---

<out_of_scope>
## Out-of-scope ring-fence

`prepare` populates context. It does **not**:
- run quality gates (build/lint/test) — onboarding reads, it doesn't verify the build;
- install linters/formatters or any tooling;
- scaffold vendor-adapter dirs (`ports/`/`adapters/`/`composition.ts`) — that's `new-project.md`;
- author `DESIGN.md` — design-token authority is a separate concern; tokens are only sometimes code-inferable and a wrong contract is worse than none. If a UI project lacks one, mention it; don't generate it. See `references/design-md.md`;
- create `ROADMAP.md` — only on explicit user request;
- create a working branch, commit, push, or merge — leave VCS actions to the human;
- write secret file *contents* into any artifact.
</out_of_scope>
