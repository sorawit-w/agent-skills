# Title-card prompt template

Use this for: chapter titles, game splash screens, video/podcast
intro cards, atmospheric thumbnails with title text.

**Two paths in v1:**

1. **Image-gen path** — background imagery via an image model
   (using the prompt below), text added separately via the SVG
   template (`title-card.svg`) so the typography stays crisp.
2. **Pure SVG path** — use only `title-card.svg` with a solid or
   gradient background. Best when text is the entire subject.

Whichever path you pick, **text is always SVG** (not in the image
generation). Image models render text inconsistently; SVG renders
it perfectly.

## Fill in these tokens

- `<title>` — the title text (e.g., *"Whispers of the Flame"*)
- `<font>` — `VT323` (default) or alternate from `references/fonts.md`
- `<palette>` — palette name + hex anchors
- `<mode>` — `hi-fi` (default for title cards) or `lo-fi`
- `<background-subject>` — optional one-line description if you
  want background imagery (e.g., *"dimly-lit tavern interior with
  fireplace"*)
- `<lighting>` — profile from `references/lighting.md`
- `<style>` — title styling (e.g., *bold + inset shadow*, *thin
  outlined*, *with subtle glow*)

## Universal prompt — image-gen path (background imagery only)

```
[STYLE] <mode> pixel art — hi-density crafted pixel work, sharp pixel
edges, deliberate hue shifts, cluster studies, atmospheric haze;
DIMMED for title text overlay (60% brightness, slight gaussian-free
soft tint at center to seat the title)

[PALETTE] <palette name> — <hex anchors>

[SUBJECT] <background-subject> — rendered as atmospheric backdrop,
NOT as foreground subject; details should be readable but quiet,
nothing competing with the title text overlay

[COMPOSITION] cinematic wide shot; center-frame visual gravity well
where the title will sit (a softer area, slight vignette); details
push to corners; background atmospheric haze

[LIGHTING] <lighting>; centralized soft glow to seat the title text;
no harsh highlights in the center of the frame

[DENSITY] ~96px-per-element; ordered dithering on atmospheric areas;
clean block fills on prominent props

[MOOD] cinematic, atmospheric, intriguing

[NEGATIVE] no rendered text, no signatures, no watermarks, no
anti-aliasing, no blur (other than the central-area dimming for
title-seat), no photo-real textures, no 3D rendering, no
living-artist style references
```

**Critical:** Add **"no rendered text"** to the negative — you do
not want the image model to render the title, because text rendering
in image models is unreliable. The title comes from the SVG.

## Pure SVG path (no image-gen)

If the title card needs no atmospheric backdrop, skip the image
prompt entirely and use only `title-card.svg`. Fill the SVG's
tokens:

- `{{TITLE}}` — the title text
- `{{FONT}}` — `VT323` (default) or family from `fonts.md`
- `{{FG_COLOR}}` — title foreground hex (typically palette's bright
  anchor)
- `{{SHADOW_COLOR}}` — inset shadow hex (typically palette's deep
  anchor)
- `{{BG_COLOR}}` — background hex (typically `#1f1410` candlelit or
  `#264653` warm-coastal-night)
- `{{WIDTH}}` / `{{HEIGHT}}` — canvas size (default 1280×720)

## Example — filled in (image-gen path)

Title: *"Whispers of the Flame"*

Image prompt (for the background):
```
[STYLE] hi-fi pixel art — hi-density crafted pixel work, sharp pixel
edges, deliberate hue shifts, cluster studies, atmospheric haze;
DIMMED for title text overlay (60% brightness)

[PALETTE] candlelit interior — oak #8b6f3c, hearth-orange #c2410c,
parchment #f5e7c4, shadow-brown #3a2a1a, candle-yellow #fde68a,
soot #1f1410

[SUBJECT] dimly-lit tavern interior with hearth at right, long
wooden tables, hanging lanterns; details quiet, atmospheric

[COMPOSITION] cinematic wide shot of tavern interior; center-frame
soft glow area for title-seat; details push to corners; atmospheric
haze in the foreground

[LIGHTING] candlelit, single warm hearth source at right, lanterns
as small accents, center-frame slightly brighter to seat title

[DENSITY] ~96px-per-element; ordered dithering on atmospheric haze;
clean block fills on tables and lanterns

[MOOD] mysterious, intimate, atmospheric

[NEGATIVE] no rendered text, no signatures, no watermarks, no
anti-aliasing, no blur, no photo-real, no 3D rendering, no
living-artist references
```

Then take the generated image and overlay the SVG title (from
`title-card.svg`):

- `{{TITLE}}` = "Whispers of the Flame"
- `{{FONT}}` = "VT323"
- `{{FG_COLOR}}` = `#f5e7c4` (parchment, palette's bright anchor)
- `{{SHADOW_COLOR}}` = `#3a2a1a` (shadow-brown, palette's deep anchor)
- `{{BG_COLOR}}` = transparent (the generated image is behind)

Result: hi-fi tavern-interior pixel art with crisp VT323 title in
bold + inset-shadow styling, palette-matched.

## Title styling — the "Whispers of the Flame" look

Per Kiang's reference: bold + **inset shadow**. The SVG template
implements this by default. Adjustable variants:

| Style | Effect |
|---|---|
| Bold + inset shadow (default) | Cinematic, weighty, like Kiang's reference |
| Thin + outlined | Lighter, more readable at small sizes |
| Glow (warm hue around letters) | Mystical, ethereal, fits candlelit / twilight palettes |
| No effect (solid color) | Minimal, modern lo-fi |

See `references/fonts.md` for CSS / SVG syntax for each.
