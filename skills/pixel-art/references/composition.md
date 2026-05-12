# Composition — layout, eye-line, focal point

Composition rules are mode-agnostic. They are the structural
backbone the model uses to place subject elements.

## Three-layer rule (hi-fi scenes)

Every hi-fi scene has three layers. Name them explicitly in the
prompt's `[COMPOSITION]` block.

| Layer | Role | Typical content |
|---|---|---|
| Foreground | Anchor + scale reference | Dock, table edge, foliage in front, character closest to viewer |
| Midground | Subject | The thing the image is about — ship at dock, tavern hearth, traveler on path |
| Background | Atmosphere + depth | Castle on cliff, distant trees, sky / sea, fog |

Atmospheric perspective applies — background is **desaturated +
shifted toward sky hue** vs. foreground. Name this in the prompt:

```
[COMPOSITION] mid-shot; foreground dock with crane and crates;
midground three ships at anchor; background castle on cliff with
atmospheric haze (desaturated, sky-shifted)
```

## Eye-line and horizon

The horizon line dictates how the image reads.

| Horizon position | Effect | When to use |
|---|---|---|
| Lower third | Sky-dominant, expansive | Sweeping vistas, ships at sea |
| Middle | Balanced | Standard scene composition |
| Upper third | Ground-dominant, intimate | Tavern interiors, market stalls, forest clearings |

State explicitly:

```
[COMPOSITION] eye-line at horizon (middle), or eye-line at upper third
(intimate interior)
```

## Focal point

Every image has one focal point. The model needs to know what it is
so contrast, light, and detail concentrate there.

```
[COMPOSITION] focal point: the candlelit hearth at center-right of
the tavern; everything else is supporting detail
```

Use lighting (Phase 5) and color (the palette anchor) to reinforce
focal point — the focal subject typically gets the warmest hue and
the highest contrast.

## Light source

State light source direction + type. This determines shadow
direction across the whole scene.

```
[LIGHTING] golden hour key light from west (off-frame right), cool
fill from sky (east), single warm lantern accent at dock
```

Multiple light sources are fine for indoor scenes (hearth + window +
candle) — name each. Avoid contradictory sources ("sunlight from
both sides") — that reads as flat lighting and breaks the painterly
effect.

## Character placement (when subject = character)

For character art, the composition shifts:

| Shot type | Use when |
|---|---|
| Portrait (head + shoulders) | NPC profile, dialog avatar |
| Half-body | Character with prop (sword, lantern, book) |
| Full-body | Standing pose, action stance, walk cycle reference |
| Three-quarter | Most versatile; shows posture without filling the frame |

State the shot type and the pose:

```
[COMPOSITION] three-quarter shot, knight standing with sword
shouldered, looking off-frame left toward unseen distance
```

## Building art

Buildings get their own composition rules:

| View | Use when |
|---|---|
| Front elevation | Inn sign, market stall, single facade |
| Three-quarter | Most common — shows two faces of the building, suggests space |
| Bird's-eye | Map-style, isometric, town overview |
| Ground-level worm's-eye | Heroic monument, castle gate from below |

State explicitly:

```
[COMPOSITION] three-quarter view of Old Oak Inn; oak tree to the
left as foreground anchor; cobblestone path leads viewer toward door
```

## Nature scenes

Nature scenes prioritize **silhouette layering** — overlapping
silhouettes at different distances create depth without explicit
focal point.

```
[COMPOSITION] forest clearing; foreground ferns (dark silhouette);
midground pine trunks (mid-tone); background canopy (light,
atmospheric); shaft of sunlight through canopy at center
```

## Title cards

Title cards are typographic compositions. The text IS the subject.
See `templates/title-card-prompt.md` for the full template. Key rule:
**typography occupies the center optical zone**, with optional
background imagery dimmed and behind a tint overlay.

## Lo-fi (banner) composition

Lo-fi banners follow the three-panel repo standard:

| Panel | Role |
|---|---|
| Left card | Context / input |
| Center card | The signature move (often warm-accent color) |
| Right card | Output / result |

Plus chapter markers in a row below, plus title centered top
(LinkedIn) or top-left (X). Pixel-art arrows between cards: `#6b7280`
(entering) → `#c2410c` (exiting).

See `assets/team-composer-li.svg` and `assets/team-composer-x.svg`
for canonical examples.

## When to deviate

These rules are defaults. Deviate when the user asks for it (and
state the deviation in the prompt) or when the subject demands it
(e.g., a vertical scroll for a tower, a panoramic for a coastline).
Do not deviate silently.
