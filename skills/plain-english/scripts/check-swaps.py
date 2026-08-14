#!/usr/bin/env python3
"""Scan text for words the plain-english rule block bans.

The block's last rule is "read the words you actually wrote, not the ones you
meant to write". Left to prose, that check is the agent grading itself — the
exact failure this skill exists to fix. This script makes it mechanical.

The swap list is read from references/rule-block.md at run time, so the script
and the rules can never drift apart. Editing the table is the only way to
change what this checks.

What it does NOT do:

- Police the agent's live replies. Nothing can, from here — the reply is
  written after this script could run. It grades text you hand it, which makes
  it useful for rewrite-mode output and for auditing the skill.
- Catch hard words that are not in the table. The table is examples, not the
  whole rule, and that half stays a judgement call.
- Tell a quoted example from real use. Running this on the skill's own README
  reports hits, because the README prints the banned words on purpose.
- Catch every word form. The suffix window is 4 characters, so "leveraging"
  and "surfaced" are caught but "brittleness" is not. The stem is matched
  literally, so a y-to-i change ("ceremony" vs "ceremonial") is missed too.
  Widening either rule starts matching unrelated words. Both limits are pinned
  by the selftest so a later edit cannot move them by accident.

A clean result means "none of the listed words, in the forms this can see".
It does not mean the text is plain. That judgement stays with the reader.

Usage:
    python3 check-swaps.py FILE
    cat draft.md | python3 check-swaps.py -
    python3 check-swaps.py --selftest

Exit code 0 = clean; 1 = at least one banned term found; 2 = usage error.
"""
import pathlib
import re
import sys

BLOCK = pathlib.Path(__file__).resolve().parent.parent / "references" / "rule-block.md"


def load_swaps(path=BLOCK):
    """Return [(banned, replacement)] from the swap table in the rule block."""
    text = path.read_text(encoding="utf-8")
    m = re.search(r"```markdown\n(.*?)\n```", text, re.S)
    if not m:
        raise SystemExit(f"error: no fenced block found in {path}")
    rows = re.findall(r"^\| ([^|]+?) \| ([^|]+?) \|$", m.group(1), re.M)
    swaps = [(b.strip(), g.strip()) for b, g in rows if b.strip() != "Do not write"]
    if not swaps:
        raise SystemExit(f"error: swap table is empty in {path}")
    return swaps


def build_pattern(banned):
    """Compile a matcher for one table entry.

    Two things the naive version got wrong, both found by running it:

    1. A phrase wrapped across a line break ("blast\\nradius") was missed, so
       any hard-wrapped document scanned clean. Spaces match any whitespace.
    2. Inflected forms were missed — the table says "retro-fit" and the text
       said "retro-fitting". Bases of 5 characters or more allow a short
       suffix; a trailing "e" is dropped first so "surface" catches
       "surfacing". Short bases stay strict, because "rot" must never fire
       inside "protocol" or "rotates".
    """
    base = banned.replace(" (verb)", "").lower()
    core = r"\s+".join(re.escape(w) for w in base.split())
    if len(base) >= 5:
        core = core[:-1] if core.endswith("e") else core   # surface -> surfac
        return re.compile(r"(?<!\w)" + core + r"\w{0,4}(?!\w)")
    return re.compile(r"(?<!\w)" + core + r"(?!\w)")


def scan(text, swaps):
    """Return [(banned, replacement, line_no, excerpt)] for every hit."""
    lowered = text.lower()
    starts = [0]
    for i, ch in enumerate(text):
        if ch == "\n":
            starts.append(i + 1)

    hits = []
    for banned, good in swaps:
        for m in build_pattern(banned).finditer(lowered):
            line_no = sum(1 for s in starts if s <= m.start())
            excerpt = " ".join(text[m.start():m.start() + 72].split())
            hits.append((banned, good, line_no, excerpt))
    return sorted(hits, key=lambda h: (h[2], h[0]))


def selftest():
    swaps = load_swaps()
    def names(text):
        return sorted({h[0] for h in scan(text, swaps)})

    dirty = "The blast radius is large and it will bite you later.\nWe should close the loop."
    assert names(dirty) == ["blast radius", "close the loop", "it will bite you"], names(dirty)

    clean = "This affects a lot. It will cause problems later.\nWe should finish this."
    assert names(clean) == [], f"clean text produced hits: {names(clean)}"

    # a phrase split by a hard line wrap must still be caught
    wrapped = "The change has a large blast\nradius, so be careful."
    assert names(wrapped) == ["blast radius"], f"line-wrap leak: {names(wrapped)}"

    # inflected forms of a long base must be caught
    inflected = "Retro-fitting it while leveraging the old path oscillates badly."
    assert names(inflected) == ["leverage", "oscillate", "retro-fit"], names(inflected)

    # ...but a short base must NOT bleed into unrelated words
    tricky = "The protocol rotates the token. The rotation is fine."
    assert names(tricky) == [], f"short-base leak: {names(tricky)}"

    # short suffixes on a stem are caught: "surfaced", "surfacing", "leveraged"
    assert names("We are surfacing the leveraged paths.") == ["leverage", "surface (verb)"]

    # TWO KNOWN LIMITS, pinned deliberately so a later edit cannot quietly
    # widen or narrow them. Both are stated in the module docstring.
    #
    # 1. The suffix window is 4 characters. "brittleness" (+5) slips past.
    #    Widening it starts matching unrelated words.
    assert names("The brittleness metric is high.") == [], "suffix window changed"
    # 2. The stem is literal, so a y->i change breaks the match:
    #    "ceremony" does not catch "ceremonial" or "ceremonies".
    assert names("A ceremonial review of the ceremonies.") == [], "stem rule changed"

    print(f"selftest OK — {len(swaps)} swap rows loaded from {BLOCK.name}")
    print("  covers: phrases, line-wrapped phrases, inflected forms,")
    print("          short-base guard, pinned 4-char suffix limit")
    return 0


def main(argv):
    if len(argv) != 2:
        print(__doc__.strip().split("Usage:")[1].strip(), file=sys.stderr)
        return 2
    if argv[1] == "--selftest":
        return selftest()

    src = argv[1]
    text = sys.stdin.read() if src == "-" else pathlib.Path(src).read_text(encoding="utf-8")
    swaps = load_swaps()
    hits = scan(text, swaps)

    if not hits:
        print(f"clean — no banned terms ({len(swaps)} rows checked)")
        return 0

    print(f"{len(hits)} banned term(s) found:\n")
    for banned, good, n, line in hits:
        print(f"  line {n}: {banned!r} -> write {good!r}")
        print(f"    {line[:72]}")
    print(f"\nThe list is examples, not the whole rule. Hard words that are not")
    print(f"on it still need swapping — this script cannot see those.")
    return 1


if __name__ == "__main__":
    sys.exit(main(sys.argv))
