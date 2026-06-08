---
name: gamification-fit
description: >
  Analyze a product, idea, or resource set (source code, docs, URLs, analytics
  exports) against a stated goal and produce a restraint-first report on where
  gamification genuinely fits — and, more prominently, where it deliberately does
  NOT. The superpower is discrimination, not idea volume: most features should not
  be gamified, and a tool that gamifies everything is harmful (dark patterns,
  noise). Anchored on Self-Determination Theory; steers away from default
  Points/Badges/Leaderboards; refuses manipulation outright via a non-droppable
  ethics veto. Produces an editable Markdown artifact plus a self-contained HTML
  report (default paths `docs/gamification-fit/gamification-fit.md` and
  `docs/gamification-fit/gamification-fit.html`). The report is a forward-looking,
  hand-off-ready brief a developer or agent builds from.

  Use whenever the user asks to "gamify my product", "where should I add
  gamification", "should I gamify X", "suggest game mechanics for", "make this more
  engaging with game mechanics", "gamification ideas for my app", or points the
  skill at a codebase / docs / URL + a goal and asks where play would help.

  Requires TWO inputs: the resources AND a goal/metric. Code reveals what features
  exist, not what behavior to reinforce — gamification only makes sense relative to
  a target behavior. If the goal is missing, the skill infers candidates and
  confirms, or asks a 3-question intake.

  Does NOT trigger for: reviewing the UX of an EXISTING AI feature (use
  `ai-ux-review`); designing an actual game (this gamifies non-game products, it
  does not design games — use `team-composer` with `@game_designer`); implementing
  the mechanics or writing feature code (this skill suggests, then hands off);
  business-model / lean-canvas work (use `validation-canvas`); building a
  dark-pattern / engagement-maximization growth hack (the skill refuses these);
  general retention strategy without a product or resource set to read (use
  `team-composer`).
---

# Gamification Fit

Analyze a product, idea, or resource set against a stated goal and report **where
gamification genuinely fits — and, far more often, where it deliberately does
not.** Each candidate feature is run through a *fit-test*, not a template: the
value of this skill is whether it correctly **withholds** a mechanic, not whether
it generates a long list.

The job is **discrimination**. Most features should not be gamified. A tool that
gamifies everything manufactures dark patterns and noise — it is actively harmful.
The most valuable section of every report is **"deliberately NOT gamified, and
why."** Treat restraint as the deliverable.

This is **not** a reviewer of gamification you already have, and **not** a
generator that decorates every action with points. It ingests resources + a goal,
finds the few places play would honestly serve the user, refuses the rest, and
hands a buildable brief to a developer or agent.

> **Anchor — Self-Determination Theory (SDT).** Good gamification *supports*
> intrinsic motivation (autonomy, competence, relatedness); dark patterns *hijack*
> it. Default to intrinsic-supporting mechanics. The lazy LLM answer —
> Points/Badges/Leaderboards (PBL) — is usually the worst, most manipulation-prone
> choice; steer away from it unless explicitly justified.

## What this skill produces

Always produced under the resolved output root (default `docs/gamification-fit/`):

1. **`gamification-fit.md`** — canonical, editable Markdown. Sections in order:
   `## Scorecard` (N analyzed / Y recommended / Z refused), `## Recommended
   mechanics` (few, high-conviction cards), `## Deliberately NOT gamified, and why`
   (prominent, usually the majority), `## Cross-feature checks`, `## Hand-off`.
   Headings are load-bearing.
2. **`gamification-fit.html`** — single self-contained HTML file rendering the
   scorecard header + a variable-length card grid (recommended vs. refused) with
   collapsible provenance. Opens offline, prints cleanly to PDF, zero network
   dependencies.

The HTML is the visual primary; the Markdown is the source of truth the builder
edits and hands off.

## What this skill is NOT

- **Not a generator.** It does not gamify everything. Restraint is the point; the
  refusals are the most important output.
- **Not a reviewer of existing gamification.** It suggests where to *add* play. To
  audit an existing AI feature's UX, use `ai-ux-review`.
- **Not a game-design tool.** It gamifies *non-game* products. Designing an actual
  game is `team-composer` with `@game_designer`.
- **Not an implementer.** It prescribes mechanics, motion specs, and microcopy —
  it does not write feature code or run experiments. Hand off the report.
- **Not analytics integration.** It *reads provided* analytics exports; it does not
  connect to live PostHog/GA. Absent analytics, the "is this action repeated?"
  question is confidence-tiered, never asserted.
- **Not a substitute for craft.** Good gamification is textural (easing, timing, a
  fill that feels *earned*). A static report can prescribe motion specs and
  references; it cannot deliver the feel. The report says so plainly.
- **Not regulatory advice.** Regulated / risk-bearing flows are *refused*, not
  advised (see the ethics veto).

> **Influences.** This skill draws on general ideas from Self-Determination Theory
> (Deci & Ryan), the Octalysis framework (Yu-kai Chou), the Fogg Behavior Model
> (BJ Fogg), and *Hooked* (Nir Eyal — used as much for what to *refuse* as to
> apply). It is **not a derivative work** under copyright law: it uses general
> concepts (ideas / facts, not protected expression) and authors its own fit-test,
> mechanic taxonomy, and anti-pattern prose from first principles. No framework's
> protected expression, diagrams, or pattern names are reproduced. See `README.md`
> for full attribution.

---

## Phase 0: Intake (RUN FIRST, BEFORE ANY ANALYSIS)

**Goal:** establish what's being analyzed, where output goes, and what context
already exists — so the analysis adapts and never re-elicits what an upstream
artifact already answers.

### Step 0.1 — Resolve the output root

Look for these in order; first match wins:

1. **Explicit `output_dir` arg** → use as-is.
2. **`STARTUP_KIT_DOCS_ROOT` env var** → `${STARTUP_KIT_DOCS_ROOT}/gamification-fit/`.
3. **Smart default — `docs/startup-kit/` exists** → `docs/startup-kit/gamification-fit/`.
   Surface: *"Writing to `docs/startup-kit/gamification-fit/` (smart default — kit
   folder exists). Set `STARTUP_KIT_DOCS_ROOT=./docs` for standalone."*
4. **Solo fallback** → `docs/gamification-fit/`.

If a prior `gamification-fit.md` exists at the resolved root, this is an
**update-mode** run — see "Update mode" below.

### Step 0.2 — Scan for adjacent artifacts

Before analyzing, read what already exists — never re-elicit what these answer:

- **`<canvas-root>/validation-canvas.md`** — Key Metrics, the value-prop "aha"
  behavior, and ICP. Best goal source for early-stage products. If present, the
  goal is largely settled — confirm, don't re-ask.
- **`<root>/.gtm/config.yaml`** — the GTM North Star metric. Best goal source for
  post-launch products.
- **`<root>/ai-ux-review.md`** — its trust / feedback / control blocks tell you
  *where* mechanics could honestly live (a feedback affordance is a natural home
  for progress visibility; a trust surface is not a place for a streak).
- **`<brand-root>/DESIGN.md`** — brand tokens for the HTML (`colors.primary` per
  the [Google Labs spec](https://github.com/google-labs-code/design.md); neutral
  fallback otherwise).
- **Provided analytics exports** (CSV/JSON from PostHog/GA/Amplitude/Mixpanel) —
  the only source that *grounds* "is this action actually repeated?". Read
  event/action counts only; **never** read or echo user-level rows or PII.

### Step 0.3 — Pick the ingestion lane + lock the redaction rule

- **SocratiCode MCP present** (`mcp__socraticode__codebase_*`) → index once, then
  query. Best for large / unconventional repos.
- **Absent** → glob/grep fallback over high-signal files. Record which lane ran;
  the report states it.

**Secret- and PII-redaction rule (hard, non-negotiable).** Capture key *names /
presence* only — never values. A `STRIPE_SECRET_KEY` entry is signal that Stripe
is wired; its value must never enter any artifact or log. If a real secret is
encountered, record `<redacted secret present>` and move on. The same applies to
analytics: capture event *names and aggregate counts* only — never user-level
rows, identifiers, or PII.

### Step 0.4 — Confirm the framing in one line

Mirror back before proceeding, so the user can correct you:

> *"Analyzing a SvelteKit habit-tracker for the goal 'users log an entry 4+
> days/week'. Found a validation-canvas — I'll take the goal from its Key Metrics
> and pressure-test it. No analytics export, so repeat-usage is inferred, not
> measured. Stop me if I should reframe."*

### Hard rules for Phase 0

- **Never start analysis without resolving the path.** Files in the wrong folder
  are the most common skill failure.
- **Never re-elicit a goal an upstream artifact already states.** Read it.
- **Never read or echo a secret value or user-level analytics row.** Names and
  aggregates only.

---

## Phase 1: Ingest → feature/action inventory

**Goal:** turn the resource set into a **provenance-pinned inventory** of the
user-facing actions the product affords — the subjects the fit-test will judge.

Read `references/signal-extraction.md` for the broadened source taxonomy (code +
docs/PDF + URL + analytics) and the per-ecosystem extractors. Output of this phase
is an internal signal set, each entry:

```
{ source: "<file:path | url | export>", action: "<the user-facing action>",
  category: "<taxonomy #>", repeatable: <observed|inferred|unknown>,
  data_captured: <yes|no|unknown> }
```

**The provenance gate is absolute: `source == null` → it cannot become a candidate.**
An action with no evidence is not analyzed — it is not a guess.

**Triage, don't enumerate.** A product affords 3 to 40+ actions; you cannot
fit-test 40. Rank by *goal-relevance* (does this action move the stated metric?)
and *repeatability*, and carry the **top candidates** (aim ≤ ~12) into the
fit-test. State how many were found vs. carried — silent truncation reads as full
coverage when it isn't.

---

## Phase 2: Acquire the goal (cascade)

**Two inputs are required: the resources AND a goal/metric.** Gamification only
makes sense relative to a target behavior. Acquire the goal by cascade — stop at
the first that succeeds:

1. **Upstream artifact** — `validation-canvas.md` Key Metrics / aha-behavior, or
   `.gtm/config.yaml` North Star. Confirm it in one line; don't re-ask.
2. **Infer-and-confirm** — from the inventory, infer **2–3 candidate goals, each
   pinned to provenance** (e.g. *"'increase weekly active logging' — inferred from
   the `entries` table + a `streak` column already in schema"*), and ask the user
   to confirm or correct one. Costs one turn; grounds the goal in real evidence.
3. **3-question intake** (fallback when neither exists):
   - What's the **target behavior + metric** you want to move?
   - **Who** is the user (segment)?
   - Is this behavior a **chore** (extrinsically motivated) or **intrinsically
     motivated**? (This sets the mechanic branch in Phase 4.)

Do not proceed past this phase without a confirmed goal — **except** when the
request or goal itself trips a hard veto bar, which is refused immediately (see
Phase 5 "Early refusal").

---

## Phase 3: Fit-test each candidate

**Goal:** for each carried candidate, decide `[FIT]` or `[SKIP — reason]`. Read
`references/fit-test.md` for the full per-feature test. The load-bearing questions:

- Is there a **repeatable** user action? (One-shot actions rarely reward play.)
- Is there **visible progression** worth reinforcing?
- Is there a **goal worth reinforcing** here, tied to the Phase 2 metric?
- Is **intrinsic motivation present or absent**? (Branches Phase 4.)
- Is the underlying **data even captured**? (Can't reward what you can't measure.)
- Is the action **reversible / low-stakes**? (Never gamify high-stakes or
  irreversible decisions.)

A "no" on a load-bearing question → `[SKIP]` with the reason. **Specificity gate:**
a vague candidate ("add points to the dashboard") fails the same way `ai-ux-review`
rejects "we handle errors" — name the action, the metric, and the mechanic, or
it's a skip.

---

## Phase 4: Select mechanics (SDT branch)

For each `[FIT]` candidate, choose mechanics from `references/mechanic-taxonomy.md`
(every entry tagged intrinsic-supporting vs. extrinsic). Branch on the Phase 3
intrinsic read:

- **Intrinsic motivation present** → *support* it: progress visibility, mastery
  feedback, meaningful choice, a satisfying "done" state. **Do NOT bolt on
  extrinsic rewards** — they can *crowd out* the intrinsic motivation that was
  already working.
- **Intrinsic motivation absent** (genuine chores — compliance training, expense
  reports) → extrinsic scaffolding (e.g. a streak) is honest **only if the
  mechanic card names an explicit, checkable sunset condition**. No named sunset →
  the mechanic is refused, not recommended.

**Default away from PBL.** If the chosen mechanic is Points/Badges/Leaderboards,
justify why nothing intrinsic-supporting fits — PBL is the answer of last resort.

---

## Phase 5: Ethics veto (STRUCTURAL — non-droppable)

This is a behavior-change tool; the harm filter is **mandatory and refusal-capable**,
not a cooperative flag. It runs *before* render. A mechanic that trips a bar does
not get softened — it **moves to the refusals section with its reason**, and if a
whole recommendation set is built on a tripped bar, the run **re-derives** rather
than ships soft.

**Early refusal (skips the two-input requirement).** If the *request or goal itself*
trips a hard veto bar — a regulated / risk-bearing / minors flow (bar 5), or an
explicit manipulation / time-on-app-maximization objective — refuse it
**immediately**, before ingestion or the goal cascade. The veto is category- and
goal-triggered; it does not need a completed inventory. State the refusal, decline
the regulated flow (point to qualified review where relevant), and go straight to the
refusals output. Do not demand the resource set first just to refuse something the
request already made unsafe.

Read `references/anti-patterns.md` for the full blocklist. The veto bars (refuse on
any hit):

- **Variable-ratio / "Skinner box"** reward schedules engineered for compulsion.
- **Shame / loss-aversion microcopy** ("Don't lose your streak!", "You'll
  disappoint your team").
- **Manufactured-loss streaks** that punish a single missed day.
- **Social-comparison leaderboards** that demotivate the bottom ~80%.
- **Regulated / risk-bearing flows** — financial risk-taking (Robinhood-style),
  health, safety-critical actions, **anything targeting minors**.
- **Extrinsic mechanic with no named sunset** (from Phase 4).
- **A recommendation with no provenance** (violates the Phase 1 gate).

**The litmus test:** *does this mechanic respect the user's ability to put it
down?* If it only works by making *stopping* feel like loss, it is manipulation
wearing a progress bar — refuse it.

---

## Phase 6: Cross-feature checks

Read the whole recommendation set together and apply:

1. **Cannibalization** — two mechanics competing for the same attention (don't
   recommend a streak *and* a leaderboard *and* a daily quest for the same action).
2. **Attention/notification budget** — sum the total interruption load across all
   recommendations. If the product would become a slot machine, cut the weakest.
   State the budget you assumed.
3. **Goal contradiction** — flag a competitive mechanic (leaderboard) that
   contradicts a stated *collaboration* goal, or a speed mechanic against a stated
   *quality* goal.

---

## Phase 7: Render & ship

**Goal:** produce `gamification-fit.md` + `gamification-fit.html`, save to the
resolved root, present to the user. Read `references/report-contract.md` for the
per-card contract and `templates/gamification-fit.html` for the render.

### Per recommended card

feature → goal it serves → recommended mechanic(s) → **SDT/behavior rationale** →
sample microcopy + tone note → effort tag (CSS-afternoon | websockets-project) →
**"skip if"** condition → anti-pattern warning → confidence (analytics-grounded
`observed` when an export backs the repeat-usage claim, else `inferred`/`unknown`).

### Top-level scorecard

`N analyzed / Y recommended / Z refused`. Z is usually the largest number — that is
the skill working, not failing.

### The "feel" honesty note (render verbatim-equivalent)

> Good gamification is textural craft — easing curves, asymmetric timing, a
> progress fill that feels *earned*. This report prescribes motion specs and
> references; it cannot deliver the feel. Implementation craft is required, and the
> mechanic is only as good as that craft.

### Opinion framing (this is a behavior-change tool)

Every recommendation is an opinion, not a directive. Frame as *"in our opinion"* /
*"the evidence suggests"*. Never claim a mechanic *will* move a metric. Render the
disclaimer block from `references/report-contract.md`.

### Three-line close

End every run with exactly three lines:

1. *"The single highest-conviction place to add play is: …"*
2. *"The most important thing to deliberately NOT gamify is: … — because …"*
3. *"Next step: hand the recommended cards to a developer or agent to build; or run
   `team-composer` / `sub-agent-coordinator` to scope the build."*

Do not replace with a "final deliverable" header or meta-commentary.

---

## Update mode (loop-back)

When `gamification-fit.md` already exists at the resolved root:

1. **Read the existing file first.** Don't overwrite cards the user hasn't asked to
   change.
2. **Confirm scope.** *"Your last report recommended 3 mechanics and refused 9.
   Re-analyze everything, or just re-test the streak you asked about?"*
3. **Apply the same rigor** on changed cards — a glib revision gets the same veto.
4. **Mark changes** with `<!-- updated YYYY-MM-DD: <reason> -->`.

---

## Output Files

```
<root>/gamification-fit.md     Canonical, editable source of truth
<root>/gamification-fit.html   Self-contained visual report (primary deliverable)
```

Where `<root>` resolves per Phase 0.1. No other files — do not scatter drafts.

---

## Quality Checklist

Before presenting, verify:

**Phase 0**
- [ ] Output root resolved; smart-default notice surfaced if it fired
- [ ] Adjacent artifacts scanned (canvas / gtm / ai-ux-review / DESIGN.md / analytics)
- [ ] Ingestion lane recorded; secret/PII redaction rule active
- [ ] Framing confirmed in one line

**Analysis**
- [ ] Inventory is provenance-pinned; no `source == null` candidate carried
- [ ] Candidate count stated (found vs. carried) — no silent truncation
- [ ] Goal confirmed via the cascade; two inputs (resources + goal) present
- [ ] Every candidate is `[FIT]` or `[SKIP — reason]`; specificity gate enforced
- [ ] Mechanics branch correctly on intrinsic present/absent; PBL justified if used
- [ ] Every extrinsic mechanic names a checkable sunset

**Ethics veto (non-droppable)**
- [ ] All veto bars run; tripped mechanics moved to refusals with a reason
- [ ] No regulated/risk/minors flow recommended
- [ ] The "put it down" litmus applied to every recommendation

**Cross-feature**
- [ ] Cannibalization, attention budget, and goal-contradiction checks run

**Render**
- [ ] Scorecard present (N / Y / Z); refusals section prominent
- [ ] Each card has the full contract incl. "skip if" + confidence tier
- [ ] "Feel" honesty note + opinion disclaimer present
- [ ] HTML is a single file, opens offline, prints to PDF, no localStorage / network / PII
- [ ] Response ends with the three-line close

---

## Cross-Skill Integration

| Skill | When to Use |
|-------|-------------|
| `validation-canvas` (our own) | Upstream goal source for early-stage products — Key Metrics + aha-behavior + ICP. If absent and the user wants one, offer to run it before analyzing. |
| `gtm` (our own) | Upstream goal source for post-launch products — the `.gtm/config.yaml` North Star. Note: `gtm`'s event bus is a closed v1 enum; this skill does **not** emit events. |
| `ai-ux-review` (our own) | Adjacent. Its trust/feedback/control blocks tell this skill *where* mechanics could honestly live. Run it first when the product is an AI feature and the UX surface isn't mapped. |
| `team-composer` + `sub-agent-coordinator` (our own) | Downstream. When the recommended cards become a build, hand off to scope and assemble the work. Use `@game_designer` here for designing an actual game (out of this skill's scope). |
| `brand-workshop` / `theme-factory` (ours / Anthropic) | For HTML styling when no `DESIGN.md` exists. Apply after content is finalized. |
| `i18n` (our own) | When the report's microcopy must ship localized. |
| `skill-evaluator` (our own) | To audit this skill's rule-adherence (specificity gate, structural veto, refusal section, three-line close). Run in the **main loop**. |
| `pdf` / `docx` (Anthropic) | When the report ships in a larger packet. The HTML already prints to PDF. |
| `ai-safety-mindset` (Anthropic) | Shared vocabulary (HHH, responsible deployment) for the ethics framing — load alongside; it is vocabulary, not the veto. The veto lives here. |

**Principle:** this skill owns the **gamification-fit recommendation** — where play
honestly serves the goal, and where it must be withheld. It does not validate the
business model (`validation-canvas`), review existing UX (`ai-ux-review`), design a
game (`@game_designer`), or implement the mechanics (hand off).

**Graceful degradation:** if a referenced skill is absent, this skill still ships
both artifacts. Cross-skill chains are enhancements, not requirements. When a goal
source is missing, the skill tells the user and offers the cascade — it does not
hard-gate.

---

## Reference files

- `references/signal-extraction.md` — broadened source taxonomy (code + docs/PDF + URL + analytics); per-ecosystem extractors; provenance + secret/PII redaction
- `references/fit-test.md` — the per-feature fit-test; load-bearing questions; SKIP patterns
- `references/mechanic-taxonomy.md` — mechanics tagged intrinsic vs. extrinsic; the present/absent branch; the named-sunset requirement
- `references/anti-patterns.md` — the ethics-veto blocklist; the "put it down" litmus; regulated/minors refusals
- `references/exemplars.md` — good, often-invisible gamification vs. cheap bolted-on badges; the "feel" honesty caveat
- `references/report-contract.md` — per-card shape; scorecard; refusals section; opinion disclaimer

Read these when the phase calls for them — progressive disclosure, not front-loaded
(see `CLAUDE.md` → "Harness vocabulary").

**Tags:** gamification, behavior-design, self-determination-theory, product, ethics, restraint
