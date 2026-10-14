import os
import io
import requests
from PIL import Image
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("ADMIN_BOT_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")

headers = {"Authorization": f"Bot {TOKEN}"}

extra_stickers = [
    {
        "name": "PepeHappy",
        "description": "Pepe Happy Oficial",
        "tags": "pepe,frog,happy",
        "url": "https://upload.wikimedia.org/wikipedia/en/thumb/6/63/Feels_good_man.jpg/320px-Feels_good_man.jpg"
    },
    {
        "name": "DogeClassic",
        "description": "Doge Much Wow Oficial",
        "tags": "doge,dog,wow",
        "url": "https://upload.wikimedia.org/wikipedia/en/5/5f/Original_Doge_meme.jpg"
    }
]

for s in extra_stickers:
    try:
        r_img = requests.get(s["url"], timeout=10, headers={"User-Agent": "Mozilla/5.0"})
        if r_img.status_code == 200:
            img = Image.open(io.BytesIO(r_img.content)).convert("RGBA")
            img = img.resize((320, 320), Image.Resampling.LANCZOS)
            buf = io.BytesIO()
            img.save(buf, format="PNG", optimize=True)
            buf.seek(0)

            files = {"file": (f"{s['name']}.png", buf, "image/png")}
            data = {"name": s["name"], "description": s["description"], "tags": s["tags"]}
            r = requests.post(f"https://discord.com/api/v10/guilds/{GUILD_ID}/stickers", headers=headers, data=data, files=files)
            print(f"Sticker '{s['name']}': HTTP {r.status_code}")
    except Exception as e:
        print(f"Error: {e}")
