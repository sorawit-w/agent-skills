# Measurement Loop

Three-layer measurement framework, tool-agnostic adapters, and the weekly
loop that closes execution.

## The three layers

Every channel reports up through these three layers. Skipping any layer
breaks the closed loop — you can't tell what to do next without all three.

| Layer | Question | Examples (B2C) |
|---|---|---|
| **Activity** | Did I do the work? | posts published, emails sent, videos shipped |
| **Engagement** | Is it landing? | impressions, replies, click-through, dwell time |
| **Outcome** | Is it converting? | signups, activation, week-2 retention, paid conversion |

## Per-channel cheat sheet (B2C-weighted)

| Channel | Activity | Engagement | Outcome |
|---|---|---|---|
| Blog/SEO | posts published | uniques, scroll depth, dwell time | email signups from blog |
| X/Twitter | tweets/threads | impressions, replies, profile visits | profile→landing CTR, signups |
| TikTok / Reels | videos posted | views, saves, shares | bio-link CTR, signups |
| Reddit | comments/posts | upvotes, reply rate | profile visits, signups |
| Discord/community | messages, AMAs | active members, msgs/day | invites, signups |
| Email | sends | open rate, CTR | signups, activations |
| YouTube | videos posted | view duration, sub growth | description CTR, signups |
| Paid ads | spend | CPM, CTR | CPA, ROAS |

## Tool adapters

GTM is tool-agnostic. Founder picks a measurement tool at first run. GTM
loads the relevant adapter and pulls metrics on the configured cadence.

### PostHog adapter

- **Best for:** product events (signups, activations) + funnels
- **Auth:** PostHog API key in `secrets.local.yaml`
- **Pulls:** events by name, funnel conversions, retention curves
- **Limits:** rate-limited per project; daily pulls fine, hourly may hit
  limits on free tier
- **MCP:** if PostHog MCP is configured, prefer that over raw API

### Plausible / Umami adapter

- **Best for:** site analytics, privacy-friendly
- **Auth:** Plausible API key (Umami varies)
- **Pulls:** uniques, sessions, top pages, referrers, UTM breakdowns
- **Limits:** daily pulls usually fine; per-page-per-day is the natural
  granularity

### GA4 adapter

- **Best for:** founders already on Google stack
- **Auth:** OAuth via Google MCP if configured; otherwise service account
  JSON in `secrets.local.yaml`
- **Pulls:** standard GA4 reports, custom dimensions if configured
- **Limits:** GA4's quota is generous for daily pulls

### Mixpanel / Amplitude adapter

- **Best for:** product analytics with deep funnels
- **Auth:** API key + project token
- **Pulls:** events, funnels, cohorts, retention
- **Limits:** free tiers have row caps; respect them

### Native-only adapter

When the founder doesn't want a centralized tool. GTM pulls per-platform:

- X: impressions/engagement via X API or scraping (TOS-aware)
- TikTok: TikTok Business API or queue manual export
- IG: Meta Graph API (heavy lift; usually queue manual export)
- YouTube: YouTube Data API
- Reddit: Reddit API (read-only is fine)
- LinkedIn: LinkedIn API or queue manual export

When an MCP doesn't exist for a platform, GTM queues a manual-export task
in Notion or Calendar instead of auto-pulling.

### Supermetrics MCP

If `mcp__plugin_marketing_supermetrics` is configured, prefer it for paid
ad data (Meta, Google, LinkedIn ads). Supermetrics handles the
authentication and aggregation that's otherwise tedious to wire up.

## The weekly loop

Sunday-night cadence (configurable). This is what closes the loop.

```
1. PULL    — agents pull metrics from each connected platform
2. COMPUTE — deltas vs last week + 4-week rolling baseline
3. RANK    — top 3 wins, bottom 3 losses, anomalies (>2σ)
4. SYNTH   — generate hypotheses for next week's adjustments
5. DIGEST  — post summary to #agent-digest
6. ESCAL   — if any metric breached floor or budget alert fired,
              post separately to #agent-escalation
```

## Anomaly detection

For any metric:

- 4-week rolling mean (μ) and stddev (σ)
- Anomaly if |this_week_value - μ| > 2σ
- Floor breach if `this_week_value < config#channels.{name}.floor.{metric}`

Anomalies are warn-level by default; floor breaches are escalation-level.
The founder can override either threshold per metric in `config.yaml`.

## What "winning" looks like — the founder must decide

GTM cannot decide what success means for a project. The first-run wizard
asks for the North Star metric, but ongoing tuning is the founder's job.

GTM surfaces:
- "X is up 20%, Y is flat, Z is down 8% — here's why I think so"
- "Hypothesis A would test whether the TikTok algorithm change matters"
- "Three actions I'd take next week if you say yes"

GTM does not decide:
- Whether a 20% bump is "good enough" (depends on baseline)
- Whether to keep investing in a channel that's flat (depends on stage,
  budget, founder's strategic patience)
- Whether to pivot the message (founder's positioning call)

The loop generates *evidence*; the founder makes the *decision*. P3 mode
expands the agent's decision authority within configured caps, but
North-Star-pivots are always founder calls.

## Honest reporting practices

1. **Report ranges, not point estimates** for last-touch attribution.
   Marketing attribution is messy; agents should not pretend otherwise.
2. **Flag missing data explicitly.** "TikTok numbers missing this week —
   API returned 503 three times. Manual export queued." beats silently
   filling zeros.
3. **Surface the trade-off.** When a metric moves, name what it traded
   off (engagement up, but spend up too — CPA worse).
4. **Distinguish lift from noise.** A single-week spike is noise until
   it persists. Two-week trend is signal.
