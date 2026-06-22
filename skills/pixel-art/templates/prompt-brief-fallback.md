# Prompt-brief fallback — copy-pasteable, model-agnostic

When you genuinely cannot generate an image by any means in this
runtime (no host-native capability and no image-gen MCP), or the user
wants a portable prompt to run elsewhere, emit a brief in this shape.
**This is a first-class deliverable**, not a degraded fallback — most
users will want this format anyway, because they have a preferred
generator they want to run it in. **Return** the brief to the caller;
do not write it to disk.

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

## Per-model variants (optional — include only what's useful)

These are optional nudges, not a required fixed set. If the user named
a target generator, expand the variant for *theirs* plus one or two
alternatives for portability. Examples of generators with known nudges
in references/model-routing.md (Z-image, OpenAI/DALL-E, Imagen,
Midjourney, SDXL):

### <generator the user named, or a common one>
<prompt with that generator's phrasing tweaks from references/model-routing.md>

### <one or two alternatives for portability>
<universal block + the alternative's nudges>

## Notes

- This prompt is model-agnostic. The block structure works across
  generators; per-model variants above add the small phrasing nudges
  each model responds to.
- For the negative prompt, paste the [NEGATIVE] block verbatim into
  your generator's negative-prompt field (where supported).
- Verify the output against the craft-marker checklist in
  references/anti-patterns.md — hi-fi requires at least 5 of 6
  markers.
```

## What to include / what to skip

- **Always include** the universal prompt and the negative block.
- **Always include** a one-line note pointing at the craft-marker
  checklist.
- **Include** 1–3 per-model variants — expand the one for the
  generator the user named, plus a couple of alternatives for
  portability. The variants are optional nudges, not a required set.

## Surfacing the brief to the user

**Return** the brief to the caller as a value — do not write it to a
repo path. Example user-facing line:

> I can't generate an image in this runtime, so here's a portable
> prompt brief. It works in any generator — paste the universal block,
> or use one of the per-model variants for a tighter fit. If an image
> generator becomes reachable, I'll generate + quantize inline next
> time.
