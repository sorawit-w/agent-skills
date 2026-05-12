# Lighting — time of day, mood, color temperature

Lighting is the single biggest mood lever. Pick a lighting profile
before composing the prompt; it ties together palette choice and
composition.

## Lighting profiles

### Golden hour — warm key, cool fill

Time: late afternoon, early evening. Key light is **warm, low-angle**;
fill light from sky is **cool**. Long shadows.

Palette pairing: warm coastal, sun-drenched market.

Prompt fragment:
```
[LIGHTING] golden hour, warm low-angle key light from west, cool
sky fill from east, long shadows raking across foreground
```

### Candlelit / hearth-lit — point source, falloff

Time: indoor night. Single warm point source (hearth, candle,
lantern). Sharp falloff to deep shadow. Faces and props pick up the
warmth where lit; everything else sinks into shadow-brown.

Palette pairing: candlelit interior.

Prompt fragment:
```
[LIGHTING] hearth-lit interior, single warm point source at the
fireplace, sharp falloff to deep shadow, faces near the hearth
glow warm, far corners deep brown-shadow
```

### Twilight — cool dominant, warm accents

Time: post-sunset, pre-night. Sky is violet-gray; ground is
desaturated. Warm light sources (lanterns, candles, fires) read
as small bright accents against the cool wash.

Palette pairing: twilight forest, stormy seas (calmer variant).

Prompt fragment:
```
[LIGHTING] twilight, cool desaturated overall wash, lantern light
as small warm accents, sky violet-gray
```

### Stormy — dramatic, low-key, sparse warm

Time: night during storm. Mostly cool/dark. Only one or two
intentional warm accents (lighthouse, ship lantern, distant window).
Rain or spray as texture.

Palette pairing: stormy seas.

Prompt fragment:
```
[LIGHTING] stormy night, low-key, mostly cool storm-blue and slate,
single warm lantern accent on the ship, rain streaks as fine texture
```

### Midday — high-key, flat shadows

Time: noon. Light from above. Short, hard shadows. Saturation is
high. Good for markets, busy plazas, action scenes.

Palette pairing: sun-drenched market, warm coastal (sunnier variant).

Prompt fragment:
```
[LIGHTING] midday sun, light from directly overhead, short hard
shadows, high saturation, busy plaza
```

### Dawn — soft warm, low contrast

Time: early morning. Soft warm light, low contrast, mist or fog.
The atmosphere is the main visual interest.

Palette pairing: warm coastal (foggy variant).

Prompt fragment:
```
[LIGHTING] dawn, soft warm low-angle light, low contrast, mist on
the water, atmospheric haze in the distance
```

### Banner / lo-fi — flat documentary

For lo-fi banners, lighting is **flat documentary**. No dramatic
shadows. Light reads as "from above" in a neutral way. The
warm-paper background is the main atmospheric anchor.

Prompt fragment (lo-fi):
```
[LIGHTING] flat documentary lighting, no dramatic shadows, light
from above, warm-paper background does the atmospheric work
```

## Mood adjective vocabulary

Pair these with the lighting profile in the `[MOOD]` block:

| Profile | Mood adjectives |
|---|---|
| Golden hour | warm, tranquil, lived-in, painterly, cinematic |
| Candlelit | cozy, intimate, smoky, secretive, mysterious |
| Twilight | mysterious, atmospheric, contemplative, hushed |
| Stormy | dramatic, tense, lonely, dangerous |
| Midday | busy, bright, energetic, hopeful |
| Dawn | hopeful, quiet, fresh, contemplative |
| Banner / lo-fi | hand-made, friendly, readable, documentary, retro |

## Color temperature anchors

| Hue | Read |
|---|---|
| Warm orange `#c2410c`, hearth `#e8732d` | Fire, lantern, hearth, sunset key light |
| Warm yellow `#fde68a`, `#fbbf24` | Candle, glow, sunlit highlights |
| Cool blue `#1e3a5f`, `#5d8aa8` | Sky fill, water, twilight wash, storm |
| Cool violet `#6b5b95` | Twilight sky, atmospheric depth |
| Neutral gray `#6b7280`, `#9ca3af` | Shadow on cool surfaces, fog, stone |

The general rule: **warm light produces cool shadow; cool light
produces warm shadow.** Not the same as "light vs dark version of
the same color" — that reads as flat. Hue shifts in shadows are
what the eye reads as painterly.

## Multiple sources

Indoor scenes often have 2–3 light sources. Name each, with its
direction and color temperature.

```
[LIGHTING] tavern interior, three sources: hearth (warm key,
right-foreground), tall narrow window (cool secondary, top-left),
candle on each table (warm point accents); shadows pool in the
ceiling corners
```

Avoid sources that contradict ("sunlight from both sides") — that
reads as flat.
