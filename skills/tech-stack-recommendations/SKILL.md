---
name: tech-stack-recommendations
description: "Opinionated technology stack guidance for new projects and migrations. Use when starting a new project, picking a runtime (Bun/Deno/Node), choosing frontend frameworks, databases, auth, hosting, styling, mobile, i18n, or AI agents, setting up a monorepo, or migrating between stacks. Not for debugging or maintaining existing code with an established stack."
---

# Tech Stack Recommendations

Complete guide for choosing opinionated technology stacks for new projects and migrations. **Read this first to pick your runtime, then load the appropriate reference guides below.**

---

## When to Use This Skill

- **New projects:** Starting from scratch and need stack guidance
- **Stack migrations:** Moving from Node → Bun, rewriting in Deno, etc.
- **Framework selection:** Choosing between SvelteKit, Next.js, Angular, Nuxt, etc.
- **Architecture decisions:** Building monorepos, multi-platform apps, or complex systems
- **Infrastructure choices:** Selecting databases, auth, hosting, styling, mobile frameworks

**NOT for:** Existing projects with established stacks (unless actively migrating).

---

## This Skill Has a Shelf Life

Framework ecosystems drift fast. The specific names in this skill (Bun, SvelteKit, Elysia, Neon, Drizzle, Clerk, etc.) reflect 2026-era tooling and *will* age. Before recommending any named tool:

- If the user's request is recent and the skill hasn't been updated in a while, flag the age — e.g., "this was written against 2026 tooling; double-check pricing/status for [vendor] before committing."
- For syntax or API details, defer to the project's current docs, not a snippet pasted from here.
- If a named framework is clearly deprecated or superseded, say so instead of recommending it.

The *shape* of the advice (pick one runtime, name the override factors, prefer what the team can debug) ages more slowly than the specific names. Prefer the shape over the names when the two disagree.

---

## This Skill Is Opinionated. Override When the Context Says So.

The defaults here (Bun + SvelteKit + Elysia + Neon + Drizzle + Clerk) are one person's taste, not universal truth. Before applying them, surface the context that should shift the recommendation, and say so out loud rather than silently enforcing the default.

**Override the default runtime or framework when any of these apply:**

| Factor | Example override |
|---|---|
| **Team expertise** | Team has deep Angular/NestJS background → use Node + Next.js/Angular + Nx, not Bun. |
| **Hiring pool** | Hiring at scale in a market where Node is dominant → Node > Bun, even for greenfield. |
| **Compliance / data residency** | SOC 2, HIPAA, GDPR with strict self-hosting or region pinning → prefer self-hostable auth (Ory, Supabase Auth, Lucia) over Clerk; prefer regionally-pinned DB over serverless Neon by default. |
| **Vendor / third-party policy** | Org forbids third-party auth providers → custom JWT (e.g. `@elysiajs/jwt`) or self-hosted Kratos. |
| **Ecosystem maturity** | A required SDK is Node-only → use Node; don't contort Bun. |
| **Runtime constraints** | Target is edge / deno-only platforms, or strictly AWS Lambda Node runtime → choose accordingly, not Bun by default. |
| **Existing infra** | Monorepo already on pnpm + Nx, or org-wide CI assumes Node → extending that is usually cheaper than forking the toolchain. |
| **Cost profile at scale** | Clerk's per-MAU pricing breaks at your scale → self-host. Neon autoscaling costs > a single RDS → switch. |
| **Realtime / collaborative features** | Supabase (realtime channels) > Neon. Worth breaking the default DB choice. |
| **Latency-sensitive global apps** | Deno Deploy / edge-first frameworks (Fresh, Hono on edge) > Bun+SvelteKit on a single region. |

**Rules of thumb when applying this skill:**

1. **State the override factors that apply** before recommending a stack. Don't just output the default and hope no one notices.
2. **Name the trade-off.** "Bun is faster, but your team is Node-fluent — picking Bun costs you ~2 weeks of ramp."
3. **Prefer the stack the team can debug over the one with the best benchmark.** Developer fluency beats synthetic performance in almost every real project.
4. **Compliance and policy are vetoes, not tiebreakers.** If self-hosting is mandatory, Clerk is out — don't argue.
5. **If you can't tell which factors apply, ask one crisp question** (team makeup, compliance, deployment target, scale) rather than assuming the default is safe.

The default exists so small-team greenfield projects don't burn a week on stack selection. It is not a recommendation for every project that could technically run on it.

---

## Platform Inference: What Should You Build?

If business requirements don't specify platforms, infer from the application's nature:

| Signal | Suggests | Example |
|--------|----------|---------|
| On-the-go usage, notifications, offline | **Mobile** (Expo) | Ride-sharing, delivery, fitness tracking |
| Data-heavy dashboards, complex workflows | **Web** (SvelteKit / Next.js) | Analytics, CRM, project management |
| Consumer-facing product with users everywhere | **Web + Mobile** | Social media, messaging, banking |
| Internal tool for staff only | **Web only** | Admin dashboards, internal workflows |

**Rule:** When in doubt, build web first. Mobile can be added later via Expo (Bun/Node) or Capacitor (Deno).

---

## Runtime Selection: Bun vs. Deno vs. Node

**Default: Bun** for all new TypeScript/JavaScript projects.

| Runtime | Use When | Strengths | Trade-offs |
|---------|----------|-----------|------------|
| **Bun** (default) | Fast builds, modern stacks | Lightning-fast, native TS, built-in test runner, smallest footprint | Limited ecosystem maturity; some packages missing |
| **Deno** | Sandbox security, edge-first, no node_modules | Secure by default, direct TS imports, explicit permissions | Some npm package incompatibility; smaller ecosystem |
| **Node 22 LTS** | Legacy compatibility, team expertise | Mature ecosystem, stable, battle-tested tooling | Slower than Bun, heavier |

**Decision tree:**
1. **Is this a new greenfield project?** → Use **Bun** (default)
2. **Do you need sandboxed security or edge deployment?** → Use **Deno**
3. **Do you have legacy dependencies or Angular/NestJS expertise?** → Use **Node 22 LTS**

> **Pin your runtime version** in `.tool-versions` or `package.json` → `engines` field.

---

## Quick Stack Selection Matrix

Choose based on your primary use case and platform target:

| Use Case | Recommended Stack | Load Guide |
|----------|------------------|-----------|
| **New web + API** (default) | Bun + SvelteKit + Elysia + Neon + Drizzle | [stacks/bun.md](references/stacks/bun.md) |
| **Sandbox security or edge-first** | Deno + Fresh + Hono + Deno KV | [stacks/deno.md](references/stacks/deno.md) |
| **Large ecosystem or Angular/NestJS** | Node + Next.js + NestJS + Nx + Neon + Drizzle | [stacks/node.md](references/stacks/node.md) |
| **Need to choose a frontend framework** | Load guides below | [guides/frontend-frameworks.md](references/guides/frontend-frameworks.md) |
| **Choosing deployment platform** | Load guides below | [guides/hosting.md](references/guides/hosting.md) |
| **Setting up database + auth** | Load guides below | [guides/database-auth.md](references/guides/database-auth.md) |
| **Adding mobile support** | Load guides below | [guides/mobile.md](references/guides/mobile.md) |

---

## Step 1: Choose Your Runtime

Load **exactly one** of these based on your signals:

| File | When to Load | Stack Includes |
|------|--------------|---|
| **[references/stacks/bun.md](references/stacks/bun.md)** | **Most new projects (default)** | Bun + SvelteKit + Elysia + Eden RPC + Neon + Drizzle + Clerk + Tailwind |
| **[references/stacks/deno.md](references/stacks/deno.md)** | Sandbox security, edge, no node_modules | Deno + Fresh + Hono + Deno KV + Clerk + Tailwind |
| **[references/stacks/node.md](references/stacks/node.md)** | Legacy compat, Angular, team expertise | Node 22 LTS + Next.js/Angular + NestJS + Nx + Neon + Drizzle + Clerk + Tailwind |

Each file includes:
- Complete layer-by-layer stack overview
- Monorepo setup (Bun Workspaces, Deno Workspaces, or Nx)
- Standard project structure (apps/, packages/)
- Quick-start commands

---

## Step 2: Load Topic Guides On-Demand

After selecting a runtime, load **any of these guides** that apply to your project:

| Guide | Load When | File |
|-------|-----------|------|
| **Frontend Frameworks** | Choosing between SvelteKit, Next.js, Astro, Remix, Angular, etc. | [references/guides/frontend-frameworks.md](references/guides/frontend-frameworks.md) |
| **Backend Hosting** | Selecting deployment platform (Cloud Run, Railway, Vercel, Deno Deploy, etc.) | [references/guides/hosting.md](references/guides/hosting.md) |
| **Database & Auth** | Setting up Postgres + Clerk (or Supabase, Turso alternatives) | [references/guides/database-auth.md](references/guides/database-auth.md) |
| **Styling & UI** | Setting up Tailwind + component systems (shadcn/ui, shadcn-svelte, etc.) | [references/guides/styling.md](references/guides/styling.md) |
| **Mobile Support** | Adding Expo, Capacitor, Flutter, or Dioxus to your monorepo | [references/guides/mobile.md](references/guides/mobile.md) |
| **Internationalization** | Setting up i18n (translations, locales, RTL support) | [references/guides/i18n.md](references/guides/i18n.md) |
| **Font Awesome** | Using Font Awesome v7 icons in your stack | [references/guides/font-awesome.md](references/guides/font-awesome.md) |
| **AI Coding Assistant Config** | Setting up Claude Code / skills / MCP for your repo (context files, `.ai/` folder, tool definitions) | [references/guides/ai-agents.md](references/guides/ai-agents.md) |
| **Building AI Agent Products** | *Out of scope for this skill.* This skill covers the web / backend / DB layer for an agent app, but NOT the agent framework itself. Use Claude Agent SDK, MCP, LangChain, or LlamaIndex per project needs. | — |

---

## Monorepo Patterns: Pick One

All three runtimes support monorepos with the same logical structure. **Pick based on your runtime:**

### Bun Monorepos: Native Workspaces

```json
{
  "name": "my-monorepo",
  "workspaces": ["apps/*", "packages/*"]
}
```

**Command:** `bun install` (installs all workspaces)

### Deno Monorepos: Native Workspaces

```json
{
  "workspace": [
    "./apps/web",
    "./apps/api",
    "./packages/shared"
  ]
}
```

**Command:** `deno run --allow-all deno.json` (runs workspace)

### Node Monorepos: Nx + pnpm Workspaces

```bash
npx create-nx-workspace@latest my-monorepo --preset=apps
```

**Command:** `pnpm install && nx serve web` (runs specific app)

---

## Standard App Structure

All monorepos follow this logical layout:

```
my-monorepo/
├── apps/
│   ├── web/              # Customer-facing web (SvelteKit / Next.js)
│   ├── mobile/           # Mobile app (Expo / Capacitor)
│   ├── admin/            # Internal admin dashboard
│   └── api/              # Backend API (Elysia / Hono / NestJS)
└── packages/             # Bun/Deno workspaces use this name
    └── shared/           # Shared types, utils, components
```

> **Workspace directory naming:** Bun and Deno workspaces use `packages/` (shown above). **Nx (Node) uses `libs/` instead** — this is Nx's own default, and `references/stacks/node.md` follows it. Do not mix the two within one monorepo; pick the convention that matches your runtime's tooling.

**When to include each app:**

| App | Include When |
|-----|--------------|
| `api` | **Always** — backend is required |
| `admin` | **Almost always** — manage users, data, content |
| `web` | Most customer-facing projects |
| `mobile` | When users need on-the-go access (infer from signals above) |

> **Rule:** When in doubt, include `admin` — it's easier to remove later than add.

---

## Decision Flow: Pick a Stack in 3 Steps

**Step 1: Does your project need security/edge features?**
- Yes → Use **Deno** [→ load stacks/deno.md](references/stacks/deno.md)
- No → Go to Step 2

**Step 2: Do you need large Node ecosystem or Angular/NestJS?**
- Yes → Use **Node 22 LTS** [→ load stacks/node.md](references/stacks/node.md)
- No → Go to Step 3

**Step 3: Proceed with default**
- Use **Bun** [→ load stacks/bun.md](references/stacks/bun.md)

---

## After You Pick Your Stack

1. **Read your runtime stack file** (Bun, Deno, or Node)
2. **Load topic guides on-demand** as you make specific choices
3. **Initialize your monorepo** using the command from your stack file
4. **Build your first app** (usually `api` or `web`)
5. **Deploy** using the hosting guide

---

## Platform-Specific Rules

### For Web Apps
- **Default frontend:** SvelteKit (Bun) / Next.js (Node)
- **Default styling:** Tailwind + Plain CSS
- Load [guides/frontend-frameworks.md](references/guides/frontend-frameworks.md) if you want alternatives

### For Backend APIs
- **Default (Bun):** Elysia + Eden RPC (end-to-end types)
- **Default (Deno):** Hono or Oak
- **Default (Node):** NestJS with modules and DI
- All use Neon + Drizzle by default

### For Databases
- **Default:** Neon (serverless Postgres) + Drizzle ORM
- Alternative: Supabase, Turso, Prisma
- Load [guides/database-auth.md](references/guides/database-auth.md) for detailed comparisons

### For Authentication
- **Default:** Clerk (best auth DX, 10k MAU free)
- **Override when:** self-hosting is mandatory, strict data-residency rules apply, or policy bars third-party vendors. Alternatives: Supabase Auth (self-hostable), Ory Kratos, Lucia, Auth.js, or custom JWT (e.g. `@elysiajs/jwt`).
- Load [guides/database-auth.md](references/guides/database-auth.md) for setup

### For Deployment
- **Web frontends:** Vercel (Next.js) or Cloud Run (SvelteKit)
- **APIs:** Cloud Run (default) or Railway (MVP)
- **Deno apps:** Deno Deploy or Cloud Run
- Load [guides/hosting.md](references/guides/hosting.md) for deployment commands

### For Mobile
- **Bun/Node:** Use Expo for native feel
- **Deno:** Use Capacitor (wraps your web app)
- Load [guides/mobile.md](references/guides/mobile.md) for integration steps

---

## Signals → Stack Recommendation Table

Use this table if you're given conflicting requirements:

| Signal | Recommendation | Rationale |
|--------|----------------|-----------|
| "We're a startup building fast" | Bun + SvelteKit + Railway | Fastest iteration, smallest bundles |
| "We have legacy Angular code" | Node + Angular + Nx + NestJS | Leverage existing team expertise |
| "We need global edge deployment" | Deno + Fresh + Deno Deploy | Built for edge, instant deploys |
| "We're migrating from Node to TypeScript" | Bun + SvelteKit + Elysia | 10x faster builds, native TS |
| "We need OAuth + complex auth flows" | Clerk + [any stack] | Pre-built, battle-tested components |
| "We're building an admin dashboard" | [Any stack] + Tailwind + shadcn | Fast, accessible component library |
| "We need real-time or collaborative features" | Supabase (realtime) instead of Neon | Built-in realtime subscriptions |

---

## Summary

1. **New TypeScript/JavaScript projects:** Start with **Bun** (unless you have specific signals)
2. **Monorepos:** Use native workspaces (Bun/Deno) or Nx (Node)
3. **Defaults rule:** Use Bun + SvelteKit + Elysia + Neon + Drizzle + Clerk unless you have a reason not to
4. **Scope rule:** Recommend only what the user asked for. If the ask is narrow — a CLI, a script, an AI agent, a library, a microservice — do NOT auto-scaffold the full-stack default. Name only the pieces needed; mention additional layers (persistence, auth, UI) as optional "when you need X."
5. **Load topic guides as needed:** Backend hosting, frontend frameworks, mobile, etc.
6. **Build fast:** This stack prioritizes developer experience and iteration speed

---

## Reference Map

```
tech-stack-recommendations/
├── SKILL.md (you are here)
├── references/
│   ├── stacks/
│   │   ├── bun.md          # Bun + SvelteKit + Elysia + Neon + Drizzle
│   │   ├── deno.md         # Deno + Fresh + Hono + Deno KV
│   │   └── node.md         # Node + Next.js/Angular + NestJS + Nx
│   └── guides/
│       ├── frontend-frameworks.md    # SvelteKit vs Next.js vs Remix vs Angular
│       ├── hosting.md                # Cloud Run vs Railway vs Vercel vs Deno Deploy
│       ├── database-auth.md          # Neon + Clerk vs Supabase vs Turso
│       ├── styling.md                # Tailwind + Plain CSS + component systems
│       ├── mobile.md                 # Expo vs Capacitor vs Flutter
│       ├── i18n.md                   # Internationalization setup
│       ├── font-awesome.md           # Font Awesome v7 reference
│       └── ai-agents.md              # AI coding assistant config (skills, MCP, context files)
```

---

## Need Help?

- **New project:** Load your runtime stack file first (Bun / Deno / Node)
- **Migrating:** Decide on new runtime, then load stack file
- **Specific choice (frontend, DB, auth, mobile):** Load the matching topic guide
- **Unsure?** Default to Bun + SvelteKit + Elysia + Neon + Drizzle + Clerk

---

## Cross-Skill Integration

| Skill | When to Use |
|-------|-------------|
| `mcp-builder` (Anthropic) | When the stack decision includes building an MCP server — whether to expose tools from the chosen backend, or to author a custom connector. This skill picks the runtime/framework; `mcp-builder` owns MCP authoring conventions (FastMCP for Python, MCP SDK for Node/TS) and tool-design best practices. |
| `web-artifacts-builder` (Anthropic) | When the recommendation is "prototype first, commit later" — e.g., a claude.ai artifact with React + shadcn/ui before scaffolding a full Next.js repo. This skill advises the long-term stack; `web-artifacts-builder` ships a same-day prototype against which the stack decision can be tested. |
| `doc-coauthoring` (Anthropic) | When the founder/team wants the recommendation written up as an ADR (architecture decision record) or decision doc rather than a raw chat summary. Hand off after the choice is made; don't attempt long-form co-authoring inline. |
| `team-composer` (our own) | When the stack decision is entangled with product, org, or operational constraints and a single-role recommendation isn't enough — e.g., `@senior_software_architect` + `@platform_engineer` + `@security_engineer` should weigh in together. Prefer `team-composer` when the question is "what stack fits this org" vs. "what's the best stack for this workload". |
| `engineering:architecture` (official) | When the downstream need is a formal ADR with trade-offs and consequences. This skill's recommendation is upstream — a sharp-ended opinion — and feeds into that ADR. |

**Graceful degradation:** if `mcp-builder`, `web-artifacts-builder`, or `doc-coauthoring` aren't installed, the stack recommendations in this skill still stand. The referenced skills are handoff destinations, not hard dependencies.
