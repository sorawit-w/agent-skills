# team-composer

A Claude Code skill that assembles a virtual team of domain personas, runs a structured 3-round discussion, and hands you back a synthesized conclusion — across tech, healthcare, finance, climate, biotech, and beyond.

## Why this exists

Most "brainstorm this with me" prompts collapse into one voice wearing different hats. The model nods along with itself. You get a list of plausible-sounding bullets, none of them in tension with any of the others, and no real trade-offs surfaced.

The fix isn't "add more roles." It's: pick the *right* roles for the brief, give each one a distinct bias and blind spot, and force them to disagree before synthesizing. The team has to earn its seats, and the discussion has to produce pushback — otherwise the output is theater.

That's what this does.

## What it does

- **Detects the project signals** that matter for role selection — stage, domain, regulated status, minors involved, UI/no-UI, data intensity, international scope, behavior design, brand impact, complexity, scope.
- **Scores and selects roles** across three tiers: 7 Tier-1 core roles (almost always present), frequently-included Tier-2 specialists triggered by signals, and Tier-3 roles that only join on strong signal.
- **Runs a mandatory Gap Detection pass** — 10 questions that catch roles the signal-scoring can miss (IP risk, minors, clinical content, significant audio, narrative/game mechanics, etc.).
- **Enforces a hard team cap of 12** with a risk-weighted pruning rule: Tier 1 is never dropped, and triggered risk-blocking roles (legal, security, developmental-psych, clinical-psych) are non-droppable — "collapse into" and "covered by" are explicitly disallowed workarounds.
- **Runs a 3-round discussion:** Opening Positions → Rebuttals → Synthesis. Every role must contribute substantively or explicitly pass. At least one real rebuttal is required — unanimity means the discussion was too shallow.
- **Commits to a pre-written word budget** before Round 1, with per-contribution caps. Empirically, prose-only ceilings overshoot by 30–50%; a committed budget bites.
- **Produces a conclusion that actually concludes** — recommendation (with dissent named), decisions made, open questions, trade-offs, and numbered/prioritized next steps. Trade-offs section is required even when empty ("No material trade-offs identified").
- **Delegates to sub-agents for deliverable production** (not for the discussion itself) when complexity and scope justify the overhead.
- **Optionally audits high-stakes outputs** in fresh context — to catch the blind spots the assembled team wasn't equipped to see.

## What it doesn't do

- **Pure brand-identity work.** If you want "a logo + tagline + brand strategy brief," use [`brand-workshop`](https://github.com/anthropics/skills) directly. This skill will call that out in its Skill Boundaries section and defer.
- **Hiring advice.** "Who should I hire?" is a different question. The skill will clarify and offer to simulate the team instead.
- **Weight opinions by seniority.** All roles have equal weight. The rebuttal round is what separates strong arguments from weak ones — not the speaker's title.
- **Auto-downgrade sub-agent models.** Sub-agents inherit the orchestrator's model. Silent cost optimization is not a default.
- **Force a phased-launch framing on simple features.** The phased variant only triggers when the team surfaces credibility / regulatory / uncertainty risks *and* a smaller scope materially reduces them.

## When to use it

- You have a project brief that genuinely needs multi-perspective input — a new product, a pivot, a regulated feature, a redesign — and you don't want to pick the roles yourself.
- You want structured disagreement, not nodding consensus. (If every role in your imagined team would agree, the team isn't diverse enough.)
- You're about to plan or build something that touches regulated/children/clinical/financial territory and you want the team to *include the role that can see the risk*, not just discuss it.
- You want a conclusion you can act on — recommendation, dissent, trade-offs, prioritized next steps — not a transcript.

## When not to use it

- **Pure branding deliverable** (logo / tagline / identity). Use `brand-workshop`.
- **Single-asset trivial work** (a tooltip, a subject line, one email). The skill will scale down to 3–4 roles under 400 words, but a dedicated copy/design skill is usually a better fit.
- **You already know exactly which roles you want and why.** The skill respects user-specified role lists, but at that point the value is the discussion structure, not the composition.
- **Hard-real-time pairing.** This is a single-shot assembly + discussion, not a live back-and-forth with the user across every round.

## How it works — 6 phases (+ optional audit)

1. **Detect project signals.** Extract 13 signals from the brief. Ambiguous? Pick the most conservative interpretation, state every assumption in one line, proceed — don't stall. Conflicting signals? Risk-blocking signals win over stage/scope for *inclusion*; scope shapes *depth*, not presence.
2. **Score & select roles.** Tier 1 lock-in (7 roles, minus designer/frontend if `has_ui=false`). Tier 2 triggered by signal matches. Tier 3 only on strong signal.
3. **Assemble & pre-flight.** Emit the Team Assembly table with a "Why Included" rationale per non-core role, followed by a Tier 1 lock-in check and a pre-flight checklist. Small-team framing in the user prompt is NOT a Tier 1 exception — that's a common silent compression the skill guards against.
4. **Gap Detection pass.** 10 mandatory questions. A "yes" either adds a role or is explicitly justified. This catches what signal-scoring misses.
5. **Run the discussion.** 3 rounds. Commit a word budget up front. Per-contribution caps enforced during Round 1, not at the end. At least one real rebuttal.
6. **Conclude.** Recommendation, decisions, open questions, trade-offs (required section, even if empty), numbered+prioritized next steps.

Optional phases when triggered:

- **Deliverable production via sub-agents** — only for `scope=building` with high complexity, or explicit "deep dive" requests. Discussion itself always runs single-agent to preserve cross-role interaction.
- **External audit in fresh context** — auto-triggered for `complexity=high` + `is_regulated=true`, or `complexity=high` + IP-using product, or on explicit user request. Uses a fresh sub-agent to catch what the team wasn't equipped to see.

## What the output looks like

A single Markdown block:

1. A one-line **word budget commitment** at the top.
2. A brief **signals summary** (one line of key signals; full 13-row table only if the brief is ambiguous).
3. A **Team Assembly** table with a one-clause "Why Included" for each non-core role, plus a compressed Gap Check subsection.
4. The **3-round discussion** — roles identified by `@handle`, each contribution 2–5 sentences (40–120 word caps by scope), with at least one rebuttal that actually pushes back.
5. A **Conclusion** with five required subsections: Recommendation, Decisions Made, Open Questions, Trade-offs Identified, Recommended Next Steps (numbered, prioritized).

Length targets range from 300–600 words for trivial scopes to 1200–2000 for building scopes, with *hard* ceilings — if you're over, you're padding.

## Design choices worth knowing

- **Risk-blocking roles are non-droppable.** When legal, security, developmental-psych, or clinical-psych are triggered by their specific risk signal, no amount of team-size pressure can drop them. The rule explicitly forbids "collapse into" and "covered by" justifications — those are the workarounds this rule exists to prevent.
- **Gap Detection is a second pass, not an alternative.** Signal-scoring and Gap Detection are additive. Either can trigger a required role; the Gap Check questions specifically target cases signal-scoring tends to miss (existing IP, ambient audio, clinical-adjacent content).
- **Word budgets commit before the discussion, not after.** Empirically, prose-only ceilings overshoot by 30–50%. Committing a per-section budget, writing short the first time, and truncating as you go — not rewriting to shrink afterward — is what actually keeps the output tight.
- **No seniority weighting.** Every role earned its seat through Phase 2 scoring. Weighting opinions by title would introduce hierarchical bias and reduce the diversity that makes the team valuable. The rebuttal round provides emergent quality filtering — arguments that don't survive carry less weight naturally.
- **Split-context for audits.** The optional Phase 6.5 audit runs in a fresh sub-agent context. Self-audit in the same context has confirmation bias and defeats the purpose; if the platform doesn't support sub-agents, the skill recommends a human review rather than running it in-context.

## Install

This skill is distributed as a [Claude Code](https://docs.claude.com/en/docs/claude-code) plugin inside the [`sorawit-w/agent-skills`](https://github.com/sorawit-w/agent-skills) marketplace. From Claude Code or Cowork:

```
/plugin marketplace add sorawit-w/agent-skills
/plugin install team-composer@sorawit-w
```

Once installed, Claude picks the skill up automatically from the description in its `SKILL.md` frontmatter. Invocation triggers on phrases like "brainstorm this with me," "who should be involved," "assemble a team," "let's workshop this," "plan this feature," or "review this project."

## Cross-skill integration

| Skill | When it kicks in |
|---|---|
| `brand-workshop` | Preferred for pure brand-identity deliverables (logo + tagline + strategy brief). |
| `ui-ux-pro-max` | When the designer or frontend engineer needs to produce high-fidelity UI. |
| `tech-stack-recommendations` | When the architect/lead needs to pick or evaluate a stack. |
| `i18n-contextual-rewriting` | When the i18n specialist is active and the team produces translatable content. |
| `theme-factory` | When any team-composer deliverable needs consistent visual styling. |
| `pptx` (fallback only) | Only when the user explicitly requests `.pptx`; otherwise a self-contained HTML deck is preferred for decks. |

The principle: this skill owns team assembly and discussion. When the discussion produces actionable deliverables, hand off to the specialized skill rather than attempting it inline.

## Status and scope

v0.1. The role catalog covers ~30 personas across product, engineering, design, compliance, behavioral science, clinical, creative, naming, localization, data, dharma/contemplative, and humor lenses. More domains will be added as concrete briefs exercise them.

- **Supported:** projects with a tech component, regulated domains, multi-perspective planning/review, new products, pivots, feature design, fintech/health/biotech/climate/games/education/AI/social.
- **Adaptable:** non-tech projects via `@domain_expert`, though a specialized skill may be a better fit.
- **Not supported:** pure brand-identity deliverables (use `brand-workshop`), hiring, 1-on-1 pairing, live multi-turn facilitation across rounds.

## Contributions

Not accepting external contributions right now. Feel free to fork.

## License

MIT — see the [LICENSE](https://github.com/sorawit-w/agent-skills/blob/main/LICENSE) file at the repo root.
