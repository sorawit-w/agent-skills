# Backend Hosting Reference

Load this when deciding where to deploy your backend services.

---

## Platform Comparison

| Platform | Best For | Strengths | Trade-offs |
|----------|----------|-----------|------------|
| **GCP Cloud Run** | Core production APIs | Auto-scaling, revisions, GCP ecosystem | Cold starts |
| **Railway** | Fast iteration, MVPs | One-click deploy + Postgres + Redis | Not GCP-native |
| **Vercel** | Frontend + thin APIs | Instant deploys, serverless | Short timeouts |
| **Deno Deploy** | Edge-first Deno apps | Global edge, instant deploys | Deno-only |
| **GKE** | Large multi-service | Full Kubernetes control | High ops overhead |
| **Cloudflare Workers** | Edge routing, mini-APIs | Low latency | Limited Node APIs |

---

## Rules of Thumb

1. **Default to Cloud Run** for GCP-aligned production APIs
2. **Use Railway** for prototypes, MVPs, instant DB + cache
3. **Keep Vercel** for Next.js frontends with minimal APIs
4. **Use Deno Deploy** for Deno edge-first apps
5. **Use Cloudflare Workers** as edge layer only

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

**Deno Deploy:**
```bash
deployctl deploy --project=my-project main.ts
```

**Netlify (Static/SSG):**
```bash
netlify build && netlify deploy --prod
```
