import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("ADMIN_BOT_TOKEN")
TICKET_CHANNEL_ID = "1559844380934807612"

headers = {
    "Authorization": f"Bot {TOKEN}",
    "Content-Type": "application/json"
}

embed = {
    "title": "🛒 TIENDA OFICIAL SHADOW BLOCK • PANELES C++ & BOTS 24/7",
    "description": (
        "¡Bienvenido a la tienda oficial desarrollada por **rafamodzyt**!\n\n"
        "🔥 **Productos Disponibles:**\n\n"
        "💻 **1. Panel C++ DirectX 11 Win32 (Discord Server Manager)**\n"
        "• Control total del servidor desde tu PC en tiempo real.\n"
        "• Gestión de canales, roles, purga de chat y moderación instantánea.\n"
        "• Pestaña de 300+ Stickers/Memes y Wallpapers 4K automáticos.\n"
        "• Modificador de perfiles de miembros (Apodos, roles, RPC).\n\n"
        "🎙️ **2. Bot Erick x de Voz 24/7 (Meta 1,000,000 Horas)**\n"
        "• Bot de voz permanente con auto-reconexión instantánea.\n"
        "• Ensordecido `self_deaf` y avatar personalizado en HD.\n"
        "• Conteo persistente y comandos de control.\n\n"
        "⚡ **¿Cómo comprar o pedir soporte?**\n"
        "Haz clic en los botones de abajo o escribe un mensaje en este canal para que el staff te atienda."
    ),
    "color": 0x5865F2,
    "fields": [
        {"name": "💳 Métodos de Pago Aceptados", "value": "• PayPal\n• Criptomonedas (USDT / BTC)\n• Transferencias Locales", "inline": True},
        {"name": "👑 Creador & Desarrollador", "value": "`rafamodzyt`\nDiscord: [SHADOW BLOCK](https://discord.gg/dc5HAzAMmg)", "inline": True}
    ],
    "footer": {"text": "Sistema de Tickets y Ventas • SHADOW BLOCK Oficial"}
}

# Enviar embed con componentes interactivos
payload = {
    "embeds": [embed],
    "components": [
        {
            "type": 1,
            "components": [
                {
                    "type": 2,
                    "style": 1, # Primary (Azul)
                    "label": "Comprar Panel C++ DX11",
                    "custom_id": "buy_panel_cpp",
                    "emoji": {"name": "💻"}
                },
                {
                    "type": 2,
                    "style": 3, # Success (Verde)
                    "label": "Comprar Bot 24/7",
                    "custom_id": "buy_bot_voice",
                    "emoji": {"name": "🎙️"}
                },
                {
                    "type": 2,
                    "style": 5, # Link
                    "label": "Discord Oficial",
                    "url": "https://discord.gg/dc5HAzAMmg",
                    "emoji": {"name": "👑"}
                }
            ]
        }
    ]
}

r = requests.post(f"https://discord.com/api/v10/channels/{TICKET_CHANNEL_ID}/messages", headers=headers, json=payload)
print(f"Envío de panel de tienda y tickets: HTTP {r.status_code}")
