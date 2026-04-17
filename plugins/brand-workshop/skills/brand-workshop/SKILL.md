---
name: brand-workshop
description: >
  Simulate a collaborative branding team to create logos and taglines from a business overview.
  Use this skill whenever the user asks to create a logo, brand identity, tagline, or brand concept
  for a business, product, app, or project. Also trigger when the user says things like
  "help me brand this," "I need a logo," "come up with a tagline," "brand identity for my app,"
  or provides a business description and asks for visual identity work. This skill runs a
  structured multi-role brainstorming workshop, produces a brand strategy brief (.md),
  a tagline, and a code-generated logo (.svg). Even if the user only asks for a logo or
  only a tagline, use this skill — the full workshop produces better results.
---

# Brand Workshop

A collaborative branding skill that assembles a virtual creative team, runs a structured
brainstorming session, and delivers a brand strategy brief, tagline, and logo.

## Overview

This skill simulates a brand workshop with specialized roles working together. The process
moves through three phases: **Discovery → Concept → Creation**. The output is always:

1. **Brand Strategy Brief** (`.md`) — the team's rationale, concepts explored, and final direction
2. **Tagline** — embedded in the brief and called out prominently
3. **Logo** (`.svg` rendered to `.png`) — code-generated, defaulting to minimalist style

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

### Output Files

Save all outputs to the working directory:

| File | Description |
|------|-------------|
| `brand-brief.md` | Full brand strategy brief |
| `logo.svg` | Vector logo |
| `logo-256.png` | Rendered PNG (256px) |
| `logo-512.png` | Rendered PNG (512px) |
| `logo-64.png` | Favicon-size render |

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

- [ ] Tagline is concise (≤8 words ideal), memorable, and relevant
- [ ] Logo works at small sizes (mentally test at 32px)
- [ ] Color palette has sufficient contrast (check primary on white and dark backgrounds)
- [ ] SVG is valid and renders correctly
- [ ] Brief captures the reasoning, not just the output
- [ ] No cultural red flags were ignored
- [ ] Files are saved and presented to user
