# Building prompt template

Use this for: inn, castle gate, lighthouse, market stall,
guildhall, tower, ruin — anything where the *structure* is the
subject.

## Fill in these tokens

- `<mode>` — `hi-fi` or `lo-fi`
- `<building>` — one-line description (e.g., *"timber-framed
  three-story coastal inn with thatched roof and oak-tree sign"*)
- `<view>` — front elevation / three-quarter / bird's-eye / worm's-eye
- `<palette>` — palette name + hex anchors
- `<setting>` — what surrounds the building (street, market, hilltop,
  cliff, plaza)
- `<lighting>` — profile from `references/lighting.md`
- `<mood>` — adjectives

## Universal prompt

```
[STYLE] <mode> pixel art — hi-density crafted pixel work, sharp pixel
edges, deliberate hue shifts in shadow ramps, cluster studies,
material variation (stone vs wood vs thatch vs slate) via tight
palette shifts, sub-pixel detail in windows and signage

[PALETTE] <palette name> — <hex anchors>

[SUBJECT] <building>

[COMPOSITION] <view> view; <setting context>; foreground <anchor
detail — cobblestones, sign-post, foliage>; midground <building
itself>; background <atmospheric backdrop>

[LIGHTING] <lighting>, key light from <direction>, shadows fall
toward <direction>, window light if interior is implied

[DENSITY] ~96px-per-tile (hi-fi) — buildings benefit from per-tile
detail (one stone, one shingle, one timber); ordered dithering on
walls; block fills on signage and prominent features

[MOOD] <mood>

[NEGATIVE] no anti-aliasing, no blur, no photo-real textures, no
3D architectural rendering, no smooth roof gradients, no
signatures, no living-artist style references
```

## Example — filled in

Subject: *"timber-framed three-story coastal inn with thatched
roof and oak-tree sign"*

```
[STYLE] hi-fi pixel art — hi-density crafted pixel work, sharp pixel
edges, deliberate hue shifts, cluster studies, material variation
between dark timber framing and pale plaster fill via tight palette
shifts, sub-pixel detail in window panes and inn signage

[PALETTE] candlelit interior + warm coastal blend — oak #8b6f3c,
plaster-cream #f5e7c4, slate-roof #6b6258, sea-blue accent #5d8aa8,
hearth-warm #c2410c, shadow-brown #3a2a1a

[SUBJECT] timber-framed three-story coastal inn with thatched roof
and a wooden sign hanging from an oak-tree post; "Old Oak Inn"
painted on the sign

[COMPOSITION] three-quarter view of the inn; cobblestone street
foreground with two pedestrian figures for scale; midground the inn
itself with oak tree to the left; background: distant cliff and
sky; afternoon sun

[LIGHTING] midday into early afternoon, warm key from upper-right,
cool sky fill, two windows lit warm-yellow suggesting interior
hearth visible through panes

[DENSITY] ~96px-per-tile; per-timber-beam detail in framing; ordered
dithering on plaster walls and thatched roof; block fills on the
sign and shutters

[MOOD] welcoming, lived-in, sturdy, painterly

[NEGATIVE] no anti-aliasing, no blur, no photo-real wood texture,
no 3D architectural rendering, no smooth roof, no signatures, no
living-artist style references
```

## Building notes

- **Three-quarter view** is the most versatile — it shows two
  faces of the building, suggests depth, and reads well at small
  sizes.
- **Material variation** is what makes hi-fi buildings sing. Use
  the palette to mark timber vs plaster vs stone vs thatch via
  small palette shifts, not via realistic textures.
- **Signage and windows** are where sub-pixel detail belongs — a
  one-pixel candle glow in a window says "inhabited" without
  rendering an entire interior.
- **Lo-fi buildings** are simpler — silhouette + one accent color +
  block-fill windows.
