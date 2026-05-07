<p align="center">
  <img src="https://raw.githubusercontent.com/sorawit-w/agent-skills/main/assets/gtm-li.svg" alt="gtm — ship the playbook, keep the gate" width="100%"/>
</p>

# gtm 🚧 BETA

A Claude Code skill for the post-pitch-deck step nobody else owns: actually getting users. Builds a phased GTM playbook from your existing startup artifacts, produces multi-channel content with brand-voice fidelity, schedules cadenced rituals (digests, metrics pulls, budget checks), enforces compliance gates, and emits structured handoff events so future workers (support, sales, eng) can plug in without coordination overhead.

> **🚧 Beta — read before relying on it.** Iteration-1 evals scored 100% with-skill (24/24 assertions) vs 27.8% baseline (7/24, +72pp delta) across three test cases (first-run-with-artifacts, cold-start, kill-switch). Those evals validate **structural reliability** — `.gtm/` file structure, helper-function kill-switch pattern, handoff event vocabulary, compliance-gate refusals. They do **not** validate real founder workflows on a real startup project; that dogfooding is the next milestone before graduating to v1. Treat outputs as drafts to review, not artifacts to ship. Breaking changes possible before v1.

## Why this exists

The startup pipeline in this shelf takes a founder from `brand-workshop` → `validation-canvas` → `riskiest-assumption-test` → `pitch-deck` → `startup-grill`. Five sharp steps, each with a clear deliverable. Then the founder hits a wall: **a good product nobody knows about is a waste**, but every "growth" or "marketing" tool out there is either a one-shot content generator (no state, no continuity) or an enterprise CRM (overkill for a solo founder still finding product-market fit).

`gtm` exists to fill that gap. It treats GTM as **the same kind of disciplined artifact** the rest of the pipeline produces — with state, gates, compliance, and a clean handoff to whatever's next — rather than a black box you try once and forget. The trust ramp (P1 read-only → P2 scheduled execution → P3 autonomous-with-escalation) is one-way on purpose, because empirically founders who skip the ramp burn an account, their reputation, or several thousand dollars in ad spend within the first week.

This is also the **first worker designed-for-orchestration** in this shelf. It works standalone today, but it emits structured events (`lead.captured`, `content.needs_eng`, `crisis.detected`) so a future virtual-company agent fleet can read GTM's outputs as inputs without coordination handshakes.

## What it does

- **Builds a phased GTM playbook** from upstream artifacts (auto-detects `validation-canvas.md`, `pitch-deck` content, `brand-workshop` `DESIGN.md`). Channels and ICP come from the canvas; messaging comes from the deck; voice tokens come from `DESIGN.md`. No blank-page generation.
- **Produces multi-channel content** by dispatching to the `marketing:*` plugin via `sub-agent-coordinator` when installed, or falling back to inline prompts when not. Drafts land in `.gtm/drafts/{channel}/` for review before publish.
- **Schedules cadenced tasks** via the `schedule` skill — daily metrics pull, daily digest, weekly retro, 6-hour budget check. If `schedule` isn't installed, writes a `.gtm/scheduled-tasks.md` reminder for manual runs.
- **Enforces compliance gates** — CAN-SPAM, GDPR, FTC endorsement rules, COPPA where minors are in scope, platform TOS for X / Reddit / etc. Refuses non-compliant outputs with a clear reason; three refusals in one cycle escalates as `crisis.detected`.
- **Emits structured handoff events** to `<repo-root>/.workspace/events/YYYY-MM.jsonl` (append-only). Future workers consume by `event_type` + `consumed_by`. v1 taxonomy: `lead.captured`, `lead.qualified_b2b`, `content.needs_eng`, `crisis.detected`, `feedback.collected`, `experiment.concluded`.
- **Posts to Discord** when an MCP is configured (separate channels for `#agent-digest` low-noise and `#agent-escalation` high-signal). Falls back to copy-paste-ready blocks in chat when no MCP.

## What it doesn't do

- **Doesn't auto-post to channels.** First use of any channel on any project requires explicit human approval. After one successful manual review per channel per project, the founder can opt in to autonomous posting for that channel — but never globally, never silently.
- **Doesn't manage relationships.** Community replies, 1:1 DMs, real-human outreach — the skill drafts, never sends. Astroturfing rules apply.
- **Isn't a CRM.** GTM emits handoff events when leads are captured; lead scoring, pipeline progression, and sales motion are downstream concerns.
- **Isn't brand identity, pitch construction, or validation work.** Those are upstream skills (`brand-workshop`, `pitch-deck`, `validation-canvas`, `riskiest-assumption-test`). GTM consumes their outputs; never re-runs them.
- **Isn't a one-shot content tool.** If you just need a single LinkedIn post and don't care about state, voice consistency, or scheduling, route to `marketing:content-creation` directly.

## When to use it

- The pitch deck is locked and you're ready to go acquire users.
- You want multi-channel content with **state, voice fidelity, compliance gates, and a kill switch you can trust**.
- You have upstream artifacts (`validation-canvas.md`, `DESIGN.md`, pitch deck) and want them to flow into the next step automatically.
- You're running marketing solo and keep losing track of what got posted where.
- A campaign needs to halt mid-flight (PR fire, account issue) and you want a real architectural stop, not a prompt-text "please pause."

## When not to use it

- You don't have upstream artifacts yet — run the upstream pipeline first (or accept the cold-start path, where the wizard offers `brand-workshop` as a starting point).
- You want a one-shot piece of content for a non-startup context (a coffee shop announcement, a personal social post, a board-update paragraph that *describes* GTM in prose) — route to `marketing:content-creation` directly.
- You're asking about Google Tag Manager (a different "GTM"). Route to a tag-manager / web-analytics workflow.
- You want a CRM, sales pipeline tool, or relationship-management surface. Wrong shape.
- You want fully autonomous marketing automation with no human in the loop — that's not what this is, and the skill refuses to skip the trust ramp.

## The trust ramp (one-way)

GTM operates in one of three modes, configured per-project in `.gtm/config.yaml`:

- **P1 — Playbook mode (default first run).** Read-only. Generates the playbook + content drafts in `.gtm/drafts/`. No external API calls, no posts, no spend. Promote to P2 when the founder explicitly sets `mode: p2` AND the relevant MCPs (Notion, Discord, the chosen analytics tool) are configured.
- **P2 — Scheduled execution.** All P1 capabilities + scheduled metric pulls + Discord digest posting + manual-task fallback for offline channels. Drafts still require human review per channel, per project, on first use. Promote to P3 when the founder sets `mode: p3` AND has approved at least one round of content per active channel in P2.
- **P3 — Autonomous-with-escalation.** Posts to channels the founder has explicitly opted in (`channels.{name}.autonomous: true`); spends ad budget within configured caps; sends email within caps. Always escalates: budget thresholds, metric breaches, new-region first-touches, sentiment cliffs, compliance refusals.

**Skipping the ramp is a configured refusal.** Setting `mode: p3` without P2 history is a hard error — not a warning. The skill explains why and refuses to run.

## The kill switch (architectural, not prompt-only)

Prompt-text-only kill switches don't work — agents rationalize past them under task-completion pressure, especially on scheduled runs. GTM's enforcement is structural:

- **`.gtm/HALT` file.** Its presence means "no external actions, period." Optional one-line reason inside. Checked by a `require_active()` helper-function wrapper before every external action. The agent doesn't decide whether to honor HALT; the helper enforces.
- **`state.json#status`.** Soft pause — finishes in-flight work, blocks new actions.
- **Harness-killable scheduled tasks.** Cadenced runs are registered through the `schedule` skill, which the harness manages. The founder can disable scheduled runs from the Cowork or Claude Code scheduling UI even if the agent inside the run is misbehaving — outside the agent's blast radius entirely.

Honest limitation: this is a Claude-based skill running in a Claude harness, not a hardened sandbox. The pattern is **best-effort enforcement**, not perfect isolation. The harness scheduling UI is the actually-killable layer; the file-flag pattern is the next-most-reliable; the prompt text is reinforcement, not enforcement. Don't run unattended for >24h until you've observed the trust ramp work end-to-end on your own project.

See [`references/kill-switch-pattern.md`](references/kill-switch-pattern.md) for the helper-function contract and the audit trail format.

## Design choices worth knowing

- **Project-local config, never global.** Each project has its own `.gtm/` folder. Cross-project queries are out of scope at v1; if you run multiple startups, each lives in its own repo with its own state.
- **Append-only event log.** Events are never edited or deleted. Mistakes get corrected via a follow-up `event_correction` event referencing the original `event_id`. The log is the audit trail.
- **Tool-agnostic measurement.** GTM ships with named adapters for PostHog / Plausible / GA4 / Mixpanel / native-only / custom, but mandates none. Founder picks at first run; the choice is recorded; the relevant adapter loads from `references/measurement-loop.md`.
- **B2C primary, B2B opt-in.** Default channel mix and floor heuristics assume B2C. B2B mode adds LinkedIn / cold-email / qualified-lead handling as an opt-in module rather than a fork — keeps the skill from bifurcating before there's evidence both paths need divergent rules.
- **Marketing skills are dispatch targets, not reimplemented inline.** When `marketing:*` is installed, GTM dispatches via `sub-agent-coordinator`. Inline fallback exists for graceful degradation, but the canonical path is delegation.
- **First-run wizard is one question at a time, never batched.** Walls of form questions hit consent fatigue and produce shallow answers, exactly when the founder's attention is most worth respecting. The pacing is deliberate, even though the schema is structured.
- **Beta means "evals validated structure; the world hasn't validated workflow yet."** Iteration-1 was thorough on file outputs and architectural promises; it did not test what real founders feel like during a real launch. That's iteration-2 with real users.

## Install

This skill is distributed as a [Claude Code](https://docs.claude.com/en/docs/claude-code) plugin inside the [`sorawit-w/agent-skills`](https://github.com/sorawit-w/agent-skills) marketplace. From Claude Code or Cowork:

```
/plugin marketplace add sorawit-w/agent-skills
/plugin install agent-skills@sorawit-w
```

Once installed, invocation triggers on phrases like "set up GTM for my startup," "create a launch plan," "build my marketing playbook," "kick off go-to-market," "schedule social posts for my product," "post-launch marketing," or having the upstream pipeline output and asking "what's next for getting users."

## Status and scope

`v0.1` — **BETA**. Single-project per-repo, B2C primary, US region adapter only, three-phase trust ramp, architectural kill switch, six-event handoff taxonomy, `marketing:*` orchestration with inline fallback.

- **Validated by evals (iteration-1, structural):** `.gtm/` file creation, P1 mode default, brand-voice consumption from `DESIGN.md`, ICP detection from `validation-canvas.md`, HALT file behavior, helper-function pattern, three-layer kill switch, handoff event vocabulary, compliance refusals, region adapter loading.
- **Not yet validated:** real founder workflow on a live startup, content quality on real brands, graceful degradation when `marketing:*` is missing, multi-region adapter behavior under non-English content, sustained P2/P3 operation over weeks, scheduling integration with the actual harness scheduler, description-optimization loop pass against your live model.
- **Deferred to v1:** region adapters beyond US (TH, JP, EU, BR added when launches into those markets demand them), the full description-optimization loop run via `skill-creator/run_loop.py` against your authenticated `claude` CLI, the `skill-evaluator` audit on real prompts (not synthetic fixtures).

If asked to do something outside this scope, the skill says so explicitly rather than expanding silently.

## File issues

Beta status means **your real-world findings are the most valuable input we can get**. File at https://github.com/sorawit-w/agent-skills/issues with the `gtm` label — wizard friction, content-quality misses, gates that fired wrong, kill-switch ambiguity, anything.

## Contributions

Not accepting external contributions right now. Feel free to fork.

## License

MIT — see the [LICENSE](https://github.com/sorawit-w/agent-skills/blob/main/LICENSE) file at the repo root.
