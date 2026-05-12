# Scene prompt template

Use this for: harbor scenes, tavern interiors, forest clearings,
market plazas, mountain passes — anything where the *place* is the
subject.

## Fill in these tokens

- `<mode>` — `hi-fi` or `lo-fi` (see `references/style-modes.md`)
- `<subject>` — one-line scene description (e.g., *"medieval harbor
  at dusk with a stone lighthouse and three ships at anchor"*)
- `<palette>` — palette name from `references/palette.md` + 4–6 hex
  anchors
- `<time-of-day>` — golden hour / candlelit / twilight / stormy /
  midday / dawn (see `references/lighting.md`)
- `<focal-point>` — the one thing the eye lands on (e.g., *"the
  lighthouse at center-left"*)
- `<mood>` — 2–4 adjectives from the lighting profile

## Universal prompt (model-agnostic)

```
[STYLE] <mode> pixel art — hi-density crafted pixel work, sharp pixel
edges, deliberate hue shifts in shadows, cluster studies (no orphan
pixels), painterly mid-tones via ordered dithering, nearest-neighbor
upscale aesthetic

[PALETTE] <palette name> — <hex 1>, <hex 2>, <hex 3>, <hex 4>, <hex 5>

[SUBJECT] <subject>

[COMPOSITION] mid-shot; foreground <foreground element with scale
reference>; midground <subject placement>; background <atmospheric
backdrop>; eye-line at <horizon position>; focal point: <focal-point>

[LIGHTING] <time-of-day>, <key light direction and color>, <fill
light direction and color>, <accent lights if any>

[DENSITY] ~96px-per-character (hi-fi) / ~40px-per-character (lo-fi);
ordered dithering at palette-shade transitions; clean block fills on
foreground subjects

[MOOD] <mood>

[NEGATIVE] no anti-aliasing, no blur, no soft edges, no photo-real
textures, no 3D rendering, no JPEG artifacts, no signatures, no
living-artist style references, no orphan pixels, no banding in
large surfaces, no pure-lightness shadows
```

## Example — filled in

Subject: *"medieval harbor at dusk"*

```
[STYLE] hi-fi pixel art — hi-density crafted pixel work, sharp pixel
edges, deliberate hue shifts in shadows, cluster studies (no orphan
pixels), painterly mid-tones via ordered dithering, nearest-neighbor
upscale aesthetic

[PALETTE] warm coastal — sandstone #d9c2a3, sea-blue #5d8aa8,
sky-cream #f7f0e0, stone-gray #8b8680, rust-accent #b1542a,
deep-water #264653

[SUBJECT] medieval harbor at dusk with a stone lighthouse and three
ships at anchor

[COMPOSITION] mid-shot; foreground stone dock with wooden crane and
cargo crates; midground three ships at anchor; background fortified
castle on cliff with atmospheric haze (desaturated, sky-shifted);
eye-line at middle horizon; focal point: the lighthouse at center-left

[LIGHTING] golden hour, warm low-angle key light from west, cool sky
fill from east, single lantern accent on dock, long shadows raking
foreground

[DENSITY] ~96px-per-character; ordered dithering at palette-shade
transitions; clean block fills on the lighthouse and ships; dithered
sky and water

[MOOD] tranquil, lived-in, painterly, cinematic

[NEGATIVE] no anti-aliasing, no blur, no soft edges, no photo-real
textures, no 3D rendering, no JPEG artifacts, no signatures, no
living-artist style references, no orphan pixels, no banding, no
pure-lightness shadows
```

## After generation

Run the craft-marker checklist from `references/anti-patterns.md`.
Hi-fi: at least 4 of 5 markers. If fewer, surface the gap and
regenerate with adjusted blocks.
