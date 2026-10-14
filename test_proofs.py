import os
import requests
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("ADMIN_BOT_TOKEN")
WEBHOOK_URL = os.getenv("WEBHOOK_URL")
GUILD_ID = os.getenv("GUILD_ID")

headers = {
    "Authorization": f"Bot {TOKEN}",
    "Content-Type": "application/json"
}

# 1. Enviar prueba a canal de bienvenida 1559359413402472488
welcome_ch = "1559359413402472488"
embed_welcome = {
    "title": "✅ PRUEBA EN VIVO: Sistema de Bienvenidas y Administración",
    "description": (
        "✨ **Prueba de canal confirmada exitosamente.**\n\n"
        "👑 **Creador:** `rafamodzyt`\n"
        "🔗 **Servidor:** https://discord.gg/dc5HAzAMmg\n"
        "🎮 **Panel C++ DX11 Win32:** Compilado y listo para gestión en tiempo real."
    ),
    "color": 0x5865F2,
    "footer": {"text": "Sistema Shadow Block • Bot Administrador Online"}
}
res1 = requests.post(f"https://discord.com/api/v10/channels/{welcome_ch}/messages", headers=headers, json={"embeds": [embed_welcome]})
print(f"Canal Bienvenida ({welcome_ch}): HTTP {res1.status_code}")

# 2. Enviar prueba a canal de control 1559826233620168734
control_ch = "1559826233620168734"
embed_control = {
    "title": "⚡ PRUEBA EN VIVO: Erick x 24/7 & Panel DX11 Conectado",
    "description": (
        "🎙️ **Bot de Voz 24/7:** Activo en canal `General` (Meta 1,000,000 Horas)\n"
        "💻 **Panel C++ DX11:** `DiscordAdminPanel.exe` activo con pestañas de Canales, Voz, Alertas, Roles y Moderación.\n"
        "👑 **Desarrollado para:** `rafamodzyt`"
    ),
    "color": 0x2ECC71,
    "footer": {"text": "Panel C++ DirectX 11 Win32 • Estado Online"}
}
res2 = requests.post(f"https://discord.com/api/v10/channels/{control_ch}/messages", headers=headers, json={"embeds": [embed_control]})
print(f"Canal Control ({control_ch}): HTTP {res2.status_code}")

# 3. Enviar prueba via Webhook
if WEBHOOK_URL:
    res3 = requests.post(WEBHOOK_URL, json={
        "content": "🚀 **[PRUEBA EN VIVO]** El Panel C++ DirectX 11 Win32 ha sido compilado exitosamente y está listo para administrar Canales, Voz, Alertas y Roles desde el escritorio. Creado por **rafamodzyt**.",
        "username": "RafaMoDzYT Panel DX11"
    })
    print(f"Webhook: HTTP {res3.status_code}")
