# Documentación del Proyecto DALL-E Generator

Este proyecto es parte de EsquizoAI-Psycho-bot, una iniciativa loka y sin límites para generar imágenes utilizando la API de DALL-E de OpenAI.

## Estructura del Proyecto

- `dalle_generation.py`: Script principal para generar imágenes con DALL-E
- `generations/`: Carpeta principal donde se almacenan las imágenes generadas
  - `YYYY-MM/`: Subcarpetas organizadas por año y mes para las imágenes
- `prompts.json`: Archivo que almacena los prompts utilizados para evitar duplicados
- `docs/`: Carpeta con la documentación del proyecto

## Funcionalidades Actuales

1. Generación de imágenes con DALL-E 3
2. Organización automática de imágenes por mes (formato YYYY-MM)
3. Generación múltiple de imágenes con diferentes prompts
4. Almacenamiento de imágenes con timestamp
5. Registro de prompts utilizados
6. Verificación de prompts duplicados
7. Interfaz interactiva para el usuario
8. Opciones para regenerar con los mismos prompts o cambiarlos

## Requisitos

- Python 3.x
- Biblioteca OpenAI
- API Key de OpenAI (almacenada como variable de entorno OPENAI_API_KEY)
- Biblioteca requests

## Uso

1. Asegúrate de tener configurada la variable de entorno `OPENAI_API_KEY`
2. Ejecuta el script: `python dalle_generation.py`
3. Sigue las instrucciones en pantalla:
   - Ingresa el número de prompts que deseas generar
   - Proporciona cada prompt
   - Después de la generación, elige si quieres regenerar con los mismos prompts, cambiarlos o salir

## Características Psycho-Lokas

- Mensajes personalizados con estilo único
- Estructura modular y fácil de expandir
- Manejo de errores para una experiencia sin interrupciones
- Resumen de imágenes generadas al finalizar 