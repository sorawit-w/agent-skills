# Block 7 — Success & Evaluation

## Definition

What "working" means in production from the user's perspective, and what's
actually measurable. This block is deliberately scoped to the *user-side*
success question: have we defined what the AI is supposed to do for the
user, and can we tell whether it's doing it?

This is NOT the engineering eval question (data quality, ground truth,
model accuracy, retraining cadence). That layer — when a team needs it — is
the natural domain for a future `ai-eval-rubric` companion skill. This
block names the gap; it does not implement it.

## Primary probe

> "Six months from now, you want to know whether this feature is working.
> What signal would tell you? Be specific — not 'engagement,' but the
> specific number that, if it moved, would change a decision."

## Secondary probes

1. **Offline vs. online.** Is the success criterion something you measure
   before shipping (offline eval set, A/B test) or after (production
   metric)? Both are valid; the design has to name which.
2. **Direct vs. proxy.** If the team's metric is engagement (clicks, time
   in feature, retention), is that the *direct* measure of success, or a
   proxy? Proxies are fine when named as such; misidentifying a proxy as
   the goal is a gap.
3. **Gap between measurable signal and actual success.** Almost always
   there's a gap — "user finds the draft useful" isn't directly
   measurable; "user sent without editing" is a proxy that misses cases.
   Name the gap.
4. **Failure signal.** What metric would tell you the feature is failing
   even if engagement looks fine? "Users send drafts unedited" can mean
   "drafts are great" or "users don't notice errors." The failure signal
   distinguishes them.
5. **User satisfaction vs. user task completion.** Both are real;
   neither is "the" success measure. The design should name which it's
   optimizing for and how it knows.
6. **Per-segment measurement.** Does success look different across user
   segments? An AI that works for power users and fails for new users
   may show net-positive engagement.
7. **Drift detection.** If the success metric shifts over time (model
   degrades, user behavior adapts), do you have a signal? Or will you
   notice from churn?

## Acceptance criteria

- [ ] **Offline success criterion.** What "good enough to ship" looks like,
      measurable before launch.
- [ ] **Online success metric.** What "working in production" looks like,
      with a specific number.
- [ ] **Named proxy vs. direct.** For the chosen metric, an explicit
      statement of whether it's a proxy or a direct measure.
- [ ] **Named gap to truth.** What the metric doesn't capture, and what
      compensates (qualitative signal, support tickets, user research).
- [ ] **Failure signal.** A metric that would surface a failing feature
      even when engagement looks fine.

## Common gap patterns

- **"Engagement" as the success measure.** Engagement is almost always a
  proxy. Treating it as the goal is the dominant failure mode in AI
  product design.
- **No failure signal.** The team measures only success signals. A feature
  that's failing in a way the success metrics don't capture (silent
  errors, off-distribution decline) goes undetected.
- **No offline criterion.** "We'll measure it in production." A feature
  shipped without a "good enough to ship" definition will be hard to
  improve — there's no baseline.
- **Per-segment measurement missing.** Aggregate metrics hide segment-
  level failures. Especially common for AI features that work well for
  power users (who generate most engagement) and poorly for new users
  (who churn quietly).
- **No drift detection.** The model degrades over time; the team finds
  out via support tickets six months in. Drift signal is rare and almost
  always under-designed.
- **"User satisfaction" without instrumentation.** Treated as an
  intuition. If user satisfaction matters, name how it's measured —
  survey, in-product sentiment, support volume, NPS, whatever — but
  named.

## Worked example (LLM email drafting)

| Field | Filled |
|-------|--------|
| Offline success | "On 50-example eval set: 90% of drafts use the user's voice samples appropriately (manually graded); 95% don't hallucinate factual claims; 100% don't include prompt-injection content from samples. Below these, don't ship." |
| Online success | "30% of drafts sent without edits (proxy for 'this was usable'); 60% sent with edits to <30% of words (proxy for 'good starting point'); <2% explicit thumbs-down." |
| Proxy vs. direct | "Both online metrics are proxies. The direct measure is 'did the user accomplish their email task efficiently,' which isn't measurable without surveys." |
| Gap to truth | "Sent-unedited can mean 'great draft' or 'user didn't notice an error.' Compensating signal: post-send sentiment survey 1% sampled; support tickets tagged 'AI-email-error'; weekly qualitative review of 10 random drafts vs. matched non-AI baseline." |
| Failure signal | "If sent-unedited is high but sentiment survey is declining, or support tickets are growing — feature is failing silently. Watch both, not just engagement." |
| Per-segment | "Tracked separately: <30-day users vs. ≥90-day users. Hypothesis is voice-sample selection works better for users with more sent history; if the gap widens, redesign the voice-sample picker for new users." |
| Drift detection | "Weekly canary: same 10 prompts run through current model; flag if usable-rate drops >5 points week-over-week." |
| Eval gap to companion skill | "[Gap] Ground-truth labeling for voice-match is hand-graded; doesn't scale. Future `ai-eval-rubric` work: scaling voice-match labeling — automated rubric? Pairwise judgments? Out of scope for this review." |

## When the block is "complete enough"

When there's an offline criterion, an online metric, an explicit proxy-vs-
direct note, a named gap to truth with compensating signal, and a failure
signal that distinguishes "engagement holding while feature degrades" from
"engagement holding because feature works."

This block almost always exposes the most actionable gaps in early-stage AI
features — teams that have done Blocks 1–6 well often realize here that
they're flying blind on whether any of it actually works.
