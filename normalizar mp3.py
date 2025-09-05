import os  # Importa el módulo 'os' para trabajar con archivos
from pydub import AudioSegment

# Ruta donde están tus archivos MP3
MUSIC_DIR = "./descargas_mp3"

# Función para normalizar MP3: convertir a bitrate constante (CBR) y exportar
def normalize_mp3_files():
    for file in os.listdir(MUSIC_DIR):  # Itera sobre los archivos en la carpeta
        if file.lower().endswith(".mp3"):  # Verifica si el archivo es un MP3
            input_file = os.path.join(MUSIC_DIR, file)  # Ruta completa del archivo
            output_file = os.path.join(MUSIC_DIR, f"normalized_{file}")  # Nuevo nombre para el archivo procesado
            
            try:
                # Cargar el archivo MP3
                audio = AudioSegment.from_mp3(input_file)
                
                # Exportar con bitrate constante (128k)
                audio.export(output_file, format="mp3", bitrate="128k")
                print(f"Archivo procesado: {output_file}")
            except Exception as e:
                print(f"Error al procesar {input_file}: {e}")

if __name__ == "__main__":
    normalize_mp3_files()