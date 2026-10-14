import json
import time
from datetime import datetime, timezone
from pathlib import Path
import config

class StatsManager:
    """Administra el conteo persistente de horas en el canal de voz hacia la meta de 1,000,000 de horas."""
    
    def __init__(self, filepath: Path = config.STATS_FILE):
        self.filepath = filepath
        self.target_hours = config.TARGET_HOURS
        self.data = self._load()
        self._session_start_time = None
        self._is_in_voice = False

    def _load(self) -> dict:
        if self.filepath.exists():
            try:
                with open(self.filepath, "r", encoding="utf-8") as f:
                    data = json.load(f)
                    # Asegurar campos requeridos
                    data.setdefault("total_voice_seconds", 0.0)
                    data.setdefault("total_uptime_seconds", 0.0)
                    data.setdefault("first_started", datetime.now(timezone.utc).isoformat())
                    data.setdefault("sessions_count", 0)
                    data.setdefault("target_hours", self.target_hours)
                    return data
            except Exception as e:
                print(f"[Stats] Error al leer {self.filepath}: {e}. Se reiniciará la estructura.")
        
        default_data = {
            "total_voice_seconds": 0.0,
            "total_uptime_seconds": 0.0,
            "first_started": datetime.now(timezone.utc).isoformat(),
            "last_saved": datetime.now(timezone.utc).isoformat(),
            "sessions_count": 0,
            "target_hours": self.target_hours
        }
        self._save_raw(default_data)
        return default_data

    def _save_raw(self, data: dict):
        try:
            self.filepath.parent.mkdir(parents=True, exist_ok=True)
            with open(self.filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4, ensure_ascii=False)
        except Exception as e:
            print(f"[Stats] Error al guardar estadísticas: {e}")

    def save(self):
        """Guarda el estado actual acumulado en el archivo JSON."""
        self.tick()
        self.data["last_saved"] = datetime.now(timezone.utc).isoformat()
        self._save_raw(self.data)

    def on_voice_connected(self):
        """Notifica que el bot se ha conectado al canal de voz."""
        self._is_in_voice = True
        self._session_start_time = time.time()
        self.data["sessions_count"] = self.data.get("sessions_count", 0) + 1
        self.save()

    def on_voice_disconnected(self):
        """Notifica que el bot se ha desconectado del canal de voz."""
        if self._is_in_voice and self._session_start_time:
            elapsed = time.time() - self._session_start_time
            self.data["total_voice_seconds"] = self.data.get("total_voice_seconds", 0.0) + elapsed
        self._is_in_voice = False
        self._session_start_time = None
        self.save()

    def tick(self, uptime_delta: float = 0.0):
        """Actualiza los segundos de la sesión activa en tiempo real."""
        now = time.time()
        if self._is_in_voice and self._session_start_time:
            elapsed = now - self._session_start_time
            self.data["total_voice_seconds"] = self.data.get("total_voice_seconds", 0.0) + elapsed
            self._session_start_time = now
        
        if uptime_delta > 0:
            self.data["total_uptime_seconds"] = self.data.get("total_uptime_seconds", 0.0) + uptime_delta

    @property
    def is_in_voice(self) -> bool:
        return self._is_in_voice

    @property
    def total_voice_seconds(self) -> float:
        total = self.data.get("total_voice_seconds", 0.0)
        if self._is_in_voice and self._session_start_time:
            total += (time.time() - self._session_start_time)
        return total

    @property
    def total_voice_hours(self) -> float:
        return self.total_voice_seconds / 3600.0

    @property
    def current_session_seconds(self) -> float:
        if self._is_in_voice and self._session_start_time:
            return time.time() - self._session_start_time
        return 0.0

    def get_progress_percentage(self) -> float:
        pct = (self.total_voice_hours / self.target_hours) * 100.0
        return min(100.0, max(0.0, pct))

    def get_progress_bar(self, length: int = 15) -> str:
        pct = self.get_progress_percentage()
        filled = int((pct / 100.0) * length)
        unfilled = length - filled
        return "█" * filled + "░" * unfilled

    @staticmethod
    def format_duration(seconds: float) -> str:
        seconds = int(seconds)
        days, rem = divmod(seconds, 86400)
        hours, rem = divmod(rem, 3600)
        minutes, secs = divmod(rem, 60)
        
        parts = []
        if days > 0:
            parts.append(f"{days}d")
        if hours > 0 or days > 0:
            parts.append(f"{hours}h")
        if minutes > 0 or hours > 0 or days > 0:
            parts.append(f"{minutes}m")
        parts.append(f"{secs}s")
        return " ".join(parts)
