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
- Catch every word form. Three limits, all pinned by --selftest so a later
  edit cannot move them by accident:
    * endings come from a fixed list, so "surfacing" is caught but
      "brittleness" is not;
    * the stem is literal, so a y-to-i change ("ceremony" vs "ceremonial")
      is missed;
    * a multi-word entry matches exactly, so "backed out of" and "rides
      along" are missed.
  Every one of these is the price of not producing false hits. An earlier
  wildcard version caught those forms and also flagged "surfactant",
  "fixed pointer" and "close the loopback".
- Tell a verb from a noun. The table bans "surface" as a verb; this flags
  "surface tension" too. Review the hits, do not apply them blindly.

A clean result means "none of the listed words, in the forms this can see".
It does not mean the text is plain. That judgement stays with the reader.

Exit codes: 0 clean, 1 banned terms found, 2 could not run (bad usage, or a
file that does not exist or cannot be decoded). A caller that treats any
non-zero as "found terms" will misread a missing file.

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


# Endings allowed after a single-word stem. An explicit list, not a wildcard:
# an earlier version allowed any 4 word characters and matched "surfactant"
# from "surface" and "fixed pointer" from "fixed point".
# "e" is in the list because the stem has its trailing "e" stripped, so the
# base word has to be able to earn it back: "surface" is "surfac" + "e".
# Leaving it out silently stopped every e-ending entry from matching its own
# plain form, which the inflection tests did not notice.
SUFFIXES = ("e", "s", "es", "d", "ed", "ing",
            "ted", "ting", "ped", "ping", "ged", "ging")


def build_pattern(banned):
    """Compile a matcher for one table entry.

    Three things earlier versions got wrong, all found by running them:

    1. A phrase wrapped across a line break ("blast\\nradius") was missed, so
       any hard-wrapped document scanned clean. Spaces match any whitespace.
    2. Inflected forms were missed — the table says "retro-fit", the text said
       "retro-fitting". A single-word entry of 5 characters or more now allows
       one ending from SUFFIXES, after dropping a trailing "e" so "surface"
       reaches "surfacing".
    3. Those two rules together produced false hits on longer unrelated words
       and on phrases. A multi-word entry now matches exactly, and short
       entries stay strict — "rot" must never fire inside "protocol", and
       "close the loop" must never fire inside "close the loopback".
    """
    base = banned.replace(" (verb)", "")
    words = base.split()
    core = r"\s+".join(re.escape(w) for w in words)

    if len(words) == 1 and len(base) >= 5:
        stem = core[:-1] if core.endswith("e") else core      # surface -> surfac
        core = stem + "(?:" + "|".join(SUFFIXES) + ")?"
    return re.compile(r"(?<!\w)" + core + r"(?!\w)", re.IGNORECASE)


def scan(text, swaps):
    """Return [(banned, replacement, line_no, excerpt)] for every hit.

    Matching is case-insensitive on the ORIGINAL text. An earlier version
    searched `text.lower()` and applied the offsets back to `text`; characters
    whose lowercase form is longer (Turkish dotted capital I, for one) shifted
    every offset after them, so line numbers and excerpts came out wrong.
    """
    line_starts = [0] + [i + 1 for i, ch in enumerate(text) if ch == "\n"]

    hits = []
    for banned, good in swaps:
        for m in build_pattern(banned).finditer(text):
            line_no = sum(1 for s in line_starts if s <= m.start())
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

    # EVERY entry must match its own plain form. This is first because leaving
    # it out is how an e-stripped stem quietly stopped matching "surface".
    for banned, _ in swaps:
        probe = f"We should {banned.replace(' (verb)', '')} it."
        assert banned in names(probe), f"entry does not match its own form: {banned!r}"

    # endings on a single-word stem are caught
    assert names("We are surfacing the leveraged paths.") == ["leverage", "surface (verb)"]
    assert names("It surfaced once and oscillates now.") == ["oscillate", "surface (verb)"]

    # FALSE POSITIVES that an earlier wildcard version produced. Each of these
    # must stay empty; they are the reason SUFFIXES is an explicit list and
    # multi-word entries match exactly.
    for text in ("A surfactant lowers the tension.",     # surface + "tant"
                 "The fixed pointer remains valid.",     # phrase + "er"
                 "Back out often, it is fine.",          # phrase + "ten"
                 "Close the loopback route.",            # phrase + "back"
                 "It will bite younger readers."):       # phrase + "nger"
        assert names(text) == [], f"false positive returned for {text!r}"

    # ...while the real phrase still fires
    assert names("The fixed point is reached.") == ["fixed point"]

    # case-insensitive matching must not shift offsets. An earlier version
    # searched text.lower(), and a character whose lowercase form is longer
    # pushed every later offset out of place.
    tricky_case = "İİİ The blast radius is large."
    hits = scan(tricky_case, swaps)
    assert [h[0] for h in hits] == ["blast radius"], hits
    assert hits[0][2] == 1, f"line number wrong: {hits[0]}"
    assert hits[0][3].startswith("blast radius"), f"excerpt wrong: {hits[0]!r}"

    # THREE KNOWN LIMITS, pinned deliberately so a later edit cannot quietly
    # move them. All three are stated in the module docstring.
    #
    # 1. No ending in SUFFIXES reaches "brittleness".
    assert names("The brittleness metric is high.") == [], "suffix list changed"
    # 2. The stem is literal, so a y->i change breaks the match.
    assert names("A ceremonial review of the ceremonies.") == [], "stem rule changed"
    # 3. Multi-word entries match exactly, so an inflected word inside a phrase
    #    is missed. This is the price of killing the false positives above.
    assert names("She rides along and backed out of it.") == [], "phrase rule changed"

    print(f"selftest OK — {len(swaps)} swap rows loaded from {BLOCK.name}")
    print("  covers: every entry matches its own form; phrases; line-wrapped")
    print("          phrases; inflections; short-base guard; case-offset")
    print("          safety; 5 pinned false-positive cases; 3 pinned limits")
    return 0


def main(argv):
    if len(argv) != 2:
        print(__doc__.strip().split("Usage:")[1].strip(), file=sys.stderr)
        return 2
    if argv[1] == "--selftest":
        return selftest()

    src = argv[1]
    try:
        if src == "-":
            text = sys.stdin.read()
        else:
            text = pathlib.Path(src).read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        # Exit 2, never 1. Exit 1 means "banned terms found"; letting a missing
        # or unreadable file exit 1 would tell a caller the scan ran and failed,
        # when it never ran at all.
        print(f"error: cannot read {src}: {exc}", file=sys.stderr)
        return 2
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
