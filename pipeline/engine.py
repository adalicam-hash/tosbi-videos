"""Tosbi episode engine: builds an EN video + full TR audio track from episodes.py content.

usage: python3 engine.py OUT_PREFIX LAYOUT(v|h) SEG1[,SEG2...] [--long]
  v = 1080x1920 Short, h = 1920x1080 long video. --long adds "say it with me" repetitions.
Outputs: OUT_PREFIX_en.mp4 (video + EN audio), OUT_PREFIX_tr_track.mp3 (full TR mix for YouTube),
         OUT_PREFIX_tr_preview.mp4, OUT_PREFIX_timeline.json
Models: /home/claude/models/kokoro-v1.0.int8.onnx + voices-v1.0.bin (see FORMAT.md)."""
import sys, os, io, math, json, hashlib, subprocess, tempfile
import numpy as np, soundfile as sf
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from tosbi import tosbi, sparkle, INK
from items import DRAW
import episodes as E

SR = 44100
FPS = 30
MODELS = os.environ.get("TOSBI_MODELS", "/home/claude/models")
CACHE = os.environ.get("TOSBI_CACHE", "/home/claude/tosbi_cache")
os.makedirs(CACHE, exist_ok=True)

LAYOUTS = {
    "v": dict(W=1080, H=1920, GROUND=1560, TX=420, TS=1.85, SX=[270, 540, 810], SY=820, R=70,
              WORD=(540, 450, 170), TITLE=(540, 170, 120), BUBBLE=(830, 880), SUN=(900, 230)),
    "h": dict(W=1920, H=1080, GROUND=960, TX=470, TS=1.25, SX=[1130, 1420, 1710], SY=560, R=78,
              WORD=(1420, 250, 150), TITLE=(240, 95, 90), BUBBLE=(860, 610), SUN=(1780, 120)),
}

# ---------------------------------------------------------------- voice
_k = _tr = None


def _engines():
    global _k, _tr
    if _k is None:
        import espeakng_loader
        from phonemizer.backend.espeak.wrapper import EspeakWrapper
        EspeakWrapper.set_library(espeakng_loader.get_library_path())
        EspeakWrapper.set_data_path(espeakng_loader.get_data_path())
        from phonemizer.backend import EspeakBackend
        from kokoro_onnx import Kokoro
        _tr = EspeakBackend("tr", preserve_punctuation=True, with_stress=True)
        _k = Kokoro(f"{MODELS}/kokoro-v1.0.int8.onnx", f"{MODELS}/voices-v1.0.bin")
    return _k, _tr


def _part(lang, text):
    key = hashlib.md5(f"v2|{lang}|{text}".encode()).hexdigest()
    fn = f"{CACHE}/{key}.wav"
    if not os.path.exists(fn):
        k, tr = _engines()
        if lang == "tr":
            s, sr = k.create(tr.phonemize([text])[0].strip().replace("ɫ", "l"), voice="af_heart", speed=0.9, is_phonemes=True)
        else:
            s, sr = k.create(text, voice="af_heart", speed=0.92, lang="en-us")
        s = np.asarray(s)
        a = np.where(np.abs(s) > 0.01)[0]
        if len(a):
            s = s[max(0, a[0] - 240):a[-1] + 480]
        tmp = fn + ".raw.wav"
        sf.write(tmp, s, sr)
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", tmp, "-af",
                        f"asetrate={sr}*1.16,aresample={SR},atempo=0.95", fn], check=True)
        os.remove(tmp)
    y, _ = sf.read(fn)
    return y if y.ndim == 1 else y.mean(1)


def voice(parts):
    """Return (audio, onsets_sec) for a list of (lang, text) parts joined by short gaps."""
    out, on, cur = [], [], 0
    gap = np.zeros(int(0.16 * SR))
    for i, (lang, t) in enumerate(parts):
        y = _part(lang, t)
        on.append(cur / SR)
        out.append(y)
        cur += len(y)
        if i < len(parts) - 1:
            out.append(gap)
            cur += len(gap)
    return np.concatenate(out), on


def _last_en(parts):
    return max(i for i, (l, _) in enumerate(parts) if l == "en")


# ---------------------------------------------------------------- timeline
class TL:
    def __init__(self):
        self.en, self.tr, self.talk = [], [], []
        self.knocks, self.bubbles, self.pops, self.words, self.bounces = [], [], [], [], []
        self.numbers, self.celebrate, self.clears, self.chapters = [], [], [], []
        self.walk = None
        self.bye = None
        self.dur = 0

    def place(self, en_parts, tr_parts, t, align=True):
        ea, eo = voice(en_parts)
        ta, to = voice(tr_parts)
        if align:
            oe, ot = eo[_last_en(en_parts)], to[_last_en(tr_parts)]
            m = max(oe, ot)
            se, st, wt = t + m - oe, t + m - ot, t + m
        else:
            se = st = t
            wt = None
        self.en.append((se, ea))
        self.tr.append((st, ta))
        self.talk += [(se, se + len(ea) / SR - 0.08), (st, st + len(ta) / SR - 0.08)]
        return max(se + len(ea) / SR, st + len(ta) / SR), wt


def build(seg_names, long=False):
    tl = TL()
    t = 0.5
    tl.walk = (0.0, 2.2)
    end, _ = tl.place(E.INTRO["en"], E.INTRO["tr"], t, align=False)
    t = max(end + 0.3, 2.4)
    for si, name in enumerate(seg_names):
        seg = E.SEGMENTS[name]
        tl.chapters.append((max(0, t - 0.3), name))
        ask = E.ASK if si == 0 else E.ASK_AGAIN
        b0 = t
        end, _ = tl.place(ask["en"], ask["tr"], t, align=False)
        t = end + 0.2
        tl.bubbles.append((b0, t))
        end, wt = tl.place(E.KNOCK["en"], E.KNOCK["tr"], t)
        tl.knocks += [wt + 0.02, wt + 0.38]
        t = end + 0.4
        slots = []
        for i, it in enumerate(seg["items"]):
            tl.pops.append(dict(t=t, slot=i, kind=it["kind"], clear=None))
            slots.append(len(tl.pops) - 1)
            t += 0.7
            end, wt = tl.place(it["en"], it["tr"], t)
            tl.words.append(dict(t=wt, text=it["word"], color=seg["word_color"][i]))
            t = end + 0.4
            if long:
                key = [("en", it["word"].capitalize() + "!")]
                end, wt = tl.place(E.REPEAT["en"] + key, E.REPEAT["tr"] + key, t)
                tl.words.append(dict(t=wt, text=it["word"], color=seg["word_color"][i]))
                t = end + 1.3  # pause for the child to repeat
        end, _ = tl.place(E.COUNT["en"], E.COUNT["tr"], t, align=False)
        t = end + 0.2
        for n in range(3):
            end, wt = tl.place(E.NUMS[n], E.NUMS[n], t)
            tl.bounces.append((wt, slots[n]))
            tl.numbers.append((wt, slots[n], n + 1, seg["word_color"][n]))
            t = end + 0.35
        if long:
            end, _ = tl.place(E.QUIZ_INTRO["en"], E.QUIZ_INTRO["tr"], t, align=False)
            t = end + 0.3
            for i in [1, 2, 0]:
                it = seg["items"][i]
                qe, qt = E.quiz_q(it)
                b0 = t
                end, _ = tl.place(qe, qt, t, align=False)
                t = end + 1.6  # thinking time
                tl.bubbles.append((b0, t))
                ae, at = E.quiz_a(it)
                end, wt = tl.place(ae, at, t)
                tl.bounces.append((wt, slots[i]))
                tl.words.append(dict(t=wt, text=it["word"], color=seg["word_color"][i]))
                t = end + 0.6
        s = seg["summary"]
        end, wt = tl.place(s["en"], s["tr"], t)
        tl.words.append(dict(t=wt, text=s["word"], color="#2E8B57"))
        tl.celebrate.append((wt, end + 0.8))
        t = end + 0.9
        if si < len(seg_names) - 1:
            tl.clears.append(t)
            for p in slots:
                tl.pops[p]["clear"] = t
            tl.words.append(dict(t=t, text="", color="#000"))
            t += 1.1
    end, wt = tl.place(E.OUTRO["en"], E.OUTRO["tr"], t)
    tl.bye = wt
    tl.words.append(dict(t=wt, text="Bye-bye!", color="#E94B3C"))
    tl.dur = end + 1.6
    return tl


# ---------------------------------------------------------------- drawing
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


def text(x, y, s, size, fill, scale=1.0, op=1.0):
    c = f'text-anchor="middle" font-family="Poppins" font-weight="bold" font-size="{size}" dominant-baseline="middle"'
    return (f'<g transform="translate({x},{y}) scale({scale:.3f})" opacity="{op:.2f}">'
            f'<text {c} fill="#fff" stroke="#fff" stroke-width="{size*0.18:.0f}" stroke-linejoin="round">{s}</text>'
            f'<text {c} fill="{fill}" stroke="{INK}" stroke-width="{max(2,size*0.03):.0f}" stroke-linejoin="round">{s}</text></g>')


def background(L, t):
    W, H, G = L["W"], L["H"], L["GROUND"]
    cl = ""
    for i, (cx, cy, s) in enumerate([(0.18, 0.27, 1.0), (0.76, 0.2, 0.8), (0.55, 0.33, 0.6)]):
        x = (cx * W + t * (12 + 6 * i)) % (W + 300) - 150
        cl += (f'<g transform="translate({x:.1f},{cy*G:.0f}) scale({s})" fill="#fff"><circle cx="-60" cy="10" r="50"/>'
               '<circle cx="0" cy="-15" r="65"/><circle cx="65" cy="10" r="48"/><rect x="-110" y="10" width="225" height="50" rx="25"/></g>')
    sx, sy = L["SUN"]
    fl = "".join(f'<g transform="translate({W*fx:.0f},{G+70+(i%2)*90})"><circle r="16" fill="{c}"/><circle r="7" fill="#FFE27A"/></g>'
                 for i, (fx, c) in enumerate([(0.1, "#FF9AA2"), (0.3, "#fff"), (0.52, "#C3A6FF"), (0.73, "#FF9AA2"), (0.9, "#fff")]))
    return ('<defs><linearGradient id="sky" x1="0" y1="0" x2="0" y2="1"><stop offset="0" stop-color="#8FD3FF"/>'
            '<stop offset="1" stop-color="#E9F7FF"/></linearGradient></defs>'
            f'<rect width="{W}" height="{H}" fill="url(#sky)"/>'
            f'<circle cx="{sx}" cy="{sy}" r="90" fill="#FFE27A"/><circle cx="{sx}" cy="{sy}" r="120" fill="#FFE27A" opacity="0.3"/>' + cl +
            f'<path d="M 0 {G-80} Q {W*0.28:.0f} {G-170} {W*0.57:.0f} {G-90} T {W} {G-110} L {W} {H} L 0 {H} Z" fill="#B7E59A"/>'
            f'<rect x="0" y="{G-20}" width="{W}" height="{H-G+20}" fill="#9AD67E"/>' + fl)


def frame_svg(tl, L, t):
    W, H = L["W"], L["H"]
    TX, TS, G = L["TX"], L["TS"], L["GROUND"]
    lid_o = (TX - 8 * TS, G - 175 * TS)
    p = [background(L, t)]
    tx, ty, ts = L["TITLE"]
    p.append(text(tx, ty, "Tosbi", ts, "#2E8B57", pop_scale(t, 0.1)))
    w0, w1 = tl.walk
    walking = t < w1
    x = -0.4 * W + (TX + 0.4 * W) * ease_out(t / w1) if walking else TX
    squash = 0.0
    for k in tl.knocks:
        if k <= t < k + 0.25:
            squash = math.sin((t - k) / 0.25 * math.pi) * 0.8
    for a, b in tl.celebrate:
        if a <= t < b:
            squash = 0.35 * math.sin((t - a) * 9)
    if tl.bye and t >= tl.bye:
        squash = 0.4 * math.sin((t - tl.bye) * 9)
    lid, surprised = 0.0, False
    for pp in tl.pops:
        tp = pp["t"]
        if tp - 0.1 <= t < tp + 1.2:
            lid = ease_out((t - tp + 0.1) / 0.15)
            if t > tp + 0.9:
                lid = 1 - (t - tp - 0.9) / 0.3
            surprised = surprised or t < tp + 0.6
    bt = t % 3.1
    blink = math.sin(bt / 0.14 * math.pi) if bt < 0.14 else 0.0
    talking = any(a <= t <= b for a, b in tl.talk)
    expr = "surprised" if surprised else ("talk" if talking and int(t * 8) % 2 == 0 else "happy")
    look = (0, -6) if any(a <= t < b for a, b in tl.bubbles) else ((-4, -8) if tl.pops and t >= tl.pops[0]["t"] else (0, 0))
    p.append(tosbi(x, G, TS, expr=expr, lid=lid, blink=blink, legs=t * 14 if walking else 0, look=look, squash=squash))
    bx, by = L["BUBBLE"]
    for a, b in tl.bubbles:
        if a <= t < b:
            s = pop_scale(t, a)
            p.append(f'<g transform="translate({bx},{by}) scale({s:.3f})"><circle r="70" fill="#fff" stroke="{INK}" stroke-width="6"/>'
                     f'<circle cx="-70" cy="70" r="16" fill="#fff" stroke="{INK}" stroke-width="5"/></g>')
            p.append(text(bx, by + 2, "?", 100, "#F59E3B", s))
    for i, k in enumerate(tl.knocks):
        if k <= t < k + 0.9:
            p.append(text(bx - 420 + (i % 2) * 300, by - 60 - (i % 2) * 40, "knock!", 64, "#8B5A2B", pop_scale(t, k, 0.25)))
    # items
    for pp in tl.pops:
        tp = pp["t"]
        if t < tp:
            continue
        if pp["clear"] and t > pp["clear"] + 0.8:
            continue
        sx, sy, R = L["SX"][pp["slot"]], L["SY"], L["R"]
        u = (t - tp) / 0.7
        sq = 0.0
        if u < 1:
            x0, y0 = lid_o
            ix = x0 + (sx - x0) * u
            iy = y0 + (sy - y0) * u - 0.22 * H * math.sin(math.pi * u)
            r = R * (0.4 + 0.6 * ease_out(u * 2))
            for a in range(5):
                ang = math.radians(a * 72 + 20)
                d = 80 + 200 * u
                p.append(sparkle(x0 + d * math.cos(ang), y0 - 40 - d * math.sin(ang) * 0.8, 1.6 * (1 - u) + 0.4, 1 - u))
        else:
            ix, r = sx, R
            iy = sy + 12 * math.sin((t - tp) * 3 + pp["slot"])
            land = t - tp - 0.7
            if land < 0.25:
                sq = math.sin(land / 0.25 * math.pi) * 0.6
            for bt_, slot in tl.bounces:
                if tl.pops.index(pp) == slot and bt_ <= t < bt_ + 0.6:
                    iy -= 110 * math.sin((t - bt_) / 0.6 * math.pi)
            for a, b in tl.celebrate:
                if a <= t < b and (pp["clear"] is None or a < pp["clear"]):
                    iy -= 60 * abs(math.sin((t - a) * 6 + pp["slot"]))
            if pp["clear"] and t > pp["clear"]:
                v = (t - pp["clear"]) / 0.8
                iy -= v * v * H
        p.append(DRAW[pp["kind"]](ix, iy, r, sq))
    for nt, slot, n, col in tl.numbers:
        pp = tl.pops[slot]
        if t >= nt and not (pp["clear"] and t > pp["clear"]):
            p.append(text(L["SX"][pp["slot"]], L["SY"] - L["R"] - 100, str(n), 110, col, pop_scale(t, nt)))
    wx, wy, wsz = L["WORD"]
    cur = None
    for w in tl.words:
        if w["t"] <= t:
            cur = w
    if cur and cur["text"]:
        sz = wsz if len(cur["text"]) <= 6 else int(wsz * 6.5 / len(cur["text"]) + wsz * 0.25)
        p.append(text(wx, wy, cur["text"], sz, cur["color"], pop_scale(t, cur["t"])))
    if tl.bye and t >= tl.bye + 0.4:
        for j in range(5):
            a = (t - tl.bye) * 1.5 + j * 1.2566
            p.append(sparkle(wx + 0.25 * W * math.cos(a) * (0.7 if W < H else 1), wy + 150 + 110 * math.sin(a), 1.0, 1.0,
                             ["#FFE066", "#FF9AA2", "#9AD67E", "#8FD3FF", "#C3A6FF"][j]))
    op = 0
    if t < 0.3:
        op = 1 - t / 0.3
    if t > tl.dur - 0.5:
        op = (t - (tl.dur - 0.5)) / 0.5
    if op > 0:
        p.append(f'<rect width="{W}" height="{H}" fill="#fff" opacity="{min(1,op):.2f}"/>')
    return f'<svg xmlns="http://www.w3.org/2000/svg" width="{W}" height="{H}">{"".join(p)}</svg>'


# ---------------------------------------------------------------- audio
def music_and_sfx(tl):
    n = int(tl.dur * SR) + SR
    mix = np.zeros(n)

    def add(sig, t, g=1.0):
        i = int(t * SR)
        if i >= n:
            return
        mix[i:i + len(sig)] += sig[:n - i] * g

    def pluck(f, d=0.6):
        tt = np.arange(int(d * SR)) / SR
        return (np.sin(2 * np.pi * f * tt) + 0.3 * np.sin(4 * np.pi * f * tt) + 0.1 * np.sin(6 * np.pi * f * tt)) * np.exp(-tt * 5)
    chords = [[261.6, 329.6, 392.0], [196.0, 246.9, 293.7], [220.0, 261.6, 329.6], [174.6, 220.0, 261.6]]
    mel = [523.3, 659.3, 784.0, 659.3, 587.3, 493.9, 587.3, 784.0, 523.3, 659.3, 523.3, 440.0, 523.3, 440.0, 349.2, 440.0]
    beat, t, b = 0.6, 0.0, 0
    while t < tl.dur - 0.6:
        ch = chords[(b // 4) % 4]
        add(pluck(ch[0] / 2, 1.2), t, 0.05)
        for j, f in enumerate(ch):
            add(pluck(f, 0.5), t + beat * 0.5 + 0.02 * j, 0.025)
        add(pluck(mel[b % 16], 0.4), t, 0.03)
        t += beat
        b += 1

    def sweep(d, f0, f1, decay):
        tt = np.arange(int(d * SR)) / SR
        f = f0 + (f1 - f0) * tt / d
        return np.sin(2 * np.pi * np.cumsum(f) / SR) * np.exp(-tt * decay)
    tt = np.arange(int(0.12 * SR)) / SR
    knock = np.sin(2 * np.pi * 140 * tt) * np.exp(-tt * 40) + 0.3 * np.random.RandomState(0).randn(len(tt)) * np.exp(-tt * 80)
    for k in tl.knocks:
        add(knock, k, 0.5)
    for pp in tl.pops:
        add(sweep(0.25, 300, 1800, 12), pp["t"], 0.3)
        add(sweep(0.4, 220, 300, 7), pp["t"] + 0.7, 0.15)
    for bt_, _ in tl.bounces:
        add(sweep(0.4, 220, 320, 7), bt_, 0.2)
    for c in tl.clears:
        add(sweep(0.5, 400, 1600, 5), c, 0.2)
    return mix


def render_mix(tl, clips, path):
    mix = music_and_sfx(tl)
    for st, y in clips:
        i = int(st * SR)
        mix[i:i + len(y)] += y[:len(mix) - i]
    mix = mix[:int(tl.dur * SR)]
    f = int(0.5 * SR)
    mix[-f:] *= np.linspace(1, 0, f)
    mix = mix / np.max(np.abs(mix)) * 0.89
    raw = path + ".raw.wav"
    sf.write(raw, mix, SR)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", raw, "-af", "loudnorm=I=-14:TP=-1.5:LRA=11", "-ar", str(SR), path], check=True)
    os.remove(raw)


# ---------------------------------------------------------------- video
def render_chunk(args):
    tl, L, f0, f1, out = args
    import cairosvg
    from PIL import Image
    pr = subprocess.Popen(["ffmpeg", "-y", "-loglevel", "error", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{L['W']}x{L['H']}",
                           "-r", str(FPS), "-i", "-", "-c:v", "libx264", "-preset", "veryfast", "-crf", "20", "-pix_fmt", "yuv420p",
                           out + ".tmp.mp4"], stdin=subprocess.PIPE)
    for f in range(f0, f1):
        png = cairosvg.svg2png(bytestring=frame_svg(tl, L, f / FPS).encode())
        pr.stdin.write(Image.open(io.BytesIO(png)).convert("RGB").tobytes())
    pr.stdin.close()
    assert pr.wait() == 0
    os.rename(out + ".tmp.mp4", out)
    return out


def render_video(tl, L, path, workers=2):
    from multiprocessing import Pool
    n = int(tl.dur * FPS)
    step = math.ceil(n / workers)
    tmpd = tempfile.mkdtemp()
    jobs = [(tl, L, i, min(n, i + step), f"{tmpd}/c{j:02d}.mp4") for j, i in enumerate(range(0, n, step))]
    with Pool(workers) as pool:
        outs = pool.map(render_chunk, jobs)
    lst = f"{tmpd}/list.txt"
    open(lst, "w").write("".join(f"file '{o}'\n" for o in outs))
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-f", "concat", "-safe", "0", "-i", lst, "-c", "copy", path], check=True)


def main():
    prefix, lay, segs = sys.argv[1], sys.argv[2], sys.argv[3].split(",")
    long = "--long" in sys.argv
    L = LAYOUTS[lay]
    tl = build(segs, long)
    print(f"duration {tl.dur:.1f}s, chapters {[(round(a,1), n) for a, n in tl.chapters]}", flush=True)
    render_mix(tl, tl.en, prefix + "_en.wav")
    render_mix(tl, tl.tr, prefix + "_tr.wav")
    if "--stills" in sys.argv:
        import cairosvg
        for s in [float(x) for x in sys.argv[sys.argv.index("--stills") + 1].split(",")]:
            cairosvg.svg2png(bytestring=frame_svg(tl, L, s).encode(), write_to=f"{prefix}_still_{s}.png")
        return
    render_video(tl, L, prefix + "_silent.mp4")
    for lang in ["en", "tr"]:
        out = prefix + ("_en.mp4" if lang == "en" else "_tr_preview.mp4")
        subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", prefix + "_silent.mp4", "-i", f"{prefix}_{lang}.wav", "-map", "0:v",
                        "-map", "1:a", "-c:v", "copy", "-c:a", "aac", "-b:a", "192k", "-shortest", out + ".tmp.mp4"], check=True)
        os.rename(out + ".tmp.mp4", out)
    subprocess.run(["ffmpeg", "-y", "-loglevel", "error", "-i", prefix + "_tr.wav", "-b:a", "192k", prefix + "_tr_track.mp3"], check=True)
    json.dump(dict(duration=tl.dur, chapters=tl.chapters), open(prefix + "_timeline.json", "w"))
    print("done", flush=True)


if __name__ == "__main__":
    main()
