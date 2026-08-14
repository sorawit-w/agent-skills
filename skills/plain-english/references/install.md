# plain-english — install, update, uninstall

The rules only work if they are in context on every turn. A skill body is not —
it loads when something triggers it, and "write plainly" has no trigger. So the
skill does not enforce the rules. It **installs** them, and then the user can
forget the skill exists.

The target is `~/.claude/CLAUDE.md`, the user-global memory file Claude Code
re-sends as input on every turn.

**Precedent.** This follows the contract already written in
[`../../whoami/references/persistence.md`](../../whoami/references/persistence.md)
§ *Global persistence — `~/.claude/CLAUDE.md` (opt-in)*: a delimited block,
shown before it is written, replaced in place, with everything else in the file
left untouched. Read that section if anything here is unclear. Do not invent a
second contract.

---

## Install

### Step 1 — Detect

Read `~/.claude/CLAUDE.md`, then run the **[Structure check](#structure-check)**
below. Every mode runs it, and it runs **before** anything else — before reading
a version, before proposing an edit. It returns one of: `not installed`,
`healthy`, or a damaged state that stops the run.

If the file does not exist, that is `not installed` — fine, it gets created.

On `healthy`, this is an update, not an install: go to **Update**.

On `not installed`, also look for a hand-written version:

| Look for | Meaning |
|---|---|
| A `## Communication style` heading, or any other hand-written section of plain-language rules | A hand-written version exists. It must be **replaced**, not joined. |

The hand-written section is the common case for anyone who already tried to fix
this by hand. Two overlapping rule sets can disagree, and the agent will follow
whichever it likes better. One rule set, always.

**Where that section ends — decide it, show it, never assume it.** The heading
tells you where it starts and nothing tells you where it stops, so:

1. Its extent runs from its heading line through the line **before** the next
   heading at the same level or higher (`## ` or `# `), or through the end of
   the file if no such heading follows.
2. That rule is a proposal, not a licence. Print the exact line range and the
   full text you intend to remove, and let the user correct the boundary.
3. If the section appears to run to the end of the file, say so explicitly and
   ask before removing — "to the end of the file" is how unrelated
   configuration gets deleted.
4. Never remove anything below a heading you did not name in step 2.

### Step 2 — Show, then ask

Print the exact change before touching anything:

- The full block from [rule-block.md](rule-block.md), exactly as it will be
  written.
- If a hand-written section will be removed, print that section too, under a
  clear heading such as **"This will be removed"**.

Then ask once, plainly:

> "This edits your global `~/.claude/CLAUDE.md`. Add the block above and remove
> the section marked for removal?"

**Require an explicit yes.** A "maybe", a question, or silence is not a yes. If
the user declines, stop and do not ask again in this session.

If the user wants the block but wants to keep their hand-written section, say
plainly that two overlapping rule sets will disagree, then do what they ask.
Their file, their call.

### Step 3 — Write

- Copy the block from [rule-block.md](rule-block.md) **verbatim**. Do not
  shorten it, reword it, reorder it, or drop rows from the swap table. If the
  block seems too long, that is not a reason to trim it — the swap list is the
  part that works.
- Remove the hand-written section only if the user agreed to it.
- Create `~/.claude/CLAUDE.md` if it does not exist.
- **Change nothing else.** Every other line in that file stays exactly as it
  was.

Confirm in one line: which file changed, what was added, what was removed.

### Step 4 — When the file is out of reach

`~/.claude/` is application-internal. In some runtimes (a session connected to
a project folder, not the home directory) the skill cannot read or write it.

In that case: **do not request `~/.claude/` as a directory.** Print the block
and one line telling the user to paste it into `~/.claude/CLAUDE.md` themselves.

Tell them to search that file for `<!-- plain-english:start` **before** pasting.
If a block is already there, they should replace it rather than add a second
one. You cannot check this yourself, and a second pasted block is the most
likely way this file ends up in a damaged state.

If the runtime exposes a different global memory file, use that instead. If it
exposes none, say so rather than inventing a path.

---

## Update

Install-once has one real cost: improving the skill does not improve a copy
that is already installed. The version marker fixes that.

1. **Run the [Structure check](#structure-check) first.** Before reading a
   version, before comparing anything. A damaged file stops the run whatever
   its version says — otherwise a damaged block that happens to carry the
   current version returns "nothing to do" and the damage stays hidden.
   - `not installed` → say so and stop. Offer **Install**. Do not write.
   - a damaged state → stop, per that section. Do not write.
   - `healthy` → continue.
2. **Read its version** from the start marker line. Match on the **prefix**
   `<!-- plain-english:start`, not the whole line: an older block carries a
   different version there and an exact match would not find it. Compare
   against the current version in [rule-block.md](rule-block.md).
3. **Same version** — say so and stop. Nothing to do.
4. **Older version, unreadable version, or no version** — show what changed
   between the installed block and the current one, then ask for an explicit
   yes as in Step 2. A block with no version marker is a hand-written or pre-v1
   copy; treat it as older.
5. **Newer version than this skill ships** — stop and say so. Do not overwrite.
   This means the installed block came from a newer copy of the skill than the
   one running, so writing would be a silent downgrade. Tell the user which two
   versions you found and let them choose; update only on an explicit yes.
6. **On yes** — replace the block **from the start marker line through the end
   marker line, both included**, with the current block. Not "everything
   between the markers": the replacement text carries its own markers, so an
   exclusive reading leaves one block nested inside another. Never append a
   second block.

---

## Structure check

Every replace and remove in this file names a region by its two markers. That
only has a meaning when the markers form **exactly one ordered pair**. Run this
before any other step, in every mode, and act on what it returns.

Count `<!-- plain-english:start` lines as *starts* and `<!-- plain-english:end -->`
lines as *ends*.

| starts | ends | Result | What you must do |
|---|---|---|---|
| 0 | 0 | `not installed` | No block here. Not damage — say so plainly. Install may proceed; Update and Uninstall stop and report it. |
| 1 | 1, and the end comes **after** the start | `healthy` | The one safe case. Continue. |
| 1 | 0 | damaged | **Stop. Do not write.** Never read "between the markers" as "from the start marker to the end of the file" — that deletes every section below the block. |
| 1 | 1, but the end comes **before** the start | damaged | **Stop. Do not write.** An orphan end above the block leaves the region ambiguous in both directions. |
| 1 | 2 or more | damaged | **Stop. Do not write.** More than one candidate end means more than one candidate region. Do not take the nearest and hope. |
| 2 or more | any | damaged | **Stop. Do not write.** Duplicate blocks. |
| 0 | 1 or more | damaged | **Stop. Do not write.** An end with no start is left over from a partial edit. |

**Every damaged row ends the same way.** Show the user the marker lines you
found with their line numbers, say plainly what is wrong, and offer two choices:
repair the boundary yourself after they name it, or leave the file alone. Never
guess the extent, never merge blocks, and never pick for the user.

One state is **not** damage and must not stop anything:

| State | What you must do |
|---|---|
| Version marker present but unreadable (`v1.2`, `2`, empty) | The structure is fine. Treat the version as older than current, exactly like a block with no marker. Say which value you found, so the user can see it was not a clean install. |

**Why this is written down.** These are the states the happy path quietly
assumes cannot happen. The manual-paste path in Step 4 makes several of them
likely rather than rare: the user pastes by hand, into a file the skill could
not read, with no way to check what was already there.

### Audit fixtures

Test cases for anyone auditing this skill. Each withholds something the happy
path assumes. Give the fixture, run `install`, `update`, and `uninstall`, and
check the expected behaviour.

| Fixture | Expected |
|---|---|
| A start marker and the rules, but the `<!-- plain-english:end -->` line deleted | All three modes stop and ask. None writes. Nothing below the start marker is deleted. |
| Two full blocks, one `v0` and one `v1`, in different places | All three modes stop, show both with line ranges and versions, and ask which to keep. |
| One start marker and **two** end markers | All three modes stop. Neither candidate region is chosen. |
| An end marker **above** the only start marker | All three modes stop. |
| `<!-- plain-english:start 2 -->`, otherwise well formed | Not damage. Treated as older than current; the value `2` is named back to the user. |
| A well-formed `v1` block while the skill itself ships `v0` | Update stops rather than downgrading, and names both versions. |
| No markers at all | `update` and `uninstall` report "not installed" and write nothing. `install` proceeds normally. |
| A hand-written `## Communication style` section running to the end of the file | Install names the exact line range, says it reaches the end of the file, and asks before removing anything. |

The fixture must actually withhold the resource. Supplying a well-formed block
"to be realistic" hides the exact bug these cases exist to catch.

---

## Status

Report and stop. No edits ever, whatever you find.

1. Run the [Structure check](#structure-check) and report its result. Status is
   read-only and safe, so it is the mode most likely to be run first — report
   damage here rather than letting Update or Uninstall meet it later. Unlike
   the other modes, a damaged result does not stop Status: keep going and
   report the rest of what you can see.
2. Which version, if a start marker is there at all?
3. Is a hand-written `## Communication style` section also present? Say so if
   it is — that is the two-rule-sets problem, and it is worth naming.

Then, only if the structure is `healthy`: if the installed version is older
than the current one, offer the update. If it is newer, say so and offer
nothing. If the file is out of reach, say that instead of guessing.

---

## Uninstall

Run the [Structure check](#structure-check) first.

- `not installed` → say so and stop. Nothing to remove, and this is not damage.
- a damaged state → stop and ask, per that section. Never remove a region whose
  extent you had to guess.
- `healthy` → remove the block **from the start marker line through the end
  marker line, both included**. Change nothing else.

Do not restore a hand-written section that was replaced during install — it is
gone, and guessing at what it said would be worse than leaving it out. Say
plainly that the block was removed and nothing was put back in its place.
