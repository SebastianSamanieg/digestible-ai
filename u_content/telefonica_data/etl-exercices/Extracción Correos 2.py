import json
from tqdm import tqdm
import time
import os
import google.generativeai as genai
from typing import List, Tuple, Dict, Optional
import uuid
from dotenv import load_dotenv

# Configurar la API key de Gemini
api_key = "AIzaSyD78R2MF-eQhhqCDC-I6hzNoTq-_w8Cfoc"
genai.configure(api_key=api_key)

# Inicializar el modelo Gemini
model = genai.GenerativeModel("gemini-1.5-flash")

# Instrucciones del sistema para resumir correos
SYSTEM_PROMPT = """
Eres un asistente especializado en resumir correos electrónicos de manera concisa y profesional.
Tu tarea es analizar el contenido del correo y crear un resumen que capture:
1. El propósito principal del correo
2. Información clave como fechas, eventos o acciones requeridas
3. Detalles importantes para el destinatario

El resumen debe ser breve (máximo 3 líneas) pero informativo, enfocándose en lo más relevante.
"""


def summarize_email(email_content: str) -> str:
    """
    Usa Gemini para resumir el contenido de un correo electrónico.

    Args:
        email_content: El contenido del correo a resumir

    Returns:
        Un resumen conciso del correo
    """
    try:
        # Limitar el contenido si es muy largo para evitar errores de token
        if len(email_content) > 30000:
            email_content = email_content[:30000] + "..."

        response = model.generate_content(
            [
                {"role": "user", "parts": [SYSTEM_PROMPT]},
                {"role": "user", "parts": [f"Analiza y resume este correo electrónico:\n\n{email_content}"]},
            ],
            generation_config={"temperature": 0.2, "max_output_tokens": 150},
        )

        return response.text.strip()
    except Exception as e:
        print(f"Error al resumir el correo: {e}")
        return "No se pudo generar un resumen debido a un error."


def process_emails(input_file: str, output_file: str) -> None:
    """
    Lee correos de un archivo JSON, los resume usando Gemini y guarda los resultados.

    Args:
        input_file: Ruta al archivo JSON con los correos de Outlook
        output_file: Ruta donde guardar el nuevo JSON con los resúmenes
    """
    try:
        # Leer el archivo JSON de entrada
        with open(input_file, "r", encoding="utf-8") as f:
            emails = json.load(f)

        print(f"Se cargaron {len(emails)} correos para procesar.")

        # Procesar cada correo y añadir el resumen
        for i, email in enumerate(tqdm(emails, desc="Procesando correos")):
            # Extraer el contenido del correo
            email_body = email.get("Cuerpo", "")

            # Obtener resumen
            summary = summarize_email(email_body)

            # Añadir el resumen al correo
            email["Resumen IA"] = summary

            # Pequeña pausa para evitar límites de tasa en la API
            if i > 0 and i % 5 == 0:
                time.sleep(1)

        # Guardar el resultado en un nuevo archivo JSON
        with open(output_file, "w", encoding="utf-8") as f:
            json.dump(emails, f, ensure_ascii=False, indent=2)

        print(f"Procesamiento completado. Resultados guardados en {output_file}")

    except Exception as e:
        print(f"Error durante el procesamiento: {e}")


if __name__ == "__main__":
    # Definir rutas de archivos
    input_json_path = r"C:\Users\JSSAMANIEGPO\PycharmProjects\etl-exercices\data\correos_outlook.json"
    output_json_path = r"C:\Users\JSSAMANIEGPO\PycharmProjects\etl-exercices\data\resumen_ia.json"

    # Verificar que el archivo de entrada existe
    if not os.path.exists(input_json_path):
        print(f"Error: No se encontró el archivo {input_json_path}")
    else:
        # Procesar los correos
        process_emails(input_json_path, output_json_path)