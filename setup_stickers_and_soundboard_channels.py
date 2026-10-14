# -*- coding: utf-8 -*-
import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import os
import requests
import json
from dotenv import load_dotenv

load_dotenv()
TOKEN = os.getenv("ADMIN_BOT_TOKEN")
GUILD_ID = os.getenv("GUILD_ID")

headers = {
    "Authorization": f"Bot {TOKEN}",
    "Content-Type": "application/json"
}

def get_or_create_channel(name, ch_type=0, topic="", parent_id=None):
    r = requests.get(f"https://discord.com/api/v10/guilds/{GUILD_ID}/channels", headers=headers)
    if r.status_code == 200:
        for c in r.json():
            if c.get("name") == name:
                print(f"Canal existente encontrado: {name} ({c.get('id')})")
                return c.get("id")

    payload = {"name": name, "type": ch_type, "topic": topic}
    if parent_id:
        payload["parent_id"] = parent_id

    cr = requests.post(f"https://discord.com/api/v10/guilds/{GUILD_ID}/channels", headers=headers, json=payload)
    if cr.status_code in (200, 201):
        data = cr.json()
        print(f"Canal creado exitosamente: {name} ({data['id']})")
        return data["id"]
    else:
        print(f"Error creando canal {name}: HTTP {cr.status_code} - {cr.text}")
        return None

def setup_all():
    print("=== Configurando Canales de Stickers 9,999 y Soundboard 500 Voces ===")

    # 1. Canal de Stickers 9,999
    stickers_ch_id = get_or_create_channel(
        name="🎨・stickers-9999-hd",
        ch_type=0,
        topic="Catálogo Masivo de 9,999 Stickers y Memes Famosos HD • SHADOW BLOCK • rafamodzyt"
    )

    # 2. Canal de Soundboard 500 Voces
    soundboard_ch_id = get_or_create_channel(
        name="🔊・soundboard-500-freefire",
        ch_type=0,
        topic="Soundboard Oficial con 500 Voces de Free Fire: Donato, Zelika, Hackers, Gang y Booyah • rafamodzyt"
    )

    # Publicar Hub en Canal de Stickers
    if stickers_ch_id:
        embed_stickers = {
            "title": "🎭 HUB OFICIAL DE 9,999 STICKERS & MEMES FAMOSOS",
            "description": (
                "¡Bienvenido al catálogo interactivo de **9,999 Stickers y Memes HD** de **SHADOW BLOCK**!\n\n"
                "📌 **¿Cómo usar los stickers?**\n"
                "• Usa el menú desplegable abajo para explorar por categorías.\n"
                "• Presiona los botones rápidos para generar ráfagas de memes.\n"
                "• Usa `/sticker [id]` o `!sticker [id]` (1 al 9999) para enviar cualquier sticker al chat.\n\n"
                "📂 **Categorías Disponibles:**\n"
                "🔥 **Free Fire & Battle Royale** (Todo Rojo, Pared Gloo, MP40 Cobra)\n"
                "🐸 **Pepe The Frog & Wojaks** (Pepe Hype, Yes Chad, Galaxy Brain)\n"
                "🗿 **GigaChad & Sigma Rules** (Bateman, Thomas Shelby, The Rock)\n"
                "🐕 **Cheems & Doge** (Cheems Bonk, Doge Thug Life, Ansiedad)\n"
                "👑 **Karely Ruiz HD** (Colección exclusiva de fotos y poses VIP)\n"
                "🤖 **Hackers, Matrix & Cyber** (Aimbot, Terminal Hacker, Anonymous)\n"
                "😂 **Memes Virales & Shitpost** (Trollface, PopCat, Risas Virales)"
            ),
            "color": 0xF1C40F,
            "image": {"url": "https://media.giphy.com/media/CAYVZA5NRb529kKQUc/giphy.gif"},
            "footer": {"text": "9,999 Stickers • Creado por rafamodzyt • SHADOW BLOCK"}
        }

        components_stickers = [
            {
                "type": 1,
                "components": [
                    {
                        "type": 3,
                        "custom_id": "select_sticker_category",
                        "placeholder": "🔍 Selecciona una categoría de stickers (1-9999)...",
                        "options": [
                            {"label": "Free Fire & Battle Royale", "value": "cat_freefire", "description": "Todo Rojo, Donato, Zelika, Pared Gloo", "emoji": {"name": "🔥"}},
                            {"label": "Pepe The Frog & Wojaks", "value": "cat_pepe", "description": "Pepe Hype, Sad, Rich, Yes Chad, Soyjak", "emoji": {"name": "🐸"}},
                            {"label": "GigaChad & Sigma Rules", "value": "cat_sigma", "description": "Patrick Bateman, Thomas Shelby, GigaChad", "emoji": {"name": "🗿"}},
                            {"label": "Cheems & Doge Memes", "value": "cat_doge", "description": "Cheems Bonk, Doge Thug Life, Hamburmgesa", "emoji": {"name": "🐕"}},
                            {"label": "Karely Ruiz HD", "value": "cat_karely", "description": "Reina VIP, Sesiones de Fotos HD", "emoji": {"name": "👑"}},
                            {"label": "Hackers & Cyberpunk", "value": "cat_hacker", "description": "Aimbot, Matrix Code, Anonymous Cyber", "emoji": {"name": "🤖"}},
                            {"label": "Memes Virales & Shitpost", "value": "cat_memes", "description": "Trollface, PopCat, Shitpost clásico", "emoji": {"name": "😂"}}
                        ]
                    }
                ]
            },
            {
                "type": 1,
                "components": [
                    {"type": 2, "style": 1, "label": "🔥 Stickers Free Fire", "custom_id": "btn_stk_ff"},
                    {"type": 2, "style": 3, "label": "🐸 Pepe & Wojak", "custom_id": "btn_stk_pepe"},
                    {"type": 2, "style": 2, "label": "🗿 GigaChad Sigma", "custom_id": "btn_stk_sigma"},
                    {"type": 2, "style": 4, "label": "🎲 Sticker Random", "custom_id": "btn_stk_random"}
                ]
            }
        ]

        r_post = requests.post(
            f"https://discord.com/api/v10/channels/{stickers_ch_id}/messages",
            headers=headers,
            json={"embeds": [embed_stickers], "components": components_stickers}
        )
        print(f"Publicación Sticker Hub: HTTP {r_post.status_code}")

    # Publicar Hub en Canal de Soundboard 500 Voces
    if soundboard_ch_id:
        embed_sound = {
            "title": "🔊 REPRODUCTOR SOUNDBOARD: 500 VOCES DE FREE FIRE",
            "description": (
                "¡Sistema Oficial de Soundboard con **500 Voces y Audios Épicos** para llamadas de voz!\n\n"
                "🎙️ **En la pestaña Soundboard de Discord:**\n"
                "Ya tienes disponibles directamente en el drawer oficial de llamadas los sonidos de:\n"
                "• `agarrate`\n"
                "• `donato_headshot` 🎯\n"
                "• `zelika_insano` 🔥\n"
                "• `hacker_aimbot` 🤖\n"
                "• `gang_freefire` 👑\n"
                "• `booyah_epico` 🏆\n"
                "• `gloo_360` 🛡️\n"
                "• `mp40_cobra` 🐍\n\n"
                "⚡ **Catálogo Extendido de 500 Voces en Vivo:**\n"
                "Selecciona abajo la categoría que deseas reproducir en el canal de voz:\n"
                "🎯 **1 al 100:** The Donato & Gritos Virales\n"
                "🔥 **101 al 200:** Zelika & Jugadas Insanas\n"
                "🤖 **201 al 300:** Hackers & Aimbot Todo Rojo\n"
                "👑 **301 al 400:** El Gang de Free Fire & Escuadra\n"
                "🏆 **401 al 500:** Booyah Magistral, Pared Gloo & Armas\n\n"
                "💬 *También puedes escribir `!voz [1-500]` o `/voz [1-500]` para reproducir cualquiera al instante.*"
            ),
            "color": 0xE74C3C,
            "image": {"url": "https://images.unsplash.com/photo-1542751371-adc38448a05e?q=80&w=1200&auto=format&fit=crop"},
            "footer": {"text": "Soundboard 500 Voces • Desarrollado por rafamodzyt • SHADOW BLOCK"}
        }

        components_sound = [
            {
                "type": 1,
                "components": [
                    {
                        "type": 3,
                        "custom_id": "select_voice_category",
                        "placeholder": "🎙️ Selecciona qué voz reproducir en llamada (1-500)...",
                        "options": [
                            {"label": "🎯 The Donato (Voces 1 a 100)", "value": "voice_cat_donato", "description": "Headshot pa tu casa crack, Risa demente, Watafac"},
                            {"label": "🔥 Zelika Insano (Voces 101 a 200)", "value": "voice_cat_zelika", "description": "Movimiento insano 360, Pared Gloo agachado flash"},
                            {"label": "🤖 Hackers & Aimbot (Voces 201 a 300)", "value": "voice_cat_hackers", "description": "Aimbot 100% todo rojo, Bypass antiban, Vuelo"},
                            {"label": "👑 El Gang de Free Fire (Voces 301 a 400)", "value": "voice_cat_gang", "description": "El Gang dominando partida, Rushea por izquierda"},
                            {"label": "🏆 Booyah & Armas (Voces 401 a 500)", "value": "voice_cat_booyah", "description": "Booyah victoria legendaria, MP40 Cobra, M1887"}
                        ]
                    }
                ]
            },
            {
                "type": 1,
                "components": [
                    {"type": 2, "style": 4, "label": "🎯 Donato Headshot", "custom_id": "play_snd_donato"},
                    {"type": 2, "style": 1, "label": "🔥 Zelika Insano", "custom_id": "play_snd_zelika"},
                    {"type": 2, "style": 2, "label": "🤖 Hacker Aimbot", "custom_id": "play_snd_hacker"},
                    {"type": 2, "style": 3, "label": "👑 Gang Free Fire", "custom_id": "play_snd_gang"},
                    {"type": 2, "style": 2, "label": "🏆 Booyah Épico", "custom_id": "play_snd_booyah"}
                ]
            }
        ]

        r_sound = requests.post(
            f"https://discord.com/api/v10/channels/{soundboard_ch_id}/messages",
            headers=headers,
            json={"embeds": [embed_sound], "components": components_sound}
        )
        print(f"Publicación Soundboard Hub: HTTP {r_sound.status_code}")

    # Guardar IDs de canales en archivo para el bot y el panel
    with open("channels_config.json", "w", encoding="utf-8") as f:
        json.dump({
            "stickers_channel_id": stickers_ch_id,
            "soundboard_channel_id": soundboard_ch_id
        }, f, indent=4)
    print("Canales configurados y guardados con éxito.")

if __name__ == "__main__":
    setup_all()
