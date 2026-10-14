import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("ADMIN_BOT_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")

headers = {"Authorization": f"Bot {TOKEN}"}
r = requests.get(f"https://discord.com/api/v10/guilds/{GUILD_ID}/members?limit=100", headers=headers)
print(f"Status miembros: HTTP {r.status_code}")
if r.status_code == 200:
    members = r.json()
    print(f"Total miembros obtenidos: {len(members)}")
    for m in members:
        u = m.get("user", {})
        print(f" - {u.get('username')}#{u.get('discriminator')} | Nick: {m.get('nick')} | ID: {u.get('id')} | Roles: {m.get('roles')}")
