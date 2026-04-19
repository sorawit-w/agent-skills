---
name: pitch-deck
description: Constructs an investor-ready pitch deck as a single self-contained HTML file (Reveal.js, print-to-PDF, zero network dependencies). Interviews the founder for real content — problem, solution, market, product, business model, traction, team, competition, ask, use of funds — and enforces one-claim-per-slide plus required-slot gating. Use whenever the user asks to "build a pitch deck", "create a fundraising deck", "make an investor deck", "put my pitch together", "Series A deck", "seed deck", "demo day deck", or uploads a business-model.md / brand-kit and asks for the pitch. Also trigger when the user has `brand-workshop` and/or `business-model-canvas` output ready and wants the next artifact, or when `@startup_strategist` + `@vc_partner` are the right lenses. Even if the user only asks for one slide (e.g., "help me with my market slide"), use this skill — the surrounding slides stress-test that slide's claims.
---

# Pitch Deck

Construct an investor-ready pitch deck from founder inputs. Output is a single
self-contained HTML file built on Reveal.js. The narrative is the deliverable; the
slide template is the scaffold that keeps the narrative honest.

## What this skill produces

Every run produces exactly THREE files at these exact paths:

1. **`pitch/deck.html`** — single self-contained HTML file. Reveal.js-based, keyboard
   nav (←/→/Space/Esc), AAA contrast for projection, prints cleanly to PDF via
   `?print-pdf` query param + CSS paged media, zero network dependencies (all JS/CSS
   inline, images base64 if any).
2. **`pitch/speaker-notes.md`** — per-slide speaker notes with the 15–30 second spoken
   version of each slide's message and the most likely investor pushback.
3. **`pitch/deck-checklist.md`** — before-you-send-this-deck checklist covering the
   required-slot gate, the 90-second read test, and legal/disclosure reminders.

All three paths are named explicitly in the response (see Phase 3 Step 5).
Single-slide reworks still produce three files — the untouched files are
regenerated from prior content so the pitch folder stays consistent. All
three files go into `pitch/` inside the founder's working directory.

## What this skill is NOT

- **Not a template you fill in later.** Slides ship with real content or with explicit
  `[fill in: …]` slots that block rendering until answered. This skill owns deck
  construction end-to-end — `brand-workshop` does not ship a deck template.
- **Not a financial model.** The Ask and Use of Funds slides reference numbers the
  founder provides; this skill does not produce projections, cohort curves, or unit
  economics beyond what the founder inputs.
- **Not a substitute for customer validation.** Traction claims are only as good as
  the founder's data. The skill flags unsubstantiated traction but doesn't go
  validate it.
- **Not a design tool.** Visual polish comes from the brand kit. If no `brand-kit/`
  is present, the deck uses neutral-professional defaults — don't try to invent a
  visual identity inside this skill.

## Skill Boundaries

This skill intentionally overlaps with `team-composer` (`@startup_strategist` and
`@vc_partner` are active there too) but differs in deliverable:

- **Use `pitch-deck` when:** the founder wants a *shippable artifact* — an HTML deck
  they can attach to an investor email or present from a laptop.
- **Use `team-composer` with `@startup_strategist` + `@vc_partner` when:** the founder
  wants a *discussion* on narrative structure, investor positioning, or one slide
  without committing to a full deck.

> **Companion plugins:**
> - `brand-workshop` — upstream. Produces `brand-kit/` which this skill reads for
>   visual tokens (`design-system.md`), positioning/voice (`brand-brief.md`), and
>   taglines (`descriptions.md`). Brand-workshop does not pre-emit a deck template;
>   this skill generates its own Reveal CSS from the design-system tokens.
> - `business-model-canvas` — upstream. If `business-model.md` exists, this skill
>   reads it directly to seed the Business Model slide and to stress-test the
>   Ask slide against the Stress Tests section.
>
> An umbrella `startup-launch-kit` plugin may later orchestrate all three.

---

## The Standard 10-Slide Arc

Investors read decks in **under 4 minutes**. One claim per slide, numbers where numbers
belong, faces on the team slide, a specific ask. The standard arc:

| # | Slide | Core question it answers |
|---|-------|---------------------------|
| 1 | Title | What is this company and who's pitching? |
| 2 | Problem | Who hurts, how much, and why hasn't it been solved? |
| 3 | Solution | What do we do, in one sentence? |
| 4 | Market | How big is this, credibly, with SAM and SOM (not just TAM)? |
| 5 | Product | What does it actually do — screenshot or demo, not an architecture diagram. |
| 6 | Business Model | Who pays, how, how often, at what price band? |
| 7 | Traction | Numbers with a time axis. Revenue, users, logos, LOIs, retention — whatever is strongest. |
| 8 | Team | Faces + relevant prior experience. Why this team for this problem. |
| 9 | Competition | The real competitor is the customer's status quo, not "no one does this." |
| 10 | Ask & Use of Funds | Specific amount, specific milestones it buys, specific runway. |

**Optional slides** (add only if the founder has real content): Why Now, Vision,
Appendix (cohort data, cap table, legal structure). Adding optional slides without
real content *weakens* the deck — resist the urge to pad.

See `references/slide-contracts.md` for each slide's required slots, anti-patterns,
and the investor-read-test question it must pass.

---

## Phase 1: Intake

**Goal:** inventory what's already written and figure out the narrative gaps.

### Step 1 — Read the working directory

Check for these files, in order:

1. **`business-model.md`** (from `business-model-canvas`) — if present, parse the
   Customer Segments, Value Propositions, Revenue Streams, and Stress Tests sections.
   These seed slides 2, 3, 6, 7, and the anti-patterns check.
2. **`brand-kit/design-system.md`** (from `brand-workshop`) — if present, extract
   color tokens, typography, and logo path for deck styling. Use the same strict
   token mapping as `business-model-canvas` (see `business-model-canvas`'s
   `references/bmc-html-template.md` — `Color Tokens → Primary` maps to the deck's
   accent; `Typography → display` maps to headings, fall back to `Typography →
   body`).
3. **`brand-kit/brand-brief.md`** (from `brand-workshop`) — if present, read the
   `## Positioning` and `## Voice & Tone` sections (named anchor headings) for
   tone matching. If those sections are missing, fall back to the `## Executive
   Summary` + `## Workshop Transcript` sections.
4. **`brand-kit/descriptions.md`** (from `brand-workshop`) — if present, read the
   tagline row and short/medium bios. Slide 1 (Title) uses the tagline from here
   first, falling back to `brand-brief.md → Final Concept → Tagline`.

**Note on deck CSS:** `brand-workshop` does **not** emit a deck template or CSS file.
This skill owns deck construction end-to-end. Generate the Reveal CSS directly from
the tokens in `design-system.md` (color, typography, spacing) using the same strict
mapping convention. Do not look for `brand-kit/deck/pitch-styles.css` or
`brand-kit/deck/pitch-template.html` — those artifacts no longer exist.

**If none of the above exist:** ask the founder whether to run `brand-workshop` and/or
`business-model-canvas` first, or to proceed with neutral defaults. Proceeding without
them is fine for early-stage pre-seed; for Series A+ the brand-kit and business model
should usually exist first.

### Step 2 — Classify the deck variant FIRST

Before any slide drafting, ask exactly ONE question and wait for the answer:

> "Which variant: (a) pre-seed, (b) seed, (c) Series A/B, or (d) demo-day /
> cold-send / warm intro / follow-up? This changes how I treat traction and
> the ask."

**Do not skip. Do not infer from context. Do not proceed to Step 3 without
an answer.** The variant gates, at minimum:

- **Traction slide depth** — pre-seed = validation proxies (LOIs, waitlist,
  pilots with end dates); Series A/B = revenue curve, retention cohorts
- **Ask slide format** — pre-seed = SAFE/note, round size only;
  Series A/B = priced round, use-of-funds table, runway in months
- **Competition framing** — pre-seed = "why now + insight"; Series A/B =
  "why us beats them, with evidence"
- **Length tuning** — see `references/deck-variants.md`

If the user refuses to pick, default to **seed** and state that assumption
verbatim in the first line of the response: "Assuming seed variant — correct
me if wrong."

### Step 3 — Identify what's missing

List the slides whose required slots (`references/slide-contracts.md`) aren't yet
answered by inputs from `business-model.md` or prior founder content. Show the list
to the founder before launching into the interview — this prevents surprise and lets
the founder batch context.

---

## Phase 2: Narrative Interview

**Goal:** fill every required slot with content the founder actually owns.

### Role setup

Run in first-person voice with these roles active:

| Role | Lens |
|------|------|
| `@startup_strategist` | Workshop lead. Drives the narrative construction slide-by-slide. |
| `@vc_partner` | Read-test after every 2–3 slides. "Would I keep reading?" |
| `@senior_copywriter` | Enforces one-claim-per-slide, cuts buzzwords, ensures the segment's language lands. |
| `@dataviz_engineer` | Charts for Market (bar/stack), Traction (line with time axis), Competition (2×2). Active only when the relevant slide needs a chart. |

### Interview protocol

Go in the **standard arc order** (Title → Ask), slide by slide. For each slide:

1. Read the slide's required slots from `references/slide-contracts.md`.
2. Show the founder the required slots. Collect real answers in their words — do not
   paraphrase into VC-speak.
3. **Every 2–3 slides, run the @vc_partner read test.** They read what's been produced
   so far as if it were cold, and flag what doesn't land. If something doesn't land,
   revise before continuing — not at the end.
4. Surface the top anti-pattern for the slide (see `references/slide-contracts.md`).
   Explicitly check the deck doesn't fall into it.

**What to do when the founder doesn't have an answer:** do not invent. Mark the slot
`[fill in: ${specific-question}]`. The `deck-checklist.md` will block shipping until
these are filled. See "Required-Slot Gating" below.

### The four cardinal sins (flag and refuse)

The skill must refuse to ship a deck that commits any of these:

1. **TAM-only market sizing.** A market slide with only TAM (top-down) and no
   bottom-up SAM or SOM is a lie by omission. Refuse to render without both.
2. **Traction without a time axis.** "10,000 users" could be over 10 years or 10
   days. Every traction number has a start date.
3. **Team slide with no faces or no relevant experience.** Faces + prior-experience
   tag per founder. Missing either is a flag.
4. **Vague ask.** "Raising $X to grow the business" fails. Required: amount,
   milestones the amount buys, runway in months.

These are hard gates. If the founder wants to ship anyway, document the override
in `deck-checklist.md` so they own the decision.

### Single-slide rework mode

When the user asks to rework ONE slide without rebuilding the full deck
(e.g., "just help me with my Competition slide", "rework my Market slide"):

1. Apply that slide's contract from `references/slide-contracts.md` as usual
   — **including its required visual format** (e.g., Competition needs a 2×2
   or comparison matrix, not a bullet list; Traction needs a chart with a
   time axis, not a number-in-prose). Name the format requirement in your
   first response so the founder knows what they're ultimately producing,
   even while you're still gathering intake content.
2. **Cross-check against the named adjacent slides before finalizing.** An
   isolated rework is how a single-slide edit quietly breaks the rest of the
   deck. Standard adjacencies:

   | Slide being reworked | Must stay consistent with |
   |----------------------|---------------------------|
   | Problem      | Market (SAM named segment), Solution (fits this pain) |
   | Solution     | Problem (addresses stated pain), Product (matches demo) |
   | Market       | Problem (same segment), Business Model (ACV × SOM math) |
   | Product      | Solution (what the demo proves), Business Model (the action pricing hangs on) |
   | Business Model | Traction (metric must match the model), Market (SOM matches ACV × customer count) |
   | Traction     | Business Model (MRR vs GMV vs users — match the model), Ask (trajectory supports runway) |
   | Team         | Ask (team has skills to execute the milestones) |
   | Competition  | Problem (segment), Solution (differentiation axis), Product (claim is demonstrable) |
   | Ask          | Traction (trajectory supports milestones), Team (can execute), `business-model.md` Stress Tests |

3. Ask the founder briefly for the adjacent slides' current content, or read
   them from prior drafts if provided. Do not rework in isolation.
4. The four cardinal sins still apply to the single slide being reworked —
   e.g., a standalone Market rework is still gated on SAM + SOM bottom-up;
   a standalone Traction rework is still gated on a time axis.

---

## Phase 3: Build & Ship

**Goal:** produce `pitch/deck.html`, `pitch/speaker-notes.md`, and
`pitch/deck-checklist.md`.

### Step 1 — Assemble the Reveal.js HTML

Follow the template pattern in `references/deck-template.md`. Key constraints:

- **Single file.** Reveal.js core, theme CSS, plugin JS, and any images all inline or
  base64. No `<script src="https…">`. No `<link rel="stylesheet" href="https…">`.
- **Brand token substitution.** If `brand-kit/design-system.md` is present, substitute
  color and font tokens into the Reveal theme via CSS custom properties. Check contrast
  for projection (AAA for body text, AA minimum for accents).
- **Print-to-PDF.** Include `@media print` rules that hide controls, force one slide
  per page, and respect page breaks. Test that appending `?print-pdf` to the file URL
  produces a clean slide-per-page PDF when the user prints from the browser.
- **Charts.** Use inline SVG from `references/deck-charts.md`. No external chart
  library. Market bar/stack, Traction line with time axis, Competition 2×2 — these
  three cover ~95% of deck chart needs.
- **Images.** Base64-encode any images the founder provides. If the founder provides
  image paths instead, copy the files into the `pitch/` folder and reference them
  relatively — the deck still works offline even if the encoded version isn't used.

### Step 2 — Required-slot gating

Before writing the file, scan for any `[fill in: …]` markers in the content. For each:

- If the slot is a **cardinal required slot** (see `references/slide-contracts.md`),
  render a warning slide at position 0 titled "**This deck is not ready to send**"
  listing each unfilled cardinal slot.
- If the slot is **non-cardinal** (e.g., optional metric, secondary logo), render the
  slot inline with muted styling and `[fill in: …]` prompt text.

Never silently ship a hollow deck. Investors spot them instantly and it costs the
founder credibility with that firm.

### Step 3 — Write speaker notes

For every slide, write `pitch/speaker-notes.md` with:

- The **15–30 second spoken version** of the slide's message (investor meetings run
  fast — if a slide can't be delivered in 30 seconds, it's too dense).
- The **most likely investor pushback** and the one-line response.
- **Optional: the deep-dive redirect** — what slide or data the founder can pull up
  if pushback goes deeper.

See `references/speaker-notes.md` for the format.

### Step 4 — Write the deck checklist

Produce `pitch/deck-checklist.md` covering:

- **Before you send:** required slots filled, traction has a time axis, ask is
  specific, team slide has faces.
- **The 90-second read test:** the founder reads the deck cold in 90 seconds and
  verifies they understand the business. If they don't, the deck isn't done.
- **Legal / disclosure reminders:** "Confidential" in the footer if under NDA,
  forward-looking-statement disclaimer if projections are shown, CCPA/GDPR if
  personal data is referenced anywhere.

See `references/deck-checklist.md` for the template.

### Step 5 — Present to the user

Use `present_files` if available. Otherwise emit clickable `computer://` links.

**Always name all three output files explicitly in the response:**

- `pitch/deck.html`
- `pitch/speaker-notes.md`
- `pitch/deck-checklist.md`

Name them even on partial runs — a single-slide rework still names the file
being edited. Do not substitute "the deck file", "your slides", or "the notes"
for the path.

End with EXACTLY these three lines, in this order, prefixed verbatim:

1. `Weakest slide for investor read-test: <slide name> — <why>`
2. `Strongest remaining anti-pattern: <pattern> on <slide name>`
3. `Highest-value next edit: <one sentence>`

This applies to first-pass decks, single-slide reworks, and regenerations.
Do not replace the triad with presentation-prep tips, "next steps", or a
summary block. If a line is genuinely N/A (e.g., deck passed every gate),
write the prefix + `none` — never omit the line.

---

## Output Files

```
pitch/
├── deck.html              Self-contained Reveal.js deck (primary deliverable)
├── speaker-notes.md       Per-slide 15–30 sec spoken version + likely pushback
└── deck-checklist.md      Before-you-send gate + 90-second read test + legal
```

No other files. Do not scatter intermediate HTML drafts.

---

## Quality Checklist

Before presenting to the user, verify each:

**Narrative**
- [ ] Every slide answers the core question from the standard arc (one claim per slide)
- [ ] Market slide has both bottom-up SAM and SOM, not just TAM
- [ ] Traction slide has a time axis on every number
- [ ] Team slide has faces + relevant prior experience per founder
- [ ] Ask slide names amount, milestones, and runway in months
- [ ] No `[fill in: …]` cardinal slots remain — or a warning slide at position 0 lists them

**Rendering**
- [ ] `deck.html` is a single file — no external CSS/JS/font/image URLs
- [ ] Keyboard navigation works (←/→/Space/Esc)
- [ ] `?print-pdf` produces a clean slide-per-page PDF
- [ ] AAA contrast for body text against projection backgrounds; AA minimum for accents
- [ ] Brand tokens applied if `brand-kit/design-system.md` present; neutral defaults otherwise

**Shipping**
- [ ] Three files present: `deck.html`, `speaker-notes.md`, `deck-checklist.md`
- [ ] Speaker notes have 15–30 sec spoken version + likely pushback per slide
- [ ] Checklist has the 90-second read test and legal reminders
- [ ] Files saved to `pitch/` inside the founder's working directory
- [ ] Response ends with: weakest slide + worst remaining anti-pattern + single highest-value next edit

---

## Cross-Skill Integration

| Skill | When to Use |
|-------|-------------|
| `brand-workshop` (our own) | Before this skill, when a brand kit is needed. This skill reads `brand-kit/design-system.md` (tokens), `brand-kit/brand-brief.md` (`## Positioning` + `## Voice & Tone`), and `brand-kit/descriptions.md` (tagline) if present. Brand-workshop does not emit a deck template or CSS — this skill generates its own Reveal CSS from the design-system tokens. |
| `business-model-canvas` (our own) | Before this skill. This skill reads `business-model.md` to seed slides 2, 3, 6, 7 and to stress-test the Ask against the Stress Tests section. |
| `team-composer` (our own) | Instead of this skill when the founder wants discussion on narrative without committing to a full deck. Also for deep dives on single slides (e.g., Competition slide with `@competitive_intel` mental model). |
| `tech-stack-recommendations` (our own) | When the Product slide depends on tech choices the founder hasn't made yet. |
| `theme-factory` (Anthropic) | When the deck needs a visual theme and no `brand-kit/` is present. Apply after content is finalized. |
| `canvas-design` (Anthropic) | For hero / cover-slide static art when the brand-kit logo is too minimal to anchor the opening slide. Also for one-off slide graphics that justify the investment in real design over a chart. |
| `web-artifacts-builder` (Anthropic) | When the "deck" is actually a product demo that needs shadcn/ui components, routing, or state — i.e., beyond what Reveal.js can reasonably do. |
| `doc-coauthoring` (Anthropic) | For the long-form founder memo that precedes the deck (e.g., converting a 10-page memo into 12 slides). |
| `pptx` (Anthropic — **fallback only**) | Use **only** when the user explicitly requests `.pptx` — corporate constraints, Keynote / PowerPoint / Google Slides collaboration, or an existing `.pptx` template must be preserved. State the trade-off: `.pptx` loses interactivity, custom animations, and programmable charts. HTML-first is the default. |

**Principle:** this skill owns the investor-facing HTML deck. It does not do financial
models, does not do customer validation, does not do brand identity. Upstream plugins
feed it; downstream decisions (negotiation, term sheets) are `@vc_partner` territory
in `team-composer`.

**Graceful degradation:** if a referenced skill is not installed, this skill still
ships a complete `pitch/` folder — downstream integrations are enhancements, not
requirements.
