# RetroRadio Bot

Un bot de Discord para reproducir música retro en canales de voz.

## 🎵 Características
- Reproducción aleatoria de pistas MP3.
- Comandos básicos:
  - `!join`: Conecta el bot al canal de voz.
  - `!play`: Inicia la reproducción en modo random.
  - `!pause`: Pausa la música.
  - `!resume`: Reanuda la música.
  - `!skip`: Salta a la siguiente pista.
  - `!stop`: Detiene la reproducción.
  - `!queue`: Muestra la cola de reproducción.

## 🛠️ Requisitos
- Python 3.8+
- FFmpeg instalado y accesible en el PATH.
- Token de Discord y ID del canal de voz.

## 📦 Instalación
1. Clona este repositorio:
   ```bash
 git clone https://github.com/Shatenjagger/BlackWolf-RADIO.git
 cd BlackWolf-RADIO
 2. Instala las dependencias:
   pip install -r requirements.txt
3. Crean un archivo .env con las siguientes variables:   
   DISCORD_TOKEN=TU_TOKEN_DE_DISCORD
   CHANNEL_ID=ID_DEL_CANAL_DE_VOZ
  
   🚀 Ejecución
   python retroradio.py

   📄 Licencia
Este proyecto está bajo la licencia MIT.

