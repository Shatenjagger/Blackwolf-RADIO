# Usar una imagen base ligera de Python
FROM python:3.10-slim

# Instalar FFmpeg y limpiar cachés
RUN apt-get update && \
    apt-get install -y ffmpeg && \
    apt-get clean && \
    rm -rf /var/lib/apt/lists/*

# Exponer el puerto 8080 para Flask
EXPOSE 8080

# Copiar archivos del proyecto
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código fuente del bot
COPY . .

# Ejecutar el bot
CMD ["python", "retroradio.py"]
