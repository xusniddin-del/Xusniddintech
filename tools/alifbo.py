"""Eski o'zbek lotin yozuvini yangi alifboga (O'RQ-1184) o'tkazadi:
O' -> Ö, G' -> Ğ, Sh -> Ş, Ch -> Ç. Tutuq belgisi (ma'no) saqlanadi.
Hashtag, @handle, URL va inglizcha/brend so'zlar o'zgarmaydi.
Foydalanish: python3 tools/alifbo.py plan/2026-11-08.json ...  (faylni joyida o'zgartiradi)"""
import json, re, sys

APOS = "'‘’ʻ`"
SKIP_STEMS = ("scratch", "chatgpt", "finish", "shift", "shortcut", "unsplash", "xusniddintech",
              "photoshop", "chrome", "chat", "push", "cache", "dashboard", "match", "branch", "fetch",
              "search", "english", "fresh", "sketch", "touch", "switch", "flash", "telegram", "youtube",
              "canva", "figma", "github", "windows", "microsoft", "excel", "powerpoint", "illustrator")
SKIP_EXACT = {"tech", "black", "blue", "ink", "light", "calm", "playful", "cards", "cover", "cta",
              "number", "subscribe", "words"}
SKIP_KEYS = {"type", "mood", "handle", "media", "date", "time", "topic", "url"}

def _case(src, up, low):
    return up if src[0].isupper() else low

def word(w):
    lw = w.lower()
    if lw in SKIP_EXACT or lw.startswith(SKIP_STEMS):
        return w
    w = re.sub(f"([Oo])[{APOS}]", lambda m: "Ö" if m.group(1) == "O" else "ö", w)
    w = re.sub(f"([Gg])[{APOS}]", lambda m: "Ğ" if m.group(1) == "G" else "ğ", w)
    w = re.sub("[Ss][Hh]", lambda m: "Ş" if m.group(0)[0] == "S" else "ş", w)
    w = re.sub("[Cc][Hh]", lambda m: "Ç" if m.group(0)[0] == "C" else "ç", w)
    return w

TOKEN = re.compile(r"https?://\S+|[#@][\w]+|[\w" + APOS + r"]+")

def convert(text):
    return TOKEN.sub(lambda m: m.group(0) if m.group(0)[0] in "#@h" and (m.group(0)[0] in "#@" or m.group(0).startswith("http")) else word(m.group(0)), text)

def walk(x, key=None):
    if isinstance(x, dict):
        return {k: (v if k in SKIP_KEYS else walk(v, k)) for k, v in x.items()}
    if isinstance(x, list):
        return [walk(i, key) for i in x]
    if isinstance(x, str):
        return convert(x)
    return x

if __name__ == "__main__":
    for p in sys.argv[1:]:
        d = json.load(open(p, encoding="utf-8"))
        json.dump(walk(d), open(p, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print("ok", p)
