# AI Agent Context & Skills Reference

Load this when configuring AI agents for a project.

---

## Context Files

Agents may create a `.ai/` folder to store project context:

| File | Purpose | Format |
|------|---------|--------|
| `context.yaml` | Structured project metadata (stack, conventions, skills) | YAML |
| `IDENTITY.md` | Brand/design identity | Markdown |
| `CLAUDE.md` | Human-readable project overview (root level) | Markdown |

**`context.yaml`** is the canonical config. Agents should:
- Create it if missing
- Update it when project context changes
- Reference it for all project decisions

---

## Example context.yaml

```yaml
project:
  name: MyApp
  description: Personal finance tracker

stack:
  runtime: bun
  frontend: sveltekit
  backend: elysia
  database: neon
  orm: drizzle
  auth: clerk
  styling: tailwind + plain css

conventions:
  - Use Svelte 5 runes ($state, $derived), not legacy syntax
  - Tailwind for layout, plain CSS for animations
  - API routes via Elysia, not SvelteKit endpoints
  - Drizzle for all database queries

skills:
  - name: ui-ux-pro-max
    installed: true

brand:
  identity_file: .ai/IDENTITY.md
```

> **Tip:** Keep `context.yaml` under 50 lines if possible. It's config, not documentation.

---

## Skills

Skills are installable modules that give AI agents specialized capabilities.

**Install pattern:**
```bash
bunx <skill-cli> init --ai claude       # Bun
npx <skill-cli> init --ai claude        # Node
```

**Suggested skills:**

| Skill | Use Case | Install |
|-------|----------|---------|
| **UI UX Pro Max** | Design systems, palettes, typography | `bunx uipro-cli init --ai claude` |
| **ClaudeKit Skills** | Comprehensive skill collection | See below |

---

## ClaudeKit Skills

A curated collection of 50+ specialized skills for Claude Code agents.

**Installation:**
```bash
# Add marketplace
/plugin marketplace add mrgoonie/claudekit-skills

# Install skill categories as needed
/plugin install ai-ml-tools@claudekit-skills
/plugin install web-dev-tools@claudekit-skills
/plugin install devops-tools@claudekit-skills
```

**Categories:**
| Category | Contents |
|----------|----------|
| **ai-ml-tools** | Gemini API, context engineering, multimodal |
| **web-dev-tools** | React, Next.js, Tailwind, shadcn/ui, Three.js |
| **devops-tools** | Cloudflare, Docker, GCP, databases |
| **backend-tools** | Node.js, Python, Go, authentication |
| **debugging-tools** | Systematic debugging, root-cause tracing |
| **problem-solving-tools** | Advanced thinking techniques |
| **document-processing** | Word, PDF, PowerPoint, Excel |

**When to suggest:**
- **Web projects** → `web-dev-tools`, `ui-styling`
- **Backend APIs** → `backend-tools`, `devops`
- **AI/ML tasks** → `ai-ml-tools`
- **Debugging** → `debugging-tools`
- **Complex problems** → `problem-solving-tools`

**Repository:** https://github.com/mrgoonie/claudekit-skills

---

## MCP Servers (Optional)

MCP servers extend AI agent capabilities beyond the project. Unlike skills (which install files), MCP servers run in your IDE environment.

| Server | Use Case | Setup |
|--------|----------|-------|
| **Sequential Thinking** | Improves reasoning quality | See MCP docs |
| **Magic MCP** | Generate UI components from 21st.dev | `npx @21st-dev/cli@latest install <client>` |
| **shadcn MCP** | Browse/install shadcn/ui components | `pnpm dlx shadcn@latest mcp init` |
| **Framelink (Figma)** | Fetch Figma designs | See Framelink docs |

**Key differences:**
- **MCP servers** run as background processes in IDE (per-developer)
- **Skills** install static files into project (shared across team)

**Agent behavior:**
- Agents can **suggest** MCP servers when relevant
- Agents **cannot install** MCP servers automatically (requires IDE config)
