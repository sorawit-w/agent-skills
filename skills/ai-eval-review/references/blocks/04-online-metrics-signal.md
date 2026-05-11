# Block 4 — Online Metrics & Signal

## Definition

What's measured in production, and what signal those measurements give. Three things must hold: (1) at least one metric should approximate Block 1's success definition; (2) at least one failure signal must distinguish "feature is working" from "feature is failing silently while engagement holds"; (3) the proxy-vs-direct relationship of every metric is named honestly.

This block depends on Block 1 (without a success target, you can't tell if metrics measure success), Block 2 (production metrics often have weaker label quality than offline — acknowledged), and Block 7 (drift detection feeds off the same metrics).

## Primary probe

> "Pick the metric on your production dashboard that, if it dropped 10 points, would trigger an alarm. Now: would that drop tell you the feature is failing, or could it look identical for a healthy feature where user behavior shifted?"

## Secondary probes

1. **The success-tracking metric.** Which metric most closely tracks Block 1's success definition? "Send-as-is rate" tracks "user got a usable draft" reasonably well — but not for users who send with errors they didn't notice.
2. **Direct vs. proxy.** For each tracked metric: is it the direct measure of success, or a proxy? Engagement / clicks / time-in-feature / retention are almost always proxies. Name them.
3. **Failure signal.** A metric that would surface failing-while-engagement-holds. Examples: support-ticket rate tagged "AI error," post-send sentiment survey, user-detected error reports, downstream conversion (did the sent email get a reply?).
4. **Per-cohort visibility.** Aggregate metrics hide cohort-level failures. Block 5 (cohort breakdown) overlaps here. Does the production dashboard show metrics per segment, or only aggregate?
5. **Latency / cost as metrics.** AI features have non-trivial inference cost and latency. If those aren't tracked, you'll discover a $50K/month bill or 30-second p95 in production. Often missed.
6. **User-side metrics.** What can the user explicitly tell you? Thumbs / 5-star / inline correction / explicit "this was wrong." Without explicit feedback affordances (ai-ux-review Block 4), you only see implicit metrics.
7. **Sample size and significance.** A metric that fluctuates ±15% week-over-week has low signal. State the noise floor.
8. **Counter-metrics.** Metrics designed to NOT improve. If send-rate goes up but sentiment-survey-score goes down, the feature isn't winning — it's just sticky.

## Acceptance criteria

- [ ] **At least one success-tracking metric** named, with explicit relationship to Block 1.
- [ ] **At least one failure signal** that distinguishes silent degradation from engagement.
- [ ] **Proxy-vs-direct** stated for every named metric.
- [ ] **At least one counter-metric** (or explicit acknowledgment of none and acceptance of the optimization risk).
- [ ] **Per-cohort visibility** stated (full breakdown / partial / none — connects to Block 5).
- [ ] **Latency and cost** instrumented or explicitly out of scope for this stage.

## Common gap patterns

- **Engagement-as-success.** Click-through, time-in-feature, retention treated as the success metric. They're proxies for satisfaction, which is a proxy for task completion. Without a failure signal, you can't distinguish "feature is working" from "users are stuck in it."
- **No failure signal.** The team measures only success metrics. A feature failing in ways the success metrics don't capture (silent errors, off-distribution decline) goes undetected.
- **Aggregate-only metrics.** Per-cohort metrics aren't available; the dashboard shows one number. Segment-level failures hide.
- **No counter-metrics.** Send-rate goes up; team celebrates. Nobody checks whether reply-rate, error-flag rate, or sentiment went down.
- **Latency / cost unmeasured.** Discovered after launch: 30-second p95, $80K/month inference bill. The team accepted this in development and lost the chance to design around it.
- **User feedback not instrumented.** Block 4 has no explicit "this was wrong" affordance feeding back into metrics. Only inferred signal (edit rate, churn) is tracked; users with feedback have no path to surface it.
- **Survey fatigue.** "We send a satisfaction survey monthly." Response rate <5%; respondents are biased. The metric exists but isn't real signal.

## Worked example (LLM email drafting)

| Field | Filled |
|-------|--------|
| Success-tracking metric | "Send-as-is rate" + "send-with-edits-to-<30%-words rate." Proxy for Block 1's oracle ("did the recipient interpret it as the user intended"). Estimated correlation: 0.65 to oracle. |
| Direct vs. proxy | "Both above are proxies. The direct measure is post-send reply quality, which we don't yet instrument (gap)." |
| Failure signal | (a) Support tickets tagged "AI-email-error" (rate per 1k drafts sent). (b) Sentiment-survey-score 1% sampled post-send. (c) "Report this draft" button — explicit user flagging. Three independent signals; alarm if any one diverges from aggregate success trend. |
| Counter-metric | "Edit-distance heat-map: if median edit-distance is dropping but explicit-flag rate is rising, users are accepting drafts uncritically — a silent over-trust failure (Block 3 of ai-ux-review). This is our most-important counter-metric." |
| Per-cohort visibility | Dashboard filters by: user tenure (<30d / 30-90d / 90d+), email type (professional / casual / with-factual-claims), voice-sample quality (low / medium / high). Connects to Block 5. |
| Latency / cost | "p50 generation: 2.1s. p95: 6.8s. p99: 14s. Tracked daily. Alert at p95 > 10s. Cost: ~$0.008/draft. Tracked weekly; alert at >$50/day per active user." |
| User feedback | "Thumbs-down on draft (rare — 0.4%). Edit-then-send is the dominant feedback channel; we track word-level edits per draft and feed top-edited-spans back to weekly review. Plain-language 'report this' button in beta — sees 5x more usage than thumbs-down for the same error rate." |
| Sample size / noise | "Send-as-is rate has ±2pp daily noise on current traffic. We don't claim improvements <5pp without a multi-week window." |
| Eval gap to companion |  *Note: This is the explicit hand-off point. If the team needs to actually instrument these — wire up the dashboard, set up alerting, configure W&B/Datadog/Grafana — that's the team's eval platform work, not this skill's. We've named what to track.* |

## When the block is "complete enough"

When there's a success-tracking metric tied to Block 1 with proxy-relationship named, at least one failure signal independent from engagement, counter-metrics in place, per-cohort visibility resolved (full / partial / none with reasoning), and latency + cost instrumented at the lifecycle-appropriate level.

This block is where most "shipped without instrumentation" failures get surfaced. Pre-launch, the gap is usually "we'll measure it after launch." Post-launch, the gap is usually "we measure engagement and assume it tracks success."
