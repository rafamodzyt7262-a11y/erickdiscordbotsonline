import urllib.request
import json
from config import ADMIN_BOT_TOKEN, GUILD_ID

headers = {
    "Authorization": f"Bot {ADMIN_BOT_TOKEN}",
    "User-Agent": "DiscordBot (https://github.com/rafamodzyt, 1.0)"
}

url = f"https://discord.com/api/v10/guilds/{GUILD_ID}/soundboard-sounds"
try:
    req = urllib.request.Request(url, headers=headers)
    with urllib.request.urlopen(req) as resp:
        sounds = json.loads(resp.read().decode())
        print(f"Total de sonidos en el servidor: {len(sounds)}")
        for s in sounds:
            print(f" - {s.get('name')} (ID: {s.get('sound_id')})")
except Exception as e:
    print(f"Error checking soundboard sounds: {e}")
