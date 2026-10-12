#!/usr/bin/env python3
# Xusniddin Tech motion Reel renderer: python3 reel.py spec.json out.mp4
import json, math, os, subprocess, sys, wave
from functools import lru_cache
import numpy as np
from PIL import Image, ImageDraw, ImageFilter, ImageFont
W, H, FPS = 1080, 1920, 30
FD = "/usr/share/fonts/opentype/inter/"
FN = {"black": "InterDisplay-Black.otf", "bold": "InterDisplay-Bold.otf", "semi": "InterDisplay-SemiBold.otf", "light": "InterDisplay-Light.otf"}
C = {"ink": (11, 11, 15), "blue": (10, 75, 240), "sky": (45, 137, 243), "ice": (228, 234, 247), "white": (255, 255, 255)}
@lru_cache(None)
def font(w, s): return ImageFont.truetype(FD + FN[w], int(s))
def fit(txt, w, s, maxw=960):
    while s > 40 and font(w, s).getlength(txt) > maxw: s -= 6
    return font(w, s)
def eo(t): t = max(0, min(1, t)); return 1 - (1 - t) ** 3
def eio(t): t = max(0, min(1, t)); return 3 * t * t - 2 * t ** 3
def bo(t, s=1.4): t = max(0, min(1, t)) - 1; return t * t * ((s + 1) * t + s) + 1
BW, BH = 1600, 2600
def make_bg():
    b = Image.new("RGB", (BW // 4, BH // 4), C["white"]); d = ImageDraw.Draw(b)
    for x, y, r, c in [(10, 60, 150, "blue"), (400, 40, 110, "sky"), (390, 640, 170, "blue"), (20, 600, 120, "sky"), (210, 330, 170, "white")]:
        d.ellipse([x - r, y - r, x + r, y + r], fill=C[c])
    return b.filter(ImageFilter.GaussianBlur(70)).resize((BW, BH), Image.BICUBIC)
BG = make_bg()
def bg(t):
    ox = int(160 + 120 * math.sin(t * .35)); oy = int(220 + 160 * math.cos(t * .27))
    return BG.crop((ox, oy, ox + W, oy + H)).convert("RGBA")
@lru_cache(512)
def timg(txt, f, col):
    bb = f.getbbox(txt); im = Image.new("RGBA", (bb[2] - bb[0] + 40, f.size + 60), (0, 0, 0, 0))
    ImageDraw.Draw(im).text((20 - bb[0], 20), txt, font=f, fill=col); return im
def paste(fr, im, cx, cy, a=1., sc=1., bl=0):
    if a <= .01: return
    if sc != 1: im = im.resize((max(1, int(im.width * sc)), max(1, int(im.height * sc))), Image.BICUBIC)
    if bl > .5: im = im.filter(ImageFilter.GaussianBlur(bl))
    if a < 1: im = im.copy(); im.putalpha(im.getchannel("A").point(lambda v: int(v * a)))
    fr.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))
def outk(t, out): return 0 if out is None or t <= out else eio((t - out) / .35)
def word(fr, t, st, txt, f, col, cy, rise=60, out=None):
    p = (t - st) / .45
    if p <= 0: return
    e = eo(p); q = outk(t, out)
    paste(fr, timg(txt, f, col), W / 2, cy + (1 - e) * rise - q * 40, e * (1 - q), 1, (1 - e) * 10 + q * 12)
def card(fr, t, st, lab, cx, cy, out=None, w=420, h=210):
    p = (t - st) / .55
    if p <= 0: return
    e = bo(p); a = eo(p) * (1 - outk(t, out))
    im = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([24, 30, w + 24, h + 30], 36, fill=(10, 30, 120, 40)); im = im.filter(ImageFilter.GaussianBlur(12)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([20, 20, w + 20, h + 20], 36, fill=(255, 255, 255, 215), outline=(255, 255, 255, 255), width=3)
    f = fit(lab, "black", 64, w - 50); d.text((20 + (w - f.getlength(lab)) / 2, 20 + h / 2 - f.size * .62), lab, font=f, fill=C["blue"])
    paste(fr, im, cx, cy + (1 - e) * 120, a, .85 + .15 * e)
def pill(fr, t, st, lab, cy):
    p = (t - st) / .5
    if p <= 0: return
    f = font("bold", 48); tw = int(f.getlength(lab)); w, h = tw + 110, 110
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], h // 2, fill=C["blue"]); d.text(((w - tw) / 2, 26), lab, font=f, fill=C["white"])
    paste(fr, im, W / 2, cy, eo(p), .6 + .4 * bo(p))
def bignum(fr, t, st, txt, cy, out=None):
    p = (t - st) / .7
    if p <= 0: return
    e = eo(p); a = e * (1 - outk(t, out)); f = fit(txt, "black", 760, 900)
    paste(fr, timg(txt, f, (10, 30, 120, 70)).filter(ImageFilter.GaussianBlur(30)), W / 2 + 20, cy + 50, a * .8, 1.25 - .25 * e)
    paste(fr, timg(txt, f, C["blue"]), W / 2, cy, a, 1.25 - .25 * e, (1 - e) * 14)
def scene(fr, t, s, st, en, last):
    out = None if last else en - .35; k = s["type"]
    if k == "words":  # lines: [[text, weight, color], ...]
        ls = s["lines"]; sizes = [fit(x[0], x[1], {"black": 190, "light": 120}.get(x[1], 110)).size for x in ls]
        y = 960 - sum(sz * 1.05 for sz in sizes) / 2
        for i, (x, sz) in enumerate(zip(ls, sizes)):
            word(fr, t, st + .15 + i * .4, x[0], fit(x[0], x[1], sz), C[x[2]], y + sz * .5, out=out); y += sz * 1.05
    elif k == "cards":
        word(fr, t, st, s["kicker"], fit(s["kicker"], "light", 100), C["ink"], 470, out=out)
        word(fr, t, st + .3, s["title"], fit(s["title"], "black", 150), C["ink"], 610, out=out)
        for i, lab in enumerate(s["cards"][:4]):
            card(fr, t, st + .8 + i * .35, lab, W / 2 + (-235 if i % 2 == 0 else 235), 930 + (i // 2) * 260, out)
    elif k == "number":
        bignum(fr, t, st, s["num"], 780, out)
        word(fr, t, st + .5, s["head"], fit(s["head"], "black", 170), C["ink"], 1300, out=out)
        word(fr, t, st + .9, s["l1"], fit(s["l1"], "semi", 64), C["ink"], 1450, 30, out)
        word(fr, t, st + 1.2, s["l2"], fit(s["l2"], "semi", 64), C["blue"], 1535, 30, out)
    elif k == "subscribe":
        subscribe(fr, t, st, s)
    elif k == "cta":
        word(fr, t, st, s["l1"], fit(s["l1"], "black", 200), C["ink"], 820, out=out)
        word(fr, t, st + .35, s["l2"], fit(s["l2"], "black", 200), C["blue"], 1010, out=out)
        pill(fr, t, st + .9, s.get("pill", "@xusniddintech"), 1260)
AVATAR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "avatar.jpg")
@lru_cache(4)
def avatar_img(d):
    sz = d * 2  # supersample
    try:
        src = Image.open(AVATAR).convert("RGB"); s = min(src.size)
        src = src.crop(((src.width - s) // 2, (src.height - s) // 2, (src.width + s) // 2, (src.height + s) // 2)).resize((sz, sz), Image.LANCZOS)
    except Exception:
        src = Image.new("RGB", (sz, sz), C["blue"]); dd = ImageDraw.Draw(src); f = font("black", int(sz * .36))
        bb = f.getbbox("XT"); dd.text(((sz - bb[2] - bb[0]) / 2, (sz - bb[3] - bb[1]) / 2), "XT", font=f, fill=C["white"])
    m = Image.new("L", (sz, sz), 0); ImageDraw.Draw(m).ellipse([0, 0, sz - 1, sz - 1], fill=255)
    ring = Image.new("RGBA", (sz + 28, sz + 28), (0, 0, 0, 0)); rd = ImageDraw.Draw(ring)
    rd.ellipse([0, 0, sz + 27, sz + 27], fill=C["white"]); ring.paste(src, (14, 14), m)
    out = Image.new("RGBA", (sz + 120, sz + 120), (0, 0, 0, 0)); sh = Image.new("RGBA", out.size, (0, 0, 0, 0))
    ImageDraw.Draw(sh).ellipse([46, 66, sz + 74, sz + 94], fill=(10, 30, 120, 70)); out.alpha_composite(sh.filter(ImageFilter.GaussianBlur(22)))
    out.alpha_composite(ring, (46, 46)); return out.resize((out.width // 2, out.height // 2), Image.LANCZOS)
def btn(label, fill, col, scale=1.):
    f = font("bold", 46); tw = int(f.getlength(label)); w, h = max(tw + 120, 300), 96
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], h // 2, fill=fill); d.text(((w - tw) / 2, 20), label, font=f, fill=col)
    return im
def pillimg(label, fnt, fill, col, w, h, shadow=True):
    im = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    if shadow:
        d.rounded_rectangle([22, 26, w + 18, h + 26], h // 2, fill=(10, 30, 120, 45)); im = im.filter(ImageFilter.GaussianBlur(9)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([20, 20, w + 19, h + 19], h // 2, fill=fill)
    tw = fnt.getlength(label); bb = fnt.getbbox(label)
    d.text((20 + (w - tw) / 2, 20 + (h - (bb[3] - bb[1])) / 2 - bb[1]), label, font=fnt, fill=col); return im
def subscribe(fr, t, st, s):
    # Stacked like the reference ending: handle pill overlaps the avatar's bottom edge,
    # the narrower button tucks under the pill; a tap turns "Obuna" into the thank-you label.
    title = s.get("title", "SAHIFAMIZGA"); word(fr, t, st, title, fit(title, "black", 170), C["ink"], 560)
    tap = st + s.get("tap_at", 2.0)
    sub = s.get("sub", "obuna bo'ling"); word(fr, t, tap + .15, sub, fit(sub, "light", 92), C["blue"], 668, rise=24)
    AD = 330; AY = 905; abot = AY + (AD + 14) / 2
    PH = 96; PY = abot - 30 + PH / 2
    BH = 74; BY = PY + PH / 2 - 20 + BH / 2
    p = (t - st - .45) / .6
    if p > 0:
        e = bo(p); paste(fr, avatar_img(AD), W / 2, AY + (1 - e) * 80, eo(p), .7 + .3 * e)
    p = (t - st - .7) / .5
    if p > 0:
        e = bo(p); h = s.get("handle", "xusniddintech"); f = font("semi", 46)
        pw = max(int(f.getlength(h)) + 150, 480)
        paste(fr, pillimg(h, f, C["white"], C["ink"], pw, PH), W / 2, PY + (1 - e) * 50, eo(p), .8 + .2 * e)
    p = (t - st - .95) / .45
    if p > 0:
        e = bo(p); fb = font("bold", 40)
        def b(label, fill, col): return pillimg(label, fb, fill, col, max(int(fb.getlength(label)) + 110, 250), BH, shadow=False)
        if t < tap:
            paste(fr, b(s.get("button", "Obuna"), C["blue"], C["white"]), W / 2, BY, eo(p), .7 + .3 * e)
        else:
            q = (t - tap) / .35; sq = 1 - .1 * math.sin(min(1, q) * math.pi)
            if q < .5: paste(fr, b(s.get("button", "Obuna"), C["sky"], C["white"]), W / 2, BY, 1, sq)
            else: paste(fr, b(s.get("thanks", "Yashang!"), C["ice"], C["ink"]), W / 2, BY, 1, .92 + .08 * bo((q - .5) * 2))
    k = (t - tap + .25) / .7  # small tap ring landing on the button
    if 0 < k < 1:
        r = int(40 - 14 * eo(k)); a = int(170 * (1 - max(0, k - .5) * 2))
        ring = Image.new("RGBA", (2 * r + 8, 2 * r + 8), (0, 0, 0, 0)); ImageDraw.Draw(ring).ellipse([4, 4, 2 * r + 4, 2 * r + 4], fill=(255, 255, 255, a // 2), outline=(90, 95, 110, a), width=3)
        fr.alpha_composite(ring, (int(W / 2 + 45 - r - 4), int(BY + 12 - r - 4)))
def music(path, dur, mood):
    sr = 44100; n = int(sr * dur); t = np.arange(n) / sr; hz = lambda m: 440 * 2 ** ((m - 69) / 12)
    M = {"tech": (104, [[57, 60, 64, 67], [53, 57, 60, 64], [48, 52, 55, 59], [55, 59, 62, 66]], .35),
         "calm": (84, [[60, 64, 67, 71], [57, 60, 64, 67], [53, 57, 60, 64], [55, 59, 62, 65]], .15),
         "energetic": (120, [[62, 65, 69, 72], [58, 62, 65, 69], [60, 64, 67, 70], [57, 60, 64, 67]], .45),
         "playful": (112, [[60, 64, 67, 72], [65, 69, 72, 76], [67, 71, 74, 79], [60, 64, 67, 72]], .3)}
    bpm, chords, kick = M.get(mood, M["tech"]); beat = 60 / bpm; bar = 4 * beat; out = np.zeros(n); rng = np.random.default_rng(1)
    for b in range(int(dur / bar) + 1):
        ch = chords[b % 4]; bs = b * bar; s, e = int(bs * sr), min(n, int((bs + bar) * sr))
        if s >= n: break
        tt = t[s:e] - bs; env = np.minimum(1, tt / .25) * np.minimum(1, (bar - tt) / .3)
        for m in ch: f = hz(m - 12); out[s:e] += env * (np.sin(2 * np.pi * f * tt) + np.sin(2 * np.pi * f * 1.004 * tt)) * .05
        for k in range(16):
            ps = int((bs + k * beat / 4) * sr)
            if ps >= n: break
            m = ch[[0, 1, 2, 3, 2, 1, 2, 3][k % 8]] + 12; pe = min(n, ps + int(.22 * sr)); tp = np.arange(pe - ps) / sr
            out[ps:pe] += np.exp(-tp * 14) * np.sign(np.sin(2 * np.pi * hz(m) * tp)) * .025
        for k in range(4):
            ks = int((bs + k * beat) * sr)
            if ks < n and kick:
                ke = min(n, ks + int(.25 * sr)); tp = np.arange(ke - ks) / sr
                out[ks:ke] += np.sin(2 * np.pi * (50 + 90 * np.exp(-tp * 30)) * tp) * np.exp(-tp * 12) * kick
            hs = int((bs + k * beat + beat / 2) * sr)
            if hs < n and kick:
                he = min(n, hs + int(.05 * sr)); out[hs:he] += rng.standard_normal(he - hs) * np.exp(-np.arange(he - hs) / sr * 80) * .04
    out = np.tanh(out * 1.5); out = out / np.max(np.abs(out)) * .22 * np.minimum(1, np.minimum(t, (dur - t) / 1.2))
    with wave.open(path, "wb") as w:
        w.setnchannels(2); w.setsampwidth(2); w.setframerate(sr); w.writeframes((np.stack([out, out], 1) * 32767).astype(np.int16).tobytes())
def main(spec_path, outp):
    spec = json.load(open(spec_path)); sc = spec["scenes"]; starts = [0.]
    for s in sc: starts.append(starts[-1] + s["dur"])
    dur = starts[-1]; wav = outp + ".wav"; music(wav, dur, spec.get("mood", "tech"))
    p = subprocess.Popen(["ffmpeg", "-v", "error", "-y", "-f", "rawvideo", "-pix_fmt", "rgb24", "-s", f"{W}x{H}", "-r", str(FPS), "-i", "-", "-i", wav,
                          "-c:v", "libx264", "-preset", "medium", "-crf", "20", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-shortest", "-movflags", "+faststart", outp], stdin=subprocess.PIPE)
    wm = timg("Xusniddin Tech", font("bold", 42), C["ink"])
    for i in range(int(dur * FPS)):
        t = i / FPS; fr = bg(t); paste(fr, wm, W / 2, 120, min(1, t / .6))
        for j, s in enumerate(sc):
            if starts[j] - .1 < t < starts[j + 1] + .4: scene(fr, t, s, starts[j], starts[j + 1], j == len(sc) - 1)
        k = min(1, t / .25, (dur - t) / .4)
        if k < 1: fr = Image.blend(Image.new("RGBA", (W, H), C["ice"] + (255,)), fr, max(0, k))
        p.stdin.write(fr.convert("RGB").tobytes())
    p.stdin.close(); p.wait()
if __name__ == "__main__": main(sys.argv[1], sys.argv[2])
