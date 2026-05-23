# DESIGN.md — Design-Token Authority

The agent's contract for repos that contain a project-level `DESIGN.md`.

---

## When This Rule Fires

- The repo has a file named exactly `DESIGN.md` (uppercase) at its root, AND
- The current task touches UI, styling, theming, or anything that references design tokens (colors, typography, spacing, radius, motion).

**HTML document export counts.** Producing a self-contained HTML version of a document (see `references/html-export.md`) is a styling task — its stylesheet references design tokens — so `DESIGN.md` governs the export's colors and typography.

If both conditions hold, this rule overrides any local guess about design tokens. If `DESIGN.md` is absent, see [Absence](#absence) below.

---

## Location

`DESIGN.md` lives at the repo root. If you find a `DESIGN.md` elsewhere in the tree (e.g., under `outputs/`, a sub-package, or a sibling folder), surface it as a warning and ask the developer where the authoritative copy should live. Do not silently pick one.

The `brand-workshop` skill emits `DESIGN.md` to its own output folder; the founder moves it to repo root when adopting. If you find one only at a non-root path, the adoption step likely hasn't happened yet — ask before treating it as authoritative.

---

## Authority

When `DESIGN.md` exists at repo root, the YAML front matter IS the canonical design contract. Treat its tokens — colors (hex, sRGB only), typography, spacing, rounded values, components — as authoritative.

- **DO NOT** invent alternative tokens, palettes, or scales when generating UI.
- **DO NOT** silently override a token because the surrounding code uses a different value — flag the drift instead (see [Conflict Resolution](#conflict-resolution)).
- The markdown body explains *why* the tokens are what they are. Read it before generating UI; cite it when explaining design choices to the developer.

---

## Editing Safety

When asked to edit `DESIGN.md`:

- **Never strip the YAML front matter.** It is the cross-plugin contract — downstream skills (e.g., `validation-canvas`, `riskiest-assumption-test`, `pitch-deck`) parse it directly.
- Edit prose freely. The markdown body explains the *why* and tolerates iteration.
- For token changes, surface a diff and confirm with the developer before writing.
- Preserve the canonical section order: Overview → Colors → Typography → Layout → Shapes → Do's and Don'ts → Voice. Custom sections are allowed and appear after Voice (preserved by spec-compliant consumers under the spec's "unknown section" rule).
- If a spec linter is available, run it after the edit:
  ```bash
  npx @google/design.md lint DESIGN.md
  ```

This file is in the same category as `references/guardrails.md` → "Overwrite guideline/spec files" — read-only for unrelated tasks; edits require explicit instruction and a confirmed diff.

---

## Conflict Resolution

If the project also has downstream theme configs, `DESIGN.md` is the single source of truth. Common downstream targets:

- `tailwind.config.{ts,js}` — Tailwind theme tokens
- `components.json` + `app/globals.css` — shadcn/ui tokens
- `theme.ts` / `tokens.ts` / CSS-in-JS theme files (Stitches, Emotion, vanilla-extract, Panda) — or similar

Behavior on drift:

1. Detect drift between `DESIGN.md` tokens and downstream files.
2. Flag the divergence — name which token diverges where.
3. Offer to regenerate the downstream from `DESIGN.md`. The spec ships an `export` command; prefer it over hand-rewriting:
   ```bash
   npx @google/design.md export DESIGN.md --format tailwind > tailwind.theme.js
   npx @google/design.md export DESIGN.md --format dtcg > tokens.json
   ```
4. Do not rewrite downstream files silently. The developer chooses whether to regenerate.

---

## Absence

If no `DESIGN.md` exists at repo root, fall back to existing project conventions in this order:

1. Tailwind config (`tailwind.config.{ts,js}`)
2. CSS-in-JS theme or a `design-system/` / `tokens/` directory
3. shadcn `components.json` + `globals.css`
4. Figma exports referenced in the README

**Do not synthesize design tokens** unless the developer explicitly asks. If they want a starter system, route to the `DESIGN.md + ui-ux-pro-max` pattern in `references/recommendations.md` (signal: "UI work needed, no DESIGN.md or design system").

---

## Spec Version

The DESIGN.md spec is at `alpha` (current as of 2026-05). Schema may break before a non-alpha tag. Re-check the [spec repo](https://github.com/google-labs-code/design.md) when:

- The agent encounters a `DESIGN.md` whose front matter contains keys this rule doesn't recognize, or
- The spec repo tags a non-alpha version.

---

## See Also

- [DESIGN.md spec — google-labs-code](https://github.com/google-labs-code/design.md) — canonical schema and `export` command.
- [Stitch — design-md docs](https://stitch.withgoogle.com/docs/design-md/overview) — Google's reference implementation context.
- `references/external-resources.md` → `awesome-design-md` — 59 curated brand specs (Stripe, Linear, Notion, BMW…) usable as reference corpus or starting templates.
- `references/external-resources.md` → `ui-ux-pro-max` — pairs with `DESIGN.md` for stack-specific UI generation.
- `references/external-resources.md` → `impeccable` — frontend quality / anti-slop refinement after generation.
- `references/external-resources.md` → `taste-skill` — opinionated dial-based bias (DESIGN_VARIANCE / MOTION_INTENSITY / VISUAL_DENSITY) for UI execution.
- `agent-skills:brand-workshop` (upstream producer) — emits a starter `DESIGN.md` as part of a brand-identity package; the founder moves it to repo root when adopting.
- `references/html-export.md` — opt-in self-contained HTML document export; consumes `DESIGN.md` tokens for its stylesheet when present.
