import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("ADMIN_BOT_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")

headers = {
    "Authorization": f"Bot {TOKEN}",
    "Content-Type": "application/json"
}

# 1. Crear canal de wallpapers
payload = {
    "name": "🖼️・wallpapers-4k-hd",
    "type": 0, # Texto
    "topic": "Wallpapers diarios y a cada hora en calidad 4K Ultra HD para PC y Celular • rafamodzyt"
}

r = requests.post(f"https://discord.com/api/v10/guilds/{GUILD_ID}/channels", headers=headers, json=payload)
print(f"Creación canal wallpapers: HTTP {r.status_code}")
if r.status_code == 201:
    ch_data = r.json()
    ch_id = ch_data["id"]
    print(f"Canal creado con ID: {ch_id}")

    # 2. Publicar primer wallpaper 4K
    embed_pc = {
        "title": "🖥️ WALLPAPER 4K PARA PC / ESCRITORIO",
        "description": "🌟 **Tema:** Cyberpunk Neon City Skyline\n📐 **Resolución:** 3840 x 2160 (4K UHD)\n👑 **Canal Oficial:** `wallpapers-4k-hd`",
        "color": 0x5865F2,
        "image": {"url": "https://images.unsplash.com/photo-1542751371-adc38448a05e?q=80&w=2070&auto=format&fit=crop"},
        "footer": {"text": "Sistema de Wallpapers Automáticos • Hecho por rafamodzyt"}
    }
    embed_mobile = {
        "title": "📱 WALLPAPER 4K PARA MÓVIL / CELULAR",
        "description": "🌌 **Tema:** Galaxia Cósmica AMOLED Black\n📐 **Resolución:** 1440 x 3120 (Ultra Portrait)\n👑 **Canal Oficial:** `wallpapers-4k-hd`",
        "color": 0x9B59B6,
        "image": {"url": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?q=80&w=1968&auto=format&fit=crop"},
        "footer": {"text": "Auto-Wallpapers cada hora • Servidor SHADOW BLOCK"}
    }
    r_msg = requests.post(f"https://discord.com/api/v10/channels/{ch_id}/messages", headers=headers, json={"embeds": [embed_pc, embed_mobile]})
    print(f"Publicación inicial de wallpapers: HTTP {r_msg.status_code}")

    # Guardar ID en .env o archivo
    with open("wallpapers_config.txt", "w", encoding="utf-8") as f:
        f.write(ch_id)
