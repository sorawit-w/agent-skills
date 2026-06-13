# Styles — presets, channel defaults, free-form interpretation

Shipped presets for ghostwriter's `style` argument. Load only the section you need. Every preset is an **overlay on the user's voice** (sign-offs, emoji norms, rhythm persist), and the SKILL.md ban list applies to all of them — including the examples below.

Each preset follows the same schema. Free-form styles are interpreted into this schema in-place; "save this style" writes a section in this exact shape to `~/.claude/ghostwriter/styles-custom.md`.

> **Schema:** Purpose · Register knobs (formality / warmth / sentence shape / emoji) · Signature moves · Failure mode · Example
>
> All examples share one scenario — telling someone the deploy slipped to Thursday — so registers are directly comparable.

---

## `formal`

- **Purpose:** professional register for clients, strangers, executives, first contact. Human-formal, NOT AI-formal — the ban list fully applies.
- **Register knobs:** formality high · warmth moderate · complete sentences, moderate length · no emoji.
- **Signature moves:** real greeting with the recipient's name; states the point in the first or second sentence; commits to a concrete follow-up.
- **Failure mode:** drifting into corporate-newsletter voice. "Per my last email" ceremony, hedge-balance constructions, warmth openers. Formal means careful, not stiff.
- **Example:** "Hi Sarah, quick update on the release. We found a data migration issue this morning and decided to move the deploy to Thursday rather than risk a partial rollout. I'll confirm as soon as it's live."

## `friend`

- **Purpose:** casual register for close coworkers and actual friends.
- **Register knobs:** formality low · warmth high · fragments welcome, short · emoji per the user's observed habit.
- **Signature moves:** contractions, shorthand, lowercase if the user's samples show it; gets to the point with zero ceremony; humor allowed where the user's samples show it.
- **Failure mode:** performed casualness — slang the user never uses, forced memes, or flawless punctuation undermining the register (a typo-free, perfectly capitalized "casual" message reads as AI).
- **Example:** "heads up, deploy slipped to thursday 😅 migration bug, didn't want to yolo it. will ping you when it's out"

## `direct`

- **Purpose:** blunt, information-first updates for people who hate fluff. Status updates, quick asks, busy recipients.
- **Register knobs:** formality neutral · warmth low-but-not-cold · short declaratives, fragments fine · no emoji unless the user's habit.
- **Signature moves:** the news in sentence one; reason in sentence two; next step in sentence three; done. No greeting if channel norms allow.
- **Failure mode:** rudeness. Direct cuts ceremony, not respect — no softeners is the point, but no acknowledgment of impact reads as hostile in bad-news contexts (use `diplomatic` there).
- **Example:** "Deploy's moving to Thursday. Migration bug, not worth the risk. Will confirm when live."

## `diplomatic`

- **Purpose:** softened but honest. Bad news, declines, escalations, mixed or senior audiences where the relationship matters as much as the message.
- **Register knobs:** formality medium-high · warmth high · fuller sentences, moderate length · no emoji unless the user's habit.
- **Signature moves:** flags the news early rather than burying it; names the impact on the recipient; gives the honest reason; offers a concrete opening to discuss. Honesty stays intact — diplomatic softens delivery, never the facts.
- **Failure mode:** mush. So much cushioning the recipient can't find the message, or hedge-balance constructions that read as AI. The news must still land in the first two sentences. On casual channels, diplomatic does NOT license extra length — a Slack decline still fits the channel cap (≤4 lines); soften with word choice, not added sentences.
- **Example:** "Wanted to flag this early rather than surprise you: we hit a migration issue and I'd rather move the deploy to Thursday than ship something we're not confident in. I know the timing isn't great, so happy to talk through the impact if it causes problems on your side."

## `storybook`

- **Purpose:** narrative, vivid, personality-forward. *Genre-leaning preset:* announcements, launch posts, team farewells — pieces with an audience, not replies in a thread.
- **Register knobs:** formality low-medium · warmth high · varied sentence shapes, rhythm matters · emoji sparing.
- **Signature moves:** opens with a scene or small story instead of a statement; personifies the situation; lands on a genuine note (gratitude, pride, relief), not a moral.
- **Failure mode:** whimsy where gravity is owed (incidents, layoffs, anything with real harm), or stretching a two-line update into a saga. If the content is thin, this is the wrong preset.
- **Example:** "So, our deploy met the database migration this morning, and they did not get along. After a brief standoff we've decided everyone needs until Thursday to cool off. The good news: nothing broke, nobody panicked, and Thursday's version will be the one we're actually proud of."

## `eli5`

- **Purpose:** explain something difficult in terms a non-expert immediately gets. *Genre-leaning preset:* explanation mode ("explain like I'm 5"), layered onto whatever relationship the message has.
- **Register knobs:** formality follows the relationship · warmth moderate · short sentences, plain words · no emoji unless the user's habit.
- **Signature moves:** one concrete analogy from everyday life carries the whole explanation; no jargon, no acronyms without unpacking; ends with the practical consequence for the recipient.
- **Failure mode:** **condescension.** The analogy treats the *concept* as new, never the *person* as a child. No "imagine you're five", no exclamation-mark cheerfulness, no over-simplifying things the recipient obviously knows. Condescension is also an AI tell.
- **Example:** "Think of the deploy like moving day. Everything was packed, but one box, the database, turned out to have stuff that won't fit the new shelves. We could force it and maybe break things, or take two days to repack properly. We're repacking. New move day is Thursday."

---

## Channel × relationship defaults

Cold-start table for when no sample covers the channel in play. **Samples always override this table.** Cells give: maximum length (hard cap) · greeting/sign-off norm · formality floor.

| | Close coworker | Manager | Client | Stranger |
|---|---|---|---|---|
| **Email** | 1–3 sentences · greeting optional, short sign-off | 2–4 sentences · light greeting + sign-off | 3–5 sentences · full greeting + sign-off · formality ≥ medium | 3–5 sentences · full greeting + sign-off · formality high |
| **Slack / Teams** | 1–2 lines · no greeting, no sign-off | 1–3 lines · optional "hey" · no sign-off | 2–4 lines · light greeting · formality medium | 2–4 lines · greeting · formality medium-high |
| **DM / text** | 1–2 lines · nothing ceremonial | 1–2 lines · nothing ceremonial | rare channel; mirror their last message | rare channel; mirror their last message |
| **LinkedIn** | 2–3 sentences · first-name greeting | 2–3 sentences · first-name greeting | 2–4 sentences · greeting · formality medium-high | 2–4 sentences · greeting, no flattery opener · formality medium-high |

Reading the table: pick the channel row and relationship column. The cell's length is a **hard cap** (shorter is always fine; never add sentences to reach it), its formality is a **floor** (don't get more casual than the cell, unless samples say otherwise), and the greeting/sign-off norm is the default ceremony. Apply the resolved style on top — register changes, the length cap doesn't. Conflicts resolve in this order: samples > explicit style > this table.

---

## Free-form style interpretation

When the `style` string is not a preset, not a saved custom style, and not a synonym/typo of either (snap those instead — `professional`→`formal`, `casual`→`friend`, `simple`→`eli5`):

1. Derive the four register knobs (formality, warmth, sentence shape, emoji tolerance) from the descriptor's plain meaning. "Warm but firm" → warmth high, formality medium, short declaratives for the firm part.
2. Apply as an overlay on the user's voice: their mechanics (sign-off, emoji habits, rhythm) persist except where the descriptor explicitly contradicts them.
3. The ban list still applies in full. A free-form style changes register; it never re-admits AI tells.
4. Don't announce the interpretation — the draft reveals it, and the user iterates if it's off. The interpretation is only made explicit at save-time.

If the string carries no register signal at all (`style=blue`, `style=q3-report`): ask one short question; if still unresolved, fall back to `user`.

## `styles-custom.md` contract

Saved styles live in `~/.claude/ghostwriter/styles-custom.md`, one section per style, same schema as the presets above (Purpose / Register knobs / Signature moves / Failure mode / Example — use the draft that prompted the save as the example). Custom styles resolve *before* shipped presets on exact match.

**Reserved names (refuse at save-time, offer a rename):** `polished`, `structured`, `normal`, `normally`, `default`, `ai`, `claude`, `standard` — these belong to the escape hatch and a custom style by these names would be unreachable.
