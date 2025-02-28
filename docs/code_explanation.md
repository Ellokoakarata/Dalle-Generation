# Explicación del Código

El archivo `dalle_generation.py` contiene el código principal para generar imágenes utilizando la API de DALL-E 3 de OpenAI. A continuación, se explica cada sección del código:

## Importación de Bibliotecas

```python
import os
import time
from datetime import datetime
from openai import OpenAI
import requests
import json
```

- `os`: Para interactuar con el sistema operativo (variables de entorno, creación de directorios)
- `time`: Para medir el tiempo de ejecución
- `datetime`: Para generar timestamps para los nombres de archivo
- `openai`: Cliente oficial de OpenAI para acceder a la API
- `requests`: Para descargar las imágenes generadas
- `json`: Para manejar el archivo de prompts

## Función `guardar_prompt`

```python
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
```

Esta función:
1. Verifica si existe el archivo `prompts.json`
2. Carga los prompts existentes si el archivo existe
3. Comprueba si el prompt actual ya está en la lista
4. Si es nuevo, lo añade y actualiza el archivo
5. Retorna `True` si se guardó un nuevo prompt, `False` si ya existía

## Función `crear_carpeta_mes`

```python
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
```

Esta función:
1. Obtiene el año y mes actual usando `datetime`
2. Crea la carpeta principal `generations` si no existe
3. Crea una subcarpeta con formato `YYYY-MM` para el mes actual si no existe
4. Retorna la ruta completa a la carpeta del mes

## Función `generar_imagen`

```python
def generar_imagen(prompt, ruta_carpeta):
    print(f"\nGenerando imagen para prompt: {prompt[:50]}...")
    
    # Guardar el prompt si es nuevo
    if guardar_prompt(prompt):
        print("Nuevo prompt guardado en prompts.json")
    else:
        print("Prompt ya existente, no se guardó")
    
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
    filename = os.path.join(ruta_carpeta, f"image_{timestamp}.png")
    
    print(f"Guardando imagen como {filename}...")
    # Guardar la imagen
    with open(filename, 'wb') as f:
        f.write(image_content)
    
    print(f"La imagen se ha guardado con éxito en: {filename}")
    return filename
```

Esta función:
1. Muestra información sobre el prompt que se está procesando
2. Guarda el prompt en el archivo JSON si es nuevo
3. Genera la imagen utilizando DALL-E 3
4. Descarga la imagen generada
5. Crea un nombre de archivo único con timestamp
6. Guarda la imagen en la carpeta del mes correspondiente
7. Retorna la ruta del archivo guardado

## Función `obtener_prompts`

```python
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
```

Esta función:
1. Solicita al usuario el número de prompts que desea generar
2. Valida que el número sea positivo
3. Solicita cada prompt individualmente
4. Retorna una lista con todos los prompts ingresados

## Función `menu_post_generacion`

```python
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
```

Esta función:
1. Muestra un menú con opciones para el usuario
2. Procesa la opción seleccionada
3. Retorna una tupla con la acción a realizar y los prompts actuales (si se van a reutilizar)

## Función `main`

```python
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
```

Esta función:
1. Inicializa el programa con un mensaje de bienvenida
2. Establece un bucle principal que continúa hasta que el usuario elija salir
3. Solicita nuevos prompts o reutiliza los existentes según la elección del usuario
4. Crea la carpeta del mes actual
5. Genera imágenes para cada prompt
6. Muestra un resumen de las imágenes generadas y el tiempo empleado
7. Pregunta al usuario qué hacer a continuación

## Bloque Principal

```python
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
```

Este bloque:
1. Verifica que la API key de OpenAI esté configurada como variable de entorno
2. Inicializa el cliente de OpenAI
3. Ejecuta la función principal dentro de un bloque try-except para manejar errores
4. Proporciona mensajes de error amigables en caso de problemas
5. Muestra un mensaje de despedida al finalizar 