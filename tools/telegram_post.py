#!/usr/bin/env python3
"""Send Instagram autopilot posts to a Telegram channel.

Manifest (posts/YYYY-MM-DD.json):
  {"post_at": "2026-10-13T20:30:00+05:00", "type": "video" | "carousel",
   "media": ["https://...mp4"] | ["https://...jpg", ...], "caption": "..."}
Media is downloaded immediately (Canva links expire in a few hours), then the
job waits until post_at and sends: video -> sendVideo, carousel -> sendMediaGroup.
"""
import json, os, sys, time, urllib.parse, urllib.request, urllib.error, uuid
from datetime import datetime, timezone

TOKEN = os.environ.get("TELEGRAM_BOT_TOKEN", "").strip()
CHAT = os.environ.get("TELEGRAM_CHAT_ID", "").strip()
API = f"https://api.telegram.org/bot{TOKEN}/"


def download(url, path):
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(req, timeout=120) as r, open(path, "wb") as f:
        f.write(r.read())
    return path


def multipart(method, fields, files):
    boundary = uuid.uuid4().hex
    body = b""
    for k, v in fields.items():
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"\r\n\r\n{v}\r\n".encode()
    for k, (name, path, ctype) in files.items():
        body += f"--{boundary}\r\nContent-Disposition: form-data; name=\"{k}\"; filename=\"{name}\"\r\nContent-Type: {ctype}\r\n\r\n".encode()
        body += open(path, "rb").read() + b"\r\n"
    body += f"--{boundary}--\r\n".encode()
    req = urllib.request.Request(API + method, data=body, headers={"Content-Type": f"multipart/form-data; boundary={boundary}"})
    try:
        with urllib.request.urlopen(req, timeout=300) as r:
            res = json.load(r)
    except urllib.error.HTTPError as e:
        res = json.loads(e.read() or b"{}")
    if not res.get("ok"):
        raise SystemExit(f"Telegram xatosi ({method}): {res.get('description', res)}")
    return res


def tg_caption(text, limit=1024):
    return text if len(text) <= limit else text[: limit - 1] + "…"


def main(paths):
    if not TOKEN or not CHAT:
        raise SystemExit("TELEGRAM_BOT_TOKEN yoki TELEGRAM_CHAT_ID secret'i qo'shilmagan (Settings → Secrets and variables → Actions).")
    def call(method, **params):
        q = urllib.parse.urlencode(params)
        for attempt in range(5):
            try:
                with urllib.request.urlopen(API + method + ("?" + q if q else ""), timeout=30) as r:
                    return json.load(r)
            except urllib.error.HTTPError as e:
                return json.loads(e.read() or b"{}")
            except (TimeoutError, urllib.error.URLError, OSError) as e:
                if attempt == 4:
                    raise
                print(f"::warning::{method} xato ({e}), {10 * (attempt + 1)}s dan keyin qayta urinish")
                time.sleep(10 * (attempt + 1))
    me = call("getMe")
    if not me.get("ok"):
        raise SystemExit(f"Bot tokeni noto'g'ri: {me.get('description')}")
    ch = call("getChat", chat_id=CHAT)
    if not ch.get("ok"):
        raise SystemExit(f"Kanal topilmadi yoki bot admin emas ({CHAT}): {ch.get('description')}")
    adm = call("getChatMember", chat_id=CHAT, user_id=me["result"]["id"])
    st = adm.get("result", {})
    if st.get("status") not in ("administrator", "creator") or st.get("can_post_messages") is False:
        raise SystemExit(f"Bot kanalda xabar joylash huquqiga ega emas (status: {st.get('status')})")
    print(f"::notice::Bot @{me['result']['username']} -> kanal '{ch['result'].get('title')}' tayyor")
    jobs = []
    for p in paths:
        m = json.load(open(p))
        files = []
        for i, url in enumerate(m["media"]):
            ext = ".mp4" if m["type"] == "video" else ".jpg"
            files.append(download(url, f"/tmp/{os.path.basename(p)}_{i}{ext}"))
        print(f"{p}: {len(files)} ta fayl yuklandi")
        jobs.append((datetime.fromisoformat(m["post_at"]), m, files))
    failed = []
    for when, m, files in sorted(jobs, key=lambda j: j[0]):
        wait = (when - datetime.now(timezone.utc)).total_seconds()
        if os.environ.get("SEND_NOW") != "1" and wait > 5.6 * 3600:
            print(f"{when.isoformat()} juda uzoq (>5.6 soat) — o'tkazib yuborildi, o'sha kuni qayta push qilinadi")
            continue
        if os.environ.get("SEND_NOW") != "1" and wait > 0:
            print(f"{when.isoformat()} gacha {int(wait // 60)} daqiqa kutiladi")
            time.sleep(wait)
        # "chats": optional list of extra/other channels; "default" = TELEGRAM_CHAT_ID secret
        chats = [CHAT if c == "default" else c for c in (m.get("chats") or ["default"])]
        for chat in chats:
            if chat != CHAT:
                adm = call("getChatMember", chat_id=chat, user_id=me["result"]["id"])
                st = adm.get("result", {})
                if not adm.get("ok") or st.get("status") not in ("administrator", "creator") or st.get("can_post_messages") is False:
                    print(f"::error::{chat}: bot kanalda admin emas yoki joylash huquqi yo'q ({adm.get('description') or st.get('status')})")
                    failed.append(chat)
                    continue
            try:
                send(chat, m, files)
                print(f"Yuborildi: {m['type']} -> {chat} ({when.isoformat()})")
            except SystemExit as e:
                print(f"::error::{chat}: {e.code}")
                failed.append(chat)
    if failed:
        raise SystemExit(f"Ba'zi kanallarga yuborilmadi: {', '.join(sorted(set(failed)))}")


def send(chat, m, files):
    cap = tg_caption(m.get("caption", ""))
    if m["type"] == "text":
        multipart("sendMessage", {"chat_id": chat, "text": m.get("caption", "")}, {})
    elif m["type"] == "video":
        multipart("sendVideo", {"chat_id": chat, "caption": cap, "supports_streaming": "true", "width": "1080", "height": "1920"},
                  {"video": ("reel.mp4", files[0], "video/mp4")})
    elif len(files) == 1:
        multipart("sendPhoto", {"chat_id": chat, "caption": cap}, {"photo": ("p.jpg", files[0], "image/jpeg")})
    else:
        for start in range(0, len(files), 10):
            chunk = files[start:start + 10]
            media = [{"type": "photo", "media": f"attach://f{i}"} for i in range(len(chunk))]
            if start == 0:
                media[0]["caption"] = cap
            multipart("sendMediaGroup", {"chat_id": chat, "media": json.dumps(media, ensure_ascii=False)},
                      {f"f{i}": (f"{i}.jpg", f, "image/jpeg") for i, f in enumerate(chunk)})


if __name__ == "__main__":
    try:
        main([p for p in sys.argv[1:] if p.endswith(".json")])
    except SystemExit as e:
        if e.code not in (0, None):
            print(f"::error::{e.code}")
        raise
    except Exception as e:
        print(f"::error::{type(e).__name__}: {e}")
        raise
