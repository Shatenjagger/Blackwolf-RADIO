import os
import requests

# Función para descargar un archivo MP3
def descargar_mp3(url, folder):
    try:
        response = requests.get(url, stream=True)
        if response.status_code == 200:
            # Extraer el nombre del archivo desde la URL
            nombre_archivo = url.split("/")[-1]
            ruta_completa = os.path.join(folder, nombre_archivo)
            
            # Guardar el archivo
            with open(ruta_completa, 'wb') as archivo:
                for chunk in response.iter_content(chunk_size=1024):
                    archivo.write(chunk)
            print(f"Descargado: {nombre_archivo}")
        else:
            print(f"Error al descargar ({response.status_code}): {url}")
    except Exception as e:
        print(f"Error inesperado con {url}: {e}")

# Carpeta donde se guardarán los archivos
output_folder = "descargas_mp3"
os.makedirs(output_folder, exist_ok=True)

# Leer las URLs desde el archivo urls.txt usando UTF-8
archivo_urls = "urls.txt"
if os.path.exists(archivo_urls):
    try:
        with open(archivo_urls, "r", encoding="utf-8") as f:
            urls = [line.strip() for line in f.readlines() if line.strip()]
    except UnicodeDecodeError as e:
        print(f"Error al leer el archivo: {e}")
        urls = []
else:
    print("El archivo urls.txt no existe.")
    urls = []

# Descargar todos los archivos
for url in urls:
    descargar_mp3(url, output_folder)

print("Todas las descargas han terminado.")