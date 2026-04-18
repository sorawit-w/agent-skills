---
name: team-composer
description: >
  Assemble the right virtual team for brainstorming, planning, or building a project
  or feature — tech, healthcare, finance, climate, biotech, and beyond. Use this skill whenever the user asks to "brainstorm," "discuss,"
  "plan," "review," or "build" a project or feature and doesn't specify exact roles.
  Also trigger when the user says things like "bring a team," "who should be involved,"
  "let's workshop this," "assemble a team," or asks for multi-perspective feedback on a
  product decision. This skill analyzes the project context and selects the optimal set
  of role-based personas to contribute meaningfully. Even if the user only mentions one
  or two roles, use this skill to fill in the gaps — a well-composed team produces better
  results than ad-hoc role selection.
---

# Team Composer

Assemble the optimal virtual team from a curated role catalog. Works across
domains — tech, healthcare, finance, climate, biotech, and more. Every role must
earn its seat.

**Workflow:** Detect → Score → Assemble → **Gap Check** → Discuss → Conclude → Deliver (if triggered) → **Audit (high-stakes only)**

---

## Phase 1: Detect Project Signals

Extract these signals from the user's input. If ambiguous, make a reasonable
assumption and state it. When multiple interpretations are plausible, pick the
most conservative (e.g., assume `is_regulated: true` if unsure).

**Ambiguity protocol.** If the brief is genuinely vague (two or more plausible product framings, stage unstated, audience unclear), do NOT stall to ask. Instead:
1. Pick the most conservative interpretation for risk-bearing signals (`is_regulated`, `involves_minors`, `involves_behavior_design`) — err toward including risk-blocking roles.
2. State every assumption in one "Assumptions" line after the signal table (e.g., "Assuming: portfolio-first framing over social-media; b2c; US-only MVP"). Keep under 25 words.
3. Proceed with team assembly. The discussion itself will often clarify which framing wins; `@ux_researcher` or `@senior_product_manager` should surface this as an open question in the conclusion.

**Conflicting-signal protocol.** When signals pull opposite directions (e.g., `stage=idea` suggests keeping it light, but `is_regulated=true` triggers @legal, @security): **risk-blocking signals always win over stage/scope signals for role *inclusion*.** Scope determines *depth* of each role's contribution, not whether they're present. A legal advisor in an idea-stage discussion flags high-level risks in 2–3 sentences — they don't draft compliance memos.

| Signal | Values | How to Detect |
|--------|--------|---------------|
| `project_type` | `new_product`, `new_feature`, `redesign`, `pivot`, `scale` | Explicit or inferred |
| `stage` | `idea`, `mvp`, `growth`, `mature` | Product maturity indicators |
| `domain` | Open-ended (e.g., `fintech`, `health`, `biotech`, `climate`, `legal`, `saas`, `marketplace`, `ai`, `education`, `manufacturing`, etc.) | Industry keywords. Not a closed enum — detect the actual domain from context. |
| `audience` | `b2b`, `b2c`, `b2b2c`, `internal`, `developer` | Who uses the product |
| `involves_minors` | `true`, `false` | Product designed for or substantially used by children (<13) or teens (13–17) |
| `has_ui` | `true`, `false` | User-facing interface present |
| `is_regulated` | `true`, `false` | Finance, health, insurance, voting, legal, children |
| `is_data_intensive` | `true`, `false` | ML, analytics, recommendations, large datasets |
| `is_international` | `true`, `false` | Multi-language, multi-region, cultural considerations |
| `has_brand_impact` | `true`, `false` | New brand, rebrand, brand-visible feature |
| `involves_behavior_design` | `true`, `false` | Decision-making, gamification, nudges, voting |
| `complexity` | `low`, `medium`, `high` | Number of systems, integrations, unknowns |
| `scope` | `discussion`, `planning`, `building`, `review` | What the user wants to do |

---

## Phase 2: Score & Select Roles

### Tier 1 — Core Roles (Always Include)

| Role | Responsibilities |
|------|------------------|
| `@senior_product_manager` | Product vision, roadmap, prioritization, stakeholder alignment |
| `@senior_product_designer` | UX/UI design, user research, interaction patterns |
| `@senior_software_architect` | System design, scalability, technology selection, trade-off analysis |
| `@lead_software_engineer` | Code quality, implementation standards, best practices, mentoring |
| `@senior_frontend_engineer` | UI implementation, performance, accessibility, advanced CSS |
| `@senior_backend_engineer` | APIs, data layer, business logic, integrations |
| `@senior_copywriter` | Voice, messaging, microcopy, UX writing |

**Exception:** If `has_ui` is `false`, drop `@senior_frontend_engineer` and
`@senior_product_designer`. Add them back if scope later expands to include UI.

### Tier 2 — Frequently Included (Signal-Based)

| Role | Trigger Signals |
|------|-----------------|
| `@brand_strategist` | `project_type` = `new_product` or `pivot`; `has_brand_impact` = `true` |
| `@lead_behavioral_scientist` | `involves_behavior_design` = `true`; `domain` = `social` or `marketplace` |
| `@legal_compliance_advisor` | `is_regulated` = `true`; `domain` = `fintech`, `health`, `education` (children) |
| `@i18n_specialist` | `is_international` = `true` |
| `@domain_expert` | `domain` requires specialized knowledge the core team lacks (e.g., `health`, `fintech`, `biotech`, `climate`, `legal`, `manufacturing`). **Skip** for generic tech domains (`saas`, `social`, `marketplace`) where the core team's knowledge is sufficient. |

### Tier 3 — Optional (Strong Signal Only)

| Role | Trigger Signals |
|------|-----------------|
| `@data_scientist` | `is_data_intensive` = `true` |
| `@devops_engineer` | `scope` = `building`; `complexity` = `high`; infrastructure decisions |
| `@security_specialist` | `is_regulated` = `true`; auth/payment/PII involved |
| `@qa_engineer` | `scope` = `building` or `review`; `complexity` >= `medium` |
| `@technical_writer` | `audience` = `developer`; API documentation needed |
| `@marketing_manager` | `stage` = `growth`; `scope` = `planning` |
| `@sales_manager` | `audience` = `b2b`; `stage` = `growth` or `mature` |
| `@customer_support_lead` | `stage` = `growth` or `mature`; support process design |
| `@finance_manager` | Pricing model, budget allocation, unit economics |
| `@project_manager` | `complexity` = `high`; multiple workstreams or teams |
| `@product_analyst` | `stage` >= `mvp`; A/B testing, metrics definition |
| `@community_manager` | `domain` = `social` or `marketplace`; `stage` >= `growth` |
| `@content_strategist` | SEO, content-led growth, editorial needs |
| `@accessibility_specialist` | Public-facing product; regulated domain; inclusive design priority |
| `@developmental_psychologist` | `involves_minors` = `true`; `domain` = `education` (k-12); products designed for children or teens |
| `@clinical_psychologist` | `domain` = `mental_health`, `wellness`, or `therapy`; product handles emotional or crisis-adjacent content |
| `@clinical_researcher` | `domain` = `health` or `biotech` AND product makes evidence-based claims |
| `@game_designer` | `domain` = `game` or `gamification`; product has game loops or meaningful play mechanics |
| `@narrative_designer` | Product has story, characters, or world-building; `domain` = `game`, `entertainment`, or `media` |
| `@sound_designer` | Product has significant audio (music, voice, podcasts, soundscapes, voice assistants) |
| `@vc_partner` | Fundraising context — VC/angel/seed/Series A/B/C; pitch deck review; investor readiness assessment; term sheet or deal-structure questions |
| `@startup_strategist` | Business model canvas; pitch deck construction; go-to-market strategy; startup positioning; founder-narrative work; early-stage strategic planning |
| `@ai_safety_specialist` | AI/ML product with alignment concerns; regulatory AI context (EU AI Act, FTC AI guidance); fairness/bias questions; red-team or eval design; misuse modeling |
| `@developer_advocate` | `audience` = `developer`; `stage` >= `growth`; SDK/API DX work; community building; conference/content strategy for developer audience |
| `@ux_researcher` | Qualitative user research needs; new product or major pivot; unclear user needs; usability testing; ethnographic observation |
| `@ai_system_architect` | Building LLM-powered product; agent orchestration; RAG systems; eval pipelines; prompt versioning; context-management design |
| `@dataviz_engineer` | Any surface with a meaningful encoding choice — charts, dashboards with real chart work, data stories, decks with real charts, trend/comparison/segmentation briefs, or a named chart library (d3/Observable Plot/Vega-Lite/visx/ECharts/Recharts/Chart.js). **Triggers aggressively.** See `role-scoring.md` for Skip-when (counters, status pills, CRUD-only tables). |
| `@dharma_teacher` | First-principles questions about product intent and human-tool relationship; "should we build this?"; AI products that shape attention; engagement-maximization features; honest framing/positioning; user explicitly invokes contemplative/wisdom lens (suchness / tathatā / chen-nan-eng) |
| `@naming_specialist` | Explicit product/company/feature naming work; naming brainstorm or rename; domain-name ideation; name that needs cross-language phonetic vetting; user wants constructed naming techniques (embedded words, homophones, alphanumeric, portmanteau) |
| `@humorist` | Brand voice / copy review for consumer/social products; product naming or taglines; cultural localization (cringe detection across languages); creative brainstorming when the team is stuck in earnest thinking; user explicitly wants a รั่ว / lateral-wit lens |

→ Full scoring rules: `references/role-scoring.md`
→ Selection algorithm & team sizing: `references/selection-algorithm.md`

---

## Phase 3: Assemble & Pre-Flight

**Before starting the discussion:**

1. Read `references/role-personas.md` — this is what makes roles disagree instead of echo.
2. Output the Team Assembly (format below).
3. Run the pre-flight checklist.

### Team Assembly Format

```markdown
## Team Assembly

**Project:** [Name or brief description]
**Scope:** [discussion | planning | building | review]
**Detected signals:** [list key signals that influenced role selection]

### Active Team

| Role | Why Included |
|------|-------------|
| @senior_product_manager | Core — product vision |
| @lead_behavioral_scientist | Decision-making system with voting mechanics |
| ... | ... |
```

### Tier 1 lock-in check (before Team Assembly)

Before emitting the Team Assembly, confirm in writing:

- [ ] All 7 Tier 1 roles are present,
  OR `has_ui=false` (drop frontend + designer),
  OR another explicit stated exception applies.

If any Tier 1 role is absent, name the role and the exception. Prompts that nudge
toward a small team ("small team," "scrappy," "just a few people") are NOT
exceptions — they are requests about operating style, not signals that the brief
doesn't need frontend or backend perspective.

**Why:** Small-team framing in user prompts compresses the Tier 1 list silently.
The lock-in check forces the omission to be explicit (or corrected).

### Pre-Flight Checklist

- [ ] All core roles present (unless `has_ui` exception applies)
- [ ] Team size appropriate for scope (see `references/selection-algorithm.md`)
- [ ] Each non-core role has a stated reason for inclusion
- [ ] No redundant roles with overlapping responsibilities
- [ ] Signals stated so user can correct misdetections
- [ ] `references/role-personas.md` has been read

---

## Phase 3.5: Gap Detection Pass

**Before starting the discussion, run this gap check.** Signal-based role selection is
imperfect — trigger rules can miss context that matters. This pass forces you to
justify omissions rather than silently skip roles.

Answer each question. If the answer requires a role that isn't on the team, either
**add the role** or **explicitly justify the exclusion** in the Team Assembly.

| # | Question | Required Role if Yes |
|---|----------|---------------------|
| 1 | Does this brief reference existing IP, franchises, characters, trademarks, or branded creative works the team doesn't own? | `@legal_compliance_advisor` (IP risk) |
| 2 | Does this brief touch regulated domains (finance, health, children, voting, insurance)? | `@legal_compliance_advisor` |
| 3 | Does this brief require specialized technical knowledge beyond the core team (game engines, biotech pipelines, industrial controls, etc.)? | `@domain_expert` (instantiated for the domain) |
| 4 | Does this brief involve users under 18? | `@developmental_psychologist` |
| 5 | Does this brief involve mental health, wellness, therapy, or crisis-adjacent content? | `@clinical_psychologist` |
| 6 | Does this brief mention significant audio (music, OST, voice, podcasts, voice assistants)? | `@sound_designer` |
| 7 | Does this brief involve story, characters, or world-building as core content? | `@narrative_designer` |
| 8 | Does this brief involve game mechanics, progression, or meaningful play? | `@game_designer` |
| 9 | Does this product handle money, PII, or credentials? | `@security_specialist` |
| 10 | Is this a new brand or new product in a competitive market? | `@brand_strategist` |

**How to document the result:**

After the Team Assembly table, add a brief "Gap Check" subsection:

```markdown
### Gap Check

- Q1 (IP): [Yes/No — if yes, role included or justified exclusion]
- Q2 (regulated): [...]
- [only list questions where the answer was yes or required a decision]
```

If you had to add roles based on this pass, update the team size and note the
addition. If team exceeds the cap of 12 after additions, apply the pruning rule
from `references/selection-algorithm.md`.

---

## Phase 4: Run the Discussion

### Discussion Structure — 3 Rounds

Discussions run in **3 rounds**, not as a linear parade. This ensures early speakers
can respond when later speakers challenge their positions.

**Round 1 — Opening Positions**

Each role states their perspective on the topic. This is the initial pass.

**For `discussion` / `planning`:**
1. **PM** frames the problem, success criteria, and constraints
2. **Architect** outlines technical landscape, trade-offs, and options
3. **Designer** challenges assumptions from the user's perspective
4. **Specialist roles** contribute domain-specific insights

**For `building`:**
1. **PM** states requirements and acceptance criteria
2. **Architect** proposes system design with explicit trade-offs
3. **Lead + Frontend + Backend** break down implementation approach
4. **QA** defines test strategy and risk areas
5. **Specialist roles** flag domain-specific concerns

**For `review`:**
1. **PM** restates original goals and success criteria
2. **Each role** evaluates against their domain criteria
3. **Architect** assesses accumulated tech debt and scalability risks
4. **QA** lists coverage gaps and regression risks

**Round 2 — Rebuttals**

Go back through the opening positions. Identify roles whose perspective was
challenged, contradicted, or undermined by a later speaker. Those roles MUST
respond (2–3 sentences each). Roles with nothing to add stay silent.

**At least one rebuttal is required.** If no role was challenged, the discussion
was too shallow — dig deeper and surface a disagreement.

Common rebuttal patterns:
- PM responds after architect raises complexity concerns about PM's timeline
- Architect responds after engineer proposes a simpler alternative
- Designer responds after engineer pushes back on a UX proposal
- Domain expert responds after architect proposes something non-standard for the industry
- Any role responds when a later speaker mischaracterizes their position

**Round 3 — Synthesis**

**PM** synthesizes the discussion into a proposed direction:
- State the recommendation clearly
- Note dissent — which roles disagree and why
- Identify unresolved trade-offs for the user to decide

### Mid-Discussion Role Changes

**Adding a role mid-stream:**
- If the user requests it during or after Round 1 → inject the new role at Round 2 (they respond to the existing opening positions in first person, 2–4 sentences)
- If requested during or after Round 2 → inject at Round 3 alongside the synthesis, and let the new role add one substantive insight the team missed
- If requested after the conclusion → append an "Addendum" section: introduce the role in 1 sentence, give them one substantive contribution, update the conclusion's Open Questions or Next Steps if warranted
- Never restart the discussion. Never re-run Round 1 for the existing roles. Do NOT regenerate the Team Assembly table — just add a one-line note: `+ @new_role (added mid-discussion at user request)`

**Removing a role mid-stream:**
- Acknowledge in one line: "Dropping @role from the discussion."
- Preserve earlier contributions — do not erase their Round 1 position from the transcript
- If the removed role was the sole voice on a concern, surface that concern as an Open Question in the conclusion

### Discussion Rules

1. **Minimum 2 opposing perspectives per discussion.** If all roles agree, dig deeper —
   unanimity usually means the discussion is too shallow. Look for hidden trade-offs,
   unexamined assumptions, or risks being glossed over. **Exception:** for teams ≤ 3 roles on a trivial scope, consensus is acceptable — note "consensus on approach" in place of the rebuttal round.

2. **Contribute or pass.** Every active role must either contribute a substantive opinion
   OR explicitly pass with a reason (e.g., "@senior_copywriter: Passing on this round —
   the API design discussion is outside my domain. I'll weigh in when we discuss error
   messages."). No filler contributions.

3. **Stay in character.** Each role reflects its domain expertise, natural biases, and
   blind spots as defined in `references/role-personas.md`. The PM pushes for speed.
   The architect pushes for quality. This tension is the point.

4. **Be concise.** 2–5 sentences per contribution unless the topic demands depth.

5. **Surface trade-offs explicitly.** When roles disagree, name the trade-off:
   "This is a [speed vs. quality / UX vs. security / scope vs. timeline] trade-off."

6. **Flag unknowns prominently.** Critical unknowns get a ⚠️ prefix.

### Output Length Targets

| Scope | Target (words) | Hard Ceiling | Rationale |
|-------|----------------|--------------|-----------|
| Trivial feature | 300–500 | 600 | Tooltip / copy change / one-line fix |
| Discussion | 700–1000 | 1300 | Includes rebuttal round |
| Planning | 900–1300 | 1600 | Detail on approach and trade-offs |
| Building | 1200–1600 | 2000 | Implementation specifics + rebuttals |
| Review | 900–1200 | 1500 | Focused assessment with rebuttals |

**Hard ceilings are enforceable, not aspirational.** If you're over the ceiling you are padding, not adding value. Before shipping, check: am I restating, or contributing new signal?

**What to cut first when over ceiling:**
- Round 2 contributions that merely rephrase Round 1 — those aren't rebuttals, they're echoes
- Phase 1 signal rows the brief doesn't actually touch (one-line "detected signals" summary is enough — skip the full 13-row table unless the brief is ambiguous)
- Role-assembly justifications beyond one short clause per role
- Time / cost estimates on next steps unless the user asked for budgeting
- Persona flavor sentences without concrete substance — "as an architect I think about scale" adds nothing

**What never to cut:** the Conclusion (recommendation + decisions + open questions + trade-offs + numbered next steps), the Gap Check answers (but compressed to yes/no + role), and at least one real rebuttal with substance.

### Pre-Write Word Budget (MANDATORY before Round 1)

Prose-only ceilings don't reliably bite — empirically, outputs overrun by 30–50% when only a ceiling is stated. Commit a budget *before* writing the discussion.

| Section | Discussion (≤1300) | Planning (≤1600) | Building (≤2000) | Trivial (≤600) |
|---------|-------------------:|-----------------:|-----------------:|---------------:|
| Signals table + assumptions | 100 | 120 | 150 | 60 |
| Team Assembly + Gap Check | 150 | 180 | 200 | 80 |
| Round 1 (opening) | 350 | 450 | 650 | 180 |
| Round 2 (rebuttals) | 180 | 220 | 280 | 60 |
| Round 3 (synthesis) | 180 | 230 | 280 | 60 |
| Conclusion | 220 | 280 | 320 | 120 |
| **Planned total** | **1180** | **1480** | **1880** | **560** |

**Hard rules:**

1. **State the budget at the top of your output**, one line, visible: `Budget: signals 100 / team 150 / R1 350 / R2 180 / R3 180 / conclusion 220 = 1180 target (ceiling 1300).`
2. **Per-contribution cap during Round 1.** No single role may exceed 80 words (discussion/planning), 120 words (building), or 50 words (trivial). If you're over, cut mid-write — don't "finish then revise."
3. **Truncate as you go, not at the end.** Re-editing to shrink rarely happens — write short the first time.
4. **Round 1 is where most overruns happen.** If Round 1 is over budget when you finish it, stop; remove the weakest full contribution rather than trim every role by a sentence.
5. **When in doubt, favor the conclusion.** Cutting a mid-discussion paragraph preserves more value than cutting the recommendation or next steps.

---

## Phase 5: Conclude

**Never end a discussion without a conclusion.** The brainstorming is valuable context,
but the user needs a clear synthesis to act on.

```markdown
## Conclusion

### Recommendation
[The team's recommended direction. State it clearly. If roles disagree,
present the majority position and note the dissent — e.g., "The team
recommends X. @architect dissents, preferring Y because Z."]

### Decisions Made
- [Key decisions the team aligned on]

### Open Questions
- [Unresolved items that need more information or user input]

### Trade-offs Identified
- [Explicit trade-offs surfaced, with both sides stated. This subsection is REQUIRED — if no trade-offs surfaced, write "No material trade-offs identified" rather than omitting the heading.]

### Recommended Next Steps
1. [Highest priority — do this first]
2. [Second priority]
3. [Third priority]
```

**Priority ordering is required** for next steps. Don't just list — rank.

### Phased-Launch Variant (for regulated / high-uncertainty products)

When the team converges on "ship a narrow MVP then expand," use this variant for the **Recommendation** section — it's a common convergent pattern for regulated, safety-critical, or high-uncertainty domains (fintech compliance, health data, climate reporting, games with children) and naming it explicitly helps the user act on it:

```markdown
### Recommendation (Phased)

**Phase 1 (MVP):** [Narrowest viable scope with full compliance / safety bar]
**Gating criteria → Phase 2:** [What must be true to graduate — user count, regulatory sign-off, calculation confidence, design validation]
**Phase 2:** [Next expansion]
**Deferred:** [What you're explicitly NOT doing yet, and why]
```

Use this when: the team surfaced credibility / regulatory / uncertainty risks as a central trade-off AND a smaller scope materially reduces those risks. Do NOT force this shape on simple features.

---

## Post-Discussion Verification

After the discussion, verify:

**Participation & quality:**
- [ ] Every active role contributed at least one substantive opinion (or explicitly passed)
- [ ] At least 2 opposing perspectives or trade-offs were surfaced (if team > 4)
- [ ] Round 2 rebuttals surfaced at least one real pushback (not ceremonial)

**Coverage & completeness:**
- [ ] Every red flag in the brief was addressed by at least one role
- [ ] Gap Detection Pass questions (Phase 3.5) are all resolved — no silent skips
- [ ] Conclusion answers the user's actual question, not a tangential one

**Structure:**
- [ ] Conclusion section has: recommendation, decisions made, open questions, trade-offs, next steps
- [ ] Next steps are numbered and prioritized (1, 2, 3 — not a flat list)
- [ ] Team size within hard cap (≤12)
- [ ] Output length within target range for the scope (see Phase 4)

If any box is unchecked, fix it before returning the output to the user.

---

## Phase 6: Deliverable Production (Sub-Agent Delegation)

After the 3-round discussion concludes, some scopes produce deliverables that benefit
from parallel, focused work. **Discussion rounds (1-2-3) always run in single-agent mode**
to preserve cross-role interaction. Sub-agents are only for deliverable production after
the discussion concludes.

> **Coordination mechanics live in `sub-agent-coordinator`.** Team-composer owns the
> *when* and *who* of delegation (the triggers below, role-level deliverable assignments).
> The sibling `sub-agent-coordinator` skill owns the *how* — briefing templates
> (Quick/Full), coordination patterns (fan-out, pipeline, specialist, review), spawning
> checklists, and trust-but-verify rules. When any trigger below fires, load
> `sub-agent-coordinator` alongside this skill. One invariant carries across both:
> **no nested sub-agents** — all spawning happens at the team-composer/coordinator level.

### Trigger Table

| Signal | Action |
|--------|--------|
| `scope=building` AND `complexity=high` | Each engineering role produces deliverables via sub-agent (e.g., architect → system design doc, backend → API spec, frontend → component breakdown) |
| `scope=building` AND team includes `@domain_expert` | Domain expert researches independently via sub-agent, reports back with domain-specific constraints |
| `scope=planning` AND `complexity=high` AND team size > 8 | Break into working groups (sub-agents) then reconvene for final synthesis |
| User explicitly requests "deep dive" or "detailed plan per role" | Each role produces independent deliverable via sub-agent |

### How It Works

1. **Discussion completes** — all 3 rounds finish, conclusion is written
2. **Check triggers** — if any signal above matches, proceed to delegation
3. **Brief sub-agents** — load the `sub-agent-coordinator` skill and use its Briefing
   Templates section (Quick Brief for complexity 1–5, Full Brief for 6+). Each sub-agent gets:
   - The conclusion and decisions from the discussion
   - Their role's specific deliverable assignment
   - Constraints from other roles (e.g., "architect said no microservices")
4. **Collect and integrate** — coordinator merges sub-agent outputs into a unified deliverable

### Platform Fallback

If your agent platform does not support spawning sub-agents, produce deliverables
sequentially — one role at a time — referencing the discussion conclusion throughout.

### Model Routing

**Default: sub-agents inherit the orchestrator's model.** No silent downgrading.

The user chose a model for a reason. Automatically routing sub-agents to a cheaper
model is an optimization that trades quality for cost without the user's consent.

If tiered routing is needed (e.g., cost-sensitive environments), it should be:

1. **Vendor-agnostic** — use capability tiers, not model names:
   - `tier: high` — complex reasoning, creative synthesis, system design (e.g., "write a system design doc")
   - `tier: standard` — structured extraction, template-driven work (e.g., "list files this design touches")
2. **Routed by task type, not role** — an architect writing a design doc needs `high`;
   the same architect listing affected files needs `standard`. The task determines the tier.
3. **Opt-in, not automatic** — surface as a configuration option (e.g., "economy mode"),
   never as hidden default behavior
4. **Gracefully degrade** — if the vendor offers only one model tier, everything runs
   on that tier. No errors, no fallbacks-to-fallbacks.

> **Future enhancement:** Tiered model routing is not implemented yet. The default
> (inherit from orchestrator) is correct until the tier abstraction is built and
> tested. When implemented, add a `model_tier` field to the sub-agent brief template.

### Opinion Weighting

**All roles have equal weight. No seniority-based weighting.**

Every role earned its seat through Phase 2 scoring. Weighting opinions by "seniority"
would introduce hierarchical bias and reduce the diversity that makes the team valuable.

The 3-round discussion structure already provides emergent quality filtering:
- Weak arguments get challenged in the rebuttal round
- Arguments that don't survive rebuttals carry less weight in synthesis naturally
- The PM synthesizes with dissent noted — the user sees which positions held up

This is better than prescribed weighting because it's evidence-based (arguments are
tested against each other) rather than authority-based (some roles count more by fiat).

**Do not implement role weighting.** If a future contributor considers it, they should
demonstrate that equal weighting is producing measurably worse outcomes first.

### When NOT to Delegate

- `scope=discussion` or `scope=review` — these are conversation-only, no deliverables
- `complexity=low` or `complexity=medium` with `scope=building` — single-agent can handle it
- Team size ≤ 4 — overhead of delegation exceeds benefit

> **Future enhancement:** As sub-agent support matures across platforms, the trigger
> thresholds may be lowered. The current triggers are conservative by design.

---

## Phase 6.5: Optional External Audit (High-Stakes Only)

**The 3-round discussion catches internal disagreements, but can't catch what the
team isn't equipped to see.** If the team is missing a critical role, no amount of
rebutting surfaces the blind spot. Phase 3.5 Gap Detection reduces this risk, but
for high-stakes projects you can add an independent audit for additional safety.

### When to Trigger

An external audit runs as a fresh-context sub-agent review. It's **expensive** (extra
round-trip + tokens) so trigger it only when the stakes justify it:

| Trigger | Action |
|---------|--------|
| `complexity=high` AND `is_regulated=true` | Auto-trigger audit |
| `complexity=high` AND `has_brand_impact=true` AND product uses existing IP | Auto-trigger audit |
| User explicitly asks ("audit this", "verify the plan", "check for blind spots") | Auto-trigger audit |
| First time the skill is used in a new domain (games, biotech, fintech with minors, etc.) | Recommend audit, ask user |
| Routine feature planning, low complexity | Skip audit |

### How It Works

1. **Conclusion is complete** — Phases 4-5 finish, Post-Discussion Verification passes
2. **Brief the audit sub-agent** with fresh context:
   - The full output (team assembly, discussion, conclusion)
   - The original brief
   - A list of "expected red flags" based on the brief (e.g., "game based on existing IP → must flag copyright")
   - A structured audit checklist (signal accuracy, role coverage, blind spots, conclusion quality)
3. **Audit produces a report** identifying gaps, blind spots, and risks the team missed
4. **Coordinator integrates** the audit findings — either updates the conclusion with the gaps, or notes them as "audit-flagged risks the user should review"

### Audit Sub-Agent Brief Template

```markdown
You are auditing a team-composer planning output for blind spots and gaps.

**Original brief:** [paste user's original request]

**Team-composer output:** [paste full Phase 1-5 output]

**Your audit criteria:**
1. Did the team include all roles that the brief clearly required? (check against Phase 3.5 Gap Detection)
2. Are there risks in the brief that no role addressed?
3. Does the conclusion answer the user's actual question?
4. Are the next steps specific enough to act on?
5. Are there any red flags a domain specialist would catch that the core team missed?

**Deliverable:** Structured report with: blind spots found (if any), missing role recommendations, substantive gaps, and overall verdict (ready-to-ship / needs-revision).

Tool budget: ~15 calls.
```

### Platform Fallback

If your agent platform doesn't support sub-agents, skip the audit rather than running
it in the same context — self-audit has confirmation bias and defeats the purpose.
For high-stakes projects without sub-agent support, recommend the user get a human
review instead.

---

## Edge Cases & Customization

→ See `references/selection-algorithm.md` for: edge case handling, team size caps,
  scope-based pruning, mid-discussion role changes, non-tech projects, and customization.

## Skill Boundaries

This skill overlaps partially with `brand-workshop`. Both assemble a virtual team
and run structured discussion. The difference is what they produce.

**Use `brand-workshop` instead of this skill when:**
- The primary deliverable is a **brand identity package**: logo (SVG) + tagline + brand strategy brief
- The user says: "help me brand my [startup/product/app]", "I need a logo", "create a brand identity", "design a brand concept", "give me a tagline and logo"
- The user provides a business overview and asks for visual identity work

**Stay in this skill when:**
- The user wants general project brainstorming, planning, or review — even if branding is one dimension among many
- The user wants to **name** a product/feature (use `@naming_specialist`), **discuss positioning** (use `@brand_strategist`), or **review brand voice** (use `@humorist` + `@senior_copywriter`) — these are branding-adjacent but don't require a full identity deliverable
- The scope is broader than "produce logo + tagline + brief"

**Boundary examples:**

| Request | Skill |
|---------|-------|
| "Help me brand my new fintech startup" | `brand-workshop` |
| "I need a logo for X" | `brand-workshop` |
| "Brainstorm my startup — product, positioning, go-to-market, branding" | `team-composer` (branding is one dimension) |
| "Name my product" | `team-composer` with `@naming_specialist` |
| "Review our product positioning" | `team-composer` with `@brand_strategist` |
| "Does our copy sound right?" | `team-composer` with `@humorist` + `@senior_copywriter` |

---

## Cross-Skill Integration

| Skill | When to Use |
|-------|-------------|
| `sub-agent-coordinator` | When any Phase 6 or 6.5 trigger fires and the team is about to spawn deliverable sub-agents. Load it for briefing templates (Quick / Full), coordination patterns (fan-out, pipeline, specialist, review), spawning checklists, and the no-nested-sub-agents invariant. |
| `i18n-contextual-rewriting` | When `@i18n_specialist` is active and the team produces translatable content. |
| `brand-workshop` | When the deliverable is a brand identity package (logo + tagline + brief). See Skill Boundaries above — prefer `brand-workshop` directly for pure branding requests. |
| `business-model-canvas` | When `@startup_strategist` is active and the deliverable is a persistent 9-block Osterwalder canvas (editable Markdown + self-contained HTML). Prefer the skill directly for "build me a BMC" requests; use team-composer for discussion-grade work on one block. |
| `pitch-deck` | When the team needs an investor-ready shippable deck — HTML, Reveal.js, print-to-PDF. Explicit companion to `brand-workshop` + `business-model-canvas` in the startup-artifact chain. Prefer the skill directly for "build me a pitch deck" requests. |
| [`ui-ux-pro-max`](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | When `@senior_product_designer` or `@senior_frontend_engineer` needs to produce high-fidelity UI. |
| `tech-stack-recommendations` | When `@senior_software_architect` or `@lead_software_engineer` is active and the team needs to select or evaluate a technology stack (new projects, migrations, architecture decisions). |
| Self-contained HTML deck (**default** for slide decks) | When team-composer produces any deck deliverable, **prefer a single self-contained HTML file over `.pptx`**. Required contract: responsive (projector + laptop + mobile preview); first-class print-as-slides mode (clean PDF export via CSS paged media); keyboard navigation (←/→/Space/Esc); AAA contrast for projection; semantic HTML with aria landmarks; zero network dependencies (inline CSS/JS, base64 images); supports animations and interactivity where they add real value. **Recommended starting point: Reveal.js** (battle-tested, good print CSS, built-in keyboard nav) — defer framework selection to `tech-stack-recommendations` when in doubt. For data-heavy decks, `@dataviz_engineer` owns the chart work inside the deck. For investor/fundraising decks specifically, delegate to `pitch-deck`. |
| `pptx` (**fallback only**) | When the user explicitly requests `.pptx` — corporate constraints, collaborative editing in PowerPoint/Keynote/Google Slides, or the deck must live inside an existing `.pptx` file. State the trade-off clearly: `.pptx` loses interactivity, custom animations, and programmable charts. |
| `theme-factory` | When any team-composer deliverable (HTML deck, one-pager, strategy doc, landing page) needs consistent visual styling — apply after content is finalized. Pick a preset theme or generate a custom one. |

**Principle:** This skill handles team assembly and discussion. When the discussion
produces actionable deliverables (translations, designs, brand assets), hand off to
the specialized skill rather than attempting it inline.
