# Signal Detection & Recommendations

Use this reference to identify gaps in developer tooling, invoke available skills, and suggest missing ones.

---

## External Resources Registry

A curated catalog of external skills, tools, and design resources is maintained in `external-resources.md`. When a signal is detected and no installed tool covers it, **check the registry before searching the MCP marketplace** — it may already have a vetted recommendation with install instructions.

→ See `references/external-resources.md` for the full catalog, install commands, and the lookup flow.

---

## How to Detect Signals

Scan the project systematically for indicators:

1. **package.json / deno.json / pyproject.toml** — runtime, framework, dependencies
2. **Directory structure** — presence of specific app types (web, mobile, api, admin)
3. **Config files** — .env, .github/, .gitlab-ci.yml, figma links, etc.
4. **agent-context.yaml** (project root) — explicitly recorded signals and tech stack
5. **Git history** — recent commits, patterns in changes
6. **README / docs** — stated project goals and planned work

---

## Pre-Check Rule

**Always check first:** Before suggesting a new skill or MCP, verify it is not already:
- Installed and available in the current session (check loaded tools/skills)
- Referenced in agent-context.yaml under installed_skills or installed_mcps
- Already used elsewhere in the codebase

Never suggest what is already there. Suggest complementary tools only.

---

## Finding Available MCPs

Don't guess which MCPs exist — look them up. Most agents have a way to query an MCP registry or marketplace programmatically.

**Lookup workflow:**
1. **Detect signal** — e.g., project uses Stripe for payments
2. **Check installed** — is a Stripe MCP already loaded in the session?
3. **Search registry** — if the agent supports it, query the MCP registry with relevant keywords (e.g., `["stripe", "payment", "billing"]`). Use multiple keywords to cast a wider net.
4. **Evaluate results** — check that the MCP covers what's actually needed (don't install a generic "finance" MCP when you need Stripe-specific API access)
5. **Suggest with context** — tell the developer what you found, why it's relevant, and let them decide whether to install

**Example flow:**
```
Signal: stripe.config.ts found in project root

→ Check: No Stripe MCP loaded in session
→ Search registry: ["stripe", "payment"]
→ Found: "Stripe MCP" — manage products, subscriptions, invoices, webhooks
→ Suggest to developer with rationale
```

If the agent doesn't support registry search, fall back to naming the MCP category and letting the developer find it in their agent's marketplace or settings.

---

## Signal → Suggestion Mapping

| Signal | Category | Suggestion | When to Recommend | Rationale |
|--------|----------|------------|--------------------|-----------|
| `locales/` dir, i18n package (react-i18next, next-intl, etc.) | Skill | i18n contextual rewriting | Multi-language content exists | Streamline translation workflows |
| No framework chosen, new project, vague requirements | Skill | Tech stack recommendations | Decisions not yet made | Fast-track platform + runtime choice |
| Auth config (Clerk, Auth0, Firebase, etc.) | MCP | Auth provider MCP (e.g., Clerk MCP, Auth0 MCP, Supabase Auth MCP) | Auth is integrated or planned | Connect to auth service for real-time user/org data |
| Database config (Drizzle, Prisma, TypeORM, Mongo, etc.) | MCP | Database MCP (e.g., Postgres MCP, Supabase MCP, PlanetScale MCP, MongoDB MCP) | Schema or migrations exist | Query schema, inspect migrations, understand data model |
| Figma file links in README or .ai/ files | MCP | Design tool MCP (e.g., Figma MCP) | Design system or components referenced | Extract design context, create Code Connect mappings |
| .github/workflows, .gitlab-ci.yml, vercel.json present | MCP / Skill | Deployment MCP + CI strategy (e.g., Vercel MCP, Cloudflare MCP, Netlify MCP) | Pipelines exist or need work | Deploy, inspect logs, manage environments |
| No test framework configured (jest, vitest, bun test absent) | Skill | Testing strategy | Tests not yet implemented | Design test plan before writing tests |
| Linear, Jira, Asana URL in docs or git commits | MCP | Project tracker MCP (e.g., Linear MCP, Jira MCP, Asana MCP) | Work is tracked externally | Fetch issues, update status, link PRs |
| Slack, Teams, Discord references in docs or README | MCP | Communication MCP (e.g., Slack MCP, Discord MCP) | Team communicates via chat platform | Send updates, read channels, post notifications |
| Google Drive, Notion, Confluence links in docs | MCP | Knowledge base MCP (e.g., Notion MCP, Google Drive MCP, Confluence MCP) | Documentation lives externally | Read/write docs, search knowledge base |
| Figma file + code component refs not linked | Skill | Code Connect mapping | Design system exists | Map Figma components to code with Code Connect |
| Stripe, payment config, billing references | MCP | Payment MCP (e.g., Stripe MCP) | Payment integration exists or planned | Manage products, check subscriptions, inspect webhooks |
| 3+ independent, non-blocking tasks | Delegation | Sub-agent or teammate | Parallelism possible | Speed up execution via delegation |
| Team brainstorming, design critique, user research needed | Skill | Design/research skills | Feedback or validation required | Structured collaboration on design/product decisions |
| UI work needed, `DESIGN.md` exists at repo root | Rule | Load `references/design-md.md` | Task touches design tokens (colors, typography, spacing, components) | YAML front matter is the canonical design contract — do not invent alternatives or silently override |
| UI work needed, no DESIGN.md or design system present | Pattern | DESIGN.md + ui-ux-pro-max | UI/UX work with no brand constraints | Bootstrap a design system from a brand reference |
| Component in shared dir (`components/`, `ui/`, `lib/`) imported by ≥2 callers, no `storybook` in package.json | Tool | Storybook | A reusable UI component exists with no interactive documentation tool | Document component states; prevent visual drift across consumers |
| `storybook` in package.json but `@storybook/test-runner` is not | Tool | @storybook/test-runner | Storybook is installed without auto-render-smoke | Every story becomes a Playwright-driven render test for free |
| Brand/logo/visual identity work | Skill | Brand workshop | Visual brand not yet defined | Facilitate collaborative brand exploration |
| Multiple languages in codebase (JS, Python, Go, etc.) | Skill | i18n (if content) or multi-language support skill | Polyglot codebase | Support development across multiple language ecosystems |
| Complex refactor or multi-file changes | Delegation | Sub-agent | Scope affects many files | Parallelize refactoring to speed execution |

---

## How to Present Suggestions

When you detect a signal, format the suggestion like this:

```
Detected signal: [what you found]

Recommendation: [skill or MCP name]
Why: [concrete reason why it would help with this project]
Install: [command from external-resources.md or MCP registry]
```

Example:

```
Detected signal: UI work needed, no design system found

Recommendation: ui-ux-pro-max + awesome-design-md
Why: Generate a tailored design system; use BMW's DESIGN.md as brand reference
Install: npm i -g uipro-cli && uipro init --ai claude
```

---

## Suggestion Guidelines

- **Be helpful, not pushy** — Present as "Consider X because..." not "You must use X"
- **Developer chooses** — Emphasize that suggestions are optional and the developer decides
- **Group by phase** — If multiple signals detected, suggest in setup/planning phase, not mid-implementation
- **Link to workflow** — If suggesting a skill, show where it fits in the playbook (e.g., "Use during Planning phase")
- **Verify context** — Always ask if unsure whether a tool is already in use

---

## Quick Check Template

Use this when assessing a new project:

```
[ ] i18n? locales/ directory found → recommend i18n skill
[ ] Auth? Config detected → search registry for auth provider MCP
[ ] Database? Schema/migration files found → search registry for database MCP
[ ] Design? Figma links found → search registry for Figma MCP
[ ] CI/CD? .github/ or vercel.json found → search registry for deployment MCP
[ ] Payments? Stripe/billing config found → search registry for payment MCP
[ ] Chat? Slack/Discord references found → search registry for communication MCP
[ ] Docs? Notion/Confluence/GDrive links → search registry for knowledge base MCP
[ ] Tracker? Linear/Jira/Asana references → search registry for project tracker MCP
[ ] Tests? Framework configured → note testing patterns; if missing → recommend testing strategy skill
[ ] Multiple tasks? Task list created → consider sub-agents
[ ] Brand work? Visual brand undefined → recommend brand workshop
[ ] UI work? `DESIGN.md` present at repo root → load `references/design-md.md`; treat YAML front matter as authoritative
[ ] UI work? No DESIGN.md or design system → suggest DESIGN.md pattern + ui-ux-pro-max
```
