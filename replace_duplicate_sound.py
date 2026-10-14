import requests
import os
import subprocess
import json
import base64
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv('ADMIN_BOT_TOKEN')
GUILD_ID = os.getenv('GUILD_ID')
headers = {'Authorization': f'Bot {TOKEN}', 'Content-Type': 'application/json'}
ffmpeg = r'C:\Users\RafaPlug11\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg.Essentials_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.1-essentials_build\bin\ffmpeg.EXE'

# 1. Delete duplicate
requests.delete(f'https://discord.com/api/v10/guilds/{GUILD_ID}/soundboard-sounds/1559852051146612778', headers={'Authorization': f'Bot {TOKEN}'})

# 2. Generate mp40_cobra
wav = 'mp40.wav'
mp3 = 'mp40.mp3'
subprocess.run(['powershell', '-ExecutionPolicy', 'Bypass', '-File', 'generate_voice.ps1', '-text', 'Rafaga letal de MP40 Cobra al pecho', '-output', wav], capture_output=True)
subprocess.run([ffmpeg, '-y', '-i', wav, '-c:a', 'libmp3lame', '-b:a', '96k', mp3], capture_output=True)

with open(mp3, 'rb') as f:
    b64 = base64.b64encode(f.read()).decode('utf-8')

payload = {
    'name': 'mp40_cobra',
    'sound': f'data:audio/mp3;base64,{b64}',
    'volume': 0.95,
    'emoji_name': '🐍'
}
r = requests.post(f'https://discord.com/api/v10/guilds/{GUILD_ID}/soundboard-sounds', headers=headers, json=payload)
print('Upload mp40_cobra status:', r.status_code, r.text)
for f in [wav, mp3]:
    if os.path.exists(f):
        try:
            os.remove(f)
        except Exception:
            pass
