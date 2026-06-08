# Mechanic Taxonomy

The vocabulary of mechanics, each tagged **intrinsic-supporting** or **extrinsic**,
with the branch rule that decides which applies. The single most important rule:
**match the mechanic to the motivation that's already there** — don't import
extrinsic rewards into a place intrinsic motivation is already doing the work.

> **SDT in one line.** People are intrinsically motivated when an activity feeds
> *autonomy* (I chose this), *competence* (I'm getting better), or *relatedness*
> (this connects me to others). Intrinsic-supporting mechanics *amplify* one of
> those. Extrinsic mechanics add an *external* reward (points, prizes, streaks) —
> useful for genuine chores, corrosive when they replace intrinsic drive.

---

## The branch rule (from the fit-test Q6)

```
intrinsic motivation PRESENT  -> support-only mechanics (this section, group A)
                                 do NOT add extrinsic rewards (crowding-out risk)
intrinsic motivation ABSENT   -> extrinsic scaffolding allowed (group B)
   (a genuine chore)             ONLY with a named, checkable sunset condition
unsure                        -> treat as PRESENT (support-only); the safer error
```

---

## Group A — Intrinsic-supporting (the default, reach here first)

These make existing motivation *visible* and *felt*. They are almost always the
right answer and rarely manipulative.

| Mechanic | Feeds | What it is | Good when |
|---|---|---|---|
| **Progress visibility** | Competence | A bar/ring/map showing how far along a real arc the user is | The action has a genuine arc (a course, a profile, a project) |
| **Mastery feedback** | Competence | Immediate, specific signal that you did it *well* (not just "done") | Skill improves with practice (writing, code, music) |
| **A satisfying "done" state** | Competence | A crisp, earned completion moment — the check, the clear, the ship | Any discrete task worth finishing |
| **Meaningful choice** | Autonomy | Real branching the user controls (pick your path, your goal, your pace) | The product can offer genuine agency |
| **Streak as a *record*, not a leash** | Competence | Showing a run the user built, framed as *theirs* — never "don't lose it" | The user opted into a recurring goal themselves |
| **Visible contribution** | Relatedness | Surfacing how the user's action helped others / a shared whole | Collaborative or community products |
| **Quiet collection** | Competence | An accruing set that fills naturally from real activity (e.g. a history that becomes a graph) | Activity naturally accumulates and is worth seeing |

**Design note:** the best of these are *invisible as gamification* — they read as
good product design (see `references/exemplars.md`). If a Group A mechanic feels
like a "feature you bolted on," it's probably too loud.

---

## Group B — Extrinsic scaffolding (chores only, and only with a sunset)

These add an *external* reward to motivate a behavior that carries no intrinsic
pull. Honest for genuine chores; corrosive everywhere else. **Every Group B
recommendation MUST name a checkable sunset** — the condition under which the
scaffold is removed — or it is refused (Phase 5).

| Mechanic | What it is | Honest only when | Sunset example |
|---|---|---|---|
| **Onboarding streak** | A short run that pulls a user past the cold-start | The first-week habit is the chore; the activity becomes intrinsic later | "Remove after the user logs 3 weeks unprompted" |
| **Completion points** | Points for finishing required, un-fun tasks | Compliance training, mandatory data entry | "Retire once completion rate stabilizes >90%" |
| **Reward for a one-time setup** | A small nudge to finish a tedious configuration | The setup is genuinely tedious and one-time | "One-time; never re-shown" |

**The named-sunset gate:** the card must state *when this scaffold is removed and
how you'll know*. "We'll see how it goes" is not a sunset → refuse. The reason: a
permanent extrinsic reward on a once-chore eventually trains users to do it *for the
reward*, not the outcome — and removing it later then feels like a loss.

---

## PBL (Points / Badges / Leaderboards) — the default trap

PBL is what an LLM emits by default and what most "gamified" products ship. It is
**extrinsic by nature** and the most manipulation-prone family. Default *away* from
it.

- **Points** — only as Group B completion scaffolding, with a sunset. As a
  general-purpose "engagement" currency, refuse.
- **Badges** — acceptable *only* when they mark genuine, hard-won mastery
  milestones (a real achievement), never participation. A badge for logging in is
  noise.
- **Leaderboards** — the most dangerous. They motivate the top ~20% and demotivate
  the bottom ~80%, and they contradict any collaboration goal. Recommend only with
  a specific, defended reason (a genuinely competitive product where users opted
  in); prefer *personal-best* framing over social ranking. A social-comparison
  leaderboard that demotivates the majority is a veto trip (Phase 5).

If you find yourself reaching for PBL, return to Group A and ask what intrinsic
need the action actually feeds. PBL is the answer of last resort, justified
explicitly or not at all.

---

## Output for the card

For each FIT, the card names: the mechanic(s) (group + name), the SDT need it feeds,
the effort tag (CSS-afternoon for a progress ring; websockets-project for live
multiplayer), and — for any Group B mechanic — the **named sunset**. No sunset, no
recommendation.
