import os
import time
from datetime import datetime
from openai import OpenAI
import requests

def guardar_prompt(prompt):
    archivo_prompts = 'prompts.txt'
    if os.path.exists(archivo_prompts):
        with open(archivo_prompts, 'r') as f:
            ultimo_prompt = f.read().strip().split('\n\n')[-1]
        if prompt == ultimo_prompt:
            return False
    
    with open(archivo_prompts, 'a') as f:
        if os.path.getsize(archivo_prompts) > 0:
            f.write('\n\n')
        f.write(prompt)
    return True

print("Iniciando el proceso de generación de imagen...")
tiempo_inicio = time.time()

# Obtener la API key desde las variables de entorno
api_key = os.getenv('OPENAI_API_KEY')
print("API key obtenida de las variables de entorno.")

# Crear el cliente de OpenAI con la API key
client = OpenAI(api_key=api_key)

# Crear la carpeta 'generations' si no existe
if not os.path.exists('generations'):
    os.makedirs('generations')
    print("Carpeta 'generations' creada.")
else:
    print("Carpeta 'generations' ya existe.")

prompt = """acid surreal  bizarre horror psycho punk portrait painting  of the junkie cannabis being mystic wizard of chaos,
 the being He wears worn, paint-stained punk crust clothing and his face is big and grotesque"""

# Imprimir información del prompt
if guardar_prompt(prompt):
    print("Nuevo prompt guardado en prompts.txt")
else:
    print("Prompt ya existente, no se guardó")

print("Generando imagen...")
# Generar la imagen
response = client.images.generate(
    model="dall-e-3",
    prompt=prompt,
    size="1024x1024", #1792x1024 , 1024x1792 
    quality="standard", # hd 
    n=1,
)

# Obtener la URL de la imagen generada
image_url = response.data[0].url
print("URL de la imagen generada obtenida.")

print("Descargando imagen...")
# Descargar la imagen
image_content = requests.get(image_url).content

# Generar el nombre del archivo con fecha y hora
timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
filename = f"generations/image_{timestamp}.png"

print(f"Guardando imagen como {filename}...")
# Guardar la imagen
with open(filename, 'wb') as f:
    f.write(image_content)

# Imprimir mensaje de éxito
print(f"La imagen se ha guardado con éxito en: {filename}")

tiempo_fin = time.time()
tiempo_total = tiempo_fin - tiempo_inicio
print(f"Proceso completado en {tiempo_total:.2f} segundos.")

