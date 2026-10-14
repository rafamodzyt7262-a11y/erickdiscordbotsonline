# 🤖 Suite de Bots Discord - SHADOW BLOCK (24/7)

Sistema completo de bots para Discord diseñado para estar **Online 24/7 sin apagarse jamás**, con sistema de conteo hacia **1,000,000 de horas en voz**, control total del servidor (canales, roles, moderación), sistema automático de bienvenidas y despedidas, y soporte para Webhooks.

👑 **Creador:** `rafamodzyt`  
🌐 **Servidor de Discord Oficial:** [https://discord.gg/dc5HAzAMmg](https://discord.gg/dc5HAzAMmg)  
🏠 **Servidor ID:** `1350706770527653989` (SHADOW BLOCK)

---

## 👥 Resumen de los 2 Bots

| Bot | App ID | Función Principal | Estado |
|---|---|---|---|
| **Erick x** | `1559437873265119252` | 🎙️ Voz 24/7 continua & Meta de **1,000,000 de horas**, foto de Karely Ruiz y personalización | 🟢 ONLINE 24/7 |
| **Bot Administrador** | `1559830923174744125` | 🛡️ Control del servidor: Canales, Roles, Moderación, Bienvenidas y Despedidas automáticas | 🟢 ONLINE 24/7 |

---

## 🚀 Bot 2: Administrador y Bienvenidas (RafaMoDzYT)

- **Canal de Bienvenidas y Despedidas:** `<#1559359413402472488>` (`bienvenida-☺️`)
- **Webhook Integrado:** Envía mensajes oficiales a `#general` vía webhook.
- **Permisos:** Administrador total en el servidor.

### 📋 Comandos del Bot Administrador (Prefijo `//` o `/`)

#### 👋 Sistema de Bienvenidas y Despedidas
- `//testbienvenida`: Envía un mensaje de bienvenida de prueba en `<#1559359413402472488>` con embed, avatar, conteo de miembros y botón oficial.
- `//testdespedida`: Envía un mensaje de despedida de prueba.
- `//setbienvenida <#canal>`: Cambia el canal donde se enviarán los avisos de bienvenida.

#### 📁 Control y Gestión de Canales
- `//crearcanal <texto|voz> <nombre>`: Crea un canal de texto o de voz con categoría opcional.
- `//borrarcanal [canal]`: Elimina un canal.
- `//renombrarcanal <nuevo_nombre>`: Renombra el canal.
- `//bloquear` (`//lock`): Bloquea el canal para que miembros normales no puedan escribir.
- `//desbloquear` (`//unlock`): Desbloquea el canal.
- `//lento <segundos>` (`//slowmode`): Establece el modo lento (cooldown entre mensajes).
- `//tema <texto>`: Cambia la descripción o tema del canal.
- `//clonar`: Clona un canal con exactamente los mismos permisos y ajustes.

#### 🎭 Control y Gestión de Roles
- `//crearrol <nombre> [#color_hex]`: Crea un nuevo rol (ej: `//crearrol VIP #FFD700`).
- `//borrarrol <@rol>`: Elimina un rol.
- `//darrol <@usuario> <@rol>`: Asigna un rol a un miembro.
- `//quitarrol <@usuario> <@rol>`: Remueve un rol a un miembro.
- `//colorrol <@rol> <#color_hex>`: Cambia el color de un rol.
- `//renombrarrol <@rol> <nuevo_nombre>`: Renombra un rol.
- `//roles`: Muestra la lista de todos los roles del servidor y cuántos miembros los tienen.

#### 🔨 Moderación y Mensajería
- `//limpiar <1-100>` (`//clear` / `//purge`): Borra entre 1 y 100 mensajes del chat.
- `//kick <@usuario> [razon]`: Expulsa a un miembro.
- `//ban <@usuario> [razon]`: Banea a un miembro.
- `//unban <id_usuario>`: Desbanea a un usuario por su ID.
- `//mutear <@usuario> <minutos> [razon]`: Aísla temporalmente a un usuario.
- `//desmutear <@usuario>`: Quita el aislamiento.
- `//anuncio <#canal> <titulo> | <mensaje> | [#color]`: Envía un anuncio decorado.
- `//webhook <mensaje>`: Envía un mensaje oficial utilizando tu Webhook de Discord.
- `//servidor`: Muestra estadísticas detalladas del servidor SHADOW BLOCK.
- `//ping`: Muestra la latencia del bot en milisegundos.
- `//ayuda`: Abre el menú interactivo de ayuda.

---

## 🎙️ Bot 1: Erick x (Voz 24/7 & 1M de Horas)

- **Canal de Voz 24/7:** `<#1350706770527653993>` (General)
- **Canal de Control:** `<#1559826233620168734>`
- **Meta:** 1,000,000 de horas acumuladas con guardado persistente en `data/stats.json`.
- **Foto de Perfil:** Karely Ruiz HD (`karely_ruiz_avatar.jpg`).

### Comandos de Erick x:
- `//horas`: Muestra la barra de progreso hacia las 1,000,000 de horas.
- `//avatar <url o adjunto>`: Cambia la foto del bot.
- `//nombre <nuevo nombre>`: Cambia el nombre global.
- `//apodo <nuevo apodo>`: Cambia el apodo en el servidor.
- `//estado <online|idle|dnd|invisible>`: Cambia el estado de conexión.
- `//actividad <jugando|viendo|escuchando|compitiendo> <texto>`: Cambia la actividad.
- `//stream <texto>`: Activa modo transmisión morado con enlace a Twitch.
- `//conectar` y `//desconectar`: Control de voz 24/7.
- `//perfil`: Tarjeta oficial con créditos a **rafamodzyt**.

---

## ⚙️ Configuración en Discord Developer Portal

Para que las **bienvenidas automáticas** se envíen cuando un miembro entra al servidor:

1. Entra a **[Discord Developer Portal - Bot Administrador](https://discord.com/developers/applications/1559830923174744125/bot)**.
2. Baja a la sección **"Privileged Gateway Intents"**.
3. Activa los interruptores:
   - ✅ **Server Members Intent** *(Necesario para detectar cuando alguien entra o sale)*.
   - ✅ **Message Content Intent** *(Para leer comandos con prefijo `//`)*.
4. Haz clic en **Save Changes**.
5. En tu archivo `.env`, puedes colocar:
   ```env
   ENABLE_MEMBERS_INTENT=true
   ENABLE_MESSAGE_CONTENT=true
   ```

---

## ☁️ Despliegue en Railway (Ambos Bots 24/7 Juntos)

El archivo `run_all.py` se encarga de iniciar y supervisar **ambos bots al mismo tiempo** bajo una sola instancia en Railway:

1. Ve a **[railway.app](https://railway.app/)** y crea un proyecto importando tu repositorio de GitHub.
2. En la pestaña **"Variables"** de Railway, copia todas las variables de tu archivo `.env`:
   - `DISCORD_TOKEN`
   - `APPLICATION_ID`
   - `ADMIN_BOT_TOKEN`
   - `ADMIN_BOT_APP_ID`
   - `WELCOME_CHANNEL_ID`
   - `WEBHOOK_URL`
   - `SERVER_LINK`
   - `GUILD_ID`
   - `VOICE_CHANNEL_ID`
   - `CONTROL_CHANNEL_ID`
   - `CREATOR_NAME` = `rafamodzyt`
   - `PORT` = `8080`
3. Railway ejecutará `python run_all.py` mediante el `Procfile` y mantendrá ambos bots online de forma continua y perpetua.
