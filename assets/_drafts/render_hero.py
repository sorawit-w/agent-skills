#!/usr/bin/env python3
"""Re-render the hero banner from the source ChatGPT PNG.

Input:  assets/_drafts/hero-draft-05-chatgpt.png  (1916x821, 21:9)
Output: assets/hero.png                            (1916x559, 24:7)

Composites pixel-font text overlay (VT323) on the quiet left-third.
To change copy or fonts, edit constants below and re-run:
  python3 assets/_drafts/render_hero.py
Then re-optimize with: oxipng -o 4 assets/hero.png
"""
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent.parent
SRC  = REPO / "assets/_drafts/hero-draft-05-chatgpt.png"
OUT  = REPO / "assets/hero.png"
FONT = "/tmp/fonts/VT323-Regular.ttf"   # download: https://github.com/google/fonts/raw/main/ofl/vt323/VT323-Regular.ttf

CHARCOAL = (31, 41, 55)   # #1f2937
SHADOW   = (250, 230, 190)
TITLE    = "agent-skills"
TAGLINE  = "a personal shelf of\nClaude Code plugins"
CAPTION  = "PIXELS · CRAFT · ONE\nSKILL AT A TIME"

img = Image.open(SRC).convert("RGB")
W, H = img.size
target_h = round(W * 7 / 24)
top = (H - target_h) // 2
img = img.crop((0, top, W, top + target_h))

draw = ImageDraw.Draw(img)
title_f   = ImageFont.truetype(FONT, 80)
tagline_f = ImageFont.truetype(FONT, 30)
caption_f = ImageFont.truetype(FONT, 20)

def shadow_text(pos, text, font, fill=CHARCOAL, shadow=SHADOW, offset=(2, 2)):
    sx, sy = offset
    x, y = pos
    draw.text((x+sx, y+sy), text, fill=shadow, font=font)
    draw.text(pos, text, fill=fill, font=font)

X = 120
shadow_text((X, 160), TITLE,   title_f)
shadow_text((X, 250), TAGLINE, tagline_f)
shadow_text((X, 350), CAPTION, caption_f)

img.save(OUT, "PNG", optimize=True)
print(f"Saved {OUT} ({OUT.stat().st_size/1024:.0f} KB, {img.size[0]}x{img.size[1]})")
