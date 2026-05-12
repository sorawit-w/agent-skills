# Palette — named palettes by mood

Pick one palette per generation. The palette name + hex anchors go
into the `[PALETTE]` prompt block. Models do not consistently honor
exact hex codes (especially across renderers), but **naming the
anchors in the prompt steers the model toward the intended hue
family** — that is the load-bearing function.

## Hi-fi palettes

### Warm coastal — *harbor, fishing village, sun-soaked dock*

Anchors: sandstone `#d9c2a3`, sea-blue `#5d8aa8`, sky-cream `#f7f0e0`,
stone-gray `#8b8680`, rust-accent `#b1542a`, deep-water `#264653`.

Mood: golden hour, lived-in, painterly, tranquil. Mid-tones lean
warm; cool only appears in water and distant sky.

### Candlelit interior — *tavern, hearth, inn common room*

Anchors: oak `#8b6f3c`, hearth-orange `#c2410c`, parchment `#f5e7c4`,
shadow-brown `#3a2a1a`, candle-yellow `#fde68a`, soot `#1f1410`.

Mood: cozy, warm, smoky, mid-shadow detail. The hearth is the key
light source; everything else picks up its warmth.

### Twilight forest — *forest clearing, dusk pines, mountain pass*

Anchors: pine-dark `#1f3a2e`, moss `#4a6741`, sky-violet `#6b5b95`,
fog-pale `#cfd8dc`, lantern-warm `#e8a04b`, root-brown `#2a1f12`.

Mood: mysterious, painterly, atmospheric perspective (distant
elements desaturated and shifted blue).

### Stormy seas — *night harbor, lighthouse, fishing ship in rain*

Anchors: storm-blue `#1e3a5f`, sea-foam `#a8c8d8`, lantern-orange
`#e8732d`, slate `#2a2f3a`, sail-cream `#e8dcc0`, deep-black `#0d1117`.

Mood: dramatic, cool-dominant, sparse warm accents from lantern light.

### Sun-drenched market — *daytime stalls, fruit baskets, plaza*

Anchors: terracotta `#c8743b`, sky-bright `#a8d8e8`, fabric-red
`#a82a2a`, fabric-green `#4a7a3a`, sandstone-pale `#e8d8b8`,
shadow-cool `#5a4a3a`.

Mood: high-key, saturated, busy, midday warmth.

## Lo-fi palettes (banner-style)

### Warm paper (default banner mode)

Anchors: paper-base `#f5efe6`, paper-edge `#eadfcf`, ink `#1f2937`,
warm-accent `#c2410c`, muted `#6b7280`, soft-shadow `#9ca3af`.

Use the `<pattern>` background from existing banners — `#f5efe6`
with `#eadfcf` 2px stripes every 6px (or 8x8 pattern with 6-row
stripes per `team-composer-li.svg`).

### Card-paper variants

For lo-fi card foregrounds: warm card `#f3e7c9`, cool card `#fdf7ea`,
border-wood `#b79a5c`, border-deep-wood `#c9b58a`.

### Chip colors (lo-fi accents)

- Yellow chip: `#fde68a` / `#fbbf24`
- Blue chip: `#bae6fd` / `#0e7490`
- Green pass: `#15803d` / `#dcfce7` / `#0d7c3c`
- Red flag: `#b91c1c` / `#fecaca`

## How to pick

1. **Match the subject.** Harbor scenes → warm coastal. Tavern
   interior → candlelit. Forest path → twilight forest.
2. **Match the time of day.** Morning leans warm-coastal or
   sun-drenched-market. Evening leans candlelit or twilight.
3. **Match the mood.** Tranquil → warm coastal. Mysterious →
   twilight forest. Dramatic → stormy seas.
4. **Lo-fi banners** default to **warm paper** unless the user
   wants something else.

## Palette anchors in prompts

Format the `[PALETTE]` block as:

```
[PALETTE] warm coastal — sandstone #d9c2a3, sea-blue #5d8aa8,
sky-cream #f7f0e0, stone-gray #8b8680, accent rust #b1542a
```

Listing 4–6 anchors is enough. Listing every shade dilutes the
signal.

## Extending the catalog

When a new mood comes up regularly (e.g., snowy mountain, desert
caravan, sci-fi cyber-alley), **add it to this file** — do not
invent ad-hoc palettes inline. Naming the palette in `palette.md`
makes it reusable across future generations and across templates.
