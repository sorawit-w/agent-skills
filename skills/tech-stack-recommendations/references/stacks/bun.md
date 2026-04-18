# Bun Stack

Complete stack for Bun-based projects. **Default for all new TypeScript/JavaScript projects.**

> **Related:** [Mobile](../guides/mobile.md) | [Styling](../guides/styling.md) | [Hosting](../guides/hosting.md)

---

## Stack Overview

| Layer | Tool | Notes |
|-------|------|-------|
| **Runtime** | Bun | Default for all new projects |
| **Frontend** | SvelteKit | Best DX, smallest bundles, `svelte-adapter-bun` |
| **Backend** | Elysia + Eden | End-to-end types, OpenAPI, TypeBox |
| **Database** | Neon + Drizzle | Scale-to-zero, SQL-like syntax, Bun-native |
| **Auth** | Clerk | Best DX, pre-built components, 10k MAU free |
| **Testing** | `bun test` + Playwright | Native, fast unit tests; cross-browser E2E |
| **Styling** | Tailwind + Plain CSS | Layout utilities + modern CSS features |
| **Deployment** | Railway (dev) / Cloud Run (prod) | Nixpacks for fast dev, Docker for prod |

---

## Monorepo: Bun Workspaces

Bun has native workspace support via `package.json`:

```json
{
  "name": "my-monorepo",
  "workspaces": ["apps/*", "packages/*"]
}
```

**Standard project structure:**

```
my-monorepo/
├── package.json          # workspaces defined here
├── apps/
│   ├── web/              # Customer-facing web app (SvelteKit)
│   ├── mobile/           # Customer-facing mobile app (Expo)
│   ├── admin/            # Internal admin dashboard (SvelteKit)
│   └── api/              # Backend API (Elysia)
└── packages/
    └── shared/           # shared types/utils
```

```bash
bun install                      # install all workspace deps
bun run --filter web dev         # run specific workspace
bun add lodash --filter api      # add to specific workspace
```

- Zero config, uses npm workspaces syntax
- Symlinks local packages automatically
- Single lockfile, fast installs

---

## Frontend: SvelteKit

```bash
# scaffold project
bunx sv create my-app
cd my-app && bun install

# add Tailwind CSS
bunx svelte-add tailwindcss

# development
bun run dev
```

- Use **Svelte 5 runes** for reactivity
- Use `svelte-adapter-bun` for production builds
- Component library (optional): **shadcn-svelte**

---

## Backend: Elysia

```bash
# create Elysia API
bun create elysia my-api
cd my-api && bun install

# development
bun run dev
```

- Use **Eden** (`@elysiajs/eden`) for type-safe client
- **TypeBox** validation as single source of truth for API types
- No code generation required—types flow automatically
- **API docs:** OpenAPI auto-generated at `/swagger`

---

## Database & Auth

**Database: Neon + Drizzle**

```bash
bun add drizzle-orm @neondatabase/serverless
bun add -D drizzle-kit
```

**Auth: Clerk**

```bash
bun add @clerk/backend
```

- Neon: Scale-to-zero, DB branching, sub-10ms queries
- Drizzle: SQL-like syntax, tiny runtime (~50KB)
- Clerk: Pre-built components, generous free tier

---

## Testing

```bash
# unit tests (native)
bun test

# e2e tests
bunx playwright test
```

---

## Styling

- **Tailwind** for layout, spacing, typography
- **Plain CSS** (Svelte scoped) for animations, `:has()`, `@container`, `color-mix()`
- Rule: Tailwind for layout problems, CSS for visual experiences

---

## Deployment

**Development:** Railway (Nixpacks auto-detect)

```bash
railway up
```

**Production:** Cloud Run (Docker)

```bash
docker build -t gcr.io/$GCP_PROJECT/api:$(git rev-parse --short HEAD) .
gcloud run deploy api --image gcr.io/$GCP_PROJECT/api:$(git rev-parse --short HEAD) --region=$GCP_REGION
```

**Static/SSG:** Netlify

```bash
netlify build && netlify deploy --prod
```

---

## Mobile: Expo

Expo is the default mobile framework for cross-platform iOS/Android development.

| Layer | Tool | Notes |
|-------|------|-------|
| **Framework** | Expo (React Native) | Managed workflow preferred |
| **Navigation** | Expo Router | File-based routing |
| **State** | Zustand / Jotai | Zustand for simple, Jotai for atomic state |
| **Storage** | Expo SecureStore + AsyncStorage | Secure for credentials, AsyncStorage for general |
| **Testing** | Jest + React Native Testing Library | Native component testing |
| **Build** | EAS Build | Cloud builds or `eas build --local` |
| **Deploy** | EAS Submit | Direct to App Store / Play Store |

```bash
# scaffold project
bunx create-expo-app my-app -t expo-template-blank-typescript
cd my-app && bun install

# add navigation (Expo Router)
bunx expo install expo-router expo-linking expo-constants

# development
bunx expo start

# build for production
bunx eas build --platform all

# submit to stores
bunx eas submit --platform all
```

> **More details:** See [guides/mobile.md](../guides/mobile.md)

---

## Command Cheatsheet

```bash
# package management
bun install
bun add <package>
bun remove <package>

# development
bun run dev
bun test
bun test --watch

# scaffolding
bunx sv create my-app          # SvelteKit
bun create elysia my-api       # Elysia API
bunx create-expo-app my-app    # Expo mobile

# database
bunx drizzle-kit generate
bunx drizzle-kit push

# mobile
bunx expo start                # development
bunx eas build --platform all  # production build
bunx eas submit --platform all # store submission

# deployment
railway up                     # Railway
docker build -t <tag> .        # Docker
netlify deploy --prod          # Netlify
```
