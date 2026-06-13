#!/usr/bin/env python3
"""Cross-platform SKILL.md frontmatter compatibility checker.

Claude Code imposes no hard limit on the `description` field, but OpenAI Codex
*silently skips* any skill whose SKILL.md violates its frontmatter rules. Since
the `description` field is shared across platforms (Codex has no per-platform
override), every skill in this repo must satisfy the stricter Codex contract.

Codex rules enforced here (a violation = skill not loaded in Codex):
  - description: 1..=1024 in LENGTH, checked as UTF-8 BYTES in the Codex Rust
    loader (str::len), not unicode chars. See openai/codex issue #7730.
  - description: must not contain '<' or '>' (angle brackets).
  - name: must match ^[a-z0-9]+(-[a-z0-9]+)*$ and be <= 64 bytes.
  - entry file must be named exactly SKILL.md (all caps).

We target a 1000-byte soft cap (LIMIT - MARGIN) so multibyte punctuation
(em-dashes, arrows) never pushes a description over the hard 1024-byte wall.

Exit code 0 = all good; 1 = at least one violation. Run from repo root:
    python3 scripts/check-skill-compat.py
"""
import glob
import os
import re
import sys

HARD_LIMIT = 1024          # Codex hard cap, in UTF-8 bytes
SOFT_LIMIT = 1000          # our authoring target, leaves multibyte headroom
NAME_RE = re.compile(r"[a-z0-9]+(-[a-z0-9]+)*$")


def parse_frontmatter(text):
    m = re.match(r"^---\n(.*?)\n---\n", text, re.S)
    return m.group(1) if m else None


def extract_field(fm, field):
    """Minimal YAML extractor for a top-level scalar or block-scalar field.

    Handles `field: value`, quoted values, and `>`/`|` block scalars — enough
    for SKILL.md frontmatter without a YAML dependency.
    """
    lines = fm.split("\n")
    for i, line in enumerate(lines):
        m = re.match(r"^(\s*)(" + re.escape(field) + r"):(.*)$", line)
        if not m:
            continue
        indent = len(m.group(1))
        rest = m.group(3).strip()
        if rest in (">", "|", ">-", "|-", "|+", ">+"):
            buf = []
            for nxt in lines[i + 1:]:
                if nxt.strip() == "":
                    buf.append("")
                    continue
                ni = len(nxt) - len(nxt.lstrip())
                if ni > indent:
                    buf.append(nxt.strip())
                else:
                    break
            if rest.startswith(">"):
                return " ".join(x for x in buf if x != "")
            return "\n".join(buf)
        if rest and rest[0] in "\"'" and rest[-1] == rest[0]:
            return rest[1:-1]
        return rest
    return None


def check_file(path):
    """Return (errors, warnings) for one SKILL.md. Errors fail the build; warnings don't."""
    errors, warnings = [], []
    if os.path.basename(path) != "SKILL.md":
        errors.append(f"entry file must be named SKILL.md, got {os.path.basename(path)}")
    text = open(path, encoding="utf-8").read()
    fm = parse_frontmatter(text)
    if fm is None:
        errors.append("missing YAML frontmatter")
        return errors, warnings
    name = extract_field(fm, "name")
    desc = extract_field(fm, "description")
    if not name:
        errors.append("missing `name`")
    else:
        if len(name.encode("utf-8")) > 64:
            errors.append(f"name exceeds 64 bytes ({len(name.encode('utf-8'))})")
        if not NAME_RE.fullmatch(name):
            errors.append(f"name must match ^[a-z0-9]+(-[a-z0-9]+)*$ (got '{name}')")
    if not desc:
        errors.append("missing `description`")
    else:
        nbytes = len(desc.encode("utf-8"))
        if nbytes > HARD_LIMIT:
            errors.append(f"description {nbytes}B exceeds Codex hard limit {HARD_LIMIT}B — skill is SKIPPED in Codex")
        elif nbytes > SOFT_LIMIT:
            warnings.append(f"description {nbytes}B over {SOFT_LIMIT}B soft cap (under {HARD_LIMIT}B hard limit, but little margin for multibyte drift)")
        if "<" in desc or ">" in desc:
            errors.append("description contains angle bracket(s) '<'/'>' (Codex rejects)")
    return errors, warnings


def main():
    root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    files = sorted(glob.glob(os.path.join(root, "skills", "*", "SKILL.md")))
    failures = warns = 0
    for path in files:
        rel = os.path.relpath(path, root)
        errors, warnings = check_file(path)
        if errors:
            failures += 1
            print(f"FAIL  {rel}")
        elif warnings:
            warns += 1
            print(f"warn  {rel}")
        else:
            print(f"ok    {rel}")
        for e in errors:
            print(f"        ✗ {e}")
        for w in warnings:
            print(f"        ! {w}")
    print()
    if failures:
        print(f"{failures} skill(s) FAIL Codex compatibility ({warns} warning-only). See scripts/check-skill-compat.py header for rules.")
        return 1
    print(f"All {len(files)} skills pass Codex compatibility checks ({warns} soft-cap warning(s)).")
    return 0


if __name__ == "__main__":
    sys.exit(main())
