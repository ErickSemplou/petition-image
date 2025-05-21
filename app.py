# -*- coding: utf-8 -*-
from flask import Flask, send_file, render_template_string
import requests
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont
from pathlib import Path

app = Flask(__name__)

# 8 петицій: ім’я та посилання
petitions = [
    {"name": "Роман Кінаш", "url": "https://petition.president.gov.ua/petition/245246"},
    {"name": "Антон Листопад", "url": "https://petition.president.gov.ua/petition/245654"},
    {"name": "Василь Клекач", "url": "https://petition.president.gov.ua/petition/244660"},
    {"name": "Олег Гнед", "url": "https://petition.president.gov.ua/petition/244852"},
    {"name": "Юрій Бузіков", "url": "https://petition.president.gov.ua/petition/244036"},
    {"name": "Богдан Танасюк", "url": "https://petition.president.gov.ua/petition/243292"},
    {"name": "Руслан Валько", "url": "https://petition.president.gov.ua/petition/244108"},
    {"name": "Юрій Чмут", "url": "https://petition.president.gov.ua/petition/243630"},
]

def get_votes(petition_url):
    try:
        r = requests.get(petition_url)
        soup = BeautifulSoup(r.text, "html.parser")
        span = soup.select_one("div.petition_votes_txt span")
        if span:
            return int(span.text.replace(" ", "").strip())
    except Exception as e:
        print(f"Error fetching {petition_url}: {e}")
    return 0

def create_image(petitions):
    width, height = 900, 700
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)

    # Шрифт (переконайся, що файл fonts/DejaVuSans.ttf є у проекті)
    font_path = Path("fonts/DejaVuSans.ttf")
    try:
        font_large = ImageFont.truetype(str(font_path), 28)
        font_small = ImageFont.truetype(str(font_path), 22)
    except Exception as e:
        print(f"Font load error: {e}")
        font_large = font_small = ImageFont.load_default()

    y = 20
    for idx, p in enumerate(petitions):
        votes = get_votes(p["url"])
        text = f"{idx+1}. {p['name']}"
        count = f"{votes} голосів"
        draw.text((20, y), text, font=font_large, fill="black")
        draw.text((600, y), count, font=font_small, fill="darkgreen")
        y += 60

    footer = "💔 8 ЯНГОЛІВ, ЯКІ НАЗАВЖДИ У ПАМ'ЯТІ. ПІДПИШИСЬ 🙏"
    draw.text((20, y + 30), footer, font=font_small, fill="red")

    output = BytesIO()
    img.save(output, format='PNG')
    output.seek(0)
    return output

@app.route("/petition_image")
def petition_image():
    image = create_image(petitions)
    return send_file(image, mimetype='image/png')

@app.route("/petition_page")
def petition_page():
    # Заміни на повний URL, якщо розгортаєш на сервері
    image_url = "/petition_image"
    html = f"""
    <!DOCTYPE html>
    <html lang="uk">
    <head>
        <meta charset="UTF-8" />
        <title>Петиції - Підтримай героїв</title>

        <!-- Open Graph для Facebook -->
        <meta property="og:title" content="Петиції - Підтримай героїв" />
        <meta property="og:description" content="Підпиши петиції за 8 Янголів, які назавжди у пам'яті." />
        <meta property="og:image" content="{image_url}" />
        <meta property="og:type" content="website" />

        <!-- Twitter Cards -->
        <meta name="twitter:card" content="summary_large_image" />
        <meta name="twitter:title" content="Петиції - Підтримай героїв" />
        <meta name="twitter:description" content="Підпиши петиції за 8 Янголів, які назавжди у пам'яті." />
        <meta name="twitter:image" content="{image_url}" />
    </head>
    <body>
        <h1>Петиції - Підтримай героїв</h1>
        <p>Переглянь динамічний статус петицій нижче.</p>
        <img src="{image_url}" alt="Петиції" />
    </body>
    </html>
    """
    return render_template_string(html)

if __name__ == "__main__":
    app.run()
