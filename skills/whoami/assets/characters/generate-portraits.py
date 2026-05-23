#!/usr/bin/env python3
"""
whoami — hi-density pixel-art class portrait generator.

Renders 13 class portraits as crafted pixel art (64x64 logical grid,
upscaled x8 nearest-neighbour to 512x512 PNG). Deterministic: same input
-> same output, no external services, version-controlled alongside the
assets it produces.

Craft discipline (see skills/pixel-art/references/):
  - hard pixel edges, no anti-aliasing (NEAREST upscale)
  - per-material shade ramps with hue-shifted shadows
  - ordered Bayer dithering at the background vignette transition
  - a clean 1px dark silhouette outline (selout pass)
  - readable silhouette at thumbnail size

6 axis-family designs (high/low variant pairs) + Wildcard = 13 classes.

Run:  python3 generate-portraits.py
Out:  <class>.png  (this directory, 13 files)
      a review contact sheet in the system temp dir (not committed)
"""

import os
import tempfile
from PIL import Image

W = H = 64
SCALE = 8
OUT_DIR = os.path.dirname(os.path.abspath(__file__))

BG1 = (0xf3, 0xea, 0xd6)   # cream centre
BG2 = (0xe8, 0xda, 0xbd)   # cream mid
BG3 = (0xd9, 0xc8, 0xa6)   # cream corner

BAYER4 = [[0, 8, 2, 10], [12, 4, 14, 6], [3, 11, 1, 9], [15, 7, 13, 5]]


def hx(s):
    s = s.lstrip("#")
    return (int(s[0:2], 16), int(s[2:4], 16), int(s[4:6], 16))


# ---------------------------------------------------------------- canvas
class Canvas:
    def __init__(self):
        self.p = [[BG1 for _ in range(W)] for _ in range(H)]
        self.fig = [[False for _ in range(W)] for _ in range(H)]

    def _ok(self, x, y):
        return 0 <= x < W and 0 <= y < H

    def bg(self, x, y, c):
        if self._ok(x, y):
            self.p[y][x] = c

    def f(self, x, y, c):
        """Draw a figure pixel (recorded in the silhouette mask)."""
        if self._ok(x, y):
            self.p[y][x] = c
            self.fig[y][x] = True

    def frect(self, x0, y0, x1, y1, c):
        for y in range(y0, y1 + 1):
            for x in range(x0, x1 + 1):
                self.f(x, y, c)

    def frow(self, y, x0, x1, c):
        for x in range(x0, x1 + 1):
            self.f(x, y, c)

    def fcol(self, x, y0, y1, c):
        for y in range(y0, y1 + 1):
            self.f(x, y, c)


def background(cv, tint):
    """Warm-cream vignette with a dithered ring; faint per-family tint."""
    cx, cy = 32, 26
    for y in range(H):
        for x in range(W):
            d = ((x - cx) ** 2 + ((y - cy) * 1.05) ** 2) ** 0.5
            if d > 36:
                base = BG3
            elif d > 27:
                t = (d - 27) / 9.0
                thr = (BAYER4[y % 4][x % 4] + 0.5) / 16.0
                base = BG3 if t > thr else BG2
            elif d > 18:
                t = (d - 18) / 9.0
                thr = (BAYER4[y % 4][x % 4] + 0.5) / 16.0
                base = BG2 if t > thr else BG1
            else:
                base = BG1
            if tint:
                base = mix(base, tint, 0.10)
            cv.bg(x, y, base)


def mix(a, b, t):
    return tuple(int(round(a[i] * (1 - t) + b[i] * t)) for i in range(3))


def rounded(cv, x0, y0, x1, y1, c, r):
    """Filled rounded rectangle (figure pixels)."""
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            cx = 0
            if x < x0 + r:
                cx = x0 + r - x
            elif x > x1 - r:
                cx = x - (x1 - r)
            cy = 0
            if y < y0 + r:
                cy = y0 + r - y
            elif y > y1 - r:
                cy = y - (y1 - r)
            if cx * cx + cy * cy <= r * r + 1:
                cv.f(x, y, c)


def outline_pass(cv, c):
    """Selout: every background pixel touching the figure becomes outline."""
    add = []
    for y in range(H):
        for x in range(W):
            if cv.fig[y][x]:
                continue
            hit = False
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                nx, ny = x + dx, y + dy
                if 0 <= nx < W and 0 <= ny < H and cv.fig[ny][nx]:
                    hit = True
                    break
            if hit:
                add.append((x, y))
    for x, y in add:
        cv.p[y][x] = c
        cv.fig[y][x] = True


# ---------------------------------------------------------------- shoulders
def shoulders(cv, pal, placket=True):
    """Shared bust: shaded trapezoid mantle with a collar band."""
    for y in range(45, 64):
        fr = (y - 45) / 18.0
        hw = int(round(13 + fr * 14))
        l, r = 32 - hw, 32 + hw
        cv.frow(y, l, r, pal["mid"])
        # lit side (upper-left)
        cv.f(l, y, pal["light"])
        cv.f(l + 1, y, pal["light"])
        if y <= 49:
            cv.frow(y, l, l + 3, pal["light"])
        # core shadow (lower-right)
        cv.frow(y, r - 6, r, pal["dark"])
        if y >= 57:
            cv.frow(y, l + 2, r, pal["dark"])
        # dither bridge mid->dark
        if 50 <= y <= 56:
            thr = (BAYER4[y % 4][(r - 8) % 4] + 0.5) / 16.0
            if thr < 0.5:
                cv.f(r - 7, y, pal["dark"])
    # collar band
    for y in range(45, 48):
        fr = (y - 45) / 18.0
        hw = int(round(13 + fr * 14))
        cv.frow(y, 32 - hw, 32 + hw, pal["trim"])
    cv.frow(44, 26, 38, pal["trim"])
    # centre placket
    if placket:
        cv.fcol(32, 48, 63, pal["dark"])
        cv.fcol(31, 50, 63, pal["light"])


def neck(cv, pal):
    cv.frect(28, 39, 35, 47, pal["dark"])
    cv.fcol(28, 39, 46, pal["shadow"])
    cv.fcol(35, 39, 46, pal["shadow"])
    cv.frow(40, 29, 34, pal["mid"])


# ---------------------------------------------------------------- emblems
EMBLEMS = {
    "chevron": ["....X....", "...XXX...", "..XX.XX..", ".XX...XX.",
                "XX.....XX", "...XXX...", "..XX.XX.."],
    "baton":   [".........", "X.......X", "XX.....XX", ".XXXXXXX.",
                "XX.....XX", "X.......X", "........."],
    "book":    ["...X.X...", "..XXXXX..", ".XX.X.XX.", "XX..X..XX",
                "XX..X..XX", "XX..X..XX", ".XXXXXXX."],
    "eyeorb":  ["..XXXXX..", ".X.....X.", "X..XXX..X", "X.XX.XX.X",
                "X..XXX..X", ".X.....X.", "..XXXXX.."],
    "branch":  ["X.......X", ".X.....X.", "..X...X..", "...X.X...",
                "....X....", "....X....", "...XXX..."],
    "lance":   ["....X....", "...XXX...", "..XX.XX..", "....X....",
                "....X....", "....X....", "...XXX..."],
    "gear":    ["..X.X.X..", ".XXXXXXX.", "XX.....XX", "X..XXX..X",
                "XX.....XX", ".XXXXXXX.", "..X.X.X.."],
    "star":    ["....X....", "....X....", "X..XXX..X", ".XXXXXXX.",
                "..XXXXX..", ".XX...XX.", "X.......X"],
    "heart":   [".XX...XX.", "XXXX.XXXX", "XXXXXXXXX", "XXXXXXXXX",
                ".XXXXXXX.", "..XXXXX..", "...XXX..."],
    "shield":  ["XXXXXXXXX", "X.......X", "X.XXXXX.X", "X.XXXXX.X",
                ".X.XXX.X.", "..X.X.X..", "...XXX..."],
    "swords":  ["X.......X", ".X.....X.", "..X...X..", "...X.X...",
                "..XXXXX..", "...X.X...", "..X...X.."],
    "block":   ["XXXXXXXXX", "XX.....XX", "X.XXXXX.X", "X.XXXXX.X",
                "X.XXXXX.X", "XX.....XX", "XXXXXXXXX"],
    "query":   ["..XXXXX..", ".X..X..X.", "....X..X.", "...XX.X..",
                "...XX....", ".........", "...XX...."],
}


def emblem(cv, name, cx, cy, c, shade):
    rows = EMBLEMS[name]
    w = len(rows[0])
    x0 = cx - w // 2
    y0 = cy - len(rows) // 2
    for j, row in enumerate(rows):
        for i, ch in enumerate(row):
            if ch == "X":
                cv.f(x0 + i, y0 + j, c)
                if j == len(rows) - 1 or (j + 1 < len(rows)
                                          and rows[j + 1][i] != "X"):
                    cv.f(x0 + i, y0 + j + 1, shade)


# ---------------------------------------------------------------- helm head
def helm_head(cv, pal, kind, crest, face):
    """Great-helm family: Vanguard, Marshal, Duelist, Guardian."""
    if kind == "broad":
        x0, x1, y0, y1 = 17, 46, 12, 45
        r = 9
    elif kind == "sharp":
        x0, x1, y0, y1 = 21, 42, 11, 45
        r = 5
    else:
        x0, x1, y0, y1 = 20, 43, 12, 45
        r = 7
    rounded(cv, x0, y0, x1, y1, pal["mid"], r)
    # vertical shade ramp by column
    for y in range(y0, y1 + 1):
        for x in range(x0, x1 + 1):
            if not cv.fig[y][x]:
                continue
            rel = (x - x0) / float(x1 - x0)
            if rel < 0.16 or (y - y0) < 3:
                cv.f(x, y, pal["light"])
            if rel < 0.07:
                cv.f(x, y, pal["hi"])
            if rel > 0.72:
                cv.f(x, y, pal["dark"])
            if rel > 0.88 or (y1 - y) < 3:
                cv.f(x, y, pal["shadow"])
    # dither bridge on the shadow flank
    for y in range(y0 + 4, y1 - 3):
        bx = x0 + int((x1 - x0) * 0.72)
        thr = (BAYER4[y % 4][bx % 4] + 0.5) / 16.0
        if thr < 0.5:
            cv.f(bx, y, pal["dark"])
    # sharp helm cheek bevels
    if kind == "sharp":
        for k in range(4):
            cv.f(x0 + k, y1 - 2 - k, pal["shadow"])
            cv.f(x1 - k, y1 - 2 - k, pal["shadow"])
    # brow ridge
    cv.frow(24, x0 + 2, x1 - 2, pal["dark"])
    cv.frow(23, x0 + 3, x1 - 3, pal["light"])
    # eye slit
    sl0, sl1 = x0 + 3, x1 - 3
    cv.frow(27, sl0, sl1, pal["shadow"])
    cv.frow(28, sl0, sl1, pal["shadow"])
    cv.frow(26, sl0, sl1, pal["outline"])
    if face == "visor_open":
        cv.frect(sl0, 26, sl1, 31, hx("#caa07a"))     # raised visor: face
        cv.frow(31, sl0, sl1, hx("#9a6f4c"))
        cv.f(x0 + 6, 28, pal["outline"])
        cv.f(x1 - 6, 28, pal["outline"])
        cv.f(x0 + 6, 29, hx("#3a2614"))
        cv.f(x1 - 6, 29, hx("#3a2614"))
    else:
        cv.f(x0 + 6, 28, pal["eye"])
        cv.f(x0 + 7, 28, pal["eye"])
        cv.f(x1 - 6, 28, pal["eye"])
        cv.f(x1 - 7, 28, pal["eye"])
        cv.f(x0 + 6, 27, mix(pal["eye"], (255, 255, 255), 0.5))
        cv.f(x1 - 6, 27, mix(pal["eye"], (255, 255, 255), 0.5))
    # breather slot
    if kind != "broad":
        cv.fcol(32, 31, 40, pal["shadow"])
        cv.f(31, 36, pal["dark"])
        cv.f(33, 36, pal["dark"])
    else:
        for yy in range(33, 41):
            cv.f(31, yy, pal["shadow"])
            cv.f(33, yy, pal["shadow"])
    # rivets
    for ry in (20, 38):
        cv.f(x0 + 2, ry, pal["hi"])
        cv.f(x1 - 2, ry, pal["hi"])
    # crest
    cx = 32
    if crest == "plume_up":
        cv.frect(cx - 2, 9, cx + 2, 13, pal["dark"])          # socket
        widths = [1, 2, 3, 4, 4, 4, 4, 3, 3, 3, 2, 2, 2]      # tip -> base
        for j, w in enumerate(widths):
            cv.frow(j, cx - w, cx + w, pal["trim"])
            cv.f(cx - w, j, mix(pal["trim"], (255, 255, 255), 0.45))
            cv.f(cx + w, j, pal["dark"])
        for y in range(1, 13):                                # lit spine
            cv.f(cx, y, mix(pal["trim"], (255, 240, 200), 0.55))
        for j in range(2, 12, 3):                             # feather notches
            cv.f(cx - widths[j] - 1, j, pal["trim"])
    elif crest == "brush_h":
        for x in range(x0 + 1, x1):                           # transverse arc
            rel = abs(x - cx) / ((x1 - x0) / 2.0)
            h = int(round(6 * (1 - rel * rel)))
            for k in range(h):
                cv.f(x, 12 - k, pal["trim"])
            if h > 0:
                cv.f(x, 13 - h, mix(pal["trim"], (255, 255, 255), 0.4))
        cv.frow(13, x0 + 1, x1 - 1, pal["dark"])
        cv.frect(cx - 1, 13, cx + 1, 15, pal["dark"])         # crest mount
    elif crest == "blade":
        widths = [0, 0, 1, 1, 1, 2, 2, 2, 2, 3, 3, 3]         # sharp fin
        for j, w in enumerate(widths):
            cv.frow(j, cx - w, cx + w, pal["trim"])
            cv.f(cx + w, j, pal["dark"])
            cv.f(cx - w, j, mix(pal["trim"], (255, 255, 255), 0.4))
        cv.fcol(cx, 0, 11, mix(pal["trim"], (255, 255, 255), 0.3))
        cv.frect(cx - 2, 11, cx + 2, 13, pal["dark"])         # socket
    elif crest == "ridge":
        for x in range(x0 + 3, x1 - 2):                       # low broad comb
            rel = abs(x - cx) / ((x1 - x0) / 2.0)
            h = int(round(5 * (1 - rel * rel)))
            for k in range(h):
                cv.f(x, 12 - k, pal["trim"])
            if h > 0:
                cv.f(x, 13 - h, mix(pal["trim"], (255, 255, 255), 0.4))
        cv.frow(13, x0 + 3, x1 - 3, pal["dark"])
        for x in range(x0 + 5, x1 - 4, 3):                    # comb teeth
            cv.f(x, 8, pal["dark"])


# ---------------------------------------------------------------- cowl head
def cowl_head(cv, pal, depth):
    """Depth family: Loremaster (deep layered) / Oracle (minimal)."""
    # outer cowl
    for y in range(8, 52):
        if y < 14:
            hw = 5 + (y - 8)
        elif y < 30:
            hw = 11 + (y - 14) * 11 // 16
        else:
            hw = 22 + (y - 30) * 4 // 22
        hw = min(hw, 25)
        cv.frow(y, 32 - hw, 32 + hw, pal["mid"])
    # shade ramp
    for y in range(8, 52):
        for x in range(W):
            if not cv.fig[y][x]:
                continue
            if x < 26:
                cv.f(x, y, pal["light"])
            if x < 22:
                cv.f(x, y, pal["hi"])
            if x > 39:
                cv.f(x, y, pal["dark"])
            if x > 44:
                cv.f(x, y, pal["shadow"])
    # fold lines
    if depth == "deep":
        for fx in (24, 28, 36, 40):
            for y in range(20, 50):
                if cv.fig[y][fx]:
                    cv.f(fx, y, pal["shadow"] if fx > 32 else pal["light"])
        # inner second hood line
        for y in range(12, 30):
            cv.f(32 - (8 + (y - 12) // 2), y, pal["dark"])
            cv.f(32 + (8 + (y - 12) // 2), y, pal["dark"])
    else:
        for y in range(22, 50):
            cv.f(27, y, pal["light"])
            cv.f(37, y, pal["shadow"])
    # face cavity
    for y in range(20, 40):
        hw = 9 if 24 <= y <= 35 else 7
        cv.frect(32 - hw, y, 32 + hw, y, pal["outline"])
    for y in range(21, 39):
        hw = 8 if 24 <= y <= 34 else 6
        cv.frect(32 - hw, y, 32 + hw, y, hx("#1b1622"))
    # eyes
    if depth == "deep":
        cv.frect(27, 28, 29, 29, pal["eye"])
        cv.frect(35, 28, 37, 29, pal["eye"])
        cv.f(27, 28, mix(pal["eye"], (255, 255, 255), 0.6))
        cv.f(35, 28, mix(pal["eye"], (255, 255, 255), 0.6))
    else:
        cv.frect(30, 27, 34, 29, pal["eye"])
        cv.frect(31, 28, 33, 28, mix(pal["eye"], (255, 255, 255), 0.6))
    # peak gem
    cv.f(32, 9, pal["trim"])
    cv.f(32, 10, pal["trim"])
    cv.f(31, 10, mix(pal["trim"], (255, 255, 255), 0.5))


# ---------------------------------------------------------------- ranger head
def ranger_head(cv, pal, openhood, feather_up):
    """Breadth family: Pathfinder (feathered, open) / Lancer (tight)."""
    # peaked hood
    for y in range(7, 50):
        if y < 26:
            hw = 3 + (y - 7) * 16 // 19
        else:
            hw = 19 + (y - 26) * 5 // 24
        hw = min(hw, 24)
        cv.frow(y, 32 - hw, 32 + hw, pal["mid"])
    # peak tip
    cv.fcol(32, 5, 8, pal["dark"])
    # shade ramp
    for y in range(5, 50):
        for x in range(W):
            if not cv.fig[y][x]:
                continue
            if x < 27:
                cv.f(x, y, pal["light"])
            if x < 23:
                cv.f(x, y, pal["hi"])
            if x > 38:
                cv.f(x, y, pal["dark"])
            if x > 43:
                cv.f(x, y, pal["shadow"])
    # hood rim — lit edge left, shadowed edge right
    fw = 11 if openhood else 8
    for y in range(18, 42):
        rim = fw + abs(y - 30) // 4
        cv.f(32 - rim, y, pal["light"])
        cv.f(32 + rim, y, pal["dark"])
    # face
    sk = hx("#e3b287") if openhood else hx("#c79972")
    skd = hx("#a9774f")
    for y in range(21, 40):
        hw = (fw - 2) - abs(y - 29) // 3
        if hw < 2:
            continue
        cv.frect(32 - hw, y, 32 + hw, y, sk)
    for y in range(21, 40):
        hw = (fw - 2) - abs(y - 29) // 3
        if hw >= 2:
            cv.fcol(32 + hw, y, y, skd)
    cv.frow(39, 30, 34, skd)
    # eyes
    ey = 29
    cv.frect(29, ey, 30, ey + 1, pal["outline"])
    cv.frect(34, ey, 35, ey + 1, pal["outline"])
    cv.f(29, ey, pal["eye"])
    cv.f(34, ey, pal["eye"])
    # brow / focus line for the tight (Lancer) variant
    if not openhood:
        cv.frow(26, 28, 36, skd)
    # feather (Pathfinder only — Lancer stays unadorned, deeper green)
    if feather_up:
        fx = 46
        vane = [1, 1, 2, 2, 3, 3, 3, 3, 3, 2, 2, 1, 1]   # tip -> quill
        for j, w in enumerate(vane):
            y = 5 + j
            cv.frow(y, fx - w, fx + w, pal["trim"])
            cv.f(fx - w, y, mix(pal["trim"], (255, 255, 255), 0.4))
            cv.f(fx + w, y, pal["dark"])
        cv.fcol(fx, 6, 5 + len(vane) + 2, pal["dark"])    # quill shaft
        for j in range(2, len(vane) - 2, 3):              # serrations
            cv.f(fx + vane[j] + 1, 5 + j, pal["trim"])
            cv.f(fx - vane[j] - 1, 5 + j, pal["trim"])


# ---------------------------------------------------------------- hat head
def hat_head(cv, pal, tall):
    """Rationale family: Sorcerer (tall hat) / Artificer (short, goggles)."""
    # face base
    sk = hx("#e6b78b")
    skd = hx("#ad7c54")
    for y in range(20, 44):
        hw = 11 - abs(y - 30) // 4
        cv.frect(32 - hw, y, 32 + hw, y, sk)
    for y in range(20, 44):
        hw = 11 - abs(y - 30) // 4
        cv.fcol(32 + hw, y, y, skd)
        cv.fcol(32 + hw - 1, y, y, skd if y > 32 else sk)
    cv.frow(43, 29, 35, skd)
    # cone hat
    apex_y = 3 if tall else 11
    brim_y = 22 if tall else 19
    for y in range(apex_y, brim_y):
        fr = (y - apex_y) / float(brim_y - apex_y)
        hw = int(round(1 + fr * (13 if tall else 15)))
        lean = int(round((1 - fr) * (5 if tall else 2)))
        cv.frow(y, 32 - hw + lean, 32 + hw + lean, pal["mid"])
    for y in range(apex_y, brim_y):
        for x in range(W):
            if not cv.fig[y][x]:
                continue
            if x < 30:
                cv.f(x, y, pal["light"])
            if x < 26:
                cv.f(x, y, pal["hi"])
            if x > 36:
                cv.f(x, y, pal["dark"])
    # brim
    cv.frow(brim_y, 17, 47, pal["dark"])
    cv.frow(brim_y - 1, 19, 45, pal["mid"])
    cv.frow(brim_y - 1, 19, 27, pal["light"])
    cv.frow(brim_y, 17, 23, pal["mid"])
    if tall:
        # star on the hat
        emblem(cv, "star", 33, 13, pal["eye"], pal["dark"])
        # shadowed eyes under the brim
        cv.frect(28, 26, 30, 27, pal["outline"])
        cv.frect(34, 26, 36, 27, pal["outline"])
        cv.f(29, 26, pal["eye"])
        cv.f(35, 26, pal["eye"])
        cv.frow(24, 24, 40, mix(sk, (0, 0, 0), 0.35))    # brim shadow
    else:
        # goggle band across the forehead
        cv.frow(24, 22, 42, pal["trim"])
        cv.frow(25, 22, 42, pal["dark"])
        for gx in (27, 37):
            rounded(cv, gx - 4, 21, gx + 4, 28, pal["dark"], 3)
            rounded(cv, gx - 3, 22, gx + 3, 27, pal["eye"], 2)
            cv.f(gx - 2, 23, mix(pal["eye"], (255, 255, 255), 0.7))
        cv.frow(31, 33, 31, pal["dark"])
        # mouth
        cv.frow(38, 30, 34, skd)
    cv.frow(20, 25, 39, hx("#3a2a1c"))   # hair line under brim/band


# ---------------------------------------------------------------- face head
def face_head(cv, pal, sealed):
    """Warmth family: Bard (open warm face) / Sentinel (sealed visor)."""
    sk = hx("#eebb8c")
    skm = hx("#d49a6a")
    skd = hx("#a9744a")
    # head
    rounded(cv, 21, 14, 43, 44, sk, 8)
    for y in range(14, 45):
        for x in range(21, 44):
            if not cv.fig[y][x]:
                continue
            if x < 26:
                cv.f(x, y, mix(sk, (255, 255, 255), 0.25))
            if x > 38:
                cv.f(x, y, skm)
            if x > 41:
                cv.f(x, y, skd)
    # hair
    cv.frect(20, 12, 44, 19, hx("#5a3a1c"))
    rounded(cv, 20, 11, 44, 18, hx("#6e4824"), 6)
    cv.frow(12, 24, 33, hx("#8a5e30"))
    cv.fcol(21, 16, 26, hx("#5a3a1c"))
    cv.fcol(43, 16, 26, hx("#3f2814"))
    # circlet
    cv.frow(17, 22, 42, pal["trim"])
    cv.frow(16, 24, 40, mix(pal["trim"], (255, 255, 255), 0.4))
    cv.frow(18, 22, 42, pal["dark"])
    cv.f(32, 15, pal["eye"])
    cv.f(32, 14, mix(pal["eye"], (255, 255, 255), 0.6))
    if sealed:
        # steel visor drops over the face
        for y in range(22, 41):
            hw = 12 - max(0, y - 36)
            cv.frect(32 - hw, y, 32 + hw, y, pal["mid"])
        for y in range(22, 41):
            for x in range(W):
                if not cv.fig[y][x] or y < 22:
                    continue
                if 19 < x < 46:
                    if x < 27:
                        cv.f(x, y, pal["light"])
                    if x < 24:
                        cv.f(x, y, pal["hi"])
                    if x > 38:
                        cv.f(x, y, pal["dark"])
                    if x > 42:
                        cv.f(x, y, pal["shadow"])
        cv.frow(22, 21, 43, pal["trim"])          # visor brow trim
        cv.frow(30, 23, 41, pal["outline"])       # eye slit
        cv.frow(31, 23, 41, pal["outline"])
        cv.frow(30, 26, 30, pal["eye"])
        cv.frow(30, 35, 39, pal["eye"])
        cv.fcol(32, 33, 40, pal["shadow"])        # breather ridge
    else:
        # warm open face
        cv.frect(27, 27, 29, 29, hx("#ffffff"))
        cv.frect(34, 27, 36, 29, hx("#ffffff"))
        cv.frect(28, 28, 29, 29, hx("#3b2a18"))
        cv.frect(35, 28, 36, 29, hx("#3b2a18"))
        cv.f(28, 28, pal["eye"])
        cv.f(35, 28, pal["eye"])
        cv.frow(25, 27, 30, hx("#5a3a1c"))        # brows
        cv.frow(25, 34, 37, hx("#5a3a1c"))
        cv.f(32, 33, skd)                          # nose
        cv.f(32, 34, skm)
        cv.frow(37, 29, 35, hx("#b06a4a"))         # smile
        cv.f(28, 37, hx("#b06a4a"))
        cv.f(36, 37, hx("#b06a4a"))
        cv.f(26, 33, mix(sk, pal["trim"], 0.45))   # cheek warmth
        cv.f(38, 33, mix(skm, pal["trim"], 0.4))


# ---------------------------------------------------------------- wildcard
def wildcard_head(cv, pal):
    """No dominant dial: split-tone harlequin, four-hue crown."""
    hues = [hx("#c2410c"), hx("#0e7490"), hx("#15803d"), hx("#7c3a9c")]
    sk = hx("#e6c0a0")
    rounded(cv, 21, 14, 43, 44, sk, 8)
    # split-tone shading: left warm, right cool
    for y in range(14, 45):
        for x in range(21, 44):
            if not cv.fig[y][x]:
                continue
            if x < 32:
                base = mix(sk, hx("#c2410c"), 0.12)
            else:
                base = mix(sk, hx("#0e7490"), 0.12)
            if x < 25:
                base = mix(base, (255, 255, 255), 0.25)
            if x > 40:
                base = mix(base, (0, 0, 0), 0.22)
            cv.f(x, y, base)
    # facet diamond — one clean four-hue outline, no checker noise
    quad = [hx("#c2410c"), hx("#0e7490"), hx("#7c3a9c"), hx("#15803d")]
    R = 9
    for k in range(R):
        cv.f(32 - k, 30 - (R - k), quad[0])     # top-left edge
        cv.f(32 + k, 30 - (R - k), quad[1])     # top-right edge
        cv.f(32 + k, 30 + (R - k), quad[2])     # bottom-right edge
        cv.f(32 - k, 30 + (R - k), quad[3])     # bottom-left edge
    # eyes — heterochromia
    cv.frect(27, 27, 29, 29, hx("#ffffff"))
    cv.frect(34, 27, 36, 29, hx("#ffffff"))
    cv.f(28, 28, hx("#c2410c"))
    cv.f(35, 28, hx("#0e7490"))
    cv.frow(37, 29, 35, hx("#9a5a3a"))            # neutral mouth
    # four-point jester crown
    cv.frect(22, 12, 42, 16, pal["dark"])
    cv.frow(12, 22, 42, pal["mid"])
    pts = [24, 30, 34, 40]
    for i, px in enumerate(pts):
        c = hues[i]
        for j in range(5):
            cv.frow(11 - j, px - (2 - abs(2 - j)), px + (2 - abs(2 - j)), c)
        cv.f(px, 4, mix(c, (255, 255, 255), 0.6))
    cv.frow(16, 22, 42, hx("#3a3024"))


# ---------------------------------------------------------------- palettes
P = {
    "vanguard": dict(outline="#241208", shadow="#5a3417", dark="#8a5520",
                     mid="#b9803a", light="#d9a456", hi="#f3cd8c",
                     eye="#ff9a3c", trim="#c2410c"),
    "marshal":  dict(outline="#1f160d", shadow="#48381f", dark="#6f5a32",
                     mid="#937a44", light="#b89e63", hi="#dcc792",
                     eye="#9ab4c4", trim="#5d7a8c"),
    "loremaster": dict(outline="#0b1322", shadow="#1c2f4f", dark="#2f4c7d",
                       mid="#46689f", light="#6f93c2", hi="#a7c6e6",
                       eye="#ffd673", trim="#c9a24e"),
    "oracle":   dict(outline="#0c2128", shadow="#214b54", dark="#357a86",
                     mid="#56a3ad", light="#8fc8cf", hi="#cfe9ec",
                     eye="#ffe39a", trim="#e0d2a6"),
    "pathfinder": dict(outline="#11220c", shadow="#2b431d", dark="#456a2c",
                       mid="#669440", light="#8fbd60", hi="#c7e09a",
                       eye="#ffe07a", trim="#b9763a"),
    "lancer":   dict(outline="#0e1a0a", shadow="#243a1a", dark="#395c28",
                     mid="#527e3c", light="#7aa45a", hi="#a9c585",
                     eye="#e9d27e", trim="#8a5a30"),
    "artificer": dict(outline="#2a1a0a", shadow="#553715", dark="#855a20",
                      mid="#b3812f", light="#d9a94e", hi="#f4d58e",
                      eye="#62c6d6", trim="#7a5226"),
    "sorcerer": dict(outline="#170d26", shadow="#2e1d48", dark="#4c3274",
                     mid="#6f4ca0", light="#9b78c9", hi="#d2bfec",
                     eye="#ffd45a", trim="#3b6f7a"),
    "bard":     dict(outline="#2c1d0c", shadow="#5a3e18", dark="#8a6526",
                     mid="#bb8f3c", light="#e0bd62", hi="#ffe7ad",
                     eye="#3b6f7a", trim="#e0564f"),
    "sentinel": dict(outline="#15191e", shadow="#2d343c", dark="#4c5660",
                     mid="#76828f", light="#a9b4be", hi="#dfe5ea",
                     eye="#8fbcd8", trim="#c9a24e"),
    "duelist":  dict(outline="#250908", shadow="#511712", dark="#83271d",
                     mid="#b23a2a", light="#d76a52", hi="#f0b095",
                     eye="#ffd24a", trim="#283041"),
    "guardian": dict(outline="#1d0807", shadow="#3a1611", dark="#5f2a1e",
                     mid="#883c2c", light="#b06450", hi="#d79e89",
                     eye="#f0c270", trim="#283041"),
    "wildcard": dict(outline="#1a1814", shadow="#34302a", dark="#5b5246",
                     mid="#8a7f6a", light="#b3a890", hi="#dfd6c4",
                     eye="#ffffff", trim="#9a8f78"),
}


def palette(name):
    return {k: (hx(v) if isinstance(v, str) else v)
            for k, v in P[name].items()}


# ---------------------------------------------------------------- per class
def render(name):
    cv = Canvas()
    pal = palette(name)
    background(cv, pal["mid"])

    if name == "vanguard":
        neck(cv, pal)
        shoulders(cv, pal)
        helm_head(cv, pal, "great", "plume_up", "closed")
        emblem(cv, "chevron", 32, 54, pal["trim"], pal["shadow"])
    elif name == "marshal":
        neck(cv, pal)
        shoulders(cv, pal)
        helm_head(cv, pal, "great", "brush_h", "visor_open")
        emblem(cv, "baton", 32, 55, pal["trim"], pal["shadow"])
    elif name == "loremaster":
        shoulders(cv, pal, placket=False)
        cowl_head(cv, pal, "deep")
        emblem(cv, "book", 32, 56, pal["trim"], pal["shadow"])
    elif name == "oracle":
        shoulders(cv, pal, placket=False)
        cowl_head(cv, pal, "min")
        emblem(cv, "eyeorb", 32, 56, pal["trim"], pal["shadow"])
    elif name == "pathfinder":
        shoulders(cv, pal, placket=False)
        ranger_head(cv, pal, openhood=True, feather_up=True)
        emblem(cv, "branch", 32, 55, pal["trim"], pal["shadow"])
    elif name == "lancer":
        shoulders(cv, pal, placket=False)
        ranger_head(cv, pal, openhood=False, feather_up=False)
        emblem(cv, "lance", 32, 55, pal["trim"], pal["shadow"])
    elif name == "artificer":
        neck(cv, pal)
        shoulders(cv, pal)
        hat_head(cv, pal, tall=False)
        emblem(cv, "gear", 32, 55, pal["eye"], pal["shadow"])
    elif name == "sorcerer":
        shoulders(cv, pal, placket=False)
        hat_head(cv, pal, tall=True)
        emblem(cv, "star", 32, 55, pal["eye"], pal["shadow"])
    elif name == "bard":
        neck(cv, pal)
        shoulders(cv, pal)
        face_head(cv, pal, sealed=False)
        emblem(cv, "heart", 32, 55, pal["trim"], pal["shadow"])
    elif name == "sentinel":
        neck(cv, pal)
        shoulders(cv, pal)
        face_head(cv, pal, sealed=True)
        emblem(cv, "shield", 32, 55, pal["trim"], pal["shadow"])
    elif name == "duelist":
        neck(cv, pal)
        shoulders(cv, pal)
        helm_head(cv, pal, "sharp", "blade", "closed")
        emblem(cv, "swords", 32, 54, pal["eye"], pal["shadow"])
    elif name == "guardian":
        neck(cv, pal)
        shoulders(cv, pal)
        helm_head(cv, pal, "broad", "ridge", "closed")
        emblem(cv, "block", 32, 55, pal["eye"], pal["shadow"])
    elif name == "wildcard":
        neck(cv, pal)
        shoulders(cv, pal)
        wildcard_head(cv, pal)
        emblem(cv, "query", 32, 55, pal["hi"], pal["shadow"])
    else:
        raise ValueError(name)

    outline_pass(cv, pal["outline"])
    return cv


def to_image(cv):
    img = Image.new("RGB", (W, H))
    for y in range(H):
        for x in range(W):
            img.putpixel((x, y), cv.p[y][x])
    return img.resize((W * SCALE, H * SCALE), Image.NEAREST)


CLASSES = ["vanguard", "marshal", "loremaster", "oracle", "pathfinder",
           "lancer", "artificer", "sorcerer", "bard", "sentinel",
           "duelist", "guardian", "wildcard"]


def main():
    imgs = {}
    for name in CLASSES:
        cv = render(name)
        img = to_image(cv)
        img.save(os.path.join(OUT_DIR, name + ".png"))
        imgs[name] = img
        print("rendered", name)
    # contact sheet, 4 columns
    cols, cell, pad = 4, W * SCALE // 2, 8
    rows = (len(CLASSES) + cols - 1) // cols
    sheet = Image.new("RGB", (cols * (cell + pad) + pad,
                              rows * (cell + pad + 14) + pad), (250, 246, 238))
    for i, name in enumerate(CLASSES):
        r, c = divmod(i, cols)
        x = pad + c * (cell + pad)
        y = pad + r * (cell + pad + 14)
        sheet.paste(imgs[name].resize((cell, cell), Image.NEAREST), (x, y))
    # review aid only — written to the temp dir, never committed
    contact = os.path.join(tempfile.gettempdir(), "whoami-portraits-contact.png")
    sheet.save(contact)
    print("contact sheet ->", contact)


if __name__ == "__main__":
    main()
