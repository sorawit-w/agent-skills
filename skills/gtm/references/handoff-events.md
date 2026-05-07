# Handoff Events

The contract that lets future workers (support, sales, eng) consume GTM's
output without GTM knowing they exist. Append-only JSONL.

## Storage

Path: `<project-root>/.workspace/events/YYYY-MM.jsonl`

Centralized at the project root (not under `.gtm/`) so future workers can
emit and consume events without reaching into another worker's namespace.
One file per month — minimizes contention and keeps file size manageable
without adding rotation complexity. v1 lets the log grow indefinitely; v2
may add archival when files exceed 50MB.

## Common envelope

Every event has these fields. Reject events that lack any of them.

```json
{
  "event_id": "evt_01HXYZ...",
  "event_type": "lead.captured",
  "version": 1,
  "project": "myapp",
  "timestamp": "2026-05-05T12:34:56Z",
  "source": {
    "worker": "gtm",
    "channel": "tiktok",
    "campaign_id": "tt-launch-42"
  },
  "payload": { /* event-specific */ },
  "consumed_by": []
}
```

| Field | Type | Required | Notes |
|---|---|---|---|
| `event_id` | string (ULID) | yes | Idempotency key. Receivers dedupe by this. |
| `event_type` | enum | yes | Taxonomy entry below. |
| `version` | int | yes | Bump on breaking payload changes only. |
| `project` | string | yes | Project namespace from `config.yaml#project.slug`. |
| `timestamp` | ISO 8601 | yes | UTC. Receivers convert as needed. |
| `source.worker` | string | yes | Worker that emitted ("gtm" today; "support", "sales", "eng" future). |
| `source.channel` | string | optional | When applicable. |
| `source.campaign_id` | string | optional | When applicable. |
| `payload` | object | yes | Event-specific. See per-type schemas below. |
| `consumed_by` | array | yes | Receivers append their worker ID when they pick up the event. Empty at emit. |

## Event types (v1)

### `lead.captured`

Emitted when a person signs up via any GTM channel.

```json
{
  "event_type": "lead.captured",
  "version": 1,
  "payload": {
    "user_id": "u_01HXYZ...",
    "source_channel": "tiktok",
    "utm": {
      "source": "tiktok",
      "medium": "video",
      "campaign": "tt-launch-42",
      "content": "hook-v3",
      "term": null
    },
    "signup_method": "email",
    "first_action": "signup",
    "captured_via": "posthog"
  }
}
```

**Fields:**
- `user_id` — stable identifier for the lead (from analytics tool)
- `source_channel` — which GTM channel drove the signup
- `utm` — full UTM tag set; nulls allowed for missing tags
- `signup_method` — `email | oauth_google | oauth_github | sso | other`
- `first_action` — `signup | demo_request | trial_start | other`
- `captured_via` — analytics source for the event (`posthog`, `plausible`, `manual`, etc.)

**Future receivers:** support/onboarding worker → welcome sequence, activation
tracking. Sales worker (if B2B mode and qualifies) → outreach.

### `lead.qualified_b2b`

Emitted when a B2B form is filled with company info. B2B mode only.

```json
{
  "event_type": "lead.qualified_b2b",
  "version": 1,
  "payload": {
    "contact_id": "c_01HXYZ...",
    "company": "Acme Corp",
    "company_size_band": "51-200",
    "role": "VP Engineering",
    "intent_signal": "demo_request",
    "source_form": "contact-sales-page",
    "enriched_via": "clearbit | apollo | manual | null"
  }
}
```

**Future receivers:** sales worker → SDR sequence, pipeline entry.

### `content.needs_eng`

Emitted when a campaign requires a landing page or feature gate that GTM
cannot produce.

```json
{
  "event_type": "content.needs_eng",
  "version": 1,
  "payload": {
    "artifact_type": "landing_page | feature_gate | redirect | api_endpoint",
    "requirements": "1-page LP for /tiktok-launch with hero, 3 features, signup form posting to /api/leads",
    "deadline": "2026-05-12",
    "blocked_until": null,
    "context_url": ".gtm/drafts/landing-pages/tiktok-launch.md"
  }
}
```

**Future receivers:** engineering worker → build the artifact, post a
`content.delivered` event back when shipped.

### `crisis.detected`

Emitted when sentiment cliff, account issue, or PR signal fires.

```json
{
  "event_type": "crisis.detected",
  "version": 1,
  "payload": {
    "severity": "minor | major | critical",
    "signal_type": "sentiment_cliff | account_suspended | rate_limited | brand_mention_spike | refund_storm | review_storm",
    "affected_channels": ["x", "tiktok"],
    "evidence_url": ".gtm/drafts/crisis-2026-05-05.md",
    "auto_actions_taken": ["paused_x", "paused_tiktok"]
  }
}
```

**Critical severity → full GTM auto-pause.** GTM writes
`.gtm/HALT` with a reason and emits this event. Founder must remove HALT
to resume.

**Future receivers:** founder (always); support worker → may need to
respond to affected users; comms worker (if exists) → public response.

### `feedback.collected`

Emitted when survey responses, review themes, or comment-thread synthesis
produces signal worth handing off.

```json
{
  "event_type": "feedback.collected",
  "version": 1,
  "payload": {
    "source": "in_app_survey | app_store_review | community_thread | nps",
    "theme": "onboarding_friction | pricing_concern | feature_request | bug_report",
    "sentiment": "positive | neutral | negative",
    "confidence": 0.85,
    "raw_excerpts": ["..."],
    "synthesis_url": ".gtm/drafts/feedback/2026-05-05-onboarding-friction.md"
  }
}
```

**Future receivers:** product worker → roadmap input. Support worker →
update KB. Engineering worker → bug triage if `bug_report`.

### `experiment.concluded`

Emitted when an A/B test or campaign hits a decision threshold.

```json
{
  "event_type": "experiment.concluded",
  "version": 1,
  "payload": {
    "experiment_id": "exp-tiktok-hook-v3-vs-v4",
    "winner": "v4",
    "lift_percent": 23.5,
    "confidence": 0.92,
    "sample_size": 12400,
    "recommendation": "Roll out v4 to all TikTok ads; archive v3.",
    "auto_rolled_out": false
  }
}
```

**Future receivers:** GTM itself (self-loop — promote winning variants in
next cycle). Founder (digest mention). Product worker if recommendation
implicates feature flags.

## Idempotency rules

1. **Same `event_id` is the same event.** Receivers dedupe by `event_id`
   on consume.
2. **Re-emission is allowed** when GTM detects the same underlying signal
   on a subsequent run AND the prior event has not been `consumed_by` the
   intended receiver. Use the same `event_id` — receivers will dedupe.
3. **Corrections** use a new event of type `event_correction` referencing
   the original `event_id`:
   ```json
   {
     "event_type": "event_correction",
     "payload": {
       "corrects_event_id": "evt_01HXYZ...",
       "field_path": "payload.utm.campaign",
       "old_value": "tt-launch-42",
       "new_value": "tt-launch-43",
       "reason": "campaign ID was logged before final naming"
     }
   }
   ```
   The original event is never modified or deleted.

## Versioning

Bump `version` on **breaking** payload changes only — removed required
fields, semantically changed enums, structural reshapes. Adding new
optional fields does not require a bump.

Receivers must handle missing optional fields gracefully and log a warning
rather than crashing. If a receiver encounters a `version` it doesn't know
how to handle, it should log a warning and skip the event (not crash, not
block downstream events).
