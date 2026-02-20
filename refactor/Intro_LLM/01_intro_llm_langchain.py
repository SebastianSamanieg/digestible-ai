# ═══════════════════════════════════════════════════════════════════════════════
# 🤖 CURSO LLM + AGENTES CON LANGCHAIN & LANGGRAPH
#
# Objetivo de este modulo.
#
#    Aprender los conceptos base:
#       1. Cómo conectar un LLM (Azure OpenAI)
#       2. Qué es un PromptTemplate
#       3. Qué es una Chain
#       4. Cómo ejecutar un flujo simple
#
# NOTA:
# LangChain = framework para orquestar LLMs
# LangGraph = extensión para crear flujos tipo grafo (lo veremos después)
# ═══════════════════════════════════════════════════════════════════════════════

import os

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_openai import AzureChatOpenAI

from config.logger_config import log

# ───────────────────────────────────────────────────────────────────────────────
# Cargar variables de entorno
# ───────────────────────────────────────────────────────────────────────────────
load_dotenv()

# ───────────────────────────────────────────────────────────────────────────────
# VARIABLES DE ENTORNO
# ───────────────────────────────────────────────────────────────────────────────
deployment_name = os.getenv("DEPLOYMENT")
temperature_ia = 0.7
endpoint = os.getenv("ENDPOINT")
api_key = os.getenv("KEY")
api_version = os.getenv("API_VERSION")

# ═══════════════════════════════════════════════════════════════════════════════
# CREACIÓN DEL LLM (Large Language Model)
# ═══════════════════════════════════════════════════════════════════════════════
llm = AzureChatOpenAI(
    azure_deployment=deployment_name,
    temperature=temperature_ia,
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version=api_version
)

# ───────────────────────────────────────────────────────────────────────────────
# ✅ USO DIRECTO DEL LLM (FORMA SIMPLE)
#
# invoke() envía un texto al modelo y devuelve la respuesta completa.
#
# respuesta = llm.invoke("Hola")
# print(respuesta.content)
#
# Normalmente NO trabajaremos así,
# porque LangChain está pensado para usar PROMPTS + CHAINS.
# ───────────────────────────────────────────────────────────────────────────────


# ═══════════════════════════════════════════════════════════════════════════════
# 🧩 PROMPT TEMPLATE
#
# Un PromptTemplate es una plantilla reutilizable.
# Permite definir variables dinámicas dentro del prompt.
#
# {nombre} será reemplazado al ejecutar.
#
# Esto evita concatenar strings manualmente.
# ═══════════════════════════════════════════════════════════════════════════════
plantilla = PromptTemplate(
    input_variables=["nombre"],
    template="""
Saluda al usuario con su nombre.

Nombre del usuario: {nombre}

Asistente:
"""
)

# ═══════════════════════════════════════════════════════════════════════════════
# 🔗 CHAINS (CADENAS)
#
# Una Chain conecta componentes:
#
# PromptTemplate  →  LLM
#
# El operador | significa:
# "la salida del prompt entra como input del modelo"
#
# Esto es programación funcional aplicada a IA.
# ═══════════════════════════════════════════════════════════════════════════════
chain_actual = plantilla | llm

# ═══════════════════════════════════════════════════════════════════════════════
# ▶️ EJECUCIÓN DE LA CHAIN
#
# invoke recibe un diccionario con los valores de las variables del prompt.
#
# {nombre} será reemplazado por "Carlos".
# ═══════════════════════════════════════════════════════════════════════════════
resultado = chain_actual.invoke({"nombre": "Carlos"})

# ───────────────────────────────────────────────────────────────────────────────
# 📤 RESPUESTA
#
# LangChain devuelve un objeto AIMessage.
# .content contiene solo el texto generado.
# ───────────────────────────────────────────────────────────────────────────────
log.info(resultado.content)
