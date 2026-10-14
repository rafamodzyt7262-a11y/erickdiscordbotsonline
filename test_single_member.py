import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("ADMIN_BOT_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")

headers = {"Authorization": f"Bot {TOKEN}"}

# Probar consultar al bot 1 Erick x
bot1_id = "1559437873265119252"
r = requests.get(f"https://discord.com/api/v10/guilds/{GUILD_ID}/members/{bot1_id}", headers=headers)
print(f"Consulta miembro individual ({bot1_id}): HTTP {r.status_code}")
if r.status_code == 200:
    print(r.json())
