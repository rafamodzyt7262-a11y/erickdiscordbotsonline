import os
import sys
import requests
from dotenv import load_dotenv

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

load_dotenv()
TOKEN = os.getenv("ADMIN_BOT_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")

cat_voice_id = "1559844313670754367"

headers = {
    "Authorization": f"Bot {TOKEN}",
    "Content-Type": "application/json"
}

# 1. Crear Categoría TIENDA & TICKETS
r_cat_tickets = requests.post(f"https://discord.com/api/v10/guilds/{GUILD_ID}/channels", headers=headers, json={
    "name": "🛒・TIENDA & SOPORTE",
    "type": 4 # Categoría
})
cat_tickets_id = r_cat_tickets.json().get("id") if r_cat_tickets.status_code == 201 else None
print(f"Categoría Tienda: {r_cat_tickets.status_code} (ID: {cat_tickets_id})")

# 2. Crear Canal de Tickets para Comprar Panel y Bots
r_ticket_ch = requests.post(f"https://discord.com/api/v10/guilds/{GUILD_ID}/channels", headers=headers, json={
    "name": "🎫・comprar-panel-y-bots",
    "type": 0, # Texto
    "parent_id": cat_tickets_id,
    "topic": "Compra aquí el Panel C++ DirectX 11 Win32 y Bots de Discord 24/7 personalizados • rafamodzyt"
})
ticket_ch_id = r_ticket_ch.json().get("id") if r_ticket_ch.status_code == 201 else None
print(f"Canal de Tickets: {r_ticket_ch.status_code} (ID: {ticket_ch_id})")

# 3. Crear Categoría ZONA GAMING & VOZ
r_cat_voice = requests.post(f"https://discord.com/api/v10/guilds/{GUILD_ID}/channels", headers=headers, json={
    "name": "🎮・ZONA GAMING & VOZ",
    "type": 4 # Categoría
})
cat_voice_id = r_cat_voice.json().get("id") if r_cat_voice.status_code == 201 else None
print(f"Categoría Gaming: {r_cat_voice.status_code} (ID: {cat_voice_id})")

# 4. Crear Canales de Voz
voice_channels = [
    {"name": "🎧・Soporte & Ayuda", "bitrate": 64000, "user_limit": 5},
    {"name": "🔥・Free Fire Escuadra 1", "bitrate": 64000, "user_limit": 4},
    {"name": "🔥・Free Fire Escuadra 2", "bitrate": 64000, "user_limit": 4},
    {"name": "🎮・Gaming General", "bitrate": 64000, "user_limit": 0},
    {"name": "💬・Chill & Charla", "bitrate": 64000, "user_limit": 0},
    {"name": "👑・Sala VIP rafamodzyt", "bitrate": 96000, "user_limit": 10}
]

for vc in voice_channels:
    r_vc = requests.post(f"https://discord.com/api/v10/guilds/{GUILD_ID}/channels", headers=headers, json={
        "name": vc["name"],
        "type": 2, # Canal de Voz
        "parent_id": cat_voice_id,
        "bitrate": vc["bitrate"],
        "user_limit": vc["user_limit"]
    })
    print(f"Canal de voz '{vc['name']}': HTTP {r_vc.status_code}")

# Guardar ID del canal de tickets para referencia
if ticket_ch_id:
    with open("ticket_channel_id.txt", "w", encoding="utf-8") as f:
        f.write(ticket_ch_id)
