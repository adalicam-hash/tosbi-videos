import cairosvg
from tosbi import *
from render import text
W,H=1800,1100
p=[f'<rect width="{W}" height="{H}" fill="#FFF9EE"/>', text(W/2,80,"Tosbi — Character Sheet",64,"#2E8B57")]
poses=[("Happy",dict()),("Talking",dict(expr="talk")),("Surprised + shell open",dict(expr="surprised",lid=1.0))]
for i,(n,kw) in enumerate(poses):
    x=330+i*570
    p.append(tosbi(x-30,560,1.0,**kw))
    if i==2: p.append(ball(x-40,200,45,"#E94B3C")+sparkle(x-150,230,1.1)+sparkle(x+60,170,0.8))
    p.append(text(x,640,n,40,"#3B2A20"))
pal=[("Skin",SKIN),("Skin shade",SKIN_DARK),("Shell",SHELL),("Shell rim",SHELL_DARK),("Shell spots",PATCH),("Cheeks",CHEEK),("Outline",INK)]
p.append(text(W/2,740,"Color palette",44,"#3B2A20"))
for i,(n,c) in enumerate(pal):
    x=180+i*240
    p.append(f'<rect x="{x-70}" y="790" width="140" height="140" rx="28" fill="{c}" stroke="{INK}" stroke-width="5"/>')
    p.append(text(x,965,n,28,"#3B2A20")); p.append(text(x,1005,c,24,"#7A6A5A"))
p.append(text(W/2,1065,"Calm, curious little turtle. A surprise comes out of the shell in every episode.",28,"#7A6A5A"))
cairosvg.svg2png(bytestring=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">{"".join(p)}</svg>'.encode(),write_to="tosbi_character_sheet.png")
