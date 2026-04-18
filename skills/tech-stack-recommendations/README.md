<p align="center">
  <img src="https://raw.githubusercontent.com/sorawit-w/agent-skills/main/assets/tech-stack-recommendations-li.svg" alt="tech-stack-recommendations — opinionated defaults, judgment-aware" width="100%"/>
</p>

# tech-stack-recommendations

A Claude Code skill that gives you an opinionated default tech stack for a new TypeScript/JavaScript project — runtime, frontend, API, database, auth, hosting, mobile, i18n — and loads topic guides on demand as the project gets real.

## Why this exists

Stack selection is where a lot of small projects die. Every vote has five reasonable answers, each answer pulls three more decisions after it, and the day ends with a blank repo, an empty `package.json`, and a Slack thread.

This skill picks a lane. It names a default, says what it's optimized for, and points at the alternatives. It's not trying to be neutral — neutrality is exactly what makes stack-selection docs unusable. What it's trying to do is collapse "what should we use?" into "here's the default, here's when you should override it, and here's the smaller guide to read next."

## What it does

- **Names a single default stack:** Bun + SvelteKit + Elysia + Neon + Drizzle + Clerk, with Tailwind + shadcn on top.
- **Offers two alternates with clear triggers:** Deno (edge-first, sandboxed) and Node 22 LTS (ecosystem-heavy, legacy-compatible, Angular/NestJS-friendly).
- **Infers platform target** from application nature — mobile vs. web vs. both vs. internal tool — instead of demanding the user specify.
- **Covers the full vertical** — runtime, monorepo layout, frontend framework, backend framework, hosting, database, auth, styling, mobile, i18n, icon system, AI coding assistant config.
- **Loads reference guides on demand**, so the model doesn't inhale the whole stack guide for a question about hosting.
- **Keeps scope honest:** if you ask for a CLI or a single script, it doesn't auto-scaffold the full-stack default. It names only the layers you asked for.
- **Flags the override factors** that should make you break the default — team expertise, compliance, vendor policy, existing infra, cost at scale, realtime needs — before recommending.

## Shelf life: this will age. Check before you trust.

Framework ecosystems move fast. The defaults in this skill were written against a specific moment in time (see the version below) and the landscape *will* drift — new runtimes ship, frameworks fall out of favor, auth vendors reprice, edge platforms consolidate. Treat the recommendation as a strong starting point, not a frozen truth.

Before you ship a decision based on this skill:

- **Check the version date** at the bottom (v0.1 reflects 2026-era tooling).
- **Sanity-check the headline picks** — is Bun still the faster runtime for your workload? Is Clerk's pricing still reasonable at your scale? Has a named framework been deprecated?
- **Prefer the project's current docs** over anything the skill quotes as a syntax snippet.
- **File an issue** (or fork) if a default has clearly aged out. This skill is versioned and will move forward, but only as fast as someone bumps it.

If you're reading this more than ~12 months after the last version bump and nothing's changed, assume some of the specific framework names have drifted even if the shape of the advice hasn't.

## It's opinionated. That's the point — and the limit.

The defaults here are one person's taste, not universal truth. The skill surfaces the factors that should shift the recommendation and asks you to state them:

- **Team expertise** — Angular/NestJS team? Use Node, not Bun.
- **Compliance / data residency** — SOC 2, HIPAA, GDPR self-hosting? Clerk is out; prefer Ory/Supabase Auth/Lucia.
- **Ecosystem maturity** — A required SDK is Node-only? Don't contort Bun.
- **Runtime constraints** — Edge-only, or strict AWS Lambda Node? Pick for the target, not for the vibe.
- **Hiring pool** — Hiring at scale where Node dominates? Pick Node.
- **Existing infra** — Monorepo already on pnpm + Nx? Extending that usually beats forking the toolchain.
- **Cost profile at scale** — Clerk per-MAU breaking at your scale? Self-host.
- **Realtime / collaborative features** — Supabase realtime > Neon.
- **Latency-sensitive global apps** — Deno Deploy / Hono on edge > Bun + SvelteKit on one region.

If you want a neutral "here are all the options, you decide" reference, this isn't it. If you want a sparring partner that picks a default, names the trade-off, and gets out of the way, it is.

Full override table and rules of thumb live in [`SKILL.md`](skills/tech-stack-recommendations/SKILL.md) under *This Skill Is Opinionated. Override When the Context Says So.*

## When to use it

- You're starting a new TypeScript/JavaScript project and don't want to spend a week litigating Bun vs. Node.
- You're migrating an existing stack (Node → Bun, Webpack → Vite, REST → Elysia + Eden) and want a curated destination rather than a grid.
- You need to pick one layer — auth, DB, hosting, mobile, i18n, icon system — and want an opinionated answer with the alternatives named.
- You're setting up a monorepo and want a structure that works for one `web` app today and `mobile` / `admin` / `api` later.

## When not to use it

- **Existing, established stack.** If the team already has a shipped Node + Express + Postgres + Auth0 app, re-picking the stack is usually the wrong move. Reach for [`engineering:tech-debt`](../../) or similar instead.
- **Compliance-driven choice without discussion.** If legal or security has already mandated a stack (say, Azure + .NET + AAD), you don't need a recommendation — you need to execute.
- **Tiny CLIs or one-off scripts.** The skill scales down (it'll name the runtime and stop), but you probably don't need a guide for `npx tsx script.ts`.
- **Non-TypeScript/JavaScript stacks.** Rust, Go, Python, Elixir — out of scope here.
- **Agent framework selection itself.** The skill covers the web / API / DB layer *around* an agent app, not the agent framework (Claude Agent SDK, LangChain, MCP). Pick that separately.

## How it works

1. **Platform inference.** If the brief doesn't say web vs. mobile vs. both, the skill infers from signals — on-the-go usage → mobile, data-heavy dashboards → web, consumer product → web + mobile, internal tool → web only.
2. **Runtime decision tree.** Three branches: Deno (edge / sandboxed), Node (legacy / ecosystem / Angular), or Bun (default). The tree is three questions deep and ends at exactly one answer.
3. **Load the matching stack file.** One of `references/stacks/{bun,deno,node}.md`, each with the full layer-by-layer stack, monorepo setup (Bun workspaces / Deno workspaces / Nx), standard directory structure, and quick-start commands.
4. **Load topic guides on demand.** Frontend frameworks, hosting, DB + auth, styling, mobile, i18n, Font Awesome, AI coding assistant config — each as a separate reference file so the model loads only what the task needs.
5. **Apply the override rules.** Before recommending, name the factors (team, compliance, vendor, existing infra, cost, realtime) that should break the default. Don't just output Bun and hope.
6. **Scope honestly.** If the user asked for a CLI, name the runtime and stop. Full-stack defaults only apply when the request is for a full-stack project.

## What the output looks like

Depends on the request. For a full-stack greenfield ask, you'll get the default stack named end-to-end (Bun + SvelteKit + Elysia + Neon + Drizzle + Clerk + Tailwind), a one-line rationale for each layer, a monorepo layout, and pointers to the topic guides for anything the user wants to override. For a narrower ask ("pick a frontend framework for a marketing site"), you'll get one layer recommended, the main alternatives named, and the override signals that would flip the answer.

Every recommendation should be accompanied by the override factors that apply — not buried at the bottom, named up front.

## Design choices worth knowing

- **One default, two alternates.** Not "here are eight runtimes, here are twenty frameworks." Opinionated collapses decision fatigue; comprehensive reintroduces it.
- **References are separate files.** `SKILL.md` picks the lane; `references/stacks/*.md` give the full stack; `references/guides/*.md` give per-topic depth. Topic guides are loaded on demand, not up front.
- **Hiring pool and team fluency matter more than benchmarks.** The skill's rules of thumb explicitly prefer the stack the team can debug over the one with the best benchmark.
- **Compliance and policy are vetoes, not tiebreakers.** If self-hosting is mandatory, Clerk doesn't get to argue its way back in.
- **Scope rule is explicit.** A CLI ask gets a CLI recommendation. The skill does not auto-scaffold the full-stack default for narrow requests.
- **Agent frameworks are explicitly out of scope.** This skill covers the platform an agent app runs on, not the agent framework itself.

## Cross-skill integration

| Skill | When it kicks in |
|---|---|
| [`team-composer`](../team-composer) | When a brief needs multi-perspective planning and a role on the team needs to pick/evaluate a stack. `team-composer` owns the discussion; this skill owns the stack recommendation the architect delivers. |
| `brand-workshop` | Separate concern (identity / tagline / logo), not stack-related. |
| [`ui-ux-pro-max`](https://github.com/nextlevelbuilder/ui-ux-pro-max-skill) | Pairs with this skill on the Web/Styling layer once the stack is picked. |
| `engineering:architecture` / `engineering:tech-debt` | Preferred over this skill when the project already has a stack and the question is "should we change it?" rather than "what do we pick?" |

The principle: this skill owns greenfield + migration stack selection. Questions about *existing* architecture decisions go to the engineering skills.

## Install

This skill is distributed as a [Claude Code](https://docs.claude.com/en/docs/claude-code) plugin inside the [`sorawit-w/agent-skills`](https://github.com/sorawit-w/agent-skills) marketplace. From Claude Code or Cowork:

```
/plugin marketplace add sorawit-w/agent-skills
/plugin install tech-stack-recommendations@sorawit-w
```

Once installed, Claude picks the skill up automatically from the description in its `SKILL.md` frontmatter. Invocation triggers on phrases like "what stack should I use," "new project," "pick a runtime," "Bun vs. Node," "SvelteKit vs. Next.js," "database and auth for [X]," "monorepo setup," or "migrate from Node to Bun."

## Status and scope

v0.1. Covers the TypeScript/JavaScript web + API + mobile vertical end-to-end. The recommendations reflect 2026-era tooling and will drift — version bumps will move them along.

- **Supported:** TypeScript/JavaScript projects, greenfield and migrations; web, API, mobile, monorepo layouts; auth, DB, hosting, styling, i18n.
- **Adaptable:** Narrow single-layer questions scale down; full-stack builds scale up.
- **Not supported:** Non-TS/JS stacks; agent framework selection; existing projects with shipped architecture; pure design-system work.

## Contributions

Not accepting external contributions right now. Feel free to fork.

## License

MIT — see the [LICENSE](https://github.com/sorawit-w/agent-skills/blob/main/LICENSE) file at the repo root.
