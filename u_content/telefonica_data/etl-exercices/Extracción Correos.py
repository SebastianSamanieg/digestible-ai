import win32com.client
from datetime import datetime
import json
import os
import logging

# Configuración de logs
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("outlook_extraction.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger()

# Ruta para almacenar los archivos json
ruta = r"C:\Users\JSSAMANIEGPO\PycharmProjects\etl-exercices\data"
archivo_json = os.path.join(ruta, "correos_outlook.json")

# Crear directorio si no existe
if not os.path.exists(ruta):
    os.makedirs(ruta)
    logger.info(f"Directorio creado: {ruta}")

try:
    # Conexión con Outlook
    logger.info("Iniciando conexión con Outlook")
    outlook = win32com.client.Dispatch("Outlook.Application").GetNamespace("MAPI")

    # Acceso a la bandeja de entrada
    bandeja_correo = "joan.samaniego@telefonica.com"
    logger.info(f"Accediendo a la bandeja de {bandeja_correo}")

    # Verificar si la bandeja existe
    try:
        bandeja = outlook.Folders[bandeja_correo].Folders["Bandeja de entrada"]
        logger.info("Bandeja de entrada encontrada")
    except Exception as e:
        logger.error(f"Error al acceder a la bandeja: {e}")
        # Verificar si el usuario existe en Outlook
        folders = [folder.Name for folder in outlook.Folders]
        logger.info(f"Carpetas disponibles: {folders}")
        raise

    # Obtener y ordenar mensajes
    messages = bandeja.Items
    messages.Sort("[ReceivedTime]", True)
    logger.info("Mensajes obtenidos y ordenados")

    # Lista para almacenar datos de correos
    correos_data = []
    fecha_actual = datetime.now().isoformat()

    count = 0
    logger.info("Iniciando extracción de correos")

    # Verificar si hay mensajes disponibles
    if messages.Count == 0:
        logger.warning("No se encontraron mensajes en la bandeja")
    else:
        logger.info(f"Total de mensajes encontrados: {messages.Count}")

    # Extraer información de cada mensaje
    for message in messages:
        try:
            correo_id = message.EntryID
            asunto = message.Subject if message.Subject else "(Sin Asunto)"
            remitente = message.SenderEmailAddress if message.SenderEmailAddress else "(Desconocido)"
            conversation_id = message.ConversationID if hasattr(message, "ConversationID") else "(Sin ConversationID)"
            fecha_recepcion = message.ReceivedTime.isoformat() if hasattr(message, "ReceivedTime") else None
            cuerpo = message.Body if hasattr(message, "Body") else "(Sin contenido)"

            # Guardar datos del correo en la lista
            correos_data.append({
                "ID": correo_id,
                "ConversationID": conversation_id,
                "Asunto": asunto,
                "Remitente": remitente,
                "FechaRecepcion": fecha_recepcion,
                "Cuerpo": cuerpo,
                "FechaExtraccion": fecha_actual
            })

            count += 1
            logger.info(f"Procesado correo {count}: {asunto}")

            # Limitar a 10 correos
            if count == 10:
                logger.info("Alcanzado límite de 10 correos")
                break
        except Exception as e:
            logger.error(f"Error procesando correo: {e}")

    # Verificar si se obtuvieron datos
    if len(correos_data) == 0:
        logger.warning("No se pudo extraer información de ningún correo")
    else:
        logger.info(f"Se extrajeron datos de {len(correos_data)} correos")

    # Guardar datos en archivo JSON
    try:
        with open(archivo_json, "w", encoding="utf-8") as f:
            json.dump(correos_data, f, ensure_ascii=False, indent=4)

        # Verificar si el archivo se creó correctamente
        if os.path.exists(archivo_json) and os.path.getsize(archivo_json) > 0:
            logger.info(f"Archivo JSON guardado exitosamente en: {archivo_json}")
            logger.info(f"Tamaño del archivo: {os.path.getsize(archivo_json)} bytes")
        else:
            logger.error(f"El archivo JSON se creó pero está vacío o no existe")
    except PermissionError:
        logger.error(f"Error de permisos al guardar el archivo JSON. Verifica los permisos de escritura en {ruta}")
    except Exception as e:
        logger.error(f"Error al guardar el archivo JSON: {e}")

except Exception as e:
    logger.error(f"Error general en la ejecución: {e}")

print("Proceso finalizado. Revisa el archivo de log para más detalles.")