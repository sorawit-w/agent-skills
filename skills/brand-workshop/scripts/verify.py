#!/usr/bin/env python3
"""Mascot-lane tools for brand-workshop (proven in the 2026-07-07 test drive).

Subcommands
  integrity <sheet.html>            Template-integrity gate (D10): zero '{{', balanced CSS
                                    braces, HTML structurally valid (strict html5lib parse),
                                    every var(--x) used is defined (incl. per-row inline
                                    vars like --w on every .fill), alt on every image.
  anchors <image.png> A=#HEX ...    Palette-anchor gate (D4): % of pixels within --tol of
                                    each named anchor; FAIL if any drops below --min.
  pagegate <sheet.html>             Print gate (D12): render in headless Chromium, assert
                                    exactly 1 page on Letter AND A4. --landscape for the
                                    landscape template. Requires playwright + pypdf;
                                    reports SKIPPED (exit 2) if unavailable — never fake a PASS.
  cutout <in.png> <out.png>         Background removal (D9): edge flood-fill (--tol, default 28),
                                    drop pale low-saturation components (soft shadows), keep
                                    saturated satellites (hearts, sparkles), feather alpha.

Exit codes: 0 PASS · 1 FAIL · 2 SKIPPED (missing optional dependency)

Integrity HTML validation (Rev 3): structural checking runs html5lib — the
browser's own HTML parsing algorithm — in error-collecting mode, and fails on
any parse error EXCEPT a small allowlist of browser-tolerated character-reference
codes (an unescaped '&' in a URL, e.g. Google Fonts '?family=A&display=swap').
This is fail-closed by design: a *new* structural defect class emits a code that
is not on the benign allowlist, so it fails by default — no per-defect regex to
keep extending (the earlier regex+HTMLParser backstop leaked an unescaped '"' in
an attribute value, e.g. alt="a"b"c", because HTMLParser silently truncates it).
A false positive from an unforeseen benign code is a loud, safe one-line
allowlist fix; a missed defect is the silent corruption this gate exists to stop.
html5lib is a required dependency (scripts/requirements.txt); if it is absent the
structural check reports SKIPPED (exit 2) rather than faking a PASS — the
dependency-free checks (tokens, CSS braces, var() defs) still run.

Rev 3 also closes the second documented leak: a custom property consumed in
<style> via var() but defined only inline (--w, set per stat row as
style="--w:90%") is now checked per element against the parsed DOM — every
element the consuming rule's subject selector targets (.fill) must *define* it
inline (a real `--w:` declaration, not just mention it) — so one good STATS_ROWS
row can no longer mask a sibling that omits it.
"""
import argparse, re, sys

# Character-reference codes browsers tolerate (an unescaped '&' in a URL-ish
# attribute value). Every other html5lib parse error is treated as a structural
# defect — fail-closed, so an unforeseen defect class fails without a code list.
_BENIGN_HTML5_CODES = {"expected-named-entity", "named-entity-without-semicolon"}


def _style_defines(style, prop):
    """True iff an inline style attr *declares* custom property `prop` (`--x: v`).
    A definition, not a mention: `width:var(--w)` (a use) and `--width:70%` (a
    different property) both contain the substring `--w` but define neither."""
    return any(d.split(":", 1)[0].strip() == prop for d in style.split(";") if ":" in d)


def _selector_subject(sel):
    """(tag, {classes}, id) of a selector's *subject* — the rightmost compound,
    after descendant/child/sibling combinators; pseudos and [attr] stripped. So
    `.track .fill:hover` → (None, {'fill'}, None); `input#q.big` → ('input', {'big'}, 'q').
    The subject is the element the rule's declarations actually style."""
    part = re.split(r"[ >+~]+", sel.strip())[-1]
    part = re.sub(r"::?[\w-]+(\([^)]*\))?|\[[^\]]*\]", "", part)  # drop pseudos / [attr]
    tag = re.match(r"[\w-]+", part)
    idm = re.search(r"#([\w-]+)", part)
    return (tag.group(0) if tag else None,
            set(re.findall(r"\.([\w-]+)", part)),
            idm.group(1) if idm else None)


def cmd_integrity(args):
    raw = open(args.file, encoding="utf-8").read()
    # Blank comments to same-count newlines (not delete): the template header comment carries
    # token examples ({{TOKEN}}, style="--w:90%", <img> shapes) that would otherwise register
    # as real placeholders, inline var defs, or images — masking the very defects this gate
    # catches. Preserving the newline count keeps html5lib parse-error line numbers pointing
    # at the real source line.
    doc = re.sub(r"<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), raw, flags=re.S)
    errs = []
    if "{{" in doc:
        errs.append("unreplaced '{{' present (token left in output, or v1-style brace bug)")
    # A str.format mis-fill collapses '{{TOKEN}}' to single-brace '{TOKEN}', which keeps CSS
    # braces balanced and HTML parseable — so it slips the '{{' check above. Token names are
    # UPPER_SNAKE, unlike CSS (lowercase properties, --vars), so this pattern can't false-match.
    singles = sorted(set(re.findall(r"\{[A-Z][A-Z0-9_]*\}", doc)))
    if singles:
        errs.append("single-brace placeholder(s) present (str.format mis-fill): " + ", ".join(singles))
    css_parts = doc.split("<style>")
    css = css_parts[1].split("</style>")[0] if len(css_parts) > 1 else ""
    if css.count("{") != css.count("}"):
        errs.append(f"CSS brace mismatch: {css.count('{')} open vs {css.count('}')} close")
    # --w is defined per-row in inline style attrs (STATS_ROWS: style="--w:90%"), not in <style>,
    # so treat it as defined only when an inline definition actually exists — otherwise a stat row
    # copied from the print shape (bare width:90%, no --w) leaves .fill{width:var(--w)} undefined.
    inline_defined = set(re.findall(r"(--[\w-]+)\s*:", doc)) - set(re.findall(r"(--[\w-]+)\s*:", css))
    defined = set(re.findall(r"(--[\w-]+)\s*:", css)) | inline_defined
    used = set(re.findall(r"var\((--[\w-]+)", css)) | set(re.findall(r"var\((--[\w-]+)", doc))
    missing = sorted(v for v in used if v not in defined)
    if missing:
        errs.append("var() used but never defined: " + ", ".join(missing))

    # Strict HTML structural validation via html5lib (the browser's own parsing algorithm),
    # in error-collecting mode. Fail on any parse error except the benign character-reference
    # codes above — catches malformed attributes (unescaped '"' in a value), unclosed /
    # mismatched tags, stray '<', bad attribute-name chars, EOF-in-tag, etc., with no
    # per-defect regex. Absent html5lib → SKIPPED (never a faked PASS); see the module docstring.
    structural_skipped = False
    img_count = None
    try:
        import html5lib
    except ImportError:
        structural_skipped = True
    else:
        parser = html5lib.HTMLParser(namespaceHTMLElements=False)
        tree = parser.parse(doc)
        bad = [(pos, code) for pos, code, _ in parser.errors if code not in _BENIGN_HTML5_CODES]
        if bad:
            shown = "; ".join(f"{code} (line {pos[0]} col {pos[1]})" for pos, code in bad[:8])
            more = f" … +{len(bad) - 8} more" if len(bad) > 8 else ""
            errs.append("malformed HTML (strict parse): " + shown + more)
        imgs = tree.findall(".//img")
        img_count = len(imgs)
        noalt = [im for im in imgs if im.get("alt") is None]
        if noalt:
            errs.append(f"{len(noalt)} <img> without alt attribute")
        # Per-element custom properties: a var(--x) consumed in <style> but defined neither
        # there nor in :root is satisfiable only inline, per element. The document-wide inline
        # scan above (defined) would let one stat row that sets it mask a sibling row that omits
        # it — the STATS_ROWS --w masking (web .fill{width:var(--w)}, set per row as
        # style="--w:90%"). Resolve it against the DOM: every element the consuming rule's
        # subject selector targets must *define* the property in its own inline style. (Print's
        # .fill uses a literal width:%, no var(--w), so this simply never triggers there.)
        # "Global" here means :root ONLY. A custom property set in any other selector is
        # scoped to that selector's subtree, so it does not guarantee an element elsewhere
        # (a .fill in a different subtree) inherits it — counting non-:root definitions as
        # global is the same document-wide masking one layer down. Bounded scope: this models
        # :root-vs-inline, not the full cascade; a var defined by a CSS rule *on the consuming
        # element itself* would be flagged as missing-inline (a safe, loud false-positive),
        # but the mascot templates only ever set per-row vars inline, never in an intermediate
        # rule — so this stays precise for them. Full cascade resolution needs a real CSS
        # engine and is deliberately out of scope for this gate.
        root = re.search(r":root\s*\{([^}]*)\}", css)
        root_defined = set(re.findall(r"(--[\w-]+)\s*:", root.group(1))) if root else set()
        for v in sorted(set(re.findall(r"var\((--[\w-]+)", css)) - root_defined):
            # Collect the subject selector of EVERY rule that consumes var(--v), not just the
            # first — an element matching any of them must define --v inline. Multiple rules
            # can legitimately consume one var; checking only the first would leave the rest
            # unenforced.
            targets, sels = [], []
            for rule in re.finditer(r"([^{}]*)\{[^{}]*var\(" + re.escape(v) + r"\)", css):
                for sel in rule.group(1).split(","):
                    tag, classes, sid = _selector_subject(sel)
                    if tag or classes or sid:
                        targets.append((tag, classes, sid))
                        sels.append(sel.strip())
            if not targets:
                continue  # var used but no rule's subject could be resolved — skip, don't guess
            offenders = 0
            for el in tree.iter():
                ecls = set((el.get("class") or "").split())
                if any((tag is None or el.tag == tag) and classes <= ecls
                       and (sid is None or el.get("id") == sid)
                       for tag, classes, sid in targets) \
                        and not _style_defines(el.get("style") or "", v):
                    offenders += 1
            if offenders:
                shown = ", ".join(dict.fromkeys(sels))  # de-dup, keep order
                errs.append(f"{offenders} element(s) matched by '{shown}' use CSS {v} but do not "
                            f"define it inline (per-row var; e.g. a broken STATS_ROWS row)")

    if errs:
        print("INTEGRITY: FAIL")
        for e in errs:
            print("  -", e)
        if structural_skipped:
            print("  ! strict HTML structural check SKIPPED (html5lib not installed); "
                  "failures above are from non-structural checks")
        return 1
    if structural_skipped:
        print("INTEGRITY: SKIPPED (html5lib not installed) — cannot run strict HTML structural validation")
        print("  non-structural checks passed (tokens, CSS braces, var() defs); install: pip install html5lib")
        return 2
    print(f"INTEGRITY: PASS ({img_count} images, {len(defined)} css vars)")
    return 0


def cmd_anchors(args):
    from PIL import Image
    im = Image.open(args.image).convert("RGB")
    px, (w, h) = im.load(), im.size
    anchors = {}
    for spec in args.anchor:
        name, hexv = spec.split("=")
        hexv = hexv.lstrip("#")
        anchors[name] = tuple(int(hexv[i:i + 2], 16) for i in (0, 2, 4))
    counts = {k: 0 for k in anchors}
    t2 = args.tol * args.tol
    for y in range(0, h, 2):
        for x in range(0, w, 2):
            r, g, b = px[x, y]
            for k, (ar, ag, ab) in anchors.items():
                if (r - ar) ** 2 + (g - ag) ** 2 + (b - ab) ** 2 < t2:
                    counts[k] += 1
    total = len(range(0, w, 2)) * len(range(0, h, 2))  # actual sampled-pixel count (ceil, not floor)
    fail = False
    for k, v in counts.items():
        pct = 100 * v / total
        ok = pct >= args.min
        fail |= not ok
        print(f"  {k:14s} {pct:5.2f}%  {'ok' if ok else 'BELOW MIN'}")
    print("ANCHORS:", "FAIL" if fail else "PASS")
    return 1 if fail else 0


def cmd_pagegate(args):
    try:
        import asyncio
        from playwright.async_api import async_playwright
        from pypdf import PdfReader
    except ImportError as e:
        print(f"PAGEGATE: SKIPPED (missing dependency: {e.name}) — install playwright+pypdf, run 'playwright install chromium'")
        return 2
    import pathlib, tempfile
    src = pathlib.Path(args.file).resolve()
    results = {}

    class _BrowserUnavailable(Exception):
        pass

    async def run():
        async with async_playwright() as p:
            try:
                b = await p.chromium.launch()
            except Exception as e:  # browser binary not installed → SKIPPED, never a fake PASS
                raise _BrowserUnavailable(e)
            pg = await b.new_page()
            await pg.goto(src.as_uri(), wait_until="networkidle")
            for fmt in ["Letter", "A4"]:
                with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
                    path = f.name
                await pg.pdf(path=path, format=fmt, landscape=args.landscape,
                             print_background=True,
                             margin={k: "8mm" for k in ("top", "bottom", "left", "right")})
                results[fmt] = len(PdfReader(path).pages)
                pathlib.Path(path).unlink()  # verification-only PDF — never left behind
            await b.close()

    try:
        asyncio.run(run())
    except _BrowserUnavailable as e:
        print(f"PAGEGATE: SKIPPED (Chromium not installed: {e}) — run 'playwright install chromium'")
        return 2
    fail = any(n != 1 for n in results.values())
    for fmt, n in results.items():
        print(f"  {fmt}: {n} page(s)")
    print("PAGEGATE:", "FAIL (must be exactly 1 page per format)" if fail else "PASS (engine: Chromium)")
    return 1 if fail else 0


def cmd_cutout(args):
    import numpy as np
    from PIL import Image
    from scipy import ndimage
    im = Image.open(args.input).convert("RGB")
    a = np.asarray(im).astype(int)
    corners = np.concatenate([a[:20, :20].reshape(-1, 3), a[:20, -20:].reshape(-1, 3),
                              a[-20:, :20].reshape(-1, 3), a[-20:, -20:].reshape(-1, 3)])
    bg = np.median(corners, axis=0)
    near = np.abs(a - bg).max(axis=2) < args.tol
    lab, _ = ndimage.label(near)
    borders = set(np.unique(np.concatenate([lab[0, :], lab[-1, :], lab[:, 0], lab[:, -1]]))) - {0}
    subj = ~np.isin(lab, list(borders))
    slab, sn = ndimage.label(subj)
    keep = np.zeros_like(subj)
    kept = dropped = 0
    for i in range(1, sn + 1):
        m = slab == i
        if int(m.sum()) < 40:
            continue
        p = a[m]
        pale = float((p.max(1) - p.min(1)).mean()) < 25 and float(p.mean()) > 200
        if pale:
            dropped += 1
        else:
            keep |= m
            kept += 1
    alpha = np.clip((ndimage.gaussian_filter(keep.astype(float), 0.7) - 0.25) / 0.5, 0, 1)
    out = np.dstack([np.asarray(im), (alpha * 255).astype(np.uint8)])
    Image.fromarray(out, "RGBA").save(args.output)
    print(f"CUTOUT: wrote {args.output} · kept {kept} component(s), dropped {dropped} pale (shadow) "
          f"· coverage {100 * keep.mean():.1f}% · bg={tuple(int(c) for c in bg)} tol={args.tol}")
    return 0


def main():
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    s = sub.add_parser("integrity"); s.add_argument("file"); s.set_defaults(fn=cmd_integrity)
    s = sub.add_parser("anchors"); s.add_argument("image"); s.add_argument("anchor", nargs="+",
        help="NAME=#RRGGBB pairs, e.g. accent=#FF7A59")
    s.add_argument("--tol", type=int, default=60); s.add_argument("--min", type=float, default=0.5)
    s.set_defaults(fn=cmd_anchors)
    s = sub.add_parser("pagegate"); s.add_argument("file"); s.add_argument("--landscape", action="store_true")
    s.set_defaults(fn=cmd_pagegate)
    s = sub.add_parser("cutout"); s.add_argument("input"); s.add_argument("output")
    s.add_argument("--tol", type=int, default=28); s.set_defaults(fn=cmd_cutout)
    args = ap.parse_args()
    sys.exit(args.fn(args))


if __name__ == "__main__":
    main()
