import os
import time
from datetime import datetime
from openai import OpenAI
import requests
import json

def guardar_prompt(prompt):
    archivo_prompts = 'prompts.json'
    prompts = []

    # Leer el archivo JSON existente si existe
    if os.path.exists(archivo_prompts):
        with open(archivo_prompts, 'r') as f:
            prompts = json.load(f)
    
    # Verificar si el prompt ya existe
    if prompt in prompts:
        return False
    
    # Añadir el nuevo prompt
    prompts.append(prompt)
    
    # Guardar la lista actualizada en el archivo JSON
    with open(archivo_prompts, 'w') as f:
        json.dump(prompts, f, indent=2)
    
    return True

def crear_carpeta_mes():
    # Obtener el año y mes actual
    fecha_actual = datetime.now()
    carpeta_mes = fecha_actual.strftime("%Y-%m")
    
    # Crear la carpeta principal 'generations' si no existe
    if not os.path.exists('generations'):
        os.makedirs('generations')
        print("Carpeta 'generations' creada.")
    else:
        print("Carpeta 'generations' ya existe.")
    
    # Crear la carpeta del mes actual si no existe
    ruta_carpeta_mes = os.path.join('generations', carpeta_mes)
    if not os.path.exists(ruta_carpeta_mes):
        os.makedirs(ruta_carpeta_mes)
        print(f"Carpeta del mes '{carpeta_mes}' creada.")
    else:
        print(f"Carpeta del mes '{carpeta_mes}' ya existe.")
    
    return ruta_carpeta_mes

def generar_imagen_con_reintento(prompt, ruta_carpeta, max_intentos=2):
    """
    Intenta generar una imagen con DALL-E, reintentando si hay violación de políticas de contenido.
    Si después de los reintentos sigue fallando, permite al usuario modificar el prompt.
    """
    intento = 1
    while intento <= max_intentos:
        try:
            print(f"\nGenerando imagen para prompt: {prompt[:50]}... (Intento {intento}/{max_intentos})")
            
            # Guardar el prompt si es nuevo (solo en el primer intento)
            if intento == 1 and guardar_prompt(prompt):
                print("Nuevo prompt guardado en prompts.json")
            elif intento == 1:
                print("Prompt ya existente, no se guardó")
            
            # Generar la imagen
            response = client.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024", #1792x1024 , 1024x1792 
                quality="standard", # hd 
                n=1,
            )
            
            # Si llegamos aquí, la generación fue exitosa
            # Obtener la URL de la imagen generada
            image_url = response.data[0].url
            print("URL de la imagen generada obtenida.")
            
            print("Descargando imagen...")
            # Descargar la imagen
            image_content = requests.get(image_url).content
            
            # Generar el nombre del archivo con fecha y hora
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = os.path.join(ruta_carpeta, f"image_{timestamp}.png")
            
            print(f"Guardando imagen como {filename}...")
            # Guardar la imagen
            with open(filename, 'wb') as f:
                f.write(image_content)
            
            print(f"La imagen se ha guardado con éxito en: {filename}")
            return filename
            
        except Exception as e:
            error_str = str(e)
            
            # Verificar si es un error de violación de políticas de contenido
            if "content_policy_violation" in error_str:
                if intento < max_intentos:
                    print("\n¡ALERTA LOKA! Tu prompt viola las políticas de contenido de OpenAI.")
                    print("Intentando de nuevo una vez más...\n")
                    intento += 1
                else:
                    print("\n¡ERROR PSYCHO! Tu prompt sigue violando las políticas de contenido.")
                    print("Necesitas modificar el prompt para continuar.")
                    
                    nuevo_prompt = input("\nIngresa un nuevo prompt modificado: ")
                    prompt = nuevo_prompt
                    intento = 1  # Reiniciar el contador con el nuevo prompt
            else:
                # Si es otro tipo de error, lo lanzamos para que lo maneje el bloque principal
                raise e

def generar_imagen(prompt, ruta_carpeta):
    """Función wrapper que llama a generar_imagen_con_reintento"""
    return generar_imagen_con_reintento(prompt, ruta_carpeta)

def obtener_prompts():
    prompts = []
    
    while True:
        try:
            num_prompts = int(input("\n¿Cuántos prompts quieres generar, psycho? "))
            if num_prompts <= 0:
                print("¡Eh, loko! Necesito un número positivo. Inténtalo de nuevo.")
                continue
            break
        except ValueError:
            print("¡Eso no es un número válido, compa! Inténtalo de nuevo.")
    
    print(f"\n¡Vamos a generar {num_prompts} imágenes lokísimas!")
    
    for i in range(num_prompts):
        prompt = input(f"\nIngresa el prompt #{i+1}: ")
        prompts.append(prompt)
    
    return prompts

def menu_post_generacion(prompts_actuales):
    while True:
        print("\n¿Qué quieres hacer ahora, mi psycho compa?")
        print("1. Generar nuevamente con los mismos prompts")
        print("2. Cambiar los prompts")
        print("3. Cerrar el programa")
        
        opcion = input("\nElige una opción (1-3): ")
        
        if opcion == '1':
            return 'regenerar', prompts_actuales
        elif opcion == '2':
            return 'cambiar', []
        elif opcion == '3':
            return 'salir', []
        else:
            print("¡Opción no válida, loko! Inténtalo de nuevo.")

def main():
    print("¡Bienvenido al generador de imágenes DALL-E psycho-loko! 🚀🔥")
    
    prompts_actuales = []
    accion = 'cambiar'
    
    while accion != 'salir':
        # Si necesitamos cambiar los prompts, pedimos nuevos
        if accion == 'cambiar':
            prompts_actuales = obtener_prompts()
        
        # Crear carpeta del mes actual
        ruta_carpeta_mes = crear_carpeta_mes()
        
        # Generar imágenes para cada prompt
        tiempo_inicio = time.time()
        imagenes_generadas = []
        
        for prompt in prompts_actuales:
            imagen = generar_imagen(prompt, ruta_carpeta_mes)
            imagenes_generadas.append(imagen)
        
        tiempo_fin = time.time()
        tiempo_total = tiempo_fin - tiempo_inicio
        
        print(f"\n¡Proceso completado en {tiempo_total:.2f} segundos!")
        print(f"Se generaron {len(imagenes_generadas)} imágenes:")
        for img in imagenes_generadas:
            print(f"- {img}")
        
        # Preguntar qué hacer después
        accion, prompts_actuales = menu_post_generacion(prompts_actuales)

if __name__ == "__main__":
    # Obtener la API key desde las variables de entorno
    api_key = os.getenv('OPENAI_API_KEY')
    if not api_key:
        print("¡ERROR! No se encontró la API key de OpenAI en las variables de entorno.")
        print("Asegúrate de configurar la variable de entorno OPENAI_API_KEY.")
        exit(1)
    
    print("API key obtenida de las variables de entorno.")
    
    # Crear el cliente de OpenAI con la API key
    client = OpenAI(api_key=api_key)
    
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n¡Programa interrumpido por el usuario! Hasta la próxima, psycho compa. 🔥")
    except Exception as e:
        print(f"\n¡ERROR LOKO! Algo salió mal: {str(e)}")
    finally:
        print("\n¡Gracias por usar el generador de imágenes DALL-E psycho-loko! 🚀")

