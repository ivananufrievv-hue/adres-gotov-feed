#!/usr/bin/env python3
"""10 тестовых вариантов инфографики «Регистрация ИП» (1200x900, формат Авито).
Запуск: python3 build.py  -> PNG/JPG рядом с папкой src."""
import os
import subprocess

HERE = os.path.dirname(os.path.abspath(__file__))
OUT = os.path.dirname(HERE)
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"

FONTS = ("https://fonts.googleapis.com/css2?family=Manrope:wght@500;600;700;800"
         "&family=Cormorant+Garamond:wght@500;600;700&family=Unbounded:wght@600;800&display=swap")

BASE = """
* { box-sizing: border-box; margin: 0; padding: 0; }
html, body { width: 1200px; height: 900px; overflow: hidden; }
body { font-family: 'Manrope', Arial, sans-serif; position: relative; }
.abs { position: absolute; }
.logo { height: 58px; border-radius: 12px; display: block; }
.partner { display: flex; align-items: center; gap: 12px; font-size: 20px; font-weight: 600; }
"""

# ---------- общие элементы ----------

def ball(x, y, d, blur=0, logo=False):
    """Глянцевый чёрный шар, как в примере 1."""
    inner = ""
    if logo:
        s = d * 0.46
        inner = (f'<div style="position:absolute;left:{(d-s)/2}px;top:{(d-s)/2}px;width:{s}px;height:{s*1.1}px;'
                 f'background:#ffdd2d;clip-path:polygon(0 0,100% 0,100% 62%,50% 100%,0 62%);'
                 f'display:flex;align-items:center;justify-content:center;font:800 {s*0.62}px Unbounded;color:#111;'
                 f'padding-bottom:{s*0.18}px">Т</div>')
    return (f'<div class="abs" style="left:{x}px;top:{y}px;width:{d}px;height:{d}px;border-radius:50%;'
            f'background:radial-gradient(circle at 32% 28%,#6a6a6a 0,#1a1a1a 22%,#050505 60%,#000 100%);'
            f'box-shadow:0 {d*0.12}px {d*0.25}px rgba(0,0,0,.35);filter:blur({blur}px)">{inner}</div>')


ICONS = {
    "doc": '<path d="M14 6h22l10 10v32a4 4 0 0 1-4 4H14a4 4 0 0 1-4-4V10a4 4 0 0 1 4-4z"/><path d="M36 6v10h10M18 26h20M18 34h20M18 42h12"/>',
    "check": '<rect x="10" y="8" width="36" height="44" rx="4"/><path d="M20 4h16v8H20zM17 24l3 3 6-6M30 24h10M17 36l3 3 6-6M30 36h10"/>',
    "badge": '<circle cx="28" cy="24" r="16"/><path d="M20 24l6 6 10-11M19 37l-5 15 8-4 4 8 2-12M37 37l5 15-8-4-4 8"/>',
    "search": '<circle cx="24" cy="24" r="13"/><path d="M34 34l12 12M18 28v-4M24 28v-8M30 28v-6"/>',
    "passport": '<rect x="12" y="6" width="32" height="44" rx="4"/><circle cx="28" cy="24" r="7"/><path d="M20 38h16M22 44h12"/>',
    "card": '<rect x="6" y="14" width="44" height="30" rx="5"/><path d="M6 22h44M12 36h12"/>',
    "key": '<rect x="18" y="4" width="20" height="34" rx="4"/><path d="M22 38v10h12V38M28 12v8"/><circle cx="28" cy="26" r="3"/>',
    "ruble": '<circle cx="28" cy="28" r="22"/><path d="M22 40V16h9a7 7 0 0 1 0 14h-13M18 35h14"/>',
    "pin": '<path d="M28 52s16-15 16-28a16 16 0 0 0-32 0c0 13 16 28 16 28z"/><circle cx="28" cy="24" r="6"/>',
    "bank": '<path d="M6 22L28 8l22 14H6zM10 22v20M20 22v20M36 22v20M46 22v20M6 46h44"/>',
    "clock": '<circle cx="28" cy="28" r="22"/><path d="M28 14v14l10 6"/>',
}


def icon(name, size=56, color="#fff", width=2.4):
    return (f'<svg width="{size}" height="{size}" viewBox="0 0 56 56" fill="none" stroke="{color}" '
            f'stroke-width="{width}" stroke-linecap="round" stroke-linejoin="round">{ICONS[name]}</svg>')


def partner(color="#1c1c1c"):
    return f'<div class="partner" style="color:{color}">Партнёр <img class="logo" src="tbiz-logo.jpg"></div>'


# ---------- 10 вариантов ----------

def v01(c, v):  # пример 1: жёлтый фон, шары, белая карточка-памятка
    balls = (ball(40, 210, 150) + ball(300, 70, 70) + ball(410, 20, 110) + ball(-60, 640, 260, blur=7)
             + ball(990, -40, 260, blur=6) + ball(1010, 640, 180) + ball(1110, 560, 60) + ball(150, 380, 70))
    return f"""<style>body{{background:radial-gradient(circle at 50% 40%,#ffe866,#ffd21f 70%,#f5c400)}}
    .card{{left:250px;top:90px;width:700px;height:720px;background:#f4f4f2;border-radius:34px;padding:56px 64px;box-shadow:0 30px 60px rgba(120,90,0,.25)}}
    h1{{font:800 46px Manrope;text-transform:uppercase;letter-spacing:.5px;margin-top:34px}}
    .lead{{font:600 26px Manrope;color:#555;margin-top:12px}}
    .row{{display:flex;gap:22px;align-items:center;margin-top:30px;font:500 25px/1.35 Manrope;color:#333}}
    .n{{font:800 70px Unbounded;color:#1a1a1a;text-shadow:0 4px 0 #777;width:70px}}
    b{{font-weight:800;color:#111}}</style>
    {balls}
    <div class="abs card">{partner()}
      <h1>Памятка: ИП за 0 ₽</h1><div class="lead">Регистрация ИП {v}</div>
      <div class="row"><div class="n">1</div><div>Присылаете <b>паспорт и СНИЛС</b> — подбираем ОКВЭД и налоговый режим</div></div>
      <div class="row"><div class="n">2</div><div>Представитель банка <b>привозит документы</b> на подпись</div></div>
      <div class="row"><div class="n">3</div><div>Через <b>3–5 рабочих дней</b> — ИП, расчётный счёт и КЭП</div></div>
    </div>"""


def v02(c, v):  # пример 1, вариант: крупный оффер, шары вокруг
    balls = ball(860, 120, 230) + ball(1080, 40, 90) + ball(760, 560, 120) + ball(980, 500, 300, blur=5) + ball(-80, 720, 220, blur=6)
    return f"""<style>body{{background:linear-gradient(135deg,#ffe766,#ffcf10)}}
    h1{{font:800 108px/0.95 Unbounded;color:#111;letter-spacing:-2px}}
    .tag{{display:inline-block;background:#111;color:#ffdd2d;font:800 30px Manrope;padding:12px 24px;border-radius:40px}}
    .chip{{background:#fff;border-radius:22px;padding:18px 26px;font:700 28px Manrope;color:#111}}</style>
    {balls}
    <div class="abs" style="left:80px;top:70px">{partner()}</div>
    <div class="abs" style="left:80px;top:220px"><div class="tag">{c}</div>
      <h1 style="margin-top:30px">ИП<br>за 0 ₽</h1>
      <div style="font:600 34px Manrope;margin-top:26px;color:#2b2b2b">Регистрация + расчётный счёт + КЭП</div></div>
    <div class="abs" style="left:80px;bottom:70px;display:flex;gap:16px">
      <div class="chip">Без госпошлины</div><div class="chip">3–5 рабочих дней</div><div class="chip">Без визита в ФНС</div></div>"""


def tech_bg(extra=""):
    dots = "".join(
        f'<div class="abs" style="left:{x}px;top:{y}px;width:{s}px;height:{s}px;border-radius:50%;background:#ffb547;box-shadow:0 0 {s*4}px {s*1.5}px rgba(255,170,60,.7)"></div>'
        for x, y, s in [(520, 330, 5), (560, 380, 3), (600, 300, 4), (640, 420, 3), (690, 350, 5), (470, 440, 3), (720, 470, 4), (580, 500, 2), (760, 300, 3), (430, 360, 2)])
    return f"""<style>body{{background:radial-gradient(ellipse at 70% 60%,#5a3d22 0,#2a1d12 45%,#120c08 100%);color:#fff}}
    .br{{position:absolute;width:44px;height:44px;border-color:rgba(255,255,255,.85);border-style:solid}}</style>{dots}{extra}"""


def frame(x, y, w, h):
    return (f'<div class="br" style="left:{x}px;top:{y}px;border-width:2px 0 0 2px"></div>'
            f'<div class="br" style="left:{x+w-44}px;top:{y}px;border-width:2px 2px 0 0"></div>'
            f'<div class="br" style="left:{x}px;top:{y+h-44}px;border-width:0 0 2px 2px"></div>'
            f'<div class="br" style="left:{x+w-44}px;top:{y+h-44}px;border-width:0 2px 2px 0"></div>')


def v03(c, v):  # пример 2: тёмный «технологичный», иконки в рамках
    return tech_bg() + f"""
    <div class="abs" style="left:70px;top:60px">{partner('#fff')}</div>
    <div class="abs" style="left:70px;top:150px;font:700 24px Manrope;color:#ffc46b;letter-spacing:3px">{c.upper()}</div>
    <div class="abs" style="left:70px;top:195px;font:800 70px/1.02 Manrope">Регистрация ИП<br><span style="color:#ffc46b">онлайн-подача, 0 ₽</span></div>
    {frame(70, 430, 300, 300)}{frame(450, 430, 300, 300)}{frame(830, 430, 300, 300)}
    <div class="abs" style="left:70px;top:470px;width:300px;text-align:center">{icon('passport',110)}<div style="font:700 26px Manrope;margin-top:24px">Паспорт<br>и СНИЛС</div></div>
    <div class="abs" style="left:450px;top:470px;width:300px;text-align:center">{icon('check',110)}<div style="font:700 26px Manrope;margin-top:24px">Документы<br>готовим мы</div></div>
    <div class="abs" style="left:830px;top:470px;width:300px;text-align:center">{icon('badge',110)}<div style="font:700 26px Manrope;margin-top:24px">ИП за 3–5<br>рабочих дней</div></div>"""


def v04(c, v):  # пример 2: большой значок-печать по центру
    return tech_bg() + f"""
    <div class="abs" style="left:70px;top:60px">{partner('#fff')}</div>
    {frame(640, 180, 480, 520)}
    <div class="abs" style="left:700px;top:230px">{icon('badge',360,'#fff',1.6)}</div>
    <div class="abs" style="left:70px;top:230px;width:540px">
      <div style="font:600 26px Manrope;color:#ffc46b;letter-spacing:3px">{c.upper()}</div>
      <div style="font:800 64px/1.05 Manrope;margin-top:16px">Своё дело —<br>через 3–5 дней</div>
      <div style="font:500 28px/1.4 Manrope;margin-top:28px;color:#e8dccd">Выписка ЕГРИП на почту через 3–5 рабочих дней. Без визита в налоговую.</div>
      <div style="margin-top:40px;display:inline-block;border:2px solid #ffc46b;color:#ffc46b;font:800 30px Manrope;padding:14px 28px;border-radius:14px">Бесплатно · 0 ₽</div>
    </div>"""


def v05(c, v):  # пример 3: приглушённый зелёный/бежевый, «плоское 3D»
    return f"""<style>body{{background:#e9e3d8;color:#24372d}}
    .sh{{box-shadow:0 18px 30px rgba(60,50,30,.18)}}</style>
    <div class="abs" style="left:640px;top:120px;width:500px;height:500px;border-radius:50%;background:#2f4a3c"></div>
    <div class="abs sh" style="left:720px;top:540px;width:360px;height:120px;border-radius:50%;background:#d8cfbf"></div>
    <div class="abs sh" style="left:720px;top:600px;width:360px;height:120px;border-radius:0 0 50% 50%/0 0 60px 60px;background:#cbc1af"></div>
    <div class="abs" style="left:770px;top:300px;font:800 190px Unbounded;color:#f3ede2;text-shadow:0 14px 30px rgba(0,0,0,.25)">0₽</div>
    <svg class="abs" style="left:640px;top:70px" width="460" height="260"><path d="M10 240 L150 150 L220 200 L400 40" fill="none" stroke="#f3ede2" stroke-width="34" stroke-linejoin="miter"/><path d="M350 20 L440 20 L430 110 Z" fill="#f3ede2"/></svg>
    <div class="abs" style="left:1050px;top:640px;width:46px;height:46px;border-radius:50%;background:#1b1b1b"></div>
    <div class="abs" style="left:620px;top:90px;width:34px;height:34px;border-radius:50%;background:#2f4a3c"></div>
    <div class="abs" style="left:70px;top:70px">{partner('#24372d')}</div>
    <div class="abs" style="left:70px;top:210px;width:560px">
      <div style="font:700 26px Manrope;letter-spacing:2px;color:#6d7f72">{c.upper()}</div>
      <div style="font:800 76px/1.02 Manrope;margin-top:14px">Регистрация ИП без затрат</div>
      <div style="font:500 28px/1.4 Manrope;margin-top:24px;color:#4a5a50">ИП, расчётный счёт и электронная подпись — бесплатно для вас.</div>
    </div>
    <div class="abs" style="left:70px;bottom:80px;display:flex;gap:14px">
      <div style="background:#2f4a3c;color:#f3ede2;font:700 26px Manrope;padding:16px 24px;border-radius:18px">3–5 рабочих дней</div>
      <div style="background:#f3ede2;font:700 26px Manrope;padding:16px 24px;border-radius:18px">Без госпошлины</div></div>"""


def v06(c, v):  # пример 3: плитки «что вы получаете»
    tiles = [("bank", "ИП в ЕГРИП", "выписка на почту"), ("card", "Расчётный счёт", "открытие 0 ₽"),
             ("key", "КЭП", "с доставкой"), ("search", "ОКВЭД и налоги", "подбор под бизнес")]
    t = "".join(f"""<div style="background:{'#2f4a3c' if i % 3 == 0 else '#f3ede2'};color:{'#f3ede2' if i % 3 == 0 else '#24372d'};
        border-radius:28px;padding:30px;box-shadow:0 16px 30px rgba(60,50,30,.15)">
        {icon(n, 64, '#f3ede2' if i % 3 == 0 else '#2f4a3c', 2.6)}
        <div style="font:800 32px Manrope;margin-top:18px">{a}</div><div style="font:500 24px Manrope;opacity:.8;margin-top:6px">{b}</div></div>"""
                for i, (n, a, b) in enumerate(tiles))
    return f"""<style>body{{background:#e9e3d8;color:#24372d}}</style>
    <div class="abs" style="left:-120px;top:520px;width:420px;height:420px;border-radius:50%;background:#d8cfbf"></div>
    <div class="abs" style="left:70px;top:60px">{partner('#24372d')}</div>
    <div class="abs" style="right:70px;top:70px;background:#2f4a3c;color:#f3ede2;font:700 26px Manrope;padding:12px 24px;border-radius:30px">{c}</div>
    <div class="abs" style="left:70px;top:170px;font:800 62px Manrope">Что вы получаете <span style="color:#8a9a8f">— бесплатно</span></div>
    <div class="abs" style="left:70px;top:290px;width:1060px;display:grid;grid-template-columns:1fr 1fr;gap:24px">{t}</div>"""


def lux_css():
    return """<style>body{background:radial-gradient(ellipse at 75% 40%,#2b2117 0,#141010 55%,#0b0909 100%);color:#e9d6a8}
    .serif{font-family:'Cormorant Garamond',serif;font-weight:600;letter-spacing:2px}
    .box{border:1px solid rgba(233,214,168,.45);padding:14px 22px;font:500 22px Manrope;color:#d9c9a3;letter-spacing:1px}
    .gold{background:linear-gradient(180deg,#f6e3b0,#c89b4c);-webkit-background-clip:text;color:transparent}</style>"""


def v07(c, v):  # пример 4: «люкс» — тёмный фон, золото, антиква
    lines = "".join(f'<div class="abs" style="left:{x}px;top:0;width:1px;height:900px;background:rgba(233,214,168,.08)"></div>' for x in (600, 640))
    return lux_css() + lines + f"""
    <div class="abs" style="left:700px;top:120px;width:420px;height:640px;border:1px solid rgba(233,214,168,.35)"></div>
    <div class="abs" style="left:740px;top:170px;width:340px;text-align:center">{icon('doc',200,'#d8b36a',1.4)}
      <div class="serif gold" style="font-size:44px;margin-top:30px">ЕГРИП</div>
      <div style="font:500 22px Manrope;color:#bba982;margin-top:8px">лист записи — на вашу почту</div>
      <div class="serif" style="font-size:110px;margin-top:20px"><span class="gold">3–5</span></div>
      <div style="font:500 22px Manrope;color:#bba982">рабочих дней</div></div>
    <div class="abs" style="left:80px;top:80px">{partner('#d9c9a3')}</div>
    <div class="abs serif gold" style="left:80px;top:220px;font-size:78px;line-height:1">РЕГИСТРАЦИЯ<br>ИП</div>
    <div class="abs box" style="left:80px;top:460px">Бесплатно · без госпошлины · без визита в ФНС</div>
    <div class="abs serif" style="left:80px;top:585px;font-size:50px;line-height:1.05;color:#efe3c6">{c.upper()}</div>
    <div class="abs box" style="left:80px;top:690px;font-size:18px">ИП · РАСЧЁТНЫЙ СЧЁТ · КЭП</div>"""


def v08(c, v):  # пример 4: три «без» крупной антиквой
    rows = "".join(f"""<div style="display:flex;align-items:baseline;gap:30px;border-bottom:1px solid rgba(233,214,168,.25);padding:26px 0">
        <div class="serif gold" style="font-size:40px;width:90px">0{i}</div><div class="serif" style="font-size:66px;color:#efe3c6">{t}</div></div>"""
                   for i, t in enumerate(["Без госпошлины", "Без визита в ФНС", "Без доплат"], 1))
    return lux_css() + f"""
    <div class="abs" style="left:80px;top:70px;right:80px;display:flex;justify-content:space-between;align-items:center">
      <div class="serif gold" style="font-size:40px">{c.upper()}</div>{partner('#d9c9a3')}</div>
    <div class="abs" style="left:80px;top:190px;width:1040px">{rows}</div>
    <div class="abs" style="left:80px;bottom:70px;font:600 30px Manrope;color:#d9c9a3">Регистрация ИП — <span class="gold" style="font-weight:800">0 ₽</span>. От вас — только подпись.</div>"""


def map_svg(dark=False, dy=0):
    """Стилизованная «сеть» городов: точки + линии, как в примере 5."""
    pts = [(130, 520), (260, 430), (330, 600), (420, 500), (520, 380), (600, 560), (690, 450), (790, 520),
           (880, 400), (960, 560), (1060, 470), (1140, 610), (470, 700), (760, 690), (240, 720), (1000, 720)]
    edges = [(0, 1), (1, 3), (0, 2), (2, 3), (3, 4), (3, 5), (4, 6), (5, 6), (6, 7), (7, 8), (7, 9), (8, 10), (9, 10),
             (10, 11), (2, 12), (5, 12), (12, 13), (7, 13), (2, 14), (13, 15), (9, 15), (11, 15)]
    land = "#2f3644" if not dark else "#262b36"
    lines = "".join(f'<line x1="{pts[a][0]}" y1="{pts[a][1]}" x2="{pts[b][0]}" y2="{pts[b][1]}" stroke="#f2a65a" stroke-width="1.6" opacity=".85"/>' for a, b in edges)
    dots = "".join(f'<circle cx="{x}" cy="{y}" r="4" fill="#ffd08a"/><circle cx="{x}" cy="{y}" r="12" fill="#f2a65a" opacity=".25"/>' for x, y in pts)
    blobs = ('<path d="M60 560 Q160 420 330 460 T620 420 T900 380 T1180 470 L1200 900 L0 900 Z" fill="%s" opacity="%s"/>'
             % (land, ".9" if not dark else "1"))
    return f'<svg class="abs" style="left:0;top:{dy}px" width="1200" height="900">{blobs}{lines}{dots}</svg>'


def pin(x, y, s=1.0, label=""):
    w, h = 90 * s, 120 * s
    lab = (f'<div style="position:absolute;left:{w+14}px;top:{18*s}px;white-space:nowrap;background:#1f2430;color:#fff;'
           f'font:800 {26*s}px Manrope;padding:{8*s}px {16*s}px;border-radius:{12*s}px">{label}</div>') if label else ""
    return (f'<div class="abs" style="left:{x}px;top:{y}px;width:{w}px;height:{h}px">'
            f'<div style="position:absolute;left:0;top:0;width:{w}px;height:{w}px;border-radius:50% 50% 50% 0;transform:rotate(-45deg);'
            f'background:linear-gradient(135deg,#3a4150,#1b1f28);box-shadow:0 10px 20px rgba(0,0,0,.35)"></div>'
            f'<div style="position:absolute;left:{w*0.25}px;top:{w*0.25}px;width:{w*0.5}px;height:{w*0.5}px;border-radius:50%;'
            f'border:{6*s}px solid #ffb35c;box-shadow:0 0 {24*s}px #ff9d3c;background:#e9edf2"></div>{lab}</div>')


def v09(c, v):  # пример 5: карта с метками, светлая
    return f"""<style>body{{background:linear-gradient(180deg,#eef1f4,#dfe4ea);color:#1f2430}}</style>
    {map_svg(dy=110)}{pin(230, 450, .8)}{pin(480, 390, 1.15, c)}{pin(860, 410, .8)}{pin(1040, 480, .7)}{pin(640, 560, .7)}
    <div class="abs" style="left:70px;top:60px;right:70px;display:flex;justify-content:space-between;align-items:center">
      <div style="font:800 30px Manrope">Адрес Готов</div>{partner('#1f2430')}</div>
    <div class="abs" style="left:70px;top:150px;font:800 66px/1.02 Manrope">Регистрация ИП<br>по всей России — <span style="color:#e2852f">0 ₽</span></div>"""


def v10(c, v):  # пример 5: тёмная карта, акцент на городе
    return f"""<style>body{{background:radial-gradient(ellipse at 60% 70%,#2a3140,#11141b 70%);color:#fff}}</style>
    {map_svg(dark=True, dy=170)}{pin(700, 330, 1.3, c)}{pin(250, 600, .6)}{pin(560, 640, .6)}{pin(1000, 620, .5)}
    <div class="abs" style="left:70px;top:60px">{partner('#fff')}</div>
    <div class="abs" style="left:70px;top:160px;width:600px">
      <div style="font:800 56px/1.04 Manrope">Представитель банка<br>приедет к вам</div>
      <div style="font:500 26px/1.4 Manrope;color:#c7cedb;margin-top:20px">Подпишите документы в удобном месте — ИП, счёт и КЭП без визита в налоговую. Бесплатно.</div></div>"""


def page_html(body):
    return (f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="{FONTS}">'
            f'<style>{BASE}</style></head><body>{body}</body></html>')


DEMO = {"01": ("Москва", "в Москве"), "02": ("Санкт-Петербург", "в Санкт-Петербурге"), "03": ("Самара", "в Самаре"),
        "04": ("Новосибирск", "в Новосибирске"), "05": ("Екатеринбург", "в Екатеринбурге"), "06": ("Пермь", "в Перми"),
        "07": ("Казань", "в Казани"), "08": ("Нижний Новгород", "в Нижнем Новгороде"), "09": ("Самара", "в Самаре"),
        "10": ("Ростов-на-Дону", "в Ростове-на-Дону")}

VARIANTS = [v01, v02, v03, v04, v05, v06, v07, v08, v09, v10]
NAMES = ["01-жёлтый-шары-памятка", "02-жёлтый-шары-оффер", "03-тёмный-иконки-в-рамках", "04-тёмный-печать",
         "05-зелёный-плоское-3D", "06-зелёный-плитки", "07-люкс-золото-ЕГРИП", "08-люкс-три-без",
         "09-карта-светлая", "10-карта-тёмная"]


def main():
    for fn, name in zip(VARIANTS, NAMES):
        page = os.path.join(HERE, f"_{name}.html")
        with open(page, "w", encoding="utf-8") as fh:
            fh.write(page_html(fn(*DEMO[name[:2]])))
        png = os.path.join(HERE, f"_{name}.png")
        subprocess.run([CHROME, "--headless=new", "--hide-scrollbars", "--window-size=1200,900",
                        "--virtual-time-budget=8000", f"--screenshot={png}", "file://" + page],
                       check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "90", png,
                        "--out", os.path.join(OUT, name + ".jpg")], check=True, stdout=subprocess.DEVNULL)
        os.remove(png)
        print("ok", name)


if __name__ == "__main__":
    main()
