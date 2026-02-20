import os

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import AzureChatOpenAI
from langchain_core.messages import HumanMessage, AIMessage

from config.logger_config import log

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
chat = AzureChatOpenAI(
    azure_deployment=deployment_name,
    temperature=temperature_ia,
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version=api_version
)

chat_prompt = ChatPromptTemplate.from_messages(
    [
        ("system", "Eres un traudctor del español al ingles muy preciso."),
        ("human", "{texto}")
    ]
)

mensajes = chat_prompt.invoke({"texto":"Hola mundo, como estas?"})

#respuesta = chat.invoke(mensajes)

#print(respuesta.content)

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente útil que mantiene el contexto de la conversación."),
    MessagesPlaceholder(variable_name="historial"),
    ("human", "Usuario: {pregunta_actual}")
])

historial_conversacion = [
    HumanMessage(content="Usuario: ¿Cuál es la capital de Francia?"),
    AIMessage(content="IA: La capital de Francia es París."),
    HumanMessage(content="Usuario: ¿Y cuántos habitantes tiene?"),
    AIMessage(content="IA: París tiene aproximadamente 2.2 millones de habitantes en la ciudad propiamente dicha.")
]

mensajes = chat_prompt.format_messages(
    historial=historial_conversacion,
    pregunta_actual="¿Puedes decirme algo interesante de su arquitectura?"
)

for m in mensajes:
    print(m.content)

from langchain_core.messages import HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder

# Template para clasificación de sentimientos con few-shot examples
chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un experto en análisis de sentimientos. Clasifica cada texto como: POSITIVO, NEGATIVO o NEUTRO."),
    MessagesPlaceholder(variable_name="ejemplos"),
    ("human", "Texto a analizar: {texto_usuario}")
])

# Few-shot examples para análisis de sentimientos
ejemplos_sentimientos = [
    HumanMessage(content="Texto a analizar: Me encanta este producto, es increíble"),
    AIMessage(content="POSITIVO"),
    HumanMessage(content="Texto a analizar: El servicio fue terrible, muy decepcionante"),
    AIMessage(content="NEGATIVO"),
    HumanMessage(content="Texto a analizar: El clima está nublado hoy"),
    AIMessage(content="NEUTRO")
]

# Generar el prompt con los ejemplos
mensajes = chat_prompt.format_messages(
    ejemplos=ejemplos_sentimientos,
    texto_usuario="¡Qué día tan maravilloso!"
)

# Ver el resultado
for i, m in enumerate(mensajes):
    print(f"Mensaje {i + 1} ({m.__class__.__name__}):")
    print(m.content)
    print("-" * 40)