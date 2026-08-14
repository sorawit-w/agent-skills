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

Read `~/.claude/CLAUDE.md`. Look for two things:

| Look for | Meaning |
|---|---|
| One line starting `<!-- plain-english:start` | Already installed. Go to **Update**. |
| **Two or more** lines starting `<!-- plain-english:start` | Duplicate blocks. Go to **Damaged states** below. Do not install on top. |
| A start marker with **no** `<!-- plain-english:end -->` after it | Broken block. Go to **Damaged states** below. Do not replace anything. |
| A `## Communication style` heading, or any hand-written section of plain-language rules | A hand-written version exists. It must be **replaced**, not joined. |

The hand-written section is the common case for anyone who already tried to fix
this by hand. Two overlapping rule sets can disagree, and the agent will follow
whichever it likes better. One rule set, always.

If the file does not exist, that is fine — it gets created.

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

1. **Find the installed block.** Match on the **prefix** `<!-- plain-english:start`,
   not the whole line. An older block has a different version in that line and
   would not be found by an exact match.
2. **Read its version** from that line. Compare against the current version in
   [rule-block.md](rule-block.md).
3. **Same version** — say so and stop. Nothing to do.
4. **Older version** — show what changed between the installed block and the
   current one, then ask for an explicit yes as in Step 2.
5. **On yes** — first run the delimiter guard in **Damaged states** below. Only
   if both markers are present, replace everything between
   `<!-- plain-english:start` and `<!-- plain-english:end -->` with the current
   block. Never append a second block.

A block with no version marker at all is a hand-written or pre-v1 copy. Treat
it as older.

---

## Damaged states

Every replace and remove in this file is written as "everything between the two
markers". That phrase only has a meaning when **both** markers are there. These
three states break that assumption. Check for them before any write.

| State | What you must do |
|---|---|
| Start marker present, **end marker missing** | **Stop. Do not write.** Do not read "between the markers" as "from the start marker to the end of the file" — that deletes every section below the block. Show the user the region you found, say the end marker is missing, and ask whether to treat the block as ending at the next `## ` heading or to leave the file alone. Never guess the extent. |
| **Two or more** start markers | **Stop. Do not write.** Show the user each block with its version and its line range, and ask which one to keep. Remove the other. Do not merge them, and do not pick for the user. |
| Version marker present but unreadable (e.g. `v1.2`, `2`, empty) | Treat it as older than the current version, exactly like a block with no marker. Say which value you found, so the user can see it was not a clean install. |

**The guard applies to Update and to Uninstall.** Both delete a region defined
by the two markers, so both can destroy the rest of the file when one marker is
missing.

**Why this is written down.** These are the states the happy path quietly
assumes cannot happen. The manual-paste path in Step 4 makes the first two
likely rather than rare: the user pastes by hand, into a file the skill could
not read, with no way to check what was already there.

### Audit fixtures

Three test cases for anyone auditing this skill. Each one withholds something
the happy path assumes. Give the fixture, run `install`, `update`, and
`uninstall`, and check the expected behaviour.

| Fixture | Expected |
|---|---|
| File has `<!-- plain-english:start v1 -->` and the rules, but the `<!-- plain-english:end -->` line has been deleted | All three modes stop and ask. None writes. None deletes anything below the start marker. |
| File has two full blocks, one `v0` and one `v1`, in different places | All three modes stop, show both with line ranges and versions, and ask which to keep. |
| File has `<!-- plain-english:start 2 -->` | Treated as older than current. The unreadable value `2` is named back to the user. |

The fixture must actually withhold the resource. Supplying a well-formed block
"to be realistic" hides the exact bug these cases exist to catch.

---

## Status

Report three facts and stop. No edits, no offers unless something is out of
date.

1. Is the block installed? (Is `<!-- plain-english:start` in the file?)
2. Which version?
3. Is a hand-written `## Communication style` section also present? Say so if
   it is — that is the two-rule-sets problem, and it is worth naming.
4. Is the file in any of the **Damaged states** below? Status is read-only and
   safe, so it is the mode most likely to be run first. Report the damage here
   rather than letting Update or Uninstall meet it later.

If the installed version is older than the current one, offer the update. If
the file is out of reach, say that instead of guessing.

---

## Uninstall

Run the delimiter guard in **Damaged states** first. If either marker is
missing, or there is more than one start marker, stop and ask — do not remove a
region whose extent you had to guess.

With both markers present: remove everything from `<!-- plain-english:start`
through `<!-- plain-english:end -->`, including both delimiters. Change nothing
else.

Do not restore a hand-written section that was replaced during install — it is
gone, and guessing at what it said would be worse than leaving it out. Say
plainly that the block was removed and nothing was put back in its place.
