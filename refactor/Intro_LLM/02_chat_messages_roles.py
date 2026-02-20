# ═══════════════════════════════════════════════════════════════════════════════
# 🤖 MÓDULO 02 — CHAT + ROLES DE MENSAJES (System / Human / AI)
#
# Objetivo de este modulo.
#
# 1. Cómo representar conversaciones con objetos LangChain
# 2. Qué son SystemMessage, HumanMessage y AIMessage
# 3. Cómo mantener historial
# 4. Cómo prototipar rápidamente con Streamlit
#
# IMPORTANTE:
# Streamlit solo es la UI.
# El verdadero aprendizaje está en los tipos de mensajes.
# ═══════════════════════════════════════════════════════════════════════════════

import os

import streamlit as st
from dotenv import load_dotenv
from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate
from langchain_openai import AzureChatOpenAI

# ───────────────────────────────────────────────────────────────────────────────
# 🌱 Cargar variables de entorno
# ───────────────────────────────────────────────────────────────────────────────
load_dotenv()

# ═══════════════════════════════════════════════════════════════════════════════
# 🖥️ CONFIGURACIÓN BÁSICA STREAMLIT
#
# Streamlit permite crear interfaces web con pocas líneas.
# Aquí solo lo usamos como medio visual para chatear.
# ═══════════════════════════════════════════════════════════════════════════════


st.set_page_config(page_title="ChatPromptTemplate Demo", page_icon="🤖")
st.title("🤖 Chatbot con ChatPromptTemplate")
st.markdown("Demostración práctica de ChatPromptTemplate + LangChain")

# ═══════════════════════════════════════════════════════════════════════════════
# SIDEBAR CONFIG
# ═══════════════════════════════════════════════════════════════════════════════

with st.sidebar:
    st.header("Configuración")

    temperature = st.slider("Temperatura", 0.0, 1.0, 0.5, 0.1)

    personalidad = st.selectbox(
        "Personalidad",
        [
            "Útil y amigable",
            "Profesional",
            "Casual",
            "Experto técnico",
            "Creativo"
        ]
    )

# ═══════════════════════════════════════════════════════════════════════════════
# MODELO
# ═══════════════════════════════════════════════════════════════════════════════

llm = AzureChatOpenAI(
    azure_deployment=os.getenv("DEPLOYMENT"),
    temperature=temperature,
    azure_endpoint=os.getenv("ENDPOINT"),
    api_key=os.getenv("KEY"),
    api_version=os.getenv("API_VERSION")
)

# ═══════════════════════════════════════════════════════════════════════════════
# SYSTEM PROMPTS
# ═══════════════════════════════════════════════════════════════════════════════

system_messages = {
    "Útil y amigable": "Eres un asistente útil y amigable. Responde claro y corto.",
    "Profesional": "Eres un asistente profesional. Responde estructurado.",
    "Casual": "Eres un asistente casual. Habla relajado.",
    "Experto técnico": "Eres experto senior en software. Da respuestas técnicas.",
    "Creativo": "Eres creativo. Usa ejemplos y analogías."
}

# ═══════════════════════════════════════════════════════════════════════════════
# CHATPROMPTTEMPLATE
# ═══════════════════════════════════════════════════════════════════════════════

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", system_messages[personalidad]),
    ("human", "Historial:\n{historial}\n\nPregunta: {mensaje}")
])

cadena = chat_prompt | llm

# ═══════════════════════════════════════════════════════════════════════════════
# SESSION STATE
# ═══════════════════════════════════════════════════════════════════════════════

if "mensajes" not in st.session_state:
    st.session_state.mensajes = []

# ═══════════════════════════════════════════════════════════════════════════════
# MOSTRAR HISTORIAL
# ═══════════════════════════════════════════════════════════════════════════════

for msg in st.session_state.mensajes:
    role = "assistant" if isinstance(msg, AIMessage) else "user"
    with st.chat_message(role):
        st.markdown(msg.content)

if st.button("🗑️ Nueva conversación"):
    st.session_state.mensajes = []
    st.rerun()

# ═══════════════════════════════════════════════════════════════════════════════
# INPUT
# ═══════════════════════════════════════════════════════════════════════════════

pregunta = st.chat_input("Escribe tu mensaje...")

if pregunta:

    with st.chat_message("user"):
        st.markdown(pregunta)

    # Preparar historial
    historial = ""

    for msg in st.session_state.mensajes[-10:]:
        if isinstance(msg, HumanMessage):
            historial += f"Usuario: {msg.content}\n"
        elif isinstance(msg, AIMessage):
            historial += f"Asistente: {msg.content}\n"

    if not historial:
        historial = "(Sin historial)"

    # Streaming
    with st.chat_message("assistant"):
        placeholder = st.empty()
        respuesta_final = ""

        for chunk in cadena.stream({"mensaje": pregunta, "historial": historial}):
            respuesta_final += chunk.content
            placeholder.markdown(respuesta_final + "▌")

        placeholder.markdown(respuesta_final)

    # Guardar historial
    st.session_state.mensajes.append(HumanMessage(content=pregunta))
    st.session_state.mensajes.append(AIMessage(content=respuesta_final))

# ═══════════════════════════════════════════════════════════════════════════════
# 🚀 CÓMO EJECUTAR ESTA APLICACIÓN
#
# Desde la raíz del proyecto, ejecuta:
#
#     streamlit run 02_chat_messages_roles.py
#
# Streamlit abrirá automáticamente el navegador en:
#
#     http://localhost:8501
#
# Cada vez que guardes el archivo:
# 👉 Streamlit recarga automáticamente.
#
# Para detener la app:
# CTRL + C en la terminal.
# ═══════════════════════════════════════════════════════════════════════════════

# ═══════════════════════════════════════════════════════════════════════════════
# 🧠 RESUMEN DEL MÓDULO — ROLES DE MENSAJES EN LANGCHAIN
#
# LangChain NO maneja texto plano.
# Maneja objetos estructurados llamados "Messages".
#
# Esto permite:
#   ✅ Mantener historial
#   ✅ Diferenciar roles
#   ✅ Crear agentes
#   ✅ Construir grafos con LangGraph
#
# Existen tres tipos principales:
# ═══════════════════════════════════════════════════════════════════════════════


# ───────────────────────────────────────────────────────────────────────────────
# 🟢 HumanMessage
#
# Representa lo que dice el usuario.
#
# Ejemplo:
#
# HumanMessage(content="Hola, ¿puedes ayudarme?")
#
# Se usa para:
# - Inputs humanos
# - Preguntas
# - Respuestas del usuario
# ───────────────────────────────────────────────────────────────────────────────


# ───────────────────────────────────────────────────────────────────────────────
# 🔵 AIMessage
#
# Representa lo que responde el modelo.
#
# Ejemplo:
#
# AIMessage(content="Claro, dime en qué puedo ayudarte.")
#
# Se usa para:
# - Respuestas del LLM
# - Decisiones del agente
# - Resultados intermedios
# ───────────────────────────────────────────────────────────────────────────────


# ───────────────────────────────────────────────────────────────────────────────
# 🟡 SystemMessage
#
# Define comportamiento del asistente.
# NO es visible para el usuario.
#
# Ejemplo:
#
# SystemMessage(content="Eres un experto en ciberseguridad.")
#
# Se usa para:
# - Personalidad
# - Reglas
# - Contexto global
# - Instrucciones del sistema
# ───────────────────────────────────────────────────────────────────────────────


# ═══════════════════════════════════════════════════════════════════════════════
# 🧩 EJEMPLO COMPLETO
#
# mensajes = [
#     SystemMessage(content="Responde como arquitecto de software"),
#     HumanMessage(content="¿Qué es LangChain?"),
#     AIMessage(content="LangChain es un framework para orquestar LLMs...")
# ]
#
# Este arreglo representa una conversación completa.
#
# LangGraph usará exactamente esta estructura más adelante
# para crear flujos de agentes.
# ═══════════════════════════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════════════════════════
# ⭐ IDEA CLAVE DEL MÓDULO
#
# Prompt + LLM es solo el inicio.
#
# El verdadero poder está en:
#
# 👉 Mensajes estructurados
# 👉 Historial
# 👉 Roles
#
# Esto es la base de:
# - Memory
# - Tools
# - Agents
# - LangGraph
#
# Sin esto, no existen agentes reales.
# Lo veremos en futuro modulos.
# ═══════════════════════════════════════════════════════════════════════════════
