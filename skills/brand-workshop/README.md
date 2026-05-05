<p align="center">
  <img src="https://raw.githubusercontent.com/sorawit-w/agent-skills/main/assets/brand-workshop-li.svg" alt="brand-workshop — logo, tagline, brief, built by a team" width="100%"/>
</p>

# brand-workshop

A Claude Code skill that assembles a virtual creative team, runs a structured brand workshop across Discovery → Concept → Creation, and ships a launch-ready brand identity package: brand strategy brief (`.md`), tagline, code-generated logo (`.svg` rendered to `.png`), favicon pack with HTML install snippet, social banner set (OG / X / LinkedIn / Instagram), descriptions pack (bios + elevator pitch + boilerplate), and a starter `DESIGN.md` (tokens only). For pitch decks, hand off to the companion [`pitch-deck`](../pitch-deck/README.md) plugin, which reads `DESIGN.md` directly.

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
- **Ships a starter design system — tokens only** — `DESIGN.md` with color tokens, typography scale, spacing scale, radius scale, and voice principles. Explicitly not a component library: buttons, forms, and grids depend on the implementing team's stack and aren't this skill's call. Downstream plugins (`validation-canvas`, `riskiest-assumption-test`, `pitch-deck`) read these tokens directly — no intermediate deck or canvas template is emitted here.
- **Produces a brand strategy brief** — executive summary, inputs, workshop transcript, final concept (tagline + logo description + color palette table + typography), and **rejected alternatives with reasoning**. The brief records the thinking, not just the output.
- **Files every deliverable into a launch-ready kit** — `brand-brief.md`, `descriptions.md`, `DESIGN.md`, plus folders for logos, favicons, and social banners — all presented to the user together. Minimum-viable order if time or tooling is constrained: brand-brief + logo → descriptions → favicons → DESIGN.md → social banners.
- **Iterates surgically** — "more playful," "different palette," "tagline #3 instead" re-runs only the affected phase and updates the brief. Full workshop only re-runs when direction fundamentally changes.

## What it doesn't do

- **General project brainstorming.** If branding is one of many dimensions in a product decision (positioning + product + GTM + brand), reach for [`team-composer`](https://github.com/sorawit-w/agent-skills/tree/main/skills/team-composer) instead. This skill is a deliverable factory, not a thinking partner.
- **Product or feature naming in isolation.** "Name this product" belongs to `team-composer` with `@naming_specialist`. This skill names when the tagline requires it, not as a standalone service.
- **Brand voice reviews / style audits.** Those belong to `team-composer` with `@humorist` + `@senior_copywriter`, or to a dedicated review skill.
- **AI-generated imagery by default.** Raster image generation is opt-in only (via Hugging Face `dynamic_space`), never the default path. The skill exists to ship *vector* identity you can actually ship.
- **Replace human review on regulated or trademarked marks.** The cultural advisor flags obvious pitfalls, but the skill explicitly recommends human trademark and legal review before use.
- **Emit a pitch deck or deck template.** Pitch decks are owned end-to-end by the companion [`pitch-deck`](../pitch-deck/README.md) plugin, which reads `DESIGN.md` directly and generates its own brand-skinned Reveal deck. Hand off there for both the scaffold and the filled content — don't ask this skill for either.
- **Produce a validation canvas (Lean Canvas + VPC).** Deliberately out of scope. A canvas needs revenue model, cost structure, and customer-job inputs this skill doesn't ask for. Use the `validation-canvas` companion skill (next step in the pipeline) or `team-composer` instead. For a 9-block Osterwalder BMC specifically, use `team-composer` with `@startup_strategist`.

## When to use it

- You have a new product, app, or startup and the deliverable you actually need is a **launch-ready identity kit** — logo, tagline, brief, favicons, social banners, descriptions, and a starter `DESIGN.md` — handed off as a single bundle. (For decks, follow up with the companion `pitch-deck` plugin.)
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
3. **Creation.** Write the brand strategy brief (with full transcript and rejected alternatives). Generate the logo as SVG and render PNGs at 64 / 256 / 512. Build the favicon pack and its HTML install snippet. Render the social banner set. Assemble the descriptions pack from the copywriter's draft. Emit the starter `DESIGN.md`. Present every file together, organized into the launch-kit folder structure.

Optional iteration loop: re-run only the affected phase when the user refines ("more serious," "swap the palette," "tagline #3 please"); update the brief to reflect the change.

## What the output looks like

A single launch-ready bundle, every file saved and presented:

```
/
├── brand-brief.md      — Executive Summary, Inputs, Workshop Transcript, Final Concept, Rejected Alternatives
├── descriptions.md     — Tagline + short/medium/long bios + elevator pitch + press boilerplate
├── DESIGN.md    — Color, typography, spacing, radius, voice — tokens only
├── logos/              — logo.svg, logo-64.png, logo-256.png, logo-512.png
├── favicons/           — favicon.svg, 16/32/180/512 PNGs, site.webmanifest, favicon-install.html
└── social/             — og-image, x-header, linkedin-banner, instagram-square, profile-avatar
```

The tagline is called out prominently in the brief. Symbolism, color rationale, and palette usage are explained inline — the brief records thinking, not just output. Every asset downstream of the brief is derived from the same workshop decisions, so the bundle is consistent with itself by construction: the favicon is the logo simplified, the banners use the same palette and typography, and the descriptions share the tagline's voice. Downstream plugins (`validation-canvas`, `riskiest-assumption-test`, `pitch-deck`) skin themselves from `DESIGN.md` directly.

## Design choices worth knowing

- **Minimalist + negative space as the default, not the fallback.** Most logos compete against themselves at small sizes. A default that starts from clean geometry and hidden meaning wins the favicon test for free, and is easier to refine later than to rescue.
- **Convergence is strategist-led, not democratic.** Each role votes, the strategist synthesizes. A flat vote produces plausible-sounding averages; a single owner with transparent reasoning is what turns a workshop into a decision.
- **Rejected alternatives are part of the brief.** The concepts you passed over are half the value — they tell the next reviewer what the brand *deliberately isn't*. Skipping this section is a silent way to lose the rationale.
- **Vector-first, raster on request.** AI image generation is opt-in because the default deliverable needs to be usable: an SVG scales, survives color conversions, and edits without regeneration. Raster marks are a liability masquerading as polish.
- **Cultural & market check is a gate, not a footnote.** It sits between visual direction and convergence deliberately. A beautiful mark that lands badly in one of the target markets is a failed brief, and that catch happens before the vote, not after.
- **Narrow cross-skill boundaries.** `brand-workshop` does identity deliverables; `team-composer` handles multi-dimensional product thinking; naming / voice / copy audits belong to more specialized skills. The skill's boundary table spells out which request belongs where so neither side over-reaches.
- **Decks are out of scope.** Both the deck scaffold *and* the filled investor content belong to the companion `pitch-deck` plugin, which consumes `DESIGN.md` directly. Keeping decks out of this skill avoids duplicating styling logic and forking the source-of-truth for brand tokens.
- **Tokens, not components.** `DESIGN.md` stops at color, type, spacing, radius, and voice. Button variants, form styles, grids, and motion depend on a framework choice this skill deliberately doesn't make — they belong to the implementing team, not to a brand workshop.

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

This skill is intentionally scoped to brand identity. It is **step 1 of 5** in the startup pipeline. Each downstream skill is its own plugin (matching the one-plugin-per-skill pattern used across the repo) rather than folded into `brand-workshop`:

- **[`validation-canvas`](../validation-canvas/README.md)** — suggested next step (light gate). Produces a Lean Canvas + Value Proposition Canvas combined artifact from founder inputs. `@startup_strategist` territory with `@vc_partner` + `@finance_manager` + `@senior_product_manager` read-tests. Outputs `validation-canvas.md` + `validation-canvas.html`.
- **[`riskiest-assumption-test`](../riskiest-assumption-test/README.md)** — two steps downstream. Converts canvas Stress Tests into falsifiable hypotheses with success/kill criteria and chosen test methods. Outputs `rat/assumption-test-plan.md` + interactive `rat/test-matrix.html`.
- **[`pitch-deck`](../pitch-deck/README.md)** — three steps downstream. Fills in a real investor deck. Reads the `brand-kit/`, `validation-canvas.md`, and `rat/assumption-test-plan.md` to seed content. Enforces required-slot gating; heavy-gated on populated RAT Results. Outputs a single self-contained `pitch/deck.html`.
- **[`startup-grill`](../startup-grill/README.md)** — last step. Adversarially probes the deck with a kill-report verdict and an iteration-evidence check.

An umbrella `startup-launch-kit` plugin may later orchestrate the full pipeline as a single founder-facing flow. Not scheduled yet; until it ships, run the five plugins in order in the same working directory — they compose via shared folder conventions (`brand-kit/`, `validation-canvas.md`, `rat/`, `pitch/`, `grill/`) rather than a manifest.

## Status and scope

v3.0.0. The role catalog covers the core branding team plus a regional cultural advisor. The deliverable set is a launch-ready identity kit — logo, tagline, brief, favicons, social banners, descriptions, and a starter `DESIGN.md` ([Google Labs spec](https://github.com/google-labs-code/design.md), alpha). Validation canvases, assumption tests, pitch decks, and adversarial grilling are out of scope: the `validation-canvas`, `riskiest-assumption-test`, `pitch-deck`, and `startup-grill` companion plugins read `DESIGN.md` directly and own those deliverables end-to-end. Minimalist-with-negative-space is the default logo style; `references/logo-styles.md` documents the alternatives available on request.

- **Supported:** product / app / startup identity packages, iteration on existing concepts, multi-language taglines (with a note about font embedding for CJK/Thai/Arabic logotypes), HTML install snippet for favicons.
- **Adaptable:** existing brand assets are respected as constraints; visual designer works within provided palettes/typography; the starter `DESIGN.md` can be extended by the implementing team with components in their framework of choice.
- **Not supported:** trademark clearance, registered-mark review, AI image generation as default, live iterative pairing across every round, pitch-deck construction (scaffold *or* filled content), Business Model Canvas.

## Contributions

Not accepting external contributions right now. Feel free to fork.

## License

MIT — see the [LICENSE](https://github.com/sorawit-w/agent-skills/blob/main/LICENSE) file at the repo root.
