# Style modes — hi-fi vs lo-fi

This skill ships two style modes. They share composition + typography
rules but diverge on **density**, **palette range**, and **background
treatment**. Pick one before composing the prompt.

## `hi-fi` (default) — painterly hi-density pixel art

**Anchor:** medieval harbor at dusk, candlelit tavern interior,
twilight forest. The user's reference screenshots are the lodestar.

**Density.** ~64–128px-per-character (or per meaningful unit), then
upscaled with nearest-neighbor or sharp-bilinear. Sub-pixel detail is
allowed — facial features, lantern light, water reflections — but
edges stay clean (no anti-aliasing fringe).

**Palette range.** 32–48 colors typical. Multi-mood palettes with
deliberate hue shifts in shadow ramps (warm shadows on warm
materials, cool shadows on cool materials, NOT global desaturation).

**Background.** Painterly scenes with foreground / midground /
background separation. Backgrounds are atmospheric (clouds, distant
silhouettes, color gradients via dithering).

**Mood vocabulary.** Painterly, lived-in, atmospheric, cinematic,
warm, candlelit, twilight, dawn, tranquil, mysterious.

**When to pick.** Game scenes, character portraits, fantasy
interiors, atmospheric title cards, social-media cover images,
splash screens.

## `lo-fi` — scanlined warm-paper banner aesthetic

**Anchor:** the agent-skills banners (e.g.,
`assets/team-composer-li.svg`). Three-panel layouts on warm paper
background with horizontal scanlines.

**Density.** Lower — 32–48px-per-character. Simpler silhouettes.
Block-color fills with minimal dithering. Pixel-art icons and props
rather than painterly scenes.

**Palette range.** 8–16 colors typical. Tight palette per asset.
Warm-paper background (`#f5efe6`) with `#eadfcf` scanlines is the
signature.

**Background.** Flat scanlined paper. No depth. Three-panel
composition (left = context, center = subject, right = output) is
the repo's standard.

**Mood vocabulary.** Hand-made, retro, readable, friendly,
documentary, schematic.

**When to pick.** Repo banners, blog headers, retro UI mockups,
documentation illustrations, skill icons.

## Cross-mode rules

- **Both modes** use the same font catalog (`fonts.md`).
- **Both modes** forbid anti-aliasing fringes.
- **Both modes** forbid living-artist-name prompts.
- **Hi-fi** prioritizes craft markers (hue shifts, clusters,
  dithering). **Lo-fi** prioritizes silhouette legibility and
  scanlined-paper background.

## Switching modes mid-prompt

If a user asks for a hi-fi scene but with a lo-fi-style background
(scanlined paper), that is **not a separate mode** — it is a hi-fi
scene with a stylized background. Note this in the composition block
of the prompt; do not switch the density profile.
