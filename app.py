from flask import Flask, send_file
import requests
from bs4 import BeautifulSoup
from io import BytesIO
from PIL import Image, ImageDraw, ImageFont

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
    width, height = 800, 600
    img = Image.new('RGB', (width, height), color='white')
    draw = ImageDraw.Draw(img)

    try:
        font_large = ImageFont.truetype("arial.ttf", 28)
        font_small = ImageFont.truetype("arial.ttf", 22)
    except:
        font_large = font_small = ImageFont.load_default()

    y = 20
    for idx, p in enumerate(petitions):
        votes = get_votes(p["url"])
        text = f"{idx+1}. {p['name']}"
        count = f"{votes} голосів"
        draw.text((20, y), text, font=font_large, fill="black")
        draw.text((500, y), count, font=font_small, fill="darkgreen")
        y += 60

    # Підпис внизу
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

if __name__ == "__main__":
    app.run(debug=True)
