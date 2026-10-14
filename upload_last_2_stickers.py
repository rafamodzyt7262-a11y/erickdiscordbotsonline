import os
import io
import requests
from PIL import Image
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('ADMIN_BOT_TOKEN')
GUILD_ID = os.getenv('GUILD_ID')
headers = {'Authorization': f'Bot {TOKEN}'}

stickers_to_try = [
    {'name': 'GigaChad', 'desc': 'GigaChad Sigma', 'tags': 'chad', 'url': 'https://i.imgflip.com/4a034w.png'},
    {'name': 'CheemsBonk', 'desc': 'Cheems Bonk', 'tags': 'doge', 'url': 'https://i.imgflip.com/43wwhc.jpg'}
]

for s in stickers_to_try:
    resp = requests.get(s['url'], timeout=10)
    print(f"Img dl status for {s['name']}: {resp.status_code}")
    img = Image.open(io.BytesIO(resp.content)).convert('RGBA')
    img = img.resize((320, 320), Image.Resampling.LANCZOS)
    buf = io.BytesIO()
    img.save(buf, format='PNG', optimize=True)
    buf.seek(0)
    files = {'file': (s['name'] + '.png', buf, 'image/png')}
    data = {'name': s['name'], 'description': s['desc'], 'tags': s['tags']}
    r = requests.post(f'https://discord.com/api/v10/guilds/{GUILD_ID}/stickers', headers=headers, data=data, files=files)
    print(s['name'], r.status_code, r.text)
