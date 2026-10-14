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

def create_or_get_channel(name, ch_type=0, topic="", permission_overwrites=None, parent_id=None):
    r = requests.get(f"https://discord.com/api/v10/guilds/{GUILD_ID}/channels", headers=headers)
    if r.status_code == 200:
        for c in r.json():
            if c.get("name") == name:
                print(f"Canal ya existente: {name} (ID: {c.get('id')})")
                return c.get("id")

    payload = {
        "name": name,
        "type": ch_type,
        "topic": topic
    }
    if permission_overwrites:
        payload["permission_overwrites"] = permission_overwrites
    if parent_id:
        payload["parent_id"] = parent_id

    cr = requests.post(f"https://discord.com/api/v10/guilds/{GUILD_ID}/channels", headers=headers, json=payload)
    if cr.status_code in (200, 201):
        data = cr.json()
        print(f"Canal creado con éxito: {name} (ID: {data['id']})")
        return data["id"]
    else:
        print(f"Error creando {name}: HTTP {cr.status_code} - {cr.text}")
        return None

def main():
    print("--- Configurando Canales GAME BOTS y SEND REPORTS ---")
    
    # Overwrites para que TODOS vean pero NADIE escriba (solo bots/interacción)
    # allow: VIEW_CHANNEL (1024), READ_MESSAGE_HISTORY (65536)
    # deny: SEND_MESSAGES (2048), ADD_REACTIONS (64)
    everyone_role_id = GUILD_ID
    overwrites_readonly = [
        {
            "id": everyone_role_id,
            "type": 0, # role
            "allow": "66560", # 1024 | 65536
            "deny": "2112"    # 2048 | 64
        }
    ]

    # Overwrites para canal de voz (todos ven y entran pero no hablan)
    # deny: SPEAK (2097152)
    overwrites_voice = [
        {
            "id": everyone_role_id,
            "type": 0,
            "allow": "1049600", # VIEW_CHANNEL | CONNECT
            "deny": "2097152"   # SPEAK
        }
    ]

    # 1. Canal de voz GAME BOTS
    vc_id = create_or_get_channel(
        name="🔊・GAME BOTS (MUTED)",
        ch_type=2, # Voice
        permission_overwrites=overwrites_voice
    )

    # 2. Canal de texto GAME BOTS
    game_bots_ch_id = create_or_get_channel(
        name="🤖・game-bots",
        ch_type=0, # Text
        topic="Sistema de Emparejamiento con Cuentas Bot de Free Fire para subir de rango rápido • rafamodzyt",
        permission_overwrites=overwrites_readonly
    )

    # 3. Canal de texto SEND REPORTS
    send_reports_ch_id = create_or_get_channel(
        name="🚨・send-reports",
        ch_type=0, # Text
        topic="Sistema Automatizado de 55 Reportes y Cola de Blacklist Free Fire en 12 segundos • rafamodzyt",
        permission_overwrites=overwrites_readonly
    )

    # Publicar Mensaje Interactivo en 🤖・game-bots
    if game_bots_ch_id:
        embed_game_bots = {
            "title": "🎮 SISTEMA OFICIAL: EMPAREJAMIENTO CON BOTS FREE FIRE",
            "description": (
                "¡Bienvenido a la herramienta de **Emparejamiento con Bots** de **SHADOW BLOCK**!\n\n"
                "⚡ **¿Cómo funciona este sistema?**\n"
                "• Este bot conecta tu cuenta en partidas de escuadra con **cuentas bots automáticas**.\n"
                "• Permite subir de rango (Heroico / Gran Maestro) de forma acelerada y segura.\n"
                "• Solo debes ingresar tu **ID de jugador** y elegir tu **Región**.\n\n"
                "🌐 **Regiones Válidas Permitidas:**\n"
                "• `SUR` (Sudamérica)\n"
                "• `NORTE` (Norteamérica)\n"
                "• `EEUU` (Estados Unidos / US)\n\n"
                "⚠️ **Límite y Alerta del Sistema:**\n"
                "• **Bots disponibles por día:** Máximo **55 cuentas bots** por usuario.\n"
                "• El sistema generará el nombre del equipo y los nombres de las cuentas bots asignadas.\n\n"
                "👇 *Presiona el botón abajo para iniciar tu emparejamiento.*"
            ),
            "color": 0x2ECC71,
            "image": {"url": "https://images.unsplash.com/photo-1542751371-adc38448a05e?q=80&w=1200&auto=format&fit=crop"},
            "footer": {"text": "Sistema de Matchmaking Bots • Creado por rafamodzyt • SHADOW BLOCK"}
        }

        components_game_bots = [
            {
                "type": 1,
                "components": [
                    {
                        "type": 2,
                        "style": 3, # Success (Verde)
                        "label": "🎮 Iniciar Emparejamiento con Bots",
                        "emoji": {"name": "🤖"},
                        "custom_id": "btn_game_bots_match"
                    },
                    {
                        "type": 2,
                        "style": 2, # Secondary (Gris)
                        "label": "📊 Ver Cuentas Bots Disponibles (55)",
                        "emoji": {"name": "⚡"},
                        "custom_id": "btn_game_bots_info"
                    }
                ]
            }
        ]

        r1 = requests.post(
            f"https://discord.com/api/v10/channels/{game_bots_ch_id}/messages",
            headers=headers,
            json={"embeds": [embed_game_bots], "components": components_game_bots}
        )
        print(f"Panel en #game-bots publicado: HTTP {r1.status_code}")

    # Publicar Mensaje Interactivo en 🚨・send-reports
    if send_reports_ch_id:
        embed_send_reports = {
            "title": "🚨 SISTEMA DE REPORTES MASIVOS FREE FIRE (55 REPORTES / 12 SEG)",
            "description": (
                "¡Herramienta oficial para procesar **55 reportes automáticos en 12 segundos**!\n\n"
                "⚡ **Información del Sistema de Reportes:**\n"
                "• Este bot despliega una red de **55 cuentas bots con nombres aleatorios**.\n"
                "• Envía ráfagas sincronizadas de reportes a la ID de la cuenta objetivo.\n"
                "• Diseñado para aplicar **Blacklist inmediata** y congelar/bugear el rango del objetivo.\n"
                "• Tiempo de procesamiento garantizado: exactamente **12 segundos**.\n\n"
                "🌐 **Regiones Soportadas:**\n"
                "• `SUR` | `NORTE` | `EEUU`\n\n"
                "⚙️ **¿Cómo usar el Bot de Reportes?**\n"
                "1. Toca el botón **'Enviar 55 Reportes'** abajo.\n"
                "2. Escribe la **ID de la cuenta objetivo** y selecciona tu **Región**.\n"
                "3. Verás en vivo cómo cargan las **55 cuentas bots** enviando cada reporte.\n"
                "4. Al finalizar los 12 segundos recibirás el comprobante con los créditos oficiales.\n\n"
                "👑 **Créditos Oficiales:** `rafamodzyt`"
            ),
            "color": 0xE74C3C,
            "image": {"url": "https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?q=80&w=1200&auto=format&fit=crop"},
            "footer": {"text": "Bot de Reportes & Blacklist • Hecho por rafamodzyt • SHADOW BLOCK"}
        }

        components_send_reports = [
            {
                "type": 1,
                "components": [
                    {
                        "type": 2,
                        "style": 4, # Danger (Rojo)
                        "label": "🚨 Enviar 55 Reportes (12 Segundos)",
                        "emoji": {"name": "⚡"},
                        "custom_id": "btn_send_reports_modal"
                    },
                    {
                        "type": 2,
                        "style": 1, # Primary (Azul)
                        "label": "🛡️ Estado del Servidor & Blacklist",
                        "emoji": {"name": "📜"},
                        "custom_id": "btn_send_reports_status"
                    }
                ]
            }
        ]

        r2 = requests.post(
            f"https://discord.com/api/v10/channels/{send_reports_ch_id}/messages",
            headers=headers,
            json={"embeds": [embed_send_reports], "components": components_send_reports}
        )
        print(f"Panel en #send-reports publicado: HTTP {r2.status_code}")

    print("🎉 Canales y paneles interactivos creados exitosamente.")

if __name__ == "__main__":
    main()
