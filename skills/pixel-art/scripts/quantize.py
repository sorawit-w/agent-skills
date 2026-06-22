#!/usr/bin/env python3
"""Deterministic pixel-art quantize: raster -> true grid-aligned pixel art.

Raw diffusion output is *pseudo* pixel art — tens of thousands of unique
colors, no real grid. This makes it real:

    nearest-neighbor downscale to a target grid
      -> median-cut palette quantize (deterministic; honors a fixed ramp)
      -> optional error-diffusion dither + orphan-pixel cleanup
      -> nearest-neighbor upscale x N for display

Output is PNG or SVG of the *same* grid. SVG = one <rect> per
run-length-merged horizontal cell (single sprite only — not a banner /
composition path).

Determinism: median-cut (kmeans=0) + explicit dither setting means same
input + params -> byte-identical output. (k-means would random-init and
break this — that's why it's median-cut.)

Usage:
    python3 quantize.py IN.png --format png|svg [--out OUT]
        [--grid N] [--palette N] [--ramp "#rrggbb,#rrggbb,..."]
        [--dither] [--cleanup] [--scale N]

Needs Pillow (`pip install -r requirements.txt`). Alpha is flattened to
RGB in v1 — sprites needing transparency are a future addition.
"""
import argparse
import sys

from PIL import Image

DEFAULT_GRID = 192      # target grid (longer side), in the 128–256 band
DEFAULT_PALETTE = 32    # colors, in the 24–48 band
DEFAULT_SCALE = 8       # display upscale factor


def parse_ramp(ramp):
    """'#rrggbb,#aabbcc' -> [(r,g,b), ...]. Returns None if no ramp."""
    if not ramp:
        return None
    out = []
    for tok in ramp.split(","):
        h = tok.strip().lstrip("#")
        if len(h) != 6:
            raise ValueError(f"bad hex in --ramp: {tok!r} (want #rrggbb)")
        out.append((int(h[0:2], 16), int(h[2:4], 16), int(h[4:6], 16)))
    if not out:
        return None
    if len(out) > 256:
        raise ValueError("--ramp supports at most 256 colors")
    return out


def downscale(img, grid):
    """NEAREST downscale so the longer side == grid, aspect preserved."""
    img = img.convert("RGB")
    w, h = img.size
    longest = max(w, h)
    if longest <= grid:
        return img  # already at/under target; don't upscale here
    scale = grid / longest
    new = (max(1, round(w * scale)), max(1, round(h * scale)))
    return img.resize(new, Image.Resampling.NEAREST)


def quantize(img, palette_n, ramp_rgb, dither):
    """Return a P-mode image. Median-cut, or a fixed ramp if given."""
    d = Image.Dither.FLOYDSTEINBERG if dither else Image.Dither.NONE
    if ramp_rgb:
        flat = []
        for rgb in ramp_rgb:
            flat.extend(rgb)
        # Pillow needs a 256-color palette; pad by repeating the last color.
        last = ramp_rgb[-1]
        while len(flat) < 256 * 3:
            flat.extend(last)
        pal = Image.new("P", (1, 1))
        pal.putpalette(flat)
        return img.quantize(palette=pal, dither=d)
    return img.quantize(
        colors=palette_n, method=Image.Quantize.MEDIANCUT, kmeans=0, dither=d
    )


def cleanup_orphans(pimg):
    """Remove single-pixel islands: a pixel whose 4-neighbors all share one
    other index is reassigned to that index. One pass, deterministic."""
    w, h = pimg.size
    px = list(pimg.getdata())

    def at(x, y):
        return px[y * w + x]

    out = px[:]
    for y in range(h):
        for x in range(w):
            c = at(x, y)
            neigh = []
            if x > 0:
                neigh.append(at(x - 1, y))
            if x < w - 1:
                neigh.append(at(x + 1, y))
            if y > 0:
                neigh.append(at(x, y - 1))
            if y < h - 1:
                neigh.append(at(x, y + 1))
            if neigh and all(n == neigh[0] and n != c for n in neigh):
                out[y * w + x] = neigh[0]
    res = pimg.copy()
    res.putdata(out)
    return res


def grid_indices(pimg):
    """(indices_2d, palette_hexes). indices_2d[y][x] = palette index."""
    w, h = pimg.size
    data = list(pimg.getdata())
    pal = pimg.getpalette() or []
    hexes = {}
    rows = [data[y * w:(y + 1) * w] for y in range(h)]
    used = set(data)
    for idx in used:
        r, g, b = pal[idx * 3:idx * 3 + 3]
        hexes[idx] = f"#{r:02x}{g:02x}{b:02x}"
    return rows, hexes


def to_svg(rows, hexes, scale):
    """One <rect> per run-length-merged horizontal run of identical index."""
    if not rows:
        return '<svg xmlns="http://www.w3.org/2000/svg"></svg>'
    h = len(rows)
    w = len(rows[0])
    parts = [
        f'<svg xmlns="http://www.w3.org/2000/svg" '
        f'viewBox="0 0 {w * scale} {h * scale}" '
        f'shape-rendering="crispEdges" '
        f'style="image-rendering: pixelated;">'
    ]
    for y, row in enumerate(rows):
        x = 0
        while x < w:
            idx = row[x]
            run = 1
            while x + run < w and row[x + run] == idx:
                run += 1
            parts.append(
                f'<rect x="{x * scale}" y="{y * scale}" '
                f'width="{run * scale}" height="{scale}" '
                f'fill="{hexes[idx]}"/>'
            )
            x += run
    parts.append("</svg>")
    return "".join(parts)


def to_png_upscaled(pimg, scale):
    """RGB image, each grid cell upscaled to scale x scale (NEAREST)."""
    w, h = pimg.size
    return pimg.convert("RGB").resize(
        (w * scale, h * scale), Image.Resampling.NEAREST
    )


def run(in_path, fmt, out_path, grid, palette_n, ramp, dither, cleanup, scale):
    img = Image.open(in_path)
    img = downscale(img, grid)
    ramp_rgb = parse_ramp(ramp)
    pimg = quantize(img, palette_n, ramp_rgb, dither)
    if cleanup:
        pimg = cleanup_orphans(pimg)
    if fmt == "svg":
        rows, hexes = grid_indices(pimg)
        svg = to_svg(rows, hexes, scale)
        if out_path:
            with open(out_path, "w") as f:
                f.write(svg)
        else:
            sys.stdout.write(svg)
        return svg
    # png
    big = to_png_upscaled(pimg, scale)
    out = out_path or (in_path.rsplit(".", 1)[0] + ".quant.png")
    big.save(out, "PNG")
    return out


def main(argv=None):
    p = argparse.ArgumentParser(description="Deterministic pixel-art quantize.")
    p.add_argument("input", help="source raster (PNG/JPG/...)")
    p.add_argument("--format", choices=["png", "svg"], default="png")
    p.add_argument("--out", default=None, help="output path (SVG defaults to stdout)")
    p.add_argument("--grid", type=int, default=DEFAULT_GRID, help="grid target, longer side")
    p.add_argument("--palette", type=int, default=DEFAULT_PALETTE, help="palette size")
    p.add_argument("--ramp", default=None, help='fixed palette "#rrggbb,#rrggbb,..."')
    p.add_argument("--dither", action="store_true", help="error-diffusion dither (default off)")
    p.add_argument("--cleanup", action="store_true", help="remove single-pixel islands")
    p.add_argument("--scale", type=int, default=DEFAULT_SCALE, help="display upscale factor")
    a = p.parse_args(argv)
    res = run(a.input, a.format, a.out, a.grid, a.palette, a.ramp,
              a.dither, a.cleanup, a.scale)
    if a.format == "png":
        sys.stderr.write(f"wrote {res}\n")


if __name__ == "__main__":
    main()
