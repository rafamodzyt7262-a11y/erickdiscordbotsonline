# -*- coding: utf-8 -*-
import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import os
import requests
import time
from dotenv import load_dotenv
from stickers_catalog_9999 import get_sticker_by_id

load_dotenv()
TOKEN = os.getenv("ADMIN_BOT_TOKEN")
channel_id = "1559852912727822396"

headers = {
    "Authorization": f"Bot {TOKEN}",
    "Content-Type": "application/json"
}

# Post a showcase burst of stickers across all categories
featured_ids = [1, 2, 5, 8, 12, 18, 25, 42, 55, 69, 77, 100, 150, 200, 300, 500, 777, 1000, 1337, 2026, 5000, 7777, 9999]

print("Enviando stickers destacados a 🎨・stickers-9999-hd...")

# Group into batches of 4
for i in range(0, len(featured_ids), 4):
    batch = featured_ids[i:i+4]
    embeds = []
    for sid in batch:
        s = get_sticker_by_id(sid)
        embeds.append({
            "title": f"🎭 {s['title']}",
            "description": f"📂 **Categoría:** `{s['category']}`\n🏷️ **Etiqueta:** `{s['tag']}`\n⚡ **Comando:** `/sticker id:{s['id']}` o `!sticker {s['id']}`",
            "color": 0x5865F2,
            "image": {"url": s["url"]},
            "footer": {"text": f"Sticker #{s['id']:04d} de 9,999 • SHADOW BLOCK • rafamodzyt"}
        })
    r = requests.post(f"https://discord.com/api/v10/channels/{channel_id}/messages", headers=headers, json={"embeds": embeds})
    print(f"Lote stickers {batch}: HTTP {r.status_code}")
    time.sleep(1)

print("¡Stickers destacados publicados exitosamente!")
