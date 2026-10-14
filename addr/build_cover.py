#!/usr/bin/env python3
"""
Обложки объявлений по юр. адресам: фото помещения + инфографика.

Слева цветная панель (заголовок, три тезиса, кнопка), справа фото помещения
с плашкой адреса. 6 палитр по мотивам шаблонов Юрмаркета чередуются по объявлениям.

    python3 addr/build_cover.py --test <папка>   # по одному объявлению на палитру
    python3 addr/build_cover.py                  # все объявления -> images/<NN>/cover-<VER>.jpg,
                                                 # в feed.xml обложка встаёт вместо первого фото
"""
import os
import re
import subprocess
import sys
import tempfile
import xml.etree.ElementTree as ET

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
VER = "v1"
FONTS = "https://fonts.googleapis.com/css2?family=Montserrat:wght@800;900&family=Manrope:wght@600;700;800&display=swap"

# bg панели, заголовок, акцент заголовка, плитка иконки, цвет иконки, фон тезиса, текст тезиса, кнопка, текст кнопки
PALETTES = {
    "green":  ("linear-gradient(160deg,#0f5a28,#073217)", "#fff", "#7cf06a", "linear-gradient(135deg,#5be05a,#22a53a)", "#fff", "rgba(255,255,255,.08)", "#fff", "#7cf06a", "#06301a"),
    "red":    ("linear-gradient(160deg,#ec1c24,#b5040b)", "#fff", "#fff", "#fff", "#d10a12", "#fff", "#b0060c", "#fff", "#c8070f"),
    "blue":   ("linear-gradient(160deg,#1f56f0,#0a2fb0)", "#fff", "#b9f53a", "#b9f53a", "#0b2a8f", "rgba(255,255,255,0)", "#fff", "#b9f53a", "#0b2a8f"),
    "white":  ("linear-gradient(160deg,#ffffff,#f1f1f1)", "#151515", "#e3000f", "#e3000f", "#fff", "#f2f2f2", "#1d1d1d", "#e3000f", "#fff"),
    "redgreen": ("linear-gradient(160deg,#ffffff,#f4f4f4)", "#e30613", "#e30613", "#fff", "#1c9c39", "linear-gradient(135deg,#25b145,#178a31)", "#fff", "#e30613", "#fff"),
    "yellow": ("linear-gradient(160deg,#ffe600,#ffd400)", "#111", "#111", "#fff", "#111", "rgba(255,255,255,0)", "#111", "#111", "#fff"),
}
ORDER = ["green", "red", "blue", "yellow", "white", "redgreen"]

ICONS = {
    "ruble": '<circle cx="28" cy="28" r="21"/><path d="M23 40V16h8a7 7 0 0 1 0 14H18M18 35h13"/>',
    "bank": '<path d="M7 22L28 9l21 13H7zM12 22v18M22 22v18M34 22v18M44 22v18M7 45h42"/>',
    "shield": '<path d="M28 6l18 7v13c0 12-8 20-18 24C18 46 10 38 10 26V13z"/><path d="M20 28l6 6 11-12"/>',
    "pin": '<path d="M28 52s16-15 16-28a16 16 0 0 0-32 0c0 13 16 28 16 28z"/><circle cx="28" cy="24" r="6"/>',
}

THESES = [("ruble", "Оплата после<br>регистрации"), ("bank", "Согласование<br>с налоговой"), ("shield", "Не зарегистрировали —<br>не платите")]


def icon(name, color, size=50):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 56 56" fill="none" stroke="{color}" stroke-width="3.6" '
            f'stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>')


def html(photo_url, street, ifns, pal):
    bg, h, hacc, tile, ic, pill, ptxt, cta, ctatxt = PALETTES[pal]
    rows = "".join(f'<div class="row" style="background:{pill};color:{ptxt}"><div class="tile" style="background:{tile}">{icon(n, ic)}</div><div>{t}</div></div>'
                   for n, t in THESES)
    border = "border:2px solid rgba(0,0,0,.06);" if pal in ("white", "redgreen", "yellow") else ""
    chip_ifns = f'<span style="opacity:.55;margin:0 10px">·</span>{int(ifns)} ИФНС' if ifns else ""
    return f"""<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="{FONTS}"><style>
* {{ box-sizing:border-box; margin:0; padding:0 }}
html,body {{ width:1200px; height:900px; overflow:hidden }}
body {{ position:relative; font-family:'Manrope',Arial,sans-serif; background:#000 }}
.photo {{ position:absolute; left:470px; top:0; width:730px; height:900px; background:url('{photo_url}') center/cover }}
.panel {{ position:absolute; left:0; top:0; width:640px; height:900px; background:{bg};
  clip-path:polygon(0 0,100% 0,78% 100%,0 100%); }}
.in {{ position:absolute; left:52px; top:46px; width:520px }}
.brand {{ font:900 26px Montserrat; letter-spacing:3px; color:{h} }}
.brand b {{ color:{hacc} }}
h1 {{ margin-top:22px; font:900 63px/1 Montserrat; color:{h}; letter-spacing:-1.5px; text-transform:uppercase }}
h1 span {{ color:{hacc} }}
.row {{ display:flex; align-items:center; gap:18px; margin-top:20px; padding:14px 20px 14px 14px; border-radius:26px; width:470px;
  font:800 27px/1.15 Manrope; {border} }}
.tile {{ width:82px; height:82px; border-radius:22px; display:flex; align-items:center; justify-content:center; flex:none;
  box-shadow:0 6px 14px rgba(0,0,0,.18) }}
.cta {{ position:absolute; left:52px; bottom:46px; display:flex; align-items:center; gap:18px; background:{cta}; color:{ctatxt};
  font:900 36px Montserrat; padding:20px 26px 20px 34px; border-radius:60px; box-shadow:0 10px 24px rgba(0,0,0,.25) }}
.arrow {{ width:52px; height:52px; border-radius:50%; background:{ctatxt}; color:{cta}; display:flex; align-items:center; justify-content:center; font:900 30px Manrope }}
.chip {{ position:absolute; right:34px; bottom:40px; display:flex; align-items:center; gap:10px; background:rgba(255,255,255,.94); color:#151515;
  font:800 26px Manrope; padding:14px 22px 14px 16px; border-radius:20px; box-shadow:0 10px 30px rgba(0,0,0,.35) }}
</style></head><body>
<div class="photo"></div>
<div class="panel"></div>
<div class="in">
  <div class="brand">АДРЕС <b>ГОТОВ</b></div>
  <h1>Юридический<br><span>адрес</span></h1>
  <div style="margin-top:34px">{rows}</div>
</div>
<div class="cta">Напишите нам <div class="arrow">→</div></div>
<div class="chip">{icon('pin', '#e3000f', 34)}{street}{chip_ifns}</div>
</body></html>"""


def short_street(address):
    """«Москва, ул. Кржижановского, д. 29, к. 5, пом. …» -> «ул. Кржижановского, 29»"""
    parts = [p.strip() for p in address.split(",")]
    parts = [p for p in parts if p and p != "Москва" and not p.startswith(("пом.", "этаж"))]
    street = next((p for p in parts if not p.startswith(("д.", "к.", "стр.", "пос.")) and not re.match(r"^\d", p)), parts[0])
    house = next((p for p in parts if p.startswith("д.") or re.match(r"^\d", p)), "")
    house = house.replace("д. ", "").replace("д.", "")
    return f"{street}, {house}" if house else street


def ads():
    out = []
    for a in ET.parse(os.path.join(ROOT, "feed.xml")).getroot():
        ad_id = a.find("Id").text
        if ad_id.startswith("AGIP"):
            continue
        imgs = a.find("Images")
        photo = [i.get("url") for i in imgs if "/cover-" not in i.get("url")][0]
        m = re.search(r"юридический адрес (\d+) ИФНС", a.find("Description").text)
        out.append((ad_id, photo, short_street(a.find("Address").text), m.group(1) if m else None))
    return out


def local(url):
    return os.path.join(ROOT, url.split("/adres-gotov-feed/")[1])


def render(photo_url, street, ifns, pal, out_jpg):
    with tempfile.NamedTemporaryFile("w", suffix=".html", dir=os.path.dirname(local(photo_url)), delete=False, encoding="utf-8") as fh:
        fh.write(html(os.path.basename(local(photo_url)), street, ifns, pal))
        page = fh.name
    png = page[:-5] + ".png"
    try:
        subprocess.run([CHROME, "--headless=new", "--hide-scrollbars", "--window-size=1200,900", "--virtual-time-budget=8000",
                        f"--screenshot={png}", "file://" + page], check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "88", png, "--out", out_jpg],
                       check=True, stdout=subprocess.DEVNULL)
    finally:
        for p in (page, png):
            if os.path.exists(p):
                os.remove(p)


def main():
    items = ads()
    if "--test" in sys.argv:
        out_dir = sys.argv[sys.argv.index("--test") + 1]
        os.makedirs(out_dir, exist_ok=True)
        for k, pal in enumerate(ORDER):
            ad_id, photo, street, ifns = items[k * 4]
            render(photo, street, ifns, pal, os.path.join(out_dir, f"{k + 1:02}-{pal}-{ad_id}.jpg"))
            print("ok", pal, ad_id, street, ifns)
        return
    feed_path = os.path.join(ROOT, "feed.xml")
    feed = open(feed_path, encoding="utf-8").read()
    for k, (ad_id, photo, street, ifns) in enumerate(items):
        num = ad_id.split("-")[1]
        render(photo, street, ifns, ORDER[k % len(ORDER)], os.path.join(ROOT, "images", num, f"cover-{VER}.jpg"))
        # обложка заменяет первое фото: фото помещения уже есть на обложке
        cover = f"{photo.rsplit('/', 1)[0]}/cover-{VER}.jpg"
        block = re.search(rf"<Ad>\s*<Id>{re.escape(ad_id)}</Id>.*?</Ad>", feed, re.S)
        old_block = block.group(0)
        new_block = re.sub(r'<Image url="[^"]+"/>', f'<Image url="{cover}"/>', old_block, count=1)
        feed = feed.replace(old_block, new_block)
        print("ok", ORDER[k % len(ORDER)], ad_id, street, ifns)
    open(feed_path, "w", encoding="utf-8").write(feed)


if __name__ == "__main__":
    main()
