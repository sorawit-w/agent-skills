# Density — pixel resolution & dithering rules

"Hi-density" pixel art is **not** "low-resolution image." It is
crafted pixel-by-pixel work that happens to render at low effective
resolution. The difference shows up in three places: per-unit
resolution, edge cleanup, and mid-tone treatment.

## Density anchors — name a reference, not a number

Image-generation models **do not honor numeric density targets**
(e.g. "approximately 96 pixels per character"). What they do honor
is **named reference aesthetics** their training data has seen at
scale. Pick the density anchor that matches your target and name it
in the `[DENSITY]` block.

| Anchor | Looks like | When to pick |
|---|---|---|
| **8-bit / NES-density** | Mario, Mega Man — chunky 16×16 sprites, ~4-color palettes per tile | Retro game homage, lo-fi banners with strong silhouette focus |
| **16-bit / SNES-density** | Chrono Trigger, Final Fantasy VI — 32–64px characters, painterly clusters | Default hi-fi if you want a classic painterly pixel look |
| **Modern indie-density** | Stardew Valley, Celeste, Hyper Light Drifter — moderate density, expressive | A common, well-supported target |
| **HD-pixel-game-density** | Octopath Traveler, Sea of Stars, Eastward — high density with HD-2D layering | Mid-tier hi-fi, ambitious craft |
| **AI-pixel-art-density** | The Kiang harbor / tavern reference screenshots — ultra-fine pixel grain, sub-pixel detail throughout | Top-tier hi-fi. Some generators reach finer grain than others from prompting alone — but the quantize pass (SKILL.md Phase 4) downscales to the target grid regardless, so name the anchor and let quantize do the gridding. |

State the anchor explicitly in the prompt:

```
[DENSITY] HD-pixel-game-density (Octopath Traveler / Sea of Stars
aesthetic) — fine pixel grain throughout; ordered Bayer dither at
every palette-shade transition in sky and water; visible checkerboard
at sky color shifts; clean block fills on foreground subjects;
sub-pixel detail in lantern glints and water reflections
```

If the user supplied a reference image, **name the closest anchor
above** (or "matching the supplied reference") rather than guessing a
pixel-per-character number. The model handles named aesthetics better
than numeric targets.

## Edge cleanup

**Forbidden:** anti-aliasing fringes, soft edges, blurry silhouettes.

**Required:** every silhouette is legible at thumbnail size. Negative
space matters as much as positive space — orphan pixels in negative
space read as noise and break the craft.

In the prompt:

```
[NEGATIVE] no anti-aliasing, no soft edges, no blur, no orphan pixels,
no isolated single pixels in negative space
```

## Mid-tone treatment via dithering

Hi-fi pixel art uses **ordered dithering** (Bayer or checkerboard
patterns) to bridge palette colors and create painterly mid-tones.
This is the visual cue that separates crafted pixel art from a
low-res photo.

| Treatment | When to use |
|---|---|
| 50% checkerboard | Bridge between two adjacent palette shades for cloth, smoke, water |
| Bayer 2×2 | Sky gradients, mid-tone shadows on large surfaces |
| Bayer 4×4 | Subtle mid-tones in distant background, atmospheric perspective |
| No dither (block fill) | Strong shapes — silhouettes, props, near-foreground objects |

In the prompt:

```
[STYLE] hi-density pixel art, painterly mid-tones via ordered
dithering (checkerboard and Bayer patterns) where shading transitions
between palette shades; clean block fills on foreground subjects
```

## Lo-fi density treatment

Lo-fi favors **flat block fills** with minimal dithering. The
scanlined paper background does the texture work; subjects should
read as crisp silhouettes.

| Treatment | When to use (lo-fi) |
|---|---|
| Flat block fill | Default for everything |
| 1px highlight stripe | Top edge of body / object to suggest light direction (see banner characters) |
| Minimal Bayer | Only for sky / paper depth, rare |

## Sub-pixel detail

Hi-fi allows sub-pixel detail in **faces, lantern light, water,
foliage**. Sub-pixel detail means **one or two off-palette pixels**
placed deliberately for a specific signal — a glint of light in an
eye, a sparkle on water, a single bright pixel on a candle flame.

Sub-pixel detail is **forbidden** in lo-fi mode — it reads as noise
against the scanlined background.

## Output resolution

Image generators do not render at "64 px tall" natively. Generate at a
standard resolution (1024×1024 or a 16:9 equivalent like 1280×720 is a
safe default for most generators) and let the model produce a
pixel-art-styled image — then the quantize pass (SKILL.md Phase 4)
downscales it to the named grid target and median-cut-quantizes the
palette. The prompt's `[DENSITY]` block names the *aesthetic target*;
the renderer sets the source resolution; `quantize.py` sets the final
grid.
