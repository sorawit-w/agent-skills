# First-Run Wizard

The seven questions GTM asks at first invocation per project. Asked one at a
time, never batched. Each answer affects what the next question should look
like. The wizard's job is to fill `.gtm/config.yaml` with everything the skill
cannot infer from upstream artifacts.

## Hard rules for the wizard

1. **One question per turn.** Founders abandon mega-prompts. A short
   question with a sensible default beats a 10-field form every time.
2. **Always offer a default.** Never force a founder to invent a value.
   Defaults come from upstream artifacts when present, from B2C-weighted
   conventions otherwise.
3. **Auto-detect aggressively.** If `validation-canvas.md` says
   "B2C consumer", the channel mix question pre-checks B2C-heavy channels.
   If `DESIGN.md` exists, the brand-voice question doesn't ask — it confirms.
4. **The wizard fills config.yaml; nothing else.** No content production
   during the wizard. No content drafts in the wizard's output. The wizard
   ends with "config saved, ready to run — should I run a P1 playbook
   pass now?"

## Question 1 — Project identity

**Goal:** namespace for state, events, and digests.

**Auto-detect order:**
1. `package.json#name` if present
2. `pyproject.toml#name` if present
3. Parent directory name (lowercased, slugified)
4. Ask founder

**Prompt:**
> "What's the project called? Detected: `<slug>` from `<source>` — confirm,
> or give me a different one."

**Stored as:** `config.yaml#project.slug` and `config.yaml#project.name`.

## Question 2 — North Star metric

**Goal:** the one number every digest leads with.

**Default by detected stage:**
- Idea stage / no traction signal → "weekly signups"
- MVP / has signups → "weekly active users"
- Growth → "paid users" or "weekly active users + retention"
- B2B → "qualified pipeline value" or "qualified leads"

**Prompt:**
> "What's the one number you want digests to lead with? Most B2C founders
> use **weekly signups** at this stage — go with that, or pick another:
> WAU / paid users / custom."

**Stored as:** `config.yaml#north_star.metric` and
`config.yaml#north_star.target_per_week` (optional).

## Question 3 — Active channels

**Goal:** which channels GTM produces work for.

**Default by audience signal:**
- B2C primary → X (Twitter), TikTok, IG/Reels, YouTube, blog/SEO, Reddit, Discord-community, email
- B2B primary → LinkedIn, X, blog/SEO, email, cold outreach, partnerships
- Developer audience → X, blog/SEO, GitHub, Hacker News, dev.to, YouTube
- Mixed → ask founder to pick top 3–5

**Prompt:**
> "Which channels are active for this project? Pre-checked from your
> [audience signal]: [list]. Add or remove any."

Multi-select. Free-text custom channels allowed (founder names a custom
channel like "indie hackers" — GTM treats it like community-manual until
an MCP exists for it).

**Stored as:** `config.yaml#channels.{name}.enabled: true|false` per channel.

## Question 4 — Brand voice source

**Goal:** where GTM gets the project's voice profile.

**Auto-detect order:**
1. `DESIGN.md` from `brand-workshop` → use silently, confirm one line
2. `brand-voice.md` if pre-existing → use silently, confirm one line
3. Section in `validation-canvas.md` describing voice → ask to confirm
4. Nothing detected → ask founder

**Prompt when nothing detected:**
> "I don't see brand-voice docs in this project. Three options:
> (1) describe the voice in 2–3 sentences here,
> (2) point me to a doc with example copy,
> (3) run `brand-workshop` to produce a proper brand kit (recommended if
>     you haven't, takes ~20 min)."

**Stored as:** `config.yaml#brand.voice_source` (path or inline string) and
cached in `.gtm/brand-voice.md`.

If founder picks (3) and `brand-workshop` is installed, invoke it as a
sub-skill, then resume the wizard at Q5.

## Question 5 — Measurement tool

**Goal:** where GTM pulls metrics from.

**Tool-agnostic.** GTM ships with adapters for several tools but mandates
none. Founder picks; the choice is recorded; the skill loads the relevant
adapter from `references/measurement-loop.md`.

**Prompt:**
> "Which analytics tool? Common picks for B2C founders:
> **PostHog** (free tier, product events) — recommended if you don't already
> have a stack
> **Plausible** / **Umami** (privacy-friendly site analytics)
> **GA4** (free, more features but heavier)
> **Mixpanel** / **Amplitude** (free tiers, product events)
> **Native-only** (use platform-native analytics — fine for v1)
> **Custom** (you'll point me at an MCP or API I should use)."

**Stored as:** `config.yaml#measurement.tool` and any MCP-specific config
the founder provides.

If the chosen tool's MCP is not configured in this session, surface a one-line
note: *"Heads up — the [tool] MCP isn't set up yet. P1 will work without it,
but P2 metrics-pull will queue manual tasks until you connect it."*

## Question 6 — Digest cadence + Discord setup

**Goal:** when digests fire and where they go.

**Defaults:**
- Cadence: daily summary 08:00 local + weekly retro Sunday 20:00 local
- Channel names: `#agent-digest` (low noise) + `#agent-escalation` (high signal)

**Prompt:**
> "Digest cadence — daily summary at 08:00 + weekly retro Sunday 20:00 is
> the default. Adjust the times or skip dailies if you want.
>
> Discord setup — I'll post digests to `#agent-digest` and escalations to
> `#agent-escalation`. If you don't have a Discord MCP installed yet, I'll
> write digests to `.gtm/digests/` and surface copy-paste-ready blocks here
> in chat. OK?"

**Stored as:** `config.yaml#digests.cadence` (cron-like or named cadence) and
`config.yaml#digests.discord` (channel names + MCP-or-fallback flag).

## Question 7 — Region(s)

**Goal:** which regional adapters load + what languages content gets
adapted to.

**Default:** primary region inferred from working hours / locale of the
founder, or asked.

**Prompt:**
> "Primary region for this project: [detected default, e.g., US]. Add any
> secondary regions (TH, JP, EU, BR, etc.) for content adaptation. For each
> non-English region, drafts will route through `i18n-contextual-rewriting`
> for cultural adaptation."

**Stored as:** `config.yaml#regions: [primary_code, ...secondary_codes]` and
`config.yaml#languages: [primary, ...]`.

For each region listed, GTM loads `references/regions/{code}.md` (or warns
if no template exists) and applies the regional context overlay to channel
worker outputs.

## After the wizard

1. Write `.gtm/config.yaml` (atomic write — `.tmp` then rename)
2. Write initial `.gtm/state.json`:
   ```json
   {
     "status": "active",
     "mode": "p1",
     "created_at": "<iso>",
     "last_digest_at": null,
     "counters": {},
     "first_use_approved": []
   }
   ```
3. Create empty `.gtm/digests/` and `.gtm/drafts/` folders
4. Append `.gtm/secrets.local.yaml` to `.gitignore` (creating the file if
   absent), surface the change to the founder in one line
5. If founder opted into scheduling in Q6 and `schedule` is installed,
   register cadenced tasks via the schedule skill
6. Surface the next-step menu:
   > "Config saved. Ready to run a P1 playbook pass — that produces your
   > GTM strategy + first content drafts in `.gtm/drafts/`, no external
   > API calls. Should I run it now, or do you want to review the config
   > first?"

If the founder says "review config first," surface the resolved
`config.yaml` content with the safe defaults inline, then wait for the
next instruction.
