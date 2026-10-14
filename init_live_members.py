import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("ADMIN_BOT_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")

headers = {"Authorization": f"Bot {TOKEN}"}

# Crear live_members.json inicial
data = {
    "server_name": "SHADOW BLOCK",
    "guild_id": GUILD_ID,
    "events": [
        {"type": "JOIN", "user_id": "1559437873265119252", "name": "Erick X", "time": "2026-10-14 02:29:13", "avatar": "ac0c78942cfd38fa952379d92d375b15"},
        {"type": "JOIN", "user_id": "1559830923174744125", "name": "SatanasMiPadre", "time": "2026-10-14 02:42:59", "avatar": ""},
        {"type": "STATUS", "user_id": "1559437873265119252", "name": "Erick X", "time": "2026-10-14 03:00:00", "details": "Conectado 24/7 en voz (General)"}
    ],
    "members": [
        {
            "id": "1559437873265119252",
            "name": "Erick X",
            "tag": "Erick X#7193",
            "nick": "Erick x [24/7]",
            "status": "ONLINE",
            "bot": True,
            "roles": ["VIP", "Bots 24/7"],
            "joined_at": "2026-10-13",
            "avatar_url": "https://cdn.discordapp.com/avatars/1559437873265119252/ac0c78942cfd38fa952379d92d375b15.png"
        },
        {
            "id": "1559830923174744125",
            "name": "SatanasMiPadre",
            "tag": "SatanasMiPadre#5129",
            "nick": "Bot Administrador",
            "status": "ONLINE",
            "bot": True,
            "roles": ["Administrador", "Bots"],
            "joined_at": "2026-10-14",
            "avatar_url": ""
        },
        {
            "id": "1350706770527653989",
            "name": "rafamodzyt",
            "tag": "rafamodzyt#0000",
            "nick": "rafamodzyt (Owner)",
            "status": "ONLINE",
            "bot": False,
            "roles": ["Owner", "Creador", "Admin"],
            "joined_at": "2026-10-12",
            "avatar_url": ""
        }
    ]
}

with open("live_members.json", "w", encoding="utf-8") as f:
    json.dump(data, f, indent=4, ensure_ascii=False)

print("live_members.json generado exitosamente.")
