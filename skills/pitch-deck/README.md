<p align="center">
  <img src="https://raw.githubusercontent.com/sorawit-w/agent-skills/main/assets/pitch-deck-li.svg" alt="pitch-deck — investor-ready in one session" width="100%"/>
</p>

# pitch-deck

Construct an investor-ready pitch deck as a single self-contained HTML file. Built on Reveal.js (inlined, zero network dependencies), prints to PDF cleanly, enforces one-claim-per-slide, and refuses to ship a deck with any of the four cardinal sins unfilled.

This is not a template you fill in later. The deck ships with the founder's real content — or it doesn't ship at all.

## What it does

- Runs a **structured narrative interview** in `@startup_strategist` + `@vc_partner` + `@senior_copywriter` + `@dataviz_engineer` voices, slide by slide, in the standard investor arc: Title → Problem → Solution → Market → Product → Business Model → Traction → Team → Competition → Ask.
- **Reads upstream plugin output** when present. `validation-canvas.md` seeds slides 2, 3, 6 and cross-checks the Ask against the Stress Tests. `rat/assumption-test-plan.md` informs the Validation slide and Traction claims (and **gates clean shipping** — the deck refuses to ship without populated `## Results` for the top-3 hypotheses; override with `[PRE-VALIDATION DRAFT]` watermark). `brand-kit/DESIGN.md` supplies visual tokens from its YAML front matter ([Google Labs spec](https://github.com/google-labs-code/design.md), alpha).
- **Enforces required-slot gating.** Every slide has cardinal slots (from `references/slide-contracts.md`). Unfilled cardinal slots block shipping — the skill renders a warning slide at position 0 that lists them, so the deck is obviously not-ready rather than subtly hollow.
- **Refuses four cardinal sins:** TAM-only market sizing without SAM/SOM, traction numbers without a time axis, team slide without faces or relevant prior experience, vague ask without amount + milestones + runway.
- **Runs a VC read test every 2–3 slides** mid-interview — not at the end. If something doesn't land, revise before continuing.
- Produces **three files**, all saved to the founder's working directory:
  - `pitch/deck.html` — single self-contained HTML deck. Keyboard nav, AAA contrast for projection, `?print-pdf` produces a clean slide-per-page PDF, zero network dependencies.
  - `pitch/speaker-notes.md` — per-slide 15–30 second spoken version + the most likely investor pushback + optional deep-dive redirect.
  - `pitch/deck-checklist.md` — the before-you-send gate, 90-second read test, and legal/disclosure reminders for the founder to complete the day before sending.
- **Tunes to deck variant.** Cold-email send, warm-intro meeting, demo day, or follow-up-after-first-meeting — the standard arc stays intact, but slide depth, optional slides, and the closing emphasis adjust.

## What it doesn't do

- **Financial projections.** The Ask and Use of Funds slides reference numbers the founder provides; this skill does not produce cohort curves, unit economics models, or revenue forecasts.
- **Customer validation.** Traction claims are only as good as the founder's data. The skill flags unsubstantiated traction, but doesn't run interviews to validate it.
- **Brand identity.** Visual polish comes from `brand-workshop`. If no `brand-kit/` exists, the deck uses neutral-professional defaults rather than inventing a look.
- **Business model construction.** If the model isn't crisp, use `validation-canvas` first (Lean Canvas + VPC). This skill reads the canvas; it doesn't replace the work of producing one.
- **Assumption testing.** Belongs to `riskiest-assumption-test` (required upstream). The deck enforces the gate — it refuses to ship a clean draft without populated RAT Results.
- **Term-sheet or negotiation work.** That's `@vc_partner` territory via `team-composer`, post-deck.

## When to use it

- You have a business, a product, and enough traction (real or pre-revenue validation proxies) to fundraise — and need a shippable deck this week.
- You just finished `riskiest-assumption-test` and have results in hand for the top-3 hypotheses — and the next artifact you need is the investor-facing deck.
- You're preparing for cold-email outreach, a warm-intro meeting, a demo day, or a follow-up send — each variant gets tuned depth and emphasis.
- An investor asked "send me your deck" and the founder doesn't have one — or the one they have is a template with no real content.

## When to use something else

- **Narrative discussion without a full deck** → `team-composer` with `@startup_strategist` + `@vc_partner`. Faster, discussion-grade.
- **Single-slide deep dive** (e.g., rework just the Competition slide) → `team-composer` with `@startup_strategist` + `@competitive_intel`. Though this skill handles single-slide requests too — it uses the surrounding slides to stress-test the one the founder is rebuilding.
- **Brand / logo / tagline / deck template** → `brand-workshop` (upstream).
- **Business-model crispness** → `validation-canvas` (two steps upstream).
- **Assumption testing** → `riskiest-assumption-test` (required direct upstream).
- **Financial model** → a spreadsheet + the `xlsx` skill. This plugin deliberately stays narrative, not quantitative.

## How it works

Three phases, all in one Claude session.

**Phase 0 — RAT gate (~30 sec).** STOP if `rat/assumption-test-plan.md` is missing or its `## Results` is empty for top-3 hypotheses. Override path: founder declares "pre-validation draft" → proceed with watermark.

**Phase 1 — Intake (~5 min).** Read the working directory for `validation-canvas.md`, `rat/assumption-test-plan.md`, `brand-kit/DESIGN.md`, `brand-kit/brand-brief.md`, `brand-kit/descriptions.md`. Ask the founder which deck variant (cold-email / warm-intro / demo day / follow-up). List missing cardinal slots before launching the interview so the founder can batch context.

**Phase 2 — Narrative Interview (~60–90 min for a first pass).** Slide by slide in the standard arc order. `@startup_strategist` leads; `@vc_partner` runs a read test every 2–3 slides; `@senior_copywriter` enforces one-claim-per-slide and cuts VC-speak; `@dataviz_engineer` designs the Market, Traction, and Competition charts. Unknowns get marked `[fill in: specific question]` rather than invented.

**Phase 3 — Build & Ship.** Assemble `pitch/deck.html` from the template in `references/deck-template.md`, substituting brand tokens when `brand-kit/` is present. Scan for unfilled cardinal slots — if any remain, render a warning slide at position 0 listing them. Write `pitch/speaker-notes.md` with the 15–30 second spoken version + likely pushback per slide. Write `pitch/deck-checklist.md` with the full before-you-send gate. Respond with the single weakest slide + worst remaining anti-pattern + highest-value next edit.

## What the output looks like

```
<your-working-folder>/
└── pitch/
    ├── deck.html              single self-contained HTML deck (primary deliverable)
    ├── speaker-notes.md       per-slide 15–30 sec spoken version + likely pushback
    └── deck-checklist.md      before-you-send gate + 90-second read test + legal
```

Open `deck.html` in any browser — it works without internet, on a plane, in a basement conference room. Append `?print-pdf` to the URL and print for a clean slide-per-page PDF. Keyboard nav: ←/→ arrows, Space, Esc.

## Design principles

- **Required-slot gating, not optional suggestions.** Investors spot a hollow deck instantly and it costs the founder credibility with that firm. The skill would rather render a warning slide than ship a deck that looks ready but isn't.
- **Four cardinal sins are non-negotiable.** TAM-only market, traction without time axis, team without faces/experience, vague ask. Any one is a hard gate.
- **One claim per slide.** A deck full of slides that each try to say three things gets skimmed at half the density. One claim, one slide, one chart — investors read faster.
- **The customer's status quo is a competitor.** "No one does this" means you haven't looked. The Competition slide names the current workaround explicitly.
- **The VC read test is mid-stream, not end-stream.** Checking at the end produces a deck the founder has to redo. Checking every 2–3 slides produces a deck that lands.
- **Zero network dependencies in the deck.** No CDN, no webfonts from the internet, no remote images. A deck that needs wifi to render is not shippable.
- **Folder conventions over configuration.** No manifest file in v1. If `brand-kit/`, `validation-canvas.md`, and `rat/assumption-test-plan.md` are present, read them; if RAT is missing, the heavy gate STOPs the run. Write to `pitch/`, never clobber another plugin's output.
- **Speaker notes are compressed rehearsal, not a teleprompter.** The 15–30 second spoken version of each slide + the pushback you'll hear. Founders who can deliver that version cold have internalized the slide.

## Install

This skill is distributed as a [Claude Code](https://docs.claude.com/en/docs/claude-code) plugin inside the [`sorawit-w/agent-skills`](https://github.com/sorawit-w/agent-skills) marketplace. From Claude Code or Cowork:

```
/plugin marketplace add sorawit-w/agent-skills
/plugin install pitch-deck@sorawit-w
```

## Related skills

- **`brand-workshop`** — upstream. Produces the `brand-kit/` this skill reads for visual tokens (`DESIGN.md`, spec: https://github.com/google-labs-code/design.md alpha), positioning/voice (`brand-brief.md`), and tagline (`descriptions.md`).
- **`validation-canvas`** — two steps upstream. Produces `validation-canvas.md`, which this skill reads to seed the Problem, Solution, and Business Model slides — and to stress-test the Ask against the canvas's Stress Tests section.
- **`riskiest-assumption-test`** — required direct upstream (heavy gate). Produces `rat/assumption-test-plan.md`. The deck refuses to ship without populated `## Results` for top-3 hypotheses.
- **`startup-grill`** — downstream. Adversarially probes the deck after this skill ships.
- **`team-composer`** — the discussion-grade alternative when the founder wants to workshop narrative structure without committing to a full deck.
- **`theme-factory`** — sibling. If no `brand-kit/` exists and the founder wants a bespoke visual theme for the deck, apply after content is finalized.
- **`tech-stack-recommendations`** — sibling. When the Product slide depends on tech choices the founder hasn't made yet.

## Status and scope

v0.1. The ten-slide arc, cardinal-slot gating, and the Reveal.js template are locked. The skill runs in one Claude session end-to-end. Planned improvements:

- **Deck update mode** — detect an existing `pitch/deck.html`, parse its content, treat the interview as an update rather than rebuild.
- **Auto cohort-retention appendix** — when `validation-canvas.md` + a retention data file exist, generate the cohort table as an appendix slide.
- **In-session Claude-in-Chrome preview** — render the deck mid-interview and screenshot, so the founder sees what they're building before the final write.
- **Multi-language decks** — reuse content with translation pass for non-English investor markets.

**Supported:** first-pass deck for a single company and a single deck variant. Re-runs to produce a different variant (e.g., convert a warm-intro deck to a demo-day deck) by re-invoking the skill with the same working directory.

**Not supported:** multi-company decks in one pass (run the skill once per company), financial modeling, automated market research, fundraising strategy beyond slide narrative.
