import discord
from discord.ext import commands
import asyncio
import os
import random
from dotenv import load_dotenv
import logging
from threading import Thread
from flask import Flask

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

# Rutas a los archivos .m3u en la raíz del repositorio
M3U_FILES = [
    "video-game-music-remixes-archive-2018_vbr.m3u",
    "videogamemusic_201706_vbr.m3u"
]

# Lista global de URLs de canciones
global_music_queue = []

# Variable global para controlar la reproducción
is_playing = False

# Función para cargar múltiples archivos .m3u
def load_m3u_playlists():
    global global_music_queue
    global_music_queue = []  # Limpiar la cola global antes de cargar nuevas canciones
    for m3u_file in M3U_FILES:
        try:
            if not os.path.exists(m3u_file):
                print(f"❌ Archivo .m3u no encontrado: {m3u_file}")
                continue
            with open(m3u_file, "r", encoding="utf-8") as file:
                lines = file.readlines()
                music_urls = [line.strip() for line in lines if not line.startswith("#") and line.strip()]
                global_music_queue.extend(music_urls)
            print(f"✅ Se cargaron {len(music_urls)} canciones desde {m3u_file}.")
        except Exception as e:
            print(f"❌ Error al cargar el archivo .m3u {m3u_file}: {e}")
    print(f"✅ Total de canciones cargadas: {len(global_music_queue)}.")

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

# Comando para reproducir música automáticamente
@bot.command()
async def play(ctx):
    global is_playing
    voice = ctx.guild.voice_client

    if not voice:
        await ctx.send("❌ Primero usa `!join` para conectar al canal de voz.")
        return

    if not global_music_queue:
        await ctx.send("❌ No hay canciones disponibles en la cola global.")
        return

    if is_playing:
        await ctx.send("🎵 Ya estoy reproduciendo música. Usa `!skip` para cambiar de canción.")
        return

    is_playing = True
    await ctx.send("🎧 Iniciando reproducción automática de música...")

    while is_playing:
        try:
            current_song = random.choice(global_music_queue)
            source = discord.FFmpegPCMAudio(current_song)
            voice.play(source, after=lambda e: print(f"Fin de la canción: {current_song}"))
            song_name = current_song.split("/")[-1]  # Extraer el nombre del archivo de la URL
            await ctx.send(f"▶️ Reproduciendo: `{song_name}`")

            while voice.is_playing():
                await asyncio.sleep(1)

        except Exception as e:
            print(f"Error al reproducir {current_song}: {e}")
            await ctx.send(f"⚠️ Error al reproducir `{current_song}`: {e}")

    is_playing = False
    await ctx.send("🎵 La reproducción automática ha terminado.")

# Comando para saltar la canción actual
@bot.command()
async def skip(ctx):
    voice = ctx.guild.voice_client
    if voice and voice.is_playing():
        voice.stop()
        await ctx.send("⏭️ Canción saltada.")
    else:
        await ctx.send("❌ No hay ninguna canción reproduciéndose.")

# Comando para detener la reproducción
@bot.command()
async def stop(ctx):
    global is_playing
    voice = ctx.guild.voice_client
    if voice and voice.is_playing():
        voice.stop()
        is_playing = False
        await ctx.send("🛑 Reproducción detenida.")
    else:
        await ctx.send("❌ No hay ninguna canción reproduciéndose.")

# Servidor Flask para el health check
app = Flask(__name__)

@app.route('/health', methods=['GET'])
def health():
    return "OK", 200

# Evento de inicio del bot
@bot.event
async def on_ready():
    print(f"✅ Bot conectado como {bot.user}")
    load_m3u_playlists()  # Cargar las listas .m3u automáticamente al iniciar
    await bot.change_presence(activity=discord.Game(name="🎵 Reproductor de VGM"))

# Inicia el servidor Flask en un hilo separado
def run_flask():
    app.run(host='0.0.0.0', port=8080)

Thread(target=run_flask, daemon=True).start()

# Ejecutar el bot
bot.run(TOKEN)  # Token cargado desde .env





