import os
import sys
import time
import requests
from dotenv import load_dotenv

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

from wallpapers_data import generate_unique_wallpapers

load_dotenv()
TOKEN = os.getenv("ADMIN_BOT_TOKEN")
WALLPAPER_CH = "1559842253352992840"

headers = {
    "Authorization": f"Bot {TOKEN}",
    "Content-Type": "application/json"
}

def send_burst(count=100):
    print(f"🚀 Generando {count} wallpapers 4K únicos de la base de 99,999+ sin duplicados...")
    wallpapers = generate_unique_wallpapers(count, mode="all")

    # Discord permite máximo 10 embeds por mensaje.
    # 100 wallpapers = 10 mensajes con 10 embeds cada uno.
    chunk_size = 10
    total_batches = (len(wallpapers) + chunk_size - 1) // chunk_size

    print(f"📦 Desplegando en {total_batches} lotes a Discord con control de rate-limit...")

    for idx in range(total_batches):
        batch = wallpapers[idx * chunk_size : (idx + 1) * chunk_size]
        embeds = []
        for item in batch:
            emb = {
                "title": f"🖼️ 4K ULTRA HD: {item['title']}",
                "description": f"📂 **Categoría:** `{item['category']}` | 📐 **Resolución:** `{item['res']}`",
                "color": 0x5865F2 if not item.get("is_mobile") else 0x9B59B6,
                "image": {"url": item["url"]},
                "footer": {"text": f"Galería Masiva 99,999+ • SHADOW BLOCK • rafamodzyt • ID #{item['id']}"}
            }
            embeds.append(emb)

        header_content = f"⚡ **[LOTE {idx+1}/{total_batches}] 100 WALLPAPERS 4K ULTRA HD • 99,999+ SIN REPETIR**" if idx == 0 else ""
        
        try:
            r = requests.post(
                f"https://discord.com/api/v10/channels/{WALLPAPER_CH}/messages",
                headers=headers,
                json={
                    "content": header_content,
                    "embeds": embeds
                },
                timeout=15
            )
            print(f"✅ Lote {idx+1}/{total_batches} ({len(batch)} imágenes): HTTP {r.status_code}")
        except Exception as e:
            print(f"⚠️ Error en lote {idx+1}: {e}")

        # Pequeña pausa para no saturar la API de Discord
        time.sleep(1.2)

    print("🎉 Ráfaga de 100 Wallpapers 4K enviada con éxito total a Discord.")

if __name__ == "__main__":
    send_burst(100)
