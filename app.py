
from flask import Flask, send_file
from PIL import Image, ImageDraw, ImageFont
import requests
from bs4 import BeautifulSoup
from io import BytesIO

app = Flask(__name__)

petitions = [
    ("Роман Кінаш", "https://petition.president.gov.ua/petition/245246"),
    ("Антон Листопад", "https://petition.president.gov.ua/petition/245654"),
    ("Василь Клекач", "https://petition.president.gov.ua/petition/244660"),
    ("Олег Гнед", "https://petition.president.gov.ua/petition/244852"),
    ("Юрій Бузіков", "https://petition.president.gov.ua/petition/244036"),
    ("Богдан Танасюк", "https://petition.president.gov.ua/petition/243292"),
    ("Руслан Валько", "https://petition.president.gov.ua/petition/244108"),
    ("Юрій Чмут", "https://petition.president.gov.ua/petition/243630")
]

def get_signatures(url):
    try:
        r = requests.get(url, timeout=5)
        soup = BeautifulSoup(r.text, 'html.parser')
        tag = soup.find("span", class_="counter")
        return tag.text.strip() if tag else "Н/Д"
    except:
        return "Н/Д"

@app.route("/")
def petition_image():
    img = Image.new('RGB', (1200, 630), color="#2C3E50")
    draw = ImageDraw.Draw(img)

    font_title = ImageFont.truetype("DejaVuSans-Bold.ttf", 38)
    font_text = ImageFont.truetype("DejaVuSans.ttf", 26)

    draw.text((60, 30), "💔 8 ЯНГОЛІВ, ЯКІ НАЗАВЖДИ В ПАМ'ЯТІ...", font=font_title, fill="#FFD700")
    draw.text((60, 90), "🙏 ВІДДАЙ ШАНУ — ПІДПИШИ ПЕТИЦІЮ", font=font_text, fill="#FFFFFF")

    y = 160
    for i, (name, url) in enumerate(petitions):
        count = get_signatures(url)
        draw.text((60, y), f"{i+1}. {name}", font=font_text, fill="#FFFFFF")
        draw.text((700, y), f"{count} підписів", font=font_text, fill="#C0C0C0")
        y += 45

    draw.text((60, y + 20), "✍️ Будь ласка, підпишіть петиції", font=font_text, fill="#D3D3D3")

    img_bytes = BytesIO()
    img.save(img_bytes, format='PNG')
    img_bytes.seek(0)
    return send_file(img_bytes, mimetype='image/png')
