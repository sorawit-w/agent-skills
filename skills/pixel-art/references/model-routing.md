# Model routing — per-generator phrasing tweaks

The composed prompt (from Phase 2 of SKILL.md) is **model-agnostic**
by design. This file lists the small phrasing nudges each generator
responds to. Apply them on top of the universal block format —
don't rewrite the prompt structure.

The skill is **capability-gated, not vendor-gated** — when any of
these MCPs is connected, route to it. When none are, emit the
prompt brief and the user picks (this is Path B in SKILL.md
Phase 3).

## Z-image Turbo (HuggingFace MCP)

**MCP tool:** `gr1_z_image_turbo_generate` (under the HuggingFace MCP)

**Strengths:** fast, free via HF, decent at moderate-density pixel-art
style cues, good for rapid exploration and prompt iteration.

**Phrasing tweaks:**
- Lead with **"high-density pixel art"** in the `[STYLE]` block —
  Z-image responds strongly to the leading phrase.
- Name a **density anchor** in `[DENSITY]` (see `density.md` anchor
  table). Modern-indie-density (Stardew / Celeste) is Z-image's
  natural sweet spot.
- Negative prompt is well-supported; pass the full `[NEGATIVE]`
  block.

**Known weak spots — density ceiling:** Z-image's training set biases
its "pixel art" prior toward moderate-density indie-game aesthetic
(Stardew, Octopath at lower density). **It cannot reach hi-density
AI-pixel-art aesthetic via prompting alone** — verified empirically.
Prompt phrases like *"ULTRA-FINE PIXEL DETAIL"* and resolution bumps
do not override the model's prior; the output stays at moderate
density with chunkier-than-target tiles.

**When to escalate off Z-image:** if the user's reference is
HD-pixel-game-density (Octopath / Sea of Stars / Eastward) or
AI-pixel-art-density (the harbor / tavern reference screenshots),
escalate to **Midjourney `--niji 6`** or **SDXL + pixel-art LoRA**.
See "Picking by density target" below.

**Other Z-image weak spots:** sub-pixel facial detail is inconsistent
(avoid tight character close-ups); dithering discipline is hit-or-miss
even with explicit emphasis.

## OpenAI Image / DALL-E 3 (via OpenAI MCP, if installed)

**Strengths:** strong on composition, narrative coherence.

**Phrasing tweaks:**
- DALL-E 3 tends to **soften** pixel art. Be very explicit:
  *"pixel art with hard pixel edges, no anti-aliasing, no blur,
  nearest-neighbor upscale aesthetic, every pixel clearly visible."*
- Avoid the word "illustration" — DALL-E reads it as smoothed digital
  art.
- Negative prompts are limited; use positive phrasing instead
  (*"crisp pixel edges, no smoothing"* rather than `[NEGATIVE]`).

**Known weak spots:** consistent dithering. Output is more "vibey
pixel art" than crafted pixel art. Best for atmospheric scenes
where craft markers are less rigid.

## Imagen / Nano Banana (Google)

**Strengths:** good at painterly scenes, atmospheric lighting.

**Phrasing tweaks:**
- Imagen responds well to **palette named in plain language** —
  "warm coastal palette of sandstone, sea-blue, sky-cream."
- Add **"chunky pixel rendering"** to reinforce density.
- Lighting profiles (Phase 5) translate cleanly — Imagen is good at
  "golden hour with long shadows."

**Known weak spots:** strong tendency to anti-alias edges.
Compensate with `"hard pixel edges, no AA, no smoothing"` repeated
in both the `[STYLE]` and `[NEGATIVE]` blocks.

## Midjourney

**Strengths:** atmospheric mood, strong composition.

**Phrasing tweaks:**
- Append `--ar 16:9` or `--ar 1:1` for scene aspect.
- Try `--style raw` to bypass Midjourney's aesthetic smoothing.
- Add `--niji 6` for JRPG-flavored pixel scenes (good with
  candlelit / twilight palettes).
- Midjourney's negative is `--no anti-aliasing, smoothing, blur,
  photo-real`.

**Known weak spots:** signature Midjourney smoothness. Counter
with strong `--no` flags and explicit "pixel art, blocky,
nearest-neighbor" in the prompt.

## SDXL / SD3 (or local Stable Diffusion via ComfyUI / A1111)

**Strengths:** highly steerable via LoRAs; pinned outputs are
reproducible across runs.

**Phrasing tweaks:**
- Pixel-art LoRAs are widely available — search Civitai for
  "pixel art" / "hi-res pixel" LoRAs. Common ones: `pixel_art_xl`,
  `pixelart-sdxl`.
- Trigger phrase: `"pixel art, pixel style, pixel-perfect"` plus the
  LoRA trigger token.
- Negative prompt is well-supported; pass the full `[NEGATIVE]`
  block plus `"blurry, low quality, jpeg artifacts, smooth, painted"`.
- Use **CFG 7–9** for steerability; lower for more model freedom.

**Known weak spots:** depends on the LoRA. Without a pixel-art LoRA,
SDXL produces "stylized digital art" rather than true pixel art.

## How to pick which generator (if multiple are available)

| Subject | Best generator (prefer) |
|---|---|
| Atmospheric scene with strong lighting | Imagen / Midjourney |
| Character art with composition coherence | DALL-E 3 |
| Reproducible / pinned style | SDXL with pixel-art LoRA |
| Fast iteration / cheap exploration | Z-image Turbo |
| JRPG / fantasy scenes | Midjourney with `--niji 6` |
| Title cards (background imagery only — text is SVG) | Any of the above |

## Picking by density target (added v3.10.1)

The **single most important routing question** is: does the user want
moderate-density pixel art (Stardew / Octopath) or hi-density
(HD-pixel-game / AI-pixel-art aesthetic)? Generators have hard
ceilings here that prompt phrasing cannot overcome.

| Density target | Reach-for generator | Why |
|---|---|---|
| 8-bit / NES-density | SDXL + retro pixel-art LoRA, or Z-image with chunky `[STYLE]` emphasis | Either reaches it cleanly |
| 16-bit / SNES-density | Midjourney standard, SDXL, Z-image | Multiple generators handle this band |
| Modern indie-density (Stardew / Celeste) | **Z-image Turbo** (sweet spot) | Z-image's training-data center of mass |
| **HD-pixel-game-density (Octopath / Sea of Stars)** | **Midjourney `--niji 6`** | Niji is trained heavier on JRPG / hi-density anime-pixel content |
| **AI-pixel-art-density (HD-rendered pixel scenes)** | **SDXL + pixel-art LoRA**, or Midjourney `--niji 6 --style raw --stylize 50` | LoRA-driven runs reach the highest density; Z-image hard-caps below this band |

**Routing rule:** if the user supplies a hi-density reference image
(or names HD-pixel-game / AI-pixel-art density in their brief), **do
not start with Z-image** even if it is the only connected MCP.
Generate a Midjourney or SDXL prompt brief via Path B in `SKILL.md`
Phase 3 — that is a real, useful output, not a degraded fallback.

When in doubt about density, **try Z-image first** for fast iteration
on composition / palette / lighting, then escalate to Midjourney or
SDXL once those decisions are locked. Composition decisions transfer
across generators; pixel density does not.

## Surfacing routing to the user

When the skill picks a generator, name it. Example user-facing
output:

> Routing this to **Z-image Turbo** (connected, fastest). If you
> want a different generator, name it and I'll switch — the prompt
> is model-agnostic so no rework needed.

If none of these MCPs is connected, the skill defaults to Path B
(the prompt brief). Do **not** silently fail; emit the brief and
explain.
