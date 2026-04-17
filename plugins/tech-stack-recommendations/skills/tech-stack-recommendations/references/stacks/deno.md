# Deno Stack

Use when sandbox security, direct TS imports, or Deno-native features are required.

> **Related:** [Mobile](../guides/mobile.md) | [Styling](../guides/styling.md) | [Hosting](../guides/hosting.md)

---

## Stack Overview

| Layer | Tool | Notes |
|-------|------|-------|
| **Runtime** | Deno | Secure by default, explicit permissions |
| **Frontend** | Fresh | Native Deno SSR, island architecture |
| **Backend** | Hono / Oak | Lightweight, Deno-native |
| **Database** | Deno KV (simple) / Neon + Drizzle | Built-in KV or Postgres |
| **Auth** | Clerk | Same as other stacks |
| **Testing** | `deno test` + Playwright | Native test runner |
| **Styling** | Tailwind | Via Twind or Fresh plugin |
| **Deployment** | Deno Deploy / Cloud Run | Edge-first or containerized |

---

## Monorepo: Deno Workspaces

Deno has native workspace support via `deno.json`:

```json
{
  "workspace": [
    "./apps/web",
    "./apps/mobile",
    "./apps/admin",
    "./apps/api",
    "./packages/shared"
  ]
}
```

**Standard project structure:**

```
my-monorepo/
├── deno.json             # workspace members
├── apps/
│   ├── web/deno.json     # Customer-facing web (Fresh)
│   ├── mobile/           # Customer-facing mobile (Capacitor wraps Fresh)
│   ├── admin/deno.json   # Internal admin dashboard (Fresh)
│   └── api/deno.json     # Backend API (Hono)
└── packages/
    └── shared/deno.json  # shared modules
```

- Shared `deno.json` config (compilerOptions, imports)
- Each member can override root settings
- Import maps shared across workspace
- Single `deno.lock` at root

---

## When to Use Deno

- Sandboxed execution required (explicit permissions model)
- Direct TypeScript execution without transpilation
- Security-critical applications
- Edge-first deployment (Deno Deploy)

---

## Frontend: Fresh

```bash
# scaffold project
deno run -A -r https://fresh.deno.dev my-app
cd my-app

# development
deno task start
```

---

## Backend: Hono

```ts
// main.ts
import { Hono } from "https://deno.land/x/hono/mod.ts";

const app = new Hono();
app.get("/", (c) => c.text("Hello Deno!"));

Deno.serve(app.fetch);
```

```bash
deno run --allow-net main.ts
```

- **API docs:** Use `@hono/swagger-ui` for OpenAPI documentation

---

## Database

**Deno KV (simple, built-in):**

```ts
const kv = await Deno.openKv();
await kv.set(["users", id], user);
```

**Neon + Drizzle (Postgres):**

```bash
deno add npm:drizzle-orm npm:@neondatabase/serverless
```

---

## Testing

```bash
# unit tests (native)
deno test

# with permissions
deno test --allow-net --allow-read

# e2e
deno run -A npm:playwright test
```

---

## Deployment

**Deno Deploy (edge-first):**

```bash
deployctl deploy --project=my-project main.ts
```

**Cloud Run (containerized):**

```dockerfile
FROM denoland/deno:latest
WORKDIR /app
COPY . .
RUN deno cache main.ts
CMD ["run", "--allow-net", "main.ts"]
```

---

## Mobile: Capacitor

Capacitor wraps your Fresh web app as a native mobile app. Unlike Expo, Capacitor works within a Deno monorepo because it bundles your existing web output.

| Layer | Tool | Notes |
|-------|------|-------|
| **Framework** | Capacitor | Wraps Fresh web app as native |
| **Web App** | Fresh | Your Deno SSR app, built to static |
| **State** | Preact Signals | Fresh-native reactivity |
| **Storage** | @capacitor/preferences | Key-value storage |
| **Testing** | `deno test` + Playwright | Web testing applies |
| **Build** | Capacitor CLI | `npx cap build` |
| **Deploy** | Manual or Appflow | Xcode/Android Studio for stores |

```bash
# in your Fresh app directory
deno task build                             # build Fresh to static

# add Capacitor (one-time setup)
npm init -y && npm install @capacitor/core @capacitor/cli
npx cap init my-app com.example.myapp
npx cap add ios && npx cap add android

# sync web build to native
npx cap sync

# open in native IDE
npx cap open ios      # opens Xcode
npx cap open android  # opens Android Studio
```

> **More details:** See [guides/mobile.md](../guides/mobile.md)

---

## Command Cheatsheet

```bash
# project setup
deno init my-project
deno add npm:<package>

# development
deno task dev
deno run --allow-net main.ts

# testing
deno test
deno test --watch

# linting & formatting
deno lint
deno fmt
deno check main.ts

# mobile (Capacitor)
deno task build                  # build Fresh to static
npx cap sync                     # sync to native
npx cap open ios                 # open Xcode
npx cap open android             # open Android Studio

# deployment
deployctl deploy --project=my-project main.ts
```
