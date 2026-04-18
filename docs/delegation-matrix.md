# Delegation Matrix — `agent-skills` ↔ Anthropic's official skill shelf

**Status:** Phase 1 artifact from the audit recommended by `team-composer` on
2026-04-18. This is the working document for the 4-phase absorb / delegate /
reference / keep pass across the 8 custom skills in this repo.

## What this document is

A per-skill map of how each custom skill in `/skills` relates to Anthropic's
officially-shipped skills (the ones installed by default under
`~/.claude/skills/` — `skill-creator`, `docx`, `pptx`, `xlsx`, `pdf`,
`canvas-design`, `algorithmic-art`, `theme-factory`, `web-artifacts-builder`,
`mcp-builder`, `brand-guidelines`, `doc-coauthoring`, `ui-ux-pro-max`,
`ai-safety-mindset`, `consolidate-memory`, `schedule`, `setup-cowork`).

For every custom skill we pick one of four actions per official skill it
touches:

| Action | Meaning |
|---|---|
| **Keep** | No relationship. No mention needed. |
| **Reference** | The custom skill names the official skill in a `Cross-Skill Integration` section and explains when to hand off. |
| **Delegate** | The custom skill actively invokes or hands artifact production to the official skill (e.g., deck styling → `theme-factory`). |
| **Absorb** | Import patterns/conventions from the official skill into our own text (e.g., `skill-creator` authoring conventions). |

## Guiding principles

1. **No deprecations.** Every custom skill has unique orchestration value. The
   overlap is on *output primitives*, not *domain logic*.
2. **Custom owns orchestration + opinion; official owns format + primitive.**
   `pitch-deck` owns founder interview + narrative gating; `theme-factory` owns
   tokens; `pptx` owns binary format fallback.
3. **Graceful degradation.** If a referenced official skill isn't installed,
   the custom skill must still produce *something* — not fail silently.
4. **Reduce trigger collisions.** Where two skills compete on keywords,
   descriptions must state the boundary explicitly.

---

## Per-skill analysis

### 1. `brand-workshop`

**What it produces:** brand strategy brief (.md), tagline, SVG logo, favicon
pack, social banners, descriptions pack, `design-system.md`, branded
pitch-deck template.

| Official skill | Action | Why |
|---|---|---|
| `canvas-design` | **Reference** | For high-fidelity static poster/brand art output quality standards. Brand-workshop's SVG logo generation does not match canvas-design's depth — hand off when the user wants brand art beyond a logo. |
| `algorithmic-art` | **Reference** | When the brand direction calls for generative / procedural visual motifs rather than a mark. |
| `theme-factory` | **Delegate** | Color tokens and font pairing are exactly what `theme-factory` does. Brand-workshop should emit a `design-system.md` that is *compatible with* theme-factory's token shape, so downstream skills (pitch-deck, business-model-canvas) can skin themselves. |
| `brand-guidelines` | **Keep** | `brand-guidelines` is Anthropic-brand-specific. Not applicable. |
| `pitch-deck` (our own) | **Delegate** | Remove brand-workshop's own `pitch-template.html` generation; instead emit a `brand-kit/` folder and let `pitch-deck` consume it. Reduces duplication. |
| `docx` | **Reference** | If the founder wants the brand brief as a Word document. |

**Action summary:** add `Cross-Skill Integration` section. Audit whether the
`brand-kit/deck/pitch-template.html` output should be replaced by a pointer
to `pitch-deck`. Keep SVG logo generation in-skill (that's the differentiator).

---

### 2. `business-model-canvas`

**What it produces:** `business-model.md` + `business-model.html` (9-block
Osterwalder canvas).

| Official skill | Action | Why |
|---|---|---|
| `theme-factory` | **Delegate** | The HTML canvas should pick up `brand-kit/design-system.md` tokens via theme-factory when present. Today it has minimal styling logic — theme-factory is the right owner. |
| `docx` | **Reference** | For `.docx` export when the founder wants to paste into a board doc. Not default. |
| `web-artifacts-builder` | **Reference** | For interactive canvas variants (filters, block toggling). Out of scope for v1 but natural upgrade path. |
| `pdf` | **Reference** | Print-to-PDF is already handled by the inline HTML — no direct delegation needed, but document that `pdf` is the skill for programmatic PDF manipulation if the founder wants to merge the canvas into a larger packet. |
| `team-composer` (our own) | Already referenced. |

**Action summary:** update the stale `pitch-deck (forthcoming)` row (it now
exists). Add `theme-factory` and `docx` rows to the Cross-Skill Integration
section.

---

### 3. `i18n-contextual-rewriting`

**What it produces:** culturally-authentic translations of i18n resource
files.

| Official skill | Action | Why |
|---|---|---|
| All | **Keep** | No overlap. Official shelf has no translation/i18n skill. This is the purest "keep as-is" in the set. |

**Action summary:** audit pass only. Confirm description is collision-free.
No structural changes expected.

---

### 4. `pitch-deck`

**What it produces:** single self-contained Reveal.js HTML deck +
speaker-notes + investor-readiness checklist.

| Official skill | Action | Why |
|---|---|---|
| `theme-factory` | **Delegate** (already documented) | Theme-factory is the styling owner when no `brand-kit/` is present. |
| `pptx` | **Reference (fallback only)** | Per team-composer's own cross-skill guidance: use `.pptx` *only* when the user explicitly requests it. State the trade-off (loss of interactivity, custom animations, programmable charts). Add a short note in our skill. |
| `canvas-design` | **Reference** | For hero/cover-slide static art that justifies the investment in real design over a chart. |
| `web-artifacts-builder` | **Reference** | When the deck needs shadcn/ui components, routing, or state management — i.e., when the "deck" is actually a product demo. |
| `doc-coauthoring` | **Reference** | For long-form narrative drafts that precede the deck (e.g., founder's memo → deck). |

**Action summary:** the existing `Cross-Skill Integration` table is ~90%
correct. Add `pptx` fallback row and a `canvas-design` row. Do not change
core HTML-first behavior.

---

### 5. `skill-evaluator`

**What it produces:** audit findings on rule adherence for an existing
skill, with proposed rule-text diffs.

| Official skill | Action | Why |
|---|---|---|
| `skill-creator` | **Delegate + Absorb** | This is the highest-overlap relationship in the entire repo. `skill-creator` already ships: *"run evals to test a skill, benchmark skill performance with variance analysis, optimize a skill's description for better triggering accuracy."* Our skill must declare a hard boundary: **evaluator = production-time rule adherence + fix-layer classification**; **skill-creator = build-time benchmarking + description optimization**. The existing SKILL.md already has a `Differentiation from skill-creator` table — we should elevate that boundary to the description field so it fires at trigger time, not after. |
| `consolidate-memory` | **Keep** | Unrelated. |

**Action summary:** tighten the description line to put the boundary clause
earlier and more emphatically. Confirm the existing `Differentiation from
skill-creator` section stays intact. Benchmark trigger accuracy in Phase 3.

---

### 6. `sub-agent-coordinator`

**What it produces:** coordination patterns (fan-out, pipeline, specialist)
and sub-agent briefing templates.

| Official skill | Action | Why |
|---|---|---|
| `skill-creator` | **Reference** | For authoring sub-agent-specific skills. Not a delegation — a pointer. |
| Built-in `Task` / Agent SDK | **Reference (external)** | Not an Anthropic *skill* per se, but the Claude Code Agent SDK + `Task` tool is the runtime this skill advises on. Link to `docs.claude.com` where useful. |

**Action summary:** add a short `Cross-Skill Integration` section. No
structural changes.

---

### 7. `team-composer`

**What it produces:** virtual team assembly + 3-round discussion + optional
audit + deliverable delegation.

| Official skill | Action | Why |
|---|---|---|
| `ui-ux-pro-max` | Already referenced. |
| `theme-factory` | Already referenced. |
| `pptx` | Already referenced as fallback. |
| `web-artifacts-builder` | **Reference (new)** | When the team produces a full-stack demo artifact rather than a deck. Currently not named. |
| `mcp-builder` | **Reference (new)** | When the discussion surfaces that the deliverable requires building an MCP server. |
| `ai-safety-mindset` | **Reference (new)** | When `@ai_safety_specialist` is on the team — point them to the official Anthropic mindset skill for shared vocabulary. |

**Action summary:** extend the existing Cross-Skill Integration table with
the three new rows. No discussion-flow changes.

---

### 8. `tech-stack-recommendations`

**What it produces:** opinionated stack guidance for new projects and
migrations.

| Official skill | Action | Why |
|---|---|---|
| `mcp-builder` | **Reference** | When the stack choice involves whether/how to build an MCP server. Point to mcp-builder for authoring guidance. |
| `web-artifacts-builder` | **Reference** | When the recommendation is to prototype in claude.ai artifacts before committing to a full stack. |
| `doc-coauthoring` | **Reference** | When the founder wants the recommendation written up as an ADR / decision doc. |

**Action summary:** add `Cross-Skill Integration` section with the three
rows above.

---

## Summary table

| Custom skill | Keep | Reference | Delegate | Absorb |
|---|---|---|---|---|
| brand-workshop | — | canvas-design, algorithmic-art, docx | theme-factory, pitch-deck (own) | — |
| business-model-canvas | — | docx, web-artifacts-builder, pdf | theme-factory | — |
| i18n-contextual-rewriting | all | — | — | — |
| pitch-deck | — | pptx, canvas-design, web-artifacts-builder, doc-coauthoring | theme-factory | — |
| skill-evaluator | consolidate-memory | — | skill-creator (benchmarking) | skill-creator (conventions) |
| sub-agent-coordinator | — | skill-creator, Agent SDK | — | — |
| team-composer | — | web-artifacts-builder, mcp-builder, ai-safety-mindset (new) | theme-factory, pptx, ui-ux-pro-max (existing) | — |
| tech-stack-recommendations | — | mcp-builder, web-artifacts-builder, doc-coauthoring | — | — |

## Risks

1. **Chain fragility.** If a referenced official skill isn't installed, the
   user hits a silent dead-end. Every delegation must be paired with a
   graceful fallback paragraph in the SKILL.md.
2. **Trigger collisions.** `pitch-deck` + `brand-workshop` both touch
   "deck". `skill-evaluator` + `skill-creator` both touch "eval / audit a
   skill". Phase 3 benchmark must verify <15% collision rate on paired
   prompts.
3. **Description-length limits.** Adding cross-skill guidance to the
   description field risks blowing the trigger budget. Keep boundary
   clauses ≤ 30 words and prefer the body of the SKILL.md for detailed
   hand-offs.
4. **Upstream drift.** Anthropic's official shelf changes. A reference that
   works today may break silently if an official skill is renamed or
   retired. Add a CI check in a later phase that validates referenced
   skill names exist in the default install.

## Phase plan recap

- **Phase 1 (this doc):** delegation matrix produced and reviewed.
- **Phase 2:** SKILL.md edits per the "Action summary" rows above. Target:
  `brand-workshop`, `business-model-canvas`, `pitch-deck` first (highest
  value). Then `skill-evaluator` description boundary. Then the remaining
  three.
- **Phase 3:** trigger-collision benchmark via `skill-creator`. Gate:
  collision rate <15% on paired prompts.
- **Phase 4:** README update + release.

## Open questions

- Does `skill-creator`'s benchmark tool support paired-prompt A/B trigger
  tests out of the box, or do we need a thin harness? (Verify in Phase 1.)
- Does the Claude Code plugin spec support declaring "recommended official
  skills"? If yes, use it. If no, document expectations in README.
- Should `brand-workshop`'s pitch-deck template output be fully removed
  (redirect to `pitch-deck`) or kept as a minimal placeholder? Decide in
  Phase 2 by reading the current `brand-kit/deck/` emission logic.
