import os
import requests
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("ADMIN_BOT_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")

headers = {"Authorization": f"Bot {TOKEN}"}

# Obtener guild info
r = requests.get(f"https://discord.com/api/v10/guilds/{GUILD_ID}", headers=headers)
guild_data = r.json()
print("Guild Name:", guild_data.get("name"))
print("Premium Tier (Boost):", guild_data.get("premium_tier"))
print("Premium Subscription Count (Boosts):", guild_data.get("premium_subscription_count"))

# Obtener stickers actuales
r_stickers = requests.get(f"https://discord.com/api/v10/guilds/{GUILD_ID}/stickers", headers=headers)
stickers = r_stickers.json()
print("Stickers actuales en el servidor:", len(stickers) if isinstance(stickers, list) else stickers)

# Obtener emojis actuales
r_emojis = requests.get(f"https://discord.com/api/v10/guilds/{GUILD_ID}/emojis", headers=headers)
emojis = r_emojis.json()
print("Emojis actuales en el servidor:", len(emojis) if isinstance(emojis, list) else emojis)
