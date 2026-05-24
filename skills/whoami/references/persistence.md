# whoami — Persistence

How `whoami` stores its results. Three artifacts, one source of truth.

## Artifacts

| Artifact | Role | Shareable? |
|---|---|---|
| `whoami-profile.md` | Source of truth — portable profile | Yes |
| Runtime memory entry | What the local agent reads each session to calibrate | No (local) |
| HTML character sheet | Dated visual view for the user | Yes |

The profile is canonical. The memory entry and HTML are both **derived from
it** — generate the profile first.

## Regeneration vs. rerun

The profile being canonical means two operations stay distinct:

- **Rerun** (`/whoami rerun`) — runs the interview again, re-derives everything
  (dials, class, specializations, summary), and **overwrites**
  `whoami-profile.md`. A rerun resets — the new results win.
- **Regenerate** — re-renders the artifacts (HTML sheet, memory entry) from the
  **existing** `whoami-profile.md` with no interview. It mirrors the stored
  values exactly: the saved summary verbatim, the saved `flexible_traits`
  verbatim, the saved dials and class. It never re-derives and never edits the
  profile. It never rewrites, expands, or "improves" the stored summary — even
  if that summary is sparse or does not match the summary guidance below. The
  summary-authoring guidance governs *authoring* a summary on a Fresh run or
  Rerun; a Regenerate only renders what is already stored.

Because Regenerate is a pure mirror, an **empty specializations section is
correct output** when the profile's `flexible_traits` is genuinely `[]`. The
empty state faithfully reflects the profile — it is never a fallback for
"couldn't find them." The bug to guard against is the opposite: a sheet that
shows data the profile lacks, or drops data the profile holds.

**Regenerate requires the canonical profile.** Regenerate renders only from
`whoami-profile.md`. If that file does not exist, Regenerate **stops** and
renders nothing — it does not fall back to the `user`-type memory entry, a
snapshot, or any other source. Tell the user the canonical profile is missing
and that `/whoami` or `/whoami rerun` will build it. The reason it must stop
rather than improvise: a non-canonical source carries no structured
`flexible_traits`, so the Specializations section silently collapses to empty —
the exact "drops data the profile holds" failure named above. A partial sheet
is not an acceptable degradation; stopping is.

## The portable profile — `whoami-profile.md`

YAML frontmatter (machine-readable) + plain-prose body (the summary — shared
verbatim with the HTML report).

**The summary is the agent talking to the user.** Write it in the second
person, as one collaborator describing how the two of you work together — it
reads the user ("You think in routes...") and states the agent's own side of
the deal ("...I'd rather propose and wait than move on my own"), in one warm,
conversational voice.

- **Interpret the dials; never recite them.** Characterize how the person
  works — do not name dial values or tag them in parentheses ("(Breadth 9)").
  The dials have their own section on the sheet; the summary turns those six
  numbers into a human read, it does not echo them.
- **Conversational prose, no bold anchors.** Flowing paragraphs, no bolded
  scan-phrases — bolding re-imposes the spec-sheet feel the summary exists to
  avoid. Let the voice carry it instead.
- **About three short paragraphs**, lean. A loose arc — how they approach a
  decision → how to deliver to them → how they handle disagreement — not a
  rigid one-facet-per-paragraph template.
- **No bio recitation.** Don't open with a job title or résumé line; let the
  characterization carry who the person is.

The test: read it back as if briefing a new teammate on this person out loud.
A person talking → it lands. A parameter dump → it doesn't.

See `templates/profile-template.md` for the skeleton.

Only profile data lives here — never volunteered sensitive facts, never secrets.
The portable profile is sensitive-free **by construction**, so sharing it is
always safe.

## Anti-patterns — seed here, grow in feedback-memory

The `anti_patterns` field holds agent failure modes to avoid (e.g. "buries the
answer", "relitigates after I've decided"), captured by the anti-patterns
question in Step 4. whoami **seeds** 2–3 from the interview; they ride in the
portable profile and in the `user`-type memory entry, so they are consulted
every session.

The *living* set grows beyond whoami: as real misfires surface in everyday
work, they accrue as standard `feedback`-type memories through the runtime's
normal memory mechanism. whoami does not own that long tail — it only seeds the
start. A rerun re-elicits and resets the profile's `anti_patterns`; the
`feedback`-type memories accrue independently between runs.

## Runtime memory contract

Capability-gated — detect the runtime's memory mechanism; never hardcode paths.

1. **Structured memory system present** (memory directory + index) → write one
   `user`-type entry + one index line.
2. **Only `CLAUDE.md` / `AGENTS.md` present** → append one clearly-delimited
   `whoami` block.
3. **Neither** → the portable profile is the only persistence; tell the user.

The portable profile is always written, regardless of path.

**The `user`-type entry** holds the collaboration profile only — prose summary,
six dial values, class/subclass, flexible traits, anti-patterns — plus the
framing line:

> *Self-reported snapshot from a whoami session on <date> — a prior, not a
> verdict. Calibrate from it, but follow live behavior when it contradicts;
> flag the mismatch and offer to revise.*

**The index line** (~150-char budget) carries compressed scores so calibration
is always in context without opening the file:

`- [whoami profile](user_whoami_profile.md) — Loremaster/Duelist · Init7 Depth9 Breadth5 Rat8 Warm4 Chal8 · 2026-05-23`

On a re-run, find the existing entry and index line and update them **in
place** — never duplicate.

## Global persistence — `~/.claude/CLAUDE.md` (opt-in)

The runtime memory contract above persists the profile where the *current*
runtime auto-loads it — but that target is often workspace- or project-scoped
(a Cowork space, one project's `./CLAUDE.md`). For a profile that should
calibrate **every** session regardless of project, there is one more target:
the user-global `~/.claude/CLAUDE.md`, which Claude Code loads into every
session.

After persisting the profile, **offer** — never silently — to add a condensed
whoami block there:

> "Want this loaded into every Claude Code session, not just this workspace? I
> can add a short profile block to your global `~/.claude/CLAUDE.md`."

On an explicit yes:

- **Condensed, not the whole profile — compact for *signal*, not bone-terse.**
  `~/.claude/CLAUDE.md` is re-sent as input every turn, so the block stays
  compact: class + subclass; the six dials, each as **one substantive line**
  carrying its behavioral nuance (not a bare number or a 6-word tag); the
  **specializations** as a single line, with a short note on what they imply
  (assumed expertise level, how to deliver); and the anti-patterns. Leave out
  the YAML frontmatter (machine metadata) and the prose summary (it restates
  the dials) — both stay in the portable `whoami-profile.md`. The block must be
  **self-sufficient** — an agent reading only `CLAUDE.md` is fully calibrated;
  a pointer to the full profile is optional, useful only where a readable copy
  exists.
- **Delimit it.** Wrap the block in `<!-- whoami:start -->` …
  `<!-- whoami:end -->` so a re-run or correction updates it **in place**
  (find the delimiters, replace between them — never append a second block),
  and the user can find or delete it.
- **Touch nothing else.** Create `~/.claude/CLAUDE.md` if absent; if present,
  leave every other line untouched.
- **Confirm before writing.** This edits the user's global config — show the
  exact block and require an explicit yes, the standard `coding-rules` uses
  for its `CLAUDE.md` install. A decline ends it; do not re-ask.

Capability-gated. `~/.claude/CLAUDE.md` is Claude Code's user-global memory
file — reachable when the skill runs in Claude Code. If `~/.claude/` is
**outside the skill's reachable file scope** (e.g. a Cowork session connected
to a project folder, not the home directory), the skill cannot write the file
directly: do **not** request `~/.claude/` as a directory — it is
application-internal — instead show the user the exact block and a one-line
instruction to paste it into `~/.claude/CLAUDE.md` themselves. If the runtime
exposes a different global-memory location, target that. If it exposes none,
skip the offer rather than inventing a path.

Block shape:

    <!-- whoami:start -->
    ## How I work with AI — whoami profile · <Class> / <Subclass>

    - Initiative <n> — <when to act vs. check in>
    - Depth <n> — <how much detail; how to deliver it>
    - Breadth <n> — <options + trade-offs vs. a single recommendation>
    - Rationale <n> — <how much working / confidence to show>
    - Warmth <n> — <tone>
    - Challenge <n> — <how hard to push back, and when to stop>
    - Strengths — <specializations + values>; <what they imply>
    - Avoid — <2–3 anti-patterns>
    <!-- whoami:end -->

Only profile data goes in the block — sensitive-free by construction, like the
portable profile.

## Importing an existing profile

A profile built in one runtime does not automatically appear in another. Each
runtime has its own memory store, and the skill **cannot autonomously reach**
another runtime's store, another workspace's store, or `~/.claude/CLAUDE.md` —
those are outside its file scope. Cross-runtime transfer is therefore always
**user-mediated**: the user hands over a profile they already have — pasted in,
or as a file in a folder the skill can read — and the skill parses it.

Offer the import whenever Step 2 finds no local data, before the cold interview.
Two formats are accepted:

- **Full `whoami-profile.md`** — full-fidelity. The YAML frontmatter carries the
  six dials, class/subclass, `flexible_traits`, `anti_patterns`, and background;
  the body carries the prose summary. Reconstruct the dials, traits,
  anti-patterns, background, and summary verbatim. Re-derive class/subclass from
  the imported dials; if the stored class label disagrees (a hand-edited or
  older-version file), trust the derivation and flag the drift.
- **Condensed `<!-- whoami:start -->…<!-- whoami:end -->` block** — the block a
  Claude Code user has in their `~/.claude/CLAUDE.md`. It carries the six dials,
  the specializations (the `Strengths` line), and the anti-patterns (the
  `Avoid` line) — reconstruct those verbatim. Re-derive class/subclass from the
  dials (the block prints a class label too, but the dials are authoritative);
  flag any mismatch. It does **not** carry the prose summary (omitted by
  design): re-author it from the dials per the summary guidance above. Fill
  background only from what the user states.

Imported values are a **prior, not a verdict** — exactly like inferred ones.
Show them in Step 7 and have the user confirm or nudge each before anything is
stored; an import skips the cold elicitation, never the confirmation. Once
confirmed, persist normally — a fresh canonical `whoami-profile.md`, memory
entry, snapshot, and HTML sheet for *this* runtime.

Do not parse the HTML character sheet as an import source — it is rendered
output, lossy to reverse. The canonical `whoami-profile.md` and the condensed
block are the only supported import formats.

## Snapshots & versioning

Each run writes a dated snapshot; the canonical profile is always a copy of the
latest.

- `snapshots/whoami-profile-<date>.md` — the profile from that run
- `snapshots/whoami-<date>.html` — the character sheet from that run
- `whoami-profile.md` — canonical; overwritten in place to match the newest
  snapshot

The memory index points **only** to the canonical entry — never to a snapshot —
so the agent never calibrates from stale data. Snapshots exist for the user's
history and diffing.

## Where things live

User data, not skill source — never in `skills/whoami/`. Reference layout for a
typed-memory runtime:

    <memory-store>/
      MEMORY.md                          # index — gets the whoami line
      user_whoami_profile.md             # the user-type memory entry
      whoami/
        whoami-profile.md                # canonical portable profile
        snapshots/
          whoami-profile-2026-05-23.md
          whoami-2026-05-23.html

The HTML character sheet is also emitted to the user's working/output location
so they can open it. Exact paths are runtime-dependent — detect, don't assume.

## Data handling at the storage layer

- The portable profile and HTML are **shareable** — only profile data + safe
  background (role, field, AI experience, use-cases, language). Never protected
  attributes, never secrets.
- Volunteered sensitive facts the user asked to keep → written as **separate,
  standard `user`-type memories** (with confirmation), not into the whoami entry
  or the portable profile.
- Secrets (SSNs, bank/account numbers, passwords, government IDs) → never
  written to any artifact. Full policy in `background-questions.md`.

## handshake handoff

`handshake` reads `whoami-profile.md` (frontmatter dials + background) to
pre-fill its core questions. The frontmatter is the stable contract — keep
`schema_version` accurate so `handshake` can detect format changes.
