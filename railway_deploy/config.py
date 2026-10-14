import os
from pathlib import Path
from dotenv import load_dotenv

# Cargar variables de entorno desde .env
BASE_DIR = Path(__file__).resolve().parent
load_dotenv(BASE_DIR / ".env")

# Token y Credenciales - Bot 1 (Erick x)
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN", "").strip()
APPLICATION_ID = int(os.getenv("APPLICATION_ID", "1559437873265119252"))

ADMIN_BOT_TOKEN = os.getenv("ADMIN_BOT_TOKEN", "").strip()
ADMIN_BOT_APP_ID = int(os.getenv("ADMIN_BOT_APP_ID", "1559830923174744125"))
WELCOME_CHANNEL_ID = int(os.getenv("WELCOME_CHANNEL_ID", "1559359413402472488"))
WEBHOOK_URL = os.getenv("WEBHOOK_URL", "https://discord.com/api/webhooks/1559831359885680731/sknZANo0tcmUqcpUvMVaL32J9DJELoUxp4l9ynHQZJG4pNZGQJuzEDzUu3tkhqgvU0rm").strip()
SERVER_LINK = os.getenv("SERVER_LINK", "https://discord.gg/dc5HAzAMmg").strip()

# IDs de Discord
GUILD_ID = int(os.getenv("GUILD_ID", "1350706770527653989"))
VOICE_CHANNEL_ID = int(os.getenv("VOICE_CHANNEL_ID", "1350706770527653993"))
CONTROL_CHANNEL_ID = int(os.getenv("CONTROL_CHANNEL_ID", "1559826233620168734"))

# Prefijo y Textos
COMMAND_PREFIX = os.getenv("COMMAND_PREFIX", "//")
CREATOR_NAME = os.getenv("CREATOR_NAME", "rafamodzyt")
DISCORD_INVITE = os.getenv("DISCORD_INVITE", "https://discord.gg/dc5HAzAMmg")
ENABLE_MESSAGE_CONTENT = os.getenv("ENABLE_MESSAGE_CONTENT", "false").lower() in ("true", "1", "yes")
ENABLE_MEMBERS_INTENT = os.getenv("ENABLE_MEMBERS_INTENT", "false").lower() in ("true", "1", "yes")




# Puerto para servicio web (Railway)
PORT = int(os.getenv("PORT", "8080"))

# Meta de horas en canal de voz (1 millón de horas)
TARGET_HOURS = 1_000_000

# Rutas de datos
DATA_DIR = BASE_DIR / "data"
STATS_FILE = DATA_DIR / "stats.json"

DATA_DIR.mkdir(parents=True, exist_ok=True)
