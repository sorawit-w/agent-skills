<p align="center">
  <img src="https://raw.githubusercontent.com/sorawit-w/agent-skills/main/assets/brand-workshop-li.svg" alt="brand-workshop — logo, tagline, brief, built by a team" width="100%"/>
</p>

# brand-workshop

A Claude Code skill that assembles a virtual creative team, runs a structured brand workshop across Discovery → Concept → Creation, and ships a launch-ready brand identity package: brand strategy brief (`.md`), tagline, code-generated logo (`.svg` rendered to `.png`), favicon pack with HTML install snippet, social banner set (OG / X / LinkedIn / Instagram), descriptions pack (bios + elevator pitch + boilerplate), a starter design-system.md (tokens only), and a self-contained branded pitch-deck template (empty placeholder slides the founder fills in).

## Why this exists

"Give me a logo for my startup" is almost never really about a logo. It's about positioning, voice, archetype, and a visual system that holds up at 32px and on a billboard. Skip the positioning work and the logo is just a doodle.

Most one-shot branding prompts collapse the whole chain into a single pass — the model picks a shape, names a color, writes a slogan, and stops. No rationale, no archetype, no rejected alternatives, and the tagline and the logo were never in the same conversation with each other.

The fix is process, not cleverness: a small creative team, each seat with a real job, moving through Discovery → Concept → Creation, with the tagline and logo converging from shared strategy rather than arriving out of order.

That's what this does.

## What it does

- **Runs a proper Discovery pass** — name, overview, vision, mission, audience, existing assets, language, style preference — and asks concisely when inputs are missing. State assumptions, proceed; don't stall.
- **Defaults to minimalist with negative space** when no logo style is given. The default is a design choice, not a shrug: it works at 32px, survives color/mono conversion, and carries meaning in what it omits.
- **Assembles a creative team with distinct roles** — @senior-brand-strategist, @senior-copywriter, @lead-visual-designer, @product-designer, @growth-strategist, @regional-cultural-advisor, @lead-ux-ui-designer. Roles scale to the project: minimum 3 for a simple mark, full team for app/product branding, plus add-ons (e.g., accessibility specialist) when context demands.
- **Runs a five-step Concept workshop** — Strategic Foundation → Verbal Exploration → Visual Direction → Cultural & Market Check → Convergence (strategist-led vote). Each role speaks in first person with a role tag; the full transcript is preserved in the brand brief.
- **Generates the logo as code** — minimalist geometry, 2–3 colors from the chosen palette, viewBox scaling, favicon-to-billboard viable. SVG first, PNG renders at 64 / 256 / 512 via Cairo/librsvg. No raster effects, no opaque image-gen by default.
- **Generates a favicon pack with drop-in HTML snippet** — `favicon.svg`, raster sizes (16 / 32 / 180 / 512), `site.webmanifest`, and a copy-paste `<link>` block that uses the brand's actual `theme_color`. If fine detail disappears at 16×16, authors a favicon-optimized variant instead of scaling a mark that becomes illegible.
- **Ships a social banner set** — Open Graph 1200×630, X header 1500×500, LinkedIn banner 1584×396, Instagram square 1080×1080, profile avatar 400×400. Generous edge padding, tagline only on hero banners, light/dark variants when the palette allows.
- **Assembles a descriptions pack** — tagline, short/medium/long bios, elevator pitch, press boilerplate, all in the voice established in the brief. Each variant stands alone (no truncation chains) and is verified under its platform's hard character limit.
- **Ships a starter design system — tokens only** — `design-system.md` with color tokens, typography scale, spacing scale, radius scale, and voice principles. Explicitly not a component library: buttons, forms, and grids depend on the implementing team's stack and aren't this skill's call.
- **Outputs a branded pitch-deck template — a template, not a pitch** — self-contained Reveal.js HTML, zero network dependencies, print-as-PDF friendly, brand-skinned. Every content slot ships as a literal `[fill in: …]` prompt. Never fabricates traction, team names, or market numbers.
- **Produces a brand strategy brief** — executive summary, inputs, workshop transcript, final concept (tagline + logo description + color palette table + typography), and **rejected alternatives with reasoning**. The brief records the thinking, not just the output.
- **Files every deliverable into a launch-ready kit** — `brand-brief.md`, `descriptions.md`, `design-system.md`, plus folders for logos, favicons, social banners, and the deck template — all presented to the user together. Minimum-viable order if time or tooling is constrained: brand-brief + logo → descriptions → favicons → design-system → social banners → deck template.
- **Iterates surgically** — "more playful," "different palette," "tagline #3 instead" re-runs only the affected phase and updates the brief. Full workshop only re-runs when direction fundamentally changes.

## What it doesn't do

- **General project brainstorming.** If branding is one of many dimensions in a product decision (positioning + product + GTM + brand), reach for [`team-composer`](https://github.com/sorawit-w/agent-skills/tree/main/skills/team-composer) instead. This skill is a deliverable factory, not a thinking partner.
- **Product or feature naming in isolation.** "Name this product" belongs to `team-composer` with `@naming_specialist`. This skill names when the tagline requires it, not as a standalone service.
- **Brand voice reviews / style audits.** Those belong to `team-composer` with `@humorist` + `@senior_copywriter`, or to a dedicated review skill.
- **AI-generated imagery by default.** Raster image generation is opt-in only (via Hugging Face `dynamic_space`), never the default path. The skill exists to ship *vector* identity you can actually ship.
- **Replace human review on regulated or trademarked marks.** The cultural advisor flags obvious pitfalls, but the skill explicitly recommends human trademark and legal review before use.
- **Fill in your pitch deck.** The deck template ships brand-skinned and empty — the content is the founder's to write. Traction numbers, team names, ask size, and use of funds belong to the planned `pitch-deck` companion plugin or to `team-composer` with `@startup_strategist` + `@vc_partner`.
- **Produce a Business Model Canvas.** Deliberately out of scope. A BMC needs revenue model, cost structure, and key-partner inputs this skill doesn't ask for. Use the planned `business-model-canvas` companion plugin or `team-composer` instead.

## When to use it

- You have a new product, app, or startup and the deliverable you actually need is a **launch-ready identity kit** — logo, tagline, brief, favicons, social banners, descriptions, a starter design-system, and a brand-skinned deck template the founder fills in — handed off as a single bundle.
- You want the positioning work *done* — archetype, attributes, differentiation — not just a pretty mark.
- You want the tagline and the logo to have been in the same conversation with each other. The convergence step is the point.
- You want rejected alternatives documented, so refinement is a conversation, not a guessing game.

## When not to use it

- **Mixed-scope product decisions.** If the question is "how should we build/position/go-to-market this, *and* what's the brand look like?" — start with `team-composer`. It will call `brand-workshop` only if and when a pure identity deliverable is what's needed.
- **Voice / microcopy audits.** Wrong tool. Use `design:ux-copy` or `marketing:brand-review` instead.
- **Pure logo refresh with fixed strategy.** If the strategy already exists and you just need a mark, the Concept workshop is overhead. You can still use the skill, but it will spend more of its budget than necessary.

## How it works — 3 phases

1. **Discovery.** Gather inputs; ask concisely when essentials are missing; fall back to minimalist-with-negative-space as the default style; present `references/logo-styles.md` options on request.
2. **Concept.** Assemble the right roles (scale with the project), then run 5 workshop steps:
   - **Strategic Foundation** (strategist) — positioning, 2–3 archetypes, 3–5 brand attributes.
   - **Verbal Exploration** (copywriter) — 5–7 tagline candidates, tone, linguistic flags.
   - **Visual Direction** (visual designer + UX/UI designer) — 2–3 logo concepts, palette with hex values, typography, favicon/dark-mode viability.
   - **Cultural & Market Check** (cultural advisor + growth strategist) — symbolism pitfalls, memorability, market fit.
   - **Convergence** (strategist-led) — vote, synthesize, declare final tagline + logo direction.
3. **Creation.** Write the brand strategy brief (with full transcript and rejected alternatives). Generate the logo as SVG and render PNGs at 64 / 256 / 512. Build the favicon pack and its HTML install snippet. Render the social banner set. Assemble the descriptions pack from the copywriter's draft. Emit the starter `design-system.md`. Generate the branded pitch-deck template with empty placeholder slides. Present every file together, organized into the launch-kit folder structure.

Optional iteration loop: re-run only the affected phase when the user refines ("more serious," "swap the palette," "tagline #3 please"); update the brief to reflect the change.

## What the output looks like

A single launch-ready bundle, every file saved and presented:

```
/
├── brand-brief.md      — Executive Summary, Inputs, Workshop Transcript, Final Concept, Rejected Alternatives
├── descriptions.md     — Tagline + short/medium/long bios + elevator pitch + press boilerplate
├── design-system.md    — Color, typography, spacing, radius, voice — tokens only
├── logos/              — logo.svg, logo-64.png, logo-256.png, logo-512.png
├── favicons/           — favicon.svg, 16/32/180/512 PNGs, site.webmanifest, favicon-install.html
├── social/             — og-image, x-header, linkedin-banner, instagram-square, profile-avatar
└── deck/               — pitch-template.html (branded, empty, self-contained Reveal.js)
```

The tagline is called out prominently in the brief. Symbolism, color rationale, and palette usage are explained inline — the brief records thinking, not just output. Every asset downstream of the brief is derived from the same workshop decisions, so the bundle is consistent with itself by construction: the favicon is the logo simplified, the banners use the same palette and typography, the descriptions share the tagline's voice, and the deck is skinned with the design-system tokens.

## Design choices worth knowing

- **Minimalist + negative space as the default, not the fallback.** Most logos compete against themselves at small sizes. A default that starts from clean geometry and hidden meaning wins the favicon test for free, and is easier to refine later than to rescue.
- **Convergence is strategist-led, not democratic.** Each role votes, the strategist synthesizes. A flat vote produces plausible-sounding averages; a single owner with transparent reasoning is what turns a workshop into a decision.
- **Rejected alternatives are part of the brief.** The concepts you passed over are half the value — they tell the next reviewer what the brand *deliberately isn't*. Skipping this section is a silent way to lose the rationale.
- **Vector-first, raster on request.** AI image generation is opt-in because the default deliverable needs to be usable: an SVG scales, survives color conversions, and edits without regeneration. Raster marks are a liability masquerading as polish.
- **Cultural & market check is a gate, not a footnote.** It sits between visual direction and convergence deliberately. A beautiful mark that lands badly in one of the target markets is a failed brief, and that catch happens before the vote, not after.
- **Narrow cross-skill boundaries.** `brand-workshop` does identity deliverables; `team-composer` handles multi-dimensional product thinking; naming / voice / copy audits belong to more specialized skills. The skill's boundary table spells out which request belongs where so neither side over-reaches.
- **Templates ship empty on purpose.** The branded pitch-deck template leaves every content slot as a literal `[fill in: …]` prompt. Brand is real content; traction numbers, team names, market sizing, and ask size are the founder's to write. Fabricating those turns a deliverable into a liability — and a "filled" deck is the wrong skill's output anyway (that's the planned `pitch-deck` companion plugin).
- **Tokens, not components.** `design-system.md` stops at color, type, spacing, radius, and voice. Button variants, form styles, grids, and motion depend on a framework choice this skill deliberately doesn't make — they belong to the implementing team, not to a brand workshop.

## Install

This skill is distributed as a [Claude Code](https://docs.claude.com/en/docs/claude-code) plugin inside the [`sorawit-w/agent-skills`](https://github.com/sorawit-w/agent-skills) marketplace. From Claude Code or Cowork:

```
/plugin marketplace add sorawit-w/agent-skills
/plugin install brand-workshop@sorawit-w
```

Once installed, Claude picks the skill up automatically from the description in its `SKILL.md` frontmatter. Invocation triggers on phrases like "help me brand this," "I need a logo," "design a brand identity," "come up with a tagline," "brand concept for my app," or providing a business overview and asking for visual identity work.

## Cross-skill integration

| Skill | When it kicks in |
|---|---|
| [`team-composer`](https://github.com/sorawit-w/agent-skills/tree/main/skills/team-composer) | Preferred when branding is one of several dimensions in a product decision. `team-composer` may in turn hand off to this skill if the scope narrows to pure identity. |
| `design:ux-copy` | When the copy work is microcopy / error states / CTAs rather than brand voice. |
| `marketing:brand-review` | For reviewing existing content against an already-established brand. |
| `i18n-contextual-rewriting` | When the tagline needs culturally adapted translations beyond English. |
| `theme-factory` | When downstream deliverables (decks, landing pages) need to apply the produced identity system consistently. |
| `canvas-design` / `pptx` (fallback only) | Only when the user needs a static brand poster or a deck built on top of the produced identity. |

The principle: this skill owns the launch-ready identity kit. Hand off to specialized skills for everything downstream rather than attempting them inline.

## Companion plugins

This skill is intentionally scoped to brand identity. Two companion plugins ship in this repo to handle startup deliverables that overlap brand but require different inputs from the founder. Each is its own plugin (matching the one-plugin-per-skill pattern used across the repo) rather than folded into `brand-workshop`:

- **[`business-model-canvas`](../business-model-canvas/README.md)** — produces a 9-block BMC from founder inputs (customer segments, value propositions, channels, revenue model, cost structure, key partners, activities, resources). `@startup_strategist` territory with `@vc_partner` read-tests. Outputs `business-model.md` (editable source of truth) + `business-model.html` (self-contained visual canvas).
- **[`pitch-deck`](../pitch-deck/README.md)** — fills in a real investor deck from founder inputs (problem, solution, market, traction, team, ask). Reads the `brand-kit/` produced here for visual tokens and `business-model.md` if present to seed content. Enforces required-slot gating and refuses to ship a deck missing any of the four cardinal slots (TAM-only, traction without time axis, team without faces, vague ask). Outputs a single self-contained `pitch/deck.html`.

An umbrella `startup-launch-kit` plugin may later orchestrate `brand-workshop` → `business-model-canvas` → `pitch-deck` as a single founder-facing flow. Not scheduled yet; until it ships, run the three plugins in order in the same working directory — they compose via shared folder conventions (`brand-kit/`, `business-model.md`, `pitch/`) rather than a manifest.

## Status and scope

v0.2. The role catalog covers the core branding team plus a regional cultural advisor. The deliverable set is now a launch-ready kit — logo, tagline, brief, favicons, social banners, descriptions, starter design-system, and a brand-skinned deck template. Minimalist-with-negative-space is the default logo style; `references/logo-styles.md` documents the alternatives available on request.

- **Supported:** product / app / startup identity packages, iteration on existing concepts, multi-language taglines (with a note about font embedding for CJK/Thai/Arabic logotypes), HTML install snippet for favicons, self-contained Reveal.js deck template.
- **Adaptable:** existing brand assets are respected as constraints; visual designer works within provided palettes/typography; the starter design-system can be extended by the implementing team with components in their framework of choice.
- **Not supported:** trademark clearance, registered-mark review, AI image generation as default, live iterative pairing across every round, filled pitch-deck content, Business Model Canvas.

## Contributions

Not accepting external contributions right now. Feel free to fork.

## License

MIT — see the [LICENSE](https://github.com/sorawit-w/agent-skills/blob/main/LICENSE) file at the repo root.
