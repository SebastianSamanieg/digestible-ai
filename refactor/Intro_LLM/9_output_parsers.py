from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
import os

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage

from config.logger_config import log



class AnalisisTexto(BaseModel):
    resumen: str = Field(description="Resumen breve del texto.")
    sentimiento: str = Field(description="Sentimiento del texto. (Positivo, negativo o negativo)")

# ───────────────────────────────────────────────────────────────────────────────
# 🌱 Cargar variables de entorno
# ───────────────────────────────────────────────────────────────────────────────
load_dotenv()

# ───────────────────────────────────────────────────────────────────────────────
# VARIABLES DE ENTORNO
# ───────────────────────────────────────────────────────────────────────────────
deployment_name = os.getenv("DEPLOYMENT")  # Nombre del deployment en Azure
temperature_ia = 0.7  # Creatividad del modelo (0 = determinista, 1 = creativo)
endpoint = os.getenv("ENDPOINT")  # Endpoint del recurso Azure OpenAI
api_key = os.getenv("KEY")  # API Key
api_version = os.getenv("API_VERSION")  # Versión del API

# ═══════════════════════════════════════════════════════════════════════════════
# CREACIÓN DEL LLM
# ═══════════════════════════════════════════════════════════════════════════════
llm = AzureChatOpenAI(
    azure_deployment=deployment_name,
    temperature=temperature_ia,
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version=api_version
)

structured_llm = llm.with_structured_output(AnalisisTexto)

texto_prueba = "Me encanto la nueva pelicula de accion tiene muchos efectos especiales"

resultado = structured_llm.invoke(f"Analixa el siguiente texto: {texto_prueba}")
print(resultado.model_dump_json())

#Ejemplo basico
class User(BaseModel):
    id: int
    nombre: str
    activo: bool = True


data = {"id": "1", "nombre": "Ana"}

usuario = User(**data)

print(usuario.model_dump_json())


