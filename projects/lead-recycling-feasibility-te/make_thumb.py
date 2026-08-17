#!/usr/bin/env python3
"""Thumbnail for the Lead-Acid Battery Recycling FEASIBILITY (Telugu, Video 2)."""
import os
from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 720
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "thumbnail.png")

TE = "/System/Library/Fonts/Supplemental/Telugu Sangam MN.ttc"
EN_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
EN = "/System/Library/Fonts/Supplemental/Arial.ttf"

def te(sz):  return ImageFont.truetype(TE, sz)
def eb(sz):  return ImageFont.truetype(EN_BOLD, sz)
def en(sz):  return ImageFont.truetype(EN, sz)

# palette (video identity)
BG0, BG1 = (9, 18, 30), (16, 32, 48)
CYAN   = (34, 211, 238)
AMBER  = (251, 191, 36)
GREEN  = (52, 211, 153)
RED    = (251, 113, 133)
WHITE  = (238, 244, 250)
MUTE   = (150, 170, 190)

img = Image.new("RGB", (W, H), BG0)
d = ImageDraw.Draw(img)

# vertical gradient
for y in range(H):
    t = y / H
    r = int(BG0[0] + (BG1[0]-BG0[0]) * t)
    g = int(BG0[1] + (BG1[1]-BG0[1]) * t)
    b = int(BG0[2] + (BG1[2]-BG0[2]) * t)
    d.line([(0, y), (W, y)], fill=(r, g, b))

# subtle dot grid
for gx in range(0, W, 40):
    for gy in range(0, H, 40):
        d.ellipse([gx-1, gy-1, gx+1, gy+1], fill=(28, 44, 62))

def text(xy, s, f, fill, anchor="la"):
    d.text(xy, s, font=f, fill=fill, anchor=anchor)

def tw(s, f):
    return d.textlength(s, font=f)

# ---- left column ----
LX = 64
# kicker chip
kick = "FEASIBILITY  ·  పార్ట్ 2"
kf = eb(26)
kfw = tw("FEASIBILITY  ·  ", kf) + tw("పార్ట్ 2", te(26))
d.rounded_rectangle([LX, 60, LX + 430, 110], radius=12, fill=(15, 45, 55), outline=CYAN, width=2)
text((LX+22, 84), "FEASIBILITY  ·  ", kf, CYAN, anchor="lm")
text((LX+22+tw("FEASIBILITY  ·  ", kf), 84), "పార్ట్ 2", te(26), CYAN, anchor="lm")

# giant hook
text((LX, 150), "లాభమా?", te(140), AMBER, anchor="la")
text((LX, 300), "నష్టమా?", te(140), RED, anchor="la")

# subtitle
text((LX, 452), "లెడ్ బ్యాటరీ రీసైక్లింగ్", te(54), WHITE, anchor="la")
text((LX, 514), "వ్యాపారం — నిజాయితీ తీర్పు", te(46), CYAN, anchor="la")

def dotstrip(x, y, words, f, fill, gap=26, r=4):
    for i, w in enumerate(words):
        if i:
            d.ellipse([x+gap-r, y-r, x+gap+r, y+r], fill=(70, 95, 120))
            x += gap*2
        text((x, y), w, f, fill, anchor="lm")
        x += tw(w, f)

# bottom strip
d.line([(LX, 588), (LX+760, 588)], fill=(40, 60, 80), width=2)
dotstrip(LX, 618, ["మార్కెట్", "పోటీ", "రిస్క్", "తీర్పు"], te(36), MUTE)
dotstrip(LX, 672, ["హైదరాబాద్", "గుంటూరు"], te(34), GREEN)

# ---- right column: verdict stamp + battery/recycle motif ----
CX, CY, R = 1050, 250, 150
# glow rings
for i, col in enumerate([(20,60,50),(24,80,66),(30,110,86)]):
    d.ellipse([CX-R-18+i*6, CY-R-18+i*6, CX+R+18-i*6, CY+R+18-i*6], outline=col, width=6)
d.ellipse([CX-R, CY-R, CX+R, CY+R], fill=(12, 40, 34), outline=GREEN, width=6)
text((CX, CY-46), "తీర్పు", te(46), WHITE, anchor="mm")
text((CX, CY+26), "GO", eb(96), GREEN, anchor="mm")
text((CX, CY+96), "(with discipline)", en(24), MUTE, anchor="mm")

# battery icon bottom-right
bx, by, bw, bh = 940, 470, 190, 96
d.rounded_rectangle([bx, by, bx+bw, by+bh], radius=12, outline=AMBER, width=6)
d.rounded_rectangle([bx+bw, by+28, bx+bw+16, by+bh-28], radius=4, fill=AMBER)  # terminal
# charge segments
for i in range(3):
    sx = bx + 18 + i*56
    d.rounded_rectangle([sx, by+18, sx+40, by+bh-18], radius=6, fill=GREEN if i<2 else (60,80,70))
# recycle label (drawn triangle mark + text, no emoji font)
mx, my = bx+8, by+bh+34
for a in range(3):
    import math
    ang = math.radians(90 + a*120)
    d.regular_polygon((mx, my, 11), 3, rotation=a*120 - 30, outline=GREEN, width=3)
text((mx+26, my), "SECONDARY LEAD", en(24), MUTE, anchor="lm")

img.save(OUT)
print("saved", OUT, img.size)
