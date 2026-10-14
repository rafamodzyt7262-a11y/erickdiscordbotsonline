FROM python:3.12-slim

WORKDIR /app

# Instalar dependencias de audio del sistema (ffmpeg y libopus para voz de Discord)
RUN apt-get update && apt-get install -y --no-install-recommends \
    ffmpeg \
    libopus0 \
    libopus-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requerimientos e instalarlos
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código del proyecto
COPY . .

# Puerto por defecto para web healthcheck
EXPOSE 8080

# Iniciar ambos bots 24/7
CMD ["python", "run_all.py"]

