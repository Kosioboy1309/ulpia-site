"""Общ стандарт за всички публикации на Улпия (по оригиналната визия „Паркомясто −50%“ и сайта ulpia.bg).

Всеки кадър е 1080x1350 и има три части:
  1. горе – снимка (0 … panel_top) с надпис УЛПИЯ (Forum, разредени букви) и ред „НОВИ АПАРТАМЕНТИ · КОМАТЕВО · ПЛОВДИВ“;
  2. средата – светъл панел (#f7f6f3) със заоблен горен ръб, който влиза върху снимката: малък етикет с чертичка, голямо заглавие във Forum
     в тъмнозелено, текст във Manrope, бутон-контур; отдясно по желание картинка;
  3. долу – зелена лента (#2f4a3a) от y=1200: „РАЗГЛЕДАЙТЕ СВОБОДНИТЕ АПАРТАМЕНТИ“, ulpia.bg (Forum) и бял бутон с телефона.
Шрифтовете се вземат от site/fonts (woff2 → временни .ttf; нужни: pillow, fonttools, brotli). Без цени.
"""
import os, glob, tempfile
from PIL import Image, ImageDraw, ImageFont, ImageOps
from fontTools.ttLib import TTFont

W, H = 1080, 1350
PAPER = (247, 246, 243); GREEN = (47, 74, 58); INK = (29, 32, 36); MUTED = (86, 90, 97); MINT = (156, 194, 166); LINE = (68, 72, 78)
BAND_Y = 1200
PHONE = "0894 611 161"
_TMP = None; _c = {}

def setup(fonts_dir):
    global _TMP
    _TMP = tempfile.mkdtemp()
    for p in glob.glob(os.path.join(fonts_dir, "*.woff2")):
        t = TTFont(p); t.flavor = None; t.save(os.path.join(_TMP, os.path.basename(p).replace(".woff2", ".ttf")))

def font(kind, w, size):
    k = (kind, w, size)
    if k not in _c:
        name = "forum-%s-400-normal" if kind == "forum" else "manrope-%s-" + str(w) + "-normal"
        _c[k] = {}
        for s in ("latin", "cyrillic"):
            fp = os.path.join(_TMP, (name % s) + ".ttf"); _c[k][s] = (ImageFont.truetype(fp, size), set(TTFont(fp).getBestCmap()))
    return _c[k]

def _pick(fs, ch): return fs["cyrillic"][0] if ord(ch) > 127 and ord(ch) in fs["cyrillic"][1] else fs["latin"][0]

def width(text, kind, w, size, track=0):
    fs = font(kind, w, size); return sum(_pick(fs, c).getlength(c) + track * size for c in text) - track * size

def T(d, x, y, text, kind, size, fill, w=500, track=0, anchor="l", up=False):
    """текст със смесена кирилица/латиница и разредка (track в em); anchor l|c|r; връща ширината"""
    if up: text = text.upper()
    fs = font(kind, w, size); tw = width(text, kind, w, size, track)
    x = x - tw / 2 if anchor == "c" else x - tw if anchor == "r" else x
    for ch in text:
        f = _pick(fs, ch); d.text((x, y), ch, font=f, fill=fill); x += f.getlength(ch) + track * size
    return tw

def wrap(text, kind, w, size, maxw, track=0):
    lines, cur = [], ""
    for word in text.split():
        t = (cur + " " + word).strip()
        if width(t, kind, w, size, track) <= maxw: cur = t
        else: lines.append(cur); cur = word
    return lines + [cur]

def opn(path): return ImageOps.exif_transpose(Image.open(path)).convert("RGB")

def fit(im, w, h, focus=(0.5, 0.5)):
    """запълва w×h, като реже излишното (focus – коя част да остане: 0…1 по x и y)"""
    sc = max(w / im.width, h / im.height); im = im.resize((int(im.width * sc) + 1, int(im.height * sc) + 1), Image.LANCZOS)
    x = int((im.width - w) * focus[0]); y = int((im.height - h) * focus[1]); return im.crop((x, y, x + w, y + h))

def box(im, bx, by, bw, w, h):
    """кадър от оригинала: [x, y, ширина], височината следва пропорцията w:h"""
    return im.crop((bx, by, bx + bw, by + int(bw * h / w))).resize((w, h), Image.LANCZOS)

def pill(d, x, y, txt, size=22, outline=GREEN, fill=None, col=None, pad=26, h=None, w=600, anchor="l"):
    tw = width(txt, "manrope", w, size); h = h or int(size * 2.2); bw = tw + 2 * pad
    if anchor == "r": x = x - bw
    d.rounded_rectangle((x, y, x + bw, y + h), h // 2, fill=fill, outline=None if fill else outline, width=2)
    T(d, x + pad, y + (h - size) / 2 - size * 0.12, txt, "manrope", size, col or (outline if not fill else "white"), w=w); return bw

def label(d, x, y, text, col=GREEN):
    """малък етикет с чертичка: — ЕКСКЛУЗИВНО ПРЕДЛОЖЕНИЕ"""
    d.line((x, y + 11, x + 42, y + 11), fill=col, width=2); T(d, x + 60, y, text, "manrope", 19, col, w=600, track=0.3, up=True)

def page(photo, panel_top=560, caption="Нови апартаменти · Коматево · Пловдив", shade=0.6):
    """основа на кадъра: снимка горе + панел със заоблен ръб; връща (картинка, d). photo е вече 1080×panel_top+60"""
    fr = Image.new("RGB", (W, H), PAPER); ph = photo.resize((W, photo.height)) if photo.width != W else photo
    g = Image.new("L", ph.size)
    for y in range(ph.height):
        a = shade * max(0, 1 - y / (ph.height * 0.42)); g.paste(int(255 * a), (0, y, W, y + 1))
    ph = Image.composite(Image.new("RGB", ph.size, (20, 22, 30)), ph, g); fr.paste(ph, (0, 0))
    d = ImageDraw.Draw(fr)
    d.rounded_rectangle((0, panel_top, W, BAND_Y + 80), 52, fill=PAPER)
    T(d, W // 2, 52, "УЛПИЯ", "forum", 76, "white", track=0.12, anchor="c")
    T(d, W // 2, 140, caption, "manrope", 17, (236, 236, 236), w=500, track=0.34, anchor="c", up=True)
    return fr, d

def band(d, text="Разгледайте свободните апартаменти", url="ulpia.bg", phone=PHONE):
    d.rectangle((0, BAND_Y, W, H), fill=GREEN)
    T(d, 72, BAND_Y + 34, text, "manrope", 17, (222, 232, 225), w=600, track=0.24, up=True)
    T(d, 72, BAND_Y + 62, url, "forum", 58, "white")
    pill(d, W - 72, BAND_Y + 40, phone, size=22, fill=PAPER, col=INK, h=70, pad=34, anchor="r")
