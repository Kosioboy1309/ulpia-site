#!/usr/bin/env python3
"""Генерира 3 кадъра (1080x1350) за „Апартамент на седмицата“ на Улпия.

Употреба:  python3 apartment_of_week.py <папка site/img> <config.json> <изходна папка>

config.json (пример: social/a7/config.json):
{
 "cover": "v/v7.jpg",                 # снимка за корицата (site/img/v/*.jpg, 4:5 кадрира се по центъра)
 "plan": "plans/b3.jpg",              # разпределение (site/img/plans/<p>.jpg)
 "title": "Апартамент А7",
 "sub1": "2 спални · 2 бани · изложение юг-запад",
 "sub2": "Сграда А · 3-ти етаж · кв. Коматево",
 "plan_tag": "РАЗПРЕДЕЛЕНИЕ · А7",
 "plan_title": "115,49 m² · тристаен",
 "plan_rows": ["ред 1", "ред 2", "ред 3"],
 "why_title": "Защо А7?",
 "why": ["точка 1", "точка 2", "точка 3", "Плащане на етапи според строителството"]
}
Без цени. Телефон: 0894 611 161, sales@ulpia.bg, ulpia.bg (фиксирани в кадър 3).
"""
import sys, json
from PIL import Image, ImageDraw, ImageFont

IMG, CFG, OUT = sys.argv[1], json.load(open(sys.argv[2], encoding="utf-8")), sys.argv[3]
W, H = 1080, 1350
GREEN = (47, 74, 58); MINT = (156, 194, 166); PAPER = (247, 246, 243); INK = (29, 32, 36)
F = "/usr/share/fonts/opentype/inter/"
def f(n, s): return ImageFont.truetype(F + n, s)
H1, H2, B, S = f("InterDisplay-Bold.otf", 84), f("InterDisplay-Bold.otf", 60), f("Inter-Medium.otf", 40), f("Inter-SemiBold.otf", 30)

def cover(im):
    sc = max(W / im.width, H / im.height); im = im.resize((int(im.width * sc), int(im.height * sc)), Image.BICUBIC)
    x = (im.width - W) // 2; y = (im.height - H) // 2
    return im.crop((x, y, x + W, y + H))

def shade(fr, start=700):
    g = Image.new("L", (W, H))
    for yy in range(H): g.paste(int(230 * min(1, max(0, (yy - start) / (H - start)) * 1.4)), (0, yy, W, yy + 1))
    return Image.composite(Image.new("RGB", (W, H), (12, 16, 14)), fr, g)

def tag(d, x, y, txt):
    w = d.textlength(txt, font=S); d.rounded_rectangle((x, y, x + w + 44, y + 58), 29, fill=GREEN); d.text((x + 22, y + 11), txt, font=S, fill=(255, 255, 255))

fr = shade(cover(Image.open(f"{IMG}/{CFG['cover']}").convert("RGB"))); d = ImageDraw.Draw(fr)
tag(d, 70, 70, "АПАРТАМЕНТ НА СЕДМИЦАТА")
d.text((70, 900), CFG["title"], font=H1, fill="white")
d.text((72, 1010), CFG["sub1"], font=B, fill=MINT)
d.text((72, 1075), CFG["sub2"], font=B, fill=(230, 230, 230))
fr.save(f"{OUT}/1.jpg", quality=92)

fr = Image.new("RGB", (W, H), PAPER); d = ImageDraw.Draw(fr)
tag(d, 70, 70, CFG["plan_tag"])
p = Image.open(f"{IMG}/{CFG['plan']}").convert("RGB"); tw = 940 if p.width / p.height > 1.3 else 760
p = p.resize((tw, int(p.height * tw / p.width)), Image.BICUBIC)
fr.paste(p, ((W - tw) // 2, 230))
y = 230 + p.height + 70
d.text((70, y), CFG["plan_title"], font=H2, fill=INK)
for i, r in enumerate(CFG["plan_rows"]): d.text((72, y + 100 + i * 60), r, font=B, fill=(70, 74, 80))
fr.save(f"{OUT}/2.jpg", quality=92)

fr = Image.new("RGB", (W, H), GREEN); d = ImageDraw.Draw(fr)
d.text((70, 120), CFG["why_title"], font=H1, fill="white")
for i, t in enumerate(CFG["why"]):
    yy = 300 + i * 120
    d.ellipse((72, yy + 12, 100, yy + 40), fill=MINT); d.text((130, yy), t, font=B, fill="white")
d.line((70, 830, 230, 830), fill=MINT, width=6)
d.text((70, 880), "Запишете оглед", font=B, fill=MINT)
d.text((70, 940), "0894 611 161", font=f("InterDisplay-Bold.otf", 110), fill="white")
d.text((72, 1090), "sales@ulpia.bg · ulpia.bg", font=B, fill=MINT)
d.text((70, 1220), "ULPIA", font=H2, fill="white")
fr.save(f"{OUT}/3.jpg", quality=92)
