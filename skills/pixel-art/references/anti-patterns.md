# Anti-patterns — what to forbid + craft-marker checklist

The single biggest failure mode for "make this pixel art" prompts is
the model returning a **low-resolution photograph** with a slight
mosaic filter. That is not pixel art. This file is the explicit forbid
list and the craft-marker checklist for verifying outputs.

## Forbidden (always)

State each in the `[NEGATIVE]` prompt block, exactly:

- **No anti-aliasing** — every pixel edge must be hard
- **No blur** — no Gaussian blur, no motion blur, no defocus
- **No soft edges** — silhouettes are crisp
- **No photo-real textures** — no realistic skin, no realistic
  rendered cloth, no realistic stone textures
- **No JPEG artifacts** — the rendered image should look like a
  PNG, not a compressed photo
- **No 3D rendering look** — no smooth gradients, no specular
  highlights as glow, no Blender / Unity / Unreal aesthetic
- **No artist signatures, watermarks, or text** (unless subject is
  `title-card`)
- **No living-artist style references** — IP guardrail

Standard `[NEGATIVE]` block:
```
[NEGATIVE] no anti-aliasing, no blur, no soft edges, no photo-real
textures, no 3D rendering, no JPEG artifacts, no signatures or
watermarks, no living-artist style references
```

## Forbidden (hi-fi only)

- **Orphan pixels** in negative space (single bright pixels floating
  unrelated to anything)
- **Long uniform bands** of a single color without dithering breakup
  (banding in skies, walls, water)
- **Mismatched dithering** (different dither patterns on adjacent
  surfaces — read as messy)
- **Pure-lightness shadow ramps** (a darker shade of the same hue,
  with no hue shift — reads as flat)

Add to `[NEGATIVE]` for hi-fi:
```
no orphan pixels, no banding in large surfaces, no pure-lightness
shadows without hue shift
```

## Forbidden (lo-fi only)

- **Sub-pixel detail** (reads as noise against scanlined paper)
- **Heavy dithering** (reads as muddy)
- **Multi-layer atmospheric perspective** (lo-fi is flat; depth comes
  from card layering, not air haze)
- **Saturated photographic backgrounds** (always use the warm-paper
  pattern)

Add to `[NEGATIVE]` for lo-fi:
```
no sub-pixel detail, no heavy dithering, no atmospheric perspective,
no photographic background, use scanlined warm-paper pattern
```

## Craft-marker checklist (hi-fi)

Apply before declaring a generation done. **Hi-fi mode requires at
least 5 of 6 markers** present in the output:

| # | Marker | What to look for |
|---|---|---|
| 1 | **Deliberate hue shifts** in shadows | Shadows are not just darker — they shift hue (warm-light scene → cool shadow; cool-light → warm shadow). Check a shadow ramp and verify the hue moves. |
| 2 | **Cluster studies** — no orphan pixels | Every detail is at least 2 pixels. Single floating bright pixels are removed. |
| 3 | **Banding avoidance** | Large uniform surfaces (sky, water, walls) show dithering or hue-stepping, not flat fields. |
| 4 | **Painterly mid-tones via ordered dithering** | At transitions between palette shades, a checkerboard or Bayer pattern bridges them. |
| 5 | **Clean edges** | Silhouettes are crisp at thumbnail size. No anti-aliasing fringes. |
| 6 | **Pixel scale matches the density anchor** | Output's pixel scale lands in the band named by `[DENSITY]` (see `density.md`). If `[DENSITY]` says HD-pixel-game-density and the output reads as 16-bit-SNES-density, it failed this marker even if 1–5 pass. **Compare to the named anchor or the user's supplied reference, not just internal craft.** |

**Reactive note:** marker 6 was added in v3.10.1 after a real failure
mode surfaced — Z-image scored 5/5 on markers 1–5 while still failing
the user's actual density target. Markers 1–5 check *how* pixels
behave; marker 6 checks *whether the pixels are the right size*.

If fewer than 5 markers are present, **regenerate** with adjusted
prompt blocks. Common fixes:

- Marker 1 missing → strengthen the lighting block's color
  temperature contrast
- Marker 2 missing → add "cluster pixels, no orphans" to the `[STYLE]`
  block
- Marker 3 missing → add "dithered skies and walls, no flat fields"
  to `[STYLE]`
- Marker 4 missing → strengthen `[DENSITY]` block with explicit
  dithering callout
- Marker 5 missing → strengthen `[NEGATIVE]` with "no anti-aliasing,
  crisp edges"
- Marker 6 missing → name the density anchor explicitly in `[DENSITY]`
  (see `density.md` anchor table) and let the quantize pass (SKILL.md
  Phase 4) downscale to the target grid — that normalizes pixel scale
  regardless of which generator produced the source. If the grain is
  still off after quantize, lower the `--grid` target, or (if you have
  another generator available) try regenerating there. Some generators
  reach finer grain than others from prompting alone, but that's a
  soft tendency, not a routing gate — see `model-routing.md`.

## Craft-marker checklist (lo-fi)

Lo-fi is more permissive. Check:

| # | Marker | What to look for |
|---|---|---|
| 1 | **Scanlined warm-paper background** | The `#f5efe6` base with `#eadfcf` stripes (or visual equivalent) is present |
| 2 | **Crisp silhouettes** | Characters / props read at thumbnail size |
| 3 | **Tight palette** | 8–16 colors, not a photographic gradient |
| 4 | **Three-panel layout** (banners) | Left context / center subject / right output, or single centered subject for icons |

If marker 1 (scanlined paper) is missing for a banner, regenerate.
Other markers are nice-to-have for lo-fi.

## Reference comparison

When the user provides a reference screenshot, compare the
generation against the reference for **style markers**, not for
**content**:

- Does the generation hit the same density (per-unit pixel scale)?
- Does the generation use a comparable palette range (number of
  colors, hue family)?
- Does the generation match the dithering style?
- Does the generation have the same edge cleanup discipline?

It is **explicitly fine and expected** for the generation's content
to differ — different ships, different buildings, different
characters. The skill produces original compositions, not derivatives.

## Surfacing failures to the user

When a generation fails the checklist, do not silently regenerate.
Tell the user:

> The first generation missed 2 craft markers: hue shifts in
> shadows (came out flat) and dithering on the sky (came out as a
> smooth gradient). Regenerating with stronger emphasis on both.

This makes the craft-discipline visible and gives the user a
chance to redirect.
