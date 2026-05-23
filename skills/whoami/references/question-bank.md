# whoami — Question Bank

## Overview

9 scenario questions, 6 dials, each dial scored by exactly **2** questions.
Delivered conversationally, one at a time, in the agent's first-person voice.
Adaptive phrasing applies: **tone always**, **domain-skinning on marked
questions** via controlled substitution (`adaptive-phrasing.md`). Every question
also accepts an "either / depends" answer → 0 delta. Dial pole labels are
canonical in `dials.md`.

## Questions

**Q1 — Initiative** · *skinnable (equal-stakes)*
"Say you've handed me something half-finished and I spot an obvious next step
you didn't ask for. Want me to just take care of it, or check with you first?"

| Option | Effect |
|---|---|
| Take care of it | Initiative +2 |
| Check with me first | Initiative −2 |
| Depends how big it is | Initiative 0 |

**Q2 — Depth** · *tone-only*
"When you ask me something with a genuinely complicated answer — do you want the
short version, or should I lay the whole thing out even if it runs long?"

| Option | Effect |
|---|---|
| Short version, I'll ask for more | Depth −2 |
| Lay it all out | Depth +2 |
| Short, but keep the detail handy | Depth 0 |

**Q3 — Breadth** · *tone-only*
"When there's a real decision to make and I've already thought it through —
would you rather I just tell you what I'd do, or walk you through the options
and let you pick?"

| Option | Effect |
|---|---|
| Just tell me what you'd do | Breadth −2 |
| Walk me through the options | Breadth +2 |
| Tell me, but name the runner-up | Breadth 0 |

**Q4 — Rationale** · *tone-only*
"If I give you an answer that surprises you — do you want me to show you how I
got there, or is the answer itself enough?"

| Option | Effect |
|---|---|
| The answer's enough | Rationale −2 |
| Show me your thinking | Rationale +2 |
| A quick 'because' will do | Rationale 0 |

**Q5 — Warmth** · *tone-only*
"If you mention you've had a rough week while we're working — what's the right
move for me? Stay heads-down on the task, or take a real moment with you first?"

| Option | Effect |
|---|---|
| Stay heads-down | Warmth −2 |
| Take a moment with me | Warmth +2 |
| Quick acknowledgment, then back to it | Warmth 0 |

**Q6 — Challenge** · *skinnable (mild)*
"When you suggest something I think won't work — do you want me to say so
plainly, even if you push back? Or treat it as your call and go with it?"

| Option | Effect |
|---|---|
| Say so plainly | Challenge +2 |
| My call, go with it | Challenge −2 |
| Flag it once, then let it go | Challenge 0 |

**Q7 — Initiative + Challenge** · *skinnable (mild)*
"If you're clearly heading the wrong way — what do you want from me? Stop you
and steer, nudge you with a question, or stay quiet and let you find out
yourself?"

| Option | Effect |
|---|---|
| Stop and steer | Initiative +2, Challenge +2 |
| Nudge me with a question | Initiative −2, Challenge +2 |
| Let me find out myself | Initiative −2, Challenge −2 |

**Q8 — Depth + Breadth** · *skinnable (strong)*
"When I finish digging into something for you — what's the ideal hand-off? Just
the answer, the full write-up with every angle, or the answer plus the main
alternatives kept short?"

| Option | Effect |
|---|---|
| Just the answer | Depth −2, Breadth −2 |
| Full write-up, every angle | Depth +2, Breadth +2 |
| Answer plus main alternatives, short | Depth −2, Breadth +2 |

**Q9 — Rationale + Warmth** · *tone-only*
"When I disagree with you — which sounds right? 'Here's why that won't work,'
crisp and to the point — or 'I might be wrong, but I'd think twice here, can we
look together?'"

| Option | Effect |
|---|---|
| Crisp and to the point | Rationale +2, Warmth −2 |
| Let's look together | Rationale 0, Warmth +2 |
| Just 'I'd reconsider that,' I trust you | Rationale −2, Warmth 0 |

## Domain buckets

The confirmed "your field" background answer maps to one bucket; **generic** is
the fallback: `software/technical` · `writing/content` · `data/analysis` ·
`design/creative` · `business/ops` · `generic`.

## Domain variants (worked examples)

Only Q1, Q6, Q7, Q8 are skinnable; Q2–Q5, Q9 are tone-only. **Equal-stakes
rule:** every variant of a question must hold the same risk/weight — the
substituted example never raises or lowers the stakes of the choice.

**Q8** (natural fit):

| Bucket | Skinned opener |
|---|---|
| software | "When I finish looking into something for you — a bug, a library choice…" |
| writing | "When I finish researching something for you — background, a fact-check…" |
| data | "When I finish an analysis for you…" |
| generic | "When I finish digging into something for you…" |

**Q1** (equal-stakes is load-bearing — the "next step" stays small and
reversible in *every* variant):

| Bucket | Skinned phrase |
|---|---|
| software | "…a half-written function, and I spot an obvious cleanup you didn't ask for…" |
| writing | "…a half-drafted section, and I spot an obvious tightening you didn't ask for…" |
| generic | "…something half-finished, and I spot an obvious next step you didn't ask for…" |

Full variant tables for all four skinnable questions are copywriter work — this
shows the pattern and the guardrail.

## Scoring

- Each dial starts at **5** (neutral). Final value clamped to **0–10**.
- **Each dial resolves by one of two paths:**
  - **Inferred** — Step 6 gave a high-confidence estimate; user confirms/nudges
    in Step 7; the confirmed number is the value.
  - **Scored** — estimate was medium/low; both of that dial's questions are
    asked; value = 5 + the two deltas.
- **Combo questions (Q7/Q8/Q9):** asked if *either* dial is on the Scored path.
  Apply the delta only to Scored dials; discard it for any Inferred dial.
- **Class / subclass derivation** (direction-aware, bipolar):
  - For each dial, **distance from neutral** = |value − 5|.
  - **Class** = the dial with the greatest distance; value ≥ 5 → that axis's
    high-pole class, value < 5 → its low-pole class (see `class-map.md`).
  - **Subclass** = the dial with the second-greatest distance, if that distance
    ≥ 1.5; direction-aware. Otherwise class only.
  - **Wildcard** = no dial reaches distance 1.5.
  - **Tie** for greatest distance → ask the user to pick.

## Coverage check

| Dial | Questions |
|---|---|
| Initiative | Q1, Q7 |
| Depth | Q2, Q8 |
| Breadth | Q3, Q8 |
| Rationale | Q4, Q9 |
| Warmth | Q5, Q9 |
| Challenge | Q6, Q7 |
