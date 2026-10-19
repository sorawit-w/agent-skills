# Backend Hosting Reference

Load this when deciding where to deploy your backend services.

---

## Platform Comparison

| Platform | Best For | Strengths | Trade-offs |
|----------|----------|-----------|------------|
| **GCP Cloud Run** | Core production APIs | Auto-scaling, revisions, GCP ecosystem | Cold starts |
| **Railway** | Fast iteration, MVPs | One-click deploy + Postgres + Redis | Not GCP-native |
| **Vercel** | Frontend + thin APIs | Instant deploys, serverless | Short timeouts |
| **Cloudflare Workers** | Edge-first apps and APIs | Global edge, Hono-native, D1/KV bindings | Per-request CPU and memory limits; bindings tie you to Cloudflare |
| **GKE** | Large multi-service | Full Kubernetes control | High ops overhead |

> **Deno Deploy is closing** (~2027-04, after Cloudflare acquired Deno). Do not deploy new apps there; see [stacks/deno.md](../stacks/deno.md) to move existing ones.

---

## Rules of Thumb

1. **Default to Cloud Run** for GCP-aligned production APIs
2. **Use Railway** for prototypes, MVPs, instant DB + cache
3. **Keep Vercel** for Next.js frontends with minimal APIs
4. **Use Cloudflare Workers** for edge-first apps (Hono API, SvelteKit frontend)

---

## Cloudflare Workers (Edge-First)

The edge-first stack: Bun as local tooling, Hono for the API, SvelteKit for the web app, Workers for hosting.

| Layer | Tool | Notes |
|-------|------|-------|
| **API** | Hono | `export default app` is the Worker entrypoint |
| **Frontend** | SvelteKit | `@sveltejs/adapter-cloudflare` |
| **Database** | Neon + Drizzle, or D1 + Drizzle | Neon for Postgres; D1 is Cloudflare's SQLite. Hyperdrive pools Postgres connections |
| **Key-value** | Workers KV | Simple global reads |
| **Auth** | Clerk | Same as other stacks |
| **Testing** | Vitest + Workers pool | Runs tests inside the Workers runtime |

```bash
bun create hono@latest my-api           # choose the cloudflare-workers template
bunx wrangler dev                       # local dev
bunx wrangler types --env-interface CloudflareBindings   # typed bindings for Hono
bunx wrangler deploy                    # deploy
```

> **Node APIs:** projects with a `compatibility_date` of 2026-08-04 or later get Node.js compatibility by default. For earlier dates, add `"compatibility_flags": ["nodejs_compat"]` to the Wrangler config. Database drivers need it.

---

## Deployment Commands

**Railway:**
```bash
railway up
```

**Cloud Run:**
```bash
docker build -t gcr.io/$GCP_PROJECT/api:$(git rev-parse --short HEAD) .
gcloud run deploy api --image gcr.io/$GCP_PROJECT/api:$(git rev-parse --short HEAD) --region=$GCP_REGION
```

**Vercel:**
```bash
vercel --prod
```

**Cloudflare Workers:**
```bash
bunx wrangler deploy
```

**Netlify (Static/SSG):**
```bash
netlify build && netlify deploy --prod
```
