#!/usr/bin/env python3
"""Ovozli reel + oblojka.

  python3 tools/render/voiced.py cover  plan/YYYY-MM-DD.json  media/YYYY-MM-DD-cover.jpg
  python3 tools/render/voiced.py render plan/YYYY-MM-DD.json  <ovoz_soniyasi>  media/ovozli/YYYY-MM-DD.mp4
  python3 tools/render/voiced.py prepend plan/YYYY-MM-DD.json in.mp4 out.mp4   # mavjud videoga oblojka qo'shish

plan["voice"] = har bir sahna uchun ovoz matni (sahnalar tartibida, "" = jim sahna).
render: sahna uzunliklari ovoz matni uzunligiga mutanosib (jami = ovoz soniyasi + 0.6),
musiqa pasaytiriladi, boshiga COVER_SEC soniyalik oblojka qo'yiladi.
vidIQ compose'da voiceover.startAtSeconds = COVER_SEC + 0.3, Buffer thumbnailOffset = 200 ms.
"""
import json, os, subprocess, sys, tempfile
sys.path.insert(0, os.path.dirname(__file__))
import reel
from PIL import Image, ImageDraw

COVER_SEC = 0.6
TOPIC = {"vibe": "VIBE CODING", "ai": "SUN'IY INTELLEKT", "dizayn": "GRAFIK DIZAYN", "scratch": "SCRATCH · BOLALAR",
         "kompyuter": "KOMPYUTER SAVODXONLIGI", "kiber": "KIBERXAVFSIZLIK", "uiux": "UI/UX DIZAYN"}
MIN = {"words": 1.6, "cards": 2.6, "number": 2.6, "cta": 2.4, "subscribe": 4.6}


def cover(plan, out):
    W, H, C = reel.W, reel.H, reel.C
    fr = reel.bg(3.0)
    # sarlavha = birinchi (hook) sahna qatorlari, o'sha uslub va ranglar bilan
    hook = next((s for s in plan["spec"]["scenes"] if s["type"] == "words"), None)
    src = hook["lines"] if hook else [[plan["title"], "black", "ink"]]
    lines = [(t, reel.fit(t, "light", 120, 940) if w == "light" else reel.fit(t, "black", 180, 960), C.get(c, C["ink"])) for t, w, c in src]
    hs = [f.size * 1.08 for _, f, _ in lines]; y = H / 2 - sum(hs) / 2 + 20
    for (txt, f, col), h in zip(lines, hs):
        reel.paste(fr, reel.timg(txt, f, col), W / 2, y + h / 2); y += h
    lab = TOPIC.get(plan.get("topic", ""), plan.get("topic", "").upper())
    f = reel.font("bold", 44); tw = int(f.getlength(lab)); w, h = tw + 100, 96
    im = Image.new("RGBA", (w, h), (0, 0, 0, 0)); d = ImageDraw.Draw(im)
    d.rounded_rectangle([0, 0, w - 1, h - 1], h // 2, fill=C["blue"]); d.text(((w - tw) / 2, 22), lab, font=f, fill=C["white"])
    reel.paste(fr, im, W / 2, H / 2 - sum(hs) / 2 - 110)
    reel.paste(fr, reel.timg("Xusniddin Tech", reel.font("bold", 42), C["ink"]), W / 2, 120)
    reel.paste(fr, reel.timg("@xusniddintech", reel.font("semi", 48), C["ink"]), W / 2, H / 2 + sum(hs) / 2 + 120)
    fr.convert("RGB").save(out, quality=92)


def prepend(cover_jpg, src, out):
    tmp = tempfile.mkdtemp(); c = os.path.join(tmp, "c.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-loop", "1", "-t", str(COVER_SEC), "-i", cover_jpg, "-f", "lavfi", "-t", str(COVER_SEC),
                    "-i", "anullsrc=r=44100:cl=stereo", "-r", "30", "-c:v", "libx264", "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-shortest", c], check=True)
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", c, "-i", src, "-filter_complex",
                    "[0:v][0:a][1:v][1:a]concat=n=2:v=1:a=1[v][a]", "-map", "[v]", "-map", "[a]", "-c:v", "libx264", "-crf", "20",
                    "-pix_fmt", "yuv420p", "-c:a", "aac", "-b:a", "128k", "-movflags", "+faststart", out], check=True)


def render(plan, voice_sec, out):
    sc = plan["spec"]["scenes"]; vo = plan["voice"]; assert len(vo) == len(sc), "voice va scenes soni teng emas"
    # har sahna o'z gapi ovozda boshlanganda boshlanadi (matn uzunligiga mutanosib taxmin);
    # ovoz videoda COVER_SEC + 0.3 da boshlanadi -> birinchi sahna +0.3; oxirgi (subscribe) kamida 4.6 s
    L = [max(len(v), 1) for v in vo]; tl = sum(L)
    durs = [voice_sec * l / tl for l in L]
    durs[0] += 0.3
    durs[-1] = max(MIN.get(sc[-1]["type"], 1.6), durs[-1] + 0.8)
    spec = {"mood": plan["spec"].get("mood", "tech"), "scenes": [dict(s, dur=round(d, 2)) for s, d in zip(sc, durs)]}
    tmp = tempfile.mkdtemp(); sp = os.path.join(tmp, "s.json"); json.dump(spec, open(sp, "w"), ensure_ascii=False)
    base = os.path.join(tmp, "b.mp4"); reel.main(sp, base)
    quiet = os.path.join(tmp, "q.mp4")
    subprocess.run(["ffmpeg", "-v", "error", "-y", "-i", base, "-c:v", "copy", "-af", "volume=0.45", "-c:a", "aac", "-b:a", "128k", quiet], check=True)
    cj = os.path.join(tmp, "cover.jpg"); cover(plan, cj); prepend(cj, quiet, out)
    print(json.dumps({"durs": [round(d, 2) for d in durs], "total": round(sum(durs) + COVER_SEC, 2)}))


if __name__ == "__main__":
    cmd, plan = sys.argv[1], json.load(open(sys.argv[2]))
    if cmd == "cover": cover(plan, sys.argv[3])
    elif cmd == "render": render(plan, float(sys.argv[3]), sys.argv[4])
    elif cmd == "prepend":
        tmp = tempfile.mkdtemp(); cj = os.path.join(tmp, "c.jpg"); cover(plan, cj); prepend(cj, sys.argv[3], sys.argv[4])
