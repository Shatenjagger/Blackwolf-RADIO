FROM python:3.10-slim

# Instalar ffmpeg
RUN apt-get update && apt-get install -y ffmpeg

# Copiar archivos del proyecto
COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

# Ejecutar el bot
CMD ["python", "retroradio.py"]