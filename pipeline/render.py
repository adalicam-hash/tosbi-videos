import math, subprocess, io, sys, os
TL = os.environ.get("TL", "en")
NEUTRAL = os.environ.get("NEUTRAL") == "1"
import numpy as np
import cairosvg
from PIL import Image
from tosbi import tosbi, ball, sparkle, INK

W, H, FPS, DUR = 1080, 1920, 30, 25.0
GROUND = 1560
TX, TS = 420, 1.85  # Tosbi rest x, scale

LINES = {"01": 0.5, "02": 2.8, "03": 5.0, "04": 7.3, "05": 9.9, "06": 12.1,
         "07": 13.8, "08": 15.8, "09": 16.9, "10": 18.0, "11": 19.3, "12": 21.2}
LEN_EN = {"01": 1.79, "02": 1.81, "03": 1.66, "04": 1.83, "05": 1.45, "06": 1.15,
       "07": 1.47, "08": 0.73, "09": 0.79, "10": 0.81, "11": 1.34, "12": 2.52}
LEN_TR = {"01": 2.04, "02": 1.90, "03": 1.91, "04": 1.99, "05": 1.42, "06": 1.10, "07": 1.42, "08": 0.68, "09": 0.74, "10": 0.61, "11": 1.14, "12": 2.64}
LEN = LEN_EN if TL == "en" else LEN_TR
import json as _json
if os.environ.get("TIMING"):
    _t = _json.load(open(os.environ["TIMING"]))
    LEN = _t["len"]
TXT = {"en": dict(words=["RED", "YELLOW", "BLUE"], knock="knock!", three="3 balls!", bye="Bye-bye!", see="See you tomorrow!"),
       "tr": dict(words=["KIRMIZI", "SARI", "MAVİ"], knock="tık!", three="3 top!", bye="Hoşça kal!", see="Yarın görüşürüz!")}[TL]
KNOCKS = [5.78, 6.12] if TL == "en" else [6.20, 6.72]
if os.environ.get("TIMING"):
    KNOCKS = __import__('json').load(open(os.environ['TIMING']))['knocks']
BALLS = [  # pop time, color, word, target x
    (7.0, "#E94B3C", TXT["words"][0]),
    (9.6, "#FFC93C", TXT["words"][1]),
    (11.8, "#3C8DE9", TXT["words"][2]),
]
BX = [270, 540, 810]
WORD_T = [8.3, 10.6, 12.7]
TR_STARTS = {"01":0.5,"02":2.6,"03":4.57,"04":7.4,"05":10.0,"06":12.2,"07":13.8,"08":15.8,"09":16.9,"10":18.0,"11":18.6,"12":20.3}
TR_DUR = {}
try:
    TR_DUR = {k: v["dur"] for k, v in __import__("json").load(open("trk_info.json")).items()}
except Exception:
    pass
BY = 820
COUNT = [15.8, 16.9, 18.0]
LID_ORIGIN = (TX + (-8) * TS, GROUND + (-175) * TS)


def ease_out(x):
    x = min(max(x, 0), 1)
    return 1 - (1 - x) ** 3


def pop_scale(t, t0, d=0.35):
    if t < t0:
        return 0
    x = (t - t0) / d
    if x >= 1:
        return 1
    return 1 + 0.25 * math.sin(x * math.pi) * (1 - x) + (ease_out(x) - 1)


def speaking(t):
    for k, s in LINES.items():
        if s <= t <= s + LEN[k] - 0.1:
            return True
    for k, s in TR_STARTS.items():
        if k in TR_DUR and s <= t <= s + TR_DUR[k] - 0.1:
            return True
    return False


def background(t):
    clouds = ""
    for i, (cx, cy, s) in enumerate([(200, 520, 1.0), (820, 380, 0.8), (600, 640, 0.6)]):
        x = (cx + t * (12 + 6 * i)) % (W + 300) - 150
        clouds += (f'<g transform="translate({x:.1f},{cy}) scale({s})" fill="#fff">'
                   '<circle cx="-60" cy="10" r="50"/><circle cx="0" cy="-15" r="65"/><circle cx="65" cy="10" r="48"/>'
                   '<rect x="-110" y="10" width="225" height="50" rx="25"/></g>')
    return (
        '<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1">'
        '<stop offset="0" stop-color="#8FD3FF"/><stop offset="1" stop-color="#E9F7FF"/></linearGradient></defs>'
        f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
        f'<circle cx="900" cy="230" r="90" fill="#FFE27A"/><circle cx="900" cy="230" r="120" fill="#FFE27A" opacity="0.3"/>'
        + clouds +
        f'<path d="M 0 {GROUND-80} Q 300 {GROUND-170} 620 {GROUND-90} T {W} {GROUND-110} L {W} {H} L 0 {H} Z" fill="#B7E59A"/>'
        f'<rect x="0" y="{GROUND-20}" width="{W}" height="{H-GROUND+20}" fill="#9AD67E"/>'
        + "".join(f'<g transform="translate({fx},{GROUND+90+(i%2)*120})"><circle r="16" fill="{c}"/><circle r="7" fill="#FFE27A"/></g>'
                  for i, (fx, c) in enumerate([(120, "#FF9AA2"), (330, "#fff"), (560, "#C3A6FF"), (790, "#FF9AA2"), (980, "#fff")]))
    )


def text(x, y, s, size, fill, scale=1.0, op=1.0):
    common = (f'text-anchor="middle" font-family="Poppins" font-weight="bold" font-size="{size}" '
              f'dominant-baseline="middle"')
    return (f'<g transform="translate({x},{y}) scale({scale:.3f})" opacity="{op:.2f}">'
            f'<text {common} fill="#fff" stroke="#fff" stroke-width="{size*0.18 if size>=60 else 0:.0f}" stroke-linejoin="round">{s}</text>'
            f'<text {common} fill="{fill}" stroke="{INK if size>=60 else fill}" stroke-width="{max(1,size*0.03):.0f}" stroke-linejoin="round">{s}</text></g>')


def ball_pos(i, t):
    tp, color, _ = BALLS[i]
    fly = 0.7
    if t < tp:
        return None
    x0, y0 = LID_ORIGIN
    x1, y1 = BX[i], BY
    u = (t - tp) / fly
    if u < 1:
        x = x0 + (x1 - x0) * u
        y = y0 + (y1 - y0) * u - 420 * math.sin(math.pi * u)
        r = 30 + 40 * ease_out(u * 2)
        return x, y, r, 0.0
    # idle float
    y = y1 + 12 * math.sin((t - tp) * 3 + i)
    sq = 0.0
    land = t - tp - fly
    if land < 0.25:
        sq = math.sin(land / 0.25 * math.pi) * 0.6
    # counting jump
    for j, c in enumerate(COUNT):
        if j == i and c <= t < c + 0.6:
            y -= 110 * math.sin((t - c) / 0.6 * math.pi)
    if 19.3 <= t < 21.0:
        y -= 70 * abs(math.sin((t - 19.3) * 6 + i))
    return x1, y, 70, sq


def frame(t):
    parts = [background(t)]
    # title
    parts.append(text(W / 2, 170, "Tosbi", 120, "#2E8B57", pop_scale(t, 0.1)))
    # Tosbi position
    walk = t < 2.2
    x = -420 + (TX + 420) * ease_out(t / 2.2) if walk else TX
    legs = t * 14 if walk else 0
    squash = 0.0
    for k in KNOCKS:
        if k <= t < k + 0.25:
            squash = math.sin((t - k) / 0.25 * math.pi) * 0.8
    if t >= 21.2:
        squash = 0.4 * math.sin((t - 21.2) * 9)
    lid = 0.0
    surprised = False
    for tp, _, _ in BALLS:
        if tp - 0.1 <= t < tp + 1.2:
            lid = ease_out((t - tp + 0.1) / 0.15)
            if t > tp + 0.9:
                lid = 1 - (t - tp - 0.9) / 0.3
            if t < tp + 0.6:
                surprised = True
    blink = 0.0
    bt = t % 3.1
    if bt < 0.14:
        blink = math.sin(bt / 0.14 * math.pi)
    look = (0, -6) if 2.8 <= t < 5.0 else (0, 0)
    if t >= 7.0 and t < 21.2:
        look = (-4, -8)
    expr = "surprised" if surprised else ("talk" if speaking(t) and int(t * 8) % 2 == 0 else "happy")
    parts.append(tosbi(x, GROUND, TS, expr=expr, lid=lid, blink=blink, legs=legs, look=look, squash=squash))
    # question bubble
    if 2.8 <= t < 5.0:
        s = pop_scale(t, 2.8)
        parts.append(f'<g transform="translate(830,880) scale({s:.3f})"><circle r="70" fill="#fff" stroke="{INK}" stroke-width="6"/>'
                     f'<circle cx="-70" cy="70" r="16" fill="#fff" stroke="{INK}" stroke-width="5"/></g>')
        parts.append(text(830, 885, "?", 100, "#F59E3B", s))
    # knock text
    for i, k in enumerate(KNOCKS):
        if k <= t < 7.0 and not NEUTRAL:
            parts.append(text(300 + i * 360, 900 - i * 50, TXT["knock"], 70, "#8B5A2B", pop_scale(t, k, 0.25)))
    # sparkles at pops
    for tp, color, _ in BALLS:
        if tp <= t < tp + 0.8:
            u = (t - tp) / 0.8
            for a in range(5):
                ang = a * 72 + 20
                d = 80 + 200 * u
                parts.append(sparkle(LID_ORIGIN[0] + d * math.cos(math.radians(ang)),
                                     LID_ORIGIN[1] - 40 - d * math.sin(math.radians(ang)) * 0.8,
                                     1.8 * (1 - u) + 0.5, 1 - u))
    # balls
    for i in range(3):
        p = ball_pos(i, t)
        if p:
            parts.append(ball(p[0], p[1], p[2], BALLS[i][1], p[3]))
    # color word
    for i, (tp, color, word) in enumerate(BALLS):
        end = BALLS[i + 1][0] if i < 2 else 13.8
        wt = WORD_T[i]
        if wt <= t < end:
            if NEUTRAL:
                sc = pop_scale(t, wt)
                parts.append(f'<g transform="translate({W/2},430) scale({sc:.3f})"><circle r="95" fill="#fff" opacity="0.9"/>'
                             f'<circle r="75" fill="{color}" stroke="{INK}" stroke-width="7"/></g>')
                parts.append(sparkle(W/2-130, 360, 0.9*sc)); parts.append(sparkle(W/2+130, 500, 0.7*sc, color="#FF9AA2"))
            else:
                parts.append(text(W / 2, 450, word, 170, color, pop_scale(t, wt)))
    # numbers during counting
    if t >= 15.8 and t < 21.2:
        for j, c in enumerate(COUNT):
            if t >= c:
                parts.append(text(BX[j], BY - 170, str(j + 1), 120, BALLS[j][1], pop_scale(t, c)))
        if t >= 19.3:
            parts.append(text(W / 2, 450, "3" if NEUTRAL else TXT["three"], 200 if NEUTRAL else 150, "#2E8B57", pop_scale(t, 19.3)))
    if t >= 21.2:
        if NEUTRAL:
            for j in range(5):
                a = (t - 21.2) * 1.5 + j * 1.2566
                parts.append(sparkle(W/2 + 260*math.cos(a), 480 + 120*math.sin(a), 1.0, 1.0, ["#FFE066","#FF9AA2","#9AD67E","#8FD3FF","#C3A6FF"][j]))
        else:
            parts.append(text(W / 2, 450, TXT["bye"], 150, "#E94B3C", pop_scale(t, 21.2)))
            parts.append(text(W / 2, 640, TXT["see"], 80, "#2E8B57", pop_scale(t, 22.4)))
    # fade in/out
    op = 0
    if t < 0.3:
        op = 1 - t / 0.3
    if t > DUR - 0.5:
        op = (t - (DUR - 0.5)) / 0.5
    if op > 0:
        parts.append(f'<rect width="{W}" height="{H}" fill="#fff" opacity="{op:.2f}"/>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">{"".join(parts)}</svg>'


def render_png(t, path):
    cairosvg.svg2png(bytestring=frame(t).encode(), write_to=path)


if __name__ == "__main__":
    if sys.argv[1] == "stills":
        for t in [1.0, 3.5, 7.4, 13.0, 18.3, 22.8]:
            render_png(t, f"still_{t}.png")
    else:
        out = sys.argv[2]
        p = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24",
                              "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast",
                              "-crf", "18", "-pix_fmt", "yuv420p", out], stdin=subprocess.PIPE)
        n = int(DUR * FPS)
        for f in range(n):
            png = cairosvg.svg2png(bytestring=frame(f / FPS).encode())
            img = Image.open(io.BytesIO(png)).convert("RGB")
            p.stdin.write(img.tobytes())
        p.stdin.close()
        sys.exit(p.wait())
