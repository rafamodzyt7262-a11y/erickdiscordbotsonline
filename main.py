import asyncio
import io
import os
import sys
import time

# Configurar codificación UTF-8 en consola de Windows
if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

import aiohttp
import discord
from discord.ext import commands, tasks
from discord.ui import Button, View

import config
from stats_manager import StatsManager
from keep_alive import start_keep_alive, set_bot_reference


class InviteButtonView(View):
    """Botón interactivo de Discord con el enlace oficial."""
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Button(
            label="Servidor de Discord Oficial",
            url=config.DISCORD_INVITE,
            style=discord.ButtonStyle.link,
            emoji="🚀"
        ))

def in_control_channel_or_admin():
    """Filtro: Permite ejecutar comandos solo en el canal asignado o si es Administrador."""
    async def predicate(ctx: commands.Context):
        if ctx.channel.id == config.CONTROL_CHANNEL_ID:
            return True
        if ctx.guild and ctx.author.guild_permissions.administrator:
            return True
        control_ch = ctx.guild.get_channel(config.CONTROL_CHANNEL_ID) if ctx.guild else None
        mention = control_ch.mention if control_ch else f"`{config.CONTROL_CHANNEL_ID}`"
        await ctx.send(
            f"⚠️ Este comando solo se puede usar en el canal designado: {mention}",
            ephemeral=True,
            delete_after=10
        )
        return False
    return commands.check(predicate)

class SilentAudioSource(discord.AudioSource):
    """
    Fuente de audio Opus silenciosa (paquetes oficiales Opus de 20ms = 3 bytes).
    Mantiene la conexión de voz activa 24/7 sin consumir CPU ni ancho de banda,
    y evita que Discord desconecte al bot por inactividad / timeout o lo mande a AFK.
    """
    def is_opus(self) -> bool:
        return True

    def read(self) -> bytes:
        return b'\xf8\xff\xfe'

class ErickBot(commands.Bot):
    def __init__(self, intents: discord.Intents):
        super().__init__(
            command_prefix=commands.when_mentioned_or(config.COMMAND_PREFIX),
            intents=intents,
            help_command=None
        )
        self.stats = StatsManager()
        self.auto_reconnect_enabled = True
        self.target_voice_channel_id = config.VOICE_CHANNEL_ID
        self.bot_start_time = time.time()
        self.voice_client = None
        self._connecting_lock = asyncio.Lock()
        self._reconnecting = False

    async def setup_hook(self):
        # Iniciar tareas en segundo plano
        if not self.voice_keeper_task.is_running():
            self.voice_keeper_task.start()
        if not self.stats_and_presence_task.is_running():
            self.stats_and_presence_task.start()

        # Registrar e instantanear comandos de barra diagonal en el servidor objetivo
        try:
            guild_obj = discord.Object(id=config.GUILD_ID)
            self.tree.copy_global_to(guild=guild_obj)
            await self.tree.sync(guild=guild_obj)
            print(f"[Slash Sync] Comandos sincronizados exitosamente en servidor ID: {config.GUILD_ID}", flush=True)
        except Exception as e:
            print(f"[Slash Sync] Aviso al sincronizar comandos slash: {e}", flush=True)

    def get_target_voice_channel(self) -> discord.VoiceChannel | None:
        """
        Localiza el canal de voz 'General' con máxima resiliencia y auto-descubrimiento:
        1. Comprueba target_voice_channel_id configurado si existe en el servidor.
        2. Si no, busca cualquier canal de voz cuyo nombre sea exactamente 'General' (o 'general').
        3. Si no, busca cualquier canal que contenga la palabra 'general' en minúsculas.
        4. Si no, toma el primer canal de voz disponible en el servidor.
        """
        guild = self.get_guild(config.GUILD_ID)
        if not guild and self.guilds:
            guild = self.guilds[0]

        if not guild:
            return None

        # 1. Por ID directo configurado si existe en el servidor
        if self.target_voice_channel_id:
            ch = guild.get_channel(self.target_voice_channel_id)
            if isinstance(ch, discord.VoiceChannel):
                return ch

        # 2. Por nombre exacto 'general'
        for ch in guild.voice_channels:
            if ch.name.strip().lower() == "general":
                self.target_voice_channel_id = ch.id
                return ch

        # 3. Por coincidencia parcial de 'general' (ej: 🔊・General, General 1, etc.)
        for ch in guild.voice_channels:
            if "general" in ch.name.lower():
                self.target_voice_channel_id = ch.id
                return ch

        # 4. Fallback al primer canal de voz disponible
        if guild.voice_channels:
            chosen = guild.voice_channels[0]
            self.target_voice_channel_id = chosen.id
            return chosen

        return None

    async def on_ready(self):
        print("==================================================", flush=True)
        print(f"🤖 Bot iniciado con éxito: {self.user} (ID: {self.user.id})", flush=True)
        print(f"👑 Creador: {config.CREATOR_NAME}", flush=True)
        print(f"🌐 Discord Oficial: {config.DISCORD_INVITE}", flush=True)
        print(f"🎯 Canal de Control: {config.CONTROL_CHANNEL_ID}", flush=True)
        
        target_ch = self.get_target_voice_channel()
        ch_name = f"'{target_ch.name}' ({target_ch.id})" if target_ch else f"ID: {self.target_voice_channel_id}"
        print(f"🎙️ Canal de Voz Objetivo: {ch_name}", flush=True)
        print("🔒 Modo 24/7 General Permanente: ACTIVO", flush=True)
        print("==================================================", flush=True)
        
        # Conexión inicial inmediata a voz
        await self.ensure_voice_connection()

    async def ensure_voice_connection(self):
        """Verifica y asegura la conexión continua 24/7 al canal de voz General."""
        if not self.auto_reconnect_enabled:
            return

        if self._connecting_lock.locked():
            return

        async with self._connecting_lock:
            channel = self.get_target_voice_channel()
            if not channel:
                return

            guild = channel.guild
            try:
                current_vc = guild.voice_client

                # Caso 1: Ya está conectado a voz
                if current_vc and current_vc.is_connected():
                    # Si está en un canal diferente a General, moverlo de vuelta de inmediato
                    if current_vc.channel.id != channel.id:
                        print(f"[Voz 24/7] ⚠️ Bot en canal incorrecto ('{current_vc.channel.name}'). Moviendo de vuelta a '{channel.name}'...", flush=True)
                        try:
                            await current_vc.move_to(channel)
                        except Exception as e_mv:
                            print(f"[Voz 24/7] Error moviendo a canal objetivo: {e_mv}", flush=True)

                    self.voice_client = current_vc
                    if not self.stats.is_in_voice:
                        self.stats.on_voice_connected()

                    # Transmitir flujo de silencio anti-inactividad / anti-timeout
                    if not current_vc.is_playing():
                        try:
                            current_vc.play(SilentAudioSource())
                        except Exception:
                            pass
                    return

                # Caso 2: Cliente zombie o desconectado en cache
                if current_vc:
                    print("[Voz 24/7] Limpiando cliente de voz residual previo...", flush=True)
                    try:
                        await current_vc.disconnect(force=True)
                    except Exception:
                        pass
                    await asyncio.sleep(0.5)

                # Caso 3: Conexión limpia al canal de voz General
                print(f"[Voz 24/7] Conectando a '{channel.name}' ({channel.id})...", flush=True)
                self.voice_client = await channel.connect(reconnect=True, self_deaf=True, timeout=20.0)
                self.stats.on_voice_connected()

                # Iniciar audio silencioso continuo (evita que Discord lo bote por AFK o inactividad)
                try:
                    if self.voice_client and not self.voice_client.is_playing():
                        self.voice_client.play(SilentAudioSource())
                except Exception:
                    pass

                print(f"[Voz 24/7] 🟢 Conectado exitosamente en '{channel.name}'. Anti-kick, Ensordecido y Anti-AFK activos.", flush=True)

            except discord.ClientException as e:
                err_str = str(e)
                if "Already connected" in err_str:
                    if guild.voice_client and guild.voice_client.is_connected():
                        self.voice_client = guild.voice_client
                        if self.voice_client.channel.id != channel.id:
                            await self.voice_client.move_to(channel)
                        if not self.stats.is_in_voice:
                            self.stats.on_voice_connected()
                    else:
                        try:
                            if guild.voice_client:
                                await guild.voice_client.disconnect(force=True)
                            await asyncio.sleep(0.5)
                            self.voice_client = await channel.connect(reconnect=True, self_deaf=True, timeout=20.0)
                            self.stats.on_voice_connected()
                        except Exception as e_clean:
                            print(f"[Voz 24/7] Reintento post-limpieza: {e_clean}", flush=True)
                else:
                    print(f"[Voz 24/7] Aviso ClientException: {e}", flush=True)
            except Exception as e:
                print(f"[Voz 24/7] Aviso de conexión: {e}", flush=True)

    async def reconnect_forever(self):
        """Bucle ininterrumpido de reconexión rápida ante desconexiones accidentales o forzadas."""
        if self._reconnecting:
            return
        self._reconnecting = True
        delay = 1
        try:
            while self.auto_reconnect_enabled:
                target_ch = self.get_target_voice_channel()
                if not target_ch:
                    await asyncio.sleep(2)
                    continue

                guild = target_ch.guild
                if guild.voice_client and guild.voice_client.is_connected() and guild.voice_client.channel.id == target_ch.id:
                    break

                try:
                    await self.ensure_voice_connection()
                    if guild.voice_client and guild.voice_client.is_connected():
                        break
                except Exception as e:
                    print(f"[Auto-Reconectar] Intento fallido ({e}). Reintentando en {delay}s...", flush=True)

                await asyncio.sleep(delay)
                delay = min(delay * 1.5, 4.0)
        finally:
            self._reconnecting = False

    async def on_voice_state_update(self, member, before, after):
        """
        Monitorea el estado de voz del bot para garantizar:
        1. Si se desconecta -> Reconexión inmediata automática.
        2. Si alguien lo mueve o Discord lo pasa a AFK -> Regreso instantáneo al canal General.
        """
        if member.id != self.user.id:
            return

        target_ch = self.get_target_voice_channel()

        # Desconexión detectada
        if after.channel is None:
            print("[Voz 24/7] 🚨 Desconexión detectada. Reconectando de inmediato a General...", flush=True)
            self.stats.on_voice_disconnected()
            self.voice_client = None
            if self.auto_reconnect_enabled:
                asyncio.create_task(self.reconnect_forever())

        # El bot fue movido a otro canal de voz o al canal AFK
        elif target_ch and after.channel.id != target_ch.id:
            print(f"[Voz 24/7] ⚠️ Movimiento detectado a '{after.channel.name}'. Regresando de inmediato a '{target_ch.name}'...", flush=True)
            try:
                if self.voice_client and self.voice_client.is_connected():
                    await self.voice_client.move_to(target_ch)
                else:
                    await member.move_to(target_ch)
                print(f"[Voz 24/7] 🟢 Retornado exitosamente a '{target_ch.name}'.", flush=True)
            except Exception as e:
                print(f"[Voz 24/7] Error moviendo a canal objetivo: {e}. Forzando reconexión...", flush=True)
                asyncio.create_task(self.ensure_voice_connection())

    @tasks.loop(seconds=5)
    async def voice_keeper_task(self):
        """Vigilante Ultra-Rápido (cada 5s): Asegura presencia 100% permanente en General."""
        try:
            target_ch = self.get_target_voice_channel()
            if not target_ch:
                return

            guild = target_ch.guild
            vc = guild.voice_client

            # 1. Si no está conectado o el socket cayó
            if not vc or not vc.is_connected():
                await self.ensure_voice_connection()
                return

            # 2. Si fue movido a otro canal
            if vc.channel.id != target_ch.id:
                print(f"[Voice Keeper] Corrigiendo canal: de '{vc.channel.name}' a '{target_ch.name}'...", flush=True)
                try:
                    await vc.move_to(target_ch)
                except Exception:
                    pass

            # 3. Transmisión silenciosa continua anti-AFK
            if not vc.is_playing():
                try:
                    vc.play(SilentAudioSource())
                except Exception:
                    pass

            # 4. Asegurar que las estadísticas estén contando
            if not self.stats.is_in_voice:
                self.stats.on_voice_connected()

        except Exception as e:
            # Nunca abortar la tarea
            pass

    @tasks.loop(seconds=60)
    async def stats_and_presence_task(self):
        """Actualiza el contador acumulado y rota la presencia del bot."""
        try:
            self.stats.tick(uptime_delta=60.0)
            self.stats.save()

            total_hours = self.stats.total_voice_hours
            status_options = [
                discord.Streaming(name=f"👑 Hecho por {config.CREATOR_NAME}", url="https://twitch.tv/rafamodzyt"),
                discord.Streaming(name=f"⏳ {total_hours:,.1f}h / 1M en Voz", url="https://twitch.tv/rafamodzyt"),
                discord.Streaming(name="🚀 discord.gg/EFz8NB99N4", url="https://twitch.tv/rafamodzyt"),
                discord.Activity(type=discord.ActivityType.listening, name=f"{config.COMMAND_PREFIX}ayuda | Erick x 24/7")
            ]
            idx = int(time.time() // 60) % len(status_options)
            await self.change_presence(activity=status_options[idx], status=discord.Status.online)
        except Exception as e:
            print(f"[Presence Error] {e}", flush=True)

    @voice_keeper_task.before_loop
    @stats_and_presence_task.before_loop
    async def before_tasks(self):
        await self.wait_until_ready()

def setup_bot_commands(bot: ErickBot):
    """Registra todos los comandos híbridos (// y /) en la instancia del bot."""

    @bot.hybrid_command(
        name="avatar",
        description="Cambia la foto de perfil (avatar) del bot."
    )
    @discord.app_commands.describe(
        url="URL directa de la imagen (o adjunta un archivo)",
        archivo="Archivo de imagen desde tu dispositivo"
    )
    @in_control_channel_or_admin()
    async def cmd_avatar(ctx: commands.Context, url: str = None, archivo: discord.Attachment = None):
        await ctx.defer()
        image_bytes = None

        target_attachment = archivo or (ctx.message.attachments[0] if ctx.message and ctx.message.attachments else None)

        if target_attachment:
            if any(target_attachment.filename.lower().endswith(ext) for ext in [".png", ".jpg", ".jpeg", ".gif", ".webp"]):
                image_bytes = await target_attachment.read()
            else:
                return await ctx.send("❌ El archivo adjunto debe ser una imagen (.png, .jpg, .jpeg, .webp, .gif).")
        elif url:
            try:
                async with aiohttp.ClientSession() as session:
                    async with session.get(url) as resp:
                        if resp.status == 200:
                            image_bytes = await resp.read()
                        else:
                            return await ctx.send(f"❌ Error al descargar imagen (código {resp.status}).")
            except Exception as e:
                return await ctx.send(f"❌ Error al descargar de la URL: {e}")

        if not image_bytes:
            return await ctx.send("❌ Por favor adjunta una imagen o proporciona un enlace (URL) a la imagen.")

        try:
            await bot.user.edit(avatar=image_bytes)
            embed = discord.Embed(
                title="✅ Foto de Perfil Actualizada",
                description=f"El avatar de **{bot.user.name}** se ha actualizado con éxito.",
                color=0x23A55A
            )
            embed.set_thumbnail(url=bot.user.display_avatar.url)
            embed.set_footer(text=f"Hecho por {config.CREATOR_NAME}", icon_url=bot.user.display_avatar.url)
            await ctx.send(embed=embed)
        except discord.HTTPException as e:
            await ctx.send(f"❌ Discord limitó el cambio de avatar (Discord solo permite 2 cambios por hora): {e}")

    @bot.hybrid_command(
        name="nombre",
        description="Cambia el nombre de usuario global del bot."
    )
    @discord.app_commands.describe(nuevo_nombre="Nuevo nombre de usuario para el bot")
    @in_control_channel_or_admin()
    async def cmd_nombre(ctx: commands.Context, *, nuevo_nombre: str):
        if len(nuevo_nombre) < 2 or len(nuevo_nombre) > 32:
            return await ctx.send("❌ El nombre debe tener entre 2 y 32 caracteres.")

        await ctx.defer()
        try:
            await bot.user.edit(username=nuevo_nombre)
            embed = discord.Embed(
                title="✅ Nombre Actualizado",
                description=f"El bot ahora se llama: **{nuevo_nombre}**",
                color=0x5865F2
            )
            embed.set_footer(text=f"Hecho por {config.CREATOR_NAME}")
            await ctx.send(embed=embed)
        except discord.HTTPException as e:
            await ctx.send(f"❌ Discord no permitió cambiar el nombre (Discord solo permite 2 cambios por hora): {e}")

    @bot.hybrid_command(
        name="apodo",
        description="Cambia el apodo del bot en este servidor."
    )
    @discord.app_commands.describe(nuevo_apodo="Nuevo apodo en el servidor (deja vacío para restablecer)")
    @in_control_channel_or_admin()
    async def cmd_apodo(ctx: commands.Context, *, nuevo_apodo: str = None):
        try:
            await ctx.guild.me.edit(nick=nuevo_apodo)
            nombre_mostrado = nuevo_apodo if nuevo_apodo else bot.user.name
            await ctx.send(f"✅ Apodo en este servidor cambiado a: **{nombre_mostrado}**")
        except Exception as e:
            await ctx.send(f"❌ Error al cambiar apodo: {e}")

    @bot.hybrid_command(
        name="estado",
        description="Cambia el estado de conexión del bot (online, idle, dnd, invisible)."
    )
    @discord.app_commands.describe(estado="online, idle, dnd o invisible")
    @in_control_channel_or_admin()
    async def cmd_estado(ctx: commands.Context, estado: str):
        estados = {
            "online": discord.Status.online,
            "idle": discord.Status.idle,
            "dnd": discord.Status.dnd,
            "invisible": discord.Status.invisible
        }
        st = estados.get(estado.lower().replace(" ", ""))
        if not st:
            return await ctx.send("❌ Estado no válido. Usa: `online`, `idle`, `dnd` o `invisible`.")

        await bot.change_presence(status=st)
        await ctx.send(f"✅ Estado del bot cambiado a: **{estado.upper()}**")

    @bot.hybrid_command(
        name="actividad",
        description="Cambia la actividad visible del perfil del bot."
    )
    @discord.app_commands.describe(
        tipo="jugando, viendo, escuchando o compitiendo",
        texto="Texto de la actividad personalizada"
    )
    @in_control_channel_or_admin()
    async def cmd_actividad(ctx: commands.Context, tipo: str, *, texto: str):
        tipos = {
            "jugando": discord.ActivityType.playing,
            "viendo": discord.ActivityType.watching,
            "escuchando": discord.ActivityType.listening,
            "compitiendo": discord.ActivityType.competing
        }
        act_type = tipos.get(tipo.lower())
        if not act_type:
            return await ctx.send("❌ Tipo no válido. Usa: `jugando`, `viendo`, `escuchando` o `compitiendo`.")

        act = discord.Activity(type=act_type, name=texto)
        await bot.change_presence(activity=act)
        await ctx.send(f"✅ Actividad actualizada: **{tipo.capitalize()} {texto}**")

    @bot.hybrid_command(
        name="stream",
        description="Activa el modo Streaming (morado) en el perfil con enlace a tu canal."
    )
    @discord.app_commands.describe(texto="Texto que se mostrará en la transmisión")
    @in_control_channel_or_admin()
    async def cmd_stream(ctx: commands.Context, *, texto: str):
        act = discord.Streaming(
            name=texto,
            url="https://twitch.tv/rafamodzyt"
        )
        await bot.change_presence(activity=act)
        await ctx.send(f"🟣 Modo Transmisión (Streaming) activado: **{texto}**")

    @bot.hybrid_command(
        name="horas",
        description="Muestra el progreso detallado hacia la meta de 1,000,000 de horas en voz."
    )
    @in_control_channel_or_admin()
    async def cmd_horas(ctx: commands.Context):
        bot.stats.tick()
        total_hours = bot.stats.total_voice_hours
        target_hours = bot.stats.target_hours
        pct = bot.stats.get_progress_percentage()
        progress_bar = bot.stats.get_progress_bar(18)
        
        total_uptime = time.time() - bot.bot_start_time
        is_in_voice = bot.stats.is_in_voice

        embed = discord.Embed(
            title="⏳ Meta de 1,000,000 de Horas en Voz",
            description=(
                f"El bot **{bot.user.name}** está programado para estar activo **24/7 sin apagarse nunca**.\n\n"
                f"🎯 **Progreso hacia 1M de Horas:**\n"
                f"`{progress_bar}` **{pct:.5f}%**\n"
                f"⏱️ **{total_hours:,.2f}** de **{target_hours:,.0f} horas** acumuladas\n"
            ),
            color=0x5865F2
        )

        embed.add_field(
            name="🎙️ Estado de Voz",
            value="🟢 **Conectado al canal**" if is_in_voice else "🔴 **Desconectado**",
            inline=True
        )
        embed.add_field(
            name="⚡ Sesión Actual",
            value=f"`{bot.stats.format_duration(bot.stats.current_session_seconds)}`",
            inline=True
        )
        embed.add_field(
            name="🤖 Tiempo Online Total",
            value=f"`{bot.stats.format_duration(total_uptime)}`",
            inline=True
        )
        embed.add_field(
            name="👑 Creador",
            value=f"**{config.CREATOR_NAME}**",
            inline=True
        )
        embed.add_field(
            name="🌐 Discord Oficial",
            value=f"[Unirse aquí]({config.DISCORD_INVITE})",
            inline=True
        )
        embed.add_field(
            name="🔄 Auto-Reconexión",
            value="✅ Activada (24/7)" if bot.auto_reconnect_enabled else "❌ Desactivada",
            inline=True
        )

        embed.set_thumbnail(url=bot.user.display_avatar.url)
        embed.set_footer(
            text=f"Erick x &bull; Echo por {config.CREATOR_NAME} &bull; 1,000,000h Goal",
            icon_url=bot.user.display_avatar.url
        )

        await ctx.send(embed=embed, view=InviteButtonView())

    @bot.hybrid_command(
        name="conectar",
        description="Fuerza la conexión inmediata del bot al canal de voz 24/7."
    )
    @in_control_channel_or_admin()
    async def cmd_conectar(ctx: commands.Context):
        bot.auto_reconnect_enabled = True
        await ctx.defer()
        await bot.ensure_voice_connection()
        if bot.stats.is_in_voice:
            channel = ctx.guild.get_channel(bot.target_voice_channel_id)
            ch_name = channel.name if channel else str(bot.target_voice_channel_id)
            await ctx.send(f"✅ Conectado exitosamente al canal de voz: **{ch_name}** 🟢 (24/7 activo)")
        else:
            await ctx.send("⚠️ No se pudo conectar. Verifica que el bot tenga permisos de 'Conectar' en el canal.")

    @bot.hybrid_command(
        name="desconectar",
        description="Desconecta al bot del canal de voz y pausa el conteo."
    )
    @in_control_channel_or_admin()
    async def cmd_desconectar(ctx: commands.Context):
        bot.auto_reconnect_enabled = False
        if ctx.guild.voice_client:
            await ctx.guild.voice_client.disconnect(force=True)
            bot.stats.on_voice_disconnected()
            bot.voice_client = None
            await ctx.send("🔴 Desconectado del canal de voz. Auto-reconexión pausada. Usa `//conectar` para volver a unirte.")
        else:
            await ctx.send("ℹ️ El bot no estaba conectado a ningún canal de voz.")

    @bot.hybrid_command(
        name="autoreconnect",
        description="Activa o desactiva la auto-reconexión 24/7 del bot."
    )
    @discord.app_commands.describe(opcion="on o off")
    @in_control_channel_or_admin()
    async def cmd_autoreconnect(ctx: commands.Context, opcion: str):
        if opcion.lower() in ["on", "activar", "si", "true"]:
            bot.auto_reconnect_enabled = True
            await bot.ensure_voice_connection()
            await ctx.send("✅ Auto-reconexión **ACTIVADA**. El bot no se saldrá del canal de voz.")
        elif opcion.lower() in ["off", "desactivar", "no", "false"]:
            bot.auto_reconnect_enabled = False
            await ctx.send("⚠️ Auto-reconexión **DESACTIVADA**.")
        else:
            await ctx.send("❌ Usa `//autoreconnect on` o `//autoreconnect off`.")

    @bot.hybrid_command(
        name="canal",
        description="Cambia el canal de voz donde el bot acumulará las horas."
    )
    @discord.app_commands.describe(canal="Canal de voz al que debe unirse el bot")
    @in_control_channel_or_admin()
    async def cmd_canal(ctx: commands.Context, canal: discord.VoiceChannel):
        bot.target_voice_channel_id = canal.id
        await ctx.send(f"✅ Canal de voz objetivo actualizado a: **{canal.name}** (`{canal.id}`). Conectando...")
        await bot.ensure_voice_connection()

    @bot.hybrid_command(
        name="say",
        description="Envía un mensaje personalizado a través del bot."
    )
    @discord.app_commands.describe(mensaje="Mensaje a enviar")
    @in_control_channel_or_admin()
    async def cmd_say(ctx: commands.Context, *, mensaje: str):
        if ctx.message:
            try:
                await ctx.message.delete()
            except Exception:
                pass
        await ctx.send(mensaje)

    @bot.hybrid_command(
        name="embed",
        description="Crea y envía un mensaje embed elegante."
    )
    @discord.app_commands.describe(
        titulo="Título del embed",
        descripcion="Contenido del mensaje",
        color="Color hex (ejemplo: #5865F2 o #23A55A)"
    )
    @in_control_channel_or_admin()
    async def cmd_embed(ctx: commands.Context, titulo: str, descripcion: str, color: str = "#5865F2"):
        color_val = 0x5865F2
        try:
            clean_color = color.replace("#", "").replace("0x", "")
            color_val = int(clean_color, 16)
        except ValueError:
            pass

        if ctx.message:
            try:
                await ctx.message.delete()
            except Exception:
                pass

        embed = discord.Embed(title=titulo, description=descripcion, color=color_val)
        embed.set_footer(text=f"Enviado por {ctx.author.display_name} &bull; Echo por {config.CREATOR_NAME}")
        await ctx.send(embed=embed)

    @bot.hybrid_command(
        name="perfil",
        description="Muestra el perfil completo del bot, créditos del creador y enlace al servidor."
    )
    @in_control_channel_or_admin()
    async def cmd_perfil(ctx: commands.Context):
        bot.stats.tick()
        total_hours = bot.stats.total_voice_hours
        pct = bot.stats.get_progress_percentage()
        uptime_str = bot.stats.format_duration(time.time() - bot.bot_start_time)
        ping = round(bot.latency * 1000)

        embed = discord.Embed(
            title=f"🤖 Perfil Oficial de {bot.user.name}",
            description=(
                f"**Erick x** es un bot de alto rendimiento configurado para estar **Online 24/7** y acumular hasta **1,000,000 de horas** en canales de voz sin apagarse jamás.\n\n"
                f"👑 **Creado por:** `{config.CREATOR_NAME}`\n"
                f"🔗 **Discord Oficial:** [{config.DISCORD_INVITE}]({config.DISCORD_INVITE})\n"
            ),
            color=0x5865F2
        )

        embed.add_field(name="🎙️ Horas en Voz", value=f"**{total_hours:,.2f}h** ({pct:.4f}%)", inline=True)
        embed.add_field(name="⚡ Uptime Online", value=f"`{uptime_str}`", inline=True)
        embed.add_field(name="📶 Latencia / Ping", value=f"`{ping} ms`", inline=True)
        embed.add_field(name="🏠 Servidor", value=f"`{ctx.guild.name}`" if ctx.guild else "Direct", inline=True)
        embed.add_field(name="⚙️ Prefijo", value=f"`{config.COMMAND_PREFIX}`", inline=True)
        embed.add_field(name="🔒 Canal Autorizado", value=f"<#{config.CONTROL_CHANNEL_ID}>", inline=True)

        embed.set_thumbnail(url=bot.user.display_avatar.url)
        embed.set_footer(
            text=f"Erick x &bull; Meta: 1,000,000 de horas &bull; Echo por {config.CREATOR_NAME}",
            icon_url=bot.user.display_avatar.url
        )

        await ctx.send(embed=embed, view=InviteButtonView())

    @bot.hybrid_command(
        name="ping",
        description="Muestra la latencia del bot."
    )
    @in_control_channel_or_admin()
    async def cmd_ping(ctx: commands.Context):
        ping = round(bot.latency * 1000)
        await ctx.send(f"🏓 **Pong!** Latencia de respuesta: `{ping} ms` ⚡")

    @bot.hybrid_command(
        name="ayuda",
        description="Muestra la lista de todos los comandos y cómo usarlos."
    )
    @in_control_channel_or_admin()
    async def cmd_ayuda(ctx: commands.Context):
        embed = discord.Embed(
            title="📖 Panel de Comandos - Erick x",
            description=(
                f"Puedes usar comandos con el prefijo `{config.COMMAND_PREFIX}` o con comandos slash `/`.\n"
                f"👑 **Creador:** `{config.CREATOR_NAME}` | 🚀 **Discord:** [{config.DISCORD_INVITE}]({config.DISCORD_INVITE})\n"
            ),
            color=0x5865F2
        )

        embed.add_field(
            name="🎨 Personalización del Bot",
            value=(
                f"`{config.COMMAND_PREFIX}avatar <url o adjunto>` - Cambia la foto del bot\n"
                f"`{config.COMMAND_PREFIX}nombre <nuevo nombre>` - Cambia el nombre de usuario global\n"
                f"`{config.COMMAND_PREFIX}apodo <nuevo apodo>` - Cambia el apodo en el servidor\n"
                f"`{config.COMMAND_PREFIX}estado <online|idle|dnd|invisible>` - Cambia el estado\n"
                f"`{config.COMMAND_PREFIX}actividad <tipo> <texto>` - Cambia la actividad (jugando, viendo...)\n"
                f"`{config.COMMAND_PREFIX}stream <texto>` - Activa modo streaming morado"
            ),
            inline=False
        )

        embed.add_field(
            name="🎙️ Canal de Voz & Meta 1,000,000 Horas (24/7)",
            value=(
                f"`{config.COMMAND_PREFIX}horas` - Ver progreso y contador hacia 1,000,000h\n"
                f"`{config.COMMAND_PREFIX}conectar` - Conectar o reconectar al canal de voz\n"
                f"`{config.COMMAND_PREFIX}desconectar` - Desconectar del canal de voz\n"
                f"`{config.COMMAND_PREFIX}autoreconnect <on|off>` - Alternar auto-reconexión 24/7\n"
                f"`{config.COMMAND_PREFIX}canal <canal_voz>` - Cambiar el canal de voz objetivo"
            ),
            inline=False
        )

        embed.add_field(
            name="💬 Mensajes & Utilidades",
            value=(
                f"`{config.COMMAND_PREFIX}say <texto>` - Enviar mensaje personalizado\n"
                f"`{config.COMMAND_PREFIX}embed <titulo> | <texto> | [#color]` - Crear mensaje embed\n"
                f"`{config.COMMAND_PREFIX}perfil` - Ver tarjeta del bot y créditos a {config.CREATOR_NAME}\n"
                f"`{config.COMMAND_PREFIX}ping` - Latencia en milisegundos\n"
                f"`{config.COMMAND_PREFIX}ayuda` - Ver este menú de ayuda"
            ),
            inline=False
        )

        embed.set_thumbnail(url=bot.user.display_avatar.url)
        embed.set_footer(
            text=f"Bot Erick x &bull; Echo por {config.CREATOR_NAME}",
            icon_url=bot.user.display_avatar.url
        )

        await ctx.send(embed=embed, view=InviteButtonView())

    @bot.event
    async def on_command_error(ctx: commands.Context, error):
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.CheckFailure):
            return
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"⚠️ Argumento faltante. Usa `{config.COMMAND_PREFIX}ayuda` para revisar la forma correcta de usar el comando.")
        else:
            print(f"[Error de Comando] {error}")

def run_bot():
    """Arranque principal del bot con auto-reinicio perpetuo 24/7."""
    if not config.DISCORD_TOKEN:
        print("❌ ERROR: No se encontró DISCORD_TOKEN en .env", flush=True)
        sys.exit(1)

    intents = discord.Intents.default()
    intents.guilds = True
    intents.voice_states = True
    intents.messages = True
    
    if config.ENABLE_MESSAGE_CONTENT:
        intents.message_content = True

    bot = ErickBot(intents=intents)
    setup_bot_commands(bot)

    # Iniciar servidor web de monitoreo para Railway / Render / UptimeRobot
    start_keep_alive(stats_manager=bot.stats, bot=bot, port=config.PORT)

    print("🚀 Iniciando Erick x 24/7 (Voz Permanente en General)...", flush=True)

    while True:
        try:
            bot.run(config.DISCORD_TOKEN, reconnect=True)
        except discord.errors.LoginFailure as e:
            print("\n" + "="*60, flush=True)
            print("❌ ERROR DE AUTENTICACIÓN DE DISCORD (Token Inválido)", flush=True)
            print(f"👉 Detalle: {e}", flush=True)
            print("El DISCORD_TOKEN en tu archivo .env no es válido o fue reseteado en Discord Developer Portal.", flush=True)
            print(f"👉 Ve a: https://discord.com/developers/applications/{config.APPLICATION_ID}/bot", flush=True)
            print("Copia tu nuevo Token ('Reset Token') y pégalo en el archivo .env en DISCORD_TOKEN=...", flush=True)
            print("="*60 + "\n", flush=True)
            time.sleep(10)
        except discord.errors.PrivilegedIntentsRequired:
            print("\n⚠️ AVISO: 'Message Content Intent' no está activado en Discord Developer Portal.", flush=True)
            print(f"👉 Actívalo aquí: https://discord.com/developers/applications/{config.APPLICATION_ID}/bot", flush=True)
            print("Iniciando modo compatible con comandos Slash y conexión 24/7 a voz...", flush=True)
            
            fallback_intents = discord.Intents.default()
            fallback_intents.guilds = True
            fallback_intents.voice_states = True
            fallback_intents.messages = True
            fallback_bot = ErickBot(intents=fallback_intents)
            setup_bot_commands(fallback_bot)
            set_bot_reference(fallback_bot, fallback_bot.stats)
            try:
                fallback_bot.run(config.DISCORD_TOKEN, reconnect=True)
            except Exception as e_fb:
                print(f"⚠️ Error en bot fallback: {e_fb}. Reintentando en 5s...", flush=True)
                time.sleep(5)
        except KeyboardInterrupt:
            print("\nDetención manual solicitada por el usuario.", flush=True)
            break
        except Exception as e:
            print(f"⚠️ Caída detectada: {e}. Reiniciando bot automáticamente en 3 segundos...", flush=True)
            time.sleep(3)



if __name__ == "__main__":
    run_bot()
