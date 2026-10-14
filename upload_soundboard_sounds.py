import os
import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
import subprocess
import urllib.request
import json
import base64
from config import ADMIN_BOT_TOKEN, GUILD_ID

ffmpeg = r"C:\Users\RafaPlug11\AppData\Local\Microsoft\WinGet\Packages\Gyan.FFmpeg.Essentials_Microsoft.Winget.Source_8wekyb3d8bbwe\ffmpeg-9.0.1-essentials_build\bin\ffmpeg.EXE"

SOUNDS_TO_UPLOAD = [
    {
        "name": "donato_headshot",
        "text": "Headshot pa tu casa crack de parte del Donato",
        "emoji": "🎯",
        "volume": 0.95
    },
    {
        "name": "zelika_insano",
        "text": "Que onda cracks aqui Zelika en racha insana",
        "emoji": "🔥",
        "volume": 0.95
    },
    {
        "name": "hacker_aimbot",
        "text": "Aimbot activado todo rojo a la cabeza",
        "emoji": "🤖",
        "volume": 0.95
    },
    {
        "name": "gang_freefire",
        "text": "El Gang de Free Fire dominando la partida",
        "emoji": "👑",
        "volume": 0.95
    },
    {
        "name": "booyah_epico",
        "text": "Booyah victoria magistral en Bermuda",
        "emoji": "🏆",
        "volume": 1.0
    },
    {
        "name": "gloo_360",
        "text": "Pared Gloo a 360 grados cubreme manco",
        "emoji": "🛡️",
        "volume": 0.90
    },
    {
        "name": "mp40_cobra",
        "text": "Rafaga letal de MP40 Cobra al pecho",
        "emoji": "🐍",
        "volume": 0.95
    }
]

def generate_and_upload():
    print(f"Subiendo sonidos oficiales de Free Fire al Soundboard de Discord ({GUILD_ID})...")
    url = f"https://discord.com/api/v10/guilds/{GUILD_ID}/soundboard-sounds"

    for snd in SOUNDS_TO_UPLOAD:
        wav_file = f"snd_{snd['name']}.wav"
        mp3_file = f"snd_{snd['name']}.mp3"

        # 1. Generar audio WAV con SAPI
        ps_cmd = f"powershell -ExecutionPolicy Bypass -File generate_voice.ps1 -text \"{snd['text']}\" -output \"{wav_file}\""
        subprocess.run(ps_cmd, shell=True, check=True, capture_output=True)

        # 2. Convertir a MP3 compatible con Discord
        subprocess.run([ffmpeg, "-y", "-i", wav_file, "-c:a", "libmp3lame", "-b:a", "96k", mp3_file], check=True, capture_output=True)

        # 3. Base64
        with open(mp3_file, "rb") as f:
            b64_data = base64.b64encode(f.read()).decode("utf-8")

        payload = {
            "name": snd["name"],
            "sound": f"data:audio/mp3;base64,{b64_data}",
            "volume": snd["volume"],
            "emoji_name": snd["emoji"]
        }

        req = urllib.request.Request(
            url,
            data=json.dumps(payload).encode("utf-8"),
            headers={
                "Authorization": f"Bot {ADMIN_BOT_TOKEN}",
                "User-Agent": "DiscordBot (https://github.com/rafamodzyt, 1.0)",
                "Content-Type": "application/json"
            },
            method="POST"
        )

        try:
            with urllib.request.urlopen(req) as resp:
                res = json.loads(resp.read().decode())
                print(f"✅ Sonido '{snd['name']}' subido exitosamente al servidor (ID: {res.get('sound_id')})")
        except urllib.error.HTTPError as e:
            err = e.read().decode()
            print(f"⚠️ Error al subir '{snd['name']}': HTTP {e.code} - {err}")

        # Limpiar temporales
        for temp in [wav_file, mp3_file]:
            if os.path.exists(temp):
                try:
                    os.remove(temp)
                except Exception:
                    pass

    print("🎉 Proceso de Soundboard completado.")

if __name__ == "__main__":
    generate_and_upload()
