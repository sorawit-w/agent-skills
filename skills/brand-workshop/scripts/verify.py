#!/usr/bin/env python3
"""Mascot-lane tools for brand-workshop (proven in the 2026-07-07 test drive).

Subcommands
  integrity <sheet.html>            Template-integrity gate (D10): zero '{{', balanced CSS
                                    braces, HTML tags parse, every var(--x) used is defined.
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
"""
import argparse, re, sys


def cmd_integrity(args):
    html = open(args.file, encoding="utf-8").read()
    errs = []
    if "{{" in html:
        errs.append("unreplaced '{{' present (token left in output, or v1-style brace bug)")
    css_parts = html.split("<style>")
    css = css_parts[1].split("</style>")[0] if len(css_parts) > 1 else ""
    if css.count("{") != css.count("}"):
        errs.append(f"CSS brace mismatch: {css.count('{')} open vs {css.count('}')} close")
    defined = set(re.findall(r"(--[\w-]+)\s*:", css))
    used = set(re.findall(r"var\((--[\w-]+)", css)) | set(re.findall(r"var\((--[\w-]+)", html))
    missing = sorted(v for v in used if v not in defined and v != "--w")
    if missing:
        errs.append("var() used but never defined: " + ", ".join(missing))
    from html.parser import HTMLParser

    class P(HTMLParser):
        def __init__(self):
            super().__init__()
            self.stack, self.bad = [], []
            self.void = {"meta", "link", "img", "br", "hr", "input"}

        def handle_starttag(self, tag, attrs):
            if tag not in self.void:
                self.stack.append(tag)

        def handle_endtag(self, tag):
            if self.stack and self.stack[-1] == tag:
                self.stack.pop()
            else:
                self.bad.append(tag)

    p = P()
    p.feed(html)
    if p.stack:
        errs.append("unclosed tags: " + ",".join(p.stack))
    if p.bad:
        errs.append("mismatched closing tags: " + ",".join(p.bad))
    imgs = re.findall(r"<img\b[^>]*>", html)
    noalt = [i for i in imgs if 'alt="' not in i]
    if noalt:
        errs.append(f"{len(noalt)} <img> without alt attribute")
    if errs:
        print("INTEGRITY: FAIL")
        for e in errs:
            print("  -", e)
        return 1
    print(f"INTEGRITY: PASS ({len(imgs)} images, {len(defined)} css vars)")
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
    total = (w // 2) * (h // 2)
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

    async def run():
        async with async_playwright() as p:
            b = await p.chromium.launch()
            pg = await b.new_page()
            await pg.goto(src.as_uri(), wait_until="networkidle")
            for fmt in ["Letter", "A4"]:
                with tempfile.NamedTemporaryFile(suffix=".pdf", delete=False) as f:
                    path = f.name
                await pg.pdf(path=path, format=fmt, landscape=args.landscape,
                             print_background=True,
                             margin={k: "8mm" for k in ("top", "bottom", "left", "right")})
                results[fmt] = len(PdfReader(path).pages)
            await b.close()

    asyncio.run(run())
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
