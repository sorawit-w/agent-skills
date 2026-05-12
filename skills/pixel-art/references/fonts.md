# Font catalog — pixel-style fonts for title cards

Five pixel-style font families, hand-picked for title cards and
chapter headers. **VT323 is the default** (per Kiang). All five are
Google Fonts-available and load via the standard `<link>` /
`@import` URL.

## Default — VT323

- **Family:** `VT323`
- **Google Fonts:** https://fonts.google.com/specimen/VT323
- **Vibe:** terminal CRT, slightly chunky, monospace-flavored
- **Use for:** chapter titles, retro game splash screens, terminal /
  hacker aesthetic, lo-fi banner headlines
- **Weights:** 400 only (single weight; that is part of the charm)
- **CSS import:**
  ```html
  <link href="https://fonts.googleapis.com/css2?family=VT323&display=swap" rel="stylesheet">
  ```
- **Notes:** Excellent at large sizes (48px+). At small sizes it
  reads as standard monospace, not pixel. **Use ≥40px.**

## Alternate 1 — Pixelify Sans

- **Family:** `Pixelify Sans`
- **Google Fonts:** https://fonts.google.com/specimen/Pixelify+Sans
- **Vibe:** rounder, more modern pixel-art, friendly
- **Use for:** UI titles, modern game splash, friendly-toned banners
- **Weights:** 400, 500, 600, 700
- **CSS import:**
  ```html
  <link href="https://fonts.googleapis.com/css2?family=Pixelify+Sans:wght@400;500;700&display=swap" rel="stylesheet">
  ```

## Alternate 2 — Press Start 2P

- **Family:** `Press Start 2P`
- **Google Fonts:** https://fonts.google.com/specimen/Press+Start+2P
- **Vibe:** NES / arcade machine, blocky, very low-res
- **Use for:** 8-bit retro game titles, arcade aesthetic, very lo-fi
  banners. The blockiest of the catalog.
- **Weights:** 400 only
- **CSS import:**
  ```html
  <link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
  ```
- **Notes:** Very wide character spacing. Don't use for long titles
  — it gets unreadable past 4–5 words.

## Alternate 3 — Silkscreen

- **Family:** `Silkscreen`
- **Google Fonts:** https://fonts.google.com/specimen/Silkscreen
- **Vibe:** crisp, tiny, screen-print feel
- **Use for:** chapter sub-headers, small labels, technical readouts
  in scene compositions
- **Weights:** 400, 700
- **CSS import:**
  ```html
  <link href="https://fonts.googleapis.com/css2?family=Silkscreen:wght@400;700&display=swap" rel="stylesheet">
  ```
- **Notes:** Best at 14–24px. Larger sizes lose the screen-print
  character.

## Alternate 4 — DotGothic16

- **Family:** `DotGothic16`
- **Google Fonts:** https://fonts.google.com/specimen/DotGothic16
- **Vibe:** dot-matrix, slightly elegant, supports Japanese
- **Use for:** fantasy / JRPG title cards, international title work,
  scenes with Japanese text
- **Weights:** 400 only
- **CSS import:**
  ```html
  <link href="https://fonts.googleapis.com/css2?family=DotGothic16&display=swap" rel="stylesheet">
  ```

## Font picking — quick rules

| Title vibe | Pick |
|---|---|
| Default / when unsure | **VT323** |
| Modern / friendly | Pixelify Sans |
| Hard retro arcade | Press Start 2P |
| Small label or technical | Silkscreen |
| Fantasy / JRPG / Japanese | DotGothic16 |

## Title-card styling — the "Whispers of the Flame" look

Per Kiang's reference: bold + **inset shadow**. In SVG/CSS this is
two stacked `<text>` elements (or a single `text-shadow` on the
text element) — bright text on top, slightly offset dark text behind
to create the inset feel.

CSS approach:
```css
.title {
  font-family: 'VT323', monospace;
  font-size: 96px;
  color: #f5e7c4;
  text-shadow:
    2px 2px 0 #3a2a1a,   /* inset shadow */
    -1px -1px 0 #f5e7c4; /* highlight on top */
}
```

SVG approach (stack two `<text>` elements):
```xml
<text x="600" y="300" font-family="VT323" font-size="96"
      fill="#3a2a1a">Whispers of the Flame</text>
<text x="598" y="298" font-family="VT323" font-size="96"
      fill="#f5e7c4">Whispers of the Flame</text>
```

The shadow color should be the **deep-tone anchor of the chosen
palette** (e.g., `#3a2a1a` for candlelit, `#264653` for warm coastal,
`#1f1410` for stormy). The highlight should be the **bright anchor**
of the same palette.

## When to use a non-pixel font

Don't. The catalog above covers the use cases. If the user names a
non-pixel font, ask if they want one of the catalog or to go off-catalog
for a one-off (and then state it explicitly so it does not leak into
the canonical palette).
