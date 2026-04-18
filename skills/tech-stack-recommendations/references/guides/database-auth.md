# Database & Auth Reference

Load this when setting up database or authentication.

---

## Default Stack

**Neon + Clerk + Drizzle**

| Tool | Why |
|------|-----|
| **Neon** | Scale-to-zero (no cost idle), DB branching, sub-10ms queries |
| **Clerk** | Best auth DX, pre-built components, 10k MAU free |
| **Drizzle** | SQL-like syntax, tiny runtime (~50KB), works with all runtimes |

---

## Alternatives

| Alternative | When to Use | Trade-off |
|-------------|-------------|-----------|
| **Supabase** | Need realtime, storage, all-in-one | No scale-to-zero ($25/mo per project) |
| **Turso + Clerk** | Global users, edge-first | SQLite (no advanced Postgres) |
| **Prisma** | Team familiarity, better migration CLI | Heavier runtime |

---

## Setup Commands

### Drizzle + Neon (Preferred)

**Bun:**
```bash
bun add drizzle-orm @neondatabase/serverless
bun add -D drizzle-kit
```

**Node:**
```bash
pnpm add drizzle-orm @neondatabase/serverless
pnpm add -D drizzle-kit
```

**Deno:**
```bash
deno add npm:drizzle-orm npm:@neondatabase/serverless
```

### Prisma (Alternative)

```bash
pnpm add prisma @prisma/client
pnpm prisma generate
pnpm prisma migrate dev --name init
```

### Clerk

**Bun:**
```bash
bun add @clerk/backend
```

**Node (Next.js):**
```bash
pnpm add @clerk/nextjs
```

---

## Environment Variables

Add to `.env`:

```bash
# Database
DATABASE_URL=postgres://...@...neon.tech/...

# Clerk
CLERK_SECRET_KEY=sk_...
NEXT_PUBLIC_CLERK_PUBLISHABLE_KEY=pk_...  # for frontend
```

> **Note:** Never commit `.env` files. Include `.env.example` with placeholder values.
