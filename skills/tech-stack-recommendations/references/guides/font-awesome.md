# Font Awesome v7 — AI Agent Reference Guide

> [!NOTE]
> This document assumes a **Pro+ subscription** with access to **Font Awesome v7.x**. All families, styles, and Pro+ small-batch packs are available.
>
> The primary runtime used in examples is **Bun**. Adjust commands to match the project's actual runtime (npm, yarn, pnpm, etc.) as needed.

---

## 1. Core Concepts

### Terminology

| Term | Definition |
|---|---|
| **Family** | The visual shape/geometric style of icons (e.g. Classic has rounded corners, Sharp has 90° angles) |
| **Style** | The weight/thickness within a family (Solid, Regular, Light, Thin, Semibold) |
| **Pack** | A collection of icons sharing a family+style. "Small Batch" packs are curated sets of ~200 common icons |
| **Kit** | A Font Awesome project container that bundles selected icon styles, custom icons, and delivery settings |
| **Subset** | A slimmed-down version of FA containing only the icons/styles a project actually uses |

### Icon Class Syntax

Every icon requires **two or three CSS classes** on an `<i>` or `<span>` element:

```
<i class="[family-class] [style-class] fa-[icon-name]"></i>
```

- **Family class** — optional for Classic (it's the default), required for others: `fa-sharp`, `fa-duotone`, `fa-sharp-duotone`, `fa-brands`, `fa-chisel`, etc.
- **Style class** — `fa-solid`, `fa-regular`, `fa-light`, `fa-thin`, `fa-semibold`
- **Icon name** — always prefixed with `fa-`, e.g. `fa-user`, `fa-camera`

**Examples:**
```html
<!-- Classic Solid (default family, can omit fa-classic) -->
<i class="fa-solid fa-user"></i>

<!-- Sharp Light -->
<i class="fa-sharp fa-light fa-user"></i>

<!-- Duotone Regular -->
<i class="fa-duotone fa-regular fa-user"></i>

<!-- Sharp Duotone Thin -->
<i class="fa-sharp-duotone fa-thin fa-user"></i>

<!-- Brand icon (no style needed) -->
<i class="fa-brands fa-github"></i>

<!-- Small Batch: Jelly Fill -->
<i class="fa-jelly-fill fa-regular fa-user"></i>
```

---

## 2. All Available Families & Styles

### Major Packs (Full Icon Coverage)

These packs have full parity with the entire FA icon library.

| Family | Available Styles | CSS Classes | Shorthand | Plan |
|---|---|---|---|---|
| **Classic** | Solid, Regular, Light, Thin | `fa-solid`, `fa-regular`, `fa-light`, `fa-thin` | `fas`, `far`, `fal`, `fat` | Free (Solid/Regular), Pro (Light/Thin) |
| **Duotone** | Solid, Regular, Light, Thin | `fa-duotone fa-solid`, etc. | `fad`, `fadr`, `fadl`, `fadt` | Pro |
| **Sharp** | Solid, Regular, Light, Thin | `fa-sharp fa-solid`, etc. | `fass`, `fasr`, `fasl`, `fast` | Pro |
| **Sharp Duotone** | Solid, Regular, Light, Thin | `fa-sharp-duotone fa-solid`, etc. | `fasds`, `fasdr`, `fasdl`, `fasdt` | Pro |
| **Brands** | Single style | `fa-brands` | `fab` | Free |

### Small Batch Packs (Pro+ Only, ~200 Curated Icons Each)

These are **design-forward, opinionated** packs — each with a unique visual personality. They do NOT have full icon parity with the major packs.

| Pack | Style(s) | CSS Classes | Visual Character |
|---|---|---|---|
| **Chisel** | Regular | `fa-chisel fa-regular` | Chiseled, carved stone look |
| **Etch** | Solid | `fa-etch fa-solid` | Etched/engraved line art |
| **Graphite** | Thin | `fa-graphite fa-thin` | Pencil-sketched, hand-drawn feel |
| **Jelly** | Regular, Fill Regular, Duo Regular | `fa-jelly fa-regular`, `fa-jelly-fill fa-regular`, `fa-jelly-duo fa-regular` | Soft, bubbly, rounded |
| **Notdog** | Solid, Duo Solid | `fa-notdog fa-solid`, `fa-notdog-duo fa-solid` | Bold, quirky, modern |
| **Slab** | Regular, Press Regular | `fa-slab fa-regular`, `fa-slab-press fa-regular` | Heavy serif/slab-serif weight |
| **Thumbprint** | Light | `fa-thumbprint fa-light` | Organic, fingerprint-like textures |
| **Utility** | Semibold, Fill Semibold, Duo Semibold | `fa-utility fa-semibold`, `fa-utility-fill fa-semibold`, `fa-utility-duo fa-semibold` | Clean, functional, UI-optimized |
| **Whiteboard** | Semibold | `fa-whiteboard fa-semibold` | Hand-sketched whiteboard marker style |

### Custom Kit Icons

When using a Kit with uploaded custom icons:
```html
<i class="fa-kit fa-custom-icon-name"></i>
<i class="fa-kit-duotone fa-custom-icon-name"></i>
```

---

## 3. Style Selection Guide — Matching Icon Styles to Project Context

This is the **decision framework** for recommending icon families/styles based on a project's domain, tone, and design language.

> [!IMPORTANT]
> If a project's domain is **not listed** in the tables below, the agent should evaluate independently based on the project's visual tone, target audience, and design language. Use the **"By Icon Size Context"** and **"By Design System Pairing"** tables as additional signals, and apply best judgment drawing from the patterns in the listed domains.

### By Project Domain & Tone

| Project Type / Domain | Recommended Primary | Recommended Alt | Why |
|---|---|---|---|
| **Enterprise / SaaS dashboard** | Classic Solid or Regular | Sharp Solid, Utility | Professional, clean, universally readable |
| **Banking / Fintech** | Sharp Solid or Regular | Classic Solid | Precision, trust, no-nonsense geometric lines |
| **Healthcare / Medical** | Classic Regular or Light | Classic Solid for key actions | Open, approachable, calm weight that doesn't overwhelm |
| **Legal / Government** | Classic Solid | Slab Regular | Authoritative, formal, reliable |
| **E-commerce / Retail** | Classic Solid + Duotone | Jelly for playful brands | Duotone adds visual depth; Solid for clarity at small sizes |
| **Children/Education apps** | Jelly Regular or Jelly Fill | Notdog Solid | Friendly, playful, rounded forms kids respond to |
| **Creative portfolio / Design** | Graphite Thin | Etch Solid, Chisel Regular | Hand-drawn/artistic feel that complements creative work |
| **Startup / Modern web app** | Classic Regular or Light | Sharp Regular | Regular weight feels contemporary without being heavy |
| **Developer tools / IDEs** | Classic Solid (small UI) | Utility Semibold | Small icon sizes need heavier weights for clarity |
| **Media / Entertainment** | Duotone Solid | Notdog Duo Solid | Two-tone depth adds richness for visual-first brands |
| **Documentation / Blogs** | Classic Regular | Classic Light | Unobtrusive, pairs well with text-heavy layouts |
| **Mobile app (iOS/Material)** | Sharp Regular (iOS feel) or Classic Regular (Material feel) | Sharp Light for iOS, Classic Solid for Material actions | Match platform conventions |
| **Presentation / Pitch deck** | Whiteboard Semibold | Graphite Thin | Whiteboard mimics hand-drawn presentation style |
| **Internal admin tools** | Classic Solid | Utility Semibold | Functional, compact, high-contrast at small sizes |
| **Luxury / Premium brand** | Classic Thin or Light | Graphite Thin, Thumbprint Light | Delicate, refined, lots of white space |

### By Design System Pairing

| Design System / Framework | Best Match | Notes |
|---|---|---|
| **Material Design 3** | Classic Regular/Solid | Most similar to Material Symbols in weight/proportion |
| **Apple Human Interface** | Sharp Regular/Light | Sharp 90° angles mirror SF Symbols aesthetic |
| **Ant Design** | Classic Solid + Regular | Matches Ant's dual-weight system |
| **Shadcn/ui** | Classic Light or Regular | Minimalist, outline-first UI |
| **Bootstrap** | Classic Solid (default) | Bootstrap historically ships with FA Solid |

### By Icon Size Context

| Rendered Size | Recommended Weight | Rationale |
|---|---|---|
| **< 16px** (inline text, badges) | Solid or Semibold | Thin strokes become invisible at tiny sizes |
| **16–24px** (navigation, buttons) | Regular or Solid | Standard UI range — most weights work |
| **24–48px** (feature highlights) | Regular, Light, or Duotone | More detail visible, lighter weights breathe |
| **> 48px** (hero, decorative) | Light, Thin, or Graphite | Large icons need delicate strokes or they feel chunky |

---

## 4. Setup Methods

> [!NOTE]
> All package install commands below use **Bun** as the primary runtime. Substitute with `npm install --save`, `yarn add`, or `pnpm add` if the project uses a different package manager.

### Method 1: Kit (Recommended)

A Kit is a managed project container on fontawesome.com. **Best for most projects.**

**Workflow:**
1. Create a Kit at [fontawesome.com/kits](https://fontawesome.com/kits)
2. Choose: Free or Pro/Pro+ styles
3. Choose delivery: **Hosted** (easiest), **Self-Host**, **Package**, or **Desktop Download**
4. Optionally configure subsetting, domain restrictions, v4 compat
5. Add embed code to `<head>`:

```html
<!-- Hosted Kit embed (JS-based, default) -->
<script src="https://kit.fontawesome.com/YOUR_KIT_CODE.js" crossorigin="anonymous"></script>

<!-- CSS-only Kit embed (no JS, Web Fonts only, requires v7 + Web Fonts) -->
<link rel="stylesheet" href="https://kit.fontawesome.com/YOUR_KIT_CODE.css" crossorigin="anonymous">
```

**Kit Package (via Bun):**
```bash
# Configure .npmrc for Kit packages
@fortawesome:registry=https://npm.fontawesome.com/
@awesome.me:registry=https://npm.fontawesome.com/
//npm.fontawesome.com/:_authToken=YOUR_TOKEN

# Install
bun add @awesome.me/kit-KIT_CODE@latest
```

> [!IMPORTANT]
> **Pro+ small-batch icons are ONLY available via Kit Packages**, not through individual SVG icon packages.

### Method 2: Package Manager (Individual Packages)

For JS-based apps (React, Vue, Angular) with tree-shaking needs.

**Free packages** (no auth needed):
```bash
bun add @fortawesome/fontawesome-svg-core
bun add @fortawesome/free-solid-svg-icons
bun add @fortawesome/free-regular-svg-icons
bun add @fortawesome/free-brands-svg-icons
```

**Pro packages** (requires `.npmrc` auth config):
```bash
# .npmrc
@fortawesome:registry=https://npm.fontawesome.com/
//npm.fontawesome.com/:_authToken=YOUR_PRO_PACKAGE_TOKEN

# Install the styles you need
bun add @fortawesome/fontawesome-svg-core
bun add @fortawesome/pro-solid-svg-icons
bun add @fortawesome/pro-regular-svg-icons
bun add @fortawesome/pro-light-svg-icons
bun add @fortawesome/pro-thin-svg-icons
bun add @fortawesome/sharp-solid-svg-icons
bun add @fortawesome/duotone-solid-svg-icons
# ... etc. for each family+style combo
```

**All-Inclusive packages** (everything, large):
```bash
bun add @fortawesome/fontawesome-free   # Free
bun add @fortawesome/fontawesome-pro    # Pro (auth required)
```

### Method 3: Self-Hosted (Downloaded Kit or Manual Download)

Download from [fontawesome.com/download](https://fontawesome.com/download) or download a Kit. Contents include `css/`, `js/`, `webfonts/`, `svgs/`, `scss/`, `sprites/`, `metadata/`.

---

## 5. Rendering Technology: Web Fonts vs SVG + JS

| Feature | Web Fonts + CSS | SVG + JS |
|---|---|---|
| **Setup complexity** | Simpler | Requires JS |
| **CSS pseudo-elements** | ✅ Native support | Requires config |
| **Power transforms / masking / layering** | ❌ | ✅ |
| **Duotone color control** | Limited | Full control |
| **Tree-shaking** | N/A | ✅ (with bundler) |
| **Auto-subsetting** | ✅ (Kit only) | ✅ (Kit) / tree-shaking (packages) |
| **Best for** | Simple sites, CMS, no-JS needs | JS frameworks (React, Vue, Angular) |

**Decision rule:** If the project uses a JS framework (React, Vue, Angular, etc.), prefer **SVG + JS** with tree-shaking. If it's a CMS, static site, or no-JS environment, use **Web Fonts + CSS**.

---

## 6. Framework Integration Quick Reference

### React

```bash
bun add @fortawesome/fontawesome-svg-core @fortawesome/free-solid-svg-icons @fortawesome/react-fontawesome
```

```jsx
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import { faUser } from '@fortawesome/free-solid-svg-icons'

<FontAwesomeIcon icon={faUser} />

// Sharp family
import { faUser as faUserSharp } from '@fortawesome/sharp-solid-svg-icons'
<FontAwesomeIcon icon={faUserSharp} />
```

### Vue

```bash
bun add @fortawesome/fontawesome-svg-core @fortawesome/free-solid-svg-icons @fortawesome/vue-fontawesome@latest
```

```js
import { library } from '@fortawesome/fontawesome-svg-core'
import { FontAwesomeIcon } from '@fortawesome/vue-fontawesome'
import { faUser } from '@fortawesome/free-solid-svg-icons'
library.add(faUser)
```

```vue
<font-awesome-icon icon="fa-solid fa-user" />
```

### Angular

Use `@fortawesome/angular-fontawesome`. See [docs](https://docs.fontawesome.com/web/use-with/angular).

### WordPress

Use the [official Font Awesome WordPress plugin](https://docs.fontawesome.com/web/use-with/wordpress). Supports Kit-based setup with no code changes needed.

---

## 7. Styling Utilities Quick Reference

Icons inherit CSS `font-size` and `color` by default. Additional utility classes:

| Capability | Classes | Notes |
|---|---|---|
| **Sizing** | `fa-xs`, `fa-sm`, `fa-lg`, `fa-xl`, `fa-2xl`, `fa-1x`…`fa-10x` | Relative to parent or fixed multipliers |
| **Fixed width** | `fa-fw` | All icons same width — great for nav menus, lists |
| **List icons** | `fa-ul` + `fa-li` | Replace bullet points with icons |
| **Rotation** | `fa-rotate-90`, `fa-rotate-180`, `fa-rotate-270`, `fa-flip-horizontal`, `fa-flip-vertical` | |
| **Animation** | `fa-spin`, `fa-spin-pulse`, `fa-beat`, `fa-fade`, `fa-beat-fade`, `fa-bounce`, `fa-flip`, `fa-shake` | v7 has many built-in animations |
| **Border + pull** | `fa-border`, `fa-pull-left`, `fa-pull-right` | For pull-quote-style icon placement |
| **Stacking** | `fa-stack`, `fa-stack-1x`, `fa-stack-2x` | Layer icons on top of each other |
| **Power transforms** | `data-fa-transform="grow-6 rotate-45 up-2"` | SVG+JS only |
| **Masking** | `data-fa-mask="fa-solid fa-circle"` | SVG+JS only — crop icon inside shape |
| **Layering** | `fa-layers`, `fa-layers-counter`, `fa-layers-text` | SVG+JS only — combine icons + text |
| **Duotone colors** | CSS custom properties: `--fa-primary-color`, `--fa-secondary-color`, `--fa-primary-opacity`, `--fa-secondary-opacity` | Control both layers |

---

## 8. Subsetting & Performance

### Subsetting Options (Kit Only)

| Method | How It Works | Best For |
|---|---|---|
| **Auto-Subsetting** | Kit analyzes pages and serves only used icons on-the-fly | Most projects — zero maintenance |
| **Subset by Style** | Include only chosen styles (e.g., Solid + Regular only) | Projects that only need specific weights |
| **Custom Subset by Icon** | Hand-pick exact icons to include | Maximum performance, production apps |

### Performance Tips

- Use **Kit auto-subsetting** for hosted delivery — it's automatic
- Use **tree-shaking** when using SVG icon packages with a bundler (Webpack, Vite, etc.)
- Avoid the **all-inclusive package** (`@fortawesome/fontawesome-pro`) in production — it's very large
- Prefer **Kit packages** (`@awesome.me/kit-*`) over individual packages — they're pre-subsetted
- Domain-lock Kits to avoid unexpected pageview charges

---

## 9. Accessibility

- **Decorative icons** (next to text that already describes them): add `aria-hidden="true"` — FA does this automatically in SVG+JS mode
- **Semantic icons** (conveying meaning without text): add `role="img"` and a `title` attribute or `aria-label`
- Icons used as interactive elements (buttons/links) should have visible or `aria-label` text

```html
<!-- Decorative (auto-hidden in SVG+JS) -->
<button><i class="fa-solid fa-trash" aria-hidden="true"></i> Delete</button>

<!-- Semantic (icon-only button) -->
<button aria-label="Delete item">
  <i class="fa-solid fa-trash" role="img" title="Delete"></i>
</button>
```

---

## 10. Agent Decision Checklist

When a user describes a project, **gather this context** to recommend the right setup:

1. **Tech stack?** → Determines setup method (Kit embed vs packages vs self-host)
2. **Runtime / package manager?** → Bun (default), npm, yarn, pnpm — adjust install commands accordingly
3. **Framework?** → React/Vue/Angular need SVG+JS packages; static/CMS sites use Web Fonts
4. **Project domain/industry?** → Use the Style Selection Guide (Section 3) table. If the domain is not listed, evaluate independently using the project's visual tone, target audience, and design patterns as signals
5. **Design system?** → Match icon family to the design system's visual language
6. **Icon sizes needed?** → Smaller needs heavier weights; larger can go lighter
7. **Performance sensitivity?** → Recommend Kit auto-subsetting or tree-shaking
8. **Custom icons needed?** → Must use a Kit (Pro) with icon upload
9. **Pro+ packs desired?** → Must use Kit packages (`@awesome.me/kit-*`)
10. **CI/CD pipeline?** → Needs `.npmrc` token config for Pro packages

> [!CAUTION]
> **If the recommended icon styles are not currently installed or enabled in the project's Font Awesome Kit or packages**, do NOT silently fall back to a different style. Instead, **ask the user to set up the required styles** — either by updating their Kit settings on fontawesome.com (adding styles, adjusting the subset) or by installing the needed packages. Kit configuration and token management require user action and cannot be done by the agent.

### Setup Recommendation Flowchart

```
Start
  ├── Using JS framework? (React/Vue/Angular/etc.)
  │   ├── Yes → Need Pro+ small-batch packs?
  │   │   ├── Yes → Kit Package (@awesome.me/kit-KIT_CODE)
  │   │   └── No → Individual SVG Icon Packages (@fortawesome/*)
  │   │        └── Configure .npmrc if Pro
  │   └── Consider adding @fortawesome/react-fontawesome (or vue/angular equiv)
  │
  ├── Static site / CMS / No-JS?
  │   ├── Yes → Kit Hosted Embed (one <script> or <link> tag)
  │   └── WordPress? → Use official WP plugin with Kit
  │
  └── Need full control / air-gapped?
      └── Download Kit → Self-host (Web Fonts or SVG+JS)
```

---

## 11. Key URLs

| Resource | URL |
|---|---|
| Icon Search | https://fontawesome.com/icons |
| Kit Management | https://fontawesome.com/kits |
| Plans & Pricing | https://fontawesome.com/plans |
| Pro Package Tokens | https://fontawesome.com/account#pro-package-tokens |
| Documentation Root | https://docs.fontawesome.com/ |
| Changelog / What's New | https://docs.fontawesome.com/upgrade/whats-changed |
| Style Gallery | https://fontawesome.com/icons?t=packs |
