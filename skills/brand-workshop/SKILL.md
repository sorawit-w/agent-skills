---
name: brand-workshop
description: >
  Simulate a collaborative branding team to create a launch-ready brand identity package
  from a business overview. Use this skill whenever the user asks to create a logo, brand
  identity, tagline, or brand concept for a business, product, app, or project. Also trigger
  when the user says things like "help me brand this," "I need a logo," "come up with a tagline,"
  "brand identity for my app," or provides a business description and asks for visual identity
  work. This skill runs a structured multi-role brainstorming workshop and produces: a brand
  strategy brief (.md), tagline, code-generated logo (.svg), favicon pack with HTML install
  snippet, social banner set (OG / X / LinkedIn / Instagram), descriptions pack (tagline +
  bios + elevator pitch + boilerplate), and a starter DESIGN.md (tokens only).
  Even if the user only asks for a logo or only a tagline, use this skill — the full workshop
  produces better results. Do NOT trigger on requests for pitch decks, presentations, or
  investor materials — hand off to the `pitch-deck` skill instead, which consumes `DESIGN.md`
  directly.
  Do NOT trigger on "refresh our existing brand", "update our current style guide",
  "evolve our identity", "our current brand", "our existing voice", "audit our logo",
  or any phrasing that implies a live brand being revised. Those belong to
  `team-composer:team-composer` (with @brand_strategist / @senior_copywriter) and the
  `brand-voice:*` family. This skill only generates net-new identity from a business overview.
---

# Brand Workshop

A collaborative branding skill that assembles a virtual creative team, runs a structured
brainstorming session, and delivers a brand strategy brief, tagline, and logo.

## STOP — When NOT to use this skill

This skill generates brand identity from a business overview. It is NOT a remix tool
for a brand that already exists. **Hand off to `team-composer` — do not run the workshop —
if any of these are true:**

- The user already has a logo in use and is asking to refresh / update / audit it
- The user already has a style guide and is asking to modernize or refresh it
- The user says "our current brand", "our existing voice", "our logo", "our palette"
- The request is "update our brand voice" / "refresh our style guide" / "our brand has evolved"
- The deliverable is a style-guide update, voice audit, or brand refresh — not a net-new identity

How to hand off:

Invoke **`team-composer:team-composer`** as the next skill. Use the literal skill
identifier — do NOT pick a plausibly-adjacent skill by name match alone.

**Anti-patterns — do NOT invoke any of these in place of `team-composer`:**

- `brand-voice:guideline-generation` — this is for extracting voice from existing
  sales calls / uploaded brand documents. It's a voice-discovery workflow, not a
  refresh workshop. Using it here will pull the user into a discovery loop they
  didn't ask for.
- `brand-voice:discover-brand` — this searches Notion / Slack / Drive for scattered
  brand materials. The user already knows where their brand lives — they want to
  evolve it, not find it.
- `brand-voice:brand-voice-enforcement` — this applies an already-written voice
  guide to new content. It does not produce a refresh.
- `brand-workshop:brand-workshop` (this skill) — do not recursively re-enter after
  the STOP check.

Once inside `team-composer:team-composer`, use `@brand_strategist` + `@senior_copywriter`
for voice work, or `@naming_specialist` for naming. Do not proceed with the Discovery →
Concept → Creation workshop described below.

---

## Overview

This skill simulates a brand workshop with specialized roles working together. The process
moves through three phases: **Discovery → Concept → Creation**. The output is always:

1. **Brand Strategy Brief** (`brand-brief.md`) — the team's rationale, concepts explored, and final direction
2. **Tagline** — embedded in the brief and called out prominently
3. **Logo** (`.svg` rendered to `.png`) — code-generated, defaulting to minimalist style
4. **Favicon Pack** — `favicon.svg`, raster sizes (16/32/180/512), `site.webmanifest`, and a copy-paste HTML `<link>` install snippet
5. **Social Banner Set** — Open Graph (1200×630), X header (1500×500), LinkedIn banner (1584×396), Instagram square (1080×1080), profile avatar (400×400)
6. **Descriptions Pack** (`descriptions.md`) — tagline + short/medium/long bios + elevator pitch + press boilerplate, all matched to brand voice
7. **Starter Design System** (`DESIGN.md`) — tokens only: color, typography, spacing, radius, and voice principles (no component specs)

Scope boundary: pitch decks (both the deck template *and* filled slide content) and the Business Model Canvas are intentionally out of scope. The `pitch-deck` skill reads `DESIGN.md` directly and generates a brand-skinned deck on its own — brand-workshop does not pre-emit a deck template. See Skill Boundaries below.

---

## Skill Boundaries

This skill overlaps partially with `team-composer`. Both assemble a virtual team
and run structured discussion. The difference is what they produce.

**Use `team-composer` instead of this skill when:**
- The user wants general project brainstorming, planning, or review — even if branding is part of it
- The user wants to **name** a product/feature (use `@naming_specialist`), **discuss positioning** (use `@brand_strategist`), or **review brand voice** (use `@humorist` + `@senior_copywriter`)
- The deliverable is NOT a logo + tagline + brief package
- The user is making multi-dimensional product decisions where branding is one input among many

**Stay in this skill when:**
- The primary deliverable is a **brand identity package**: logo (SVG) + tagline + brand strategy brief
- The user says: "help me brand my [startup/product/app]", "I need a logo", "create a brand identity", "design a brand concept", "give me a tagline and logo"
- The user provides a business overview and asks for visual identity work

**Boundary examples:**

| Request | Skill |
|---------|-------|
| "Help me brand my new fintech startup" | `brand-workshop` (this skill) |
| "I need a logo for X" | `brand-workshop` (this skill) |
| "Brainstorm my startup — product, positioning, go-to-market, branding" | `team-composer` (branding is one dimension) |
| "Name my product" | `team-composer` with `@naming_specialist` |
| "Review our product positioning" | `team-composer` with `@brand_strategist` |
| "Does our copy sound right?" | `team-composer` with `@humorist` + `@senior_copywriter` |

**Stop-rule — existing brands:**

If the user's request is to audit, refresh, document, or extend an **existing**
brand (logo already in use, style guide already drafted, "make our current brand
more X", "update our brand voice"), stop and invoke `team-composer` instead.
This skill generates brand identity from a business overview — it is not a
remix/audit tool for a live brand.

> **Future refactor note (Option D):** Today this skill has its own internal team
> (see Phase 2). Long-term, this skill could invoke `team-composer` as the
> discussion engine and focus only on the Creation phase (logo SVG, brief
> assembly). That refactor is not scheduled — revisit only if the role catalog
> drift between the two skills causes real maintenance pain. When revisited,
> unify role tag format (`@hyphen-case` here vs. `@snake_case` in team-composer).

> **Companion plugins (the startup pipeline).** This skill is step 1 of 5:
> `brand-workshop` → `validation-canvas` → `riskiest-assumption-test` →
> `pitch-deck` → `startup-grill`. Each lives in its own plugin directory.
> They are intentionally not folded together: each requires founder inputs
> (traction, revenue model, ask size, test results) that are out of scope
> for a brand workshop. After this skill ships, suggest `validation-canvas`
> as the next step — see Phase 7 (Closing). An umbrella `startup-launch-kit`
> plugin may later orchestrate all five.

---

## Phase 1: Discovery

### Step 0.0 — Path resolution + manifest awareness (v2.2.0+)

**Resolve the brand root** once at invocation, in this precedence order
(canonical chain):

1. **Explicit `output_dir` arg** (passed by `startup-launch-kit`) → use as-is.
2. **`STARTUP_KIT_DOCS_ROOT` env var** set → `${STARTUP_KIT_DOCS_ROOT}/brand/`.
3. **Smart default — `docs/startup-kit/` exists** → `docs/startup-kit/brand/`.
   Surface the smart-default notice: *"Writing to `docs/startup-kit/brand/`
   (smart default). Set `STARTUP_KIT_DOCS_ROOT=./docs` to write standalone
   instead."*
4. **Solo fallback** → `docs/brand/`.

**Note (v2.2.0 path migration):** prior versions wrote artifacts to the
working-directory root and downstream skills expected `brand-kit/` as the
prefix — these were inconsistent. v2.2.0 standardizes on `<brand-root>/`
(default `docs/brand/`). Downstream skills include legacy `brand-kit/`
fallback reads for backward compat.

**Manifest awareness.** Look for `kit-manifest.json` at
`<resolved-kit-root>/kit-manifest.json` first; fall back to the
working-directory root for backward compat. Use it as a hint, never as a
bypass:

- If the manifest lists `brand-workshop` as `completed` with a recent mtime,
  surface that fact: *"Manifest says you ran brand-workshop on [date]. Update
  mode (revise specific assets), fresh run (rebuild everything), or skip to
  the next step?"*
- If the manifest's `intake_answers` cache is populated, the founder has run
  the orchestrator's intake — use those answers as defaults for the discovery
  questions below (still surface them; do not silently skip).
- Manifest read failures (corrupt JSON, missing fields) are non-fatal — log
  the issue inline and proceed as if no manifest exists.

After this skill ships its artifacts (Phase 6 — output), if a manifest
exists, append/update this skill's entry. Use atomic write (write `.tmp`, then
rename). If the manifest doesn't exist, do **NOT** create it — that's the
`startup-launch-kit` orchestrator's job. See
[`startup-launch-kit/references/manifest-schema.md`](../startup-launch-kit/references/manifest-schema.md)
for the schema.

### Gather Inputs

Collect the following from the user. If some are missing, ask concisely — but don't block
on everything. Make reasonable assumptions and state them.

| Input | Required | Notes |
|-------|----------|-------|
| Business / product name | Yes | — |
| Business overview | Yes | What it does, who it serves |
| Vision | Helpful | Long-term aspiration |
| Mission | Helpful | How it delivers value |
| App features (if app) | Optional | Helps understand the product's nature |
| Target audience | Helpful | Demographics, psychographics |
| Existing brand assets | Optional | Colors, fonts, prior logos |
| Logo style preference | Optional | Defaults to minimalist w/ negative space |
| Tagline language | Optional | Defaults to English |

### Style Default

If the user does not specify a logo style, **default to minimalist with negative space**.
This style emphasizes clean geometry, hidden meaning through negative space, and timeless
simplicity. It works well across digital and print.

If the user asks for style suggestions, read `references/logo-styles.md` and present
the options with brief descriptions and famous examples.

---

## Phase 2: Concept — The Workshop

Assemble the virtual team and run a structured brainstorming. Each role contributes
a distinct perspective. The workshop is NOT a free-for-all — it follows a deliberate sequence.

### The Team

Read `references/team-roles.md` for detailed role definitions. Summary:

| Role | Primary Contribution |
|------|---------------------|
| @senior-brand-strategist | Positioning, brand architecture, competitive differentiation |
| @senior-copywriter | Tagline candidates, verbal identity, tone of voice |
| @lead-visual-designer | Logo direction, color palette, typography |
| @product-designer | How the brand lives in-product (if app/digital) |
| @growth-strategist | Memorability, virality, market fit of the brand |
| @regional-cultural-advisor | Cultural sensitivity, linguistic pitfalls, local resonance |
| @lead-ux-ui-designer | Digital-first considerations, favicon/app-icon viability |

Not every role needs to speak on every project. Scale participation to the project:
- **Minimum** (simple logo request): strategist, copywriter, visual designer
- **Full team** (app/product branding): all roles
- **Add roles** if context demands it (e.g., @accessibility-specialist for inclusive branding)

### Workshop Flow

Run these steps sequentially. Write each role's contribution in first person with their
role tag (e.g., `**@senior-brand-strategist:**`). This becomes the brainstorming transcript
in the brand brief.

#### Step 1: Strategic Foundation (Strategist)
- Define brand positioning: what makes this distinct?
- Identify 2-3 brand archetypes that fit
- Propose core brand attributes (3-5 adjectives)

#### Step 2: Verbal Exploration (Copywriter)
- Generate 5-7 tagline candidates based on positioning
- Note tone of voice direction
- Flag any naming/linguistic concerns
- Draft the **descriptions pack** variants (short / medium / long bio, elevator pitch,
  boilerplate) — these feed directly into Phase 3 and must match the tagline's voice.
  Each variant should stand alone, not read as a truncation of the next.

#### Step 3: Visual Direction (Visual Designer + UX/UI Designer)
- Propose 2-3 logo concepts (described verbally — shape, symbolism, approach)
- Suggest color palette direction (with hex values)
- Recommend typography family
- UX/UI designer weighs in on digital viability (favicon test, dark/light modes)

#### Step 4: Cultural & Market Check (Cultural Advisor + Growth Strategist)
- Cultural advisor flags any issues with symbols, colors, or words across cultures
- Growth strategist evaluates memorability and market positioning

#### Step 5: Convergence (Strategist leads)
- Synthesize: pick the winning tagline and logo direction
- State the rationale clearly
- The team votes (brief inline votes from each role)
- Declare the final concept

---

## Phase 3: Creation

### Brand Strategy Brief

Output a `.md` file with this structure:

```markdown
# Brand Strategy Brief: [Business Name]

## Executive Summary
One paragraph: what was created and why.

## Inputs
- Business overview, vision, mission (as provided)

## Positioning
2–4 sentences naming the target segment, the category the brand plays in, and
the one axis of differentiation. This is the section downstream plugins
(`pitch-deck`) parse for the problem/solution narrative — keep it short and
literal, not aspirational.

## Voice & Tone
3–5 bullets from the copywriter describing how the brand speaks (e.g.,
"confident but not arrogant", "plain language over jargon", "contractions OK").
Must match the bullets written into `DESIGN.md → Voice` (the custom Voice
section that brand-workshop appends after Do's and Don'ts) — these are the
same ruleset, surfaced in two places.

## Workshop Transcript
The full brainstorming from Phase 2, role by role.

## Final Concept

### Tagline
> "[The chosen tagline]"

Rationale: Why this tagline wins.

### Logo Concept
Description of the chosen logo direction, symbolism, and style.

### Color Palette
| Color | Hex | Usage |
|-------|-----|-------|
| Primary | #XXXXXX | ... |
| Secondary | #XXXXXX | ... |
| Accent | #XXXXXX | ... |

### Typography
Recommended font families and usage.

## Rejected Alternatives
Brief note on other tagline/logo concepts explored and why they were passed over.
```

**Section-contract note:** `## Positioning` and `## Voice & Tone` are named
anchor headings — `pitch-deck` greps by them. If you rename, update
`pitch-deck/SKILL.md` Phase 1 Step 1 in lockstep.

### Logo Creation

Generate the logo as SVG using Python. Follow these principles:

**Design Principles (Minimalist / Negative Space default):**
- Clean geometric shapes — circles, rectangles, triangles, arcs
- Negative space to embed hidden meaning (e.g., the arrow in FedEx, the bear in Toblerone)
- Maximum 2-3 colors from the chosen palette
- The logo must work at 32x32 (favicon) and 512x512
- No raster effects — pure vector geometry
- Text in the logo (if any) should use basic sans-serif or be drawn as paths
- Aim for a logomark (icon) + optional logotype (wordmark) lockup

**Technical approach:**
1. Generate SVG using Python string construction or `svgwrite` library
2. Keep the SVG clean — no unnecessary groups or transforms
3. Render to PNG at multiple sizes (64px, 256px, 512px) using `cairosvg` or `librsvg`
4. If rendering tools aren't available, output the SVG and note that PNG conversion
   can be done externally

**Code quality:**
- Write the SVG generation code clearly with comments explaining each shape's purpose
- Test the SVG is valid XML before saving
- Include viewBox for proper scaling

**If the user requests AI-generated imagery instead:**
Use the Hugging Face `dynamic_space` tool to find and invoke an image generation space.
This is opt-in only — never default to it.

### Favicon Pack

Generate a favicon set from the logomark. The mark must remain legible at 16×16 — if fine
detail disappears at that size, author a simplified **favicon-optimized variant** (same
concept, fewer strokes) rather than scaling the full mark blindly.

**Outputs (under `favicons/`):**

| File | Purpose |
|------|---------|
| `favicon.svg` | Vector source (modern browsers prefer SVG favicons) |
| `favicon-16.png`, `favicon-32.png` | Classic browser favicons |
| `favicon-180.png` | `apple-touch-icon` (iOS home-screen) |
| `favicon-512.png` | PWA / high-DPI |
| `site.webmanifest` | Populated with `name`, `short_name`, `theme_color` (palette primary), `background_color`, icon array |
| `favicon-install.html` | Copy-paste `<link>` tags ready to drop into `<head>` |

**install snippet template:**

```html
<link rel="icon" type="image/svg+xml" href="/favicon.svg">
<link rel="icon" type="image/png" sizes="32x32" href="/favicon-32.png">
<link rel="icon" type="image/png" sizes="16x16" href="/favicon-16.png">
<link rel="apple-touch-icon" sizes="180x180" href="/favicon-180.png">
<link rel="manifest" href="/site.webmanifest">
<meta name="theme-color" content="#XXXXXX">
```

**Quality rule:** Programmatically (or mentally) test the 16×16. If the mark is unrecognizable
at that size, simplify before generating — do not ship an illegible favicon.

---

### Social Banner Set

Generate branded social assets from the logo, palette, and typography. Use generous whitespace —
do not crop the logo to the edge. Banners that look auto-stamped hurt the brand more than
helping it.

**Outputs (under `social/`):**

| File | Dimensions | Use |
|------|-----------|-----|
| `og-image.png` | 1200×630 | Open Graph (Facebook, LinkedIn posts, Slack, iMessage link previews) |
| `x-header.png` | 1500×500 | X / Twitter profile header |
| `linkedin-banner.png` | 1584×396 | LinkedIn profile banner |
| `instagram-square.png` | 1080×1080 | Instagram feed post, general square |
| `profile-avatar.png` | 400×400 | Square profile picture from logomark |

**Design rules:**

- Minimum 8% padding on the shorter axis — logo never touches the edge
- Tagline appears **only** on hero-style banners (`og-image`, `instagram-square`); profile headers stay clean
- Background: brand primary or secondary; fall back to a neutral if contrast fails WCAG AA for any overlaid text
- Generate as SVG, rasterize to PNG via `cairosvg` (same toolchain as logo)
- If the palette has strong light/dark candidates, ship both variants of `x-header` and `linkedin-banner`; minimum is one variant per file

**Quality rule:** Preview each banner at 25% scale. If the composition looks cramped at
full size, it will look worse in a timeline.

---

### Descriptions Pack

The copywriter's work from Phase 2 Step 2 is assembled into a single file. All variants must
match the voice established in the brief and stand alone — not read as truncations of each
other.

**Output: `descriptions.md`**

| Variant | Length | Use |
|---------|--------|-----|
| Tagline | ≤8 words | Everywhere — hero, email signature, favicon alt |
| Short bio | ≤60 characters | X/Instagram bio, HTML `<meta name="application-name">` |
| Medium bio | ≤160 characters | LinkedIn headline, HTML `<meta description>` |
| Long bio | ≤280 characters | One tweet, About-page lead paragraph |
| Elevator pitch | ~75 words | "About us" section, demo-day opening |
| Press boilerplate | ~120 words | Press release closing "About [Company]" paragraph |

**Quality rule:** Paste each variant into the appropriate platform's character counter before
shipping. If any variant is over its hard limit, rewrite — do not truncate.

---

### DESIGN.md (Starter Tokens)

Output `DESIGN.md` **as its own standalone file at the root of the output folder**, named exactly `DESIGN.md` (uppercase). When the founder adopts the brand kit into a real repo, this file moves to the repo root — that's the [Google Labs DESIGN.md spec](https://github.com/google-labs-code/design.md) convention. Do NOT fold tokens into `brand-brief.md` as a section — downstream plugins (`validation-canvas`, `riskiest-assumption-test`, `pitch-deck`) parse `DESIGN.md` directly and will not find tokens buried in another file.

**Format**: [Google Labs DESIGN.md](https://github.com/google-labs-code/design.md), spec version `alpha` (current as of 2026-05; the spec is under active development — re-check when the spec ships a non-alpha tag). The file has two parts:

1. **YAML front matter** — machine-readable design tokens.
2. **Markdown body** — human-readable rationale, organized into canonical sections.

Scope is deliberately narrow: **tokens, not components**. Button styles, form fields, grids, motion, and elevation depend on the engineering stack this skill does not choose — the implementing team adds those when they wire up the design system in their framework.

**Cross-plugin contract.** Downstream plugins (`validation-canvas`, `riskiest-assumption-test`, `pitch-deck`) bind their accent CSS variable (`--canvas-accent`, `--rat-accent`, `--deck-accent`) to `colors.primary` from the YAML front matter. Use the spec-recommended token names — `primary`, `secondary`, `tertiary`, `neutral` — do not invent alternatives or rename the keys. The previous `Primary | Secondary | Accent` convention is retired in favor of spec-aligned naming; downstream plugins read the YAML directly rather than greppping prose labels.

**Section order (per spec).** The DESIGN.md spec defines a canonical section order. Brand-workshop emits a subset for "starter" scope. Sections present must appear in this order:

1. **Overview** (required) — brand personality, audience, intended emotional response
2. **Colors** (required) — palette rationale + per-color usage prose
3. **Typography** (required) — type strategy + per-level role
4. **Layout** (required, even if minimal) — grid model + spacing rhythm
5. **Shapes** (required) — corner-radius philosophy
6. **Do's and Don'ts** (required) — visual / design guardrails
7. **Voice** (custom section appended after Do's and Don'ts; preserved by spec consumers as unknown but valid)

Sections explicitly omitted at "starter" scope: **Elevation & Depth** and **Components** — both stack-dependent and the implementing team's responsibility.

**File template.** Use this exact structure (replace bracketed placeholders with workshop output):

````markdown
---
version: alpha
name: [Brand Name]
description: [One-line summary of the brand's visual identity]
colors:
  primary: "#XXXXXX"      # brand hero color — drives CTAs, headlines, emphasis
  secondary: "#XXXXXX"    # supporting brand color
  tertiary: "#XXXXXX"     # accent / highlight, NOT the hero
  neutral: "#XXXXXX"      # background / surface foundation
  surface: "#FFFFFF"      # default page background — override neutral if needed
  on-surface: "#XXXXXX"   # default text color on surface
  error: "#XXXXXX"        # semantic error, harmonized with palette
typography:
  h1:
    fontFamily: [Display Family]
    fontSize: 48px
    fontWeight: 600
    lineHeight: 1.1
    letterSpacing: -0.02em
  h2:
    fontFamily: [Display Family]
    fontSize: 32px
    fontWeight: 600
    lineHeight: 1.2
  body-md:
    fontFamily: [Body Family]
    fontSize: 16px
    fontWeight: 400
    lineHeight: 1.6
  label-sm:
    fontFamily: [Body Family]
    fontSize: 12px
    fontWeight: 500
    lineHeight: 1
    letterSpacing: 0.05em
rounded:
  none: 0
  sm: 4px
  md: 8px
  lg: 16px
  full: 9999px
spacing:
  xs: 4px
  sm: 8px
  md: 16px
  lg: 24px
  xl: 32px
  "2xl": 48px
  "3xl": 64px
---

# [Brand Name] — DESIGN.md

## Overview

A holistic description of the brand's look and feel: personality, target audience, the emotional response the UI should evoke. Whether it should feel playful or professional, dense or spacious. This is foundational context for an agent making stylistic decisions when no specific token applies.

## Colors

[Describe the palette's rooting principle — e.g., "high-contrast neutrals and a single evocative accent color".]

- **Primary (#XXXXXX):** [Descriptive name + usage guidance]
- **Secondary (#XXXXXX):** [Usage]
- **Tertiary (#XXXXXX):** [Usage — clarify this is for accents, NOT the hero]
- **Neutral (#XXXXXX):** [Foundation usage]

## Typography

[Describe the typography strategy — e.g., "Two distinct weights of Public Sans for narrative; Space Grotesk for technical labels."]

- **Headlines (h1, h2):** [Family, weight, role]
- **Body (body-md):** [Family, weight, role]
- **Labels (label-sm):** [Family, weight, role]

## Layout

[Describe layout strategy at a high level — e.g., "Fluid grid on mobile, fixed-max-width 1200px on desktop. 8px spacing scale with a 4px half-step for micro-adjustments. Components grouped via containment with 24px internal padding."]

## Shapes

[Describe corner-radius philosophy — e.g., "Architectural sharpness: 4px on interactive elements, 8px on cards, 16px on hero containers. Avoid mixing radii within a view."]

## Do's and Don'ts

- Do use `primary` only for the single most important action per screen
- Do maintain WCAG AA contrast ratios (4.5:1 normal text, 3:1 large text)
- Don't mix rounded and sharp corners in the same view
- Don't use more than two font weights on a single screen
- [Add 2–4 brand-specific guardrails surfaced during the workshop]

## Voice

3–5 bullet rules from the copywriter (e.g., "confident but not arrogant", "plain language over jargon", "contractions OK"). Custom section appended after Do's and Don'ts; preserved by spec-compliant consumers per the DESIGN.md spec's "unknown section" rule.
````

**Validation before shipping.** Run these checks against the emitted file:

```bash
# 1. File exists at output root, named exactly DESIGN.md (uppercase)
test -f <brand-root>/DESIGN.md && echo "DESIGN.md present"

# 2. YAML front matter starts the file
head -1 <brand-root>/DESIGN.md | grep -qE '^---$' && echo "YAML front matter starts correctly"

# 3. Required sections present in canonical order
grep -nE "^## (Overview|Colors|Typography|Layout|Shapes|Do's and Don'ts|Voice)" <brand-root>/DESIGN.md
# Should output 7 lines in spec order

# 4. (Optional) Lint with Google's CLI if available — flags broken refs, contrast issues, orphaned tokens
npx @google/design.md lint <brand-root>/DESIGN.md
```

**Quality rule.** If a section has nothing substantive to say, drop the section rather than write placeholder text. The spec preserves omitted sections without erroring. An honest "tokens only" file beats a bloated fake one.

---

### Pitch Deck — Out of Scope

Brand-workshop does **not** emit a pitch-deck template. The `pitch-deck` skill reads
`DESIGN.md` directly and generates its own brand-skinned Reveal.js deck — there
is no intermediate template artifact for it to consume. Pre-emitting a deck here would
duplicate work and fork the styling source of truth.

If the founder wants a deck, recommend they invoke `pitch-deck` (or
`team-composer` with `@startup_strategist` + `@vc_partner`) after this workshop
completes. `pitch-deck` will read the `DESIGN.md` this skill produced.

---

### Output Files

Save all outputs to the resolved brand folder (see Phase 1 Step 0.0),
organized into subfolders so the deliverable reads like a launch-day kit:

```
<brand-root>/
├── brand-brief.md
├── descriptions.md
├── DESIGN.md
├── logos/
│   ├── logo.svg
│   ├── logo-64.png
│   ├── logo-256.png
│   └── logo-512.png
├── favicons/
│   ├── favicon.svg
│   ├── favicon-16.png
│   ├── favicon-32.png
│   ├── favicon-180.png
│   ├── favicon-512.png
│   ├── site.webmanifest
│   └── favicon-install.html
└── social/
    ├── og-image.png
    ├── x-header.png
    ├── linkedin-banner.png
    ├── instagram-square.png
    └── profile-avatar.png
```

Where `<brand-root>` resolves per Phase 1 Step 0.0:

- `docs/startup-kit/brand/` — orchestrated (via `startup-launch-kit`)
- `docs/brand/` — solo default
- `docs/startup-kit/brand/` — solo with `docs/startup-kit/` smart default
- `${STARTUP_KIT_DOCS_ROOT}/brand/` — env-var override

**Minimum viable set:** If time or tooling is constrained, ship in this order of priority:
brand-brief + logo → descriptions → favicons → DESIGN.md → social banners.

Present all files to the user using `present_files`.

---

## Edge Cases

- **User only provides a name and one sentence**: Run a minimal workshop (3 roles). Make
  assumptions explicit in the brief. Ask 1-2 clarifying questions max before proceeding.
- **User has existing brand colors/fonts**: Respect them. The visual designer works within
  those constraints and notes it.
- **User wants multiple logo options**: Generate 2-3 SVG variants and present them for selection.
- **User wants tagline in multiple languages**: Generate the primary in English, then produce
  culturally adapted (not literal) translations. Note: use the i18n-contextual-rewriting skill
  if available for quality translations.
- **Non-Latin scripts in logo**: Flag that SVG text rendering for CJK/Thai/Arabic may need
  font embedding. Recommend logotype as a separate asset for those scripts.

---

## Iteration

After presenting the first output, the user will likely want refinements. Common requests:
- "Make it more playful / serious / minimal / bold"
- "Try a different color palette"
- "I prefer tagline #3 instead"
- "Can you make the negative space more obvious?"

For these, re-run only the affected phase (don't redo the full workshop unless the
direction fundamentally changes). Update the brief to reflect changes.

---

## Closing — suggest the next step (light gate)

After the brand kit is presented, **end the response with a one-line suggestion
to run `validation-canvas` next**:

> *"Brand without a validated market is a logo on a hypothesis. Next step:
> run `validation-canvas` to articulate what you believe about the problem,
> segment, and economics. The canvas reads the DESIGN.md tokens
> automatically from the resolved brand folder."*

This is a **light gate** — informational, not enforced. The founder is free to
ship just the brand kit; this skill's job ends with the kit. But surfacing the
next step prevents the common failure mode where a founder ships a beautiful
identity for an idea they haven't pressure-tested.

---

## Quality Checklist

Before presenting final output, verify:

**Core brand**
- [ ] Tagline is concise (≤8 words ideal), memorable, and relevant
- [ ] Logo works at small sizes (mentally test at 32px)
- [ ] Color palette has sufficient contrast (check primary on white and dark backgrounds)
- [ ] SVG is valid and renders correctly
- [ ] Brief captures the reasoning, not just the output
- [ ] No cultural red flags were ignored

**Extended deliverables**
- [ ] Favicon is legible at 16×16 — no illegible detail; simplified variant used if needed
- [ ] `site.webmanifest` uses the actual brand `theme_color` (palette primary)
- [ ] `favicon-install.html` contains valid, copy-paste-ready `<link>` tags
- [ ] Social banners have ≥8% edge padding on the shorter axis
- [ ] Tagline appears only on hero banners (OG, IG square); profile headers stay clean
- [ ] All PNG banner files match their declared dimensions exactly
- [ ] Descriptions pack: every variant is under its hard character limit (verified, not estimated)
- [ ] Descriptions pack: each variant stands alone — no truncation chains
- [ ] `<brand-root>/DESIGN.md` exists as a **standalone file** — NOT folded into `brand-brief.md` as a section. Filename is exactly `DESIGN.md` (uppercase) per the [Google Labs spec](https://github.com/google-labs-code/design.md). Verify: `test -f <brand-root>/DESIGN.md && echo OK`.
- [ ] DESIGN.md begins with valid YAML front matter (delimited by `---` lines). Verify: `head -1 <brand-root>/DESIGN.md` returns exactly `---`.
- [ ] YAML front matter contains the cross-plugin contract key `colors.primary`. Verify: `grep -E '^  primary:\s*"#' <brand-root>/DESIGN.md` returns one line. Downstream plugins (`validation-canvas`, `riskiest-assumption-test`, `pitch-deck`) bind their accent CSS variable to this token.
- [ ] DESIGN.md sections appear in canonical spec order: Overview → Colors → Typography → Layout → Shapes → Do's and Don'ts → Voice. Verify: `grep -nE "^## (Overview|Colors|Typography|Layout|Shapes|Do's and Don'ts|Voice)" <brand-root>/DESIGN.md` shows the seven headings in order.
- [ ] Design system stays within tokens — no button/form/grid specs (Components and Elevation sections are intentionally omitted at "starter" scope).
- [ ] Empty DESIGN.md sections are dropped rather than filled with placeholder text. The spec preserves omitted sections without erroring.
- [ ] No `deck/` subfolder is emitted under `<brand-root>/`. Brand-workshop does not pre-build a pitch-deck template — `pitch-deck` reads `DESIGN.md` directly. Verify: `[ ! -d <brand-root>/deck ] && echo OK`.

**Shipping**
- [ ] Files are saved under `<brand-root>/` per the folder structure shown in Output Files
- [ ] Smart-default notice surfaced if smart-default fired
- [ ] Files are presented to the user using `present_files`

---

## Cross-Skill Integration

| Skill | When to Use |
|-------|-------------|
| `pitch-deck` (our own) | After this skill, when the founder wants a real investor deck. `pitch-deck` consumes `DESIGN.md` (and optionally `brand-brief.md` + `descriptions.md`) emitted by this skill. Brand-workshop does not pre-emit a deck template — `pitch-deck` owns deck construction end-to-end. Do not duplicate deck-construction logic here. |
| `validation-canvas` (our own) | **Suggested next step (light gate).** After this skill ships the brand kit, the founder is expected to articulate beliefs about market and economics. Brand without a validated market is a logo on a hypothesis. |
| `riskiest-assumption-test` (our own) | Two steps downstream of this skill. Tests the beliefs the validation canvas captures. |
| `theme-factory` (Anthropic) | When the founder wants the design tokens applied to another artifact (landing page, one-pager). Brand-workshop's `DESIGN.md` is intentionally shaped to feed theme-factory. |
| `canvas-design` (Anthropic) | When the founder wants high-fidelity static brand art (posters, campaign keyart) beyond a logo. Brand-workshop's SVG logo is the minimum viable mark, not a full art direction. |
| `algorithmic-art` (Anthropic) | When the brand direction calls for generative / procedural visual motifs rather than a single mark. |
| `docx` (Anthropic) | When the founder wants the brand brief as a polished Word document (e.g., for a board or investor packet). |
| `brand-guidelines` (Anthropic) | **Do not use.** `brand-guidelines` applies Anthropic's own brand look-and-feel; it is not a generic brand-styling skill. |
| `team-composer` (our own) | Instead of this skill when the user wants a *discussion* on brand strategy rather than a launch-ready identity package. Pure positioning / voice conversations live there, not here. |

**Principle:** this skill owns **net-new visual identity** for a business. It
does not refresh existing brands (use `brand-voice:*` skills), does not model
financials, and does not do customer validation. Artifacts downstream of the
brand folder — decks, canvases, landing pages — are owned by their respective
skills, which consume our output as input.

**Graceful degradation:** if a referenced skill is not installed, this skill
still ships a complete brand folder — the downstream integrations are
enhancements, not requirements.
