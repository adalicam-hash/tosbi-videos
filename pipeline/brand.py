import cairosvg, math
from tosbi import *
from render import text
# --- profile 800x800 ---
p=['<defs><radialGradient id="g" cx="0.5" cy="0.4" r="0.7"><stop offset="0" stop-color="#FFF6D6"/><stop offset="1" stop-color="#FFD27A"/></radialGradient></defs>',
   '<rect width="800" height="800" fill="url(#g)"/>',
   '<circle cx="400" cy="400" r="330" fill="#fff" opacity="0.35"/>',
   '<ellipse cx="400" cy="610" rx="400" ry="90" fill="#9AD67E"/>',
   tosbi(350,600,1.25,lid=0.0),
   sparkle(150,220,1.2), sparkle(660,170,0.9,color="#FF9AA2"), sparkle(600,300,0.6)]
cairosvg.svg2png(bytestring=f'<svg xmlns="http://www.w3.org/2000/svg" width="800" height="800">{"".join(p)}</svg>'.encode(),write_to="tosbi_profile_800.png")
# --- banner 2560x1440, safe area 1546x423 centered (x 507-2053, y 508-931) ---
W,H=2560,1440
clouds="".join(f'<g transform="translate({x},{y}) scale({s})" fill="#fff"><circle cx="-60" cy="10" r="50"/><circle cx="0" cy="-15" r="65"/><circle cx="65" cy="10" r="48"/><rect x="-110" y="10" width="225" height="50" rx="25"/></g>' for x,y,s in [(300,300,1.3),(1250,220,1.0),(2250,330,1.4),(900,420,0.7),(1900,180,0.8)])
flowers="".join(f'<g transform="translate({x},{1180+(i%3)*70})"><circle r="20" fill="{c}"/><circle r="9" fill="#FFE27A"/></g>' for i,(x,c) in enumerate([(120,"#FF9AA2"),(380,"#fff"),(620,"#C3A6FF"),(1500,"#FF9AA2"),(1800,"#fff"),(2100,"#C3A6FF"),(2400,"#FF9AA2"),(2000,"#fff"),(250,"#C3A6FF")]))
b=['<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8FD3FF"/><stop offset="1" stop-color="#E9F7FF"/></linearGradient></defs>',
   f'<rect width="{W}" height="{H}" fill="url(#sky)"/>',
   '<circle cx="2300" cy="180" r="110" fill="#FFE27A"/><circle cx="2300" cy="180" r="150" fill="#FFE27A" opacity="0.3"/>',
   clouds,
   f'<path d="M 0 930 Q 600 820 1300 900 T {W} 880 L {W} {H} L 0 {H} Z" fill="#B7E59A"/>',
   f'<rect x="0" y="990" width="{W}" height="{H-990}" fill="#9AD67E"/>', flowers,
   tosbi(690,912,0.95,expr="talk",lid=0.75),
   ball(700,640,34,"#E94B3C"), ball(780,605,28,"#FFC93C"), ball(615,610,27,"#3C8DE9"),
   sparkle(560,680,0.8), sparkle(870,650,0.7,color="#FF9AA2"),
   text(1535,650,"Tosbi &amp; Friends",112,"#2E8B57"),
   text(1535,775,"Learn colors, numbers &amp; kind habits",44,"#3B2A20"),
   text(1535,850,"Ages 2–6 · New episodes every week",38,"#7A6A5A"),
]
cairosvg.svg2png(bytestring=f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">{"".join(b)}</svg>'.encode(),write_to="tosbi_banner_2560x1440.png")
# preview with safe-area guide
from PIL import Image, ImageDraw
im=Image.open("tosbi_banner_2560x1440.png").convert("RGB"); d=ImageDraw.Draw(im); d.rectangle([507,508,2053,931],outline="red",width=6); im.resize((1280,720)).save("banner_check.png")
