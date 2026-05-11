# Auto-Pick Heuristic

How wear-the-hat picks a role when the user doesn't name one explicitly. This is a **literal keyword/verb table**, not an ML classifier. The point is predictable, debuggable, easy to extend.

> **Role name authority:** every role named below MUST exist as a defined persona in `team-composer/references/role-personas.md`. If you add a row that references a role not yet in the catalog, either add the catalog entry first or pick an existing role. Drift between this file and the catalog is the failure mode this file is designed to avoid.

---

## Algorithm

For each invocation:

1. **Extract signals** from the task brief:
   - Verbs (audit, design, implement, review, encode, write, debug, refactor, name, translate, …)
   - Domain keywords (security, accessibility, data-viz, brand, AI safety, performance, …)
   - Surface area (single file? whole subsystem? multi-system? URL?)
   - Deliverable shape (code, doc, copy, chart, plan, …)

2. **Match against the table below.** Each row has a `match` pattern (keywords/verbs) and a `role`. A row matches when the task contains the keywords in the `match` column.

3. **Count matches:**
   - Exactly 1 row matches → **Outcome A** (clean match). Disclose and proceed.
   - 2–3 rows match → **Outcome B** (multi-candidate). Present candidates, ask user to pick.
   - 4+ rows match OR a Multi-Role Trigger fires → **Outcome C** (multi-role task). Stop, present options, offer team-composer hand-off.
   - 0 rows match → **Outcome D** (no match). Fall back to default (see bottom of file).

4. **Return the result** for Phase 2 of the SKILL.md flow.

The four outcomes are spelled out in `SKILL.md` § Phase 1.

---

## Signal → Role Table

Roles listed below MUST be valid entries in `team-composer/references/role-personas.md`. If a role isn't there yet, add it to the catalog before adding the row here — don't invent roles in this file.

| # | Match (verbs / keywords) | Role |
|---|---|---|
| 1 | audit security, security audit, vulnerability, CSRF, XSS, auth review, threat model, OWASP | `@security_specialist` |
| 2 | architect, system design, scalability, service boundary, monolith vs microservices, distributed | `@senior_software_architect` |
| 3 | implement endpoint, API contract, database schema, query, migration, backend logic | `@senior_backend_engineer` |
| 4 | UI implement, render performance, layout shift, bundle size, frontend perf, accessibility tree | `@senior_frontend_engineer` |
| 5 | accessibility, a11y, WCAG, screen reader, keyboard nav, color contrast (alone) | `@accessibility_specialist` |
| 6 | chart, visualization, dashboard, encoding choice, d3, recharts, observable plot, vega-lite | `@dataviz_engineer` |
| 7 | UI motion, micro-interaction, polish, "does this feel right", component library, design system feel | `@design_engineer` |
| 8 | UX design, user flow, interaction pattern, wireframe, prototype | `@senior_product_designer` |
| 9 | copy, microcopy, tagline, UX writing, button text, error message wording | `@senior_copywriter` |
| 10 | brand voice, positioning, brand strategy, messaging pillar | `@brand_strategist` |
| 11 | naming, product name, feature name, domain name, brainstorm names | `@naming_specialist` |
| 12 | data analysis, statistical test, A/B test, distribution, outlier, correlation | `@data_scientist` |
| 13 | product analytics, funnel, retention, A/B test design (PM-style) | `@product_analyst` |
| 14 | user research, interview, survey, usability test, ethnographic | `@ux_researcher` |
| 15 | research synthesis, theme extraction, insight clustering | `@ux_researcher` |
| 16 | AI safety, alignment, red-team, eval design, misuse modeling | `@ai_safety_specialist` |
| 17 | LLM product, prompt engineering, agent orchestration, RAG, context-management | `@ai_system_architect` |
| 18 | DevOps, CI/CD pipeline, infrastructure, deployment, container | `@devops_engineer` |
| 19 | QA, test plan, test strategy, regression, coverage | `@qa_engineer` |
| 20 | tech writing, API documentation, runbook, developer docs | `@technical_writer` |
| 21 | legal, compliance, GDPR, CCPA, data subject request, regulation | `@legal_compliance_advisor` |
| 22 | i18n, localization, translation, locale, cultural adaptation | `@i18n_specialist` |
| 23 | game mechanics, progression, game design, level design | `@game_designer` |
| 24 | story, narrative, character, world-building, story arc | `@narrative_designer` |
| 25 | sound, music, voice, podcast, audio design | `@sound_designer` |
| 26 | clinical, mental health, therapy-adjacent, crisis content | `@clinical_psychologist` |
| 27 | developmental, children, minors, age-appropriate, K-12 | `@developmental_psychologist` |
| 28 | fundraising, pitch deck review, term sheet, VC, investor lens | `@vc_partner` |
| 29 | startup strategy, lean canvas, value proposition canvas, GTM, founder narrative | `@startup_strategist` |
| 30 | engineering plan, phased plan, decisions locked, decisions deferred, agent-executable plan | `@staff_engineer` |
| 31 | code quality review, readability, refactoring, pattern review (no security focus) | `@lead_software_engineer` |
| 32 | engagement maximization audit, attention design ethics, contemplative lens, suchness | `@dharma_teacher` |
| 33 | brand voice review, copy cringe detection, humor calibration, lateral wit | `@humorist` |
| 34 | product strategy, roadmap, prioritization, scope vs timeline | `@senior_product_manager` |

---

## Multi-Role Triggers (fire Outcome C directly)

These task shapes are intrinsically multi-role. Match any one of them → Outcome C (multi-role task), regardless of which rows above also match.

| # | Match | Candidate single-role escapes |
|---|---|---|
| MR-1 | slide deck, presentation, HTML deck, pitch deck, investor deck | `@senior_frontend_engineer` (HTML), `@senior_copywriter` (content), `@narrative_designer` (story arc), or hand off to `team-composer` / `pitch-deck` |
| MR-2 | landing page (with hero + copy + design + CTA) | `@senior_frontend_engineer` (build), `@senior_copywriter` (copy), `@brand_strategist` (positioning), or hand off to `team-composer` |
| MR-3 | end-to-end feature (UI + API + tests + docs) | `@senior_frontend_engineer`, `@senior_backend_engineer`, or hand off to `team-composer` for design, then sub-agent-coordinator for parallel implementation |
| MR-4 | new product brief (problem + audience + solution + GTM) | `@senior_product_manager`, `@startup_strategist`, or hand off to `team-composer` |
| MR-5 | full marketing campaign (channels + content + copy + brand) | `@brand_strategist`, `@senior_copywriter`, or hand off to `team-composer` for the campaign plan |
| MR-6 | rebrand / brand identity from scratch (logo + tagline + brief) | Hand off to `brand-workshop` directly — wear-the-hat is the wrong skill for this |

For MR-6 specifically: do NOT offer a single-role escape. `brand-workshop` is the correct skill; redirect there.

---

## Default fallback (Outcome D)

If zero rows match:

| Task vibe | Default role |
|---|---|
| Coding-flavored (mentions code, files, repo, commit, tests) | `@lead_software_engineer` |
| Non-coding (writing, planning, generic professional task) | `@senior_product_manager` |
| Ambiguous | `@lead_software_engineer` (this repo skews coding) |

Always disclose the fallback:

> Couldn't auto-pick a specialized role. Defaulting to `@lead_software_engineer`. If you wanted a different lens, name it: `as @<role>`.

---

## Maintenance

- **Adding a row:** if a real task came in and no row matched, add the row. Don't backfill speculatively — only add rows the actual usage exercises.
- **Catalog drift check:** before adding a row, verify the role exists in `team-composer/references/role-personas.md`. If it doesn't, add the catalog entry first or pick an existing role.
- **Row precedence:** rows are checked in order. If multiple match, the algorithm counts them (for Outcome A/B/C determination); it does not silently pick "the first one."
- **No deletions without reason.** If a row stops matching anything in practice, leave it — the cost of an unused row is one line; the cost of deleting a needed row is a silent regression.

---

## Why this is a literal table, not an ML classifier

- **Debuggable.** When auto-pick produces an unexpected result, you can read the table and see which row fired.
- **Easy to extend.** Adding a row is a one-line edit. No retraining.
- **Predictable.** Same task input → same role output, every time. No drift.
- **Cheap.** Zero inference cost; the orchestrator does string matching against the table.

The catalog (`role-personas.md`) is the rich part — each role has perspective, signature phrases, etc. This file is just the routing map.
