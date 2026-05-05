# Hero banner — production brief (v0.1)

**Job.** Replace `assets/hero.svg` (lo-fi pixel art, SVG-of-rects) with a hi-fi PNG hero in modern pixel-art style. Keep the warm paper/wood brand language; technique upgrade only, not a brand pivot.

**Style.** Mixed fidelity, à la HD-2D principle:
- **Tinkerer-agent mascot:** hi-bit pixel art — strong silhouette, ~3 shades per surface, deliberate pixel placement, minimal sub-pixel anti-aliasing. Stays iconic and reusable across 12 skill icons.
- **Backdrop (shelf, tiles, atmosphere):** hi-fi pixel art — 5–7 shades per surface, dithered gradients, soft selout outlines, atmospheric warm light from above.

---

## Canvas math

| Field | Value |
|---|---|
| Native resolution | **480 × 140 px** |
| Display resolution | 960 × 280 px (2x via `image-rendering: pixelated`) |
| Format | **PNG-8 with alpha**, optimized via `oxipng` |
| File size target | < 200 KB |
| Color depth | 32-color indexed palette (locked, see below) |
| Source file kept in repo | Yes — keep alongside PNG for re-edit |

---

## Locked palette (32 colors)

Drawn from existing brand surfaces (current `hero.svg`, README badge colors). Grouped by family with named roles:

```
WOOD (shelf + tile frames) — 6
  #3a1f0f  wood-darkest   (selout, deep shadow)
  #5e3618  wood-dark      (bracket, plank shadow)
  #7c4b2a  wood-mid       (plank base)
  #8a5a34  wood-light     (plank top)
  #a2703f  wood-grain     (highlight stripe)
  #c9b58a  wood-tile-edge (tile bevel)

PAPER / TILE FACE — 4
  #fdf7ea  paper-light    (tile inner)
  #f5efe6  paper          (background base)
  #eadfcf  paper-shadow   (subtle scan/grain)
  #f3e7c9  paper-warm     (tile, clipboard)

WARM ACCENT (rust / brand orange) — 4
  #7c2d12  rust-dark      (mascot apron shadow)
  #c2410c  rust           (brand primary, antenna)
  #ea580c  rust-light     (highlight)
  #fdba74  rust-pale      (rim glow)

SKIN / FACE (mascot) — 3
  #b08754  skin-shadow
  #fde68a  skin           (warm cream)
  #fef3c7  skin-light     (highlight)

GOLD / WARM GLOW — 3
  #b45309  gold-dark
  #fcd34d  gold           (atmospheric light, prop highlights)
  #fef9c3  gold-pale      (dust motes, rim light)

NEUTRAL (text + character body) — 5
  #111827  ink            (mascot body, hard outlines)
  #1f2937  charcoal       (text)
  #374151  gray-dark      (clothing folds)
  #6b7280  gray           (metadata text, clip metal)
  #9ca3af  gray-light     (subtle lines)

SUPPORT — 3
  #15803d  green          (skill-evaluator check, accent only)
  #bae6fd  sky            (magnifier glass; sparingly)
  #ffffff  white           (rare highlight only — use gold-pale instead by default)
```

**Discipline rules:** every shaded surface uses 3 colors from one family (shadow / base / highlight). Cross-family color borrowing is forbidden except for `gold` as universal rim light.

---

## Tinkerer-agent character sheet

**Name (proposed):** **Pip** — single syllable, evokes "pixel," friendly without being twee. Alternates if you reject: *Cobb* (cobbler/craftsman), *Tilly* (warmer), *Nib* (smaller, tool-coded).

**Form factor.** Small humanoid agent, ~64 px tall (about 45% of banner height). Extends the proto-character at lines 170–189 of current `hero.svg` — same family.

**Anatomy (top-down):**
- **Antenna:** single short rust-colored stalk with a pale gold tip (atmospheric glow point). 4 px.
- **Head:** ~16 px square, warm cream skin, two small dark eyes, hint of mouth (1–2 px line). Expression range across icon set: focused / curious / pleased / squinting.
- **Apron / body:** charcoal base with rust-dark trim, suggesting a leather workshop apron over a darker shirt. Two pixel-pocket details at hip.
- **Arms:** charcoal, posable. Default pose: one arm reaching to place a tile, the other holding the recurring prop.
- **Legs:** stubby, charcoal, two small skin-colored "boot tips."

**Recurring prop (icon-system anchor):** **a small wooden mallet** — `wood-mid` head with `wood-dark` band, `wood-light` handle. Sized so silhouette stays readable at 32 px (icon scale). Pip carries the mallet in every appearance — banner, skill icons, social variants. The mallet is the brand-anchor visual.

**Why a mallet, not a chisel/wand/glow-tile:** mallet has the strongest silhouette at small sizes, doesn't lock to a tech metaphor, is universally craft-coded, and has obvious narrative range (raised, resting, mid-tap, slung over shoulder).

---

## Composition map (480 × 140 native)

```
┌──────────────────────────────────────────────────────────────────────────┐
│  [text-area: 0–220 px wide]              [scene-area: 220–480 px wide]   │
│                                                                          │
│  agent-skills                                       ☼ (warm light)       │
│  a personal shelf of                                                     │
│   Claude Code plugins                                                    │
│  PIXELS · CRAFT · ONE                          [tile][tile][tile]        │
│   SKILL AT A TIME                              ════════════════          │ ← shelf
│                                                  Pip ↗ placing 4th       │
│                                                  ▟ (mallet at hip)       │
│                                                                          │
└──────────────────────────────────────────────────────────────────────────┘
```

**Rules:**
- Text remains as is in `hero.svg` lines 14–19 — render it as **separate SVG/HTML overlay**, not baked into the PNG. PNG carries scene only. (Cleaner i18n, no text re-renders, smaller file.)
- Scene-area carries: **shelf with 3 fully-rendered skill tiles + Pip mid-action placing a 4th**. No empty slots, no dashed-border affordances.
- Tile contents on the visible 3: pick the most recognizable — team-composer, brand-workshop, pitch-deck. (User decision-point: confirm the three.)
- Atmospheric: a soft warm light source upper-right casting subtle gradient across the shelf; a few gold-pale dust motes catching the light. Hi-fi treatment for the wood and atmosphere; hi-bit treatment for Pip and the tile silhouettes.
- Ground line: subtle paper-shadow stripe under the shelf brackets, no hard horizon.

---

## Mood references

- **Octopath Traveler / Triangle Strategy** — character-on-environment fidelity contrast (HD-2D). The exact technique we're applying.
- **Eastward** (Pixpil) — warm tone, atmospheric light, character-led composition.
- **Owlboy** (D-Pad Studio) — character-as-emotional-anchor with detailed environment behind.
- **The Last Night** (Odd Tales) — atmospheric pixel art with cinematic lighting, even though the palette is darker than ours.
- **NOT references:** Stardew Valley (too low-fi), Celeste (palette too cool), retro 8-bit constraints (we want hi-bit, not retro-bit).

---

## Prompt template (tuned for `evalstate/flux1_schnell` via HF MCP)

> **Tool note.** Pivoted from `FLUX.1-Krea-dev` after parameter inspection — Krea is tuned for photorealism ("eliminating typical AI image artifacts," camera/lens prompts), the opposite of what we want. `flux1_schnell` is vanilla FLUX, flexible across styles, and supports free width/height (we need 24:7 banner ratio, not aspect-locked). Qwen-Image considered and rejected — its enum locks aspect ratio to 16:9 max, would force heavy cropping.

```
detailed pixel art illustration of a tiny humanoid craftsman robot named Pip
with a single rust-orange antenna, warm cream face, charcoal leather workshop
apron, holding a small wooden mallet, placing a small wooden skill-tile onto
a wooden workshop shelf, three other carved wooden tiles already on the shelf,
soft warm overhead light catching dust motes, atmospheric warm paper-and-wood
color palette, rust orange and warm browns and cream tones, hi-fi modern pixel
art with rich dithered shading on the wood and background, hi-bit pixel art
style on the character with strong silhouette and three shades of shading,
wide horizontal banner composition, scene set on the right two-thirds of the
canvas, soft warm rim light, no text, no logos, no signature

negative: 3D render, vector illustration, flat design, minimalist, realistic
photography, anime, manga, cyberpunk, neon, dark fantasy, low-resolution
blurry, jpeg artifacts, watermark
```

**Generation params (proposed):**
- Aspect ratio: 24:7 (closest available; may need to crop)
- Steps: model default (FLUX-Krea is fast)
- Seed: vary per candidate
- Candidates per round: 4

---

## Prompt variants for external tools

> **Why three.** Different tools want different prompt shapes. LoRA-based tools (FLUX-LoRA-DLC, Retro Diffusion, SD+PixelArtXL) handle style via the LoRA — strip the "pixel art" descriptors. Natural-language tools (ChatGPT, Midjourney) want full sentences and prefer style-as-context over keyword soup.

### Variant A — for pixel-art-LoRA tools (best fit)
```
small humanoid craftsman robot named Pip, single rust-orange antenna with red tip,
warm cream face, two small dark eyes, charcoal leather workshop apron with rust trim,
holding a tiny wooden mallet at hip, mid-action placing a carved wooden skill-tile
onto a wooden workshop shelf already holding three other tiles, warm overhead light,
dust motes catching the light, warm rust-orange and brown and cream color palette,
wide horizontal banner composition, character positioned on the right two-thirds,
atmospheric warm rim light from upper right
```
**Negative:** `text, watermark, logo, signature, anime, manga, 3D render, photorealistic, blurry, low quality, extra limbs, multiple antennae, two heads`
**LoRA:** `nerijs/pixel-art-xl` or any PixelArtXL on FLUX-LoRA-DLC. Trigger: `pixel art`.
**Aspect ratio:** 24:7 if supported; else 21:9 and crop.

### Variant B-refined — for ChatGPT (GPT-Image-1) — second pass with brief-fixes
> **What changed:** explicit "dark charcoal not olive" apron, quieter left third for text overlay, AAA pixel-art-styled framing referencing Octopath Traveler / Eastward. Use this for the second ChatGPT attempt; variant B below is preserved for reference only.
```
Create a wide horizontal banner illustration in the AAA pixel-art-styled aesthetic
of HD-2D indie games like Octopath Traveler and Eastward — chunky visible pixels
on the character, cinematic warm lighting on a softly detailed environment.

Aspect ratio: very wide, roughly 21:9 (movie banner proportions).

Subject: a small humanoid craftsman robot named Pip — round-square head, single
slim rust-orange antenna with a tiny red ball at the tip, warm cream face with
two small dark expressive eyes and a hint of a smile. He wears a DARK CHARCOAL
(almost-black) leather workshop apron with rust-orange trim, piping, and small
brass buttons. NOT olive green, NOT brown — charcoal-leather. A tiny wooden
mallet is tucked at his hip. He is mid-action: arm extended forward, reaching
toward a wooden workshop shelf to place a small carved wooden skill-tile. Three
other carved wooden tiles are already on the shelf.

Lighting and atmosphere: warm window light streaming from above-left catching
dust motes in the air; atmospheric warm rim light on Pip's silhouette; cozy
workshop mood.

Color palette: warm rust-orange, warm browns, cream, charcoal. No blues, no
greens, no cool tones.

Composition: the LEFT THIRD of the canvas must be visually quiet — soft warm
wall or window pane, no tools or props — because text will be overlaid there.
The shelf and Pip occupy the center and right two-thirds.

No text, no logos, no signature, no watermark.
```
**Iteration follow-ups (paste as next message in same ChatGPT thread if first gen drifts):**
- Apron drifts olive/green → "Keep everything exactly the same but make the apron pure dark charcoal — almost black — with the rust-orange trim staying intact."
- Left side too busy → "Same scene but make the left third of the image quieter — just warm wall and soft window light, remove the props on the left."
- Aspect ratio comes back square → "Render this at 1792×1024 (widescreen)."

### Variant B — for ChatGPT (GPT-Image-1) / Midjourney (original — kept for reference)
```
Create a hi-fi pixel art banner illustration in the style of HD-2D / modern indie
games like Octopath Traveler. Wide horizontal composition (24:7 ratio). The scene:
a small humanoid craftsman robot named Pip — single rust-orange antenna with a red
tip, warm cream face with two small dark eyes, charcoal leather workshop apron with
rust-orange trim — holding a tiny wooden mallet, mid-action placing a carved
wooden skill-tile onto a wooden workshop shelf that already holds three other
tiles. Warm paper-and-wood color palette: rust orange, warm browns, cream, no cool
tones. Soft warm overhead light catching dust motes. Pip is on the right two-thirds
of the canvas. Atmospheric warm rim light. Pixel grid should be visible — true
pixel art with discrete chunky pixels and dithered shading, NOT smooth illustration.
No text, no logos, no signature.
```
**Midjourney suffix:** `--ar 24:7 --style raw --no text, logo, watermark, anime, 3D, photorealistic, multiple antennae`

### Variant C — verbatim prompt sent to FLUX schnell (for reference only)
This is what produced the two failed-to-be-pixel-art drafts. Kept for reproducibility.
```
detailed hi-fi pixel art illustration, small humanoid craftsman robot named Pip
with a single rust-orange antenna, warm cream face with two small dark eyes,
wearing a charcoal leather workshop apron, holding a tiny wooden mallet, placing
a small wooden skill-tile onto a wooden workshop shelf with three other carved
wooden skill-tiles, soft warm overhead light catching dust motes, warm
paper-and-wood color palette of rust orange and warm browns and cream, wide
horizontal banner composition, character on the right two-thirds of the canvas,
atmospheric warm rim light, no text, no logos
```

### Tool ranking for this job
1. **Retro Diffusion** (retrodiffusion.ai) — purpose-built, native pixel grid, controllable palette. Best fit.
2. **FLUX-LoRA-DLC + PixelArtXL** on HF — free, very good, browser-only.
3. **Recraft** (recraft.ai) — explicit "pixel art" style, free tier.
4. **ChatGPT GPT-Image-1** — quickest if you have Plus; expect "pixel-style illustration" rather than true pixel art.

---

## Acceptance criteria

A candidate is shippable when:
1. Pip's silhouette is readable at 32 px (test by downscaling).
2. Mallet is visible and recognizable.
3. Wood/shelf shows real shading (≥3 visible browns), not flat fill.
4. Palette feels warm — no cool-tone leakage (no blues outside `sky`, no purples).
5. No text, no extra characters, no fantasy elements.
6. Composition leaves the left third visually quiet (text overlays there).
7. PNG-8 export under 200 KB after `oxipng -o 4`.

---

## Open questions for Kiang

1. Mascot name — keep **Pip**, or pick from the alternates (Cobb / Tilly / Nib)?
2. Three visible tile contents — confirm **team-composer / brand-workshop / pitch-deck**, or pick three others?
3. Text overlay — keep current `hero.svg` text at the same size, or do you want a redesign of the type while we're in here?

Defaults if you don't override: Pip / those three tiles / keep current text exactly.
