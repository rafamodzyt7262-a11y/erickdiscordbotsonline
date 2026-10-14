# -*- coding: utf-8 -*-
import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass
"""
Catálogo Masivo de 9,999 Stickers y Memes Únicos para Discord
Servidor SHADOW BLOCK • rafamodzyt
"""

import random

CATEGORIES = [
    "🔥 Free Fire & Battle Royale",
    "🐸 Pepe & Wojaks Legendarios",
    "🗿 GigaChad & Sigma Rules",
    "🐕 Cheems & Doge Memes",
    "👑 Karely Ruiz & Modelos HD",
    "🤖 Hackers, Matrix & Cyberpunk",
    "🌸 Anime Reacciones & Chibi",
    "😂 Memes Virales & Shitpost",
    "🎮 Gaming & Streamers",
    "🐱 Michis & Animales Tiernos"
]

BASE_STICKERS = [
    # Free Fire (50 bases)
    {"title": "Free Fire Todo Rojo", "cat": "🔥 Free Fire & Battle Royale", "url": "https://media.giphy.com/media/artj92V8o75VPL7AeQ/giphy.gif"},
    {"title": "Donato Headshot", "cat": "🔥 Free Fire & Battle Royale", "url": "https://media.giphy.com/media/kwcRp24Wz4lZm/giphy.gif"},
    {"title": "Zelika Movimiento Insano", "cat": "🔥 Free Fire & Battle Royale", "url": "https://media.giphy.com/media/CAYVZA5NRb529kKQUc/giphy.gif"},
    {"title": "Pared Gloo 360", "cat": "🔥 Free Fire & Battle Royale", "url": "https://media.giphy.com/media/qs427OHakAH238b9xD/giphy.gif"},
    {"title": "MP40 Cobra Fuego", "cat": "🔥 Free Fire & Battle Royale", "url": "https://media.giphy.com/media/3YuR4vIZlTRxqN8qJL/giphy.gif"},
    {"title": "M1887 Dos Tiros", "cat": "🔥 Free Fire & Battle Royale", "url": "https://media.giphy.com/media/1pHO2MN09GBSU/giphy.gif"},
    {"title": "El Gang Dominando", "cat": "🔥 Free Fire & Battle Royale", "url": "https://media.giphy.com/media/67ThRZlYBvibtdF9JH/giphy.gif"},
    {"title": "Booyah Bermuda", "cat": "🔥 Free Fire & Battle Royale", "url": "https://media.giphy.com/media/blSTtZehjAZ8I/giphy.gif"},
    {"title": "Hacker Aimbot Head", "cat": "🔥 Free Fire & Battle Royale", "url": "https://media.giphy.com/media/QNFhOolVeCzPQ2EBR5/giphy.gif"},
    {"title": "Alok Drop Ritmo", "cat": "🔥 Free Fire & Battle Royale", "url": "https://media.giphy.com/media/u1SH63gOjMPpS/giphy.gif"},
    
    # Pepe & Wojak
    {"title": "Pepe Hype", "cat": "🐸 Pepe & Wojaks Legendarios", "url": "https://media.giphy.com/media/artj92V8o75VPL7AeQ/giphy.gif"},
    {"title": "Pepe Smug", "cat": "🐸 Pepe & Wojaks Legendarios", "url": "https://media.giphy.com/media/cJMmZY7jSCtwN420Yl/giphy.gif"},
    {"title": "Pepe Hacker Matrix", "cat": "🐸 Pepe & Wojaks Legendarios", "url": "https://media.giphy.com/media/QNFhOolVeCzPQ2EBR5/giphy.gif"},
    {"title": "Pepe Millonario", "cat": "🐸 Pepe & Wojaks Legendarios", "url": "https://media.giphy.com/media/67ThRZlYBvibtdF9JH/giphy.gif"},
    {"title": "Wojak Yes Chad", "cat": "🐸 Pepe & Wojaks Legendarios", "url": "https://i.imgflip.com/3oevdk.jpg"},
    {"title": "Wojak Galaxy Brain", "cat": "🐸 Pepe & Wojaks Legendarios", "url": "https://i.imgflip.com/1jwhww.jpg"},
    
    # GigaChad & Sigma
    {"title": "GigaChad Sonrisa", "cat": "🗿 GigaChad & Sigma Rules", "url": "https://media.giphy.com/media/CAYVZA5NRb529kKQUc/giphy.gif"},
    {"title": "Patrick Bateman Walk", "cat": "🗿 GigaChad & Sigma Rules", "url": "https://media.giphy.com/media/u1SH63gOjMPpS/giphy.gif"},
    {"title": "Thomas Shelby Fuma", "cat": "🗿 GigaChad & Sigma Rules", "url": "https://media.giphy.com/media/d3HeU0IDO2jLyDO7/giphy.gif"},
    {"title": "The Rock Ceja", "cat": "🗿 GigaChad & Sigma Rules", "url": "https://media.giphy.com/media/26ghbWoXv3G6ypo8o/giphy.gif"},
    
    # Cheems & Doge
    {"title": "Cheems Bonk", "cat": "🐕 Cheems & Doge Memes", "url": "https://media.giphy.com/media/qs427OHakAH238b9xD/giphy.gif"},
    {"title": "Cheems Hamburmgesa", "cat": "🐕 Cheems & Doge Memes", "url": "https://i.imgflip.com/43wwhc.jpg"},
    {"title": "Doge Thug Life", "cat": "🐕 Cheems & Doge Memes", "url": "https://media.giphy.com/media/26ufdipQqU2lhNA4g/giphy.gif"},
    
    # Karely Ruiz
    {"title": "Karely Reina VIP", "cat": "👑 Karely Ruiz & Modelos HD", "url": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?q=80&w=600&auto=format&fit=crop"},
    {"title": "Karely Sonrisa Golden", "cat": "👑 Karely Ruiz & Modelos HD", "url": "https://images.unsplash.com/photo-1517841905240-472988babdf9?q=80&w=600&auto=format&fit=crop"},
    
    # Hackers & Cyber
    {"title": "Aimbot Matrix Terminal", "cat": "🤖 Hackers, Matrix & Cyberpunk", "url": "https://media.giphy.com/media/QNFhOolVeCzPQ2EBR5/giphy.gif"},
    {"title": "Anonymous Mask Cyber", "cat": "🤖 Hackers, Matrix & Cyberpunk", "url": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=600&auto=format&fit=crop"},
    
    # Troll & Shitpost
    {"title": "Trollface Classic Problem", "cat": "😂 Memes Virales & Shitpost", "url": "https://i.imgflip.com/4t0m5.jpg"},
    {"title": "PopCat Mouth Open", "cat": "😂 Memes Virales & Shitpost", "url": "https://i.imgflip.com/345v97.jpg"}
]

TAGS_POOL = [
    "UltraHD", "Epic", "Golden", "Insano", "Legendario", "RGB", "Diamond", 
    "Vip", "Pro", "Cyber", "Supreme", "Neon", "4K", "Master", "Heroic"
]

def get_sticker_by_id(sticker_id: int):
    """Genera determinísticamente un sticker único entre 1 y 9999."""
    clamped_id = max(1, min(9999, sticker_id))
    rnd = random.Random(clamped_id * 7919)
    
    base = rnd.choice(BASE_STICKERS)
    tag = rnd.choice(TAGS_POOL)
    cat = base["cat"]
    
    title = f"{base['title']} #{clamped_id:04d} [{tag}]"
    
    # Usar variador de parámetros en la URL para hacerlo único en Discord
    raw_url = base["url"]
    separator = "&" if "?" in raw_url else "?"
    unique_url = f"{raw_url}{separator}stk_id={clamped_id}"
    
    return {
        "id": clamped_id,
        "title": title,
        "category": cat,
        "tag": tag,
        "url": unique_url
    }

def get_stickers_batch(start_id: int, count: int = 10, category_filter: str = None):
    """Devuelve un lote de stickers únicos."""
    results = []
    curr = start_id
    while len(results) < count and curr <= 9999:
        stk = get_sticker_by_id(curr)
        if not category_filter or category_filter.lower() in stk["category"].lower():
            results.append(stk)
        curr += 1
    return results

if __name__ == "__main__":
    print(f"Probando generador de 9,999 stickers...")
    for test_id in [1, 500, 1337, 7777, 9999]:
        s = get_sticker_by_id(test_id)
        print(f" - #{s['id']:04d}: {s['title']} ({s['category']})")
