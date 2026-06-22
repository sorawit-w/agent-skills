<p align="center">
  <img src="../../assets/pixel-art-li.svg" alt="pixel-art — a hi-density pixel-art studio" width="100%"/>
</p>

# pixel-art

A pocket-sized pixel-art studio. Hand it a short brief — *"medieval
harbor at dusk", "tavern interior with fireplace", "Whispers of
the Flame title card in VT323"* — and it returns a finished image
(whenever an image generator is reachable) or a model-agnostic prompt
brief you can paste into the generator of your choice. The style
is locked in `references/` so you don't have to re-describe palette,
density, composition, lighting, or typography every time.

It is **single-subject and generative**: it produces one raster, runs a
**deterministic quantize pass** so the output is true grid-aligned pixel
art (not a mosaic-filtered photo), and can serialize a single sprite to
SVG. It is **repo-agnostic** — it writes nothing to disk and **returns**
every artifact to the caller. And it is **honest**: asked for a composed
or branded SVG asset (banner, icon set, exact-text layout) it **declines**
rather than silently shipping a raster that isn't what you asked for.

## Why this exists

Hi-density pixel art is craft-marker work. The difference between
*pixel art* and *a low-res photograph with a mosaic filter* is
deliberate hue shifts in shadows, cluster studies, painterly
mid-tones via ordered dithering, and clean silhouettes. Re-typing
those constraints in every prompt is tedious and inconsistent. This
skill encodes them once — palette tokens, density specs, composition
rules, font catalog, anti-pattern checklist — and lets you express
the *intent* of an image in 4–6 words.

It also keeps you out of vendor lock-in. Every prompt this skill
emits is model-agnostic; the per-generator phrasing tweaks live in
`references/model-routing.md` and apply as small adjustments on top.
If you have Z-image Turbo, it runs inline. If you only have DALL-E
in another window, paste the brief there. Same prompt structure
either way.

## What it does

- **Two style modes.** `hi-fi` (painterly hi-density pixel art, the
  default — matches the harbor / tavern reference aesthetic) and
  `lo-fi` (scanlined warm-paper banner aesthetic, matching this
  repo's own banners).
- **Five subject categories.** Scenes, characters, buildings, nature,
  title cards. Each has its own prompt template; all share the same
  reference design system.
- **Built-in design system in `references/`.** Named palettes by
  mood, per-mode density specs with dithering rules, composition
  rules (three-layer scenes, eye-line, focal point, light source),
  lighting profiles (golden hour / candlelit / twilight / stormy /
  midday / dawn), a 5-font catalog (VT323 default + Pixelify Sans +
  Press Start 2P + Silkscreen + DotGothic16), and an explicit
  anti-pattern checklist with a 5-marker quality bar.
- **Attempt-then-fallback generation.** It *attempts* to generate by
  any means available in the runtime — host-native or an MCP tool — and
  only falls back to a copy-pasteable prompt brief when generation is
  genuinely impossible. No fixed vendor list, no "is server X
  connected?" gate. The brief is a first-class deliverable, not a
  degraded fallback.
- **Deterministic quantize.** After generation, a script
  (`scripts/quantize.py`, median-cut palette) downscales to a real
  grid and clamps the palette — so the output is grid-aligned pixel
  art with a bounded color count, not a diffusion image with tens of
  thousands of colors. Emits PNG or, for a single sprite, SVG.
- **Honest decline.** A Phase 0 gate stops composed/branded SVG-asset
  jobs (banners, icon sets, exact-text/layout, multi-asset sets) — it
  states the mismatch and stops, instead of substituting a raster.
- **Title-card SVG path.** For title cards specifically, also returns
  a portable SVG using VT323 (default) with bold + inset-shadow
  styling — the "Whispers of the Flame" look. Works without any
  image generator. (The one authored-SVG path the skill keeps.)
- **IP guardrail.** Mirrors `algorithmic-art`'s standard: never
  references living artists by name; produces original compositions,
  not derivatives of reference imagery.

## What it doesn't do

- **Vector illustration / SVG icon design** — pixel art is
  raster-first. Use `canvas-design` or hand-author SVG for vector
  work.
- **Logo or brand-identity packages** — route to `brand-workshop`.
- **Photo-realistic image generation** — wrong style entirely.
- **Algorithmic / generative art** with p5.js, flow fields, particle
  systems — use Anthropic's `algorithmic-art` skill.
- **Charts, dashboards, data visualization** — use the data-viz
  skills.
- **Rasterize an existing photograph as pixel art** — out of scope
  for v1; consider an external pixelate filter.

## When to use it

- *"Create a pixel-art harbor at dusk with a lighthouse."*
- *"Make a hi-fi pixel-art tavern interior."*
- *"Generate a lo-fi pixel banner like the agent-skills banners."*
- *"Title card for 'Whispers of the Flame' in VT323."*
- *"I want this style"* + hi-density pixel-art reference (treated as
  stylistic intent, not as a derivative source).
- *"Build me a pixel-art splash screen for chapter one."*

## When not to use it

- The user wants a logo or full identity package → `brand-workshop`.
- The user wants a chart, dashboard, or data report → data-viz skills.
- The user wants p5.js procedural art → Anthropic's `algorithmic-art`.
- The user wants vector illustration (clean lines, no pixels) →
  `canvas-design` or hand-authored SVG.
- The user wants a photo-real image with no pixel-art aesthetic →
  go directly to an image-gen MCP with a non-pixel-art prompt.

## How it works

```
brief → Phase 0 (deliverable-type gate) → Phase 1 (style) → Phase 2 (subject)
                                                                    ↓
                                                  Phase 3 (compose prompt)
                                                                    ↓
                              Phase 4 (attempt generate + quantize, or emit brief)
                                                                    ↓
                              Verification (type-check + craft-marker checklist)
```

1. **Phase 0 — Deliverable-type gate.** If the brief needs exact text,
   an exact layout/viewBox, brand tokens, an editable vector source, or
   a multi-asset set → it's a composition job; the skill **declines**
   honestly. (Title cards and single-sprite-SVG are carve-outs.)
2. **Phase 1 — Style mode.** Default `hi-fi`. Switch to `lo-fi` for a
   banner or retro UI mockup.
3. **Phase 2 — Subject detection.** Map the brief to one of five
   subjects (scene / character / building / nature / title-card). For
   mixed briefs, pick the dominant subject; note secondary subjects
   in the composition block.
4. **Phase 3 — Compose the prompt.** Load the relevant reference
   files once, fill the universal block format (`[STYLE]`, `[PALETTE]`,
   `[SUBJECT]`, `[COMPOSITION]`, `[LIGHTING]`, `[DENSITY]`, `[MOOD]`,
   `[NEGATIVE]`). Same structure across all five subjects.
5. **Phase 4 — Generation routing.** **Path A:** *attempt* inline
   generation by any available means; quantize the result with
   `scripts/quantize.py`; **return** the quantized PNG/SVG + the
   finalized prompt to the caller (no disk writes). **Path B** (only
   when generation is genuinely impossible): return a model-agnostic
   prompt brief. For title cards, **also** return the SVG title-card.
6. **Verification.** First a **deliverable-type check** (did the output
   kind match the request?), then the 6-marker craft checklist from
   `references/anti-patterns.md` (hi-fi requires 5 of 6; lo-fi is
   permissive). If markers are missing, surface the gap before
   regenerating.

## Design choices worth knowing

- **Capability-gated routing, not vendor-gated — detected by
  attempting.** The skill routes on *"can I generate at all?"*, not on
  *"is named server X connected?"* and not on *"is this Claude Code or
  Cowork?"*. Host-native generators aren't always introspectable, so it
  *attempts* generation and only briefs on genuine inability. New
  generators slot in for free; the vendor list in
  `references/model-routing.md` is optional phrasing nudges, not a gate.
- **Model-agnostic prompt structure.** The universal block format
  (`[STYLE] [PALETTE] [SUBJECT] [COMPOSITION] [LIGHTING] [DENSITY]
  [MOOD] [NEGATIVE]`) works across Z-image, SDXL, DALL-E, Imagen,
  Midjourney, OpenAI Image. Per-model tweaks are nudges on top, not
  rewrites.
- **Path B is first-class.** The prompt brief is what most users
  actually want — they have a preferred generator they want to run
  it in. Framing the brief as a "fallback" undersells it; the skill
  treats it as the primary deliverable when no MCP is connected.
- **Title-card text is always SVG.** Image models render text
  inconsistently. The skill paths around this by generating
  atmospheric background imagery via the image model and overlaying
  the title text via the SVG template. Two-step instead of one-shot,
  but the typography stays crisp.
- **VT323 as font default.** Chosen by Kiang. Catalog of 5 covers
  the common pixel-font use cases (terminal CRT, modern friendly,
  hard arcade, tiny labels, JRPG / Japanese).
- **6-marker craft-marker checklist** rather than a vibe check. Hue
  shifts in shadows, cluster studies, banding avoidance, painterly
  mid-tones via dithering, clean edges, and pixel-scale-matches-anchor.
  Hi-fi requires 5 of 6; each marker has a regenerate recipe in
  `references/anti-patterns.md`.

## Install

```bash
/plugin marketplace add sorawit-w/agent-skills
/plugin install agent-skills@sorawit-w
```

The skill auto-triggers on phrases like *"pixel art"*, *"pixel-art
scene"*, *"hi-fi pixel"*, *"lo-fi pixel banner"*, *"VT323 title
card"*, and similar.

## Cross-skill integration

| Skill | Relationship |
|---|---|
| `brand-workshop` | Logo / identity packages route there. A composed/branded asset set is a **decline** here (Phase 0), not a `pixel-art` job — the caller routes; this skill doesn't name where. |
| Anthropic's `algorithmic-art` | Sibling: algorithmic uses p5.js (procedural, seeded). `pixel-art` uses image-gen + prompts. Different toolchain. |
| Anthropic's `canvas-design` | Sibling: canvas-design ships static raster / PDF via design-philosophy prose. `pixel-art` ships pixel-style raster via tokens. |
| `team-composer` | If the brief is cross-disciplinary (e.g., game splash + marketing copy), team-composer assembles and may hand off the single-image deliverable to `pixel-art`. |
| Image generation (host-native or MCP) | Attempt-then-fallback dependency. Skill works with no generator at all via the prompt brief; works better when generation is reachable. |

## Status and scope

- **Repo-agnostic:** writes nothing to disk; returns every artifact to
  the caller.
- **Style modes supported:** `hi-fi` (default), `lo-fi`.
- **Subjects supported:** scenes, characters, buildings, nature,
  title cards (incl. SVG path).
- **Generation:** attempts inline by any reachable means (host-native
  or MCP); deterministic median-cut quantize post-process; PNG or
  single-sprite SVG output. Falls back to a model-agnostic prompt brief
  only when generation is genuinely impossible.
- **Out of scope:** composed/branded SVG-asset jobs (banners, icon
  sets, exact-text/layout, multi-asset sets — these are **declined**,
  not substituted); image-to-pixel-art conversion of existing
  photographs; animated / sprite-sheet output. The repo's own
  house-style banner/icon authoring is a separate initiative.

## Contributions

Not accepting external contributions right now. Feel free to fork.

## License

MIT.
