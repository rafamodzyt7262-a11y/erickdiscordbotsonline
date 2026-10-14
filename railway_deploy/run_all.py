import asyncio
import subprocess
import sys
import time
import config
from keep_alive import start_keep_alive

if sys.platform == "win32":
    try:
        sys.stdout.reconfigure(encoding='utf-8', errors='replace')
        sys.stderr.reconfigure(encoding='utf-8', errors='replace')
    except Exception:
        pass

async def run_process(cmd: list, name: str):
    """Ejecuta y supervisa un bot de Discord con auto-reinicio si se detiene."""
    while True:
        print(f"[{name}] Iniciando proceso...", flush=True)
        proc = await asyncio.create_subprocess_exec(
            *cmd,
            stdout=sys.stdout,
            stderr=sys.stderr
        )
        await proc.wait()
        print(f"[{name}] El proceso se detuvo (código {proc.returncode}). Reiniciando en 5 segundos...", flush=True)
        await asyncio.sleep(5)

async def main():
    print("==================================================", flush=True)
    print("🚀 INICIANDO SISTEMA MULTI-BOT DISCORD 24/7", flush=True)
    print(f"👑 Desarrollado por: {config.CREATOR_NAME}", flush=True)
    print("1️⃣ Bot 1: Erick x (Voz 24/7 & Meta 1M de Horas)")
    print("2️⃣ Bot 2: Administrador & Bienvenidas (SHADOW BLOCK)")
    print("==================================================", flush=True)

    # Iniciar servidor web de monitoreo para Railway / UptimeRobot
    start_keep_alive(port=config.PORT)

    python_exe = sys.executable

    task1 = asyncio.create_task(run_process([python_exe, "main.py"], "Erick x (Voz)"))
    task2 = asyncio.create_task(run_process([python_exe, "admin_bot.py"], "Admin Bot (Servidor)"))

    await asyncio.gather(task1, task2)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\nDeteniendo todos los bots...", flush=True)
