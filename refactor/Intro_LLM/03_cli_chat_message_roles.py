# ═══════════════════════════════════════════════════════════════════════════════
# 🤖 MÓDULO 03 — CHAT POR TERMINAL + ROLES DE MENSAJES
#
# En este módulo aprendemos:
#
# 1. SystemMessage define personalidad
# 2. HumanMessage representa input
# 3. AIMessage representa output
# 4. El historial es una lista de mensajes
# 5. Conversación desde terminal
# ═══════════════════════════════════════════════════════════════════════════════

import os

from dotenv import load_dotenv
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_openai import AzureChatOpenAI

load_dotenv()

# ═══════════════════════════════════════════════════════════════════════════════
# 🧠 CONFIGURACIÓN DEL MODELO
# ═══════════════════════════════════════════════════════════════════════════════
llm = AzureChatOpenAI(
    azure_deployment=os.getenv("DEPLOYMENT"),
    temperature=0.6,
    azure_endpoint=os.getenv("ENDPOINT"),
    api_key=os.getenv("KEY"),
    api_version=os.getenv("API_VERSION")
)

# ═══════════════════════════════════════════════════════════════════════════════
# 🎭 SELECCIÓN DE PERSONALIDAD (SystemMessage)
# ═══════════════════════════════════════════════════════════════════════════════
print("\nSelecciona personalidad del asistente:\n")
print("1 - Mentor Técnico")
print("2 - Recruiter")
print("3 - Profesor")

opcion = input("\nOpción: ")

system_prompts = {
    "1": "Eres un mentor senior de software. Responde con ejemplos técnicos.",
    "2": "Eres un recruiter IT. Evalúa respuestas como perfil profesional.",
    "3": "Eres un profesor universitario. Explica de forma pedagógica."
}

system_message = SystemMessage(content=system_prompts.get(opcion, system_prompts["1"]))

print("\nEscribe /exit para salir")
print("Escribe /reset para reiniciar conversación\n")

# ═══════════════════════════════════════════════════════════════════════════════
# 🧠 HISTORIAL
#
# Aquí guardamos HumanMessage y AIMessage
# SystemMessage se mantiene fijo
# ═══════════════════════════════════════════════════════════════════════════════
historial = []

# ═══════════════════════════════════════════════════════════════════════════════
# 🔁 LOOP PRINCIPAL
# ═══════════════════════════════════════════════════════════════════════════════
while True:

    pregunta = input("\nTú: ")

    if pregunta.lower() == "/exit":
        print("\n👋 Hasta luego")
        break

    if pregunta.lower() == "/reset":
        historial = []
        print("\n🔄 Conversación reiniciada")
        continue

    # 1️⃣ HumanMessage
    human_msg = HumanMessage(content=pregunta)

    # Construimos conversación completa
    mensajes = [system_message]
    mensajes.extend(historial)
    mensajes.append(human_msg)

    # 2️⃣ Enviamos al modelo
    respuesta = llm.invoke(mensajes)

    # 3️⃣ AIMessage
    ai_msg = AIMessage(content=respuesta.content)

    print(f"\nAsistente: {ai_msg.content}")

    # Guardamos historial
    historial.append(human_msg)
    historial.append(ai_msg)
