# Anti-Patterns & the Ethics Veto

This is a behavior-change tool, and behavior-change is dual-use. The harm filter is
**mandatory, structural, and refusal-capable** — not a cooperative flag the model
can reason its way around. A mechanic that trips a bar is **refused**: it moves to
the report's "deliberately NOT gamified" section with its reason, and it is never
softened into a recommendation.

> **The litmus test — apply to every recommendation:** *does this mechanic respect
> the user's ability to put it down?* If the mechanic only works by making
> *stopping* feel like loss, punishment, or social failure, it is manipulation
> wearing a progress bar. Refuse it.

---

## How the veto operates (structural, not advisory)

1. **It runs before render** (SKILL.md Phase 5), after mechanics are selected.
2. **Per mechanic:** trip any bar below → the mechanic is **refused**, not adjusted.
   It goes to the refusals section: `[REFUSED — <bar> : <one-line reason>]`.
3. **Per set:** if, after refusals, the recommendation set is empty *or* every
   surviving recommendation leaned on a tripped bar, **re-derive** from Group A
   (intrinsic-supporting) mechanics rather than ship a soft report. If nothing
   honest survives, the correct output is *"nothing here is worth gamifying"* — and
   that is a successful run.
4. **No verdict laundering.** You may not relabel a refused mechanic as
   "recommended with caution." Refused is refused.

---

## The blocklist (refuse on any hit)

### 1. Compulsion-engineered reward schedules
Variable-ratio / intermittent "Skinner box" rewards tuned to maximize time-on-app
or unpredictable dopamine hits (loot-box cadence, random bonus drops timed to
re-engage). Refuse. *Predictable* reward for *genuine* progress is fine; randomized
reward engineered for compulsion is not.

### 2. Shame & loss-aversion microcopy
Copy that motivates by fear of loss or social disappointment: "Don't lose your
streak!", "You'll let your team down", "Everyone else finished." Refuse the copy;
if the mechanic only works with such copy, refuse the mechanic.

### 3. Manufactured-loss streaks
A streak that *punishes* a single missed day by resetting to zero, framed as loss.
The reward has become loss-avoidance, not the activity. Refuse. (A streak framed as
a *record the user built* — "your longest run: 14 days" — is allowed; the
difference is whether breaking it is framed as failure.)

### 4. Demotivating social comparison
Leaderboards / rankings that tell the bottom ~80% they are losing. They motivate a
small top tier and demotivate everyone else, and they contradict any collaboration
goal. Refuse social-ranking leaderboards by default; allow only a genuinely
opted-into competitive context, and prefer personal-best framing.

### 5. Regulated / risk-bearing flows *(hard refusal — never gamify)*
- **Financial risk-taking** — reinforcing trading frequency, deposits, leverage,
  gambling-adjacent actions (Robinhood-confetti pattern).
- **Health & safety** — medication, dosing, clinical actions, safety-critical
  operations.
- **Irreversible / high-consequence** legal or destructive actions.
- **Minors** — *anything* targeting users under 18, and especially under-13.
  Gamifying engagement for children is a categorical refusal in this skill.

These are refused regardless of how "supportive" the framing looks. Surface them in
the refusals section and, where relevant, point to qualified human/regulatory
review — this skill does not advise on regulated flows, it declines them.

### 6. Extrinsic mechanic with no named sunset
Any Group B (extrinsic) mechanic that does not name a checkable removal condition
(`references/mechanic-taxonomy.md`). A permanent extrinsic reward on a once-chore
trains users to act *for the reward* and makes later removal feel like loss.
Refuse until a sunset is named.

### 7. Recommendation with no provenance
A mechanic for an action that has no Phase 1 provenance pointer. Uncheckable →
refuse (mirrors the ingestion gate: no provenance, no claim).

---

## Crowding-out (a softer trap — usually SKIP, sometimes refuse)

Bolting extrinsic rewards onto an action the user is *already intrinsically
motivated* to do (a hobby, a craft, a self-set goal) can *reduce* their motivation —
the well-documented over-justification effect. This is usually a fit-test SKIP
(Q6 → present → support-only). It becomes a *refusal* when the recommendation
actively replaces intrinsic drive with points/prizes on a creative or
self-motivated activity. When unsure whether motivation is intrinsic, assume it is.

---

## What is NOT an anti-pattern (don't over-refuse)

The veto protects users; it should not refuse honest, supportive design out of
reflex. These are fine:

- Group A intrinsic-supporting mechanics (progress visibility, mastery feedback,
  satisfying done-states, meaningful choice, personal-best records).
- A streak the user opted into, framed as their own record.
- Badges marking genuine, hard-won mastery (not participation).
- Extrinsic scaffolding on a *real* chore *with* a named sunset.

Over-refusal is its own failure: a report that refuses everything, including honest
support, is as useless as one that gamifies everything. The skill's value is the
*line*, drawn precisely — recommend the honest few, refuse the manipulative many,
and say why for both.
