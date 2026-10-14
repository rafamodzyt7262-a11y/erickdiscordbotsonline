import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("ADMIN_BOT_TOKEN")
WALLPAPER_CH = "1559842253352992840"

headers = {
    "Authorization": f"Bot {TOKEN}",
    "Content-Type": "application/json"
}

embed = {
    "title": "🖼️ CENTRO DE WALLPAPERS 4K ULTRA HD • SELECCIONA TU DISPOSITIVO",
    "description": (
        "¡Bienvenido a la galería de wallpapers en ultra alta definición de **SHADOW BLOCK**!\n\n"
        "👇 **Elige tu tipo de dispositivo en el menú desplegable de abajo:**\n\n"
        "🖥️ **Opción 1: Wallpapers para PC / Escritorio** (3840 x 2160 UHD)\n"
        "📱 **Opción 2: Wallpapers para Móvil / Celular** (1440 x 3120 AMOLED Portrait)\n"
        "⚡ **Opción 3: Ráfaga de 25 Wallpapers 4K HD**\n"
        "🔓 **Opción 4: Wallpapers Exclusivos / Leaks Gaming**\n\n"
        "⏰ *El bot también publica automáticamente un lote nuevo cada hora.*"
    ),
    "color": 0x5865F2,
    "footer": {"text": "Sistema de Wallpapers Inteligente • Desarrollado por rafamodzyt"}
}

payload = {
    "embeds": [embed],
    "components": [
        {
            "type": 1,
            "components": [
                {
                    "type": 3, # Select Menu / Combo
                    "custom_id": "select_wallpaper_device",
                    "placeholder": "👉 Selecciona tu dispositivo (PC o Móvil)...",
                    "options": [
                        {
                            "label": "Wallpapers 4K para PC / Escritorio",
                            "value": "wallpaper_pc",
                            "description": "Formato horizontal 16:9 3840x2160 (Gaming, Cyberpunk, Autos)",
                            "emoji": {"name": "🖥️"}
                        },
                        {
                            "label": "Wallpapers 4K para Móvil / Celular",
                            "value": "wallpaper_mobile",
                            "description": "Formato vertical 9:16 1440x3120 (AMOLED, Anime, Aesthetic)",
                            "emoji": {"name": "📱"}
                        },
                        {
                            "label": "Ráfaga de 25 Wallpapers 4K HD",
                            "value": "wallpaper_burst",
                            "description": "Envío inmediato de un pack masivo de 25 fondos 4K",
                            "emoji": {"name": "⚡"}
                        },
                        {
                            "label": "Wallpapers Exclusivos / Leaks Gaming",
                            "value": "wallpaper_leaks",
                            "description": "Fondos filtrados y ediciones especiales gamer",
                            "emoji": {"name": "🔓"}
                        }
                    ]
                }
            ]
        }
    ]
}

r = requests.post(f"https://discord.com/api/v10/channels/{WALLPAPER_CH}/messages", headers=headers, json=payload)
print(f"Despliegue de menú interactivo en #wallpapers-4k-hd: HTTP {r.status_code}")
