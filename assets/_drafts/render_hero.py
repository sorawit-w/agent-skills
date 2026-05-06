#!/usr/bin/env python3
"""Re-render the hero banner from the source ChatGPT PNG.

Input:  assets/_drafts/hero-draft-05-chatgpt.png  (1916x821, 21:9)
Output: assets/hero.png                            (1916x559, 24:7)

Composites pixel-font text overlay (VT323) on the quiet left-third.
Text sizes calibrated for GitHub README display (container ~916px, source 1916px,
~48% downscale — sizes here are 2x the visual target).

To change copy or fonts, edit constants below and re-run:
  python3 assets/_drafts/render_hero.py
Then re-quantize + optimize:
  python3 -c "from PIL import Image; Image.open('assets/hero.png').convert('RGB').quantize(colors=256).save('assets/hero.png', 'PNG', optimize=True)"
  python3 -c "import oxipng; oxipng.optimize('assets/hero.png', level=6, strip=oxipng.StripChunks.safe())"
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
title_f   = ImageFont.truetype(FONT, 120)
tagline_f = ImageFont.truetype(FONT, 48)
caption_f = ImageFont.truetype(FONT, 32)

def shadow_text(pos, text, font, fill=CHARCOAL, shadow=SHADOW, offset=(3, 3)):
    sx, sy = offset
    x, y = pos
    draw.text((x+sx, y+sy), text, fill=shadow, font=font)
    draw.text(pos, text, fill=fill, font=font)

X = 110
shadow_text((X, 100), TITLE,   title_f)
shadow_text((X, 240), TAGLINE, tagline_f)
shadow_text((X, 400), CAPTION, caption_f)

img.save(OUT, "PNG", optimize=True)
print(f"Saved {OUT} ({OUT.stat().st_size/1024:.0f} KB, {img.size[0]}x{img.size[1]})")
