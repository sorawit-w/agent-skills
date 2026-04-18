# Frontend Framework Reference

Load this when choosing a frontend framework for a new project.

---

## Quick Decision Guide

| Your Need | Recommended | Why |
|-----------|-------------|-----|
| **Best default, smallest bundles** | SvelteKit | Best DX, tiny output, Bun-native |
| **Content sites, blogs, docs** | Astro | Zero JS by default, island architecture |
| **React ecosystem, complex state** | Next.js | Mature, huge ecosystem, Vercel-optimized |
| **React + forms-heavy, progressive enhancement** | Remix | Built-in loaders/actions, works without JS |
| **React + TanStack ecosystem** | TanStack Start | File routing + TanStack Query/Router/Form |
| **Max performance, fine-grained reactivity** | SolidStart | React-like DX, no VDOM, fastest runtime |
| **Extreme performance, zero hydration** | Qwik | Resumability model, 0kb initial JS |
| **Vue projects** | Nuxt | Full-featured Vue framework |
| **Enterprise, large teams, strict conventions** | Angular | DI, modules, strong typing |

---

## Detailed Comparison

| Framework | Ecosystem | Rendering | Best For | Trade-offs |
|-----------|-----------|-----------|----------|------------|
| **SvelteKit** | Svelte | SSR, SSG, SPA | General web apps, dashboards | Smaller ecosystem than React |
| **Next.js** | React | SSR, SSG, ISR | Complex apps, e-commerce, SaaS | Heavy runtime, React lock-in |
| **Remix** | React | SSR, forms | Data-heavy apps, progressive forms | Newer, smaller community |
| **TanStack Start** | React | SSR, client | TanStack-heavy apps | Very new, less battle-tested |
| **SolidStart** | Solid | SSR, SSG | Performance-critical apps | Small ecosystem, learning curve |
| **Qwik** | Qwik | Resumable | Landing pages, instant interactivity | Unique model, niche ecosystem |
| **Astro** | Any (islands) | SSG, SSR | Content sites, marketing, docs | Not ideal for complex SPAs |
| **Nuxt** | Vue | SSR, SSG | Vue-based projects | Vue-specific |
| **Angular** | Angular | SSR, SPA | Enterprise apps, large teams | Heavy, steeper learning curve |

---

## Tie-Breaking Rule

> [!IMPORTANT]
> When multiple frameworks seem equally suitable, prefer **minimal magic** frameworks.
> The less implicit behavior, the more control and clarity.

**Preference order (when requirements don't favor one):**

1. **SvelteKit** — Template ≈ HTML, explicit reactivity, minimal abstraction
2. **Vue/Nuxt** — Template-based, explicit reactivity, readable Options API
3. **Angular** — Strict conventions and structure, but more decorator/DI magic
4. **React-based** (Next.js, Remix, etc.) — Implicit hook rules, hidden re-renders
5. **Others** — Evaluate case-by-case

---

## Scaffolding Commands

```bash
# SvelteKit (default)
bunx sv create my-app

# Next.js
bunx create-next-app@latest my-app

# Remix
bunx create-remix@latest my-app

# TanStack Start
bunx create-start@latest my-app

# SolidStart
bunx create-solid@latest my-app

# Qwik
bunx create-qwik@latest my-app

# Astro
bunx create-astro@latest my-app

# Nuxt
bunx nuxi@latest init my-app

# Angular
bunx @angular/cli@latest new my-app
```

---

## Agent Framework Selection Behavior

When no framework is explicitly specified, analyze business requirements and suggest the best fit.

**Decision Logic:**

| Condition | Agent Action |
|-----------|--------------|
| Framework explicitly specified | Use it, no prompt needed |
| Strong signal for non-default | Suggest alternative, explain why, ask to confirm |
| Ambiguous or general requirements | Use default (SvelteKit), optionally mention alternatives |

**Signal-to-Framework Mapping:**

| Business Signal | Suggested | Why |
|-----------------|-----------|-----|
| "documentation", "blog", "marketing site" | Astro | Zero JS, content-optimized |
| "e-commerce", "complex dashboard", React team | Next.js | Mature ecosystem, ISR |
| "forms-heavy", "progressive enhancement" | Remix | Built-in actions, works without JS |
| "TanStack Query/Router already used" | TanStack Start | Native integration |
| "performance-critical", "real-time updates" | SolidStart | Fine-grained reactivity |
| "landing page", "instant interactivity" | Qwik | Zero hydration cost |
| "Vue team", "Vue components" | Nuxt | Vue ecosystem |
| "enterprise", "large team", "strict conventions" | Angular | DI, modules, typing |
| General web app, no strong signals | SvelteKit (default) | Best DX, smallest bundles |

**Rules:**

- Always explain *why* the suggestion differs from default
- If user declines, proceed with default without further prompting
- Log the decision in `.ai/context.yaml` under `stack.frontend`
