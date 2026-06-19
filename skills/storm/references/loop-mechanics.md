# Loop mechanics

The procedural detail behind the SKILL.md core loop. Loaded on demand — keep SKILL.md lean.

## Perspective discovery (standalone, no seed)

When no perspectives are supplied, discover them instead of inventing them:

1. **Survey adjacent material.** One retrieval pass on the topic to surface how it is *framed* — the recurring stakeholder groups, expert disciplines, and angles that appear across sources (this is STORM's "survey related articles" move).
2. **Name distinct lenses.** Extract 3–4 perspectives that genuinely differ in what they care about. Distinctness is the test: two perspectives that would ask the same questions are one perspective. Examples of axes that produce real difference: *practitioner vs. researcher*, *proponent vs. skeptic*, *economic vs. ethical*, *incumbent vs. challenger*.
3. **Bound.** Cap at `max_perspectives` (default 4). Fewer is fine when the topic is narrow; state the count up front.

A fixed generalist set is one valid seed, never the only option — discovery beats a hardcoded roster when the topic is unfamiliar.

## Seeded perspectives (hand-off)

When a caller supplies perspectives (e.g. `team-composer`'s active roles), use them verbatim — they are already domain-relevant lenses chosen for this problem. Do **not** re-discover or "improve" them; that throws away the caller's context. Just run Phase 2 against them.

## Per-perspective Q&A

For each perspective, up to `max_turns_per_perspective` (default 3) question→retrieve→answer cycles:

- **Generate questions in the lens's voice** — what would *this* perspective most want to know? A skeptic asks for disconfirming evidence; a practitioner asks "does it work in the field?"; a researcher asks about method and sample.
- **Answer via retrieval**, capability-gated (see SKILL.md). Each answer records its source(s).
- **Stop early** when a perspective's questions are answered or retrieval stops yielding new signal — don't burn turns to hit the cap.
- **Empty retrieval** → record `[unverified / reasoning-only]`, never confident filler.

Total retrieval budget is bounded: `max_perspectives × max_turns_per_perspective` cycles. This is the acceptance-check ceiling — do not exceed it.

## Curation → outline

- **Cluster** findings that answer the same underlying question across perspectives.
- **Dedupe sources** — the same URL/document cited by three perspectives is one source, counted once, but note which perspectives leaned on it (concentration is a bias signal — see `honesty-rubric.md`).
- **Draft structure** for the chosen output format (briefing vs report).

The source→claim map is carried through unchanged — curation reorganizes, it never detaches a claim from its source.

## Contradiction-map pass (rigor, on by default)

A short structured artifact, three buckets:

- **Clashes** — where perspectives disagree, with the source each side cites. A clash backed by sources on both sides is a real tension to surface; a clash where one side is `[unverified]` is a confidence gap, not a tension.
- **Consensus** — what all perspectives agree on (and whether the agreement is independently sourced or all tracing to one source — the latter is weaker than it looks).
- **Blind spots** — what *no* perspective addressed. Often the most useful output; name it explicitly as an open question.

## Knobs summary

| Knob | Flag | Default | Maps to (STORM) |
|---|---|---|---|
| Max perspectives | `--max-perspectives N` | 4 | `max_perspective` |
| Max turns / perspective | `--max-turns N` | 3 | `max_conv_turn` |
| Output = long report | `--report` | off (briefing) | article form |
| Skip rigor passes | `--no-rigor` | off (rigor on) | — |

Two knobs only. Do not clone the reference implementation's full knob-set — that is the over-build trap the skill deliberately avoids.
