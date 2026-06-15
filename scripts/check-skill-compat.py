#!/usr/bin/env python3
"""Cross-platform SKILL.md frontmatter + manifest compatibility checker.

Claude Code imposes no hard limit on the `description` field, but OpenAI Codex
*silently skips* any skill whose SKILL.md violates its frontmatter rules. Since
the `description` field is shared across platforms (Codex has no per-platform
override), every skill in this repo must satisfy the stricter Codex contract.

Codex rules enforced here (a violation = skill not loaded in Codex):
  - description: 1..=1024 in LENGTH, measured as Unicode CHARACTERS — the Codex
    Rust loader uses `value.chars().count()` (`MAX_DESCRIPTION_LEN = 1024`).
    The earlier byte-counting bug (openai/codex#7730) is fixed; current Codex
    counts characters, so we count Python `str` length (codepoints) to match.
  - name: must match ^[a-z0-9]+(-[a-z0-9]+)*$ and be <= 64 bytes. (Codex's own
    rule is laxer — ^[a-zA-Z0-9_-]+$ — so our lowercase-hyphen house style is a
    safe subset.)
  - entry file must be named exactly SKILL.md (all caps).

We target a 1000-character soft cap (LIMIT - MARGIN) so later edits keep a little
headroom before the hard 1024-character wall.

This script also asserts VERSION PARITY across the release manifests (the Codex
addition turned the old "4-file" version ritual into a 5-file one — drift in any
one silently breaks a platform). See check_versions().

Exit code 0 = all good; 1 = at least one violation. Run from repo root:
    python3 scripts/check-skill-compat.py
"""
import glob
import json
import os
import re
import sys

HARD_LIMIT = 1024          # Codex hard cap, in Unicode characters
SOFT_LIMIT = 1000          # our authoring target, leaves headroom
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
        nchars = len(desc)
        if nchars > HARD_LIMIT:
            errors.append(f"description {nchars} chars exceeds Codex hard limit {HARD_LIMIT} — skill is SKIPPED in Codex")
        elif nchars > SOFT_LIMIT:
            warnings.append(f"description {nchars} chars over {SOFT_LIMIT}-char soft cap (under {HARD_LIMIT}-char hard limit, but little margin)")
    return errors, warnings


def _version_sources(root):
    """Return {label: version|None} for every place the release version lives."""
    out = {}

    def jget(relpath, *keys):
        try:
            with open(os.path.join(root, relpath), encoding="utf-8") as f:
                node = json.load(f)
            for k in keys:
                node = node[k]
            return node
        except (OSError, KeyError, IndexError, json.JSONDecodeError):
            return None

    out[".claude-plugin/plugin.json"] = jget(".claude-plugin/plugin.json", "version")
    out[".claude-plugin/marketplace.json"] = jget(".claude-plugin/marketplace.json", "plugins", 0, "version")
    out[".codex-plugin/plugin.json"] = jget(".codex-plugin/plugin.json", "version")

    # CHANGELOG.md — first `## [X.Y.Z]` heading
    try:
        with open(os.path.join(root, "CHANGELOG.md"), encoding="utf-8") as f:
            m = re.search(r"^##\s*\[(\d+\.\d+\.\d+)\]", f.read(), re.M)
            out["CHANGELOG.md"] = m.group(1) if m else None
    except OSError:
        out["CHANGELOG.md"] = None

    # README.md — `Current release: \`X.Y.Z\``
    try:
        with open(os.path.join(root, "README.md"), encoding="utf-8") as f:
            m = re.search(r"Current release:\s*`(\d+\.\d+\.\d+)`", f.read())
            out["README.md"] = m.group(1) if m else None
    except OSError:
        out["README.md"] = None

    return out


def check_versions(root):
    """Return list of error strings if the release version disagrees across manifests."""
    sources = _version_sources(root)
    missing = [label for label, v in sources.items() if v is None]
    present = {label: v for label, v in sources.items() if v is not None}
    errors = []
    for label in missing:
        errors.append(f"version not found in {label}")
    distinct = set(present.values())
    if len(distinct) > 1:
        detail = ", ".join(f"{label}={v}" for label, v in present.items())
        errors.append(f"version mismatch across manifests: {detail}")
    return errors, (present[next(iter(present))] if len(distinct) == 1 and present else None)


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
    version_errors, agreed = check_versions(root)
    if version_errors:
        print("FAIL  version parity")
        for e in version_errors:
            print(f"        ✗ {e}")
    else:
        print(f"ok    version parity — all manifests at {agreed}")

    print()
    total_fail = failures + (1 if version_errors else 0)
    if total_fail:
        print(f"{failures} skill(s) FAIL Codex compatibility ({warns} warning-only)"
              + ("; version parity FAILED" if version_errors else "")
              + ". See scripts/check-skill-compat.py header for rules.")
        return 1
    print(f"All {len(files)} skills pass Codex compatibility checks ({warns} soft-cap warning(s)); version parity OK.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
