# Marketing Plugin Fallback

When the `marketing:*` plugin is installed (default in Claude Cowork/Code),
GTM dispatches content production to those skills via
`sub-agent-coordinator`. They produce better output than inline prompts —
they've been tuned, they apply consistent structure, and they enforce
their own quality bars.

When the plugin is NOT installed (other harnesses, partial installs), GTM
falls back to inline prompts. Output quality drops; functionality remains.

## Detection

At skill load, check for the presence of these marketing skills:

- `marketing:content-creation`
- `marketing:draft-content`
- `marketing:email-sequence`
- `marketing:brand-review`
- `marketing:performance-report`
- `marketing:seo-audit`
- `marketing:competitive-brief`
- `marketing:campaign-plan`

Per-skill availability matters — some may be present, some absent. GTM
records what's available and dispatches only to present skills, falling
back per-skill where missing.

## Fallback prompt templates

### Replacing `marketing:content-creation`

When dispatching a multi-channel content batch:

```
You are producing a content batch for [project] on [channel] for [campaign].

Brand voice: [load from .gtm/brand-voice.md or config]
ICP: [load from validation-canvas.md or config]
North Star metric: [load from config]
Region: [load from config; apply region adapter from references/regions/{code}.md]
Compliance posture: [load from config — applicable regs]

Deliverables for this batch:
- 1 hero piece (e.g., blog post, long-form thread, video script)
- 3 channel adaptations from the hero (e.g., 3 X threads, 5 IG captions)
- 1 newsletter blurb
- Clear UTM-tagged links throughout

Constraints:
- Brand voice fidelity is non-negotiable. If voice is unclear, mark
  blocks as [VOICE-CHECK NEEDED] rather than guessing.
- All claims must be supported by [validation-canvas / pitch-deck].
  Mark unsupported claims as [CLAIM-CHECK NEEDED].
- Disclosure rules apply: #ad on sponsored, unsubscribe on email.
- Output format: Markdown, one file per piece, in
  .gtm/drafts/{channel}/YYYY-MM-DD-{slug}.md

Out of scope:
- Auto-posting (drafts only, this is dispatch)
- Cross-channel scheduling (GTM handles)
- Performance reporting (separate dispatch)
```

### Replacing `marketing:email-sequence`

```
You are designing an email sequence for [project] for [audience-segment].

Sequence type: [welcome | nurture | reactivation | win-back | launch]
Length: [N emails] over [duration]
Brand voice: [load from .gtm/brand-voice.md]
Compliance: CAN-SPAM (always), GDPR (if eu in regions), PDPA (if th/sg)

For each email:
- Subject line + 2 A/B variants
- Preheader
- Body (plain text + minimal HTML markup)
- CTA with UTM-tagged link
- Send timing relative to entry trigger
- Branch logic if applicable (e.g., "if no open in 48h → variant B")

Hard rules:
- Every email has a working unsubscribe link
- Every email has the legal entity name + physical address (CAN-SPAM)
- No deceptive subject lines
- Output to .gtm/drafts/email/{sequence-slug}/00-overview.md plus
  one file per email
```

### Replacing `marketing:brand-review`

This skill replacement is the **compliance gate**. It must be refusal-capable.

```
You are reviewing [content draft] against brand voice and compliance.

Brand voice profile: [load from .gtm/brand-voice.md]
Compliance posture: [load from config]
Region(s): [load from config]

Score each:
1. Brand voice fidelity (1-10): does this sound like the brand?
2. Claim accuracy: any unsupported claims?
3. Disclosure compliance: required tags/labels present?
4. Region appropriateness: any cultural/regulatory issues for declared regions?
5. Tone safety: anything that could be screenshotted out of context badly?

Output:
- Score per dimension
- Specific edits per issue (line + suggested change)
- Verdict: SHIP | REVISE | REFUSE
- If REFUSE, must include reason — that triggers escalation

If the draft is asking GTM to do something that violates CAN-SPAM, GDPR,
FTC, COPPA, or any platform's published TOS, return REFUSE regardless of
voice score. The compliance gate is refusal-capable for a reason.
```

### Replacing `marketing:performance-report`

For weekly retro digest body:

```
Generate the weekly performance retro for [project], week [start-end].

Inputs:
- Metrics for the week (from measurement adapter)
- 4-week rolling baseline
- Last week's hypotheses (from previous digest)
- Any escalations that fired this week

Structure:
1. North Star metric — value, week-over-week delta, vs target
2. Top 3 wins (per channel or per campaign)
3. Bottom 3 losses
4. Anomalies (>2σ deviations from baseline)
5. What worked (with hypothesis test from last week)
6. What didn't
7. Three hypotheses for next week
8. Three actions GTM recommends taking next week (founder approves)

Tone: matter-of-fact. No hype. Report ranges where attribution is fuzzy.
Length: 600-1200 words. Skim-friendly. Lead with the North Star number.
```

### Replacing `marketing:seo-audit`

```
You are doing a focused SEO audit for [domain or section].

Scope: [page list or section]
Stage: [new launch | optimization | competitive-displacement]
Target keywords: [from validation-canvas or wizard]

Cover:
1. Keyword research — 10-20 target keywords ranked by intent + volume
2. On-page audit — title, meta, H1, internal links, content depth
3. Technical signals — speed proxy, mobile, structured data presence
4. Content gaps — what competitors rank for that this doesn't
5. Quick wins — top 3 actions to ship this week
6. Strategic actions — top 3 actions to invest in this month

Output to .gtm/drafts/seo/audit-YYYY-MM-DD.md
```

### Replacing `marketing:competitive-brief`

```
Produce a competitive brief on [competitor or set of competitors].

Cover:
1. Positioning — how they describe themselves vs how customers describe them
2. Pricing — public, structure, tiering
3. Channel mix — where they show up most
4. Recent moves (last 90 days)
5. Strengths to respect
6. Weaknesses to exploit (without naming them publicly)
7. Three positioning angles this brief recommends for [project]
```

### Replacing `marketing:campaign-plan`

```
Build a campaign brief for [project] for [campaign-name].

Inputs:
- Validation canvas (ICP, value prop)
- Pitch deck (positioning, messaging)
- Brand voice
- Active channels and budgets

Output:
1. Campaign goal — measurable, time-boxed
2. Audience — primary + secondary
3. Message — 1 line, 1 paragraph, 1 elevator
4. Channel plan — per channel: format, frequency, budget, KPI
5. Content calendar — week-by-week, draft titles
6. Risk register — what could go wrong, mitigation
7. Success criteria — what greenlights post-campaign continuation

Output to .gtm/drafts/campaigns/{campaign-slug}.md
```

## Quality warning

When falling back to inline prompts, surface this once per session:

> "⚠️ The `marketing:*` plugin isn't installed. I'm using inline fallback
> prompts — output quality is lower than dispatching to dedicated marketing
> skills. Consider installing the plugin if you'll use GTM regularly.
> Available at: https://docs.claude.com (search for marketing plugin)."

Don't surface it on every action — once per session is enough.
