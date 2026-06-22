#!/usr/bin/env python3
"""Invariants for quantize.py. Run: `python3 test_quantize.py` (needs Pillow).

No pytest — stdlib assert + a __main__ self-check, matching the repo's
stdlib-only test precedent. Three invariants:

  (a) output is grid-aligned and has <= palette-size unique colors
      (vs. the tens of thousands a raw diffusion output carries);
  (b) the PNG and SVG outputs encode the SAME grid;
  (c) determinism — same input + params -> byte-identical output twice
      (the median-cut-not-k-means guarantee, made executable).
"""
import os
import re
import tempfile

from PIL import Image

import quantize as q

GRID = 64
PALETTE = 16
SCALE = 4


def make_noisy_input(path, size=320):
    """A gradient + deterministic per-pixel noise -> thousands of colors,
    no RNG (so the fixture itself is reproducible)."""
    img = Image.new("RGB", (size, size))
    px = img.load()
    for y in range(size):
        for x in range(size):
            n = (x * 37 + y * 17) % 23
            px[x, y] = (
                (x + n) % 256,
                (y + n) % 256,
                (x * y // 64 + n) % 256,
            )
    img.save(path, "PNG")
    return img


def rasterize_svg(svg):
    """Parse our run-length <rect> SVG back into a full-res RGB grid."""
    vb = re.search(r'viewBox="0 0 (\d+) (\d+)"', svg)
    W, H = int(vb.group(1)), int(vb.group(2))
    grid = [[None] * W for _ in range(H)]
    rect = re.compile(
        r'<rect x="(\d+)" y="(\d+)" width="(\d+)" height="(\d+)" fill="#([0-9a-f]{6})"/>'
    )
    for m in rect.finditer(svg):
        x, y, w, h = (int(m.group(i)) for i in range(1, 5))
        fill = m.group(5)
        rgb = (int(fill[0:2], 16), int(fill[2:4], 16), int(fill[4:6], 16))
        for yy in range(y, y + h):
            for xx in range(x, x + w):
                grid[yy][xx] = rgb
    return W, H, grid


def test_grid_and_palette(tmp):
    src = os.path.join(tmp, "in.png")
    raw = make_noisy_input(src)
    raw_colors = len(set(raw.getdata()))
    assert raw_colors > 1000, f"fixture too tame ({raw_colors} colors)"

    img = q.downscale(Image.open(src), GRID)
    pimg = q.quantize(img, PALETTE, None, dither=False)

    assert max(pimg.size) == GRID, f"grid not aligned to {GRID}: {pimg.size}"
    used = len(set(pimg.getdata()))
    assert used <= PALETTE, f"{used} colors > palette {PALETTE}"
    print(f"  (a) grid {pimg.size}, {used} <= {PALETTE} colors (from {raw_colors}) OK")


def test_png_equals_svg(tmp):
    src = os.path.join(tmp, "in.png")
    make_noisy_input(src)
    png = os.path.join(tmp, "out.png")
    q.run(src, "png", png, GRID, PALETTE, None, False, False, SCALE)
    svg = q.run(src, "svg", os.path.join(tmp, "o.svg"), GRID, PALETTE, None, False, False, SCALE)

    W, H, sgrid = rasterize_svg(svg)
    pim = Image.open(png).convert("RGB")
    assert pim.size == (W, H), f"PNG {pim.size} != SVG {(W, H)}"
    pdata = list(pim.getdata())
    for y in range(H):
        for x in range(W):
            assert sgrid[y][x] is not None, f"SVG hole at {x},{y}"
            assert sgrid[y][x] == pdata[y * W + x], f"mismatch at {x},{y}"
    print(f"  (b) PNG and SVG encode identical {W}x{H} grid OK")


def test_determinism(tmp):
    src = os.path.join(tmp, "in.png")
    make_noisy_input(src)
    a = os.path.join(tmp, "a.png")
    b = os.path.join(tmp, "b.png")
    q.run(src, "png", a, GRID, PALETTE, None, False, False, SCALE)
    q.run(src, "png", b, GRID, PALETTE, None, False, False, SCALE)
    with open(a, "rb") as f:
        ba = f.read()
    with open(b, "rb") as f:
        bb = f.read()
    assert ba == bb, "PNG output not byte-identical across runs"

    s1 = q.run(src, "svg", os.path.join(tmp, "o.svg"), GRID, PALETTE, None, False, False, SCALE)
    s2 = q.run(src, "svg", os.path.join(tmp, "o.svg"), GRID, PALETTE, None, False, False, SCALE)
    assert s1 == s2, "SVG output not identical across runs"
    print("  (c) PNG + SVG byte-identical across two runs OK")


def main():
    with tempfile.TemporaryDirectory() as tmp:
        test_grid_and_palette(tmp)
        test_png_equals_svg(tmp)
        test_determinism(tmp)
    print("all quantize invariants pass")


if __name__ == "__main__":
    main()
