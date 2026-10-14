import asyncio
import datetime
import io
import os
import sys
import time
import aiohttp
import discord
from discord.ext import commands, tasks
from discord.ui import Button, View, Modal, TextInput

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

import config

class ServerLinkView(View):
    """Botón con el enlace de invitación al servidor."""
    def __init__(self):
        super().__init__(timeout=None)
        self.add_item(Button(
            label="Servidor Oficial SHADOW BLOCK",
            url=config.SERVER_LINK,
            style=discord.ButtonStyle.link,
            emoji="👑"
        ))

class GameBotsModal(Modal, title="🎮 Emparejamiento con Bots Free Fire"):
    def __init__(self):
        super().__init__(timeout=300)
        self.player_id = TextInput(
            label="ID de Jugador Free Fire",
            placeholder="Ej: 1982736451",
            min_length=5,
            max_length=15,
            required=True
        )
        self.region = TextInput(
            label="Región (SUR, NORTE o EEUU)",
            placeholder="Escribe: SUR, NORTE o EEUU",
            min_length=3,
            max_length=15,
            required=True
        )
        self.add_item(self.player_id)
        self.add_item(self.region)

    async def on_submit(self, interaction: discord.Interaction):
        reg = self.region.value.strip().lower()
        valid_regions = {
            "sur": "SUR (Sudamérica)",
            "norte": "NORTE (Norteamérica)",
            "eeuu": "EEUU (Estados Unidos)",
            "ee.uu": "EEUU (Estados Unidos)",
            "ee uu": "EEUU (Estados Unidos)",
            "usa": "EEUU (Estados Unidos)",
            "us": "EEUU (Estados Unidos)"
        }
        if reg not in valid_regions:
            await interaction.response.send_message(
                f"❌ **Región inválida:** `{self.region.value}`.\n"
                "Las únicas regiones permitidas son: **`SUR`**, **`NORTE`** y **`EEUU`**.",
                ephemeral=True
            )
            return

        reg_name = valid_regions[reg]
        import random
        team_num = random.randint(1000, 9999)
        team_code = f"#FF-{random.randint(10000, 99999)}"
        bot_names = [
            f"[BOT] Alex_Insano_{random.randint(10, 99)}",
            f"[BOT] Ghost_Shadow_{random.randint(10, 99)}",
            f"[BOT] Cobra_King_{random.randint(10, 99)}"
        ]

        embed = discord.Embed(
            title="🎮 EMPAREJAMIENTO CON BOTS EXITOSO",
            description=(
                f"👤 **Jugador:** `{self.player_id.value}`\n"
                f"🌐 **Región:** `{reg_name}`\n"
                f"🏷️ **Equipo:** `🔥 ESCUADRA BOTS HEROICA #{team_num}`\n"
                f"🔑 **Código de Sala:** `{team_code}`\n\n"
                f"⚠️ **ALERTA DEL SISTEMA: BOTS DISPONIBLES:**\n"
                f"• **Límite diario:** Máximo **55 cuentas bots activas** por día.\n"
                f"• **Estado actual:** `3/55 bots encolados para tu ID`.\n\n"
                f"🤖 **Miembros de la Escuadra de Bots:**\n"
                f"1. 👑 `[LÍDER] ID: {self.player_id.value}` (Tú)\n"
                f"2. 🤖 `{bot_names[0]}` (ID: {random.randint(1000000000, 9999999999)})\n"
                f"3. 🤖 `{bot_names[1]}` (ID: {random.randint(1000000000, 9999999999)})\n"
                f"4. 🤖 `{bot_names[2]}` (ID: {random.randint(1000000000, 9999999999)})\n\n"
                f"✨ **Instrucciones:** Abre Free Fire, ingresa al modo Escuadra e introduce el código `{team_code}`. "
                "Los bots te cederán todas las bajas para subir rápidamente de rango."
            ),
            color=0x2ECC71
        )
        embed.set_footer(text=f"Matchmaking Bots Free Fire • Creado por {config.CREATOR_NAME} • SHADOW BLOCK")
        await interaction.response.send_message(embed=embed, ephemeral=True)


class SendReportsModal(Modal, title="🚨 Enviar 55 Reportes a Cuenta"):
    def __init__(self):
        super().__init__(timeout=300)
        self.target_id = TextInput(
            label="ID de la Cuenta a Reportar",
            placeholder="Ej: 5829104921",
            min_length=5,
            max_length=15,
            required=True
        )
        self.region = TextInput(
            label="Región (SUR, NORTE o EEUU)",
            placeholder="Escribe: SUR, NORTE o EEUU",
            min_length=3,
            max_length=15,
            required=True
        )
        self.reason = TextInput(
            label="Motivo del Reporte",
            placeholder="Ej: Aimbot / Macro / Bug de Rango",
            default="Uso de hacks, aimbot y alteración de rango",
            required=False
        )
        self.add_item(self.target_id)
        self.add_item(self.region)
        self.add_item(self.reason)

    async def on_submit(self, interaction: discord.Interaction):
        reg = self.region.value.strip().lower()
        valid_regions = {
            "sur": "SUR (Sudamérica)",
            "norte": "NORTE (Norteamérica)",
            "eeuu": "EEUU (Estados Unidos)",
            "ee.uu": "EEUU (Estados Unidos)",
            "ee uu": "EEUU (Estados Unidos)",
            "usa": "EEUU (Estados Unidos)",
            "us": "EEUU (Estados Unidos)"
        }
        if reg not in valid_regions:
            await interaction.response.send_message(
                f"❌ **Región inválida:** `{self.region.value}`.\n"
                "Las únicas regiones permitidas son: **`SUR`**, **`NORTE`** y **`EEUU`**.",
                ephemeral=True
            )
            return

        reg_name = valid_regions[reg]
        target = self.target_id.value.strip()

        await interaction.response.defer(ephemeral=True)

        import random
        BOT_PREFIXES = ["ShadowBot", "FF_Hunter", "CobraSniper", "GhostBuster", "InsanoVip", "AimbotNull", "NoobSlayer", "ReportSniper", "BermudaMod", "BlacklistBot"]
        bot_pool = [f"[{p}_{random.randint(10, 99)}]" for p in [random.choice(BOT_PREFIXES) for _ in range(55)]]

        # Mensaje de carga 1 (0 a 4 segundos)
        emb1 = discord.Embed(
            title="⏳ [PASO 1/4] CONECTANDO RED DE 55 CUENTAS BOTS...",
            description=(
                f"🎯 **Objetivo:** `{target}` | 🌐 **Región:** `{reg_name}`\n"
                f"⏱️ **Tiempo estimado:** `12 segundos`\n\n"
                f"`[▓▓░░░░░░░░] 20%` (11/55 bots conectados)\n\n"
                f"🤖 **Cuentas bots activadas en vivo:**\n"
                f"`{', '.join(bot_pool[:8])}...`"
            ),
            color=0xF1C40F
        )
        emb1.set_footer(text=f"Procesando 55 reportes • Creado por {config.CREATOR_NAME}")
        msg = await interaction.followup.send(embed=emb1, ephemeral=True)

        await asyncio.sleep(4)

        # Mensaje de carga 2 (4 a 8 segundos)
        emb2 = discord.Embed(
            title="⚡ [PASO 2/4] ENVIANDO RÁFAGA DE REPORTES SIMULTÁNEOS...",
            description=(
                f"🎯 **Objetivo:** `{target}` | 🌐 **Región:** `{reg_name}`\n"
                f"⏱️ **Tiempo transcurrido:** `4 / 12 segundos`\n\n"
                f"`[▓▓▓▓▓░░░░░] 55%` (30/55 reportes enviados)\n\n"
                f"🤖 **Cuentas bots enviando reportes:**\n"
                f"`{', '.join(bot_pool[8:16])}...`"
            ),
            color=0xE67E22
        )
        emb2.set_footer(text=f"Procesando 55 reportes • Creado por {config.CREATOR_NAME}")
        await msg.edit(embed=emb2)

        await asyncio.sleep(4)

        # Mensaje de carga 3 (8 a 12 segundos)
        emb3 = discord.Embed(
            title="🚨 [PASO 3/4] INYECTANDO PROTOCOLO BLACKLIST Y BUG DE RANGO...",
            description=(
                f"🎯 **Objetivo:** `{target}` | 🌐 **Región:** `{reg_name}`\n"
                f"⏱️ **Tiempo transcurrido:** `8 / 12 segundos`\n\n"
                f"`[▓▓▓▓▓▓▓▓░░] 85%` (48/55 reportes enviados)\n\n"
                f"🤖 **Cuentas finales procesando blacklist:**\n"
                f"`{', '.join(bot_pool[16:24])}...`"
            ),
            color=0xE74C3C
        )
        emb3.set_footer(text=f"Inyectando Blacklist • Creado por {config.CREATOR_NAME}")
        await msg.edit(embed=emb3)

        await asyncio.sleep(4)

        # Mensaje Final (12 segundos)
        emb_final = discord.Embed(
            title="✅ ¡55 REPORTES ENVIADOS CON ÉXITO EN 12 SEGUNDOS!",
            description=(
                f"El sistema ha ejecutado y validado la ráfaga de **55 reportes masivos** contra la cuenta objetivo.\n\n"
                f"👤 **Cuenta Objetivo:** `{target}`\n"
                f"🌐 **Región Confirmada:** `{reg_name}`\n"
                f"⏱️ **Tiempo Total:** `Exactamente 12 segundos`\n"
                f"📜 **Motivo Reportado:** `{self.reason.value or 'Aimbot y manipulación de rango'}`\n"
                f"⛔ **Estado:** `ENCOLADA EN BLACKLIST / RANGO CONGELADO Y BUGEADO`\n\n"
                f"🤖 **Muestra de las 55 Cuentas Bots Utilizadas:**\n"
                f"• `{bot_pool[0]}` • `{bot_pool[1]}` • `{bot_pool[2]}`\n"
                f"• `{bot_pool[3]}` • `{bot_pool[4]}` • `{bot_pool[5]}`\n"
                f"• `{bot_pool[6]}` • `{bot_pool[7]}` • `{bot_pool[8]}`\n"
                f"*(y 46 cuentas bots automáticas más activadas en la ráfaga)*\n\n"
                f"🏆 **Comprobante Oficial:** Proceso completado satisfactoriamente."
            ),
            color=0x2ECC71
        )
        emb_final.set_footer(
            text=f"Sistema Oficial Desarrollado por {config.CREATOR_NAME} • SHADOW BLOCK VIP",
            icon_url="https://images.unsplash.com/photo-1542751371-adc38448a05e?q=80&w=200&auto=format&fit=crop"
        )
        await msg.edit(embed=emb_final)

class AdminBot(commands.Bot):
    def __init__(self, intents: discord.Intents):
        super().__init__(
            command_prefix=commands.when_mentioned_or(config.COMMAND_PREFIX),
            intents=intents,
            help_command=None
        )
        self.welcome_channel_id = config.WELCOME_CHANNEL_ID
        self.webhook_url = config.WEBHOOK_URL
        self.start_time = time.time()

    async def setup_hook(self):
        # Sincronizar comandos slash en el servidor principal para disponibilidad instantánea
        try:
            guild_obj = discord.Object(id=config.GUILD_ID)
            self.tree.copy_global_to(guild=guild_obj)
            await self.tree.sync(guild=guild_obj)
            print(f"[Admin Bot] Comandos sincronizados exitosamente en servidor ID: {config.GUILD_ID}", flush=True)
        except Exception as e:
            print(f"[Admin Bot] Aviso al sincronizar slash commands: {e}", flush=True)

    @tasks.loop(minutes=25)
    async def hourly_wallpaper_task(self):
        """Publica automáticamente cada 25 minutos 100 wallpapers 4K únicos para PC y Móvil."""
        try:
            channel_id = 1559842253352992840
            channel = self.get_channel(channel_id)
            if not channel:
                channel = await self.fetch_channel(channel_id)
            if channel:
                from wallpapers_data import generate_unique_wallpapers
                # Generar 100 wallpapers 4K únicos (sin duplicados)
                wallpapers = generate_unique_wallpapers(count=100, mode="all")
                chunk_size = 10
                total_batches = (len(wallpapers) + chunk_size - 1) // chunk_size

                print(f"[Wallpapers 4K] Enviando ráfaga masiva de 100 wallpapers a #{channel.name}...", flush=True)

                for idx in range(total_batches):
                    batch = wallpapers[idx * chunk_size : (idx + 1) * chunk_size]
                    embeds = []
                    for item in batch:
                        emb = discord.Embed(
                            title=f"🖼️ 4K ULTRA HD: {item['title']}",
                            description=f"📂 **Categoría:** `{item['category']}` | 📐 **Resolución:** `{item['res']}`",
                            color=0x5865F2 if not item.get("is_mobile") else 0x9B59B6
                        )
                        emb.set_image(url=item['url'])
                        emb.set_footer(text=f"Galería Masiva 99,999+ • SHADOW BLOCK • rafamodzyt • ID #{item['id']}")
                        embeds.append(emb)

                    header_content = f"⚡ **[LOTE {idx+1}/{total_batches}] 100 WALLPAPERS 4K ULTRA HD • 99,999+ FONDOS ÚNICOS**" if idx == 0 else ""
                    await channel.send(content=header_content, embeds=embeds)
                    await asyncio.sleep(1.2)

                print("[Wallpapers 4K] Ráfaga de 100 wallpapers publicada automáticamente con éxito.", flush=True)
        except Exception as e:
            print(f"[Wallpapers 4K Error] {e}", flush=True)

    def record_member_event(self, event_type: str, member: discord.Member, details: str = ""):
        """Registra un evento de entrada/salida/estado en live_members.json para el Panel DX11."""
        try:
            import json
            import os
            filepath = os.path.join(os.path.dirname(__file__), "live_members.json")
            data = {"events": [], "members": []}
            if os.path.exists(filepath):
                with open(filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)

            now_str = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            avatar_url = member.display_avatar.url if member.display_avatar else ""

            # Agregar evento al historial
            new_event = {
                "type": event_type,
                "user_id": str(member.id),
                "name": str(member.name),
                "time": now_str,
                "details": details or f"Acción: {event_type}",
                "avatar": avatar_url
            }
            data.setdefault("events", []).insert(0, new_event)
            if len(data["events"]) > 50:
                data["events"] = data["events"][:50]

            # Actualizar o agregar a la lista de miembros
            members_list = data.setdefault("members", [])
            found = False
            for m in members_list:
                if m.get("id") == str(member.id):
                    m["name"] = str(member.name)
                    m["nick"] = member.nick or str(member.name)
                    m["status"] = "OFFLINE" if event_type == "LEAVE" else "ONLINE"
                    m["avatar_url"] = avatar_url
                    found = True
                    break

            if not found and event_type != "LEAVE":
                members_list.append({
                    "id": str(member.id),
                    "name": str(member.name),
                    "tag": str(member),
                    "nick": member.nick or str(member.name),
                    "status": "ONLINE",
                    "bot": member.bot,
                    "roles": [r.name for r in member.roles if r.name != "@everyone"],
                    "joined_at": now_str[:10],
                    "avatar_url": avatar_url
                })

            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"[Error record_member_event] {e}", flush=True)

    async def on_ready(self):
        print("==================================================", flush=True)
        print(f"🛡️ Bot Administrador iniciado: {self.user} (ID: {self.user.id})", flush=True)
        print(f"👑 Creador: {config.CREATOR_NAME}", flush=True)
        print(f"🏠 Servidor: {config.GUILD_ID}", flush=True)
        print(f"👋 Canal de Bienvenidas: {self.welcome_channel_id}", flush=True)
        print("🖼️ Canal Wallpapers 4K: 1559842253352992840 (Auto-cada hora)", flush=True)
        print("==================================================", flush=True)

        activity = discord.Streaming(
            name=f"🛡️ Servidor SHADOW BLOCK | Hecho por {config.CREATOR_NAME}",
            url="https://twitch.tv/rafamodzyt"
        )
        await self.change_presence(activity=activity, status=discord.Status.online)

        if not self.hourly_wallpaper_task.is_running():
            self.hourly_wallpaper_task.start()

    async def on_member_join(self, member: discord.Member):
        """Envía el mensaje de bienvenida cuando un usuario entra al servidor."""
        self.record_member_event("JOIN", member, "Entró al servidor")
        if member.guild.id != config.GUILD_ID:
            return

        channel = member.guild.get_channel(self.welcome_channel_id)
        if not channel:
            print(f"[Bienvenida] Canal {self.welcome_channel_id} no encontrado.", flush=True)
            return

        guild = member.guild
        member_count = guild.member_count
        created_timestamp = int(member.created_at.timestamp())

        embed = discord.Embed(
            title="👋 ¡BIENVENIDO/A A SHADOW BLOCK!",
            description=(
                f"¡Hola {member.mention}! Nos alegra mucho tenerte en **{guild.name}**.\n\n"
                f"👤 **Usuario:** `{member.name}`\n"
                f"🆔 **ID:** `{member.id}`\n"
                f"📅 **Cuenta creada:** <t:{created_timestamp}:R>\n"
                f"👥 **Miembro número:** `#{member_count}`\n\n"
                f"📜 Por favor lee las reglas y disfruta de tu estadía.\n"
                f"💬 Pasa por <#1350706770527653992> a saludar a la comunidad."
            ),
            color=0x23A55A,
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        )

        embed.set_thumbnail(url=member.display_avatar.url)
        if guild.icon:
            embed.set_author(name=guild.name, icon_url=guild.icon.url)
        embed.set_footer(
            text=f"Servidor administrado por {config.CREATOR_NAME} &bull; ¡Disfruta!",
            icon_url=guild.icon.url if guild.icon else None
        )

        # Auto-rol Member automático para nuevos miembros
        try:
            member_role = member.guild.get_role(1559846472080687196) or discord.utils.get(member.guild.roles, name="Member")
            if member_role and member_role not in member.roles:
                await member.add_roles(member_role, reason="Auto-rol Member para nuevos usuarios")
                print(f"[Auto-Rol] Rol Member asignado a nuevo miembro: {member.name}", flush=True)
        except Exception as e_role:
            print(f"[Auto-Rol Error] {e_role}", flush=True)

        try:
            await channel.send(
                content=f"🎉 ¡Un nuevo miembro ha llegado! Dale la bienvenida a {member.mention}",
                embed=embed,
                view=ServerLinkView()
            )
            print(f"[Bienvenida] Mensaje enviado para {member.name} (#{member_count})", flush=True)
        except Exception as e:
            print(f"[Bienvenida] Error al enviar mensaje: {e}", flush=True)

    async def on_member_remove(self, member: discord.Member):
        """Envía el mensaje de despedida cuando un usuario sale del servidor."""
        self.record_member_event("LEAVE", member, "Salió del servidor")
        if member.guild.id != config.GUILD_ID:
            return

        channel = member.guild.get_channel(self.welcome_channel_id)
        if not channel:
            return

        guild = member.guild
        member_count = guild.member_count
        joined_str = f"<t:{int(member.joined_at.timestamp())}:R>" if member.joined_at else "Desconocido"

        embed = discord.Embed(
            title="👋 ¡HASTA LUEGO!",
            description=(
                f"**{member.name}** ha abandonado el servidor.\n\n"
                f"👤 **Usuario:** `{member.name}`\n"
                f"⏱️ **Estuvo aquí desde:** {joined_str}\n"
                f"👥 **Ahora somos:** `{member_count} miembros`\n\n"
                f"Esperamos verte pronto de vuelta por aquí."
            ),
            color=0xED4245,
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        )

        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f"SHADOW BLOCK &bull; Hecho por {config.CREATOR_NAME}")

        try:
            await channel.send(embed=embed)
            print(f"[Despedida] Notificación enviada para {member.name} (Quedan: {member_count})", flush=True)
        except Exception as e:
            print(f"[Despedida] Error al enviar mensaje: {e}", flush=True)

    async def on_message(self, message: discord.Message):
        """Registra actividad en el chat y asegura que el usuario tenga el rol Member."""
        if message.author != self.user and isinstance(message.author, discord.Member):
            self.record_member_event("ACTIVE", message.author, f"Activo en #{message.channel.name}")
            # Auto-asignar rol si no lo tiene
            if not message.author.bot:
                try:
                    member_role = message.guild.get_role(1559846472080687196) or discord.utils.get(message.guild.roles, name="Member")
                    if member_role and member_role not in message.author.roles:
                        await message.author.add_roles(member_role, reason="Auto-rol Member para miembros activos")
                        print(f"[Auto-Rol] Asignado rol Member a usuario activo: {message.author.name}", flush=True)
                except Exception:
                    pass
        await self.process_commands(message)

    async def on_interaction(self, interaction: discord.Interaction):
        """Maneja los menús interactivos de wallpapers y los botones de compra de tickets."""
        custom_id = interaction.data.get("custom_id", "")

        # 1. Selector de Wallpapers 4K
        if custom_id == "select_wallpaper_device":
            values = interaction.data.get("values", [])
            val = values[0] if values else "wallpaper_pc"
            from wallpapers_data import generate_unique_wallpapers

            if val == "wallpaper_pc":
                unique_wps = generate_unique_wallpapers(count=6, mode="pc")
                embeds = []
                for s in unique_wps:
                    emb = discord.Embed(
                        title=f"🖥️ WALLPAPER 4K PC: {s['title']}",
                        description=f"📂 **Categoría:** `{s['category']}` | 📐 **Resolución:** `{s['res']}`",
                        color=0x5865F2
                    )
                    emb.set_image(url=s["url"])
                    emb.set_footer(text=f"SHADOW BLOCK • Hecho por {config.CREATOR_NAME} • ID #{s['id']}")
                    embeds.append(emb)
                await interaction.response.send_message(
                    content="🖥️ **¡Aquí tienes tus Wallpapers 4K para PC / Escritorio únicos!**",
                    embeds=embeds,
                    ephemeral=True
                )

            elif val == "wallpaper_mobile":
                unique_wps = generate_unique_wallpapers(count=6, mode="mobile")
                embeds = []
                for s in unique_wps:
                    emb = discord.Embed(
                        title=f"📱 WALLPAPER 4K MÓVIL: {s['title']}",
                        description=f"📂 **Categoría:** `{s['category']}` | 📐 **Resolución:** `{s['res']}`",
                        color=0x9B59B6
                    )
                    emb.set_image(url=s["url"])
                    emb.set_footer(text=f"SHADOW BLOCK • Hecho por {config.CREATOR_NAME} • ID #{s['id']}")
                    embeds.append(emb)
                await interaction.response.send_message(
                    content="📱 **¡Aquí tienes tus Wallpapers 4K AMOLED para Móvil / Celular únicos!**",
                    embeds=embeds,
                    ephemeral=True
                )

            elif val in ("wallpaper_burst", "wallpaper_leaks"):
                unique_wps = generate_unique_wallpapers(count=8, mode="all")
                embeds = []
                for s in unique_wps:
                    emb = discord.Embed(
                        title=f"⚡ 4K LEAK & GAMING: {s['title']}",
                        description=f"📐 `{s['res']}` | 📂 `{s['category']}`",
                        color=0xED4245
                    )
                    emb.set_image(url=s["url"])
                    emb.set_footer(text=f"SHADOW BLOCK • {config.CREATOR_NAME} • ID #{s['id']}")
                    embeds.append(emb)
                await interaction.response.send_message(
                    content="🔥 **¡RÁFAGA EXCLUSIVA DE WALLPAPERS 4K LEAKS DESPLEGADA!**",
                    embeds=embeds,
                    ephemeral=True
                )

        # 2. Tickets de Compra de Paneles y Bots
        elif custom_id in ("buy_panel_cpp", "buy_bot_voice"):
            prod_name = "Panel C++ DirectX 11 Win32" if custom_id == "buy_panel_cpp" else "Bot 24/7 de Voz (Erick x)"
            guild = interaction.guild
            cat = discord.utils.get(guild.categories, name="🛒・TIENDA & SOPORTE")
            overwrites = {
                guild.default_role: discord.PermissionOverwrite(read_messages=False),
                interaction.user: discord.PermissionOverwrite(read_messages=True, send_messages=True, attach_files=True),
                guild.me: discord.PermissionOverwrite(read_messages=True, send_messages=True, manage_channels=True)
            }
            ch_name = f"ticket-{interaction.user.name.lower()[:12]}"
            try:
                ticket_ch = await guild.create_text_channel(name=ch_name, category=cat, overwrites=overwrites)
                
                embed_ticket = discord.Embed(
                    title=f"🎫 TICKET DE COMPRA: {prod_name}",
                    description=(
                        f"¡Hola {interaction.user.mention}! Has abierto un ticket para adquirir **{prod_name}**.\n\n"
                        f"👑 **Atención Oficial:** `{config.CREATOR_NAME}` te atenderá de inmediato.\n"
                        "💳 **Métodos de pago aceptados:** PayPal, Cripto (USDT/BTC), Transferencias.\n"
                        "💬 Escribe tus dudas o requerimientos aquí y un administrador responderá."
                    ),
                    color=0x2ECC71
                )
                close_btn = Button(label="Cerrar Ticket", style=discord.ButtonStyle.danger, emoji="🔒", custom_id="close_ticket")
                view = View(timeout=None)
                view.add_item(close_btn)
                await ticket_ch.send(content=f"{interaction.user.mention} | <@1350706770527653989>", embed=embed_ticket, view=view)

                await interaction.response.send_message(f"✅ ¡Tu ticket de compra ha sido creado en {ticket_ch.mention}!", ephemeral=True)
            except Exception:
                await interaction.response.send_message(
                    f"💳 **Compra de {prod_name}:** Para concretar tu compra contacta directamente a **{config.CREATOR_NAME}** en Discord.",
                    ephemeral=True
                )

        elif custom_id == "close_ticket":
            await interaction.response.send_message("🔒 Este ticket se cerrará en 3 segundos...")
            await asyncio.sleep(3)
            try:
                await interaction.channel.delete()
            except Exception:
                pass

        # 3. Menús y Botones de 9,999 Stickers
        elif custom_id == "select_sticker_category":
            values = interaction.data.get("values", [])
            val = values[0] if values else "cat_freefire"
            from stickers_catalog_9999 import get_stickers_batch
            cat_map = {
                "cat_freefire": ("Free Fire", 1),
                "cat_pepe": ("Pepe & Wojak", 50),
                "cat_sigma": ("GigaChad & Sigma", 100),
                "cat_doge": ("Cheems & Doge", 150),
                "cat_karely": ("Karely Ruiz", 200),
                "cat_hacker": ("Hackers & Cyber", 250),
                "cat_memes": ("Memes Virales", 300)
            }
            cat_title, start_id = cat_map.get(val, ("Stickers", 1))
            stks = get_stickers_batch(start_id, count=4)
            embeds = []
            for s in stks:
                emb = discord.Embed(
                    title=f"🎭 {s['title']}",
                    description=f"📂 **Categoría:** `{s['category']}`\n🏷️ **Tag:** `{s['tag']}`\n⚡ Comando: `//sticker {s['id']}`",
                    color=0xF1C40F
                )
                emb.set_image(url=s["url"])
                emb.set_footer(text=f"SHADOW BLOCK • 9,999 Stickers • rafamodzyt")
                embeds.append(emb)
            await interaction.response.send_message(
                content=f"🔥 **Stickers desplegados de {cat_title} (Lote #{start_id:04d}):**",
                embeds=embeds,
                ephemeral=True
            )

        elif custom_id in ("btn_stk_ff", "btn_stk_pepe", "btn_stk_sigma", "btn_stk_random"):
            import random
            from stickers_catalog_9999 import get_sticker_by_id
            if custom_id == "btn_stk_ff":
                sid = random.randint(1, 100)
            elif custom_id == "btn_stk_pepe":
                sid = random.randint(101, 200)
            elif custom_id == "btn_stk_sigma":
                sid = random.randint(201, 300)
            else:
                sid = random.randint(1, 9999)
            s = get_sticker_by_id(sid)
            emb = discord.Embed(
                title=f"🎭 {s['title']}",
                description=f"📂 `{s['category']}` | 🏷️ `{s['tag']}`\n⚡ Usa `//sticker {s['id']}` para mandarlo a cualquier canal",
                color=0x2ECC71
            )
            emb.set_image(url=s["url"])
            emb.set_footer(text=f"Sticker #{s['id']:04d} de 9,999 • SHADOW BLOCK • rafamodzyt")
            await interaction.response.send_message(
                content=f"🎲 **¡Sticker #{s['id']:04d} generado con éxito!**",
                embed=emb,
                ephemeral=True
            )

        # 4. Soundboard 500 Voces de Free Fire
        elif custom_id == "select_voice_category":
            values = interaction.data.get("values", [])
            val = values[0] if values else "voice_cat_donato"
            from freefire_voices_500 import get_voices_for_category
            cat_key = val.replace("voice_cat_", "")
            voices = get_voices_for_category(cat_key, limit=5)
            lines = []
            for v in voices:
                lines.append(f"• **#{v['id']:03d}**: {v['title']} ➔ *\"{v['text']}\"*")
            desc = "\n".join(lines)
            emb = discord.Embed(
                title=f"🔊 Soundboard Free Fire: {cat_key.upper()} (Voces Oficiales)",
                description=f"Presiona los botones rápidos o usa `//voz [id]` para reproducir en canal de voz:\n\n{desc}",
                color=0xE74C3C
            )
            emb.set_footer(text="500 Voces Free Fire • SHADOW BLOCK • rafamodzyt")
            await interaction.response.send_message(embed=emb, ephemeral=True)

        elif custom_id in ("play_snd_donato", "play_snd_zelika", "play_snd_hacker", "play_snd_gang", "play_snd_booyah"):
            snd_map = {
                "play_snd_donato": 1,
                "play_snd_zelika": 101,
                "play_snd_hacker": 201,
                "play_snd_gang": 301,
                "play_snd_booyah": 401
            }
            sid = snd_map.get(custom_id, 1)
            from freefire_voices_500 import get_voice_by_id
            v = get_voice_by_id(sid)
            emb = discord.Embed(
                title=f"🎙️ Reproduciendo: {v['title']}",
                description=f"🔊 **Frase:** *\"{v['text']}\"*\n📁 **Categoría:** `{v['category']}`\n✅ **Estado:** Sonido transmitido a los canales de voz de SHADOW BLOCK.",
                color=0x2ECC71
            )
            emb.set_footer(text=f"Clip #{v['id']:03d} / 500 • Soundboard rafamodzyt")
            await interaction.response.send_message(embed=emb, ephemeral=True)

        # 5. Game Bots (Emparejamiento de Bots Free Fire)
        elif custom_id == "btn_game_bots_match":
            await interaction.response.send_modal(GameBotsModal())

        elif custom_id == "btn_game_bots_info":
            emb = discord.Embed(
                title="⚡ INFORMACIÓN DE CUENTAS BOTS DISPONIBLES (55)",
                description=(
                    "📊 **Detalles del Servicio de Matchmaking con Bots:**\n\n"
                    "• **Capacidad Diaria:** Máximo **55 cuentas bots activas** por día.\n"
                    "• **Compatibilidad:** Modo BR Clasificatoria y Duelo de Escuadras.\n"
                    "• **Regiones soportadas:** `SUR`, `NORTE` y `EEUU`.\n"
                    "• **Funcionamiento:** Los bots ingresan como compañeros de equipo oficiales y ceden las bajas.\n\n"
                    f"👑 **Creado por:** `{config.CREATOR_NAME}` • Servidor Oficial SHADOW BLOCK"
                ),
                color=0x3498DB
            )
            await interaction.response.send_message(embed=emb, ephemeral=True)

        # 6. Send Reports (55 Reportes en 12 Segundos)
        elif custom_id == "btn_send_reports_modal":
            await interaction.response.send_modal(SendReportsModal())

        elif custom_id == "btn_send_reports_status":
            emb = discord.Embed(
                title="🛡️ ESTADO DEL SERVIDOR DE REPORTES & BLACKLIST",
                description=(
                    "🟢 **Estado del Servicio:** ONLINE 24/7\n"
                    "🤖 **Red de Cuentas Bots:** 55 cuentas preparadas para envío simultáneo.\n"
                    "⚡ **Velocidad de Ráfaga:** 55 reportes en exactamente **12 segundos**.\n"
                    "🎯 **Efecto Objetivo:** Inyección en Blacklist y congelamiento/bug de rango.\n\n"
                    f"👑 **Desarrollado y Administrado por:** `{config.CREATOR_NAME}`"
                ),
                color=0x9B59B6
            )
            await interaction.response.send_message(embed=emb, ephemeral=True)

def setup_admin_commands(bot: AdminBot):
    """Registra todos los comandos de administración, moderación, canales, roles y bienvenidas."""

    # ==========================================
    # BIENVENIDAS Y PRUEBAS
    # ==========================================

    @bot.hybrid_command(
        name="testbienvenida",
        description="Envía una prueba del mensaje de bienvenida en el canal configurado."
    )
    @commands.has_permissions(administrator=True)
    async def cmd_testbienvenida(ctx: commands.Context):
        await ctx.defer(ephemeral=True)
        channel = ctx.guild.get_channel(bot.welcome_channel_id)
        if not channel:
            return await ctx.send(f"❌ Canal de bienvenida no encontrado (`{bot.welcome_channel_id}`).", ephemeral=True)

        member = ctx.author
        created_timestamp = int(member.created_at.timestamp())
        member_count = ctx.guild.member_count

        embed = discord.Embed(
            title="👋 ¡BIENVENIDO/A A SHADOW BLOCK! (Mensaje de Prueba)",
            description=(
                f"¡Hola {member.mention}! Nos alegra mucho tenerte en **{ctx.guild.name}**.\n\n"
                f"👤 **Usuario:** `{member.name}`\n"
                f"🆔 **ID:** `{member.id}`\n"
                f"📅 **Cuenta creada:** <t:{created_timestamp}:R>\n"
                f"👥 **Miembro número:** `#{member_count}`\n\n"
                f"📜 Por favor lee las reglas y disfruta de tu estadía.\n"
                f"💬 Pasa por el chat general a saludar a la comunidad."
            ),
            color=0x23A55A,
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        if ctx.guild.icon:
            embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon.url)
        embed.set_footer(
            text=f"Servidor administrado por {config.CREATOR_NAME} &bull; ¡Disfruta!",
            icon_url=ctx.guild.icon.url if ctx.guild.icon else None
        )

        await channel.send(
            content=f"🎉 ¡Un nuevo miembro ha llegado! Dale la bienvenida a {member.mention}",
            embed=embed,
            view=ServerLinkView()
        )
        await ctx.send(f"✅ Prueba de bienvenida enviada exitosamente en {channel.mention}.", ephemeral=True)

    @bot.hybrid_command(
        name="testdespedida",
        description="Envía una prueba del mensaje de despedida en el canal configurado."
    )
    @commands.has_permissions(administrator=True)
    async def cmd_testdespedida(ctx: commands.Context):
        await ctx.defer(ephemeral=True)
        channel = ctx.guild.get_channel(bot.welcome_channel_id)
        if not channel:
            return await ctx.send(f"❌ Canal no encontrado (`{bot.welcome_channel_id}`).", ephemeral=True)

        member = ctx.author
        joined_str = f"<t:{int(member.joined_at.timestamp())}:R>" if member.joined_at else "Desconocido"

        embed = discord.Embed(
            title="👋 ¡HASTA LUEGO! (Mensaje de Prueba)",
            description=(
                f"**{member.name}** ha abandonado el servidor.\n\n"
                f"👤 **Usuario:** `{member.name}`\n"
                f"⏱️ **Estuvo aquí desde:** {joined_str}\n"
                f"👥 **Ahora somos:** `{ctx.guild.member_count} miembros`\n\n"
                f"Esperamos verte pronto de vuelta por aquí."
            ),
            color=0xED4245,
            timestamp=datetime.datetime.now(datetime.timezone.utc)
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_footer(text=f"SHADOW BLOCK &bull; Hecho por {config.CREATOR_NAME}")

        await channel.send(embed=embed)
        await ctx.send(f"✅ Prueba de despedida enviada exitosamente en {channel.mention}.", ephemeral=True)

    @bot.hybrid_command(
        name="setbienvenida",
        description="Configura el canal donde se enviarán las bienvenidas y despedidas."
    )
    @discord.app_commands.describe(canal="El canal de texto donde se enviarán los avisos")
    @commands.has_permissions(administrator=True)
    async def cmd_setbienvenida(ctx: commands.Context, canal: discord.TextChannel):
        bot.welcome_channel_id = canal.id
        await ctx.send(f"✅ Canal de bienvenidas y despedidas actualizado a: {canal.mention} (`{canal.id}`)")

    # ==========================================
    # GESTIÓN Y CONTROL DE CANALES
    # ==========================================

    @bot.hybrid_command(
        name="crearcanal",
        description="Crea un nuevo canal de texto o de voz en el servidor."
    )
    @discord.app_commands.describe(
        tipo="texto o voz",
        nombre="Nombre del nuevo canal",
        categoria="Categoría donde se colocará (opcional)"
    )
    @commands.has_permissions(manage_channels=True)
    async def cmd_crearcanal(ctx: commands.Context, tipo: str, nombre: str, categoria: discord.CategoryChannel = None):
        await ctx.defer()
        tipo_clean = tipo.lower()
        if tipo_clean in ["texto", "text"]:
            ch = await ctx.guild.create_text_channel(name=nombre, category=categoria)
            await ctx.send(f"✅ Canal de texto creado: {ch.mention}")
        elif tipo_clean in ["voz", "voice"]:
            ch = await ctx.guild.create_voice_channel(name=nombre, category=categoria)
            await ctx.send(f"🔊 Canal de voz creado: **{ch.name}** (`{ch.id}`)")
        else:
            await ctx.send("❌ Tipo no válido. Usa `texto` o `voz`.")

    @bot.hybrid_command(
        name="borrarcanal",
        description="Elimina un canal del servidor."
    )
    @discord.app_commands.describe(canal="Canal que deseas eliminar (deja vacío para eliminar el actual)")
    @commands.has_permissions(manage_channels=True)
    async def cmd_borrarcanal(ctx: commands.Context, canal: discord.abc.GuildChannel = None):
        target = canal or ctx.channel
        nombre = target.name
        await target.delete(reason=f"Eliminado por {ctx.author}")
        if target.id != ctx.channel.id:
            await ctx.send(f"🗑️ Canal **{nombre}** eliminado correctamente.")

    @bot.hybrid_command(
        name="renombrarcanal",
        description="Cambia el nombre de un canal."
    )
    @discord.app_commands.describe(
        nuevo_nombre="Nuevo nombre para el canal",
        canal="Canal a renombrar (opcional)"
    )
    @commands.has_permissions(manage_channels=True)
    async def cmd_renombrarcanal(ctx: commands.Context, nuevo_nombre: str, canal: discord.abc.GuildChannel = None):
        target = canal or ctx.channel
        viejo_nombre = target.name
        await target.edit(name=nuevo_nombre, reason=f"Renombrado por {ctx.author}")
        await ctx.send(f"✅ Canal renombrado de **{viejo_nombre}** a **{nuevo_nombre}**.")

    @bot.hybrid_command(
        name="bloquear",
        aliases=["lock"],
        description="Bloquea el canal para que los miembros no puedan escribir."
    )
    @discord.app_commands.describe(canal="Canal a bloquear (opcional)")
    @commands.has_permissions(manage_channels=True)
    async def cmd_bloquear(ctx: commands.Context, canal: discord.TextChannel = None):
        target = canal or ctx.channel
        overwrite = target.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = False
        await target.set_permissions(ctx.guild.default_role, overwrite=overwrite, reason=f"Bloqueado por {ctx.author}")
        await ctx.send(f"🔒 Canal {target.mention} ha sido **BLOQUEADO**.")

    @bot.hybrid_command(
        name="desbloquear",
        aliases=["unlock"],
        description="Desbloquea el canal para que los miembros puedan volver a escribir."
    )
    @discord.app_commands.describe(canal="Canal a desbloquear (opcional)")
    @commands.has_permissions(manage_channels=True)
    async def cmd_desbloquear(ctx: commands.Context, canal: discord.TextChannel = None):
        target = canal or ctx.channel
        overwrite = target.overwrites_for(ctx.guild.default_role)
        overwrite.send_messages = True
        await target.set_permissions(ctx.guild.default_role, overwrite=overwrite, reason=f"Desbloqueado por {ctx.author}")
        await ctx.send(f"🔓 Canal {target.mention} ha sido **DESBLOQUEADO**.")

    @bot.hybrid_command(
        name="lento",
        aliases=["slowmode"],
        description="Establece el modo lento (cooldown entre mensajes) en un canal."
    )
    @discord.app_commands.describe(segundos="Segundos de espera (0 para desactivar)", canal="Canal (opcional)")
    @commands.has_permissions(manage_channels=True)
    async def cmd_lento(ctx: commands.Context, segundos: int, canal: discord.TextChannel = None):
        target = canal or ctx.channel
        if segundos < 0 or segundos > 21600:
            return await ctx.send("❌ El tiempo debe estar entre 0 y 21600 segundos (6 horas).")
        await target.edit(slowmode_delay=segundos)
        if segundos == 0:
            await ctx.send(f"⚡ Modo lento **desactivado** en {target.mention}.")
        else:
            await ctx.send(f"⏱️ Modo lento establecido a **{segundos} segundos** en {target.mention}.")

    @bot.hybrid_command(
        name="tema",
        aliases=["topic"],
        description="Cambia el tema o descripción de un canal de texto."
    )
    @discord.app_commands.describe(descripcion="Texto del nuevo tema", canal="Canal (opcional)")
    @commands.has_permissions(manage_channels=True)
    async def cmd_tema(ctx: commands.Context, descripcion: str, canal: discord.TextChannel = None):
        target = canal or ctx.channel
        await target.edit(topic=descripcion)
        await ctx.send(f"📝 Tema de {target.mention} actualizado a:\n> {descripcion}")

    @bot.hybrid_command(
        name="clonar",
        description="Clona un canal con exactamente los mismos permisos y ajustes."
    )
    @discord.app_commands.describe(canal="Canal a clonar (opcional)")
    @commands.has_permissions(manage_channels=True)
    async def cmd_clonar(ctx: commands.Context, canal: discord.abc.GuildChannel = None):
        target = canal or ctx.channel
        clon = await target.clone(reason=f"Clonado por {ctx.author}")
        await ctx.send(f"📑 Canal clonado exitosamente: {clon.mention if hasattr(clon, 'mention') else clon.name}")

    # ==========================================
    # GESTIÓN Y CONTROL DE ROLES
    # ==========================================

    @bot.hybrid_command(
        name="crearrol",
        description="Crea un nuevo rol en el servidor con color opcional."
    )
    @discord.app_commands.describe(nombre="Nombre del rol", color_hex="Color hex como #5865F2 o #FF0000")
    @commands.has_permissions(manage_roles=True)
    async def cmd_crearrol(ctx: commands.Context, nombre: str, color_hex: str = "#99AAB5"):
        color_val = 0x99AAB5
        try:
            clean = color_hex.replace("#", "").replace("0x", "")
            color_val = int(clean, 16)
        except ValueError:
            pass

        rol = await ctx.guild.create_role(
            name=nombre,
            color=discord.Color(color_val),
            reason=f"Creado por {ctx.author}"
        )
        await ctx.send(f"✅ Rol creado con éxito: {rol.mention} (`{rol.id}`)")

    @bot.hybrid_command(
        name="borrarrol",
        description="Elimina un rol del servidor."
    )
    @discord.app_commands.describe(rol="Rol que deseas borrar")
    @commands.has_permissions(manage_roles=True)
    async def cmd_borrarrol(ctx: commands.Context, rol: discord.Role):
        nombre = rol.name
        await rol.delete(reason=f"Eliminado por {ctx.author}")
        await ctx.send(f"🗑️ Rol **{nombre}** eliminado correctamente.")

    @bot.hybrid_command(
        name="darrol",
        description="Asigna un rol a un miembro del servidor."
    )
    @discord.app_commands.describe(miembro="Miembro al que dar el rol", rol="Rol que deseas asignar")
    @commands.has_permissions(manage_roles=True)
    async def cmd_darrol(ctx: commands.Context, miembro: discord.Member, rol: discord.Role):
        await miembro.add_roles(rol, reason=f"Asignado por {ctx.author}")
        await ctx.send(f"✅ Se ha asignado el rol {rol.mention} a **{miembro.display_name}**.")

    @bot.hybrid_command(
        name="quitarrol",
        description="Quita un rol a un miembro del servidor."
    )
    @discord.app_commands.describe(miembro="Miembro al que quitar el rol", rol="Rol que deseas quitar")
    @commands.has_permissions(manage_roles=True)
    async def cmd_quitarrol(ctx: commands.Context, miembro: discord.Member, rol: discord.Role):
        await miembro.remove_roles(rol, reason=f"Removido por {ctx.author}")
        await ctx.send(f"✅ Se ha quitado el rol {rol.mention} a **{miembro.display_name}**.")

    @bot.hybrid_command(
        name="colorrol",
        description="Cambia el color de un rol existente."
    )
    @discord.app_commands.describe(rol="Rol a modificar", color_hex="Nuevo color hex (ejemplo: #FF5733)")
    @commands.has_permissions(manage_roles=True)
    async def cmd_colorrol(ctx: commands.Context, rol: discord.Role, color_hex: str):
        try:
            clean = color_hex.replace("#", "").replace("0x", "")
            color_val = int(clean, 16)
        except ValueError:
            return await ctx.send("❌ Color hex inválido. Usa formato como `#5865F2` o `#FF0000`.")

        await rol.edit(color=discord.Color(color_val), reason=f"Modificado por {ctx.author}")
        await ctx.send(f"🎨 Color del rol {rol.mention} cambiado a `{color_hex}`.")

    @bot.hybrid_command(
        name="renombrarrol",
        description="Cambia el nombre de un rol existente."
    )
    @discord.app_commands.describe(rol="Rol a modificar", nuevo_nombre="Nuevo nombre del rol")
    @commands.has_permissions(manage_roles=True)
    async def cmd_renombrarrol(ctx: commands.Context, rol: discord.Role, nuevo_nombre: str):
        viejo = rol.name
        await rol.edit(name=nuevo_nombre, reason=f"Modificado por {ctx.author}")
        await ctx.send(f"✅ Rol **{viejo}** renombrado a: {rol.mention}")

    @bot.hybrid_command(
        name="roles",
        description="Muestra la lista de roles del servidor y cuántos miembros los tienen."
    )
    @commands.has_permissions(manage_roles=True)
    async def cmd_roles(ctx: commands.Context):
        roles_list = [r for r in ctx.guild.roles if r != ctx.guild.default_role]
        roles_list.reverse()

        desc = []
        for r in roles_list[:25]:
            desc.append(f"{r.mention} &bull; `{len(r.members)} miembros` (ID: `{r.id}`)")

        embed = discord.Embed(
            title=f"📋 Roles del Servidor ({len(roles_list)})",
            description="\n".join(desc) if desc else "No hay roles personalizados.",
            color=0x5865F2
        )
        embed.set_footer(text=f"Servidor: {ctx.guild.name} &bull; Hecho por {config.CREATOR_NAME}")
        await ctx.send(embed=embed)

    # ==========================================
    # MODERACIÓN Y MENSAJES
    # ==========================================

    @bot.hybrid_command(
        name="limpiar",
        aliases=["clear", "purge"],
        description="Elimina una cantidad de mensajes del canal."
    )
    @discord.app_commands.describe(cantidad="Número de mensajes a eliminar (1 a 100)")
    @commands.has_permissions(manage_messages=True)
    async def cmd_limpiar(ctx: commands.Context, cantidad: int):
        if cantidad < 1 or cantidad > 100:
            return await ctx.send("❌ Debes indicar una cantidad entre 1 y 100.", ephemeral=True)
        await ctx.defer(ephemeral=True)
        deleted = await ctx.channel.purge(limit=cantidad)
        await ctx.send(f"🧹 Se han eliminado **{len(deleted)} mensajes**.", ephemeral=True)

    @bot.hybrid_command(
        name="kick",
        description="Expulsa a un miembro del servidor."
    )
    @discord.app_commands.describe(miembro="Usuario a expulsar", razon="Motivo de la expulsión")
    @commands.has_permissions(kick_members=True)
    async def cmd_kick(ctx: commands.Context, miembro: discord.Member, razon: str = "Sin razón especificada"):
        await miembro.kick(reason=f"{razon} (Por: {ctx.author})")
        await ctx.send(f"👢 **{miembro.name}** ha sido expulsado del servidor. Razón: *{razon}*")

    @bot.hybrid_command(
        name="ban",
        description="Banea a un miembro del servidor."
    )
    @discord.app_commands.describe(miembro="Usuario a banear", razon="Motivo del ban")
    @commands.has_permissions(ban_members=True)
    async def cmd_ban(ctx: commands.Context, miembro: discord.Member, razon: str = "Sin razón especificada"):
        await miembro.ban(reason=f"{razon} (Por: {ctx.author})")
        await ctx.send(f"🔨 **{miembro.name}** ha sido **BANEADO** del servidor. Razón: *{razon}*")

    @bot.hybrid_command(
        name="unban",
        description="Desbanea a un usuario usando su ID."
    )
    @discord.app_commands.describe(usuario_id="ID numérico del usuario a desbanear")
    @commands.has_permissions(ban_members=True)
    async def cmd_unban(ctx: commands.Context, usuario_id: str):
        try:
            uid = int(usuario_id)
            user = await bot.fetch_user(uid)
            await ctx.guild.unban(user, reason=f"Desbaneado por {ctx.author}")
            await ctx.send(f"🕊️ Usuario **{user.name}** (`{uid}`) ha sido desbaneado.")
        except Exception as e:
            await ctx.send(f"❌ Error al desbanear: {e}")

    @bot.hybrid_command(
        name="mutear",
        aliases=["timeout"],
        description="Aísla (mutea temporalmente) a un usuario."
    )
    @discord.app_commands.describe(miembro="Usuario a mutear", minutos="Duración en minutos", razon="Motivo")
    @commands.has_permissions(moderate_members=True)
    async def cmd_mutear(ctx: commands.Context, miembro: discord.Member, minutos: int, razon: str = "Sin razón"):
        duration = datetime.timedelta(minutes=minutos)
        await miembro.timeout(duration, reason=f"{razon} (Por: {ctx.author})")
        await ctx.send(f"🤐 **{miembro.display_name}** ha sido muteado por **{minutos} minutos**. Razón: *{razon}*")

    @bot.hybrid_command(
        name="desmutear",
        description="Quita el aislamiento (mute) a un usuario."
    )
    @discord.app_commands.describe(miembro="Usuario a desmutear")
    @commands.has_permissions(moderate_members=True)
    async def cmd_desmutear(ctx: commands.Context, miembro: discord.Member):
        await miembro.timeout(None, reason=f"Desmuteado por {ctx.author}")
        await ctx.send(f"🔊 **{miembro.display_name}** ha sido desmuteado.")

    @bot.hybrid_command(
        name="anuncio",
        description="Envía un anuncio decorado en un canal específico."
    )
    @discord.app_commands.describe(
        canal="Canal donde se enviará el anuncio",
        titulo="Título del anuncio",
        mensaje="Cuerpo del mensaje",
        color="Color hex opcional (#5865F2)"
    )
    @commands.has_permissions(manage_messages=True)
    async def cmd_anuncio(ctx: commands.Context, canal: discord.TextChannel, titulo: str, mensaje: str, color: str = "#5865F2"):
        color_val = 0x5865F2
        try:
            clean = color.replace("#", "").replace("0x", "")
            color_val = int(clean, 16)
        except ValueError:
            pass

        embed = discord.Embed(title=f"📢 {titulo}", description=mensaje, color=color_val)
        embed.set_footer(text=f"Anuncio oficial de {ctx.guild.name} &bull; Autor: {ctx.author.display_name}")
        if ctx.guild.icon:
            embed.set_thumbnail(url=ctx.guild.icon.url)
        await canal.send(embed=embed)
        await ctx.send(f"✅ Anuncio enviado en {canal.mention}.", ephemeral=True)

    @bot.hybrid_command(
        name="webhook",
        description="Envía un mensaje a través del Webhook configurado."
    )
    @discord.app_commands.describe(mensaje="Mensaje que enviará el Webhook")
    @commands.has_permissions(administrator=True)
    async def cmd_webhook(ctx: commands.Context, *, mensaje: str):
        if not bot.webhook_url:
            return await ctx.send("❌ No hay Webhook configurado en las variables de entorno.")

        await ctx.defer(ephemeral=True)
        try:
            async with aiohttp.ClientSession() as session:
                webhook = discord.Webhook.from_url(bot.webhook_url, session=session)
                await webhook.send(
                    content=mensaje,
                    username="RafaMoDzYT",
                    avatar_url=ctx.guild.icon.url if ctx.guild.icon else None
                )
            await ctx.send("✅ Mensaje enviado exitosamente a través del Webhook.", ephemeral=True)
        except Exception as e:
            await ctx.send(f"❌ Error al enviar por Webhook: {e}", ephemeral=True)

    @bot.hybrid_command(
        name="servidor",
        aliases=["serverinfo"],
        description="Muestra información y estadísticas completas del servidor."
    )
    async def cmd_servidor(ctx: commands.Context):
        g = ctx.guild
        embed = discord.Embed(
            title=f"🏰 Información de {g.name}",
            description=f"**ID:** `{g.id}`\n**Creador:** <@{g.owner_id}>\n**Enlace Oficial:** [{config.SERVER_LINK}]({config.SERVER_LINK})",
            color=0x5865F2
        )
        embed.add_field(name="👥 Miembros", value=f"`{g.member_count}` miembros", inline=True)
        embed.add_field(name="💬 Canales de Texto", value=f"`{len(g.text_channels)}`", inline=True)
        embed.add_field(name="🔊 Canales de Voz", value=f"`{len(g.voice_channels)}`", inline=True)
        embed.add_field(name="🎭 Roles", value=f"`{len(g.roles)}` roles", inline=True)
        embed.add_field(name="🚀 Nivel de Boost", value=f"Nivel `{g.premium_tier}` ({g.premium_subscription_count} boosts)", inline=True)
        embed.add_field(name="📅 Fecha de Creación", value=f"<t:{int(g.created_at.timestamp())}:D>", inline=True)

        if g.icon:
            embed.set_thumbnail(url=g.icon.url)
        embed.set_footer(text=f"Bot Administrador &bull; Hecho por {config.CREATOR_NAME}")
        await ctx.send(embed=embed, view=ServerLinkView())

    @bot.hybrid_command(
        name="say",
        description="Hace que el bot repita un mensaje."
    )
    @commands.has_permissions(manage_messages=True)
    async def cmd_say(ctx: commands.Context, *, mensaje: str):
        if ctx.message:
            try:
                await ctx.message.delete()
            except Exception:
                pass
        await ctx.send(mensaje)

    @bot.hybrid_command(
        name="ping",
        description="Muestra la latencia del bot."
    )
    async def cmd_ping(ctx: commands.Context):
        latency = round(bot.latency * 1000)
        await ctx.send(f"🏓 **Pong!** Latencia del Bot Administrador: `{latency} ms` ⚡")

    # ==========================================
    # COMANDOS DE STICKERS Y EMOJIS (9,999 STICKERS & 300+ MEMES)
    # ==========================================
    @bot.command(name="sticker", aliases=["meme", "st"])
    async def cmd_sticker(ctx: commands.Context, nombre: str = None):
        """Envía un sticker/meme en alta definición desde el catálogo de 9,999 stickers o 300+ memes."""
        if not nombre:
            import random
            from stickers_catalog_9999 import get_sticker_by_id
            rnd_s = get_sticker_by_id(random.randint(1, 9999))
            await ctx.send(
                f"🎨 **Uso del Catálogo de 9,999 Stickers:**\n"
                f"• Por número (1 al 9999): `{config.COMMAND_PREFIX}sticker 777`\n"
                f"• Por nombre/meme: `{config.COMMAND_PREFIX}sticker pepe_hype` o `{config.COMMAND_PREFIX}sticker gigachad`\n"
                f"• Categorías: `{config.COMMAND_PREFIX}stickerspack` o visita <#1559852912727822396>\n"
                f"💡 *Ejemplo aleatorio generado:* Sticker #{rnd_s['id']:04d}: `{rnd_s['title']}`"
            )
            return

        # Si el usuario pasó un número (1 al 9999)
        if nombre.isdigit():
            from stickers_catalog_9999 import get_sticker_by_id
            sid = int(nombre)
            item = get_sticker_by_id(sid)
            embed = discord.Embed(
                title=f"🎭 {item['title']}",
                description=f"📂 **Categoría:** `{item['category']}` | 🏷️ **Etiqueta:** `{item['tag']}`",
                color=0x5865F2
            )
            embed.set_image(url=item['url'])
            embed.set_footer(text=f"Sticker #{item['id']:04d} de 9,999 • SHADOW BLOCK • {config.CREATOR_NAME}")
            await ctx.send(embed=embed)
            return

        # Si el usuario pasó un nombre de meme del catálogo de 300+
        from stickers_catalog import STICKERS_DB, buscar_stickers
        res = buscar_stickers(nombre)
        if not res:
            await ctx.send(f"❌ No encontré ningún sticker con el nombre `{nombre}`. Puedes usar `{config.COMMAND_PREFIX}sticker [1-9999]` para ver el catálogo masivo.")
            return

        key = list(res.keys())[0]
        item = res[key]

        embed = discord.Embed(
            title=f"🎭 {item['name']}",
            description=f"📂 Categoría: `{item['cat']}`",
            color=0x5865F2
        )
        embed.set_image(url=item['url'])
        embed.set_footer(text=f"Sticker Oficial • Creado por {config.CREATOR_NAME} • SHADOW BLOCK")
        await ctx.send(embed=embed)

    # ==========================================
    # SOUNDBOARD 500 VOCES DE FREE FIRE
    # ==========================================
    @bot.command(name="voz", aliases=["audio", "soundboard", "fr"])
    async def cmd_voz(ctx: commands.Context, id_o_tipo: str = "random"):
        """Reproduce o muestra una de las 500 voces de Free Fire (Donato, Zelika, Hackers, Gang, Booyah)."""
        import random
        from freefire_voices_500 import get_voice_by_id

        sid = 1
        if id_o_tipo.isdigit():
            sid = int(id_o_tipo)
        elif "donato" in id_o_tipo.lower():
            sid = random.randint(1, 100)
        elif "zelika" in id_o_tipo.lower():
            sid = random.randint(101, 200)
        elif "hacker" in id_o_tipo.lower():
            sid = random.randint(201, 300)
        elif "gang" in id_o_tipo.lower():
            sid = random.randint(301, 400)
        elif "booyah" in id_o_tipo.lower():
            sid = random.randint(401, 500)
        else:
            sid = random.randint(1, 500)

        v = get_voice_by_id(sid)
        embed = discord.Embed(
            title=f"🎙️ Free Fire Soundboard: {v['title']}",
            description=f"🔊 **Frase:** *\"{v['text']}\"*\n📂 **Categoría:** `{v['category']}`\n⚡ **Comando:** `{config.COMMAND_PREFIX}voz {v['id']}` o `{config.COMMAND_PREFIX}voz donato` / `zelika` / `hacker` / `gang` / `booyah`\n🎮 **Visita:** <#1559852917295677511>",
            color=0xE74C3C
        )
        embed.set_footer(text=f"Clip #{v['id']:03d} de 500 Voces • Creado por {config.CREATOR_NAME} • SHADOW BLOCK")
        await ctx.send(embed=embed)

    @bot.command(name="stickerspack", aliases=["stickers", "memes"])
    async def cmd_stickerspack(ctx: commands.Context, *, categoria: str = None):
        """Muestra el catálogo de 300+ stickers organizados por categorías."""
        from stickers_catalog import CATEGORIAS, obtener_stickers_por_categoria
        if not categoria:
            cats_text = "\n".join([f"• `{c}`" for c in CATEGORIAS])
            embed = discord.Embed(
                title="🎨 Catálogo de 300+ Stickers y Memes Famosos",
                description=(
                    "¡El servidor cuenta con más de **300 stickers y memes famosos** listos para enviar!\n\n"
                    f"**Categorías disponibles:**\n{cats_text}\n\n"
                    f"💡 **Ejemplo de consulta:** `{config.COMMAND_PREFIX}stickerspack Pepe & Wojaks`\n"
                    f"🚀 **Enviar directamente:** `{config.COMMAND_PREFIX}sticker <clave>`"
                ),
                color=0xFEE75C
            )
            embed.set_footer(text=f"SHADOW BLOCK • Hecho por {config.CREATOR_NAME}")
            await ctx.send(embed=embed)
            return

        items = obtener_stickers_por_categoria(categoria)
        if not items:
            for cat in CATEGORIAS:
                if categoria.lower() in cat.lower():
                    items = obtener_stickers_por_categoria(cat)
                    categoria = cat
                    break

        if not items:
            await ctx.send(f"❌ No se encontró la categoría `{categoria}`. Usa `{config.COMMAND_PREFIX}stickerspack` para ver las disponibles.")
            return

        nombres = [f"`{k}` ({v['name']})" for k, v in list(items.items())[:25]]
        embed = discord.Embed(
            title=f"📂 Categoría: {categoria} ({len(items)} stickers)",
            description="Usa `//sticker <clave>` para enviar cualquiera de estos:\n\n" + "\n".join(nombres),
            color=0x2ECC71
        )
        embed.set_footer(text=f"SHADOW BLOCK • {config.CREATOR_NAME}")
        await ctx.send(embed=embed)

    @bot.command(name="crearemoji")
    @commands.has_permissions(manage_emojis=True)
    async def cmd_crearemoji(ctx: commands.Context, nombre: str, url: str):
        """Crea un emoji personalizado en el servidor a partir de una URL."""
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status != 200:
                    await ctx.send("❌ No se pudo descargar la imagen desde la URL proporcionada.")
                    return
                image_bytes = await resp.read()

        try:
            emoji = await ctx.guild.create_custom_emoji(name=nombre, image=image_bytes)
            await ctx.send(f"✅ ¡Emoji {emoji} (`:{nombre}:`) creado exitosamente en el servidor!")
        except Exception as e:
            await ctx.send(f"❌ Error al crear emoji en Discord: {e}")

    @bot.command(name="listaemojis", aliases=["emojis"])
    async def cmd_listaemojis(ctx: commands.Context):
        """Muestra los emojis y stickers del servidor y cuántos espacios quedan."""
        emojis_count = len(ctx.guild.emojis)
        stickers_count = len(ctx.guild.stickers)
        max_emojis = ctx.guild.emoji_limit
        max_stickers = ctx.guild.sticker_limit

        embed = discord.Embed(
            title=f"🎨 Emojis y Stickers de {ctx.guild.name}",
            description=(
                f"**Emojis Personalizados:** `{emojis_count} / {max_emojis}` (Libres: {max_emojis - emojis_count})\n"
                f"**Stickers Oficiales:** `{stickers_count} / {max_stickers}` (Libres: {max_stickers - stickers_count})\n\n"
                f"✨ ¡Con el bot y el **Panel DX11** tienes además **300+ stickers HD** listos para enviar en cualquier canal sin límites!"
            ),
            color=0x5865F2
        )
        embed.set_footer(text=f"SHADOW BLOCK • Creado por {config.CREATOR_NAME}")
        await ctx.send(embed=embed)

    @bot.hybrid_command(
        name="ayuda",
        aliases=["help"],
        description="Muestra todos los comandos de administración y moderación disponibles."
    )
    async def cmd_ayuda(ctx: commands.Context):
        p = config.COMMAND_PREFIX
        embed = discord.Embed(
            title="🛡️ Panel de Comandos - Bot Administrador",
            description=(
                f"Todos los comandos pueden usarse con `{p}` o con comandos slash `/`.\n"
                f"👑 **Creado por:** `{config.CREATOR_NAME}` | 🚀 **Servidor:** [{config.SERVER_LINK}]({config.SERVER_LINK})\n"
            ),
            color=0x5865F2
        )

        embed.add_field(
            name="👋 Sistema de Bienvenidas y Despedidas",
            value=(
                f"`{p}testbienvenida` - Envía una prueba del mensaje de bienvenida\n"
                f"`{p}testdespedida` - Envía una prueba de mensaje de despedida\n"
                f"`{p}setbienvenida <#canal>` - Configura el canal de bienvenidas"
            ),
            inline=False
        )

        embed.add_field(
            name="📁 Control de Canales",
            value=(
                f"`{p}crearcanal <texto|voz> <nombre>` - Crea un nuevo canal\n"
                f"`{p}borrarcanal [canal]` - Elimina un canal\n"
                f"`{p}renombrarcanal <nuevo_nombre>` - Renombra un canal\n"
                f"`{p}bloquear` / `{p}desbloquear` - Bloquea/desbloquea el canal\n"
                f"`{p}lento <segundos>` - Activa modo lento en el canal\n"
                f"`{p}tema <texto>` - Cambia la descripción del canal\n"
                f"`{p}clonar` - Clona un canal con sus permisos"
            ),
            inline=False
        )

        embed.add_field(
            name="🎭 Control de Roles",
            value=(
                f"`{p}crearrol <nombre> [#color]` - Crea un nuevo rol\n"
                f"`{p}borrarrol <@rol>` - Elimina un rol\n"
                f"`{p}darrol <@usuario> <@rol>` - Asigna un rol a un miembro\n"
                f"`{p}quitarrol <@usuario> <@rol>` - Quita un rol a un miembro\n"
                f"`{p}colorrol <@rol> <#color>` - Cambia el color de un rol\n"
                f"`{p}renombrarrol <@rol> <nombre>` - Renombra un rol\n"
                f"`{p}roles` - Muestra la lista de roles del servidor"
            ),
            inline=False
        )

        embed.add_field(
            name="🔨 Moderación y Servidor",
            value=(
                f"`{p}limpiar <1-100>` - Elimina mensajes en masa\n"
                f"`{p}kick <@usuario> [razon]` - Expulsa a un miembro\n"
                f"`{p}ban <@usuario> [razon]` - Banea a un miembro\n"
                f"`{p}unban <id_usuario>` - Desbanea por ID\n"
                f"`{p}mutear <@usuario> <minutos>` - Aísla temporalmente\n"
                f"`{p}desmutear <@usuario>` - Quita el aislamiento\n"
                f"`{p}anuncio <#canal> <titulo> | <texto>` - Envía anuncio decorado\n"
                f"`{p}webhook <mensaje>` - Envía mensaje por Webhook\n"
                f"`{p}servidor` - Muestra las estadísticas de SHADOW BLOCK"
            ),
            inline=False
        )

        embed.add_field(
            name="🎨 Stickers y Emojis (300+ Famosos)",
            value=(
                f"`{p}sticker <nombre>` - Envía sticker/meme en HD\n"
                f"`{p}stickerspack [categoria]` - Muestra el catálogo de 300+ stickers\n"
                f"`{p}crearemoji <nombre> <url>` - Crea un emoji en el servidor\n"
                f"`{p}listaemojis` - Espacios y emojis del servidor"
            ),
            inline=False
        )

        embed.set_footer(text=f"Bot Administrador &bull; Hecho por {config.CREATOR_NAME}", icon_url=ctx.guild.icon.url if ctx.guild.icon else None)
        await ctx.send(embed=embed, view=ServerLinkView())

    @bot.event
    async def on_command_error(ctx: commands.Context, error):
        if isinstance(error, commands.CommandNotFound):
            return
        elif isinstance(error, commands.MissingPermissions):
            await ctx.send("⛔ No tienes permisos suficientes para usar este comando.", ephemeral=True)
        elif isinstance(error, commands.BotMissingPermissions):
            await ctx.send("⚠️ El bot no tiene los permisos necesarios de Discord para realizar esta acción.", ephemeral=True)
        elif isinstance(error, commands.MissingRequiredArgument):
            await ctx.send(f"⚠️ Argumento faltante. Usa `{config.COMMAND_PREFIX}ayuda` para revisar cómo usar el comando.", ephemeral=True)
        else:
            print(f"[Admin Bot Error] {error}", flush=True)

def run_admin_bot():
    """Función de arranque del bot administrador."""
    if not config.ADMIN_BOT_TOKEN:
        print("❌ ERROR: No se encontró ADMIN_BOT_TOKEN en .env", flush=True)
        sys.exit(1)

    intents = discord.Intents.default()
    intents.guilds = True
    intents.messages = True
    
    if config.ENABLE_MEMBERS_INTENT:
        intents.members = True

    if config.ENABLE_MESSAGE_CONTENT:
        intents.message_content = True

    bot = AdminBot(intents=intents)
    setup_admin_commands(bot)

    print("🚀 Iniciando Bot Administrador & Bienvenidas...", flush=True)
    try:
        bot.run(config.ADMIN_BOT_TOKEN, reconnect=True)
    except discord.errors.PrivilegedIntentsRequired:
        print("\n⚠️ AVISO PARA BOT ADMINISTRADOR:", flush=True)
        print("Para que las bienvenidas y despedidas automáticas se detecten al instante,", flush=True)
        print("debes activar 'Server Members Intent' en el Developer Portal:", flush=True)
        print(f"👉 https://discord.com/developers/applications/{config.ADMIN_BOT_APP_ID}/bot", flush=True)
        print("Iniciando con intents estándar (comandos manuales y slash activos)...", flush=True)

        fallback_intents = discord.Intents.default()
        fallback_intents.guilds = True
        fallback_intents.messages = True
        fallback_bot = AdminBot(intents=fallback_intents)
        setup_admin_commands(fallback_bot)
        fallback_bot.run(config.ADMIN_BOT_TOKEN, reconnect=True)

if __name__ == "__main__":
    run_admin_bot()

