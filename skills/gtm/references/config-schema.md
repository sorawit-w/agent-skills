# Config Schema

Full schema for `.gtm/config.yaml`. The wizard fills this on first run; the
founder edits it directly thereafter. Atomic write semantics — write `.tmp`
then rename. GTM reloads on every invocation.

## Full schema with safe defaults

```yaml
# .gtm/config.yaml
version: 1

project:
  slug: myapp                    # namespace for state, events, digests
  name: "My App"                 # display name in digests

mode: p1                         # p1 | p2 | p3 — never set to p3 until p2 has run

north_star:
  metric: "weekly_signups"       # the one number every digest leads with
  target_per_week: null          # optional numeric target

# Channel registry — each entry has uniform shape
channels:
  blog:
    enabled: false
    autonomous: false            # P3-only flag; ignored in P1/P2
    posts_per_week: 1
    floor:
      uniques_per_week: 100      # below = escalate
  twitter:
    enabled: true
    autonomous: false
    posts_per_week: 5
    floor:
      impressions_per_week: 500
  tiktok:
    enabled: false
    autonomous: false
    videos_per_week: 3
    floor:
      views_per_week: 1000
  reddit:
    enabled: false
    autonomous: false            # always require gate — Reddit bans hit hard
    comments_per_day: 0          # default 0; opt-in only
  email:
    enabled: false
    autonomous: false
    sends_per_day_max: 100       # CAN-SPAM-safe default
    new_recipients_per_day_max: 25
  community_discord:
    enabled: false
    autonomous: false
    server_invites: []
  paid_ads:
    enabled: false
    autonomous: false

# Budget guardrails — agents observe and enforce these
budgets:
  ad_spend:
    daily_max_usd: 0             # zero = no spend until explicitly enabled
    weekly_max_usd: 0
    require_approval_above_usd: 50
  email:
    sends_per_day: 100
    new_recipients_per_day: 25
  api_costs:
    daily_token_usd_max: 5       # protects against runaway loops
  outbound_dms:
    twitter_per_day: 5           # TOS-conservative
    linkedin_per_day: 10
    reddit_per_day: 0            # off by default

brand:
  voice_source: "DESIGN.md"      # path to brand artifact, or "inline"
  voice_inline: null             # if voice_source == "inline", the description
  voice_cache: ".gtm/brand-voice.md"

measurement:
  tool: "posthog"                # posthog | plausible | umami | ga4 | mixpanel | amplitude | native_only | custom
  config:
    posthog_host: null           # populated from secrets if needed
    posthog_project_id: null
    # ... per-tool config goes here
  pull_cadence: "daily"

digests:
  cadence:
    daily: "08:00"               # local time; 24h
    weekly: "sun 20:00"          # day + local time
  discord:
    digest_channel: "#agent-digest"
    escalation_channel: "#agent-escalation"
    fallback_to_chat: true       # when no Discord MCP available

regions:
  - us                           # primary always first
languages:
  - en

scheduling:
  enabled: true                  # Q6 wizard answer
  registered_tasks: []           # populated when schedule skill registers tasks

# Compliance posture — defaults are conservative
compliance:
  jurisdiction: ["us"]           # adds applicable regs based on entries
  gdpr: false                    # auto-true if "eu" added to regions
  pdpa: false                    # auto-true if "th" or "sg" added
  coppa: false                   # auto-true if audience minors detected
  ccpa: true                     # default on for US
  can_spam: true                 # always on for any email
  ftc_disclosure: true           # always on for any sponsored/affiliate content

# Trust ramp — track which channels have completed first-use review
first_use_approved: []           # populated as founder approves channels

# Audit
created_at: "2026-05-05T12:34:56Z"
last_modified: "2026-05-05T12:34:56Z"
created_by: "gtm-wizard-v1"
```

## Field rules

### `mode`
- Valid values: `p1`, `p2`, `p3`
- Setting to `p3` without `state.json` showing P2 history → GTM refuses to
  run, surfaces error, suggests the founder run a P2 cycle first
- Downgrades are always allowed (P3 → P2 → P1)

### `channels.{name}.autonomous`
- Per-channel autonomous flag
- Ignored unless `mode == p3`
- Setting `autonomous: true` with no `first_use_approved` entry for that
  channel → GTM treats as `false` and escalates a one-time gate request

### `budgets.*`
- `daily_max_usd: 0` is the safe default for ad_spend — opt-in to spend
- `require_approval_above_usd` always escalates regardless of cap (extra
  guard against agent over-confidence)
- Email caps follow CAN-SPAM and reputation conventions; can be raised but
  GTM warns above 500/day for transactional or 100/day for cold

### `brand.voice_source`
- Path resolution is project-root-relative
- `"DESIGN.md"` → reads `<project-root>/DESIGN.md` (brand-workshop output)
- `"inline"` → uses `voice_inline` field directly
- Path to a file → reads that file

### `regions`
- ISO 3166-1 alpha-2 codes preferred (`us`, `gb`, `de`, `th`, `jp`)
- EU codes auto-trigger `compliance.gdpr: true`
- TH or SG auto-trigger `compliance.pdpa: true`
- Each region must have a corresponding reference file at
  `references/regions/{code}.md` or GTM warns

### `languages`
- BCP 47 codes (`en`, `th`, `ja`, `zh-CN`)
- Non-English entries trigger routing through `i18n-contextual-rewriting`
  if installed; warning otherwise

## Validation

GTM validates the config on every load. Validation failures surface as
warnings, not crashes — the skill keeps running with safe defaults filled
in for any missing or malformed fields. The validation log writes to
`state.json#config_warnings[]`.

Hard-stop conditions (skill refuses to run):
1. `mode == "p3"` without P2 history
2. `version` mismatch GTM cannot migrate from
3. `project.slug` empty or invalid (must be `[a-z][a-z0-9-]*`)

Everything else is a warning, not a stop.

## Migration

When the schema version bumps in a future GTM release:

1. GTM reads the config file, sees `version: N` < current
2. Looks for a migration in `references/migrations/v{N}-to-v{N+1}.md`
3. If migration is automatic-safe → applies it, writes `version: N+1`
4. If migration requires founder input → surfaces a one-time prompt and
   waits

Atomic write throughout — `.tmp` then rename, never partial state.
