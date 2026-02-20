# ═══════════════════════════════════════════════════════════════════════════════
# 🤖 MÓDULO 04 — RUNNABLELAMBDA: CONVIRTIENDO FUNCIONES EN CADENAS
#
# En este módulo aprendemos:
#
# ✅ Qué es un Runnable
# ✅ Cómo envolver funciones Python con RunnableLambda
# ✅ Cómo encadenar pasos con "|"
# ✅ Cómo fluye la información paso a paso
#
# Idea central:
# En LangChain TODO es un Runnable.
# Un Runnable es cualquier cosa que recibe input y produce output.
#
# RunnableLambda permite transformar funciones normales en bloques compatibles
# con LangChain.
# ═══════════════════════════════════════════════════════════════════════════════

from langchain_core.runnables import RunnableLambda

# ═══════════════════════════════════════════════════════════════════════════════
# 🧩 PASO 1 — TRANSFORMAR NÚMERO A TEXTO
#
# Creamos un Runnable a partir de una función lambda.
#
# Input : 43
# Output: "Numero 43"
# ═══════════════════════════════════════════════════════════════════════════════
paso1 = RunnableLambda(lambda x: f"Numero {x}")


# ═══════════════════════════════════════════════════════════════════════════════
# 🧩 PASO 2 — DUPLICAR EL TEXTO
#
# Función Python normal.
# Recibe texto y devuelve una lista con el texto duplicado.
#
# Input : "Numero 43"
# Output: ["Numero 43", "Numero 43"]
# ═══════════════════════════════════════════════════════════════════════════════
def duplicar_texto(texto):
    return [texto] * 2


# Convertimos la función en Runnable
paso2 = RunnableLambda(duplicar_texto)

# ═══════════════════════════════════════════════════════════════════════════════
# 🔗 ENCADENAR PASOS
#
# El operador "|" significa:
# "la salida del paso anterior entra al siguiente"
#
# Visualmente:
#
# 43 → paso1 → "Numero 43" → paso2 → ["Numero 43", "Numero 43"]
# ═══════════════════════════════════════════════════════════════════════════════
cadena = paso1 | paso2

# ═══════════════════════════════════════════════════════════════════════════════
# ▶️ EJECUCIÓN
#
# invoke inicia el flujo completo.
# ═══════════════════════════════════════════════════════════════════════════════
resultado = cadena.invoke(43)

print(resultado)

# ═══════════════════════════════════════════════════════════════════════════════
# 🧠 ¿CÓMO FUNCIONA EL FLUJO?
#
# invoke(43)
#     ↓
# paso1: 43 → "Numero 43"
#     ↓
# paso2: "Numero 43" → ["Numero 43", "Numero 43"]
#     ↓
# Resultado final
#
# Cada Runnable recibe el output anterior automáticamente.
# ═══════════════════════════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════════════════════════
# ⭐ ¿POR QUÉ USAR RUNNABLELAMBDA?
#
# ✓ Convierte funciones normales en componentes LangChain
# ✓ Permite crear pipelines complejos
# ✓ Facilita testing por partes
# ✓ Es la base de Agents y LangGraph
#
# Piensa en esto como una línea de producción:
#
# Entrada → estación 1 → estación 2 → estación 3 → salida
#
# Cada estación es un Runnable.
# ═══════════════════════════════════════════════════════════════════════════════


# ═══════════════════════════════════════════════════════════════════════════════
# 🧭 IDEA CLAVE DEL MÓDULO
#
# LangChain no conecta modelos.
# Conecta Runnables.
#
# LLMs, Prompts, funciones, tools, parsers…
# todo termina siendo un Runnable.
#
# LangGraph simplemente organiza estos Runnables en grafos.
# ═══════════════════════════════════════════════════════════════════════════════
