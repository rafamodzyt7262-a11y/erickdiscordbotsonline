# -*- coding: utf-8 -*-
import os
import json
import time
import math
import logging
from threading import Thread
from flask import Flask, jsonify, request, send_from_directory, render_template_string
import requests

import config

# Silenciar logs ruidosos de werkzeug
log = logging.getLogger('werkzeug')
log.setLevel(logging.ERROR)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
WEB_DIR = os.path.join(BASE_DIR, "web_panel")
CHAT_LOGS_FILE = os.path.join(BASE_DIR, "data", "chat_logs.json")

app = Flask(__name__)

# Referencia al stats manager y al bot para mostrar datos en vivo
_stats_ref = None
_bot_ref = None
_start_time = time.time()

HTML_TEMPLATE = """
<!DOCTYPE html>
<html lang="es">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Erick x - Bot 24/7 Online</title>
    <link href="https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;800&family=JetBrains+Mono:wght@400;600&display=swap" rel="stylesheet">
    <style>
        :root {
            --bg: #090a0f;
            --card-bg: rgba(22, 27, 34, 0.7);
            --accent: #5865F2;
            --accent-glow: rgba(88, 101, 242, 0.35);
            --green: #23a55a;
            --green-glow: rgba(35, 165, 90, 0.4);
            --text-main: #f0f6fc;
            --text-sub: #8b949e;
            --border: rgba(255, 255, 255, 0.1);
        }
        * {
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }
        body {
            font-family: 'Outfit', -apple-system, BlinkMacSystemFont, sans-serif;
            background: radial-gradient(circle at 50% 10%, #171b2e 0%, var(--bg) 100%);
            color: var(--text-main);
            min-height: 100vh;
            display: flex;
            align-items: center;
            justify-content: center;
            padding: 20px;
        }
        .container {
            width: 100%;
            max-width: 620px;
            background: var(--card-bg);
            backdrop-filter: blur(16px);
            -webkit-backdrop-filter: blur(16px);
            border: 1px solid var(--border);
            border-radius: 24px;
            padding: 36px;
            box-shadow: 0 20px 50px rgba(0, 0, 0, 0.6), 0 0 30px var(--accent-glow);
            text-align: center;
            animation: fadeIn 0.8s ease;
        }
        @keyframes fadeIn {
            from { opacity: 0; transform: translateY(12px); }
            to { opacity: 1; transform: translateY(0); }
        }
        .badge {
            display: inline-flex;
            align-items: center;
            gap: 8px;
            background: rgba(35, 165, 90, 0.15);
            color: var(--green);
            border: 1px solid rgba(35, 165, 90, 0.3);
            border-radius: 999px;
            padding: 6px 16px;
            font-size: 0.85rem;
            font-weight: 600;
            letter-spacing: 0.5px;
            margin-bottom: 20px;
            box-shadow: 0 0 15px var(--green-glow);
        }
        .pulse {
            width: 8px;
            height: 8px;
            background: var(--green);
            border-radius: 50%;
            box-shadow: 0 0 8px var(--green);
            animation: pulse 1.5s infinite;
        }
        @keyframes pulse {
            0% { transform: scale(0.95); opacity: 0.8; }
            50% { transform: scale(1.4); opacity: 1; }
            100% { transform: scale(0.95); opacity: 0.8; }
        }
        h1 {
            font-size: 2.2rem;
            font-weight: 800;
            letter-spacing: -0.5px;
            margin-bottom: 8px;
        }
        .subtitle {
            color: var(--text-sub);
            font-size: 0.95rem;
            margin-bottom: 28px;
        }
        .grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 16px;
            margin-bottom: 24px;
            text-align: left;
        }
        .card {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 16px 18px;
        }
        .card-title {
            color: var(--text-sub);
            font-size: 0.75rem;
            text-transform: uppercase;
            letter-spacing: 0.5px;
            font-weight: 600;
            margin-bottom: 6px;
        }
        .card-value {
            font-family: 'JetBrains Mono', monospace;
            font-size: 1.3rem;
            font-weight: 600;
        }
        .progress-box {
            background: rgba(255, 255, 255, 0.03);
            border: 1px solid var(--border);
            border-radius: 16px;
            padding: 16px 20px;
            margin-bottom: 28px;
            text-align: left;
        }
        .progress-header {
            display: flex;
            justify-content: space-between;
            font-size: 0.85rem;
            color: var(--text-sub);
            margin-bottom: 10px;
        }
        .progress-bar-bg {
            height: 10px;
            background: rgba(255, 255, 255, 0.08);
            border-radius: 999px;
            overflow: hidden;
        }
        .progress-bar-fill {
            height: 100%;
            background: linear-gradient(90deg, #5865F2, #00F0FF);
            box-shadow: 0 0 12px rgba(88, 101, 242, 0.5);
            transition: width 0.5s ease;
        }
        .buttons {
            display: flex;
            flex-direction: column;
            gap: 12px;
        }
        .btn {
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 10px;
            background: var(--accent);
            color: #fff;
            text-decoration: none;
            padding: 14px 24px;
            border-radius: 14px;
            font-weight: 600;
            transition: 0.2s ease;
            box-shadow: 0 6px 20px var(--accent-glow);
        }
        .btn:hover {
            transform: translateY(-2px);
            box-shadow: 0 8px 25px rgba(88, 101, 242, 0.5);
        }
        .btn-panel {
            background: linear-gradient(135deg, #00F0FF, #5865F2);
            color: #fff;
            box-shadow: 0 6px 25px rgba(0, 240, 255, 0.4);
        }
        .btn-panel:hover {
            box-shadow: 0 8px 30px rgba(0, 240, 255, 0.6);
        }
        .footer {
            margin-top: 24px;
            font-size: 0.8rem;
            color: var(--text-sub);
        }
    </style>
</head>
<body>
    <div class="container">
        <div class="badge">
            <span class="pulse"></span>
            BOT ONLINE 24/7 SIN APAGARSE
        </div>

        <h1>Erick x</h1>
        <p class="subtitle">Bot 24/7 de voz y administración creado por <b>{{ creator }}</b></p>

        <div class="grid">
            <div class="card">
                <div class="card-title">Estado de Voz</div>
                <div class="card-value" style="color: {{ '#23a55a' if is_in_voice else '#faa61a' }};">
                    {{ 'Conectado 🟢' if is_in_voice else 'Reconectando...' }}
                </div>
            </div>
            <div class="card">
                <div class="card-title">Tiempo Online Total</div>
                <div class="card-value">{{ uptime_str }}</div>
            </div>
            <div class="card">
                <div class="card-title">Horas en Canal de Voz</div>
                <div class="card-value">{{ "%.2f"|format(voice_hours) }}h</div>
            </div>
            <div class="card">
                <div class="card-title">Latencia Bot</div>
                <div class="card-value">{{ ping_ms }} ms</div>
            </div>
        </div>

        <div class="progress-box">
            <div class="progress-header">
                <span>Meta: <b>1,000,000 de Horas</b></span>
                <span><b>{{ "%.4f"|format(pct) }}%</b> completado</span>
            </div>
            <div class="progress-bar-bg">
                <div class="progress-bar-fill" style="width: {{ pct if pct > 0.5 else 0.5 }}%;"></div>
            </div>
        </div>

        <div class="buttons">
            <a href="/" class="btn btn-panel">
                🚀 Entrar al Panel Web Completo (SHADOW BLOCK)
            </a>
            <a href="{{ invite_url }}" target="_blank" class="btn">
                <svg width="20" height="20" viewBox="0 0 24 24" fill="currentColor">
                    <path d="M20.317 4.37a19.791 19.791 0 0 0-4.885-1.515.074.074 0 0 0-.079.037c-.21.375-.444.864-.608 1.25a18.27 18.27 0 0 0-5.487 0 12.64 12.64 0 0 0-.617-1.25.077.077 0 0 0-.079-.037A19.736 19.736 0 0 0 3.677 4.37a.07.07 0 0 0-.032.027C.533 9.046-.32 13.58.099 18.057a.082.082 0 0 0 .031.057 19.9 19.9 0 0 0 5.993 3.03.078.078 0 0 0 .084-.028 14.09 14.09 0 0 0 1.226-1.994.076.076 0 0 0-.041-.106 13.107 13.107 0 0 1-1.872-.892.077.077 0 0 1-.008-.128 10.2 10.2 0 0 0 .372-.292.074.074 0 0 1 .077-.01c3.929 1.793 8.18 1.793 12.061 0a.074.074 0 0 1 .078.01c.12.098.246.198.373.292a.077.077 0 0 1-.006.127 12.299 12.299 0 0 1-1.873.893.077.077 0 0 0-.041.107c.36.698.772 1.362 1.225 1.993a.076.076 0 0 0 .084.028 19.839 19.839 0 0 0 6.002-3.03.077.077 0 0 0 .032-.054c.5-5.177-.838-9.674-3.549-13.66a.061.061 0 0 0-.031-.028zM8.02 15.33c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.956-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.956 2.418-2.157 2.418zm7.975 0c-1.183 0-2.157-1.085-2.157-2.419 0-1.333.955-2.419 2.157-2.419 1.21 0 2.176 1.096 2.157 2.42 0 1.333-.946 2.418-2.157 2.418z"/>
                </svg>
                Unirse a mi Discord
            </a>
        </div>

        <div class="footer">
            Bot Oficial Erick x &bull; Desarrollado por <b>{{ creator }}</b>
        </div>
    </div>
</body>
</html>
"""

# Rutas principales: Servir Panel Web Completo en / y /panel
@app.route('/')
@app.route('/panel')
def home():
    index_path = os.path.join(WEB_DIR, "index.html")
    if os.path.exists(index_path):
        return send_from_directory(WEB_DIR, "index.html")
    return show_card()

@app.route('/card')
@app.route('/monitor')
def show_card():
    uptime_sec = time.time() - _start_time
    voice_hours = _stats_ref.total_voice_hours if _stats_ref else 0.0
    is_in_voice = _stats_ref.is_in_voice if _stats_ref else False
    pct = _stats_ref.get_progress_percentage() if _stats_ref else 0.0
    uptime_str = _stats_ref.format_duration(uptime_sec) if _stats_ref else "0s"
    
    ping_ms = 0
    try:
        if _bot_ref and _bot_ref.latency is not None:
            lat = float(_bot_ref.latency)
            if not math.isinf(lat) and not math.isnan(lat):
                ping_ms = max(0, round(lat * 1000))
    except Exception:
        ping_ms = 0

    return render_template_string(
        HTML_TEMPLATE,
        creator=config.CREATOR_NAME,
        invite_url=config.DISCORD_INVITE,
        is_in_voice=is_in_voice,
        uptime_str=uptime_str,
        voice_hours=voice_hours,
        pct=pct,
        ping_ms=ping_ms
    )

# Servir archivos estáticos del panel web (css, js, mp3, imágenes)
@app.route('/<path:filename>')
def serve_web_assets(filename):
    file_path = os.path.join(WEB_DIR, filename)
    if os.path.exists(file_path):
        return send_from_directory(WEB_DIR, filename)
    # También permitir servir audios de la raíz si se piden
    root_file = os.path.join(BASE_DIR, filename)
    if os.path.exists(root_file) and (filename.endswith('.mp3') or filename.endswith('.wav') or filename.endswith('.jpg')):
        return send_from_directory(BASE_DIR, filename)
    return "Not Found", 404

# ==========================================
# APIS REST PARA EL PANEL WEB
# ==========================================

@app.route('/api/stats')
def api_stats():
    uptime_sec = time.time() - _start_time
    voice_hours = _stats_ref.total_voice_hours if _stats_ref else 0.0
    is_in_voice = _stats_ref.is_in_voice if _stats_ref else False
    pct = _stats_ref.get_progress_percentage() if _stats_ref else 0.0
    uptime_str = _stats_ref.format_duration(uptime_sec) if _stats_ref else "0s"

    ping_ms = 18
    try:
        if _bot_ref and _bot_ref.latency is not None:
            lat = float(_bot_ref.latency)
            if not math.isinf(lat) and not math.isnan(lat):
                ping_ms = max(5, round(lat * 1000))
    except Exception:
        pass

    return jsonify({
        "status": "online",
        "bot_name": "Erick x & Bot Admin",
        "creator": config.CREATOR_NAME,
        "guild_id": config.GUILD_ID,
        "is_in_voice": is_in_voice,
        "voice_hours": round(voice_hours, 2),
        "uptime_str": uptime_str,
        "uptime_sec": round(uptime_sec),
        "progress_pct": round(pct, 4),
        "ping_ms": ping_ms,
        "invite_url": config.DISCORD_INVITE
    })

@app.route('/api/chat', methods=['GET'])
def api_get_chat():
    """Obtiene el registro en vivo de mensajes y fotos de todos los canales."""
    if os.path.exists(CHAT_LOGS_FILE):
        try:
            with open(CHAT_LOGS_FILE, 'r', encoding='utf-8') as f:
                logs = json.load(f)
                return jsonify(logs)
        except Exception as e:
            print(f"[API Chat Error] {e}", flush=True)

    # Mensajes iniciales si el archivo aún no existe
    initial_sample = [
        {
            "id": "init_1",
            "author": "Erick X",
            "author_id": "1559437873265119252",
            "bot": True,
            "avatar": "https://images.unsplash.com/photo-1517841905240-472988babdf9?q=80&w=200&auto=format&fit=crop",
            "channel_name": "general",
            "channel_id": "1350706770527653992",
            "content": "🎙️ Sistema de Voz 24/7 y Panel Web sincronizados al 100%. Meta a 1,000,000 de horas.",
            "attachments": [],
            "timestamp": "04:00:00",
            "date": "2026-10-14"
        },
        {
            "id": "init_2",
            "author": "SatanasMiPadre",
            "author_id": "1559830923174744125",
            "bot": True,
            "avatar": "https://images.unsplash.com/photo-1534528741775-53994a69daeb?q=80&w=200&auto=format&fit=crop",
            "channel_name": "general",
            "channel_id": "1350706770527653992",
            "content": "🛡️ Bot Administrador activo. Monitoreando canales, roles y bienvenidas.",
            "attachments": [],
            "timestamp": "04:02:15",
            "date": "2026-10-14"
        },
        {
            "id": "init_3",
            "author": "rafamodzyt",
            "author_id": "1350706770527653989",
            "bot": False,
            "avatar": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=200&auto=format&fit=crop",
            "channel_name": "general",
            "channel_id": "1350706770527653992",
            "content": "👑 ¡Bienvenidos al Panel Web Oficial! Cualquier mensaje o foto enviado en Discord aparecerá aquí en tiempo real.",
            "attachments": ["https://images.unsplash.com/photo-1542751371-adc38448a05e?q=80&w=800&auto=format&fit=crop"],
            "timestamp": "04:05:00",
            "date": "2026-10-14"
        }
    ]
    return jsonify(initial_sample)

@app.route('/api/chat/send', methods=['POST'])
def api_send_chat():
    """Permite enviar un mensaje o foto a Discord vía Webhook y registrarlo."""
    try:
        data = request.get_json(force=True) or {}
        text = data.get("text", "").strip()
        channel_name = data.get("channel_name", "general")
        image_url = data.get("image_url", "").strip()

        if not text and not image_url:
            return jsonify({"error": "Mensaje vacío"}), 400

        attachments = [image_url] if image_url else []

        new_msg = {
            "id": f"web_{int(time.time() * 1000)}",
            "author": f"{config.CREATOR_NAME} (Web)",
            "author_id": "web_owner",
            "bot": True,
            "avatar": "https://images.unsplash.com/photo-1618005182384-a83a8bd57fbe?q=80&w=200&auto=format&fit=crop",
            "channel_name": channel_name,
            "channel_id": "1350706770527653992",
            "content": text,
            "attachments": attachments,
            "timestamp": time.strftime("%H:%M:%S"),
            "date": time.strftime("%Y-%m-%d")
        }

        # Guardar en logs
        logs = []
        if os.path.exists(CHAT_LOGS_FILE):
            try:
                with open(CHAT_LOGS_FILE, 'r', encoding='utf-8') as f:
                    logs = json.load(f)
            except Exception:
                logs = []

        logs.append(new_msg)
        if len(logs) > 300:
            logs = logs[-300:]

        os.makedirs(os.path.dirname(CHAT_LOGS_FILE), exist_ok=True)
        with open(CHAT_LOGS_FILE, 'w', encoding='utf-8') as f:
            json.dump(logs, f, ensure_ascii=False, indent=2)

        # Enviar vía Webhook a Discord si está configurado
        if config.WEBHOOK_URL:
            try:
                payload = {
                    "username": f"{config.CREATOR_NAME} (Panel Web)",
                    "content": text
                }
                if image_url:
                    payload["embeds"] = [{"image": {"url": image_url}}]
                requests.post(config.WEBHOOK_URL, json=payload, timeout=4)
            except Exception as e_hook:
                print(f"[Webhook Send Error] {e_hook}", flush=True)

        return jsonify({"status": "ok", "message": new_msg})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/api/chat/clear', methods=['POST'])
def api_clear_chat():
    """Limpia el historial de chat."""
    try:
        if os.path.exists(CHAT_LOGS_FILE):
            with open(CHAT_LOGS_FILE, 'w', encoding='utf-8') as f:
                json.dump([], f)
        return jsonify({"status": "cleared"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@app.route('/health')
def health():
    return jsonify({
        "status": "ok",
        "bot": "Erick x",
        "online_24_7": True,
        "is_in_voice": _stats_ref.is_in_voice if _stats_ref else False,
        "voice_hours": round(_stats_ref.total_voice_hours, 2) if _stats_ref else 0.0,
        "creator": config.CREATOR_NAME,
        "discord": config.DISCORD_INVITE
    }), 200

def set_bot_reference(bot, stats=None):
    """Actualiza la referencia de bot y estadísticas si cambia la instancia."""
    global _bot_ref, _stats_ref
    _bot_ref = bot
    if stats:
        _stats_ref = stats

def run_web(port=config.PORT):
    app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)

_web_running = False

def start_keep_alive(stats_manager=None, bot=None, port=config.PORT):
    """Inicia el servidor web en un hilo separado para mantener vivo el bot en Railway."""
    global _stats_ref, _bot_ref, _web_running
    if stats_manager:
        _stats_ref = stats_manager
    if bot:
        _bot_ref = bot
    if _web_running:
        return None
    _web_running = True
    try:
        t = Thread(target=run_web, args=(port,), daemon=True)
        t.start()
        print(f"[KeepAlive] Servidor web y Panel SHADOW BLOCK activos en puerto {port}.", flush=True)
        return t
    except Exception as e:
        print(f"[KeepAlive] Aviso servidor web: {e}", flush=True)
        return None

if __name__ == "__main__":
    port = int(os.getenv("PORT", config.PORT or 8080))
    print(f"[KeepAlive] Iniciando servidor web directamente en puerto {port}...")
    app.run(host="0.0.0.0", port=port, debug=False)

