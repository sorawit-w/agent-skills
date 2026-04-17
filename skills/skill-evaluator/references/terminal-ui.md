# Terminal-Friendly Output Rules

The findings report is markdown, but many readers will consume it through `cat`, `less`, `grep`, a plain-text PR diff, or an IDE preview with weak rendering. The rules below keep the output readable and scannable in all of those — while still rendering cleanly as markdown.

Apply these rules to:

- The findings report (primary output)
- Per-test assertion listings printed during Phase 3/4
- Any status updates during a long eval run

## Core rules

### 1. Width budget

- Prose: hard-wrap at **80 columns**.
- Tables: total width ≤ **100 columns**. Narrower is better.
- Code blocks / diffs: ≤ **80 columns**. Terminals don't wrap code gracefully.

If a value won't fit in its column, truncate with `…` rather than letting the column expand.

### 2. ASCII-first status symbols

Use these as default. A Unicode variant may be offered if the user asks, but never default to emoji or box-drawing.

| State | ASCII | Unicode (opt-in) |
|-------|-------|-------------------|
| Pass | `[x]` | `✓` |
| Fail | `[ ]` | `✗` |
| Unclear | `[?]` | `?` |
| Warning | `(!)` | `⚠` |
| Info | `(i)` | `ℹ` |

Put the status symbol at the **start** of the line, before the tag, so the eye catches it first:

```
[ ] [SHUTDOWN] Test 3 — executor did not invoke the shutdown ritual
[x] [SHUTDOWN] Test 5 — shutdown ritual executed in final step
[?] [ENV-PLACEHOLDER] Test 2 — output did not mention .env.example at all
```

### 3. Grep-friendly leading tags

Every line a user might want to grep for starts with a recognizable tag:

- `[SKILL]`, `[RUBRIC]`, `[BRIEF]`, `[FIXTURE]` — fix-layer classification
- `[TAG]` — the assertion tag
- `FINDING N` — finding headers
- `TOTAL:` — summary lines

Result: `grep '^\[SKILL\]' report.md` returns all skill-text issues in one shot.

Keep tag names **ALL CAPS** and **short** (≤12 chars). Don't pluralize — `[SKILL]` not `[SKILLS]`.

### 4. No bold-as-structure

Terminals render `**bold**` as literal asterisks. Use headers (`##`, `###`) or leading tags for hierarchy. Inline `**bold**` is fine sparingly for emphasis within prose — but never load-bearing.

### 5. Bullets: `-` only

Do not mix `*`, `+`, `-`, or `•`. Use `-` consistently. Some terminals render other glyphs inconsistently, and mixed glyphs break visual scanning.

### 6. Tables: narrow, fixed, truncated

- Column titles ≤ 10 chars where possible
- Right-align numbers, left-align text
- Truncate test names with `…` at a fixed width

Good:

```
| Test           | Pass | Fail | ? |
|----------------|-----:|-----:|--:|
| happy-path-1   |    4 |    0 | 0 |
| edge-case-2    |    3 |    1 | 0 |
| adj-non-mat…   |    2 |    2 | 0 |
```

Bad:

```
| Test case name that goes on for a while | Pass count | Fail count | Unclear count |
```

### 7. One-line section leads

Every section under `##` or `###` starts with a one-sentence summary before any list or table. Skimmers read first lines.

Good:

```
## Skill text findings (actionable)

Four issues cluster in the shutdown-ritual area. Highest-priority fix first.

- FINDING 1 — ...
```

Bad:

```
## Skill text findings (actionable)

- FINDING 1 — ...
```

### 8. No emoji, no box-drawing Unicode

Emoji render inconsistently. Box-drawing glyphs (`┌`, `│`, `└`) align in monospace but break in proportional fonts (e.g., some IDE previews). Stick to `|`, `-`, `+` for table borders.

### 9. Stable, predictable ordering

- Summary section first, always
- Failed items before passed items within each section
- Skill-text findings before test-quality issues
- Within a finding, highest-priority first (by impact, not alphabetical)

Readers should find the most important thing in the top third of the file without scrolling.

### 10. Horizontal rules sparingly

`---` is acceptable between findings for visual breathing room, but don't use it as a substitute for headers. One `---` between findings is fine; three in a row is clutter.

### 11. Code fences always labeled

When showing diffs or commands, label the fence:

````
```diff
- old line
+ new line
```
````

Unlabeled fences render fine in terminals but lose syntax highlighting in IDE previews. One-word labels cost nothing.

## Quick checklist before emitting a report

- [ ] All lines ≤ 80 cols (prose) / ≤ 100 cols (tables)
- [ ] Status symbols at line start, ASCII-default
- [ ] Leading tags on findings and summary lines
- [ ] Bullets are all `-`
- [ ] No emoji, no box-drawing Unicode
- [ ] Section leads with a one-sentence summary
- [ ] Failed items ordered before passed; skill findings before test-quality issues
- [ ] Code fences labeled

If any box is unchecked, the report is not yet terminal-clean.

## Anti-patterns

- **Emoji as status indicators** (`✅❌🤔`) — inconsistent rendering, not grep-friendly
- **Wide tables with descriptive column titles** — wraps horribly in 80-col terminals
- **Bold as the only differentiator between section types** — invisible in `cat` / `less`
- **Lines > 100 cols in prose** — hard to read in narrow terminals
- **Unlabeled horizontal rules every few lines** — visual noise
- **Mixed bullet glyphs** — breaks scanability

## One toggle worth considering later

Offer a `--unicode` or `--rich` flag that swaps ASCII symbols for the Unicode variants (✓ ✗ ?) and allows emoji for status icons. Default stays ASCII. Don't ship this toggle in v1 — the one-output-two-readers approach is simpler and almost as good.
