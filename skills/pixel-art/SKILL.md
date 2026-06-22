---
name: pixel-art
description: >
  Generate single-subject pixel art (scenes, characters, buildings, title cards)
  from a short brief, with a built-in style system (palette, density, lighting,
  fonts). Modes `hi-fi` (painterly high-density, default) and `lo-fi` (scanlined
  banner). Generative: produces a raster, runs a deterministic
  median-cut quantize to true grid-aligned pixel art, and can serialize one sprite
  to SVG. Repo-agnostic — returns artifacts, writes nothing; with no generator
  reachable it returns a model-agnostic prompt brief. Triggers on
  "pixel art", "hi-fi/lo-fi pixel", "VT323 title card", "generated pixel art as
  SVG" (single sprite), or a hi-density reference plus "this style". Does NOT
  trigger on — and declines — composed/branded SVG-asset jobs (banner, icon set,
  multi-asset set, needing exact text, a fixed viewBox, brand tokens, or
  an editable vector source it doesn't author). Not for vector illustration, logos
  (`brand-workshop`), photo-real, p5.js (`algorithmic-art`), or charts. Never names
  living artists.
metadata:
  tier: draft
---

# pixel-art

A pocket-sized pixel-art studio. You hand it a short brief — *"medieval
harbor at dusk"*, *"tavern interior with fireplace"*, *"Whispers of the
Flame title card in VT323"* — and it returns a finished image (whenever
any image generator is reachable) or a model-agnostic prompt brief you
can paste into the generator of your choice. The style is locked in
`references/` so you do not have to re-describe palette, density,
composition, lighting, or typography every time.

**Repo-agnostic.** This skill assumes no repository and writes nothing
to disk. Every artifact — the generated image, the quantized PNG/SVG,
the prompt brief, the title-card SVG — is **returned to the caller**,
who decides what to do with it. (Ephemeral temp files used purely to
hand a raster to the quantize script are fine; persisting to a repo path
is not.)

## When to use this skill

- *"Create a pixel-art [scene / character / building / forest / title card] of …"*
- *"Make a hi-fi pixel-art harbor at dusk."*
- *"Generate a lo-fi pixel banner like the agent-skills banners."*
- *"Title card for 'Whispers of the Flame' in VT323."*
- *"I want this image in the same hi-density pixel style as before."*
- *"Make this image a pixel-art version of itself."*
- *"Give me that sprite as SVG."* (single generated sprite → WS4 serialize)

If the user provides a reference screenshot and says *"this style"*,
treat it as stylistic intent (palette / density / mood). Do **not**
copy the reference image; produce an original composition that hits
the same craft markers (see `references/anti-patterns.md`).

## When NOT to use this skill

- **Composed / branded SVG-asset jobs** — banners, icon sets, branded
  SVGs, multi-asset sets, anything needing exact rendered text, an exact
  layout/viewBox, brand tokens, or an editable vector source. This skill
  generates a single raster; it does **not** author composition. See the
  Phase 0 gate — it **declines** these honestly rather than substituting
  a raster.
- **Vector illustration / icon design** — use `canvas-design` or
  hand-author SVG. Pixel art is raster-first; vectors are a different craft.
- **Logo or brand identity package** — route to `brand-workshop`.
- **Photo-realistic generation** — wrong style; use a general image-gen
  model directly with a non-pixel-art prompt.
- **Algorithmic / generative art with p5.js, particle systems, flow fields**
  — use Anthropic's `algorithmic-art` skill.
- **Charts, dashboards, data visualization** — use the data viz skills.
- **Rasterizing an existing photograph as pixel art** — out of scope;
  consider an external "pixelate" filter instead.

## Phase 0 — Deliverable-type gate (run FIRST)

**Before anything else, decide whether this is a job the skill does.**
`pixel-art` is a single-subject *generative* skill: it produces a
**raster** and may **serialize one sprite as SVG**. It does **not**
author composed deliverables.

If the brief needs **any** of the following, it is a
**composition/authoring job** and you must **decline**:

- exact rendered text (a banner/title with specific words laid out),
- an exact layout or `viewBox`,
- exact brand tokens / a brand spec,
- an editable / vector source as the deliverable,
- a **multi-asset set** (icon set, banner family, sprite sheet).

**How to decline:** state the mismatch plainly — *"You asked for
`<deliverable>`, which needs `<exact text / layout / vector source / a
set>`. `pixel-art` generates a single raster (optionally one sprite as
SVG); it does not author composed SVG assets, so I can't produce this
honestly."* Then **stop**. Do **not** down-convert the request to a
raster, and do **not** name a substitute tool — routing is the caller's
call.

**Carve-outs (NOT a decline):**

- **Title card** — the `title-card.svg` template is the one
  grandfathered authored-SVG path. A title-card request (even with exact
  title text) proceeds to the title-card SVG path in Phase 4. This is the
  single exception to "no exact rendered text."
- **Single-sprite SVG** — *"give me that generated sprite as SVG"* is a
  **serialize** of one generated raster (Phase 4 / WS4 quantize), not a
  composed asset. Proceed.

If the request passes the gate (a single scene / character / building /
nature / title-card / sprite), continue.

## Phase 1 — Style mode

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

## Phase 2 — Subject detection

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

## Phase 3 — Compose the prompt

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
[DENSITY]    <density anchor name, dithering policy>
[MOOD]       <2–4 adjectives>
[NEGATIVE]   <anti-patterns to forbid — see anti-patterns.md>
```

This block format is **deliberately model-agnostic** — it accepts
structured natural-language prompts across any image generator.
Optional per-model phrasing nudges live in `references/model-routing.md`.

## Phase 4 — Generation routing (attempt-then-fallback)

Two paths. Do **not** silently fall through — name which path is
running.

**The routing question is "can I generate at all?", not "is a specific
named MCP connected?"** Host-native image generation often isn't
introspectable from inside a skill, so detect by **attempting**, not by
checking a vendor list.

### Path A — Inline generation (preferred whenever reachable)

**Attempt inline generation using any available image-generation
capability — host-native OR an MCP tool.** If you can produce an image
in this runtime, do it. Pass the composed prompt (Phase 3) to the
generator; apply optional per-model phrasing tweaks from
`references/model-routing.md` *if* you happen to be on a generator listed
there (the list is nudges, not a gate).

After generation, run the **deterministic quantize pass** (next section),
then **return** the quantized artifact + the finalized prompt to the
caller. Do **not** write either to a repo path — return them as values
(image bytes/handle + the prompt text). The caller decides where they go.

> **Density note (advisory, not a gate):** generators differ in how fine
> a pixel grain they reach from prompting alone. If an output misses the
> density anchor you named, regenerate with adjusted blocks, or — if you
> have another generator available — try it. This is advice, not a
> hard route-off rule; the quantize pass below also normalizes grain.

### Quantize post-process (deterministic)

Raw diffusion output is *pseudo* pixel art — tens of thousands of unique
colors, no true grid. Run `scripts/quantize.py` (in this skill's
directory; needs Pillow — `pip install -r scripts/requirements.txt`) to
make it real grid-aligned pixel art:

```
python3 scripts/quantize.py <in.png> --format <png|svg> [--grid N] [--palette N] [--ramp <hexlist>] [--scale N]
```

Pipeline: nearest-neighbor downscale to the target grid → **median-cut**
palette quantize (deterministic; honors a supplied fixed ramp) →
optional ordered dither + orphan-pixel cleanup → nearest-neighbor upscale
×N for display. Defaults: grid 128–256px, palette 24–48 colors, dither
off, median-cut palette. Output switch emits **PNG or SVG** (SVG = one
`<rect>` per run-length-merged cell — **single sprite only**, not a
banner/composition path). Return the requested format to the caller.

If Pillow is unavailable and can't be installed, say so and return the
un-quantized raster with a noted caveat — don't silently skip the step.

### Path B — Prompt-brief (only when generation is genuinely impossible)

If you **cannot** generate an image by any means in this runtime (no
host-native capability and no image-gen MCP), OR the user explicitly
asks for a copy-pasteable prompt, emit a **prompt brief** following
`templates/prompt-brief-fallback.md`. **Return** the brief to the caller
(do not write it to disk). The brief includes:

1. The model-agnostic prompt (universal block format from Phase 3).
2. Optional per-model variants for common generators (nudges only).
3. Negative prompt block (anti-patterns).
4. A note that the prompt is model-agnostic.

Do not call Path B "fallback" in user-facing output — call it
"prompt brief" or "copy-pasteable prompt." It is a first-class
deliverable.

### Title-card SVG path (additive)

If subject is `title-card`, **always** also produce a code-based SVG
from `templates/title-card.svg`. This SVG uses VT323 by default
(per Kiang) and accepts the font, palette, and title text as
template tokens. It is portable (renders in browsers, exports to
PNG), and gives the user a path that does not depend on any image
generator at all. **Return** the filled SVG to the caller (do not write
it to disk). This is the one authored-SVG path the skill retains (see
the Phase 0 carve-out).

When both Path A and the SVG path run, surface both: *"Here's the
generated + quantized image, and a portable SVG title card — pick
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
- Any reference examples you return should be original generations, not
  derivatives of third-party reference imagery.

If a user prompt names any specific artist (living or deceased),
**rewrite it** before generating: replace the artist name with the
craft markers that artist's style would have evoked (high-density,
painterly mid-tones, warm palette, etc.). Note the rewrite in the
user-facing output.

## Verification

### Deliverable-type check (run FIRST)

Before the craft check, confirm the output's **kind** matches the
request: a single raster (or one-sprite SVG / title-card SVG) for a
generative brief; an honest **decline** for a composition/authoring
brief (Phase 0). If you generated a raster for something that should
have been declined, that is the failure this skill exists to prevent —
stop and decline instead.

### Craft-marker checklist

Then run the checklist in `references/anti-patterns.md`. Hi-fi mode
requires at least **5 of 6** craft markers present (marker 6 added in
v3.10.1; this section is the SKILL.md summary —
`references/anti-patterns.md` is authoritative on the full checklist and
regenerate-recipes):

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
│   └── model-routing.md     (optional per-model phrasing nudges)
├── scripts/
│   ├── quantize.py          (deterministic median-cut quantize → PNG/SVG)
│   ├── test_quantize.py     (stdlib assert-based invariants)
│   └── requirements.txt     (Pillow)
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
| `brand-workshop` | Logo / identity packages route there. A composed/branded asset set is a decline here (Phase 0), not a `pixel-art` job — but the caller routes; this skill does not name where. |
| Anthropic's `algorithmic-art` | Sibling: algorithmic art uses p5.js (procedural, seeded). `pixel-art` uses image-gen models + structured prompts. Different toolchain, complementary scope. |
| Anthropic's `canvas-design` | Sibling: canvas-design ships static raster / PDF via design-philosophy prose. `pixel-art` ships pixel-style raster via design-system tokens. |
| `team-composer` | If the brief is genuinely cross-disciplinary (e.g., "design a game splash screen and its marketing copy"), team-composer assembles roles and may hand `pixel-art` the single-image deliverable. |
| Image-gen capability (host-native or MCP) | Attempt-then-fallback dependency. Skill works with no generator at all via Path B (the prompt brief); works better when generation is reachable. |

## When to use this skill

(Trigger phrases above. Repeated here for the cross-tool SKILL.md
standard — Codex and other parsers look for this header.)

- "create pixel art [of X]"
- "pixel-art [scene / character / building / nature / title card]"
- "hi-fi pixel art" / "lo-fi pixel art"
- "VT323 title card" / "pixel-font title"
- "make this a pixel-art version"
- "generate a pixel-art [subject]"
- "give me that sprite as SVG" (single generated sprite)
- "I want this style" + hi-density pixel-art reference

**Tags:** `pixel-art`, `image-generation`, `design-system`,
`hi-density`, `lo-fi`, `title-card`, `VT323`, `model-agnostic`,
`quantize`, `repo-agnostic`.

## License

MIT. See repo root `LICENSE`.
