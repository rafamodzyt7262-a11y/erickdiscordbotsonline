# -*- coding: utf-8 -*-
import sys
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    except Exception:
        pass

import os
import shutil

BASE_DIR = r"d:\Discord Bots erick"
RAILWAY_DIR = os.path.join(BASE_DIR, "railway_deploy")
EXE_DIR = os.path.join(BASE_DIR, "exe_pa_compartir")

os.makedirs(RAILWAY_DIR, exist_ok=True)
os.makedirs(EXE_DIR, exist_ok=True)

# 1. Copiar archivos a railway_deploy
railway_files = [
    "main.py",
    "admin_bot.py",
    "config.py",
    "keep_alive.py",
    "stats_manager.py",
    "wallpapers_data.py",
    "stickers_catalog.py",
    "stickers_catalog_9999.py",
    "freefire_voices_500.py",
    "requirements.txt",
    "Procfile",
    "railway.json",
    "nixpacks.toml",
    "Dockerfile",
    "run_all.py",
    ".env.example",
    ".gitignore"
]

print("Copiando archivos a railway_deploy/...")
for f in railway_files:
    src_f = os.path.join(BASE_DIR, f)
    if os.path.exists(src_f):
        shutil.copy2(src_f, os.path.join(RAILWAY_DIR, f))
        print(f" [OK] {f}")
    else:
        print(f" [AVISO] No se encontro {f}")

# Copiar carpeta data/ inicial si existe
data_dir = os.path.join(BASE_DIR, "data")
if os.path.exists(data_dir):
    shutil.copytree(data_dir, os.path.join(RAILWAY_DIR, "data"), dirs_exist_ok=True)
    print(" [OK] carpeta data/")

# Crear README para Railway y GitHub
readme_railway = """# 🚀 SHADOW BLOCK - BOTS DE DISCORD 24/7 (RAILWAY & GITHUB)
**Desarrollado y Creado por rafamodzyt**

Este repositorio contiene el sistema multi-bot completo para mantenerse **ONLINE 24/7 sin interrupciones** desplegado en **Railway** o cualquier servidor en la nube.

---

## 🤖 ¿Qué bots incluye este proyecto?
1. **Bot 1: Erick x (Voz 24/7 & 1 Millón de Horas):**
   - Se mantiene conectado en canal de voz 24/7 sin desconectarse.
   - Sistema de reconexión automática ante caídas de internet.
   - Servidor web keep-alive integrado para UptimeRobot / Railway.

2. **Bot 2: SatanasMiPadre (Administrador, Free Fire & Bienvenidas):**
   - Sistema de Bienvenidas y Despedidas automáticas con embeds y avatares.
   - **Game Bots:** Matchmaking con bots de Free Fire para subir de rango (SUR, NORTE, EEUU).
   - **Send Reports:** 55 Reportes automáticos en 12 segundos con Blacklist.
   - **Wallpapers 4K Masivo:** Envío de fondos cada 25 minutos (PC y Móvil).
   - **9,999 Stickers & Memes:** Comandos y catálogo interactivo.
   - **500 Voces de Free Fire:** Donato, Zelika, Hackers, El Gang y Booyah.
   - Tienda de Tickets y Moderación Completa.

---

## 🛠️ PASOS PARA SUBIR A GITHUB Y RAILWAY (24/7 NUNCA SE APAGA)

### Paso 1: Subir a GitHub
1. Entra a [GitHub.com](https://github.com) y crea un nuevo repositorio (puedes llamarlo `discord-bots-shadowblock`).
2. Sube todos los archivos que están dentro de esta carpeta `railway_deploy/`.
3. *(Opcional)* Si usas Git por consola:
   ```bash
   git init
   git add .
   git commit -m "Deploy 24/7 bots rafamodzyt"
   git branch -M main
   git remote add origin https://github.com/TU_USUARIO/TU_REPOSITORIO.git
   git push -u origin main
   ```

### Paso 2: Desplegar en Railway
1. Ve a [Railway.app](https://railway.app) e inicia sesión con tu cuenta de GitHub.
2. Haz clic en **"New Project"** -> **"Deploy from GitHub repo"**.
3. Selecciona tu repositorio recién creado.
4. En la pestaña **"Variables"** de Railway, agrega las siguientes variables de entorno:
   - `DISCORD_TOKEN` = Tu token del Bot 1
   - `APPLICATION_ID` = 1559437873265119252
   - `ADMIN_BOT_TOKEN` = Tu token del Bot 2
   - `ADMIN_BOT_APP_ID` = 1559830923174744125
   - `GUILD_ID` = 1350706770527653989
   - `VOICE_CHANNEL_ID` = 1350706770527653993
   - `CONTROL_CHANNEL_ID` = 1559826233620168734
   - `WELCOME_CHANNEL_ID` = 1559359413402472488
   - `COMMAND_PREFIX` = //
   - `CREATOR_NAME` = rafamodzyt
   - `PORT` = 8080
5. ¡Listo! Railway detectará automáticamente el archivo `Procfile` y ejecutará `python run_all.py`. Los bots estarán online **24/7 permanentemente** sin necesidad de tener tu PC encendida.

---
👑 **Créditos:** Proyecto oficial creado para rafamodzyt • SHADOW BLOCK
"""

with open(os.path.join(RAILWAY_DIR, "README.md"), "w", encoding="utf-8") as f:
    f.write(readme_railway)
print(" [OK] README.md para Railway creado")

# 2. Copiar archivos a exe_pa_compartir
print("\nCopiando archivos a exe_pa_compartir/...")
src_exe = os.path.join(BASE_DIR, "panel_cpp", "DiscordAdminPanel.exe")
dst_exe = os.path.join(EXE_DIR, "DiscordAdminPanel.exe")
if os.path.exists(src_exe):
    shutil.copy2(src_exe, dst_exe)
    print(f" [OK] DiscordAdminPanel.exe ({os.path.getsize(dst_exe)} bytes)")
else:
    print(" [ERROR] No se encontro DiscordAdminPanel.exe")

# Launcher bat
bat_content = """@echo off
title Panel Discord C++ DX11 - rafamodzyt
cd /d "%~dp0"
echo Iniciando Discord Admin Panel DirectX 11...
start "" "DiscordAdminPanel.exe"
exit
"""
with open(os.path.join(EXE_DIR, "ABRIR_PANEL.bat"), "w", encoding="utf-8") as f:
    f.write(bat_content)
print(" [OK] ABRIR_PANEL.bat creado")

# Instrucciones para amigos
instrucciones_amigos = """========================================================
   PANEL ADMINISTRADOR DISCORD C++ DIRECTX 11 WIN32
         Desarrollado y Creado por rafamodzyt
               Servidor Oficial: SHADOW BLOCK
========================================================

¡Hola crack! Este es el ejecutable oficial del Panel de Control de Discord 
programado en C++ nativo y renderizado a 60 FPS con DirectX 11 y Dear ImGui.

---
🚀 ¿COMO ABRIRLO?
1. Simplemente haz doble clic en "ABRIR_PANEL.bat" o directamente en "DiscordAdminPanel.exe".
2. No requiere instalar nada ni librerías pesadas, funciona de inmediato en Windows 10 y Windows 11.

---
🌟 CARACTERISTICAS DEL PANEL:
• [#] Canales & Salas: Administra y crea canales de texto, voz y categorías en 1 clic.
• [CHAT] Chat en Vivo Split: Vista dividida de chat con colores RGB y formato ANSI.
• [VOZ] Voz 24/7 & 1M Horas: Control de permanencia y ecualizador gráfico en vivo.
• [!] Alertas & Anuncios: Envío de embeds decorados con banner y alertas masivas.
• [*] Moderacion & Roles: Kick, ban, mute temporal y administración de roles.
• [MEMES] Stickers 300+ y 9,999: Buscador de memes y stickers en HD listos para enviar.
• [AUDIO] Soundboard Free Fire: 500 Voces de Donato, Zelika, Hackers, El Gang y Booyah.
• [USERS] Miembros en Cuadritos: Grid visual de todos los usuarios con luces LED online/offline.
• [WALLPAPERS] 4K HD Masivo: Ráfagas de 100 wallpapers cada 25 minutos para PC y Móvil.
• [TIENDA] Tickets de Compra: Gestión de soporte y ventas VIP.
• [>] Consola en Vivo: Registro en tiempo real de todos los eventos del servidor.

---
👑 CREDITOS & CONTACTO:
• Creador Oficial: rafamodzyt
• Servidor de Discord: https://discord.gg/EFz8NB99N4
========================================================
"""

with open(os.path.join(EXE_DIR, "INSTRUCCIONES_AMIGOS.txt"), "w", encoding="utf-8") as f:
    f.write(instrucciones_amigos)
print(" [OK] INSTRUCCIONES_AMIGOS.txt creado")

# Copiar live_members.json inicial para que el panel tenga datos precargados si no hay red
src_members = os.path.join(BASE_DIR, "live_members.json")
if os.path.exists(src_members):
    shutil.copy2(src_members, os.path.join(EXE_DIR, "live_members.json"))
    print(" [OK] live_members.json")

print("\n🎉 Ambas carpetas creadas y organizadas con éxito:")
print(f" 📁 Railway & GitHub: {RAILWAY_DIR}")
print(f" 📁 Compartir con Amigos: {EXE_DIR}")
