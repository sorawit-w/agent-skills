# Node Stack

Use for legacy compatibility, unsupported dependencies, or when team expertise is Node-centric.

> **Related:** [Mobile](../guides/mobile.md) | [Styling](../guides/styling.md) | [Hosting](../guides/hosting.md)

---

## Stack Overview

| Layer | Tool | Notes |
|-------|------|-------|
| **Runtime** | Node 22 LTS | Stable, mature ecosystem |
| **Frontend** | Next.js / Angular | React ecosystem or enterprise SPAs |
| **Backend** | NestJS | DI, modules, mature tooling |
| **Database** | Neon + Drizzle / Prisma | Drizzle preferred; Prisma for migrations |
| **Auth** | Clerk | Same as other stacks |
| **Testing** | Vitest + Playwright | Fast unit tests, cross-browser E2E |
| **Styling** | Tailwind + SCSS + shadcn/ui | Full component library support |
| **Deployment** | Vercel (Next.js) / Cloud Run | Platform-optimized |

---

## Monorepo: Nx

For Node projects, use **Nx** for advanced monorepo tooling:

```bash
npx create-nx-workspace@latest my-monorepo --preset=apps
```

**Standard project structure:**

```
my-monorepo/
├── nx.json               # Nx configuration
├── package.json          # pnpm workspaces
├── apps/
│   ├── web/              # Customer-facing web (Next.js)
│   ├── mobile/           # Customer-facing mobile (Expo)
│   ├── admin/            # Internal admin dashboard (Next.js)
│   └── api/              # Backend API (NestJS)
└── libs/
    └── shared/           # shared types
```

```bash
pnpm install             # install all deps
nx serve web             # run specific app
nx run-many -t test      # run tests across all
nx affected -t build     # build only changed
nx graph                 # visualize dependencies
```

**Why Nx for Node:**

- Dependency graph visualization
- Affected-based testing and building
- Caching (local + Nx Cloud)
- Generators for consistent setup

---

## When to Use Node

- Legacy codebases or dependencies not yet Bun-compatible
- Team expertise is primarily Node-based
- Framework requirements (e.g., specific NestJS plugins)

---

## Frontend: Next.js

```bash
npx create-next-app@latest my-app
cd my-app && pnpm install

# add shadcn/ui
npx shadcn@latest init

pnpm dev
```

## Frontend: Angular

```bash
npx @angular/cli@latest new my-app
cd my-app && pnpm install

pnpm start
```

---

## Backend: NestJS

```bash
npx @nestjs/cli new my-api
cd my-api && pnpm install

pnpm start:dev
```

- Enable Swagger via `@nestjs/swagger`
- Serve API docs under `/docs`

---

## Database & Auth

**Drizzle (preferred):**

```bash
pnpm add drizzle-orm @neondatabase/serverless
pnpm add -D drizzle-kit
```

**Prisma (alternative):**

```bash
pnpm add prisma @prisma/client
pnpm prisma generate
pnpm prisma migrate dev --name init
```

**Auth: Clerk**

```bash
pnpm add @clerk/nextjs  # or @clerk/backend
```

---

## Testing

```bash
# unit tests (Vitest)
pnpm vitest

# e2e tests (Playwright)
pnpm exec playwright test
```

---

## Styling

- **Tailwind CSS** + **shadcn/ui** for React/Next.js
- **Angular Material** + **Tailwind** (layout only) for Angular
- **SCSS modules** for complex custom styling

---

## Deployment

**Vercel (Next.js):**

```bash
vercel --prod
```

**Cloud Run (containerized):**

```bash
docker build -t gcr.io/$GCP_PROJECT/api:$(git rev-parse --short HEAD) .
gcloud run deploy api --image gcr.io/$GCP_PROJECT/api:$(git rev-parse --short HEAD) --region=$GCP_REGION
```

---

## Mobile: Expo

Expo is the default mobile framework. Node/pnpm is the most common setup for Expo projects.

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
npx create-expo-app my-app -t expo-template-blank-typescript
cd my-app && pnpm install

# add navigation (Expo Router)
npx expo install expo-router expo-linking expo-constants

# development
npx expo start

# build for production
npx eas build --platform all

# submit to stores
npx eas submit --platform all
```

> **More details:** See [guides/mobile.md](../guides/mobile.md)

---

## Command Cheatsheet

```bash
# package management
pnpm install
pnpm add <package>
pnpm remove <package>

# scaffolding
npx create-next-app@latest my-app      # Next.js
npx @angular/cli@latest new my-app     # Angular
npx @nestjs/cli new my-api             # NestJS
npx create-expo-app my-app             # Expo mobile

# development
pnpm dev
pnpm start:dev

# testing
pnpm vitest
pnpm exec playwright test

# database
pnpm drizzle-kit generate
pnpm prisma migrate dev --name init

# mobile
npx expo start                         # development
npx eas build --platform all           # production build
npx eas submit --platform all          # store submission

# deployment
vercel --prod                          # Vercel
docker build -t <tag> .                # Docker
```

---

## Nx Project Configuration

**Project Configuration Preference:**

- Always use `project.json` for defining project targets in Nx
- This ensures structured metadata, dependency graph clarity, and caching
- Keep `project.json` files in each `apps/` and `libs/` project

| Situation | Preferred File | Reason |
|-----------|----------------|--------|
| Full-featured app/lib | `project.json` | Enables caching, `dependsOn`, structured Nx graph |
| Small scripts/utilities | `package.json` | Simpler, faster setup |
| Prototyping or PoC | `package.json` | Minimal config |
| Production/CI projects | `project.json` | Consistency and maintainability |

**Nx Maintenance:**

```bash
nx graph                    # visualize dependency health
nx repair                   # fix after upgrades
nx migrate latest           # update frameworks
nx g convert-to-project-json --all  # migrate legacy
```
