# whoami — Class Map

The class is a memorable **handle** for the profile — the "bonus." The agent
calibrates behavior from the six dial values (`dials.md`), **not** the class
label. Class and subclass are computed from the six fixed dials only — never
flexible traits — so they stay comparable. 12 classes (6 axes × 2 poles) +
Wildcard.

## The roster

| Class | Axis / pole | Identity | How I run with you |
|---|---|---|---|
| **Vanguard** | Initiative ▲ | "Point me at the goal and move." | Act on what's clear, report after, minimal check-ins |
| **Marshal** | Initiative ▼ | "I'll give the orders." | Propose, wait for the go-ahead, confirm before acting |
| **Loremaster** | Depth ▲ | "Give me the whole map." | Comprehensive — full context, anticipate follow-ups |
| **Oracle** | Depth ▼ | "Just the essence." | Bottom line first, cut preamble, stop when answered |
| **Pathfinder** | Breadth ▲ | "Show me the routes first." | Lay out options + trade-offs before recommending |
| **Lancer** | Breadth ▼ | "One call — commit." | A single clear recommendation, no fan of options |
| **Artificer** | Rationale ▲ | "No black boxes." | Show the working — assumptions, reasoning, how I got there |
| **Sorcerer** | Rationale ▼ | "I trust the result." | Deliver the answer, skip the derivation unless asked |
| **Bard** | Warmth ▲ | "Work with me, not at me." | Warm and personal, acknowledge effort, keep it human |
| **Sentinel** | Warmth ▼ | "All business." | Task in, result out — minimal rapport, stay on-task |
| **Duelist** | Challenge ▲ | "Don't agree — test me." | Push back, devil's advocate, stress-test your thinking |
| **Guardian** | Challenge ▼ | "Have my back." | Back your call, voice a concern once, then support |
| **Wildcard** | no dominant dial | "Read the room each time." | Calibrate per task, ask a bit more often |

## Derivation

Scoring math lives in `question-bank.md`. Summary:
- For each dial, **distance from neutral** = |value − 5|.
- **Class** = the dial with the greatest distance; direction sets the pole
  (value ≥ 5 → high class, < 5 → low class).
- **Subclass** = the dial with the second-greatest distance, if that distance
  ≥ 1.5; direction-aware. Otherwise class only.
- **Wildcard** = no dial reaches distance 1.5 (every dial within 3.5–6.5).
- **Tie** for greatest distance → the skill asks the user to pick.

## Subclass

Subclass = the second dial's pole-class as a descriptor. Format **Class /
Subclass**. Class from one axis, subclass from a different axis → 12 × 10 =
**120 combos**. Composition naming carries the meaning (*Duelist / Sentinel* =
sharp and all-business; *Sentinel / Loremaster* = all-business but wants depth).
The full per-combo blurbs live in `subclass-blurbs.md`. Wildcard never carries a
subclass.

## Default characters

13 portraits, **hi-density pixel art** — helmed, hooded, hatted, or
bare-faced character busts with shade ramps, dithered backgrounds and a class
emblem each. Built as **6 axis-family designs + Wildcard = 7 designs**. Each
axis design has a **high and a low variant** — shared base figure (helm,
cowl, hood, hat, or face), different crest / palette / emblem — so a Vanguard
and a Marshal visibly belong to the same family. The high/low pairing makes
bipolarity visible in the portrait, echoing the lollipop chart.

Files: `assets/characters/<class>.png` (skill-local, lowercase class name,
e.g. `assets/characters/vanguard.png`) — 512×512 PNG. Each portrait is
specified by a reusable per-class prompt (style, palette, subject, headgear,
crest, emblem, mood); regenerate or restyle the set against a connected image
generator from those prompts.

The portrait on the character sheet is capability-gated: a freshly generated
pixel-art portrait when `pixel-art` + an image generator are available,
otherwise the bundled class PNG, base64-embedded inline so the sheet stays
self-contained.

## IP note

All 13 names are generic archetype words — an original roster, not lifted from
any specific game's class tree. Safe per the Gap Check (Q1, IP).
