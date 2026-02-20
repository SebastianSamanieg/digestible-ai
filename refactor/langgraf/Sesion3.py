import os
from typing import TypedDict, List

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI
from langgraph.graph import StateGraph, START, END

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

# ───────────────────────────────────────────────────────────────────────────────
# CREACIÓN DEL LLM (Large Language Model)
# ───────────────────────────────────────────────────────────────────────────────
llm = AzureChatOpenAI(
    azure_deployment=deployment_name,
    temperature=temperature_ia,
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version=api_version
)


# Definición del Estado
class State(TypedDict):
    numero: int
    resultado: str

graph = StateGraph(State)

def caso_par(state):
    return  {'resultado': 'El numero es par'}

def caso_impar(state):
    return  {'resultado': 'El numero es impar'}

graph.add_node("Par", caso_par)
graph.add_node("Impar", caso_impar)

def decidir_rama(state):
    if state['numero'] % 2 == 0:
        return "Par"
    else:
        return "Impar"

# Añadr el edge condicional
graph.add_conditional_edges(START, decidir_rama)

# Conectar ambors casos al final
graph.add_edge("Par", END)
graph.add_edge("Impar", END)

compiled = graph.compile()

# Probar el grafo con ejemplos
print(compiled.invoke({"numero":3})["resultado"])

# ═══════════════════════════════════════════════════════════════════════════════
# 🔡 Titulo
# ═══════════════════════════════════════════════════════════════════════════════

# ───────────────────────────────────────────────────────────────────────────────
# 📝️ Subtitulo
# ───────────────────────────────────────────────────────────────────────────────