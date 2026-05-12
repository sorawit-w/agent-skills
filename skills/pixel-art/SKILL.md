---
name: pixel-art
description: >
  Generate hi-fidelity pixel art images — scenes, characters, buildings,
  nature, and title cards — from a short brief, with a built-in design
  system (palette tokens, density specs, composition rules, font catalog,
  anti-pattern checklist) so the user does not have to re-specify the
  style every time. Two style modes — `hi-fi` (default, painterly
  high-density pixel art like medieval harbor scenes and tavern
  interiors) and `lo-fi` (scanlined warm-paper banner aesthetic, matching
  the agent-skills repo banners). Generation is **capability-gated**:
  when a connected image generator MCP is available (Z-image Turbo,
  Imagen / Nano Banana, OpenAI Image, etc.), the skill generates inline;
  otherwise it emits a copy-pasteable, model-agnostic prompt brief the
  user runs in their preferred tool (Midjourney, DALL-E, SDXL, Imagen,
  any other). Title cards additionally have a code-based SVG path using
  VT323 (default) plus a curated pixel-font catalog. Triggers on phrases
  like "pixel art", "pixel-art [scene/character/building/title card]",
  "hi-fi pixel art", "lo-fi pixel banner", "VT323 title card", "8-bit
  banner", "make this a pixel-art image", "generate a pixel-art harbor",
  or when the user provides a hi-density pixel-art reference and asks
  for "this style". Does NOT trigger on vector illustration, SVG icon
  design, logo work (use `brand-workshop`), photo-real image generation,
  algorithmic / generative art with p5.js (use Anthropic's
  `algorithmic-art`), or chart and dashboard rendering (use the data
  visualization skills). Mirrors `algorithmic-art`'s IP guardrail —
  never reference living artists by name in prompts; produces original
  compositions only.
---

# pixel-art

> **🚧 Status: BETA** — first release (v3.10.x). Smoke-tested on
> Z-image Turbo for one subject (scenes); pre-shipment
> `skill-evaluator` audit returned 17/17 with named coverage caveats
> (author/auditor bias, several untested paths — see CHANGELOG v3.10.2
> for the gap list). Expect adherence patches as more subject
> categories, generators, and density targets get dogfooded in real
> use. Use freely; expect rough edges.

A pocket-sized pixel-art studio. You hand it a short brief — *"medieval
harbor at dusk"*, *"tavern interior with fireplace"*, *"Whispers of the
Flame title card in VT323"* — and it returns a finished image (when an
image-gen MCP is connected) or a model-agnostic prompt brief you can
paste into the generator of your choice. The style is locked in
`references/` so you do not have to re-describe palette, density,
composition, lighting, or typography every time.

## When to use this skill

- *"Create a pixel-art [scene / character / building / forest / title card] of …"*
- *"Make a hi-fi pixel-art harbor at dusk."*
- *"Generate a lo-fi pixel banner like the agent-skills banners."*
- *"Title card for 'Whispers of the Flame' in VT323."*
- *"I want this image in the same hi-density pixel style as before."*
- *"Make this image a pixel-art version of itself."*
- *"Build me a pixel-art splash screen for my game scene."*

If the user provides a reference screenshot and says *"this style"*,
treat it as stylistic intent (palette / density / mood). Do **not**
copy the reference image; produce an original composition that hits
the same craft markers (see `references/anti-patterns.md`).

## When NOT to use this skill

- **Vector illustration / icon design** — use `canvas-design` or
  hand-author SVG. Pixel art is raster-first; vectors are a different craft.
- **Logo or brand identity package** — route to `brand-workshop`.
- **Photo-realistic generation** — wrong style; use a general image-gen
  model directly with a non-pixel-art prompt.
- **Algorithmic / generative art with p5.js, particle systems, flow fields**
  — use Anthropic's `algorithmic-art` skill.
- **Charts, dashboards, data visualization** — use the data viz skills.
- **Rasterizing an existing photograph as pixel art** — out of scope for
  v1; consider an external "pixelate" filter instead.

## Phase 0 — Style mode

Two modes. **Default is `hi-fi`.** Confirm only if the user's brief
is ambiguous (e.g., "make a pixel-art banner" — banners are usually
lo-fi here).

| Mode | Use when | Anchor |
|---|---|---|
| `hi-fi` | Game-style scenes, character art, fantasy interiors, painterly title cards, anything where craft density matters | Kiang's medieval harbor + tavern reference screenshots |
| `lo-fi` | Repo banners, blog headers, retro UI mockups, anything that should feel like a CRT scanline + warm-paper background | agent-skills banners (e.g., `team-composer-li.svg`) |

The selected mode controls **which palette block** loads from
`references/palette.md` and **which density profile** loads from
`references/density.md`. Composition rules and font catalog are shared.

## Phase 1 — Subject detection

Map the user's brief to one of five subjects. Each subject has its own
prompt template in `templates/` and (when relevant) its own composition
rules in `references/composition.md`.

| Subject | Template | Examples |
|---|---|---|
| `scene` | `templates/scene-prompt.md` | Harbor at dusk, tavern interior, twilight forest |
| `character` | `templates/character-prompt.md` | Knight, merchant, traveler, NPC portrait |
| `building` | `templates/building-prompt.md` | Inn, castle gate, lighthouse, market stall |
| `nature` | `templates/nature-prompt.md` | Forest clearing, river bend, mountain pass |
| `title-card` | `templates/title-card-prompt.md` + `templates/title-card.svg` | "Whispers of the Flame", chapter title, game splash |

If the brief mixes subjects ("character in a forest"), pick the
**dominant subject** (here: `scene`, with the character as a
foreground element). Note the secondary subject in the prompt's
composition block.

## Phase 2 — Compose the prompt

Read the following references **once** at the start of the task:

1. `references/style-modes.md` — confirms hi-fi vs lo-fi profile
2. `references/palette.md` — named palettes; pick one by mood
3. `references/density.md` — pixel density + dithering rules per mode
4. `references/composition.md` — layout, eye-line, light-source rules
5. `references/lighting.md` — time-of-day + mood + color-temp guidance
6. `references/anti-patterns.md` — craft-marker checklist + what to avoid
7. `references/fonts.md` — only if subject is `title-card`

Then load the subject template from `templates/` and fill its prompt
blocks. The **universal block structure** is the same across subjects:

```
[STYLE]      hi-density pixel art / lo-fi scanlined pixel art
[PALETTE]    <named palette> — <hex anchors>
[SUBJECT]    <one-line subject description>
[COMPOSITION] <foreground / midground / background, eye-line, focal point>
[LIGHTING]   <time of day, key/fill direction, mood>
[DENSITY]    <approx pixels-per-character, dithering policy>
[MOOD]       <2–4 adjectives>
[NEGATIVE]   <anti-patterns to forbid — see anti-patterns.md>
```

This block format is **deliberately model-agnostic** — Z-image,
SDXL, DALL-E, Imagen (Nano Banana), Midjourney, and OpenAI Image
all accept structured natural-language prompts. Per-model phrasing
nudges live in `references/model-routing.md`.

## Phase 3 — Generation routing (capability-gated)

Two paths. Do **not** silently fall through — name which path is
running.

### Density-target pre-check (run BEFORE routing)

Before checking which MCP is connected, ask: **what density anchor
did the user name (or imply via a reference image)?** Generators have
hard density ceilings that prompt phrasing cannot overcome — picking
the wrong generator for the density target is the #1 failure mode of
this skill (surfaced empirically in v3.10.0 smoke testing).

Match the brief's density anchor to a generator using
`references/model-routing.md` → "Picking by density target". Key
rule:

- **Modern indie-density and below** (Stardew / Celeste / Octopath
  lower-density / 16-bit / 8-bit) → Z-image is fine inline.
- **HD-pixel-game-density and above** (Octopath / Sea of Stars /
  Eastward / AI-pixel-art aesthetic — including Kiang's harbor +
  tavern reference screenshots) → **do not start with Z-image even
  if it is the only connected MCP.** Z-image caps at moderate
  density. Route to Path B with a Midjourney `--niji 6` or SDXL +
  pixel-art LoRA brief instead — that is the correct primary
  deliverable for this density target, not a degraded fallback.

### Path A — Inline generation (preferred when available, AND when density allows)

After the density pre-check passes for the available MCP, check what
is connected. If any of the following are connected and match the
density target, generate inline:

- **Z-image Turbo** (HuggingFace MCP, `gr1_z_image_turbo_generate`)
  — caps at modern-indie-density
- **Imagen / Nano Banana** (Google AI MCP, if present)
- **OpenAI Image** (if exposed via MCP)
- **Any other image-gen MCP** the user mentions

Pass the composed prompt (Phase 2) to the generator. Apply per-model
phrasing tweaks from `references/model-routing.md`. Save the output
to `docs/pixel-art/<slug>-<yyyy-mm-dd>.png` (create the directory if
absent) and link it to the user.

If you generated an image, also emit the **finalized prompt** as a
sibling `.md` file (`docs/pixel-art/<slug>-<yyyy-mm-dd>.md`) so the
user can regenerate, iterate, or hand it to a different model later.

### Path B — Prompt-brief fallback (first-class, not degraded)

If no image-gen MCP is connected (or the user explicitly wants a
copy-pasteable prompt), emit a **prompt brief** following
`templates/prompt-brief-fallback.md`. The brief includes:

1. The model-agnostic prompt (universal block format from Phase 2).
2. Per-model variants for the four most common generators:
   - **OpenAI Image / DALL-E 3** — phrasing tweaks
   - **Imagen / Nano Banana** — phrasing tweaks
   - **Midjourney** — `--style` and `--ar` parameters
   - **SDXL / SD3** — `pixel art` tag + recommended LoRA names
3. Negative prompt block (anti-patterns).
4. A note: *"This prompt is model-agnostic. The block structure
   works across generators; per-model variants above add the small
   phrasing nudges each model responds to."*

Do not call Path B "fallback" in user-facing output — call it
"prompt brief" or "copy-pasteable prompt." It is a first-class
deliverable.

### Title-card SVG path (additive)

If subject is `title-card`, **always** also emit a code-based SVG
from `templates/title-card.svg`. This SVG uses VT323 by default
(per Kiang) and accepts the font, palette, and title text as
template tokens. It is portable (renders in browsers, exports to
PNG), and gives the user a path that does not depend on any image
generator at all. Save to `docs/pixel-art/<slug>-title.svg`.

When both Path A and the SVG path run, surface both: *"Generated
image at `<png>`; portable SVG title card at `<svg>` — pick
whichever fits your use case."*

## IP guardrail (non-negotiable)

Mirror `algorithmic-art`'s standard:

- **Never** reference any specific named artist in any prompt —
  living or deceased (no "in the style of [artist]", no
  "[artist]-style"). Deceased artists' work is typically still under
  copyright; the guardrail applies regardless of life status.
  Rewrite the prompt to encode craft markers instead.
- **Never** copy a specific copyrighted work. If the user supplies
  a reference screenshot, treat it as stylistic intent only and
  produce an original composition.
- Pinned reference examples in `docs/pixel-art/` should be original
  generations, not derivatives of third-party reference imagery.

If a user prompt names any specific artist (living or deceased),
**rewrite it** before generating: replace the artist name with the
craft markers that artist's style would have evoked (high-density,
painterly mid-tones, warm palette, etc.). Note the rewrite in the
user-facing output.

## Verification — craft-marker checklist

Before declaring a generation done, run the checklist in
`references/anti-patterns.md`. Hi-fi mode requires at least **5 of 6**
craft markers present (marker 6 added in v3.10.1; this section is
the SKILL.md summary — `references/anti-patterns.md` is authoritative
on the full checklist and regenerate-recipes):

1. **Deliberate hue shifts** in shadow / light ramps (not pure
   lightness change).
2. **Cluster studies** — no orphan single pixels.
3. **Banding avoidance** — no long stripes of uniform color
   without breakup.
4. **Painterly mid-tones via ordered dithering** where appropriate.
5. **Clean edges** — silhouettes legible, no anti-aliasing fringe.
6. **Pixel scale matches the density anchor** — output's pixel scale
   lands in the band named in `[DENSITY]`. Markers 1–5 check *how*
   pixels behave; marker 6 checks *whether they are the right size*.

Lo-fi mode is more permissive — the scanlined warm-paper background
is the main anchor; the craft markers above are nice-to-have.

If the generation fails the checklist, surface the gap to the user
and offer to regenerate with adjusted prompt blocks (usually a
density bump or a different palette).

## File map

```
skills/pixel-art/
├── SKILL.md                 (this file)
├── README.md                (user-facing docs)
├── references/
│   ├── style-modes.md       (hi-fi vs lo-fi profiles)
│   ├── palette.md           (named palettes by mood)
│   ├── density.md           (pixel density + dithering rules)
│   ├── composition.md       (layout, eye-line, light source)
│   ├── lighting.md          (time-of-day, mood, color-temp)
│   ├── fonts.md             (VT323 default + 4 alternates)
│   ├── anti-patterns.md     (craft-marker checklist + forbid list)
│   └── model-routing.md     (per-model phrasing tweaks)
└── templates/
    ├── scene-prompt.md
    ├── character-prompt.md
    ├── building-prompt.md
    ├── nature-prompt.md
    ├── title-card-prompt.md
    ├── title-card.svg       (SVG template with VT323)
    └── prompt-brief-fallback.md
```

## Cross-skill integration

| Skill | Relationship |
|---|---|
| `brand-workshop` | Pure logo / identity packages route there instead. `pixel-art` can produce pixel-art **brand banners**, but a logo is a different deliverable. |
| Anthropic's `algorithmic-art` | Sibling: algorithmic art uses p5.js (procedural, seeded). `pixel-art` uses image-gen models + structured prompts. Different toolchain, complementary scope. |
| Anthropic's `canvas-design` | Sibling: canvas-design ships static raster / PDF via design-philosophy prose. `pixel-art` ships pixel-style raster via design-system tokens. |
| `team-composer` | If the brief is genuinely cross-disciplinary (e.g., "design a game splash screen and its marketing copy"), team-composer assembles roles and may hand `pixel-art` the visual deliverable. |
| Image-gen MCPs (Z-image, Imagen, OpenAI Image, etc.) | Capability-gated dependency. Skill works without any of them via Path B; works better with at least one connected. |

## When to use this skill

(Trigger phrases above. Repeated here for the cross-tool SKILL.md
standard — Codex and other parsers look for this header.)

- "create pixel art [of X]"
- "pixel-art [scene / character / building / nature / title card]"
- "hi-fi pixel art" / "lo-fi pixel art"
- "VT323 title card" / "pixel-font title"
- "make this a pixel-art version"
- "generate a pixel-art [subject]"
- "I want this style" + hi-density pixel-art reference

**Tags:** `pixel-art`, `image-generation`, `design-system`,
`hi-density`, `lo-fi`, `title-card`, `VT323`, `model-agnostic`,
`capability-gated`.

## License

MIT. See repo root `LICENSE`.
