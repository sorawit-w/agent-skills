# Brand-source ladder — resolve or bootstrap DESIGN.md

Loaded in Phase 2. screenwright is both a **consumer** and a **bootstrapper** of DESIGN.md.
Stop at the first rung that hits. Whatever you resolve, write it in the same format —
[references/design-md-schema.md](design-md-schema.md).

## Rung 1 — DESIGN.md exists

Look for `DESIGN.md` at the repo/output root (and `./design.md`, `./.design/DESIGN.md`).
Found → parse its tokens + the `a11y` / `breakpoints` keys (default them if absent) and
use it. Do **not** re-bootstrap.

## Rung 2 — In a project, no DESIGN.md → infer from the repo

There's a codebase with styling but no DESIGN.md. Infer tokens from what's already there:

- **Colors** — scan CSS / Tailwind config / theme files / CSS custom properties for the
  recurring palette. Map the most-used brand color to `primary`, surfaces to
  `neutral`/`surface`, etc.
- **Typography** — font families from `font-family` declarations / `@font-face` / Tailwind
  `fontFamily`; sizes from the type scale in use.
- **Spacing / radius** — the recurring scale (4/8/16…) and border-radius values.

Then **persist** the inferred `DESIGN.md` at the repo root so later surfaces stay
consistent. State the inference is derived (so the user can correct it).

## Rung 3 — Greenfield / outside a project

No repo to infer from. Two sub-routes, both ending at **persist a DESIGN.md**:

### 3a — Named template (from awesome-design-md)

[`github.com/VoltAgent/awesome-design-md`](https://github.com/VoltAgent/awesome-design-md)
is **73 standalone DESIGN.md files, MIT-licensed**, organized by industry under
`/design-md/<slug>/`, each in the Stitch DESIGN.md format (a superset of ours).

1. **Menu** — `WebFetch` the repo README (it's the categorized catalog) and offer **3–5**
   entries matched to the brief's domain/vibe. Don't dump all 73.
2. **Pick** — `WebFetch` the raw file at `/design-md/<slug>/DESIGN.md`.
3. **Adopt** — keep what maps; our defaults fill missing `a11y` / `breakpoints`; keep any
   extra sections (components/elevation) as bonus painting context.
4. **Persist** — write it as the new project's DESIGN.md, **renamed** to the user's project.
   Adopt tokens/style only — do **not** reproduce the source brand's logo or wordmark.

> **Fragility note (the one external coupling).** This depends on the repo's README + the
> `/design-md/<slug>/` path convention staying stable. If a fetch fails, the repo
> restructured, or you're offline → fall straight to 3b. Never dead-end.

### 3b — Imply from the described vibe

The user describes a feel ("warm, editorial, lots of whitespace") rather than naming a
template. Assemble tokens from:
- **`ui-ux-pro-max`** style/palette/font vocabulary **if installed** (suggest it if not and
  the user wants a richer vibe library; don't synthesize its catalog), **or**
- model judgment from the description.

Then **persist** the DESIGN.md. This is also the **offline / fetch-failed fallback** for 3a.

## Positioning vs brand-workshop

`brand-workshop` is the thorough, interview-driven **author** of DESIGN.md (greenfield brand
identity). screenwright is the **quick bootstrap** when none exists. Both write the same
format. If the user wants a real brand identity (logo, tagline, full system), route them to
`brand-workshop` first, then screenwright reads its DESIGN.md.
