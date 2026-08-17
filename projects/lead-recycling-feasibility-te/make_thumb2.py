#!/usr/bin/env python3
"""Alternate (number-led, punchier) thumbnail — feasibility Video 2 (Telugu)."""
import os, math
from PIL import Image, ImageDraw, ImageFont

W, H = 1280, 720
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "thumbnail_b.png")
TE = "/System/Library/Fonts/Supplemental/Telugu Sangam MN.ttc"
EN_BOLD = "/System/Library/Fonts/Supplemental/Arial Bold.ttf"
EN = "/System/Library/Fonts/Supplemental/Arial.ttf"
def te(s): return ImageFont.truetype(TE, s)
def eb(s): return ImageFont.truetype(EN_BOLD, s)
def en(s): return ImageFont.truetype(EN, s)

CYAN=(34,211,238); AMBER=(251,191,36); GREEN=(52,211,153); RED=(251,113,133)
WHITE=(238,244,250); MUTE=(150,170,190)

img = Image.new("RGB", (W, H), (9,18,30))
d = ImageDraw.Draw(img)
# diagonal split tint: left cool-green, right cool-red
for y in range(H):
    for band, (x0,x1,col) in enumerate([(0,W,(9,18,30))]):
        pass
for y in range(H):
    t=y/H
    d.line([(0,y),(W,y)], fill=(int(9+9*t),int(18+16*t),int(30+20*t)))
# soft radial vignettes
def blob(cx,cy,r,col,a):
    for rr in range(r,0,-6):
        f=a*(rr/r)
        d.ellipse([cx-rr,cy-rr,cx+rr,cy+rr], fill=(int(col[0]*f)+int(9*(1-f)),int(col[1]*f)+int(18*(1-f)),int(col[2]*f)+int(30*(1-f))))
blob(140,160,220,(20,60,50),0.25)
blob(1150,600,240,(60,26,34),0.28)
for gx in range(0,W,40):
    for gy in range(0,H,40):
        d.ellipse([gx-1,gy-1,gx+1,gy+1], fill=(28,44,62))

def text(xy,s,f,fill,anchor="la"): d.text(xy,s,font=f,fill=fill,anchor=anchor)
def tw(s,f): return d.textlength(s,font=f)

# top alert chip
d.rounded_rectangle([64,54,64+470,54+56], radius=14, fill=(60,22,30), outline=RED, width=2)
text((86,82),"⚠", eb(30), RED, anchor="lm") if False else None
text((90,82),"5 పెద్ద రిస్క్‌లు", te(34), RED, anchor="lm")
_x=90+tw("5 పెద్ద రిస్క్‌లు",te(34))+18
text((_x,82),"|", en(26), MUTE, anchor="lm")
text((_x+22,82),"నిజాయితీ తీర్పు", te(30), MUTE, anchor="lm")

# headline
text((64,150),"పెట్టుబడి పెట్టాలా?", te(78), WHITE, anchor="la")

# hero number
text((64,258),"₹5 కోట్ల ప్లాంట్", te(96), AMBER, anchor="la")
text((64,372),"— లాభమా, నష్టమా?", te(66), CYAN, anchor="la")

# subject line
text((64,486),"లెడ్-యాసిడ్ బ్యాటరీ రీసైక్లింగ్ వ్యాపారం", te(44), WHITE, anchor="la")

# region dots
def dotstrip(x,y,words,f,fill,gap=24,r=4):
    for i,w in enumerate(words):
        if i:
            d.ellipse([x+gap-r,y-r,x+gap+r,y+r], fill=(70,95,120)); x+=gap*2
        text((x,y),w,f,fill,anchor="lm"); x+=tw(w,f)
d.line([(64,556),(64+840,556)], fill=(40,60,80), width=2)
dotstrip(64,592,["హైదరాబాద్","గుంటూరు","EPR","TSPCB","APPCB"], te(34), GREEN)

# verdict gauge (bottom-right) — needle to GO
gx,gy,gr = 1070,470,150
d.arc([gx-gr,gy-gr,gx+gr,gy+gr], 180, 360, fill=(50,70,90), width=18)
# color arc halves
d.arc([gx-gr,gy-gr,gx+gr,gy+gr], 180, 270, fill=RED, width=18)
d.arc([gx-gr,gy-gr,gx+gr,gy+gr], 270, 360, fill=GREEN, width=18)
ang=math.radians(210)  # needle points into GO side (upper-right region)
nx,ny=gx+math.cos(math.radians(-35))*(gr-30), gy+math.sin(math.radians(-35))*(gr-30)
d.line([(gx,gy),(nx,ny)], fill=WHITE, width=8)
d.ellipse([gx-12,gy-12,gx+12,gy+12], fill=WHITE)
text((gx-gr+6,gy+30),"NO-GO", eb(24), RED, anchor="lm")
text((gx+gr-6,gy+30),"GO", eb(24), GREEN, anchor="rm")
text((gx,gy-64),"తీర్పు", te(40), WHITE, anchor="mm")

img.save(OUT)
print("saved", OUT, img.size)
