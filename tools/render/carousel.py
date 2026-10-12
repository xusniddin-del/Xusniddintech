#!/usr/bin/env python3
# Xusniddin Tech carousel renderer (1080x1350, same look as reel.py): python3 carousel.py spec.json outdir
import json, os, sys
sys.argv_backup = sys.argv
from PIL import Image, ImageDraw, ImageFilter
import importlib.util
spec_r = importlib.util.spec_from_file_location("reel", os.path.join(os.path.dirname(os.path.abspath(__file__)), "reel.py"))
R = importlib.util.module_from_spec(spec_r); spec_r.loader.exec_module(R)
W, H = 1080, 1350
font, fit, C, timg = R.font, R.fit, R.C, R.timg

def bg(seed):
    ox = 160 + (seed * 97) % 240; oy = 300 + (seed * 131) % 500
    return R.BG.crop((ox, oy, ox + W, oy + H)).convert("RGBA")

def center(fr, txt, f, col, cy):
    im = timg(txt, f, col); fr.alpha_composite(im, (int(W / 2 - im.width / 2), int(cy - im.height / 2)))

def pill(fr, lab, cx, cy, size=40, pad=70):
    f = font("bold", size); tw = int(f.getlength(lab)); w, h = tw + pad, int(size * 2.1)
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], h // 2, fill=C["blue"]); d.text(((w - tw) / 2, (h - size * 1.2) / 2), lab, font=f, fill=C["white"])
    fr.alpha_composite(im, (int(cx - w / 2), int(cy - h / 2)))

def card(fr, lab, cx, cy, w=430, h=190):
    im = Image.new("RGBA", (w + 40, h + 40), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([24, 30, w + 24, h + 30], 36, fill=(10, 30, 120, 40)); im = im.filter(ImageFilter.GaussianBlur(12)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([20, 20, w + 20, h + 20], 36, fill=(255, 255, 255, 220), outline=(255, 255, 255, 255), width=3)
    f = fit(lab, "black", 58, w - 60); d.text((20 + (w - f.getlength(lab)) / 2, 20 + h / 2 - f.size * .62), lab, font=f, fill=C["blue"])
    fr.alpha_composite(im, (int(cx - im.width / 2), int(cy - im.height / 2)))

def bignum(fr, txt, cy):
    f = fit(txt, "black", 560, 860)
    sh = timg(txt, f, (10, 30, 120, 70)).filter(ImageFilter.GaussianBlur(26)); fr.alpha_composite(sh, (int(W / 2 - sh.width / 2 + 18), int(cy - sh.height / 2 + 40)))
    center(fr, txt, f, C["blue"], cy)

def page(p, i, n):
    fr = bg(i)
    center(fr, "Xusniddin Tech", font("bold", 38), C["ink"], 92)
    if p.get("pill"): pill(fr, p["pill"], 140, 92, 34, 56)
    k = p["type"]
    if k == "cover":
        ls = p["lines"]; sizes = [fit(x[0], x[1], {"black": 170, "light": 110}.get(x[1], 90)).size for x in ls]
        y = 640 - sum(s * 1.05 for s in sizes) / 2
        for x, s in zip(ls, sizes): center(fr, x[0], fit(x[0], x[1], s), C[x[2]], y + s * .5); y += s * 1.05
        if p.get("sub"): center(fr, p["sub"], fit(p["sub"], "semi", 58), C["ink"], y + 70)
        pill(fr, p.get("cta", "Suring"), W / 2, 1200)
    elif k == "number":
        bignum(fr, p["num"], 470)
        center(fr, p["head"], fit(p["head"], "black", 120), C["ink"], 860)
        center(fr, p["l1"], fit(p["l1"], "semi", 54), C["ink"], 990)
        center(fr, p["l2"], fit(p["l2"], "semi", 54), C["blue"], 1065)
    elif k == "cards":
        center(fr, p["kicker"], fit(p["kicker"], "light", 90), C["ink"], 300)
        center(fr, p["title"], fit(p["title"], "black", 130), C["ink"], 420)
        for j, lab in enumerate(p["cards"][:4]):
            card(fr, lab, W / 2 + (-235 if j % 2 == 0 else 235), 680 + (j // 2) * 240)
        if p.get("note"): center(fr, p["note"], fit(p["note"], "semi", 50), C["blue"], 1170)
    elif k == "cta":
        center(fr, p["l1"], fit(p["l1"], "black", 180), C["ink"], 520)
        center(fr, p["l2"], fit(p["l2"], "black", 180), C["blue"], 700)
        center(fr, p["q"], fit(p["q"], "semi", 52), C["ink"], 880)
        pill(fr, p.get("pill_text", "Kuzatib boring: @xusniddintech"), W / 2, 1060, 44, 100)
    center(fr, f"{i + 1}/{n}", font("semi", 30), (74, 88, 120), 1295)
    return fr.convert("RGB")

if __name__ == "__main__":
    spec = json.load(open(sys.argv[1])); out = sys.argv[2]; os.makedirs(out, exist_ok=True)
    ps = spec["pages"]
    for i, p in enumerate(ps): page(p, i, len(ps)).save(os.path.join(out, f"{i + 1:02d}.jpg"), quality=93)
    print("ok", len(ps))
