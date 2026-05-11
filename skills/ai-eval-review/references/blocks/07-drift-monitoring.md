# Block 7 — Drift Detection & Monitoring

## Definition

How you know the AI is still working tomorrow. Covers model drift (the same model produces different outputs over time — typically because user inputs shift), behavior drift (users adapt to the AI in ways that change the inputs it sees), data drift (the underlying world changes — new entities, new events, new user behaviors), and the alerting infrastructure that makes all of the above legible.

This block closes the loop. Block 1 set the target, Block 2 set the substrate, Block 3 set pre-launch rigor, Block 4 set production signal, Block 5 surfaced cohort gaps, Block 6 stress-tested failure modes — and Block 7 keeps all of that current as the world moves.

## Primary probe

> "If your AI silently got 10% worse next month — same model, same prompt, same code — how would you find out? Specifically, which monitor would page someone, and how long would you tolerate the degradation before someone investigates?"

## Secondary probes

1. **Model drift detection.** For non-deterministic LLMs: do you canary the same prompts daily and track output quality? For classical ML: do you re-evaluate offline on production samples and compare?
2. **Behavior drift detection.** As users adapt, the input distribution changes. Is this measured? E.g., users who learn the AI handles X well now send more X, masking the AI's weakness on Y.
3. **Data drift detection.** New entities, events, slang, product names — does your input distribution drift? Measured via population-stability index, KL divergence, or just visual inspection?
4. **Retraining cadence.** For products that retrain: every N days / on threshold / on demand? Whose call?
5. **Model-vendor drift.** If you use an external LLM (OpenAI, Anthropic, Google), you don't control model version. New model snapshots can subtly shift behavior. Do you eval after vendor model updates? Pin to specific versions?
6. **Alerting.** What's the alert path? Slack / email / pager? Who responds? What's the SLA? An alert nobody owns is theater.
7. **The "silent drift" scenario.** Pick the failure mode that *wouldn't* trigger headline-metric alarms. How do you catch it? Block 4's counter-metrics often live here.
8. **Eval-set refresh cadence.** The eval set built in Block 3 ages. New cohorts emerge, new failure modes appear. How often is the eval set refreshed?
9. **Documentation for next-quarter team.** If the person who set up monitoring leaves, can the next person understand what each alert means and how to respond? Often missing.

## Acceptance criteria

- [ ] **At least one drift detector per drift type** that applies (model / behavior / data). Or explicit "we accept this drift type isn't monitored."
- [ ] **Alert ownership** named — a person, a rotation, a team channel.
- [ ] **Silent-drift scenario** considered — what fails without triggering headline-metric alarms.
- [ ] **Eval-set refresh cadence** stated.
- [ ] **Model-vendor drift handled** if using external LLMs (pinning, post-update eval, or accepted-risk note).
- [ ] **Runbook or response doc** exists, or its absence is acknowledged as a gap.

## Common gap patterns

- **"We'll watch the dashboard."** The dashboard requires someone to look at it. Active watching doesn't scale. Without alerting, drift goes undetected until quarterly reviews.
- **Model-vendor drift unhandled.** Team uses "GPT-4o" without pinning to a snapshot. Vendor updates the model; behavior shifts; team doesn't notice for 2 weeks until customer escalation.
- **Behavior drift invisible.** Users adapt to the AI in ways that make headline metrics look fine while underlying value declines. Without canary eval (same inputs over time), invisible.
- **Eval set never refreshes.** The Block 3 eval set is 6 months old; production has shifted; the eval is now measuring a stale problem. Common in fast-moving products.
- **Alert with no owner.** Alerts fire in a Slack channel; everyone assumes someone else is responding. Nothing happens for days.
- **No silent-drift scenario.** Team only monitors success metrics; if those hold, "we're fine." Silent failures (Block 4 counter-metric territory) go undetected.
- **Runbook missing.** Alert fires; on-call doesn't know what it means, what to check, who to escalate to. Common in products that haven't yet had a major drift event.

## Worked example (LLM email drafting)

| Field | Filled |
|-------|--------|
| Model drift detector | "Daily canary: same 25 prompts run through current model; outputs graded by LLM-judge for 'usable-as-draft.' Alert if 5-day rolling average drops >5 percentage points." |
| Behavior drift detector | "Weekly distribution check: types of one-line asks (professional / casual / with-factual / refusal-likely) compared to prior 90-day baseline. Alert if any category shifts >10pp." |
| Data drift detector | "Embedding-distance check on user asks: weekly sample of 200 asks compared to original eval-set embedding centroid. Alert if Wasserstein distance >threshold (calibrated from pre-launch baseline)." |
| Retraining cadence | "No fine-tuning; we use base LLM via API. 'Retraining' equivalents are: (1) prompt revision (quarterly schedule), (2) voice-sample-selection algorithm update (as-needed). |
| Model-vendor drift | "Pinned to `gpt-4o-2024-08-06`. Vendor announces version updates; we re-run the full eval set against the new version before switching. **[Gap]** No automated alert when vendor releases new versions; relies on team awareness of vendor changelog." |
| Alerting | "Alerts route to #ai-email-oncall Slack channel. Daily rotation of 2 ML engineers + 1 PM. SLA: respond within 24 hours; investigate within 72 hours; escalate to engineering lead if confirmed drift." |
| Silent-drift scenario | "Most-feared: model snapshot subtly weighted toward different voice — drafts feel slightly off, send-rate holds, but reply-rate (counter-metric from Block 4) declines. Counter-metric watch is the primary defense; supplemented by weekly qualitative review of 10 random drafts vs. matched non-AI baseline." |
| Eval-set refresh cadence | "Quarterly. Pull 50 fresh examples from prior 30 days of beta-user logs (consenting), have 2 annotators grade, replace 50% of the existing eval set. **[Gap]** Cadence is documented but not yet practiced (skill is pre-launch; next refresh due 3 months post-launch)." |
| Runbook | "draft runbook at `docs/ai-ux/eval-runbook.md`. **[Gap]** Doc exists; tabletop exercise to validate runbook hasn't run yet." |

## When the block is "complete enough"

When at least one drift detector exists per applicable drift type, alert ownership is named, the silent-drift scenario is considered with a defense, eval-set refresh cadence is stated, vendor drift is handled (if applicable), and a runbook exists at the appropriate maturity for the lifecycle stage.

This block is where most pre-launch reviews surface the smallest gap (because most pre-launch teams haven't operated the system at scale yet). It's where most post-launch reviews surface the largest gap (because what looked sufficient at launch turned out to miss the failure modes that emerged from real users).

The Gap Summary entries from this block often feed directly into operational runbook work — and that runbook work is the natural cliff between this skill's review and the team's actual MLOps / observability tooling.
