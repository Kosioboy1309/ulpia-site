#!/usr/bin/env python3
"""3 кадъра (1080x1350) за „Апартамент на седмицата“ в общия стандарт на Улпия (виж ulpia_style.py).

Употреба:  python3 apartment_of_week.py <папка site/img> <папка site/fonts> <config.json> <изходна папка>

config.json (пример: social/a7/config.json):
{"cover":"v/v7.jpg","plan":"plans/b3.jpg","title":"Апартамент А7","sub1":"2 спални · 2 бани · изложение юг-запад","sub2":"Сграда А · 3-ти етаж · кв. Коматево",
 "plan_tag":"Разпределение · А7","plan_title":"115,49 m² · тристаен","plan_rows":["ред 1","ред 2","ред 3"],"why_title":"Защо А7?","why":["точка 1","точка 2","точка 3","Плащане на етапи според строителството"]}
Без цени. Телефон и ulpia.bg са в зелената лента.
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from ulpia_style import *
import ulpia_style as U

IMG, FONTS, CFGP, OUT = sys.argv[1:5]; CFG = json.load(open(CFGP, encoding="utf-8")); U.setup(FONTS); os.makedirs(OUT, exist_ok=True)
cover = lambda: fit(opn(f"{IMG}/{CFG['cover']}"), W, 620, (0.5, 0.6))
plan = opn(f"{IMG}/{CFG['plan']}"); ident = CFG["title"].split()[-1]

# 1 – корица: снимка + голям номер + разпределение отдясно
fr, d = page(cover()); label(d, 72, 640, "Апартамент на седмицата")
T(d, 64, 676, ident, "forum", 200, GREEN)
y = 930
for ln in wrap(CFG["sub1"], "manrope", 500, 27, 440): T(d, 72, y, ln, "manrope", 27, INK, w=500); y += 38
for ln in wrap(CFG["sub2"], "manrope", 500, 24, 440): T(d, 72, y + 6, ln, "manrope", 24, MUTED, w=500); y += 34
pill(d, 72, 1118, CFG["plan_title"].split("·")[0].strip().replace("m²", "кв.м"), size=22)
pw, ph_ = (470, 520); p2 = plan.copy(); p2.thumbnail((pw, ph_)); fr.paste(p2, (545 + (pw - p2.width) // 2, 640 + (ph_ - p2.height) // 2))
band(d); fr.save(f"{OUT}/1.jpg", quality=92)

# 2 – разпределение
fr, d = page(fit(opn(f"{IMG}/{CFG['cover']}"), W, 400, (0.5, 0.5)), panel_top=340)
label(d, 72, 410, CFG["plan_tag"]); T(d, 66, 450, CFG["plan_title"].replace("m²", "кв.м"), "forum", 64, GREEN)
p3 = plan.copy(); p3.thumbnail((960, 480)); fr.paste(p3, ((W - p3.width) // 2, 545))
y = 545 + p3.height + 24
for r in CFG["plan_rows"]: T(d, 72, y, r, "manrope", 25, INK, w=500); y += 36
band(d); fr.save(f"{OUT}/2.jpg", quality=92)

# 3 – защо
fr, d = page(cover()); label(d, 72, 640, "Запишете оглед")
T(d, 66, 684, CFG["why_title"], "forum", 100, GREEN)
for i, t in enumerate(CFG["why"]):
    yy = 840 + i * 80; d.ellipse((74, yy + 12, 92, yy + 30), fill=GREEN); T(d, 114, yy, t, "manrope", 30, INK, w=500)
band(d, "Разгледайте свободните апартаменти"); fr.save(f"{OUT}/3.jpg", quality=92)
print("кадри: 3")
