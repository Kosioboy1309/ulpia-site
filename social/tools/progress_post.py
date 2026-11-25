#!/usr/bin/env python3
"""Пост „Прогрес на строителството“ в общия стандарт на Улпия (виж ulpia_style.py).
Генерира Instagram карусел (1.jpg … N.jpg) и два варианта за Facebook (fb_a.jpg – лента с етапи, fb_b.jpg – преди/сега).

Употреба:  python3 progress_post.py <папка site/fonts> <config.json> <изходна папка>
config.json: {"month":"Ноември 2026","cover":"снимка","slides":[{"src","title","sub"}],"why":["…"],
 "fb_a":{"title","sub","thumbs":[["снимка","етикет"],…]},"fb_b":{"before":"снимка","after":"снимка","title":["ред1","ред2"],"text":"…"}}
Пътищата са спрямо папката на config.json. Без цени.
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ulpia_style import *
import ulpia_style as U

FONTS, CFGP, OUT = sys.argv[1], sys.argv[2], sys.argv[3]
BASE = os.path.dirname(os.path.abspath(CFGP)); CFG = json.load(open(CFGP, encoding="utf-8")); U.setup(FONTS)
ph = lambda p: opn(os.path.join(BASE, p)); os.makedirs(OUT, exist_ok=True)
LBL = "Прогрес на строителството"

# ---------- Instagram: корица ----------
fr, d = page(fit(ph(CFG["cover"]), W, 620, (0.5, 0.95)))
label(d, 72, 640, LBL)
T(d, 66, 668, CFG["month"].split()[0], "forum", 190, GREEN, up=False)
T(d, 72, 905, "От плоча до колони", "forum", 50, INK)
T(d, 72, 985, "Плъзнете, за да видите как върви обектът.", "manrope", 27, MUTED, w=500)
pill(d, 72, 1060, CFG["month"], size=22)
band(d); fr.save(f"{OUT}/1.jpg", quality=92); n = 1
# ---------- Instagram: снимки ----------
tot = len(CFG["slides"])
for i, s in enumerate(CFG["slides"], 1):
    n += 1; fr, d = page(fit(ph(s["src"]), W, 860, (0.5, 0.55)), panel_top=800)
    label(d, 72, 868, f"{LBL} · {i:02d} / {tot:02d}")
    lines = wrap(s["title"], "forum", 400, 80, 940); y = 920
    for ln in lines: T(d, 72, y, ln, "forum", 80, GREEN); y += 96
    T(d, 72, y + 14, s["sub"], "manrope", 30, MUTED, w=500)
    band(d); fr.save(f"{OUT}/{n}.jpg", quality=92)
# ---------- Instagram: последен кадър ----------
n += 1; fr, d = page(fit(ph(CFG["cover"]), W, 620, (0.5, 0.95)))
label(d, 72, 640, "Строителството продължава")
for i, t in enumerate(["Вашият нов дом", "расте"]): T(d, 72, 690 + i * 92, t, "forum", 84, GREEN)
for i, t in enumerate(CFG["why"]):
    y = 905 + i * 56; d.ellipse((74, y + 11, 90, y + 27), fill=GREEN); T(d, 112, y, t, "manrope", 28, INK, w=500)
band(d, "Запишете оглед"); fr.save(f"{OUT}/{n}.jpg", quality=92)

# ---------- Facebook A: лента с етапи ----------
a = CFG["fb_a"]; fr, d = page(fit(ph(CFG["cover"]), W, 620, (0.5, 0.95)))
label(d, 72, 640, LBL)
T(d, 66, 684, a["title"], "forum", 88, GREEN)
T(d, 72, 800, a["sub"], "manrope", 28, MUTED, w=500)
tw = (W - 144 - 2 * 24) // 3
for k, (src, lab) in enumerate(a["thumbs"]):
    x = 72 + k * (tw + 24); y = 868
    im = fit(ph(src), tw, 170); m = Image.new("L", im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, tw, 170), 16, fill=255); fr.paste(im, (x, y), m)
    T(d, x + 2, y + 186, f"{k+1:02d}  {lab}", "manrope", 17, GREEN, w=600, track=0.18, up=True)
pill(d, 72, 1118, CFG["month"], size=22)
band(d); fr.save(f"{OUT}/fb_a.jpg", quality=92)

# ---------- Facebook B: преди / сега (като „Паркомясто −50%“) ----------
b = CFG["fb_b"]; fr, d = page(fit(ph(b["after"]), W, 620, (0.5, 0.95)))
pill(d, 72, 488, "СЕГА", size=20, fill=GREEN, h=48, pad=24)
label(d, 72, 640, "Прогрес на обекта")
for i, t in enumerate(b["title"]): T(d, 66, 688 + i * 96, t, "forum", 82, GREEN)
y = 688 + len(b["title"]) * 96 + 24
for ln in wrap(b["text"], "manrope", 500, 27, 430): T(d, 72, y, ln, "manrope", 27, MUTED, w=500); y += 40
pill(d, 72, max(y + 22, 1062), CFG["month"], size=22)
im = fit(ph(b["before"]), 480, 440); m = Image.new("L", im.size, 0); ImageDraw.Draw(m).rounded_rectangle((0, 0, 480, 440), 18, fill=255); fr.paste(im, (528, 700), m)
pill(d, 552, 724, "ПРЕДИ", size=20, fill=(60, 66, 72), h=48, pad=24)
band(d); fr.save(f"{OUT}/fb_b.jpg", quality=92)
print("IG кадри:", n, "+ fb_a.jpg, fb_b.jpg")
