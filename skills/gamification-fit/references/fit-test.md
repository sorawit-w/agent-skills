# The Fit-Test

Applied per candidate action from the Phase 1 inventory. The output is `[FIT]` or
`[SKIP — reason]`. This is the discriminating core of the skill: **most candidates
should SKIP.** A long FIT list is a smell, not a success.

The test is a gate, not a score. A "no" on any *load-bearing* question is an
immediate SKIP — you do not average your way to a FIT.

---

## The six questions

Run them in order. The first three are load-bearing (a "no" → SKIP). The last
three shape *which* mechanic, and a "no" routes to the veto or a SKIP.

### 1. Is the action genuinely repeatable? *(load-bearing)*

Gamification reinforces *repetition*. A one-shot action — sign up, delete account,
change a setting once — has nothing to reinforce.

- **FIT signal:** the action recurs by design (log an entry, complete a lesson,
  review a card, ship a commit). `repeatable: observed` (analytics-backed) is
  strongest; `inferred` (schema/route implies recurrence) is acceptable with the
  confidence stated.
- **SKIP if:** the action is one-shot, rare, or its repeatability is `unknown` with
  no structural signal. *"SKIP — account deletion is one-shot; nothing to reinforce."*

### 2. Is the underlying data captured? *(load-bearing)*

You cannot reward what you cannot measure. If the event/state behind the action
isn't stored, the mechanic can't exist without first building the instrumentation.

- **FIT signal:** `data_captured: yes` — the action writes a row, increments a
  counter, emits an event.
- **SKIP if:** `data_captured: no`. *"SKIP — 'shares to social' isn't tracked;
  instrument it first, then re-test."* (Surface this as a prerequisite, not a
  recommendation.)

### 3. Is the action reversible / low-stakes? *(load-bearing — also a veto trip)*

Never add play to high-stakes or irreversible decisions. Reinforcing *speed* or
*frequency* on a consequential action is how gamification becomes harm.

- **SKIP / VETO if:** the action moves money at risk, makes a medical/safety
  choice, sends an irreversible legal action, or targets minors. → route to
  `references/anti-patterns.md`; it belongs in the refusals section, not a SKIP
  with a soft reason.

### 4. Is there visible progression worth showing?

Some actions have a natural arc (a skill curve, a collection filling, a streak);
others are flat. Progression is the rawest material for intrinsic-supporting
mechanics.

- **FIT + intrinsic-lean:** there's a real arc — mastery, completion, accumulation.
- **No progression:** still possibly FIT, but the mechanic is thinner (a satisfying
  confirmation moment, not a progress system).

### 5. Is the goal worth reinforcing here? *(specificity gate)*

The action must connect to the Phase 2 metric. "More engagement" is not a goal. If
you cannot name *the metric this mechanic moves*, it fails the specificity gate —
the same way `ai-ux-review` rejects "we handle errors."

- **SKIP if:** the action is goal-irrelevant, or you can only justify it with vague
  "stickiness." *"SKIP — gamifying the settings page doesn't move 'weekly active
  logging'."*

### 6. Is intrinsic motivation present or absent? *(branches Phase 4)*

This does not decide FIT/SKIP — it decides *which* mechanic, and it is the most
consequential judgment in the skill.

- **Present** (the user already *wants* to do this — a hobby, a craft, a goal they
  set themselves): the action carries its own reward. → Phase 4 *supports* it;
  **adding extrinsic rewards risks crowding it out.** Often the best move is a
  light progress-visibility touch, or *nothing*.
- **Absent** (a genuine chore — compliance training, expense reports, required data
  entry): no intrinsic pull exists to protect. → Phase 4 may add extrinsic
  scaffolding, **but only with a named sunset** (see taxonomy).
- **Unsure?** Default to *present*. The crowding-out failure (bolting rewards onto
  motivation that was already there) is worse and more common than the missed-chore
  failure.

---

## The verdict

- **FIT** — Q1–Q3 all "yes", Q5 names a real metric, and Phase 4 has an honest
  mechanic for the Q6 branch. Carry to the card with its mechanic, effort tag, and
  "skip if".
- **SKIP** — any load-bearing "no", or a goal-irrelevant action. Every SKIP carries
  a one-line reason; these populate the prominent "deliberately NOT gamified"
  section. A clear, specific SKIP reason is worth as much as a FIT.
- **REFUSE** — Q3 trips (high-stakes / irreversible / minors). → anti-patterns;
  refusals section, stated as a refusal, not a soft skip.

---

## Common SKIP patterns (catalog)

- **The vanity dashboard** — "add points to the home screen." No action, no metric,
  pure decoration. SKIP.
- **The one-shot** — onboarding completion, first purchase. Celebrate the moment if
  you like, but it's not a *system*. Usually SKIP for a mechanic.
- **The un-instrumented** — a real action with no stored event. Prerequisite, not a
  recommendation.
- **The crowding-out trap** — a beloved creative action (writing, drawing, playing)
  where users are already intrinsically driven. Adding points cheapens it. SKIP or
  support-only.
- **The high-stakes** — anything where reinforcing frequency/speed creates risk.
  REFUSE.
- **The goal-orphan** — fun, but disconnected from the stated metric. SKIP.
