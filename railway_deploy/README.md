# 🚀 SHADOW BLOCK - BOTS DE DISCORD 24/7 (RAILWAY & GITHUB)
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
