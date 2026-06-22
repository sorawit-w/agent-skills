# Model routing — optional per-generator phrasing nudges

The composed prompt (from Phase 3 of SKILL.md) is **model-agnostic**
by design. This file lists small, **optional** phrasing nudges each
generator responds to. Apply them on top of the universal block format
*if* you happen to be on one of these generators — don't rewrite the
prompt structure, and don't treat this list as the set of "supported"
tools.

The skill is **capability-gated, not vendor-gated**, and it detects
capability by **attempting** generation, not by checking whether a
*named* server is connected (host-native generators aren't always
introspectable). If you can generate by any means, do; the generators
below are just where known phrasing nudges exist. When you genuinely
cannot generate at all, emit the prompt brief (Path B in SKILL.md
Phase 4).

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

**Density tendency (nudge, not a gospel ceiling):** Z-image's training
set biases its "pixel art" prior toward moderate-density indie-game
aesthetic (Stardew, Octopath at lower density). Prompt phrases like
*"ULTRA-FINE PIXEL DETAIL"* and resolution bumps don't move the prior
much; the output tends to stay at moderate density. If you need finer
grain than it gives, the quantize post-process (SKILL.md Phase 4)
normalizes the grid regardless, and if you have another generator
available you can try it — but don't route *off* Z-image as a hard
rule. (This is a tendency observed for one generator, not a portable
ceiling — newer generators outside this list behave differently.)

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

## A note on density and generators

Generators differ in how fine a pixel grain they reach from prompting
alone — but this is a **soft tendency per generator**, not a portable
ceiling, and it does **not** drive routing. Two reasons it's no longer a
route-off rule:

1. **The quantize post-process normalizes the grid.** Whatever grain the
   generator produces, `scripts/quantize.py` (SKILL.md Phase 4) downscales
   to the target grid and median-cut-quantizes the palette — so the final
   output is grid-aligned regardless of the source generator's prior.
2. **The vendor list isn't the world.** Hardcoding "generator X caps at
   density Y" breaks the moment a newer generator appears (host-native
   image models, etc.). Route by *"can I generate?"*, generate, then
   quantize. If an output misses the density anchor and you have another
   generator handy, try it — as advice, not a gate.

## Surfacing routing to the user

When you generate, say how. Example:

> Generated inline, then quantized to a 192px grid / 32-color palette.
> The prompt is model-agnostic — if you'd rather run it in a specific
> generator, here it is to paste.

If you genuinely cannot generate by any means, return Path B (the
prompt brief). Do **not** silently fail; emit the brief and explain.
