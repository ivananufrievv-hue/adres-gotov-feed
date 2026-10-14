#!/usr/bin/env python3
"""
Серия объявлений «Регистрация ИП» для фида Адрес Готов.

Для каждого города: своя инфографика (3 картинки с названием города) и свой
текст из сменных блоков. Все города сразу пишутся в feed.xml с разной
DateBegin — Авито сам выпускает по PER_DAY городов в день.

Запуск из корня репозитория:
    python3 ip/build_ip.py            # картинки + feed.xml
    python3 ip/build_ip.py --no-img   # только feed.xml

Блоки AGIP-* в feed.xml перезаписываются целиком, остальные объявления не трогаются.
"""
import datetime as dt
import html
import os
import re
import subprocess
import sys
import tempfile
from xml.sax.saxutils import escape

sys.path.insert(0, os.path.dirname(__file__))
from cities import CITIES, PER_DAY, START_DATE  # noqa: E402
from texts import build  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_URL = "https://ivananufrievv-hue.github.io/adres-gotov-feed"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PHONE = "+7 999 666-51-06"
IMG_VERSION = "v1"  # при замене картинок менять: Авито кеширует по URL

LOGO = '<div class="partner">Партнёр <img src="tbiz-logo.jpg"></div>'


def variants(city, city_in):
    top = f'<div class="top"><div class="brand">Адрес Готов</div>{LOGO}</div>'
    hero = f"""<div class="card">{top}
      <div class="city">{city}</div>
      <h1>Регистрация ИП<br><em>бесплатно</em></h1>
      <div class="sub">ИП + расчётный счёт + КЭП с доставкой</div>
      <div class="pills"><div class="pill">0 ₽</div><div class="pill">3–5 рабочих дней</div><div class="pill">Без госпошлины</div></div>
    </div>"""
    steps = f"""<div class="card">{top}
      <div class="city">{city}</div>
      <h1 class="big" style="margin-top:22px">Как это работает</h1>
      <div class="steps">
        <div class="step"><b>1</b>Присылаете паспорт и СНИЛС</div>
        <div class="step"><b>2</b>Подбираем ОКВЭД и налоговый режим</div>
        <div class="step"><b>3</b>Представитель банка привозит документы на подпись</div>
        <div class="step"><b>4</b>Через 3–5 рабочих дней — выписка ЕГРИП</div>
      </div>
    </div>"""
    docs = f"""<div class="card">{top}
      <div class="city">{city}</div>
      <h1>Нужны только<br><em>паспорт и СНИЛС</em></h1>
      <div class="sub">Не нужно ехать в налоговую — документы<br>привезут на подпись {html.escape(city_in)}</div>
      <div class="pills"><div class="pill">Счёт в Т-Банке — бесплатно</div><div class="pill">КЭП с доставкой</div></div>
    </div>"""
    return [hero, steps, docs]


def render_images(slug, city, city_in):
    tpl = open(os.path.join(ROOT, "ip", "card.html"), encoding="utf-8").read()
    out_dir = os.path.join(ROOT, "images", "ip", slug)
    os.makedirs(out_dir, exist_ok=True)
    for n, body in enumerate(variants(city, city_in), 1):
        with tempfile.NamedTemporaryFile("w", suffix=".html", dir=os.path.join(ROOT, "ip"), delete=False, encoding="utf-8") as fh:
            fh.write(tpl.replace("<!--VARIANT-->", body))
            page = fh.name
        png = page[:-5] + ".png"
        try:
            subprocess.run([CHROME, "--headless=new", "--hide-scrollbars", "--window-size=1200,900",
                            "--virtual-time-budget=5000", f"--screenshot={png}", "file://" + page],
                           check=True, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            jpg = os.path.join(out_dir, f"{IMG_VERSION}-{n}.jpg")
            subprocess.run(["sips", "-s", "format", "jpeg", "-s", "formatOptions", "88", png, "--out", jpg],
                           check=True, stdout=subprocess.DEVNULL)
        finally:
            for p in (page, png):
                if os.path.exists(p):
                    os.remove(p)


def ad_xml(i, slug, city, city_in):
    title, body = build(i, city_in)
    begin = dt.date.fromisoformat(START_DATE) + dt.timedelta(days=i // PER_DAY)
    imgs = "".join(f'\n      <Image url="{BASE_URL}/images/ip/{slug}/{IMG_VERSION}-{n}.jpg"/>' for n in (1, 2, 3))
    return f"""  <Ad>
    <Id>AGIP-{slug}</Id>
    <DateBegin>{begin.isoformat()}</DateBegin>
    <ManagerName>Адрес Готов</ManagerName>
    <ContactPhone>{PHONE}</ContactPhone>
    <ContactMethod>По телефону и в сообщениях</ContactMethod>
    <Category>Предложение услуг</Category>
    <Price>0</Price>
    <Title>{escape(title)}</Title>
    <Description><![CDATA[{body}]]></Description>
    <Address>{escape(city)}</Address>
    <ServiceType>Деловые услуги</ServiceType>
    <ServiceSubtype>Юридические услуги</ServiceSubtype>
    <ServiceSubspecies>Сопровождение бизнеса</ServiceSubspecies>
    <BusinessSpecialization>Предпринимательское право</BusinessSpecialization>
    <Place>У клиента</Place>
    <Prepayment>Нет</Prepayment>
    <Consultations>Есть</Consultations>
    <WorkWithContract>Да</WorkWithContract>
    <FormatWork>Сопровождение до результата</FormatWork>
    <WorkWith>Физические лица</WorkWith>
    <Images>{imgs}
    </Images>
  </Ad>
"""


def main():
    with_img = "--no-img" not in sys.argv
    feed_path = os.path.join(ROOT, "feed.xml")
    feed = open(feed_path, encoding="utf-8").read()
    feed = re.sub(r"  <Ad>\s*<Id>AGIP-.*?</Ad>\n", "", feed, flags=re.S)
    blocks = []
    for i, (slug, city, city_in) in enumerate(CITIES):
        if with_img:
            render_images(slug, city, city_in)
        blocks.append(ad_xml(i, slug, city, city_in))
        print(f"{i + 1:2}. {city:18} {blocks[-1].split('<DateBegin>')[1][:10]}  {build(i, city_in)[0]}")
    feed = feed.replace("</Ads>", "".join(blocks) + "</Ads>")
    open(feed_path, "w", encoding="utf-8").write(feed)


if __name__ == "__main__":
    main()
