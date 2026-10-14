import os
import io
import base64
import requests
from PIL import Image
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("ADMIN_BOT_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")

headers = {"Authorization": f"Bot {TOKEN}"}

# 1. 5 Stickers oficiales para el servidor (Límite Tier 0 = 5 stickers)
STICKERS_TO_UPLOAD = [
    {
        "name": "GigaChad",
        "description": "GigaChad Sonrisa Oficial SHADOW BLOCK",
        "tags": "gigachad,chad,sigma",
        "url": "https://i.imgflip.com/4a034w.png"
    },
    {
        "name": "CheemsBonk",
        "description": "Cheems Bonk Horny Jail",
        "tags": "cheems,bonk,doge",
        "url": "https://i.imgflip.com/43wwhc.jpg"
    },
    {
        "name": "PopCat",
        "description": "Pop Cat Abriendo Boca",
        "tags": "cat,popcat,gato",
        "url": "https://i.imgflip.com/345v97.jpg"
    },
    {
        "name": "WojakChad",
        "description": "Yes Chad Wojak",
        "tags": "wojak,chad,yes",
        "url": "https://i.imgflip.com/3oevdk.jpg"
    },
    {
        "name": "Trollface",
        "description": "Trollface Problem Oficial",
        "tags": "troll,trollface,meme",
        "url": "https://i.imgflip.com/4t0m5.jpg"
    }
]

print("--- Subiendo Stickers Oficiales al Servidor SHADOW BLOCK ---")
for s in STICKERS_TO_UPLOAD:
    try:
        # Descargar imagen
        img_resp = requests.get(s["url"], timeout=10)
        if img_resp.status_code != 200:
            print(f"Error descargando {s['name']}: HTTP {img_resp.status_code}")
            continue

        # Convertir y redimensionar a 320x320 PNG exactamente como requiere Discord
        img = Image.open(io.BytesIO(img_resp.content)).convert("RGBA")
        img = img.resize((320, 320), Image.Resampling.LANCZOS)
        out_buf = io.BytesIO()
        img.save(out_buf, format="PNG", optimize=True)
        out_buf.seek(0)

        files = {
            "file": (f"{s['name']}.png", out_buf, "image/png")
        }
        data = {
            "name": s["name"],
            "description": s["description"],
            "tags": s["tags"]
        }

        r = requests.post(
            f"https://discord.com/api/v10/guilds/{GUILD_ID}/stickers",
            headers=headers,
            data=data,
            files=files
        )
        print(f"Sticker '{s['name']}': HTTP {r.status_code} - {r.text[:80]}")
    except Exception as e:
        print(f"Excepción subiendo {s['name']}: {e}")

# 2. Subir Emojis oficiales (hasta 50 en Tier 0)
EMOJIS_TO_UPLOAD = [
    {"name": "pepe_smug", "url": "https://i.imgflip.com/2wifvo.jpg"},
    {"name": "stonks", "url": "https://i.imgflip.com/31hg56.png"},
    {"name": "disaster_girl", "url": "https://i.imgflip.com/23ls.jpg"},
    {"name": "galaxy_brain", "url": "https://i.imgflip.com/1jwhww.jpg"},
    {"name": "buff_doge", "url": "https://i.imgflip.com/45v7t9.png"},
    {"name": "polite_cat", "url": "https://i.imgflip.com/2bvprb.jpg"},
    {"name": "crying_cat", "url": "https://i.imgflip.com/265j72.jpg"},
    {"name": "karely_queen", "url": "https://i.imgflip.com/3oevdk.jpg"}
]

print("\n--- Subiendo Emojis Oficiales al Servidor SHADOW BLOCK ---")
for e in EMOJIS_TO_UPLOAD:
    try:
        img_resp = requests.get(e["url"], timeout=10)
        if img_resp.status_code != 200:
            continue
        img = Image.open(io.BytesIO(img_resp.content)).convert("RGBA")
        img = img.resize((128, 128), Image.Resampling.LANCZOS)
        out_buf = io.BytesIO()
        img.save(out_buf, format="PNG", optimize=True)
        b64_str = base64.b64encode(out_buf.getvalue()).decode("utf-8")
        data_uri = f"data:image/png;base64,{b64_str}"

        payload = {
            "name": e["name"],
            "image": data_uri
        }
        r = requests.post(
            f"https://discord.com/api/v10/guilds/{GUILD_ID}/emojis",
            headers={**headers, "Content-Type": "application/json"},
            json=payload
        )
        print(f"Emoji '{e['name']}': HTTP {r.status_code} - {r.text[:80]}")
    except Exception as exc:
        print(f"Excepción subiendo emoji {e['name']}: {exc}")
