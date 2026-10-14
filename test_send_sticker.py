import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("ADMIN_BOT_TOKEN")
headers = {
    "Authorization": f"Bot {TOKEN}",
    "Content-Type": "application/json"
}

channel_id = "1559826233620168734" # Canal de control
payload = {
    "embeds": [{
        "title": "🎭 Sticker Oficial: GigaChad Sonrisa",
        "description": "📂 Categoría: `GigaChad & Sigma` | Servidor SHADOW BLOCK\n✨ ¡Catálogo de **300+ Stickers y Memes Famosos** activado!",
        "color": 0x5865F2,
        "image": {"url": "https://media.giphy.com/media/CAYVZA5NRb529kKQUc/giphy.gif"},
        "footer": {"text": "Enviado desde el Panel C++ DX11 • rafamodzyt"}
    }]
}

r = requests.post(f"https://discord.com/api/v10/channels/{channel_id}/messages", headers=headers, json=payload)
print(f"Resultado envío de sticker a Discord: HTTP {r.status_code}")
