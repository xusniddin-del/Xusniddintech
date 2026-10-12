#!/usr/bin/env python3
# Xusniddin Tech: 16 Oct - 30 Nov 2026 content plan -> specs + captions
import json, os, re, datetime as dt

TAGS = {
 "komp": "#kompyutersavodxonligi #kompyuter #office #xusniddintech #ozbekcha",
 "kiber": "#kiberxavfsizlik #xavfsizlik #parol #xusniddintech #ozbekcha",
 "uiux": "#uiux #uidesign #figma #xusniddintech #ozbekcha",
 "ai": "#suniyintellekt #ai #chatgpt #xusniddintech #ozbekcha",
 "dizayn": "#grafikdizayn #dizayn #dizayner #xusniddintech #ozbekcha",
 "scratch": "#scratch #bolalaruchun #dasturlash #xusniddintech #ozbekcha",
 "vibe": "#vibecoding #dasturlash #ai #xusniddintech #ozbekcha",
}
TIME = {0: "19:00", 1: "20:30", 2: "19:00", 3: "20:30", 4: "18:30", 5: "20:00", 6: "19:30"}
TOPIC = {0: "komp", 1: "ai", 2: "kiber", 3: "dizayn", 4: "uiux", 5: "scratch", 6: "vibe"}
MOOD = {"ai": "tech", "dizayn": "calm", "scratch": "playful", "vibe": "tech"}

# ---------- CAROUSELS: hook(light, BLACK), sub, 5 points (head, l1, l2), optional cards page at idx 3, question
CAR = {
 "uiux": [
  dict(h=("Farqi nima?", "UI VA UX"), sub="5 ta oddiy misolda", pts=[
    ("UI — KO'RINISH", "Rang, shrift, tugma", "ekranda nima ko'rinadi"),
    ("UX — TAJRIBA", "Foydalanish qulaymi?", "foydalanuvchi nima his qiladi"),
    ("MISOL: ESHIK", "UI — eshik dizayni", "UX — uni ochish osonligi"),
    ("IKKALASI KERAK", "Chiroyli, lekin noqulay —", "foydalanuvchi ketib qoladi"),
    ("QAYERDAN BOSHLASH", "Avval UX: muammo va yo'l", "keyin UI: chiroyli ko'rinish")],
   q="Siz UI'ga qiziqasizmi yoki UX'ga?"),
  dict(h=("Yaxshi tugma", "QOIDALARI"), sub="Har bir dizayner bilishi shart", pts=[
    ("KATTA BO'LSIN", "Kamida 44 px balandlik", "barmoq bilan oson bosilsin"),
    ("ANIQ MATN", "\"OK\" emas — \"Saqlash\"", "nima bo'lishini ayting"),
    ("BITTA ASOSIY", "Ekranda 1 ta asosiy tugma", "qolganlari ikkinchi darajali"),
    ("HOLATLARI", "Oddiy, hover, bosilgan", "va o'chirilgan holat"),
    ("KONTRAST", "Fon bilan aniq ajralsin", "4.5:1 nisbatdan kam emas")],
   q="Qaysi qoidani buzib kelgansiz?"),
  dict(h=("Figma", "SHORTCUTLAR"), sub="Ishingizni 2 barobar tezlashtiring", pts=[
    ("FRAME", "F — yangi frame", "ekran o'lchamini tanlang"),
    ("AUTO LAYOUT", "Shift + A", "elementlar o'zi joylashadi"),
    ("KOMPONENT", "Ctrl + Alt + K", "bir marta yasang, ko'p ishlating"),
    ("MASOFA", "Alt bosib turing", "elementlar orasini ko'rasiz"),
    ("NUSXA", "Ctrl + D", "tanlanganni takrorlash")],
   q="Sizning sevimli shortcutingiz qaysi?"),
  dict(h=("Tartibli dizayn", "8 PX TIZIMI"), sub="Professional maketlarning siri", pts=[
    ("NIMA BU?", "Barcha o'lchamlar 8 ga", "karrali: 8, 16, 24, 32"),
    ("NEGA 8?", "Ko'p ekranlarga mos", "oson bo'linadi, aniq ko'rinadi"),
    ("ICHKI MASOFA", "Tugma ichida 16 px", "kartochkada 24 px"),
    ("TASHQI MASOFA", "Bloklar orasi 32-48 px", "bo'limlar orasi 64+"),
    ("FIGMA'DA", "Nudge = 8 qilib qo'ying", "Shift + strelka 8 px suradi")],
   q="Siz qaysi tizim bilan ishlaysiz?"),
  dict(h=("Shrift tanlash", "QOIDALARI"), sub="UI uchun 5 ta maslahat", pts=[
    ("2 TADAN KO'P EMAS", "Sarlavha va matn uchun", "1-2 ta shrift yetarli"),
    ("O'QILISHI", "Matn kamida 16 px", "mobil ekranda ham aniq"),
    ("IERARXIYA", "H1, H2, matn — har xil", "o'lcham va qalinlikda"),
    ("QATOR ORASI", "Line-height 1.4 — 1.6", "matn nafas olsin"),
    ("BEPUL SHRIFTLAR", "Inter, Manrope, Roboto", "Google Fonts'da bor")],
   q="Siz qaysi shriftni yaxshi ko'rasiz?"),
  dict(h=("Mobil ekran", "XATOLARI"), sub="Yangi dizaynerlar ko'p qiladi", pts=[
    ("MAYDA TUGMALAR", "Barmoq sig'masa —", "foydalanuvchi asabiylashadi"),
    ("JUDA KO'P MATN", "Mobilda qisqa yozing", "asosiysi birinchi"),
    ("XAVFSIZ ZONA", "Kamera va pastki chiziq", "ostida matn qolmasin"),
    ("PAST KONTRAST", "Quyoshda ko'rinmaydi", "kulrang ustida kulrang yo'q"),
    ("BOSH BARMOQ", "Asosiy tugma pastda", "bir qo'lda yetadigan joyda")],
   q="Qaysi xatoni ilovalarda ko'p ko'rasiz?"),
  dict(h=("UI/UX'ni", "NOLDAN O'RGANISH"), sub="5 qadamli yo'l xaritasi", pts=[
    ("ASOSLAR", "Rang, shrift, kompozitsiya", "dizayn tamoyillari"),
    ("FIGMA", "Frame, auto layout", "komponentlar, prototip"),
    ("UX JARAYONI", "Tadqiqot, persona", "wireframe, test"),
    ("NUSXA OLING", "Mashhur ilovalarni", "qayta chizib mashq qiling"),
    ("PORTFOLIO", "3 ta to'liq loyiha", "Behance yoki Dribbble'da")],
   q="Siz hozir qaysi qadamdasiz?"),
 ],
 "komp": [
  dict(h=("Word'dagi", "SIRLI TUGMALAR"), sub="Ko'pchilik bilmaydi", pts=[
    ("STILLAR", "Sarlavha 1, Sarlavha 2", "mundarija o'zi yasaladi"),
    ("YANGI SAHIFA", "Ctrl + Enter", "Enter'ni bosib o'tirmang"),
    ("FORMAT PAINTER", "Uslubni nusxalash", "bitta bosishda boshqa joyga"),
    ("F4", "Oxirgi amalni takrorlash", "rang, shrift — hammasi"),
    ("QIDIRISH", "Ctrl + H", "so'zni bir zumda almashtiring")],
   q="Qaysi birini bilmagan edingiz?"),
  dict(h=("Excel'ning", "5 TA FORMULASI"), sub="Har kuni kerak bo'ladi", pts=[
    ("SUM", "=SUM(A1:A10)", "ustunni qo'shib beradi"),
    ("AVERAGE", "=AVERAGE(B1:B10)", "o'rtacha qiymat"),
    ("IF", "=IF(C1>50;\"O'tdi\";\"Yiqildi\")", "shartga qarab javob"),
    ("VLOOKUP", "Jadvaldan qidirish", "ism bo'yicha bahoni topish"),
    ("COUNTIF", "=COUNTIF(D:D;\"Ha\")", "nechta \"Ha\" borligini sanaydi")],
   q="Qaysi formulani ko'p ishlatasiz?"),
  dict(h=("Kompyuter", "SEKINLASHDIMI?"), sub="5 ta tez yechim", pts=[
    ("AVTOZAPUSK", "Ctrl+Shift+Esc → Startup", "keraksizini o'chiring"),
    ("DISK C", "Kamida 15% bo'sh joy", "Disk Cleanup qiling"),
    ("BRAUZER", "20 ta tab = ko'p RAM", "keraksizini yoping"),
    ("YANGILANISH", "Windows va drayverlar", "doim yangi bo'lsin"),
    ("SSD", "Eng katta tezlik", "HDD o'rniga SSD qo'ying")],
   q="Sizning kompyuteringiz necha soniyada yonadi?"),
  dict(h=("Fayllar", "TARTIBSIZMI?"), sub="Papka tizimi sirlari", pts=[
    ("ASOSIY PAPKALAR", "O'qish, Ish, Shaxsiy", "hammasi shu 3 tasiga"),
    ("NOM QOIDASI", "2026-10-26_hisobot", "sana boshida — tartib o'zi"),
    ("ISH STOLI", "Ish stoli — ombor emas", "har hafta tozalang"),
    ("YUKLANMALAR", "Downloads'ni har oy", "saralang yoki o'chiring"),
    ("BULUT", "Google Drive, OneDrive", "muhim fayllar nusxasi")],
   q="Ish stolingizda nechta fayl bor? 😄"),
  dict(h=("PowerPoint", "QOIDALARI"), sub="Taqdimotingiz zerikarli bo'lmasin", pts=[
    ("1 SLAYD = 1 FIKR", "Hammasini bitta slaydga", "tiqmang"),
    ("6 X 6", "Ko'pi bilan 6 qator", "har qatorda 6 so'z"),
    ("KATTA SHRIFT", "Kamida 28 pt", "orqa qatordan ham ko'rinsin"),
    ("RASMLAR", "Sifatli, katta rasm", "matndan ko'ra kuchli"),
    ("ANIMATSIYA", "Kam va bir xil", "har slaydda boshqa emas")],
   q="Qaysi qoidani buzgansiz?"),
  dict(h=("Brauzer", "SHORTCUTLARI"), sub="Sichqonchasiz tez ishlang", pts=[
    ("YANGI TAB", "Ctrl + T", "yopilganini qaytarish: Ctrl+Shift+T"),
    ("MANZIL", "Ctrl + L", "manzil qatoriga o'tish"),
    ("TABLAR ARO", "Ctrl + Tab", "keyingi tabga o'tish"),
    ("XATCHO'P", "Ctrl + D", "sahifani saqlab qo'yish"),
    ("YASHIRIN", "Ctrl + Shift + N", "inkognito oyna")],
   q="Siz nechta tab ochib yurasiz?"),
  dict(h=("Google Docs", "IMKONIYATLARI"), sub="Word'dan qolishmaydi", pts=[
    ("BIRGA ISHLASH", "Bir hujjatda", "bir nechta odam yozadi"),
    ("OVOZ BILAN", "Ctrl+Shift+S", "gapiring — o'zi yozadi"),
    ("TARIX", "Versiyalar tarixi", "eski holatga qaytish"),
    ("IZOHLAR", "Ctrl+Alt+M", "matnga izoh qoldirish"),
    ("OFFLINE", "Internetsiz ham", "yozish mumkin")],
   q="Siz Word'ni tanlaysizmi yoki Google Docs'ni?"),
 ],
 "kiber": [
  dict(h=("Fishing", "BELGILARI"), sub="Soxta xabarni qanday tanish mumkin", pts=[
    ("SHOSHILTIRISH", "\"24 soatda bloklanadi!\"", "— bu tuzoq"),
    ("SOXTA LINK", "telegrarn.org, c1ick.uz", "harflarga diqqat qiling"),
    ("SOVG'A VA YUTUQ", "\"Siz iPhone yutdingiz!\"", "bepul pishloq — qopqonda"),
    ("KOD SO'RASH", "SMS kodni hech kimga", "hatto \"bank\"ka ham bermang"),
    ("NOTANISH FAYL", ".apk, .exe yuborilsa", "ochmang, o'chiring")],
   q="Sizga shunday xabar kelganmi?"),
  dict(h=("Telegram'ni", "HIMOYA QILING"), sub="5 ta sozlama — 3 daqiqa", pts=[
    ("IKKI BOSQICHLI", "Maxfiylik → 2-bosqich", "parol qo'ying"),
    ("SEANSLAR", "Qurilmalar ro'yxatini", "tekshiring, begonani o'chiring"),
    ("RAQAMNI YASHIRING", "Telefon raqam →", "\"Hech kim\""),
    ("GURUHLAR", "Kim qo'sha oladi →", "\"Kontaktlarim\""),
    ("KOD", "Login kodini hech kimga", "aytmang — hech qachon")],
   q="2-bosqichli parolni yoqdingizmi?"),
  dict(h=("Bepul Wi-Fi", "XAVFLIMI?"), sub="Kafeda internetdan oldin o'qing", pts=[
    ("SOXTA TARMOQ", "\"Free_WiFi\" — kimdir", "atayin ochgan bo'lishi mumkin"),
    ("BANK YO'Q", "Ochiq Wi-Fi'da", "bank ilovasiga kirmang"),
    ("HTTPS", "Manzil qulf belgisi", "bilan bo'lsin"),
    ("AVTO ULANISH", "Avtomatik ulanishni", "o'chirib qo'ying"),
    ("MOBIL INTERNET", "Muhim ishlar uchun", "o'z internetingiz xavfsizroq")],
   q="Siz ochiq Wi-Fi'dan foydalanasizmi?"),
  dict(h=("Telefoningiz", "BUZILGANMI?"), sub="5 ta xavfli belgi", pts=[
    ("BATAREYA", "Tez tugayapti", "va telefon qiziyapti"),
    ("NOTANISH ILOVA", "O'zingiz o'rnatmagan", "ilova paydo bo'ldi"),
    ("REKLAMA", "Hamma joyda", "kutilmagan reklama"),
    ("TRAFIK", "Internet tez", "sarflanyapti"),
    ("XABARLAR", "Do'stlaringizga siz nomingizdan", "g'alati xabar ketgan")],
   q="Shunday holat bo'lganmi?"),
  dict(h=("Internetga", "NIMANI QO'YMASLIK"), sub="Bitta rasm ham xavfli bo'lishi mumkin", pts=[
    ("HUJJATLAR", "Pasport, ID karta", "rasmini joylamang"),
    ("BILET VA CHEK", "Shtrix-kodda", "shaxsiy ma'lumot bor"),
    ("MANZIL", "Uy, maktab joyi", "real vaqtda — yo'q"),
    ("KARTA", "Karta raqami, CVV", "hech qachon"),
    ("SAFAR", "\"Uyda hech kim yo'q\"", "qaytgandan keyin joylang")],
   q="Qaysi birini bilmagan edingiz?"),
  dict(h=("Ma'lumotlarni", "YO'QOTMANG"), sub="3-2-1 zaxira qoidasi", pts=[
    ("3 NUSXA", "Muhim fayl —", "3 ta nusxada saqlansin"),
    ("2 XIL JOY", "Kompyuter + fleshka", "yoki tashqi disk"),
    ("1 TASI UZOQDA", "Bulut: Google Drive,", "OneDrive, iCloud"),
    ("AVTOMATIK", "Zaxirani avto", "rejimga qo'ying"),
    ("TEKSHIRING", "Oyiga bir marta", "fayl ochilishini sinang")],
   q="Siz oxirgi marta qachon zaxira qilgansiz?"),
 ],
}

# ---------- VIDEOS: hook lines, hook2 lines, cards(kicker,title,[4]), 3 points (num, head, l1, l2), outro lines
VID = {
 "ai": [
  dict(hook=[("ChatGPT bilan", "light"), ("REZYUME", "black"), ("10 DAQIQADA", "blue")], h2=[("faqat to'g'ri", "light"), ("PROMPT KERAK", "blue")],
   cards=("Rezyume", "4 BO'LIM", ["MAQSAD", "TAJRIBA", "KO'NIKMA", "TA'LIM"]), pts=[
    ("1", "MA'LUMOT BERING", "Ish joylari, yillar, natijalar", "ro'yxat qilib yozing"),
    ("2", "ROL BERING", "\"Sen HR mutaxassisisan\"", "deb boshlang"),
    ("3", "TAHRIRLANG", "Har gapni tekshiring", "yolg'on yozdirmang")],
   end=[("AI yozadi —", "light"), ("SIZ", "black"), ("TEKSHIRASIZ", "blue")]),
  dict(hook=[("Rasm chizadigan", "light"), ("4 TA", "black"), ("AI", "blue")], h2=[("matn yozing —", "light"), ("RASM OLING", "blue")],
   cards=("Rasm uchun", "AI'LAR", ["MIDJOURNEY", "DALL-E", "LEONARDO", "IDEOGRAM"]), pts=[
    ("1", "MIDJOURNEY", "Eng badiiy natija", "pullik, lekin kuchli"),
    ("2", "LEONARDO", "Kuniga bepul limit", "boshlovchilar uchun"),
    ("3", "IDEOGRAM", "Rasm ichida matn", "logotip va posterlar")],
   end=[("prompt qanchalik", "light"), ("ANIQ BO'LSA", "black"), ("SHUNCHALIK ZO'R", "blue")]),
  dict(hook=[("AI bilan", "light"), ("2 BAROBAR", "black"), ("TEZ O'QING", "blue")], h2=[("ko'chirmang —", "light"), ("TUSHUNING", "blue")],
   cards=("O'qish uchun", "AI USULLARI", ["XULOSA", "TEST", "MISOL", "REJA"]), pts=[
    ("1", "XULOSA", "\"Shu matnni 5 punktda", "qisqacha tushuntir\""),
    ("2", "TEST", "\"Mavzu bo'yicha 10 ta", "savol tuz\""),
    ("3", "SODDA TIL", "\"12 yoshli bolaga", "tushuntirgandek ayt\"")],
   end=[("AI — ustoz emas,", "light"), ("YORDAMCHI", "blue")]),
  dict(hook=[("Ovozni", "light"), ("AI", "black"), ("YARATADI", "blue")], h2=[("matndan —", "light"), ("NUTQQA", "blue")],
   cards=("Ovoz uchun", "AI'LAR", ["ELEVENLABS", "SUNO", "WHISPER", "NOTEBOOKLM"]), pts=[
    ("1", "ELEVENLABS", "Matnni tabiiy ovozga", "aylantiradi"),
    ("2", "WHISPER", "Ovozni matnga", "yozib beradi"),
    ("3", "SUNO", "Bir gapdan", "butun qo'shiq")],
   end=[("begona ovozni", "light"), ("RUXSATSIZ", "black"), ("ISHLATMANG", "blue")]),
  dict(hook=[("Qaysi AI", "light"), ("SIZGA", "black"), ("KERAK?", "blue")], h2=[("4 ta asosiy", "light"), ("YORDAMCHI", "blue")],
   cards=("Taqqoslash", "4 TA AI", ["CHATGPT", "CLAUDE", "GEMINI", "PERPLEXITY"]), pts=[
    ("1", "CHATGPT", "Universal yordamchi", "rasm, ovoz, matn"),
    ("2", "CLAUDE", "Uzun matn va kod", "tahlil va yozish"),
    ("3", "PERPLEXITY", "Internetdan qidiradi", "manbalari bilan")],
   end=[("bittasini tanlang va", "light"), ("HAR KUNI", "black"), ("ISHLATING", "blue")]),
  dict(hook=[("AI'ga", "light"), ("ISHONSA", "black"), ("BO'LADIMI?", "blue")], h2=[("ba'zan AI ham", "light"), ("ADASHADI", "blue")],
   cards=("Tekshiring", "3 QOIDA", ["MANBA", "RAQAM", "SANA", "MANTIQ"]), pts=[
    ("1", "MANBA SO'RANG", "\"Bu ma'lumot qayerdan?\"", "deb so'rang"),
    ("2", "RAQAMLAR", "Statistika va sanalarni", "rasmiy saytda tekshiring"),
    ("3", "SHAXSIY MA'LUMOT", "Parol, karta raqamini", "AI'ga yozmang")],
   end=[("AI — tez,", "light"), ("SIZ —", "black"), ("AQLLI", "blue")]),
 ],
 "dizayn": [
  dict(hook=[("Shriftlarni", "light"), ("TO'G'RI", "black"), ("JUFTLANG", "blue")], h2=[("2 ta shrift —", "light"), ("YETARLI", "blue")],
   cards=("Juftlik", "QOIDASI", ["SARLAVHA", "MATN", "KONTRAST", "UYG'UNLIK"]), pts=[
    ("1", "SERIF + SANS", "Playfair sarlavhaga", "Inter matnga"),
    ("2", "QALINLIK", "Sarlavha qalin,", "matn oddiy"),
    ("3", "BITTA OILA", "Bitta shriftning", "har xil og'irligi")],
   end=[("3 tadan ko'p", "light"), ("SHRIFT", "black"), ("ISHLATMANG", "blue")]),
  dict(hook=[("Kompozitsiya", "light"), ("UCHDAN BIR", "black"), ("QOIDASI", "blue")], h2=[("markazda emas —", "light"), ("CHIZIQDA", "blue")],
   cards=("Setka", "3 X 3", ["CHIZIQ", "NUQTA", "FOKUS", "BO'SH JOY"]), pts=[
    ("1", "SETKA", "Ekranni 3x3 ga", "bo'ling"),
    ("2", "KESISHMA", "Asosiy obyekt", "chiziqlar kesishgan joyda"),
    ("3", "BO'SH JOY", "Qolgan qism", "nafas uchun")],
   end=[("kameradagi", "light"), ("SETKANI", "black"), ("YOQING", "blue")]),
  dict(hook=[("Logotip", "light"), ("QANDAY", "black"), ("YARALADI?", "blue")], h2=[("4 ta", "light"), ("BOSQICH", "blue")],
   cards=("Jarayon", "LOGO", ["BRIF", "ESKIZ", "VEKTOR", "TAQDIMOT"]), pts=[
    ("1", "BRIF", "Mijoz kim, kimga sotadi", "qanday his kerak"),
    ("2", "ESKIZ", "Qog'ozda 20+ g'oya", "eng yaxshi 3 tasi"),
    ("3", "VEKTOR", "Illustrator yoki Figma'da", "oq-qorada ham ishlasin")],
   end=[("yaxshi logo —", "light"), ("ODDIY", "blue")]),
  dict(hook=[("Instagram post", "light"), ("XATOLARI", "black")], h2=[("ko'pchilik", "light"), ("SHUNDAY QILADI", "blue")],
   cards=("Xatolar", "TOP 4", ["KO'P MATN", "MAYDA SHRIFT", "KO'P RANG", "TARTIBSIZ"]), pts=[
    ("1", "KO'P MATN", "Bir postda", "bitta asosiy fikr"),
    ("2", "MAYDA SHRIFT", "Telefonda", "o'qib bo'lmaydi"),
    ("3", "KO'P RANG", "Brend ranglari", "2-3 ta yetarli")],
   end=[("kamroq —", "light"), ("KUCHLIROQ", "blue")]),
  dict(hook=[("Rang palitrasi", "light"), ("10 SONIYADA", "blue")], h2=[("tayyor", "light"), ("SAYTLAR", "blue")],
   cards=("Palitra", "SAYTLARI", ["COOLORS", "ADOBE COLOR", "COLORHUNT", "HAPPY HUES"]), pts=[
    ("1", "COOLORS", "Probel — yangi palitra", "yoqqanini qulflang"),
    ("2", "ADOBE COLOR", "Rasmdan ranglarni", "ajratib oladi"),
    ("3", "COLORHUNT", "Tayyor", "mashhur palitralar")],
   end=[("ranglar —", "light"), ("KAYFIYAT", "blue")]),
  dict(hook=[("Dizayner uchun", "light"), ("BEPUL", "black"), ("RESURSLAR", "blue")], h2=[("saqlab", "light"), ("QO'YING", "blue")],
   cards=("Resurslar", "TOP 4", ["UNSPLASH", "GOOGLE FONTS", "ICONIFY", "FREEPIK"]), pts=[
    ("1", "UNSPLASH", "Sifatli bepul", "fotosuratlar"),
    ("2", "GOOGLE FONTS", "1500+ bepul", "shriftlar"),
    ("3", "ICONIFY", "200 mingdan ortiq", "ikonka")],
   end=[("litsenziyani", "light"), ("DOIM", "black"), ("TEKSHIRING", "blue")]),
 ],
 "scratch": [
  dict(hook=[("Scratch", "light"), ("NIMA", "black"), ("O'ZI?", "blue")], h2=[("bloklar bilan", "light"), ("DASTURLASH", "blue")],
   cards=("Scratch'da", "YARATING", ["O'YIN", "MULTFILM", "HIKOYA", "MUSIQA"]), pts=[
    ("1", "BEPUL", "scratch.mit.edu", "brauzerda ishlaydi"),
    ("2", "BLOKLAR", "Kod yozmaysiz —", "bloklarni ulaysiz"),
    ("3", "8+ YOSH", "Bolalar uchun", "birinchi qadam")],
   end=[("bugun", "light"), ("BIRINCHI", "black"), ("LOYIHA", "blue")]),
  dict(hook=[("Birinchi", "light"), ("ANIMATSIYA", "black"), ("3 BLOKDA", "blue")], h2=[("mushukni", "light"), ("YURGIZAMIZ", "blue")],
   cards=("Bloklar", "KERAK", ["BAYROQ", "TAKRORLASH", "YURISH", "CHETDA QAYTISH"]), pts=[
    ("1", "BAYROQ", "\"Yashil bayroq bosilganda\"", "dastur boshlanadi"),
    ("2", "TAKRORLASH", "\"Doimo\" bloki ichiga", "harakatni qo'ying"),
    ("3", "YURISH", "\"10 qadam yur\" +", "\"chetga tegsa qayt\"")],
   end=[("mushuk", "light"), ("YURDI!", "blue")]),
  dict(hook=[("Qahramon", "light"), ("QANDAY", "black"), ("YURADI?", "blue")], h2=[("sir —", "light"), ("KOSTYUMLARDA", "blue")],
   cards=("Kostyum", "ANIMATSIYA", ["KOSTYUM", "KEYINGISI", "KUTISH", "TAKROR"]), pts=[
    ("1", "KOSTYUMLAR", "Har bir sprayt", "bir nechta rasmga ega"),
    ("2", "KEYINGI KOSTYUM", "Blokni \"doimo\"", "ichiga qo'ying"),
    ("3", "KUTISH", "0.2 soniya kuting", "harakat silliq bo'ladi")],
   end=[("rasm almashadi —", "light"), ("JONLANADI", "blue")]),
  dict(hook=[("O'yinga", "light"), ("BALL", "black"), ("QO'SHAMIZ", "blue")], h2=[("bu —", "light"), ("O'ZGARUVCHI", "blue")],
   cards=("Ball tizimi", "QADAMLAR", ["YARATISH", "NOL", "QO'SHISH", "KO'RSATISH"]), pts=[
    ("1", "YARATING", "O'zgaruvchilar →", "\"Ball\" nomli yangi"),
    ("2", "NOLGA", "Boshida \"Ball\"ni", "0 ga tenglang"),
    ("3", "QO'SHING", "Tegsa → \"Ball\"ni", "1 ga o'zgartiring")],
   end=[("endi", "light"), ("REKORD", "black"), ("QO'YING", "blue")]),
  dict(hook=[("Qahramonni", "light"), ("KLAVIATURA", "black"), ("BILAN BOSHQARING", "blue")], h2=[("strelkalar —", "light"), ("RUL", "blue")],
   cards=("Tugmalar", "4 YO'NALISH", ["YUQORI", "PASTGA", "CHAPGA", "O'NGGA"]), pts=[
    ("1", "TUGMA BOSILGANDA", "\"O'ng strelka bosilganda\"", "blokini oling"),
    ("2", "X NI O'ZGARTIR", "O'ngga +10", "chapga -10"),
    ("3", "Y NI O'ZGARTIR", "Yuqoriga +10", "pastga -10")],
   end=[("endi o'yin", "light"), ("SIZNIKI", "blue")]),
  dict(hook=[("Labirint", "light"), ("O'YINI", "black"), ("YASAYMIZ", "blue")], h2=[("devorga tegsang —", "light"), ("BOSHIGA", "blue")],
   cards=("Labirint", "KERAK", ["LABIRINT", "QAHRAMON", "DEVOR RANGI", "FINISH"]), pts=[
    ("1", "FON CHIZING", "Labirintni", "bitta rangda chizing"),
    ("2", "RANGGA TEGSA", "\"Rangga tegyaptimi?\"", "→ boshlang'ich joyga"),
    ("3", "FINISH", "Finishga tegsa →", "\"G'alaba!\" deydi")],
   end=[("do'stingizni", "light"), ("SINAB", "black"), ("KO'RING", "blue")]),
  dict(hook=[("Scratch'dan", "light"), ("KEYIN", "black"), ("NIMA?", "blue")], h2=[("keyingi", "light"), ("QADAMLAR", "blue")],
   cards=("Yo'l", "XARITA", ["SCRATCH", "PYTHON", "WEB", "O'YINLAR"]), pts=[
    ("1", "PYTHON", "Oddiy sintaksis", "matnli kod boshlanishi"),
    ("2", "WEB", "HTML, CSS —", "o'z saytingiz"),
    ("3", "O'YINLAR", "Godot yoki Roblox Studio", "haqiqiy o'yinlar")],
   end=[("har bir dasturchi", "light"), ("KICHIKDAN", "black"), ("BOSHLAGAN", "blue")]),
 ],
 "vibe": [
  dict(hook=[("Vibe coding", "light"), ("NIMA", "black"), ("O'ZI?", "blue")], h2=[("gapirasiz —", "light"), ("AI KOD YOZADI", "blue")],
   cards=("Vibe coding", "TAMOYIL", ["G'OYA", "PROMPT", "SINOV", "TUZATISH"]), pts=[
    ("1", "G'OYA", "Nima qilmoqchisiz —", "oddiy so'zlar bilan"),
    ("2", "AI YOZADI", "Kodni AI yaratadi", "siz natijani ko'rasiz"),
    ("3", "SINAB KO'RING", "Ishlamasa —", "AI'ga xatoni ayting")],
   end=[("g'oya bor bo'lsa —", "light"), ("YETARLI", "blue")]),
  dict(hook=[("Birinchi", "light"), ("SAYTINGIZ", "black"), ("5 DAQIQADA", "blue")], h2=[("kod bilmasdan", "light"), ("HAM BO'LADI", "blue")],
   cards=("Qadamlar", "SAYT", ["PROMPT", "DIZAYN", "TEKSHIRISH", "JOYLASH"]), pts=[
    ("1", "TASVIRLANG", "\"Portfolio sayt: ism,", "ishlar, aloqa\""),
    ("2", "USLUB BERING", "\"Ko'k-oq, zamonaviy,", "katta sarlavhalar\""),
    ("3", "JOYLANG", "Netlify yoki Vercel —", "bepul hosting")],
   end=[("bugun", "light"), ("SINAB", "black"), ("KO'RING", "blue")]),
  dict(hook=[("Yaxshi kod", "light"), ("PROMPT", "black"), ("FORMULASI", "blue")], h2=[("aniqroq —", "light"), ("YAXSHIROQ", "blue")],
   cards=("Prompt", "4 QISM", ["MAQSAD", "TEXNOLOGIYA", "MISOL", "CHEKLOV"]), pts=[
    ("1", "MAQSAD", "Dastur nima qiladi", "kim uchun"),
    ("2", "TEXNOLOGIYA", "HTML, Python, React —", "aniq ayting"),
    ("3", "BOSQICHMA-BOSQICH", "Birdan hammasini emas", "kichik qadamlar")],
   end=[("bitta prompt —", "light"), ("BITTA VAZIFA", "blue")]),
  dict(hook=[("Vibe coding", "light"), ("ASBOBLARI", "black")], h2=[("qaysi biri", "light"), ("SIZGA MOS?", "blue")],
   cards=("Asboblar", "TOP 4", ["CLAUDE CODE", "CURSOR", "LOVABLE", "REPLIT"]), pts=[
    ("1", "LOVABLE", "Saytni brauzerda", "noldan yasaydi"),
    ("2", "CURSOR", "AI bilan ishlaydigan", "kod muharriri"),
    ("3", "CLAUDE CODE", "Terminalda ishlaydi", "katta loyihalar uchun")],
   end=[("asbob emas —", "light"), ("G'OYA", "black"), ("MUHIM", "blue")]),
  dict(hook=[("Xato chiqdimi?", "light"), ("AI", "black"), ("TUZATADI", "blue")], h2=[("faqat to'g'ri", "light"), ("SO'RANG", "blue")],
   cards=("Xato", "TUZATISH", ["XATO MATNI", "KONTEKST", "NATIJA", "SABAB"]), pts=[
    ("1", "TO'LIQ XATO", "Xato matnini", "to'liq nusxalab bering"),
    ("2", "NIMA QILDINGIZ", "Qaysi tugmani bosganda", "xato chiqdi"),
    ("3", "SABABINI SO'RANG", "\"Nega bo'ldi?\" —", "keyingi safar o'zingiz bilasiz")],
   end=[("har xato —", "light"), ("DARS", "blue")]),
  dict(hook=[("Telegram bot", "light"), ("KODSIZ", "black"), ("YASAYMIZ", "blue")], h2=[("AI bilan", "light"), ("30 DAQIQADA", "blue")],
   cards=("Bot", "QADAMLAR", ["BOTFATHER", "TOKEN", "PROMPT", "ISHGA TUSHIRISH"]), pts=[
    ("1", "BOTFATHER", "/newbot — nom bering", "token oling"),
    ("2", "PROMPT", "\"Python'da bot yoz:", "salom desa javob bersin\""),
    ("3", "TOKENNI ASRANG", "Tokenni hech kimga", "ko'rsatmang")],
   end=[("birinchi botingiz", "light"), ("TAYYOR", "blue")]),
  dict(hook=[("Vibe coding'ning", "light"), ("XAVFLARI", "black")], h2=[("bilib", "light"), ("ISHLATING", "blue")],
   cards=("Ehtiyot", "BO'LING", ["PAROL", "TUSHUNISH", "ZAXIRA", "TEKSHIRUV"]), pts=[
    ("1", "PAROLLAR", "Kod ichida parol", "va token qoldirmang"),
    ("2", "TUSHUNING", "Ishlayotgan kodni", "AI'dan tushuntirtiring"),
    ("3", "ZAXIRA", "Git bilan saqlang —", "xato bo'lsa qaytasiz")],
   end=[("AI — tezlik,", "light"), ("BILIM —", "black"), ("KUCH", "blue")]),
 ],
}

def lines(ls):
    return [[t, "light" if w == "light" else "black", "blue" if w == "blue" else "ink"] for t, w in ls]

def car_spec(c):
    pages = [{"type": "cover", "lines": [[c["h"][0], "light", "ink"], [c["h"][1], "black", "blue"]], "sub": c["sub"], "cta": "Suring"}]
    for i, (h, l1, l2) in enumerate(c["pts"]):
        pages.append({"type": "number", "pill": f"0{i+1}", "num": str(i + 1), "head": h, "l1": l1, "l2": l2})
    pages.append({"type": "cta", "l1": "SAQLAB", "l2": "QO'YING", "q": c["q"]})
    return {"pages": pages}

def vid_spec(v, mood):
    sc = [{"type": "words", "dur": 3.2, "lines": lines(v["hook"])},
          {"type": "words", "dur": 2.6, "lines": lines(v["h2"])},
          {"type": "cards", "dur": 4.2, "kicker": v["cards"][0], "title": v["cards"][1], "cards": v["cards"][2]}]
    for n, h, l1, l2 in v["pts"]:
        sc.append({"type": "number", "dur": 3.3, "num": n, "head": h, "l1": l1, "l2": l2})
    sc.append({"type": "words", "dur": 3.0, "lines": lines(v["end"])})
    sc.append({"type": "subscribe", "dur": 4.6, "title": "SAHIFAMIZGA", "sub": "obuna bo'ling", "handle": "xusniddintech", "button": "Obuna", "thanks": "Yashang!", "tap_at": 2.0})
    return {"mood": mood, "scenes": sc}

def title_of(parts):
    s = " ".join(p for p in parts).strip()
    return s[0].upper() + s[1:].lower() if s.isupper() else s

ACR = {"UI","UX","AI","SSD","HDD","HTTPS","2FA","ID","CVV","PX","SUM","IF","CHATGPT","DALL-E","RAM","OK","H1","H2","SMS","WI-FI"}
def sc(t):
    out = []
    for i, w in enumerate(t.split(" ")):
        core = re.sub(r"[^\w\-']", "", w).upper()
        if core in ACR or not w.isupper(): out.append(w if core not in ACR else w.upper().replace("CHATGPT", "ChatGPT"))
        else: out.append(w.lower())
    r = " ".join(out).replace("WI-FI", "Wi-Fi").replace("PX", "px"); return r[:1].upper() + r[1:]
def pt(h, l1, l2):
    sep = " " if l1.rstrip()[-1] in ",—→+:-\"?!." else ", "
    return f"{h}\n{l1}{sep}{l2}"
def caption(topic, head, pts, tail):
    body = "\n\n".join(f"{i+1}) {p}" for i, p in enumerate(pts))
    return f"{head}\n\n{body}\n\n{tail}\n\n{TAGS[topic]}"

def build():
    out = []; ci = {k: 0 for k in CAR}; vi = {k: 0 for k in VID}
    d = dt.date(2026, 10, 16)
    while d <= dt.date(2026, 11, 30):
        wd = d.weekday(); tp = TOPIC[wd]; ds = d.isoformat()
        if tp in CAR:
            c = CAR[tp][ci[tp]]; ci[tp] += 1
            hook = sc(f"{c['h'][0]} {c['h'][1]}") + f"\n{c['sub']} 👇"
            cap = caption(tp, hook, [pt(h, l1, l2) for h, l1, l2 in c["pts"]],
                          f"💾 Saqlab qo'ying, kerak bo'ladi.\n💬 {c['q']}")
            out.append(dict(date=ds, type="carousel", topic=tp, time=TIME[wd], spec=car_spec(c), caption=cap,
                            title=f"{c['h'][0]} {c['h'][1]}"))
        else:
            v = VID[tp][vi[tp]]; vi[tp] += 1
            hook_t = " ".join(t for t, _ in v["hook"])
            hook = sc(hook_t)
            cap = caption(tp, hook + " 🎬", [pt(h, l1, l2) for n, h, l1, l2 in v["pts"]],
                          "💾 Saqlab qo'ying va do'stingizga yuboring.\n🔔 Har kuni foydali kontent — kuzatib boring.")
            out.append(dict(date=ds, type="video", topic=tp, time=TIME[wd], spec=vid_spec(v, MOOD[tp]), caption=cap,
                            title=hook_t))
        d += dt.timedelta(days=1)
    return out

if __name__ == "__main__":
    items = build()
    os.makedirs("plan", exist_ok=True)
    json.dump(items, open("plan/all.json", "w"), ensure_ascii=False, indent=1)
    from collections import Counter
    print(len(items), Counter(i["type"] for i in items))
