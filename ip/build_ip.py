#!/usr/bin/env python3
"""
Серия объявлений «Регистрация ИП» для фида Адрес Готов.

Для каждого города: своя инфографика (2 картинки одного из 5 стилей, с названием города) и свой
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
import styles  # noqa: E402

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
BASE_URL = "https://ivananufrievv-hue.github.io/adres-gotov-feed"
CHROME = "/Applications/Google Chrome.app/Contents/MacOS/Google Chrome"
PHONE = "+7 999 000-80-64"
IMG_VERSION = "v2"  # при замене картинок менять: Авито кеширует по URL

# Пары картинок одного стиля; город i получает пару i % 5. Первая — обложка.
STYLES = [(styles.v02, styles.v01), (styles.v04, styles.v03), (styles.v05, styles.v06),
          (styles.v07, styles.v08), (styles.v09, styles.v10)]
N_IMAGES = 2


def render_images(i, slug, city, city_in):
    out_dir = os.path.join(ROOT, "images", "ip", slug)
    os.makedirs(out_dir, exist_ok=True)
    for old in os.listdir(out_dir):
        if not old.startswith(IMG_VERSION + "-"):
            os.remove(os.path.join(out_dir, old))
    for n, fn in enumerate(STYLES[i % len(STYLES)], 1):
        with tempfile.NamedTemporaryFile("w", suffix=".html", dir=os.path.join(ROOT, "ip"), delete=False, encoding="utf-8") as fh:
            fh.write(styles.page_html(fn(city, city_in)))
            page = fh.name
        png = page[:-5] + ".png"
        try:
            subprocess.run([CHROME, "--headless=new", "--hide-scrollbars", "--window-size=1200,900",
                            "--virtual-time-budget=8000", f"--screenshot={png}", "file://" + page],
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
    imgs = "".join(f'\n      <Image url="{BASE_URL}/images/ip/{slug}/{IMG_VERSION}-{n}.jpg"/>' for n in range(1, N_IMAGES + 1))
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
            render_images(i, slug, city, city_in)
        blocks.append(ad_xml(i, slug, city, city_in))
        print(f"{i + 1:2}. {city:18} {blocks[-1].split('<DateBegin>')[1][:10]}  {build(i, city_in)[0]}")
    feed = feed.replace("</Ads>", "".join(blocks) + "</Ads>")
    open(feed_path, "w", encoding="utf-8").write(feed)


if __name__ == "__main__":
    main()
