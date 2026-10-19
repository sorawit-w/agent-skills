# Deno — Migration Only

**Do not use this file to start a new project.** Cloudflare acquired Deno on 2026-10-09, and Deno is winding down as a separate runtime and hosting service. This page helps a project that is already on Deno move off it.

> **Related:** [Hosting](../guides/hosting.md) | [Bun stack](bun.md) | [Mobile](../guides/mobile.md)

---

## Timeline (as announced 2026-10-09)

| Piece | What happens | Approximate date |
|-------|--------------|------------------|
| **Deno Deploy** (hosting) | Shuts down; paying customers get migration help to Cloudflare Workers | ~2027-04 (six months after the announcement) |
| **Deno runtime** | Monthly bug-fix and security releases for about one year, then active development ends; stays open source (MIT) | ~2027-10 |
| **Deno KV on Deno Deploy** | Goes away with Deno Deploy | ~2027-04 |
| **JSR** (package registry) | Keeps running; infrastructure moves to Cloudflare | No end date announced |
| **Fresh** | No clear statement found — check the Fresh repo before relying on it | Unknown |

The dates are estimates from the announcement window, not fixed shutdown days. Check the [Deno announcement](https://deno.com/blog/cloudflare) for anything newer before you commit to a plan.

**Order of moves:** move hosting first (Deno Deploy closes first), then the runtime.

---

## Pick a Destination

| If the project is… | Move to | Then load |
|--------------------|---------|-----------|
| Edge-first, on Deno Deploy | **Cloudflare Workers + Hono** | [bun.md](bun.md) for tooling, [hosting.md](../guides/hosting.md) § Cloudflare Workers |
| A regular web app or API | **Bun** (the skill's default) | [bun.md](bun.md) |
| Tied to Node-only packages or a Node team | **Node (Active LTS)** | [node.md](node.md) |

If the project chose Deno for its permission sandbox, no destination here replaces it. Node's `--permission` model guards trusted code against mistakes, but Node's own docs say it is not a sandbox for untrusted code. Say so to the user instead of claiming an equal swap.

---

## Layer-by-Layer Map

| Deno layer | Destination | Notes |
|------------|-------------|-------|
| **Runtime** (`deno`) | Workers (edge) / Bun / Node | Replace `Deno.*` APIs with web-standard or `node:` equivalents |
| **Hosting** (Deno Deploy) | Cloudflare Workers / Cloud Run | Workers is the supported migration path for paying Deploy customers |
| **Frontend** (Fresh) | SvelteKit | `@sveltejs/adapter-cloudflare` on Workers, `svelte-adapter-bun` on Bun |
| **Backend** (Hono) | Hono | Runs on Workers, Bun, and Node; only the entrypoint changes (below) |
| **Backend** (Oak) | Hono | Oak is Deno-first; Hono is the closest portable replacement |
| **Database** (Deno KV) | Workers KV or D1 (on Workers) / Neon + Drizzle (anywhere) | Export the data before Deno Deploy closes |
| **Database** (Neon + Drizzle) | Neon + Drizzle | No change; install with `bun add` instead of `deno add` |
| **Testing** (`deno test`) | `bun test` / Vitest | Use Vitest with the Workers pool for Workers-specific code |
| **Workspaces** (`deno.json`) | Bun workspaces (`package.json`) | Same `apps/` + `packages/` layout |
| **Mobile** (Capacitor) | Capacitor | Keep it; point it at the new web build |

---

## Hono: Change the Entrypoint

Most Hono code moves as-is. Imports and the server start change:

```ts
// before (Deno)
import { Hono } from "https://deno.land/x/hono/mod.ts";
const app = new Hono();
Deno.serve(app.fetch);

// after (Cloudflare Workers or Bun)
import { Hono } from "hono";
const app = new Hono();
export default app;
```

---

## If You Must Stay on Deno for Now

- Pin the Deno version and apply each security release while they last (~2027-10).
- Move off Deno Deploy before it closes (~2027-04), even if the runtime stays for a while.
- Put the runtime move on the roadmap now; do not let the end of security releases arrive unplanned.
