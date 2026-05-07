---
name: gtm
description: Phased go-to-market for startup products. Builds a GTM playbook from upstream artifacts (validation-canvas, pitch-deck, brand-workshop), produces multi-channel content, schedules cadenced tasks, enforces compliance (CAN-SPAM/GDPR/FTC), emits handoff events. Trust ramp P1→P2→P3 (read-only → scheduled → autonomous). Project-local `.gtm/`. Kill switch via HALT file. Triggers on "set up GTM", "create a launch plan", "build a marketing playbook", "kick off go-to-market", "schedule social posts", "post-launch marketing", "growth ops", "draft launch content", or having pipeline output and asking "what's next for getting users". Single-channel asks for a startup product also trigger. NOT for brand identity (`brand-workshop`), pitch decks (`pitch-deck`), lean canvas (`validation-canvas`), adversarial review (`startup-grill`), one-shot non-startup content (`marketing:content-creation`), CRM/sales. NOT Google Tag Manager (different "GTM"). NOT the idiom "going to market with findings".
---

# GTM

> **🚧 BETA — read before relying on it.** First release: 2026-05-06.
> Iteration-1 evals scored 100% with-skill (24/24) vs 27.8% baseline (7/24,
> +72pp delta across first-run-with-artifacts, cold-start, and kill-switch
> tests). Those evals validate **structural reliability** — `.gtm/` file
> structure, helper-function kill-switch pattern, handoff event vocabulary,
> compliance gate refusals. They do **NOT** validate real founder workflows
> on a real startup project — that dogfooding is the next milestone before
> graduating to v1.
>
> **What this means in practice:** treat outputs as drafts to review, not
> artifacts to ship. The first founder to actually run this on a live
> project will surface issues the evals couldn't see. Breaking changes are
> possible before v1 — particularly around the wizard-confirmation gate
> (whether the playbook auto-runs vs. waits for explicit approval), the
> exact handoff event payload shapes, and the trust-ramp promotion criteria.
>
> **What's known to work** (per evals): auto-detection of upstream
> artifacts, `.gtm/config.yaml` + `.gtm/state.json` creation, P1 mode
> default, brand-voice consumption from `DESIGN.md`, the architectural kill
> switch (HALT file + helper-function wrapper), region-adapter loading,
> compliance-gate refusal on non-compliant content, handoff event emission.
>
> **What's NOT yet validated:** content quality on real brands (evals only
> checked structural keyword presence), graceful degradation when
> `marketing:*` is missing, multi-region adapter behavior under real
> non-English content, sustained P2/P3 operation over weeks, scheduling
> integration with the harness's actual scheduler.
>
> File issues at https://github.com/sorawit-w/agent-skills/issues with the
> `gtm` label.

Get a startup product to market through online and offline channels. This skill
takes a founder's product context (canvas, deck, brand voice) and turns it into
**a phased GTM playbook + per-channel content + scheduled rituals + a
trust-ramped execution loop with compliance gates and an architectural kill
switch**. Designed-for-orchestration: every action emits a structured event so a
future virtual-company agent fleet (support, sales, engineering workers) can
read GTM's outputs as inputs.

The skill's value cut is *founder leverage*, not *founder replacement*. Pretend
otherwise and you'll burn the founder's accounts, reputation, and budget.

## What this skill produces

All artifacts live under `<project-root>/.gtm/`. Created at first run; persists
and grows over time:

```
.gtm/
├── config.yaml           Channels, budgets, North Star, brand voice ref     (in git)
├── state.json            Status, last-digest timestamp, counters             (in git)
├── HALT                  Kill flag — checked before every external action    (in git)
├── secrets.local.yaml    API tokens, credentials                             (gitignored)
├── brand-voice.md        Cached voice (or pointer to brand-workshop output)  (in git)
├── digests/              Daily + weekly digest archives                      (in git)
│   └── 2026-05-05-weekly.md
├── drafts/               Content drafts before publish                       (in git)
│   └── twitter/2026-05-05-launch-thread.md
└── (events written to <repo-root>/.workspace/events/YYYY-MM.jsonl)
```

Plus:

1. **Discord digests** — daily and weekly summaries posted to `#agent-digest`
   when a Discord MCP is configured; otherwise written to `.gtm/digests/` and
   surfaced as copy-paste-ready blocks in chat.
2. **Discord escalations** — high-signal blocks posted to `#agent-escalation`
   when a budget triggers, a metric breaches its floor, a new channel is used
   for the first time, or a crisis signal fires.
3. **Scheduled tasks** — registered via the `schedule` skill at first-run for
   daily metrics pull, daily digest, weekly retro, and 6-hour budget check.
4. **Handoff events** — append-only JSONL at `.workspace/events/YYYY-MM.jsonl`
   so future workers (support, sales, eng) can consume `lead.captured`,
   `content.needs_eng`, `crisis.detected`, and other events GTM emits.

## What this skill is NOT

- **Not an auto-poster.** First use of any channel requires an explicit human
  gate. After one successful manual review per channel per project, the founder
  can opt the channel into autonomous mode for that project. Never global, never
  silent.
- **Not a relationship surface.** Community replies, 1:1 outreach, DMs to real
  humans — the skill drafts, never sends. Astroturfing rules apply.
- **Not a CRM.** GTM emits handoff events when leads are captured, but lead
  management, scoring, and pipeline progression are downstream concerns.
- **Not a brand identity tool.** Logo, tagline, brand strategy → use
  `brand-workshop`. GTM consumes its output, never generates it.
- **Not a pitch-deck builder.** Investor-ready decks → use `pitch-deck`. GTM
  reads pitch-deck content for messaging, never produces slides.
- **Not validation work.** Lean Canvas / VPC → use `validation-canvas`. RAT →
  use `riskiest-assumption-test`. GTM consumes their outputs for ICP and
  positioning.
- **Not adversarial review.** "Will this GTM plan get torn apart by a VC?" →
  use `startup-grill`.
- **Not a one-shot content tool.** If you just need a single LinkedIn post and
  don't care about state, voice consistency, or scheduling, route to
  `marketing:content-creation` (or `marketing:draft-content`) directly.

## Skill Boundaries

| Want this | Use this |
|---|---|
| Multi-channel campaign with state, voice, scheduling | **`gtm`** (this skill) |
| One-shot post for one channel | `marketing:content-creation` / `marketing:draft-content` |
| Email drip sequence with branching | `marketing:email-sequence` (GTM dispatches to it for sequence work) |
| Brand voice review on existing content | `marketing:brand-review` (GTM runs this as its compliance gate) |
| Performance report for a finished campaign | `marketing:performance-report` (GTM dispatches as part of weekly retro) |
| SEO audit | `marketing:seo-audit` |
| Competitor positioning research | `marketing:competitive-brief` |
| Launch identity (logo, tagline, brand) | `brand-workshop` |
| Investor pitch deck | `pitch-deck` |
| Stress-test the GTM plan adversarially | `startup-grill` |

**Pattern:** GTM is an *orchestrator* over the `marketing:*` plugin skills. When
those skills are installed (default in Claude Cowork/Code), GTM dispatches work
to them via `sub-agent-coordinator` and adds the layers they don't provide:
state, scheduling, compliance, kill switch, handoff events, region adaptation.
When `marketing:*` is not installed, GTM falls back to inline prompts (worse
output quality, still functional) — see `references/marketing-fallback.md`.

---

## Phase 0: Path resolution + first-run detection

Run before any other work. Three steps.

### Step 0.1 — Resolve the GTM root

The GTM root is `<project-root>/.gtm/`. Detection order:

1. **Explicit `gtm_root` arg** (passed by future orchestrator) → use as-is.
2. **`GTM_ROOT` env var** set → use it.
3. **Default** → `<cwd>/.gtm/` where `<cwd>` is the project's working directory.

Multi-project case: each project has its own `.gtm/` in its own repo. If the
working directory has multiple `.gtm/` siblings (monorepo of projects), GTM
asks the founder which project this run is for. Default detection: assume
single-project layout — most founders use one repo per startup.

### Step 0.2 — First-run vs subsequent-run detection

- **`.gtm/config.yaml` does NOT exist** → first run. Proceed to Phase 1
  (wizard).
- **`.gtm/config.yaml` exists** → subsequent run. Load config + state, skip the
  wizard, proceed to Phase 3 (execution loop).
- **`.gtm/HALT` exists** → halted. Read the HALT file's reason if present,
  surface to founder, refuse all external actions until founder removes the
  file. Founder can still run gtm in dry-run-only mode for planning.

### Step 0.3 — Auto-detect upstream artifacts

Look for these in the project root and one level deep — use silently if found,
ask in the wizard if not:

| Artifact | Source skill | GTM uses it for |
|---|---|---|
| `validation-canvas.md` | `validation-canvas` | ICP, channels, value prop, stress tests |
| `assumption-test-plan.md` | `riskiest-assumption-test` | Validated channel hypotheses |
| `deck.html` / `pitch-deck/*.html` | `pitch-deck` | Positioning, messaging, narrative |
| `DESIGN.md` / `brand-workshop` output | `brand-workshop` | Voice, tokens, tone profile |
| `kit-manifest.json` | `startup-launch-kit` | Pipeline state, intake-answers cache |

If the founder has `kit-manifest.json` from a prior pipeline run, GTM appends
its own entry there (atomic write) so the manifest reflects post-launch state.
If the manifest doesn't exist, GTM does NOT create it — that's the orchestrator's
job.

---

## Phase 1: First-run wizard (7 questions)

Run only on first invocation per project. The wizard surfaces the seven
decisions the skill cannot make for the founder. Asked one at a time — never
batched into a single mega-prompt — because each answer affects what the next
question should look like.

See `references/first-run-wizard.md` for the full script and answer-handling.
Summary:

1. **Project identity** — name + slug (auto-detected from `package.json#name`
   or parent dir if possible; confirms with founder).
2. **North Star metric** — pick one: weekly signups / weekly active users /
   paid users / something custom. Used as the one number every digest leads with.
3. **Active channels** — multi-select from B2C-weighted defaults (X, TikTok,
   Reels/IG, YouTube, blog/SEO, Reddit, Discord/community, email, partnerships,
   paid). Founder can add custom channels.
4. **Brand voice source** — auto-detected if `DESIGN.md` or brand-workshop
   output exists; else asks: paste a voice description / point to existing
   docs / *offer to invoke `brand-workshop` if installed*.
5. **Measurement tool** — tool-agnostic; user picks Plausible / PostHog / GA4 /
   Mixpanel / Native-only / Custom. The skill records the choice and ships
   with named-but-not-required adapters.
6. **Digest cadence + Discord setup** — daily/weekly/both; channel names for
   `#agent-digest` and `#agent-escalation` (or copy-paste fallback if no
   Discord MCP installed).
7. **Region(s)** — primary + any secondary regions for content. Each region
   loads a reference file from `references/regions/{code}.md` with cultural
   notes, platform map, and local regulations.

After wizard completion: write `config.yaml`, write initial `state.json`,
create empty `digests/` and `drafts/` folders, append secrets path to
`.gitignore` and inform the founder, register scheduled tasks via the
`schedule` skill if the founder opts in.

---

## Phase 2: Operating modes (the trust ramp)

GTM operates in one of three modes. The mode is config-driven and ramps over
time — it cannot skip levels.

### P1 — Playbook mode (default first run)

- **Reads:** auto-detected upstream artifacts + wizard answers
- **Writes:** `.gtm/` files, content drafts in `.gtm/drafts/`, daily/weekly
  digests in `.gtm/digests/`
- **Does NOT:** call any external API, send email, post to social, spend ad
  budget
- **Escalation:** Discord/copy-paste only for surfacing drafts the founder
  reviews
- **Promote to P2 when:** founder explicitly sets `mode: p2` in config.yaml AND
  the relevant MCPs are configured (Notion, Discord, etc.)

### P2 — Scheduled execution mode

- All P1 capabilities plus:
- **Reads:** metrics from connected MCPs (PostHog, Plausible, native platforms
  via supermetrics MCP, etc.)
- **Writes:** state updates with metric counters; posts digests to Discord via
  MCP
- **Does:** schedule cadenced tasks via `schedule` skill; queues offline
  manual-tasks in Calendar/Notion
- **Does NOT:** publish content to social/email/ads — drafts still require
  human review per-channel-per-project for the first run of each channel
- **Promote to P3 when:** founder explicitly sets `mode: p3` AND has approved
  at least one round of content per active channel in P2

### P3 — Autonomous-with-escalation mode

- All P2 capabilities plus:
- **Does:** publish content to channels the founder has opted in (per-channel
  flag in `config.yaml#channels.{name}.autonomous: true`); spend ad budget up
  to configured caps; send email up to caps
- **Always escalates:** budget thresholds, metric breaches, new region
  first-touch, sentiment/crisis signals, anything labeled `confirm_required`
  in the trigger table (Phase 4)

**Skipping the trust ramp is forbidden.** A `config.yaml` that declares P3
without a P2 history is an error condition — GTM refuses and explains why.
This is not negotiable. Empirically, founders who skip P2 burn either an
account, their reputation, or several thousand dollars in ad spend within
the first week.

---

## Phase 3: The execution loop

This is what happens on every (non-first-run) invocation. Order is fixed and
the helper-function wrappers are not optional — they are the architectural
enforcement layer.

```
read_state()                      → load config.yaml + state.json
plan_cycle()                      → decide what work this cycle needs
for each work_item:
    require_active()              → checks HALT file + state.status
    check_dry_run()               → if dry-run mode, log and skip external
    check_budget(category, cost)  → refuses if over cap, escalates if near cap
    check_compliance()            → CAN-SPAM/GDPR/FTC/TOS/COPPA refusals
    check_first_use_gate(channel) → human-review required for first run on channel
    dispatch_to_marketing(...)    → fan-out to marketing:* (or inline fallback)
    region_adapt(output)          → wrap with regional context, route i18n
    execute() | queue_manual()    → MCP call OR queue Calendar/Notion task
    log_event()                   → append to .workspace/events/YYYY-MM.jsonl
aggregate_digest()                → produce daily/weekly summary
post_digest()                     → Discord MCP or copy-paste fallback
```

Every external action must pass through `require_active()`,
`check_dry_run()`, `check_budget()`, `check_compliance()`, and
`check_first_use_gate()` before firing. The agent does not decide whether to
honor these — the helper wrappers enforce. See
`references/kill-switch-pattern.md` for the helper-function pattern.

The compliance gate is `marketing:brand-review` when installed; otherwise an
inline prompt-based check. The compliance gate refuses non-compliant output
with a clear reason and emits a `crisis.detected` event if the gate refuses
three times in one cycle (signals a misconfigured campaign or a confused
founder request).

---

## Phase 4: Escalation triggers

| Trigger | Severity | Auto-pause? | Channel |
|---|---|---|---|
| Budget approached (>80% of cap) | warn | no | `#agent-escalation` |
| Budget hit | block | no — action refused, future actions in category blocked | `#agent-escalation` |
| Metric below floor (per-channel or North Star) | warn | no | `#agent-escalation` |
| First-time using a new channel | confirm | yes (until ack'd) | `#agent-escalation` |
| New region first-touch (GDPR-relevant) | confirm | yes (until ack'd) | `#agent-escalation` |
| Anomaly: >2σ deviation from 4-week baseline | warn | no | `#agent-escalation` |
| Sentiment cliff / crisis signal | block | yes — full pause | `#agent-escalation` |
| Platform error (account suspended, rate-limited) | block | yes — that platform only | `#agent-escalation` |
| Legal flag (action violates CAN-SPAM/GDPR/FTC/TOS) | block | no — action refused | `#agent-escalation` |
| HALT file detected mid-run | block | yes — full halt | `#agent-escalation` |
| Daily digest | info | no | `#agent-digest` |
| Weekly retro | info | no | `#agent-digest` |

**Two-channel discipline.** Digests go to `#agent-digest` (low noise,
scheduled). Escalations go to `#agent-escalation` (high signal, real-time,
mention-on-block). If both went to the same channel the founder would mute it
within a week.

---

## Phase 5: Handoff events (the worker contract)

GTM emits structured events when its job ends and another worker's job begins.
Events accumulate in `.workspace/events/YYYY-MM.jsonl` (centralized event bus,
append-only). Future workers query by `event_type` + `consumed_by` not
containing their worker ID.

**Common envelope (every event has these fields):**

```json
{
  "event_id": "evt_01HXYZ...",
  "event_type": "lead.captured",
  "version": 1,
  "project": "myapp",
  "timestamp": "2026-05-05T12:34:56Z",
  "source": {"worker": "gtm", "channel": "tiktok", "campaign_id": "tt-launch-42"},
  "payload": { /* event-specific */ },
  "consumed_by": []
}
```

**Event taxonomy v1 (full payloads in `references/handoff-events.md`):**

- `lead.captured` — signup detected on any GTM channel
- `lead.qualified_b2b` — B2B form filled (B2B mode only)
- `content.needs_eng` — campaign requires landing page or feature gate
- `crisis.detected` — sentiment cliff, account issue, or PR signal
- `feedback.collected` — survey, review, or comment-thread synthesis
- `experiment.concluded` — A/B test or campaign hits decision threshold

Schema versions are bumped on breaking changes only. Future workers should
handle missing fields gracefully and log a warning rather than crashing.

---

## Hard rules

1. **Architectural kill switch — never prompt-only.** The HALT file +
   helper-function wrapper is the enforcement. Prompt-text-only kill switches
   get rationalized past under task-completion pressure. The agent does not
   *decide* whether to honor HALT; the helper enforces. See
   `references/kill-switch-pattern.md`.

2. **Secrets never in chat, never in git.** Three-tier secret model:
   ephemeral (paste once, in-session, never persisted) → project
   (`.gtm/secrets.local.yaml`, gitignored, agent-readable, never logged) →
   external (delegate to MCP connectors, GTM never holds raw tokens). Default
   to external. Never echo a secret value back to the founder, even
   partially. Never include a secret in a digest, draft, error message, or
   event payload.

3. **Trust ramp is one-way.** P1 → P2 → P3, never skip levels. Each level
   requires demonstrated success at the prior level. Skipping is configured
   refusal, not a warning.

4. **First-use channel gate is per-project.** First time GTM uses a channel
   on a project, content goes to drafts and waits for human review.
   "Successful in another project" does not transfer trust — different
   audience, different brand state, different platform algorithms.

5. **Compliance gate is refusal-capable.** `marketing:brand-review` (or
   inline fallback) can refuse to ship content. Refusals are logged with
   reason; three refusals in one cycle escalate as `crisis.detected`.

6. **Marketing skills are dispatch targets, not reimplemented inline.** When
   `marketing:*` is installed, dispatch via `sub-agent-coordinator`. Inline
   fallback is the worse path, used only when the plugin is missing.

7. **Project-local config; never global.** Each project has its own
   `.gtm/config.yaml`. No `~/.gtm/` global config. Multi-project state lives
   in each project's own folder.

8. **Append-only event log.** Events are never edited or deleted. Errors in
   payload structure get a follow-up `event_correction` event referencing the
   original `event_id`.

9. **`.gitignore` is append-then-inform.** First run appends
   `.gtm/secrets.local.yaml` to the project's `.gitignore` and tells the
   founder it did. Never silently rewrites.

10. **Dry-run is loose by default.** Dry-run mode blocks WRITE actions but
    allows read-only API calls so the founder can test the digest pipeline
    end-to-end without sending anything.

---

## Output Files

```
<project-root>/.gtm/
├── config.yaml                                    Per-project config
├── state.json                                     Status + counters
├── HALT                                           (optional, kill switch)
├── secrets.local.yaml                             (gitignored)
├── brand-voice.md
├── digests/YYYY-MM-DD-{daily|weekly}.md           Append-only archive
├── drafts/{channel}/YYYY-MM-DD-{slug}.md          Content before publish
└── (events written to <repo-root>/.workspace/events/YYYY-MM.jsonl)
```

No other files. Do not scatter intermediate work outside `.gtm/`.

---

## Quality Checklist

Before any external action ships, verify:

**Helper-function gates passed**
- [ ] `require_active()` returned true (no HALT file, status=active)
- [ ] `check_dry_run()` returned "execute" not "skip"
- [ ] `check_budget(category, cost)` returned within-cap
- [ ] `check_compliance()` returned no flags
- [ ] `check_first_use_gate(channel)` returned approved (or this is not a first use)

**Content quality**
- [ ] Brand voice applied — output passed `marketing:brand-review` (or inline)
- [ ] Region adapter applied — non-English drafts went through `i18n-contextual-rewriting`
- [ ] No secrets in the output (token, key, password, OAuth code, session ID)
- [ ] Required disclosures present (`#ad`, sponsored tag, unsubscribe link)

**Operational**
- [ ] State.json updated with the action (idempotency key set)
- [ ] Event logged to `.workspace/events/YYYY-MM.jsonl`
- [ ] If escalation fired, posted to `#agent-escalation` not `#agent-digest`
- [ ] Schedule registrations match `config.yaml#schedule`

**First-run only**
- [ ] `.gtm/` folder created
- [ ] `.gitignore` appended with secrets path + founder informed
- [ ] Wizard ran 7 questions one at a time — not batched
- [ ] Brand voice source resolved (auto-detect or wizard answer)

---

## Cross-Skill Integration

| Skill | When to use |
|-------|-------------|
| `validation-canvas` (our own) | Upstream. GTM reads `validation-canvas.md` for ICP, channels, value prop. If absent and the founder is at idea stage, recommend running it before GTM (better inputs → better playbook). |
| `riskiest-assumption-test` (our own) | Upstream. GTM reads `assumption-test-plan.md` to weight channels by validated hypotheses. |
| `pitch-deck` (our own) | Upstream. GTM reads pitch deck content for messaging consistency. |
| `brand-workshop` (our own) | Upstream. GTM reads `DESIGN.md` for brand voice tokens. If absent, the wizard offers to invoke brand-workshop. |
| `startup-grill` (our own) | Adjacent. After GTM ships P1 playbook, the founder may grill it for blind spots. |
| `startup-launch-kit` (our own) | Optional orchestrator. GTM is post-pipeline (after pitch-deck). The kit can call GTM as a sixth step in a future version. |
| `team-composer` (our own) | Use for *discussion* on a narrow GTM question (channel choice, messaging review) when the artifact-grade playbook isn't needed. |
| `i18n-contextual-rewriting` (our own) | Hard dispatch target. Non-English content drafts route through this skill for cultural adaptation, not raw machine translation. |
| `sub-agent-coordinator` (our own) | Hard dispatch target. Multi-channel content fan-out runs through this skill's patterns. |
| `tech-stack-recommendations` (our own) | When GTM emits a `content.needs_eng` event for a landing page and the founder has no chosen stack. |
| `schedule` (Anthropic) | Hard dispatch target. Cadenced tasks (daily metrics pull, daily digest, weekly retro, 6-hour budget check) register here at first run. |
| `marketing:content-creation` (Anthropic) | Soft dispatch target. Per-channel content drafts. Inline fallback if missing. |
| `marketing:draft-content` (Anthropic) | Soft dispatch target. Single-channel copy generation. Inline fallback if missing. |
| `marketing:email-sequence` (Anthropic) | Soft dispatch target. Drip flows + lifecycle email. Inline fallback if missing. |
| `marketing:brand-review` (Anthropic) | Soft dispatch target — used as the compliance gate. Inline fallback if missing. |
| `marketing:performance-report` (Anthropic) | Soft dispatch target. Used for weekly retro digest body. Inline fallback if missing. |
| `marketing:seo-audit` (Anthropic) | Soft dispatch target. Used when a content channel includes SEO. Inline fallback if missing. |
| `marketing:competitive-brief` (Anthropic) | Soft dispatch target. Used during P1 playbook construction. Inline fallback if missing. |
| `marketing:campaign-plan` (Anthropic) | Soft dispatch target. Used for time-boxed launches and pushes. Inline fallback if missing. |

**Principle:** GTM owns the *orchestration layer* — state, scheduling,
compliance, kill switch, region adaptation, handoff events. Content production
is delegated to `marketing:*` when available, with inline fallback when not.

**Graceful degradation:**
- Missing `marketing:*` plugin → inline content prompts, lower quality, surfaced warning to founder once per session.
- Missing `schedule` skill → cadenced tasks become a `.gtm/scheduled-tasks.md` reminder file the founder runs manually; warning surfaced.
- Missing Discord MCP → digests written to `.gtm/digests/` and surfaced as copy-paste blocks in chat.
- Missing `i18n-contextual-rewriting` → English-only mode with warning if any region in config requires non-English.
- Missing `brand-workshop` output → wizard asks for brand voice description; offers to invoke `brand-workshop` if installed.
- Missing all upstream artifacts → wizard runs longer (asks for ICP, positioning, voice directly); recommends running upstream pipeline first.
