# ═══════════════════════════════════════════════════════════════════════════════
# 🤖 MÓDULO 06 — ROLES EN CHATPROMPTTEMPLATE
#
# En este módulo aprenderás:
#
# 1. Diferencia PromptTemplate vs ChatPromptTemplate
# 2. Qué es system, human y assistant
# 3. Cómo se construyen mensajes estructurados
# 4. Ejemplos prácticos con outputs reales
# 5. Uso de assistant para few-shot learning
#
# ═══════════════════════════════════════════════════════════════════════════════

from langchain_core.prompts import PromptTemplate, ChatPromptTemplate


# ═══════════════════════════════════════════════════════════════════════════════
# 1️⃣ PromptTemplate (FORMA ANTIGUA)
# Todo es texto plano
# ═══════════════════════════════════════════════════════════════════════════════

template = "Eres un experto en marketing. Sugiere un eslogan creativo para un producto {producto}"

prompt = PromptTemplate(
    template=template,
    input_variables=["producto"]
)

prompt_lleno = prompt.format(producto="Cafe del cantante FEID")

print("\nPROMPT TEMPLATE:")
print(prompt_lleno)

"""
OUTPUT ESPERADO:

Eres un experto en marketing. Sugiere un eslogan creativo para un producto Cafe del cantante FEID
"""

# 👉 Aquí NO existen roles.
# 👉 El modelo recibe un solo bloque de texto.


# ═══════════════════════════════════════════════════════════════════════════════
# 2️⃣ ChatPromptTemplate (FORMA MODERNA)
# Mensajes estructurados por roles
# ═══════════════════════════════════════════════════════════════════════════════

chat_prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un traductor del español al inglés muy preciso"),
    ("human", "{texto}")
])

mensajes = chat_prompt.format_messages(texto="Hola, como estas?")

print("\nCHAT PROMPT TEMPLATE:")

for m in mensajes:
    print(f"{type(m).__name__}: {m.content}")

"""
OUTPUT ESPERADO:

SystemMessage: Eres un traductor del español al inglés muy preciso
HumanMessage: Hola, como estas?
"""

# 👉 Ahora el modelo recibe una LISTA de mensajes
# 👉 Cada mensaje tiene un rol claro


# ═══════════════════════════════════════════════════════════════════════════════
# 3️⃣ ¿QUÉ SIGNIFICA CADA ROL?
# ═══════════════════════════════════════════════════════════════════════════════

"""
SYSTEM
------
Define personalidad, reglas y comportamiento del modelo.
Se envía UNA sola vez normalmente.

Ejemplo:
"Eres profesor"
"Eres recruiter"
"Eres experto técnico"
"""

"""
HUMAN
-----
Es el input del usuario.
Puede incluir contexto o historial.

Ejemplo:
"Explícame Docker"
"Traduce esto"
"""

"""
ASSISTANT
---------
Representa respuestas del modelo.

Se usa principalmente para:

1. Few-shot learning
2. Ejemplos previos
3. Continuar conversaciones
"""


# ═══════════════════════════════════════════════════════════════════════════════
# 4️⃣ EJEMPLO PRÁCTICO CON ASSISTANT (FEW-SHOT)
# ═══════════════════════════════════════════════════════════════════════════════

chat_prompt_fewshot = ChatPromptTemplate.from_messages([

    ("system", "Eres un asistente que responde muy corto"),

    ("human", "Que es Python?"),
    ("assistant", "Un lenguaje de programación."),

    ("human", "Que es Docker?"),
    ("assistant", "Una plataforma de contenedores."),

    ("human", "{pregunta}")
])

mensajes_fs = chat_prompt_fewshot.format_messages(pregunta="Que es Kubernetes?")

print("\nFEW SHOT EJEMPLO:\n")

for m in mensajes_fs:
    print(f"{type(m).__name__}: {m.content}")

"""
OUTPUT ESPERADO:

SystemMessage: Eres un asistente que responde muy corto
HumanMessage: Que es Python?
AIMessage: Un lenguaje de programación.
HumanMessage: Que es Docker?
AIMessage: Una plataforma de contenedores.
HumanMessage: Que es Kubernetes?
"""

# 👉 El modelo aprende el patrón:
# preguntas cortas → respuestas cortas


# ═══════════════════════════════════════════════════════════════════════════════
# 5️⃣ RESUMEN VISUAL
# ═══════════════════════════════════════════════════════════════════════════════

"""
ChatPromptTemplate.from_messages([

    ("system", "..."),     → personalidad
    ("human", "..."),      → usuario
    ("assistant", "..."),  → ejemplo del modelo
])

FLUJO REAL:

SystemMessage     → configura
HumanMessage      → pregunta
AIMessage         → respuesta
HumanMessage      → nueva pregunta
AIMessage         → nueva respuesta
"""


# ═══════════════════════════════════════════════════════════════════════════════
# 🧠 CONCLUSIÓN
# ═══════════════════════════════════════════════════════════════════════════════

"""
PromptTemplate:
❌ Texto plano

ChatPromptTemplate:
✅ Roles
✅ Conversacional
✅ Few-shot
✅ Producción real
"""
