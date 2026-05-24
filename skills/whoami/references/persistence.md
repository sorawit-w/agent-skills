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
  if that summary is sparse or does not meet the structure guidance below. The
  structure-first summary rules govern *authoring* a summary on a Fresh run or
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
verbatim with the HTML report). Write the summary **structure-first** so every
regeneration reads the same way:

- **At most four short paragraphs**, one facet per paragraph — roughly: who
  they are + class → the one or two defining moves → how to deliver to them →
  working style + warmth.
- **Bold the key phrase** in each paragraph (e.g. *transparency*, *bottom line
  first*) — the bold anchors are what make the summary scan in one pass, not
  brevity.
- One steady register throughout: describe the user, and give the agent plain,
  direct guidance.

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
