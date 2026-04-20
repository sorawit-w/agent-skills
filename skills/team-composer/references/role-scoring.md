# Role Scoring Matrix

Detailed scoring rules for Tier 2 and Tier 3 role selection. Each role has trigger
conditions, strength indicators, and anti-patterns (when NOT to include).

---

## Tier 2 — Frequently Included Roles

### `@brand_strategist`

**Include when:**
- New product launch (not just a feature)
- Pivot or rebrand
- User-facing feature that significantly changes brand perception
- First entry into a new market segment

**Skip when:**
- Internal tool or developer-facing API
- Incremental feature update
- Backend/infrastructure work

**Strength indicator:** The word "brand," "positioning," "identity," or "differentiation"
appears in the brief, or the project introduces the product to a new audience.

---

### `@lead_behavioral_scientist`

**Include when:**
- Decision-making systems (voting, ranking, scoring, recommendations)
- **Rating, review, feedback, or social-proof systems** (star ratings, thumbs up/down, NPS, reviews, endorsements, testimonials) — these are behavior-design surfaces even when they look like CRUD
- Gamification, streaks, rewards, progress systems
- Social features (reputation, trust, moderation)
- Nudge design (defaults, framing, choice architecture)
- Onboarding flows where user motivation is critical
- Marketplace dynamics (two-sided incentives)
- **Retention surfaces** (re-engagement emails, notification timing, dormant-user revival) where response rate is the success metric

**Skip when:**
- CRUD operations *without* a scoring/feedback component (a user profile edit is not behavior design; a user profile with public reputation is)
- Infrastructure / DevOps tasks
- Content-only features (blog, docs) with no interaction loop

**Strength indicator:** The feature involves changing user behavior, motivating action,
designing incentive structures, or collecting/displaying signals that shape how users
evaluate each other or the product. Ratings and reviews are easy to miss — if users
can rate, review, or endorse anything, this role is required.

---

### `@legal_compliance_advisor`

**Include when:**
- Financial transactions or money handling
- Health data (HIPAA, medical records)
- Children's data (COPPA)
- Voting, elections, or democratic processes
- Insurance, lending, credit
- Data privacy (GDPR, CCPA) — especially if international
- Content moderation policies
- AI/ML fairness and bias considerations
- **Intellectual property risk** — product uses existing IP, franchises, characters, trademarks, or branded concepts (fan games, spin-offs, derivative works, parodies); product could infringe on existing trademarks or copyrights; licensing agreements required; DMCA/fair-use questions
- Open-source licensing decisions that affect commercial use

**Skip when:**
- Internal tools with no PII
- Static marketing sites
- Open-source developer tools (unless licensing questions arise)

**Strength indicator:** The domain has named regulations, the feature handles
personally identifiable information (PII) or financial data, OR the brief references
an existing branded product, franchise, character, or creative work that the team
doesn't own.

---

### `@domain_expert`

**This is a meta-role** — it adapts to the detected `domain`. See `role-personas.md`
for the persona template and example instantiations.

**Include when:**
- Domain requires specialized knowledge that none of the core roles possess
- Project involves industry-specific regulations, standards, certifications, or workflows
- Getting the domain wrong has serious consequences (health, finance, safety-critical, legal)
- The user's brief contains domain-specific terminology or references industry standards

**Skip when:**
- Domain is generic tech (`saas`, `social`, `marketplace`) — the core team already understands these
- Another role already covers the domain concern (e.g., `@legal_compliance_advisor` for regulatory questions, `@finance_manager` for pricing — but note: `@domain_expert` brings *industry knowledge*, not just the function)
- The feature is purely technical with no domain-specific constraints (infrastructure, developer tooling)

**Strength indicator:** The brief mentions industry-specific terms, standards, certifications,
or practitioner workflows that the core tech team wouldn't naturally know. Examples:
"HL7 FHIR," "GHG Protocol," "FDA 510(k)," "KYC/AML," "GxP," "SCADA."

**Game development special case:** When `domain=game` AND `complexity=high` (e.g., engine
selection, physics integration, animation pipeline, networking for multiplayer), include
`@domain_expert` instantiated as a game development specialist. Game engines, physics
math, asset pipelines, and platform certification are specialized and go beyond the core
team's knowledge. Skip only for small casual-game features where core team suffices.

**Differentiation from other roles:**
- `@legal_compliance_advisor` handles *legal risk and regulatory compliance* — the "can we do this?" question
- `@domain_expert` handles *industry knowledge and practitioner needs* — the "how does this domain actually work?" question
- Both may be present simultaneously. They complement, not duplicate.

**Domain Expert Depth Scoring.** Not all domain experts are the same. Pick the depth
that matches the brief so you don't over- or under-invest:

| Depth | When to use | Contribution style | Risk if wrong depth |
|-------|-------------|--------------------|--------------------|
| **Shallow (translator)** | Mainstream domain (fintech payments, SaaS health tracking, e-commerce logistics) where industry vocabulary is the main gap; `complexity` = `low` or `medium`; scope is `discussion` or `planning` | Translates industry terms, flags 2–3 practitioner norms, points to relevant standards by name — doesn't dive into implementation specifics | Cheap but can miss edge cases if the domain is actually specialized |
| **Deep (peer)** | Specialized or safety-critical domain (clinical trials, medical devices, biotech pipelines, industrial controls, aviation, nuclear); `is_regulated` = `true` with named frameworks (21 CFR Part 11, ISO 13485, DO-178C, GxP); scope is `building`; `complexity` = `high` | Engages as a technical peer with the architect — debates data models, regulatory edge cases, amendment-handling, validation strategy, standards interpretation | Expensive (uses more discussion bandwidth) but necessary when getting specifics wrong has material consequences |

**How to choose:** if the brief contains a named regulation, standard, or certification
(e.g., "21 CFR Part 11," "HL7 FHIR," "CDISC"), default to **deep**. If the domain is
named but no standard is referenced, default to **shallow** unless complexity is high.
State the depth in the Team Assembly rationale: "@domain_expert (clinical trials, deep
— CDISC and 21 CFR Part 11 in scope)" vs. "@domain_expert (fintech, shallow — standard
payments knowledge sufficient)."

---

### `@i18n_specialist`

**Include when:**
- Product targets multiple countries or language groups
- UI contains user-facing text that will be translated
- Cultural adaptation is needed (not just translation)
- Right-to-left (RTL) language support required
- Date, currency, or number formatting varies by locale

**Skip when:**
- Single-market English-only product
- Backend services with no user-facing strings
- Early MVP explicitly scoped to one market

**Strength indicator:** The brief mentions "international," "localization,"
"multi-language," specific country names, or the product already serves
multiple markets.

---

## Tier 3 — Optional Roles

### `@data_scientist`

**Include when:**
- ML model design, training, or deployment
- Analytics pipeline architecture
- Recommendation engines
- A/B test design with statistical rigor
- Large-scale data processing decisions
- Feature engineering or data modeling

**Skip when:**
- Simple analytics (use `@product_analyst` instead)
- Dashboard display (frontend work)
- Standard CRUD with basic reporting

---

### `@devops_engineer`

**Include when:**
- Infrastructure architecture decisions (cloud provider, container orchestration)
- CI/CD pipeline design or overhaul
- Deployment strategy (blue-green, canary, feature flags)
- Cost optimization for cloud resources
- Multi-environment setup (staging, production, preview)
- Database migration strategy

**Skip when:**
- Scope is `discussion` or `planning` only
- Small feature within existing infrastructure
- Local development setup

---

### `@security_specialist`

**Include when:**
- Authentication or authorization system design
- Payment processing
- PII storage or handling
- API security (rate limiting, input validation, CORS)
- Third-party integrations with sensitive data
- SOC 2, ISO 27001, or other compliance requirements
- Any feature accessible by unauthenticated users

**Skip when:**
- Internal admin tools behind VPN
- Read-only public data
- Scope is pure UI/design discussion

---

### `@qa_engineer`

**Include when:**
- Scope is `building` or `review`
- Complex business logic with many edge cases
- Integration with external services
- User-facing flows with multiple paths
- Regression risk from changes to core systems
- Pre-launch quality gate

**Skip when:**
- Scope is `discussion` or early `planning`
- Trivial changes (copy updates, color changes)
- Spike or prototype (testing comes later)

---

### `@technical_writer`

**Include when:**
- Developer-facing product (API, SDK, CLI)
- Complex onboarding flow that needs documentation
- Platform or infrastructure project
- Open-source project
- Migration guides needed

**Skip when:**
- Consumer-facing app (use `@senior_copywriter` for UX writing)
- Internal tool with small user base
- Early ideation phase

---

### `@marketing_manager`

**Include when:**
- Go-to-market planning
- Launch strategy
- Growth-stage product looking for new channels
- Competitive positioning decisions
- Pricing and packaging

**Skip when:**
- Pre-MVP ideation
- Internal tools
- Backend/infrastructure work
- The brief is purely technical

---

### `@sales_manager`

**Include when:**
- B2B product with enterprise sales motion
- Pricing strategy for sales-led growth
- Feature prioritization driven by sales pipeline
- Integration or partnership discussions
- Customer objection handling

**Skip when:**
- B2C or self-serve product
- Pre-revenue stage
- Technical implementation focus

---

### `@customer_support_lead`

**Include when:**
- Designing support workflows or ticketing
- Feature that will generate user questions
- Error handling and user recovery flows
- Knowledge base or help center planning
- Post-launch retrospective

**Skip when:**
- Pre-launch (no users yet to support)
- Backend changes with no user impact
- Developer tools with community support model

---

### `@finance_manager`

**Include when:**
- Pricing model design
- Unit economics analysis
- Budget allocation for a project
- Revenue impact assessment
- Subscription or billing system design
- Cost optimization decisions

**Skip when:**
- Feature with no pricing impact
- Open-source or free-tier only
- Technical architecture discussion

---

### `@project_manager`

**Include when:**
- High complexity with multiple workstreams
- Cross-team coordination needed
- Tight deadline with dependencies
- Resource allocation decisions
- Risk management for critical launches

**Skip when:**
- Small team working on a single feature
- Early brainstorming (too early for project management)
- Scope is `discussion` only

---

### `@product_analyst`

**Include when:**
- Defining success metrics for a feature
- A/B test planning
- User funnel analysis
- Feature adoption tracking
- Data-informed prioritization

**Skip when:**
- Pre-launch with no data yet
- Pure technical infrastructure
- The team already has a `@data_scientist` covering analytics

---

### `@community_manager`

**Include when:**
- Social platform or marketplace
- User-generated content features
- Community-driven growth model
- Moderation policy design
- Ambassador or referral programs

**Skip when:**
- B2B enterprise product
- Pre-launch (build the product first)
- Internal tools

---

### `@content_strategist`

**Include when:**
- Content-led growth strategy
- SEO-driven product
- Editorial calendar or content pipeline
- Blog, help center, or resource hub planning
- Content taxonomy or information architecture

**Skip when:**
- Product with no content component
- Pure SaaS with minimal content
- Technical implementation focus

---

### `@accessibility_specialist`

**Include when:**
- Public-facing product (especially government, education, healthcare)
- Regulated domain requiring WCAG compliance
- Design system or component library development
- Inclusive design is a stated value
- Product targeting diverse or elderly user base

**Skip when:**
- Internal tool with known user base
- Backend/API only
- Early spike or prototype (but plan for it later)

---

### `@developmental_psychologist`

**Include when:**
- `involves_minors` = true
- Product designed for or substantially used by children (<13) or teens (13–17)
- `domain` = education (k-12)
- Features involve parental controls, age verification, or child safety
- UX patterns need age-appropriate calibration

**Skip when:**
- Audience is adult-only (defer to `@lead_behavioral_scientist`)
- Minors are incidental users, not the primary audience

---

### `@clinical_psychologist`

**Include when:**
- `domain` = mental_health, wellness, therapy, or counseling
- Product handles emotional or crisis-adjacent content (journaling with self-harm signals, mood tracking, etc.)
- Features involve therapeutic framing, psychoeducation, or diagnostic concepts
- Language choices could pathologize or destigmatize

**Skip when:**
- General wellness or lifestyle product with no clinical framing
- Fitness or habit-tracking without mental health angle

---

### `@clinical_researcher`

**Include when:**
- `domain` = health or biotech AND product makes efficacy or health-outcome claims
- Marketing or product copy references studies or evidence
- Regulatory submissions involve clinical data (FDA, EMA, etc.)
- Feature design depends on what's evidence-backed vs. speculative

**Skip when:**
- Health-adjacent product with no efficacy claims (e.g., habit tracker without therapeutic claims)
- Pre-MVP where evidence threshold can't be met yet

---

### `@game_designer`

**Include when:**
- `domain` = game or gamification
- Product has game loops, progression systems, or meaningful-play mechanics
- Monetization decisions touch free-to-play, loot, or reward systems
- Difficulty tuning, retention curves, or player agency are in scope

**Skip when:**
- Non-game product with light gamification (badges, streaks — `@lead_behavioral_scientist` is enough)
- Pure utility software

---

### `@narrative_designer`

**Include when:**
- Product has story, characters, or world-building as core content
- `domain` = game, entertainment, media, or interactive fiction
- Features involve character arcs, branching dialogue, or emergent storytelling
- Onboarding or tutorial relies on narrative framing

**Skip when:**
- Microcopy and brand voice work — that's `@senior_copywriter`
- Pure utility software

---

### `@sound_designer`

**Include when:**
- Product has significant audio (music app, podcast platform, voice assistant, audiobook, game)
- Voice UX or spatial audio design decisions
- Audio accessibility (captions, audio descriptions, hearing-aid support)
- Sonic identity or audio branding matters

**Skip when:**
- Audio is incidental (UI sound effects only)
- Silent-by-default products

---

### `@vc_partner`

**Include when:**
- Project is preparing for fundraising (seed, Series A/B/C) or currently in conversations with investors
- Pitch deck review or readiness assessment
- Business model stress-testing from investor lens (TAM, moat, defensibility, unit economics at scale)
- Term sheet discussions or deal-structure questions
- User asks "is this VC-fundable?" or "what would an investor say?"

**Skip when:**
- Bootstrapped or lifestyle business with no fundraising intent
- Internal product decisions disconnected from venture narrative
- Pure execution work where investor perspective doesn't apply

**Partner well with:** `@startup_strategist` (productive disagreement on proof vs. promise), `@finance_manager` (unit economics), `@brand_strategist` (category positioning).

---

### `@startup_strategist`

**Include when:**
- Business model canvas construction or review
- Pitch deck construction (not just review)
- Go-to-market strategy for early-stage product
- Startup positioning and category definition
- Founder-narrative work (vision, wedge, 18-month arc)
- Strategic planning at pre-Series-B stage

**Skip when:**
- Mature company with established go-to-market
- Feature-level decisions disconnected from company strategy
- Work where operational detail matters more than narrative framing

**Partner well with:** `@vc_partner` (productive disagreement), `@brand_strategist` (positioning), `@marketing_manager` (GTM execution), `@senior_copywriter` (deck copy).

---

### `@ai_safety_specialist`

**Include when:**
- AI/ML product with alignment, misuse, or fairness concerns
- Regulatory AI context (EU AI Act, FTC AI guidance, sector-specific AI rules)
- Pre-launch eval or red-team design
- Misuse-modeling exercises (jailbreak, prompt injection, capability misuse)
- Model audit or post-incident review

**Skip when:**
- Non-AI product (no model in the loop)
- Low-stakes AI usage (e.g., autocomplete in an internal tool with no PII)
- Pre-MVP exploratory work where evals are premature

**Partner well with:** `@ai_system_architect` (productive disagreement on capabilities vs. guardrails), `@legal_compliance_advisor` (regulatory specifics), `@clinical_psychologist` or `@developmental_psychologist` (when AI touches mental health or minors).

---

### `@developer_advocate`

**Include when:**
- `audience` = `developer` and `stage` >= `growth`
- SDK, public API, CLI, or library design decisions
- Community sentiment matters (Discord/Slack/GitHub issues)
- Conference, content, or educational strategy for developer audience
- Onboarding or first-call experience design for developers

**Skip when:**
- Internal tools with a known small dev audience
- Pre-launch product without external developers
- Pure end-user product (no API surface)

**Partner well with:** `@technical_writer` (docs and onboarding), `@senior_backend_engineer` (API shape decisions), `@community_manager` (community engagement), `@content_strategist` (educational content).

---

### `@ux_researcher`

**Include when:**
- Qualitative user research is needed (interviews, usability testing, ethnography)
- New product or major pivot — user needs are unclear
- Feature decisions where intuition disagrees with available data
- Mental-model validation (does the user understand what we built?)
- Before-and-after research for major redesigns

**Skip when:**
- Decisions clearly answered by existing quantitative data
- Trivial features where research overhead exceeds value
- Spike or prototype where user testing comes later

**Partner well with:** `@senior_product_designer` (research → design), `@product_analyst` (qualitative + quantitative triangulation), `@lead_behavioral_scientist` (decision science context), `@developmental_psychologist` (when audience includes minors).

---

### `@ai_system_architect`

**Include when:**
- Product is LLM-powered (chat, agents, RAG, copilots, content generation)
- Agent orchestration design (single agent vs. multi-agent, sub-agent patterns)
- RAG pipeline design (chunking, retrieval, reranking, context assembly)
- Eval pipeline design (golden sets, LLM-as-judge, human eval)
- Prompt versioning, model routing, or multi-model strategies
- Context management at scale (large context windows, conversation memory, summarization)

**Skip when:**
- Traditional non-AI software (no model in the loop)
- AI usage limited to a third-party API call with no architectural decisions
- Decisions better served by `@data_scientist` (traditional ML) or `@senior_software_architect` (general systems)

**Partner well with:** `@ai_safety_specialist` (productive disagreement on capabilities vs. guardrails), `@senior_software_architect` (LLM patterns vs. traditional patterns), `@data_scientist` (when traditional ML may be the right answer instead), `@finance_manager` (model API costs at scale).

---

### `@dataviz_engineer`

**Include when:**
- Any product surface displays data — dashboards, analytics, reports, metrics pages, admin consoles
- Charts, graphs, or data visualizations appear in the product, slide deck, or documentation
- `is_data_intensive` = true (recommendation/analytics/ML products almost always need this role)
- A data story is being told (blog post with charts, pitch deck with metrics, product announcement with trends)
- User mentions a specific library by name (d3, Observable Plot, Vega-Lite, visx, ECharts, Recharts, Chart.js)
- User mentions "chart", "graph", "visualization", "dashboard", "metrics display", "data story", "report"
- A team-composer deliverable will include charts or data visuals (even trivially — this role sets the bar)

**Trigger aggressively.** If data will be shown to humans, include this role by default. The marginal cost is small (2–3 sentences in the discussion round); the cost of skipping it is charts that look fine but mislead, or decoration where information was needed.

**Skip when:**
- The only "data" is a single metric, counter, or status indicator with no comparison or trend — a number-in-a-box doesn't need encoding expertise
- Pure CRUD tables where the rows *are* the answer (no sparklines, no conditional bars, no cell-level encoding). If the table needs per-cell visual encoding, bring dataviz back in.
- Progress bars, status pills, traffic-light indicators, or badges where the encoding is trivially determined by the value
- Text-only reports, logs, audit trails, timelines of events, or changelogs — nothing to encode visually
- Admin consoles that are filter + search + table with no charts (aka most internal tools)
- Form fields that display a number (account balance, count) without comparison or time-series context
- Pure infrastructure, backend, auth, or devops work with no user-facing data surface
- Copywriting-only, brand-voice-only, or naming-only work
- Early strategic brainstorming where no visuals will be produced
- Team is already at the size cap (≥12) AND a data-adjacent role (`@data_scientist`, `@product_analyst`) is present AND the charts are standard/trivial — in that case, those roles can own encoding decisions with `@senior_frontend_engineer`

**Rule of thumb:** If there's a meaningful encoding choice (what chart type? what axes? categorical vs. sequential color? small multiples vs. overlay?), include dataviz. If the only question is "show the number" or "show the rows," skip.

**Strength indicator:** The brief mentions chart/graph/visualization, a slide deck with real charts (not just tables), a dashboard *with charts* (not a CRUD console), trend or comparison language ("change over time," "versus last quarter," "by segment"), or any chart library by name.

**Partner well with:** `@data_scientist`, `@clinical_researcher`, `@product_analyst` (analysis → visualization pipeline — they define the finding, dataviz designs the chart), `@senior_frontend_engineer` (implementation partner — library and bundle-size negotiation), `@senior_product_designer` (visual language integration; brand palette validation for categorical encoding), `@accessibility_specialist` (pattern-encoding, colorblind safety, keyboard chart navigation, screen-reader-resolvable alternatives).

**Persona discipline:** Every chart recommendation must state: (1) the question the chart answers, (2) the primary encoding and why (referencing perceptual task), (3) the library choice and rationale, (4) the accessibility plan, (5) print/screenshot behavior. Charts without this justification are decoration, not information.

---

### `@naming_specialist`

**Include when:**
- Explicit product, company, or feature naming work (new name or rename)
- Naming brainstorm sessions
- Domain-name ideation or .com/.io/.ai availability strategy
- Name that needs cross-language phonetic vetting (does it mean something embarrassing in another language?)
- User mentions specific naming techniques (embedded words, homophones, alphanumeric, portmanteau, domain hacking)

**Skip when:**
- Naming is not part of the brief (even if the product doesn't have a name yet — the user didn't ask)
- Tagline or copy work without naming (that's `@senior_copywriter` or `@humorist`)
- Brand strategy or positioning work without a naming component (that's `@brand_strategist`)
- Internal tools or codenames where naming craft is irrelevant

**Partner well with:** `@humorist` (stress-tests candidates for unintended meanings and cringe — different creative muscle from generative naming), `@brand_strategist` (evaluates positioning fit of name candidates), `@legal_compliance_advisor` (trademark viability check), `@i18n_specialist` (cross-language validation at scale when naming_specialist's pre-screen flags risks).

**Persona discipline:** Every name candidate must include: technique used, embedded meaning, pronunciation guide, and at least one known risk. Names without annotations are noise. The collaboration pipeline is: naming_specialist generates → humorist stress-tests → brand_strategist evaluates fit → legal checks trademark.

---

### `@humorist`

**Include when:**
- Brand voice, tone, or copy review for consumer/social products
- Product naming, taglines, or feature-naming work
- Cultural localization (catching embarrassing or unintended meanings in other languages)
- Creative brainstorming when the team is stuck in earnest/corporate thinking
- Consumer-facing touchpoints where warmth matters (welcome flows, onboarding, empty states, error messages)
- User explicitly asks for a playful / lateral / รั่ว lens

**Skip when:**
- B2B enterprise, legal, medical, or safety-critical copy (gravitas required)
- Crisis or incident communication
- Mental-health-adjacent contexts
- Internal docs, runbooks, or technical documentation where clarity dominates
- Early-stage strategic decisions (before the wording phase)

**Partner well with:** `@senior_copywriter` (humorist proposes lateral alternatives; copywriter enforces brand voice consistency — productive collaboration, not competition), `@brand_strategist` (warmth/personality as part of positioning), `@legal_compliance_advisor` (cringe-catching also catches trademark and regulated-claim risks), `@i18n_specialist` (cross-language cringe detection).

**Persona discipline:** This role's value depends on always proposing *better* alternatives, not just mocking existing copy. Format: "Here's what this accidentally says / here's a sharper version that lands." Without this discipline, the role becomes noise in the discussion.

---

### `@design_engineer`

Design engineer in the Emil Kowalski tradition (Sonner, Vaul) — lives at the
seam between designer intent and frontend implementation, where a component's
*feel* is decided. Three convictions: (1) taste is trained, not innate — cite
specific patterns from top-tier interfaces; (2) unseen details compound — most
users never consciously notice them, which is the point; (3) beauty is leverage —
good defaults + good motion are real differentiators, not polish-for-polish.

**Include when:**
- `has_ui` = `true` AND motion or micro-interactions are load-bearing for the feature (transitions, enter/exit animations, focus moves, state changes)
- Component-library or design-system work, especially components whose value *is* their feel: toasts, drawers, modals, popovers, dropdowns, tooltips, command menus, combobox, switches, sheets, context menus
- Review of an existing UI surface for polish, craft, or "does this feel right?" questions
- User mentions animation, motion, easing, duration, transition, spring, or references libraries like Framer Motion, Motion One, GSAP, React Spring
- Redesign or refresh of an interaction-dense product surface where the *how* of the interaction matters as much as the *what*

**Skip when:**
- `has_ui` = `false` (backend, data, infra work)
- Pure data-dense surfaces where motion is secondary (static dashboards, data tables, admin consoles, forms)
- Early strategic brainstorming — before interaction design exists to polish
- Trivial copy or content-only updates
- Infrastructure, DevOps, or auth work

**Strength indicator:** The brief mentions animation, motion, "feel," polish, micro-interactions, a named motion library, or a component type where motion is load-bearing (toast, drawer, modal, popover, dropdown, command menu, sheet).

**Differentiation from adjacent roles:**
- `@senior_product_designer` owns *intent* and information architecture — "this interaction should feel responsive"
- `@senior_frontend_engineer` owns *mechanics* and performance — "use transform and `will-change` to avoid layout shift"
- `@design_engineer` owns *craft* — "`ease-out` on entry with `cubic-bezier(0.23, 1, 0.32, 1)`, 220ms, transform-origin at the trigger, interruptible"

The three voices compound. None replaces the others — that's why `@design_engineer` earns its own seat.

**Partner well with:** `@senior_product_designer` (design-engineer takes over where "feels responsive" meets "how exactly"), `@senior_frontend_engineer` (implementation partner — design-engineer owns the motion encoding, frontend owns render performance and framework integration), `@accessibility_specialist` (reduced-motion fallbacks, focus management during animation, non-motion state encoding), `@senior_copywriter` (microcopy in micro-interactions).

**Grounding:** For the full reference, install the `emilkowalski/skill` plugin. This role invokes that philosophy even when the plugin isn't loaded in-context — the persona carries the core heuristics standalone.

---

### `@dharma_teacher`

**Include when:**
- First-principles questions about whether to build a product, or how to frame it honestly
- AI or social products that shape attention, engagement, or craving
- Engagement-maximization features being designed (streaks, infinite scroll, intermittent reinforcement)
- Mental-health-adjacent or wellness products (long time-horizon impact on the user's mind matters)
- Pivots or product framing where "as it is" vs. "as we wish it to be" matters
- User explicitly asks for a contemplative / wisdom / suchness (tathatā) lens

**Skip when:**
- Pure infrastructure or developer tooling with no end-user attention impact
- Time-pressured execution work where the strategic intent has already been decided
- Internal tools where the long-term human-tool relationship is irrelevant (e.g., one-shot scripts)
- The team is small (≤4) and the question is purely tactical

**Partner well with:** `@lead_behavioral_scientist` (productive tension on time-horizon — moment-of-choice ethics vs. years-of-use conditioning), `@senior_product_manager` (productive tension on metrics vs. wellbeing), `@ai_safety_specialist` (when AI products specifically shape attention/craving), `@clinical_psychologist` (when the product touches mental health — defer to clinical for crisis-adjacent decisions).

**Persona discipline:** This role's value depends on always proposing dharma-informed alternatives, not just diagnosing. If used for moralizing without proposals, the role is misused. The healthy use is: "Here's what this conditions in users — and here's a design alternative that serves the user's genuine interest."

---

## Signal-to-Role Quick Reference

| Signal | Roles it Triggers |
|--------|-------------------|
| `is_regulated` = true | `@legal_compliance_advisor`, `@security_specialist`, `@accessibility_specialist` |
| Brief references existing IP/franchise/character | `@legal_compliance_advisor` (IP/copyright risk), `@brand_strategist` |
| `is_data_intensive` = true | `@data_scientist`, `@product_analyst`, `@dataviz_engineer` (if any output includes charts) |
| Product has charts/graphs/visualizations (not just tables or counters) | `@dataviz_engineer`, `@senior_frontend_engineer` (implementation), `@accessibility_specialist` (a11y), `@product_analyst` (metrics definition) |
| Dashboard with real chart work (trend lines, comparative bars, small multiples) | `@dataviz_engineer`, `@senior_frontend_engineer`, `@product_analyst` |
| Dashboard is CRUD + filter + table only (no charts) | Skip `@dataviz_engineer` — `@senior_frontend_engineer` + `@senior_product_designer` own table UX |
| Slide deck with real charts / data story | `@dataviz_engineer`, `@senior_copywriter` (annotation copy), `@senior_product_designer` (visual language) |
| User mentions d3 / Observable Plot / Vega-Lite / visx / ECharts / Recharts / Chart.js | `@dataviz_engineer` (primary), `@senior_frontend_engineer` (implementation partner) |
| Trend / comparison / segmentation language ("over time," "vs. last quarter," "by segment") | `@dataviz_engineer` |
| `is_international` = true | `@i18n_specialist` |
| `has_brand_impact` = true | `@brand_strategist` |
| `involves_behavior_design` = true | `@lead_behavioral_scientist` |
| Rating / review / feedback / social-proof surface | `@lead_behavioral_scientist`, `@ux_researcher` (if launching new), `@community_manager` (if social) |
| Re-engagement / notification timing / dormant-user revival | `@lead_behavioral_scientist`, `@product_analyst`, `@marketing_manager` |
| `involves_minors` = true | `@developmental_psychologist` (replaces `@lead_behavioral_scientist` for UX decisions) |
| `domain` = specialized (non-generic) | `@domain_expert` (adapts to detected domain) |
| `domain` = fintech | `@domain_expert (fintech)`, `@legal_compliance_advisor`, `@security_specialist`, `@finance_manager` |
| `domain` = health | `@domain_expert (health)`, `@legal_compliance_advisor`, `@security_specialist`, `@accessibility_specialist` |
| `domain` = mental_health/wellness/therapy | `@clinical_psychologist`, `@legal_compliance_advisor` |
| `domain` = health/biotech + evidence claims | `@clinical_researcher` |
| `domain` = game/gamification | `@game_designer`, `@narrative_designer` (if story-heavy), `@domain_expert (game dev)` if `complexity=high` |
| `domain` = entertainment/media | `@narrative_designer`, `@sound_designer` (if audio-heavy) |
| `domain` = biotech/climate/manufacturing/etc. | `@domain_expert ({domain})` |
| `domain` = social/marketplace | `@lead_behavioral_scientist`, `@community_manager` (no domain expert — core team sufficient) |
| `domain` = saas | No additional roles triggered (core team sufficient) |
| `audience` = developer | `@technical_writer` |
| `audience` = b2b | `@sales_manager` |
| `stage` = growth/mature | `@marketing_manager`, `@customer_support_lead`, `@product_analyst` |
| `complexity` = high | `@devops_engineer`, `@project_manager`, `@qa_engineer` |
| `scope` = building | `@devops_engineer`, `@qa_engineer` |
| `scope` = review | `@qa_engineer`, `@security_specialist` |
| Product has significant audio | `@sound_designer` |
| Fundraising context (VC, angel, seed, Series A/B/C) | `@vc_partner`, `@startup_strategist` |
| Pitch deck review (stress test) | `@vc_partner` (primary), `@startup_strategist` (responds) |
| Pitch deck construction | `@startup_strategist` (primary), `@vc_partner` (critique) |
| Business model canvas work | `@startup_strategist`, `@finance_manager` |
| Go-to-market for early-stage startup | `@startup_strategist`, `@marketing_manager`, `@brand_strategist` |
| AI/ML product with safety/alignment concerns | `@ai_safety_specialist`, `@ai_system_architect`, `@legal_compliance_advisor` |
| LLM-powered product / agents / RAG / evals | `@ai_system_architect`, `@ai_safety_specialist` (if regulated or high-stakes) |
| Developer-facing product (`audience` = `developer`) at growth stage | `@developer_advocate`, `@technical_writer` |
| Qualitative user research needed | `@ux_researcher`, `@senior_product_designer` |
| First-principles "should we build this?" / honest framing / suchness lens (tathatā) | `@dharma_teacher` |
| AI/social product designing for engagement or attention | `@dharma_teacher`, `@lead_behavioral_scientist` |
| Explicit naming work (product/company/feature naming, rename, domain ideation) | `@naming_specialist`, `@humorist` (stress-test), `@brand_strategist` (fit), `@legal_compliance_advisor` (trademark) |
| Consumer/social brand voice, copy review, product naming, taglines | `@humorist`, `@senior_copywriter`, `@brand_strategist` |
| Cultural localization cringe check (accidental meanings across languages) | `@humorist`, `@i18n_specialist` |
| `has_ui` = true AND motion/animation is central to the feature | `@design_engineer`, `@senior_frontend_engineer`, `@senior_product_designer` |
| Component-library / design-system polish (toasts, drawers, modals, popovers, dropdowns, tooltips, command menus) | `@design_engineer`, `@senior_product_designer`, `@accessibility_specialist` |
| "Does this feel right?" review of an existing UI surface | `@design_engineer` |
| User mentions Framer Motion / Motion One / GSAP / React Spring / easing / spring physics | `@design_engineer`, `@senior_frontend_engineer` |
