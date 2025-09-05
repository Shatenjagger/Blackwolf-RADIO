import discord
from discord.ext import commands
import asyncio
import os
import random  # Para reproducción aleatoria
from dotenv import load_dotenv
import logging
from threading import Thread
from http.server import BaseHTTPRequestHandler, HTTPServer

# Activar el modo DEBUG para obtener logs detallados
logging.basicConfig(level=logging.DEBUG)

# Cargar variables de entorno desde .env
load_dotenv()

# Configuración del bot
TOKEN = os.getenv("DISCORD_TOKEN")  # Token del bot desde .env
CHANNEL_ID = int(os.getenv("CHANNEL_ID"))  # ID del canal de voz desde .env

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents)

# Ruta donde están tus archivos MP3 normalizados
MUSIC_DIR = "./descargas_mp3"  # Carpeta donde están los archivos MP3 normalizados

# Cola de reproducción
music_queue = []
current_song = None

# Variable global para controlar la reproducción
is_playing = False

# Función para listar todos los archivos MP3 en la carpeta
def get_mp3_files():
    mp3_files = []
    for file in os.listdir(MUSIC_DIR):
        if file.lower().endswith(".mp3"):
            mp3_files.append(os.path.join(MUSIC_DIR, file))
    return mp3_files

# Comando para unirse al canal de voz
@bot.command()
async def join(ctx):
    if ctx.author.voice:
        channel = ctx.author.voice.channel
        if ctx.voice_client and ctx.voice_client.is_connected():
            await ctx.send(f"🟠 Ya estoy conectado al canal `{channel.name}`.")
        else:
            await channel.connect()
            await ctx.send(f"🟢 Conectado al canal de voz `{channel.name}`.")
    else:
        await ctx.send("❌ Debes estar en un canal de voz.")

# Comando para salir
@bot.command()
async def leave(ctx):
    if ctx.voice_client:
        await ctx.guild.voice_client.disconnect()
        await ctx.send("🔴 Desconectado del canal de voz.")
    else:
        await ctx.send("❌ No estoy en ningún canal de voz.")

# Comando para reproducir música en modo random
@bot.command()
async def play(ctx):
    global is_playing, current_song
    voice = ctx.guild.voice_client

    if not voice:
        await ctx.send("❌ Primero usa `!join` para conectar al canal de voz.")
        return

    mp3_files = get_mp3_files()
    if not mp3_files:
        await ctx.send("❌ No se encontraron archivos MP3 normalizados en la carpeta `descargas_mp3`.")
        return

    if not music_queue:
        random.shuffle(mp3_files)  # Mezclamos las canciones para reproducirlas en orden aleatorio
        music_queue.extend(mp3_files)

    if is_playing:
        await ctx.send("🎵 Ya estoy reproduciendo música. Usa `!skip` para cambiar de canción.")
        return

    is_playing = True
    await ctx.send("🎧 Iniciando reproducción de música en modo random...")

    while music_queue and is_playing:
        current_song = music_queue.pop(0)
        try:
            # Validar que el archivo MP3 existe y es accesible
            if not os.path.isfile(current_song):
                await ctx.send(f"⚠️ Archivo no encontrado: `{os.path.basename(current_song)}`")
                continue

            # Opciones mínimas de FFmpeg (sin opciones avanzadas)
            ffmpeg_options = {
                'options': '-vn'
            }
            source = discord.FFmpegPCMAudio(current_song, **ffmpeg_options)
            voice.play(source, after=lambda e: print(f"Fin de la canción: {current_song}"))
            song_name = os.path.basename(current_song)
            await ctx.send(f"▶️ Reproduciendo: `{song_name}`")

            # Esperar mientras la canción se reproduce
            while voice.is_playing():
                await asyncio.sleep(1)
        except Exception as e:
            print(f"Error al reproducir {current_song}: {e}")
            await ctx.send(f"⚠️ Error al reproducir `{os.path.basename(current_song)}`: {e}")

    is_playing = False
    await ctx.send("🎵 La cola de reproducción ha terminado.")

# Servidor HTTP básico para el health check
class HealthCheckHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"OK")

def run_health_check_server():
    server_address = ('0.0.0.0', 8080)  # Puerto 8080
    httpd = HTTPServer(server_address, HealthCheckHandler)
    httpd.serve_forever()

# Inicia el servidor HTTP en un hilo separado
Thread(target=run_health_check_server, daemon=True).start()

# Ejecutar el bot
bot.run(TOKEN)  # Token cargado desde .env
