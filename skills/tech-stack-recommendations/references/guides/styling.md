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

**UI UX Pro Max** — Design intelligence skill for AI coding agents

When using Claude Code, Cursor, or similar AI assistants for UI work,
this skill provides a searchable database of styles, palettes, typography,
and UX guidelines.

- 57 UI styles, 95 color palettes, 56 font pairings
- Supports: Svelte, React, Next.js, Vue, Tailwind, and more

**Install:**
```bash
bunx uipro-cli init --ai claude       # Bun
npx uipro-cli init --ai claude        # Node
```

**Repo:** https://github.com/nextlevelbuilder/ui-ux-pro-max-skill
