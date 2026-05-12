# Character prompt template

Use this for: knight, merchant, traveler, NPC portrait, party
member, hero pose — anything where the *character* is the subject.

## Fill in these tokens

- `<mode>` — `hi-fi` or `lo-fi`
- `<character>` — one-line character description (e.g., *"a weathered
  fishmonger in apron and rolled-sleeve tunic"*)
- `<palette>` — palette name + hex anchors
- `<pose>` — three-quarter / portrait / full-body / action stance
- `<prop>` — what the character is holding or interacting with (optional)
- `<lighting>` — profile from `references/lighting.md`
- `<mood>` — adjectives

## Universal prompt

```
[STYLE] <mode> pixel art — hi-density crafted pixel work, sharp pixel
edges, deliberate hue shifts in shadows, cluster studies, painterly
skin shading via ordered dithering, sub-pixel detail in eyes and
facial features (hi-fi only)

[PALETTE] <palette name> — <hex anchors>

[SUBJECT] <character>

[COMPOSITION] <pose> shot; character centered; <prop placement if
any>; neutral or contextual background (specify "studio neutral" or
"in a tavern interior" etc.)

[LIGHTING] <lighting>, key light on character face from <direction>,
shadow falls toward <direction>

[DENSITY] ~96px-per-character (hi-fi character art benefits from
slightly higher density than scenes); ordered dithering on clothing
folds; block fills on hair and large garment areas; sub-pixel
detail in eyes / lantern glints

[MOOD] <mood>

[NEGATIVE] no anti-aliasing, no blur, no photo-real skin texture,
no realistic hair shading, no smooth shading gradients, no 3D
rendering, no signatures, no living-artist style references
```

## Example — filled in

Subject: *"a weathered fishmonger in apron and rolled-sleeve tunic"*

```
[STYLE] hi-fi pixel art — hi-density crafted pixel work, sharp pixel
edges, deliberate hue shifts in shadows, cluster studies, painterly
skin shading via ordered dithering, sub-pixel detail in eyes and
facial features

[PALETTE] warm coastal — sandstone #d9c2a3, sea-blue #5d8aa8,
sky-cream #f7f0e0, stone-gray #8b8680, rust-accent #b1542a

[SUBJECT] a weathered fishmonger in apron and rolled-sleeve tunic;
mid-50s; lined face, salt-grayed beard, kind eyes

[COMPOSITION] three-quarter shot; character centered; holding a
fish in left hand and a cleaver in right; background: blurred dock
detail (suggested, not detailed); eye-line at upper third (intimate
framing)

[LIGHTING] golden hour, warm key light from frame-right onto face,
cool fill from sky; sea-blue ambient reflection on apron

[DENSITY] ~96px-per-character; ordered dithering on apron folds;
block fills on tunic; sub-pixel detail in eyes and on knife blade

[MOOD] lived-in, weathered, kind, painterly

[NEGATIVE] no anti-aliasing, no blur, no photo-real skin, no
realistic hair, no smooth gradients, no 3D rendering, no
signatures, no living-artist style references
```

## Character notes

- **Faces** are where craft shows. Hi-fi mode allows sub-pixel detail
  in eyes (a single bright pixel for a glint), but be sparing — too
  much sub-pixel detail reads as noise.
- **Hair** is best as block-fills with one or two ordered-dithering
  highlights. Avoid trying to render individual strands.
- **Clothing folds** use 1–2 shadow shades plus a checkerboard
  bridge between them.
- **Lo-fi character art** is simpler — block fills on body, one
  highlight stripe on top edge (see banner characters in
  `assets/team-composer-li.svg`).
