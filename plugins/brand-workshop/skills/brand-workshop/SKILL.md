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
  bios + elevator pitch + boilerplate), a starter design-system.md (tokens only), and a
  self-contained branded pitch-deck template (empty placeholder slides the founder fills in).
  Even if the user only asks for a logo or only a tagline, use this skill — the full workshop
  produces better results.
---

# Brand Workshop

A collaborative branding skill that assembles a virtual creative team, runs a structured
brainstorming session, and delivers a brand strategy brief, tagline, and logo.

## Overview

This skill simulates a brand workshop with specialized roles working together. The process
moves through three phases: **Discovery → Concept → Creation**. The output is always:

1. **Brand Strategy Brief** (`brand-brief.md`) — the team's rationale, concepts explored, and final direction
2. **Tagline** — embedded in the brief and called out prominently
3. **Logo** (`.svg` rendered to `.png`) — code-generated, defaulting to minimalist style
4. **Favicon Pack** — `favicon.svg`, raster sizes (16/32/180/512), `site.webmanifest`, and a copy-paste HTML `<link>` install snippet
5. **Social Banner Set** — Open Graph (1200×630), X header (1500×500), LinkedIn banner (1584×396), Instagram square (1080×1080), profile avatar (400×400)
6. **Descriptions Pack** (`descriptions.md`) — tagline + short/medium/long bios + elevator pitch + press boilerplate, all matched to brand voice
7. **Starter Design System** (`design-system.md`) — tokens only: color, typography, spacing, radius, and voice principles (no component specs)
8. **Branded Pitch-Deck Template** (`pitch-template.html`) — a self-contained Reveal.js deck with empty placeholder slides, brand-skinned, that the founder fills in

Scope boundary: pitch-deck *content* (filled slides) and the Business Model Canvas are intentionally out of scope — see Skill Boundaries below.

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

> **Future refactor note (Option D):** Today this skill has its own internal team
> (see Phase 2). Long-term, this skill could invoke `team-composer` as the
> discussion engine and focus only on the Creation phase (logo SVG, brief
> assembly). That refactor is not scheduled — revisit only if the role catalog
> drift between the two skills causes real maintenance pain. When revisited,
> unify role tag format (`@hyphen-case` here vs. `@snake_case` in team-composer).

> **Planned sibling skills (same plugin):** `pitch-deck` (founder-filled content
> that consumes the brand assets produced here) and `business-model-canvas`
> (@startup_strategist territory). They are intentionally not folded into this
> skill: both require founder inputs — traction, revenue model, cost structure,
> ask size — that are out of scope for a brand workshop. When those skills ship,
> add them to the "Use instead" table above. An umbrella `startup-launch-kit`
> meta-skill may later orchestrate all three.

---

## Phase 1: Discovery

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

### Design System (Starter Tokens)

Output `design-system.md` capturing the tokens established in the workshop. Scope is
deliberately narrow: **tokens, not components**. Button styles, form fields, grids, and motion
depend on the engineering stack this skill does not choose — the implementing team adds those.

**File structure:**

```markdown
# Design System — [Brand Name]

## Color Tokens
- Primary / Secondary / Accent (hex + usage guidance)
- Neutrals (background, surface, text-primary, text-secondary, border)
- Semantic (success, warning, danger, info) harmonized with palette

## Typography
- Families: display, body, mono (with fallback stacks)
- Weights in use
- Type scale: h1 / h2 / h3 / body / small / caption with px and rem values
- Line-height and tracking guidance

## Spacing Scale
4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 (or a modular scale that fits the brand)

## Radius Scale
0 / 4 / 8 / 16 / full

## Voice & Tone Principles
3–5 bullet rules from the copywriter (e.g., "confident but not arrogant",
"plain language over jargon", "contractions OK").

## Out of Scope
Buttons, forms, cards, grid systems, motion — these depend on the
implementation stack and should be added by the engineering team that builds the product.
```

**Quality rule:** If a section has nothing substantive to say, drop the section rather than
write placeholder text. An honest "tokens only" system beats a bloated fake one.

---

### Branded Pitch-Deck Template

Output a self-contained HTML deck the founder fills with their own content. **This is a
template, not a pitch** — content slides contain `[fill in: …]` prompts in muted type. Actual
investor-ready pitch construction belongs to the forthcoming `pitch-deck` sibling skill.

**File:** `deck/pitch-template.html`

**Contract (from `team-composer` cross-skill rules):**

- Single file — Reveal.js, inline CSS/JS, base64-embedded images/fonts, zero network dependencies
- Responsive: projector + laptop + mobile preview all legible
- First-class print-as-PDF via CSS paged media
- Keyboard navigation (← → Space Esc)
- Semantic HTML with aria landmarks
- AAA contrast for projection

**Slide structure (all content slots empty):**

1. Title — logo + company name + tagline + `[presenter · date]`
2. Problem — `[fill in: the problem you solve]`
3. Solution — `[fill in: how you solve it]`
4. Why Now — `[fill in: the timing case]`
5. Market — `[fill in: TAM / SAM / SOM]`
6. Product — `[fill in: demo screenshots or key feature call-outs]`
7. Business Model — `[fill in: how you make money]`
8. Traction — `[fill in: key metrics and growth]`
9. Team — `[fill in: founders and key hires]`
10. Ask — `[fill in: round size and use of funds]`
11. Thank You — logo + contact

**Applied brand tokens:**

- Slide backgrounds use brand neutral or primary
- Headings use the display typeface from the design system
- Body copy uses the body typeface from the design system
- Accent dividers / callouts use the accent color from the palette

**Required disclaimer on the title slide (muted footnote):**

> "Template — content to be filled by the founder. For investor-ready pitch
> construction, use the `pitch-deck` skill (forthcoming) or `team-composer`
> with `@startup_strategist` + `@vc_partner`."

**Quality rule:** Never fabricate traction, team names, or market numbers. Every content slot
ships as a literal `[fill in: …]` prompt. The only "real" content is brand identity
(logo, colors, typography, tagline).

---

### Output Files

Save all outputs to the working directory, organized into folders so the deliverable reads
like a launch-day kit:

```
/brand-brief.md
/descriptions.md
/design-system.md
/logos/
  logo.svg
  logo-64.png
  logo-256.png
  logo-512.png
/favicons/
  favicon.svg
  favicon-16.png
  favicon-32.png
  favicon-180.png
  favicon-512.png
  site.webmanifest
  favicon-install.html
/social/
  og-image.png
  x-header.png
  linkedin-banner.png
  instagram-square.png
  profile-avatar.png
/deck/
  pitch-template.html
```

**Minimum viable set:** If time or tooling is constrained, ship in this order of priority:
brand-brief + logo → descriptions → favicons → design-system → social banners → deck template.
Never ship the deck template without the logo and design-system — it has nothing to render from.

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
- [ ] Design system stays within tokens — no button/form/grid specs
- [ ] Empty design-system sections are dropped rather than filled with placeholder text
- [ ] Deck template is labelled as a template; every content slot is a literal `[fill in: …]` prompt
- [ ] Deck renders as one self-contained HTML file (no external CSS/JS/font requests)
- [ ] Deck title slide includes the "forthcoming `pitch-deck` skill" disclaimer

**Shipping**
- [ ] Files are saved into the folder structure shown in Output Files
- [ ] Files are presented to the user using `present_files`
