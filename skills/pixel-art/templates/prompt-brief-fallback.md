# Prompt-brief fallback — copy-pasteable, model-agnostic

When no image-gen MCP is connected (or the user wants a portable
prompt to run elsewhere), emit a brief in this shape. **This is a
first-class deliverable**, not a degraded fallback — most users will
want this format anyway, because they have a preferred generator
they want to run it in.

## Brief structure

```markdown
# Pixel-art prompt brief — <subject in 4–6 words>

**Style mode:** <hi-fi | lo-fi>
**Subject:** <scene | character | building | nature | title-card>
**Palette:** <named palette from references/palette.md>

## Model-agnostic prompt (works in any generator)

[STYLE] ...
[PALETTE] ...
[SUBJECT] ...
[COMPOSITION] ...
[LIGHTING] ...
[DENSITY] ...
[MOOD] ...
[NEGATIVE] ...

## Per-model variants

### Z-image Turbo (HuggingFace)
<prompt with Z-image-specific phrasing tweaks from references/model-routing.md>

### OpenAI Image / DALL-E 3
<prompt with DALL-E-specific tweaks — explicit "hard pixel edges, no smoothing" reinforcement>

### Imagen / Nano Banana (Google)
<prompt with Imagen-specific tweaks — palette in plain language>

### Midjourney
<prompt with --ar / --style raw / --no flags>

### SDXL / Stable Diffusion
<prompt with pixel-art LoRA trigger + CFG suggestion>

## Notes

- This prompt is model-agnostic. The block structure works across
  generators; per-model variants above add the small phrasing nudges
  each model responds to.
- For the negative prompt, paste the [NEGATIVE] block verbatim into
  your generator's negative-prompt field (where supported).
- Verify the output against the craft-marker checklist in
  references/anti-patterns.md — hi-fi requires at least 4 of 5
  markers.
```

## What to include / what to skip

- **Always include** the universal prompt and at least 3 per-model
  variants.
- **Always include** the negative block.
- **Always include** a one-line note pointing at the craft-marker
  checklist.
- **Skip** the per-model variant for any generator the user has
  explicitly named — give them the prompt for *their* generator
  expanded, plus 1–2 alternatives for portability.

## Surfacing the brief to the user

When emitting the brief, save it to `docs/pixel-art/<slug>-<date>.md`
and link it. Example user-facing line:

> No image-gen MCP is connected, so I've drafted a portable prompt
> brief: `docs/pixel-art/harbor-dusk-2026-05-11.md`. It works in
> any generator (Midjourney, DALL-E, Imagen, SDXL, Z-image) — paste
> the universal block, or use one of the per-model variants for a
> tighter fit. Connect any image-gen MCP and I'll generate inline
> next time.
