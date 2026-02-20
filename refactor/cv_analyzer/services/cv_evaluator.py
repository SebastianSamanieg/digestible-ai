from langchain_openai import ChatOpenAI

from cv_analyzer.models.cv_model import AnalisisCV
from cv_analyzer.prompts.cv_prompts import crear_sistema_prompts
import os

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI

from config.logger_config import log

load_dotenv()

deployment_name = os.getenv("DEPLOYMENT")  # Nombre del deployment en Azure
temperature_ia = 0.7  # Creatividad del modelo (0 = determinista, 1 = creativo)
endpoint = os.getenv("ENDPOINT")  # Endpoint del recurso Azure OpenAI
api_key = os.getenv("KEY")  # API Key
api_version = os.getenv("API_VERSION")  # Versión del API

def crear_evaluador_cv():
    modelo_base = AzureChatOpenAI(
        azure_deployment=deployment_name,
        temperature=temperature_ia,
        azure_endpoint=endpoint,
        api_key=api_key,
        api_version=api_version
    )

    modelo_estructurado = modelo_base.with_structured_output(AnalisisCV)
    chat_prompt = crear_sistema_prompts()
    cadena_evaluacion = chat_prompt | modelo_estructurado

    return cadena_evaluacion

def evaluar_candidato(texto_cv: str, descripcion_puesto: str) -> AnalisisCV:
    try:
        cadena_evaluacion = crear_evaluador_cv()

        resultado = cadena_evaluacion.invoke({
            "texto_cv": texto_cv,
            "descripcion_puesto": descripcion_puesto
        })

        return resultado
    
    except Exception as e:
        return AnalisisCV(
            nombre_candidato="Error en procesamiento.",
            experiencia_años=0,
            habilidades_clave=["Error al procesar CV"],
            education="No se puede determinar.",
            experiencia_relevante="Error durante el análisis.",
            fotalezas=["Requiere revisión manual del CV"],
            areas_mejora=["Verificar formato y legibilidad del PDF"],
            porcetaje_ajuste=0
        )
