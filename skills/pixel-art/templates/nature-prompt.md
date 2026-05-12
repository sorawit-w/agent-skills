# Nature prompt template

Use this for: forest clearing, river bend, mountain pass, cliff
edge, meadow, beach, cave entrance — anything where the *natural
environment* is the subject and built structures are absent or
secondary.

## Fill in these tokens

- `<mode>` — `hi-fi` (lo-fi rarely fits nature subjects)
- `<environment>` — one-line description (e.g., *"twilight pine
  forest clearing with a shaft of sunlight piercing the canopy"*)
- `<palette>` — palette name + hex anchors
- `<silhouette-layering>` — what overlapping silhouettes create
  depth (e.g., "foreground ferns / midground trunks / background
  canopy")
- `<lighting>` — profile from `references/lighting.md`
- `<mood>` — adjectives

## Universal prompt

```
[STYLE] hi-fi pixel art — hi-density crafted pixel work, sharp pixel
edges, deliberate hue shifts, cluster studies, atmospheric
perspective (foreground saturated, background desaturated and shifted
toward sky hue), painterly foliage via ordered dithering

[PALETTE] <palette name> — <hex anchors>

[SUBJECT] <environment>

[COMPOSITION] silhouette-layered depth: foreground <fg silhouette>
in darkest palette shade; midground <mg silhouette> in mid-tone;
background <bg silhouette> in lightest, sky-shifted shade; focal
point <where the light or detail concentrates>

[LIGHTING] <lighting>, light source direction, atmospheric haze
treatment, any volumetric effects (shafts of light through canopy,
fog at distance)

[DENSITY] ~96px-per-large-element; ordered dithering on foliage
and sky; block fills on close foreground silhouettes; subtle
sub-pixel detail for glints (water sparkle, leaf highlight)

[MOOD] <mood>

[NEGATIVE] no anti-aliasing, no blur, no photo-real foliage
textures, no realistic 3D vegetation, no smooth gradients in sky,
no signatures, no living-artist style references
```

## Example — filled in

Subject: *"twilight pine forest clearing with a shaft of sunlight
piercing the canopy"*

```
[STYLE] hi-fi pixel art — hi-density crafted pixel work, sharp pixel
edges, deliberate hue shifts, cluster studies, atmospheric
perspective, painterly foliage via ordered dithering

[PALETTE] twilight forest — pine-dark #1f3a2e, moss #4a6741,
sky-violet #6b5b95, fog-pale #cfd8dc, lantern-warm #e8a04b,
root-brown #2a1f12

[SUBJECT] twilight pine forest clearing with a single shaft of late
sunlight piercing the canopy and lighting a patch of forest floor

[COMPOSITION] silhouette-layered depth: foreground ferns in
pine-dark; midground pine trunks in moss with hue-shifted shadows;
background distant trees in sky-violet (desaturated, sky-shifted);
focal point the sunlit clearing floor at center

[LIGHTING] twilight just before dusk, single warm sunbeam from
upper-right cutting through canopy, cool ambient wash everywhere
else, faint volumetric haze in the sunbeam

[DENSITY] ~96px-per-large-element; ordered dithering on foliage
masses and the violet sky glimpses; block fills on close fern
silhouettes; sub-pixel detail in the sunbeam (a couple of dust-mote
glints)

[MOOD] mysterious, atmospheric, hushed, painterly

[NEGATIVE] no anti-aliasing, no blur, no photo-real foliage, no
realistic 3D vegetation, no smooth sky gradient, no signatures, no
living-artist style references
```

## Nature notes

- **Silhouette layering** is what creates depth in pixel-art nature
  scenes. Three overlapping silhouettes at different distances do
  more than one detailed central subject.
- **Atmospheric perspective** = distant elements lose saturation
  and shift toward the sky's hue. State this explicitly in the
  composition block — image models otherwise paint all distances
  with equal saturation.
- **Foliage** is best rendered as masses with ordered dithering at
  the silhouette edges, not as individual leaves. The eye reads the
  mass as detailed even when each leaf is implied, not drawn.
- **Volumetric effects** (sunbeams, fog) work via per-column shading
  shifts — list the effect explicitly in the lighting block.
- **Water** picks up the sky color; running water gets a
  checkerboard dither for movement, still water gets a horizontal
  banding.
