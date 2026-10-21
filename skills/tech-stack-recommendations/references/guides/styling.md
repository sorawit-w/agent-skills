# Styling & UI Reference

Load this when setting up styling or UI component systems.

---

## Framework-Specific UI

| Framework | Primary Libraries | Notes |
|-----------|------------------|-------|
| **SvelteKit** | Tailwind + Plain CSS | shadcn-svelte optional |
| **Next.js/React** | Tailwind + Plain CSS | shadcn/ui optional |
| **Angular** | Tailwind + Plain CSS | Angular Material for components |

---

## Shared Standards

- Theme tokens in `libs/styles/tokens.css`
- Support dark/light modes (WCAG AA minimum)
- Enforce **Stylelint** + **Autoprefixer**
- Avoid runtime CSS-in-JS for SSR

---

## Styling Rules

- **Tailwind** for layout, spacing, typography
- **Plain CSS** for animations, `:has()`, `@container`, `color-mix()`
- Rule: Tailwind for layout problems, CSS for visual experiences

---

## Component Documentation

| Framework | Tool | Setup |
|-----------|------|-------|
| **SvelteKit** | Histoire | `bunx histoire init` |
| **Next.js/React** | Storybook | `pnpm dlx storybook@latest init` |
| **Angular** | Storybook | `pnpm dlx storybook@latest init` |

- Document shared UI components in `libs/ui/`
- Include visual states, props, and usage examples

---

## Corporate Identity Doc

Create `.ai/IDENTITY.md` to capture project-specific design decisions:

**Contents:**
- Brand name, tagline, tone of voice
- Primary/secondary/accent colors (exact hex/HSL)
- Typography (fonts, sizes, weights, line heights)
- Logo usage rules
- Spacing scale (if deviating from Tailwind defaults)
- Component patterns (button styles, card variants, etc.)
- Do's and don'ts

**Location:** `.ai/IDENTITY.md`

> **Tip:** Keep it under 200 lines. AI agents work better with concise context.

---

## UI Excellence & Accessibility

**Accessibility (a11y):**
- Target **WCAG 2.2 AA** minimum
- Run automated audits: **axe-core**, **eslint-plugin-jsx-a11y**, **Pa11y**

**Performance Budgets:**
- FCP < 1.8s, LCP < 2.5s, CLS < 0.1, TBT < 200ms

**Localization (i18n):**
| Framework | Libraries |
|-----------|-----------|
| SvelteKit | `svelte-i18n`, `typesafe-i18n` |
| Next.js | `next-intl`, `lingui` |
| Angular | `@angular/localize` |

---

## AI Design Assistance (Optional)

When an AI coding agent does UI work, split the design skills by job. Only one skill edits a
surface; the others check it.

| Job | Skill | Notes |
|---|---|---|
| Make the change | [`impeccable`](https://github.com/pbakaus/impeccable) | `document` writes a `DESIGN.md` from existing code; `critique` → `polish` change a surface. Install: see its repo README. |
| Check direction | [`taste-skill`](https://github.com/Leonxlnx/taste-skill) | Run only its scripts (`inspect.mjs`, `lint.mjs`) as a read-only check — not the full skill, whose gate fixes every FAIL. |
| Verify the render | `screenwright` (this repo) | Its read-only mode V: axe in light and dark, desktop and phone width, 320px reflow, print styling. |

Give each skill the design spec's path explicitly; most look only for a root `DESIGN.md`.
