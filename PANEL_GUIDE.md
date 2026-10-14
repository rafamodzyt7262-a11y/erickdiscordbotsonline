# 🎮 Panel C++ DirectX 11 Win32 - Discord Administrator & Voice Manager

Desarrollado para **rafamodzyt**  
**Servidor Objetivo:** `SHADOW BLOCK` (`1350706770527653989`)  
**Enlace de Invitación:** https://discord.gg/dc5HAzAMmg

---

## ⚡ 1. ¿Cómo Iniciar el Panel?
Simplemente ejecuta con doble clic el archivo:
- [`iniciar_panel.bat`](file:///d:/Discord%20Bots%20erick/iniciar_panel.bat)
O directamente el ejecutable nativo compilado:
- [`panel_cpp/DiscordAdminPanel.exe`](file:///d:/Discord%20Bots%20erick/panel_cpp/DiscordAdminPanel.exe)

*(Si realizas modificaciones al código C++, puedes recompilar en 5 segundos ejecutando [`panel_cpp/build.bat`](file:///d:/Discord%20Bots%20erick/panel_cpp/build.bat)).*

---

## 📑 2. Estructura de las 12 Pestañas del Panel

### 📁 1. Pestaña: Canales & Salas
- **Creación en vivo:** Canales de Texto (`0`), Canales de Voz (`2`) y Categorías (`4`) con nombre, topic y slowmode configurables.
- **Administración:** Renombrar canales existentes, bloquear (`Lock`) permisos de envío para `@everyone`, desbloquear (`Unlock`), configurar el modo lento (slowmode) y eliminar canales.

### 💬 2. Pestaña: Chat en Vivo & Canales (Split View)
- **Navegador de Canales (Izquierda):** Lista de todos los canales de texto y voz del servidor. Al hacer clic en cualquiera, carga el chat en tiempo real.
- **Historial de Chat (Derecha):** Lectura directa de los mensajes recientes de Discord (`[Autor]: Mensaje`).
- **Compositor de Mensajes con Colores:**
  - `⚪ Normal`
  - `🔴 ANSI Rojo`
  - `🟢 ANSI Verde`
  - `🔵 ANSI Azul`
  - `🟡 ANSI Amarillo`
  - `🟣 ANSI Magenta`
  - `💎 ANSI Cyan`
  - `🌈 RGB Rainbow Embed`
  *(Los mensajes se envían formateados con bloques ANSI de Discord para verse en colores vivos).*

### 🎙️ 3. Pestaña: Voz 24/7 & 1M Horas
- **Monitoreo de Erick x:** Conexión continua en `General` (`1350706770527653993`) con foto de Karely Ruiz HD.
- **Ecualizador de Audio Animado:** 22 barras DX11 con oscilador senoidal en tiempo real.
- **Barra de Progreso:** Visualización del camino hacia la meta de **1,000,000 de horas**.

### 📢 4. Pestaña: Alertas & Anuncios
- Editor RGB interactivo de embeds oficiales y disparador de Webhook a `#general`.

### 🛡️ 5. Pestaña: Moderación & Roles
- Purgado masivo de mensajes (1 a 100), Expulsión (`Kick`), Baneo (`Ban`), Desbaneo (`Unban`), y Aislamiento (`Timeout`).
- Creador de roles con selector de color y asignador rápido.

### 🎨 6. Pestaña: Stickers & Memes (300+)
- Catálogo clasificado: Pepe, Wojaks, GigaChad, Cheems, Karely Ruiz, Streamers, Anime y Emojis Gigantes.
- Envío directo a cualquier canal con un solo clic.

### 🔊 7. Pestaña: Soundboard & Free Fire Audios (300+)
- **Líneas de Voz Free Fire:** *¡Primera Sangre!*, *¡Doble Asesinato!*, *¡Triple Asesinato!*, *¡Cuádruple Asesinato!*, *¡BOOYAH!*, *AWM Headshot*, *MP40 Cobra*, *Pared Gloo*, *Alok Drop the Beat*, *Chrono Escudo*, *Wukong Arbusto*, *Airdrop*, etc.
- **Memes & Gaming:** *GigaChad Theme*, *Vine Boom*, *Bruh*, *Airhorn*, *Coffin Dance*, *Emotional Damage*, *Metal Pipe*, *Siuuu Cristiano*, etc.
- **Acciones:** Transmitir en llamada de voz por `Erick x`, enviar tarjeta sonora al chat o guardar permanente en el servidor.

### 👥 8. Pestaña: Miembros (Cuadritos en Tiempo Real)
- **Grid de Cuadritos:** Cada miembro se representa en un cuadro/tarjeta visual ("cuadrito") con:
  - Indicador LED de estado: `🟢 ONLINE` o `⚫ OFFLINE`.
  - Apodo y Nombre de usuario.
  - Insignia de Roles actuales.
  - Botón directo `⚙️ Administrar`.
- **Botón "⚡ Auto-Asignar Rol Member a Todos":** Asigna automáticamente el rol `Member` a todos los usuarios del servidor que no lo tengan.
- **Inspector de Perfil:** Modificar apodo directamente en Discord (vía REST PATCH), asignar/quitar roles, sanciones rápidas.

### 🖼️ 9. Pestaña: Wallpapers 4K HD Masivo (99,999+ Únicos)
- **Configuración Predeterminada:** Envío automático de **100 wallpapers 4K cada 25 minutos**.
- **Motor 99,999+:** Generador con semillas e IDs únicos. No se repite ninguna imagen.
- **Ráfaga Manual Inmediata:** Botón `🚀 Enviar Ráfaga de 100 Wallpapers 4K Ahora`.

### 🎫 10. Pestaña: Tienda & Tickets
- Monitoreo del canal `🎫・comprar-panel-y-bots` con botones de compra interactivos.

### 📜 11. Pestaña: Consola en Vivo
- Registro con marcas de tiempo y códigos HTTP (200, 201, 204) de cada acción.

### ⚙️ 12. Pestaña: Configuración & Sistema
- Reloj digital en vivo en la barra superior con indicador LED verde palpitante.
- Edición y verificación de tokens y credenciales.

---

## 🛰️ 3. Estado de los Bots en Segundo Plano
1. **Erick x (Bot 1):** Conectado 24/7 en voz `General` con auto-reconexión permanente.
2. **Bot Administrador (Bot 2):** Conectado al Gateway, ejecutando el ciclo de 100 wallpapers cada 25 min, asignando rol Member automáticamente y atendiendo tickets.
