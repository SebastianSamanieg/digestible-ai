# ═══════════════════════════════════════════════════════════════════════════════
# 🤖 MÓDULO 05 — RUNNABLELAMBDA + RUNNABLEPARALLEL (PIPELINES OPTIMIZADOS)
#
# En este módulo aprendemos:
#
# ✅ Crear pipelines reales con RunnableLambda
# ✅ Ejecutar tareas en paralelo con RunnableParallel
# ✅ Fan-out / Fan-in
# ✅ Procesar múltiples textos con batch()
#
# Este patrón es usado en:
# - Clasificación
# - Enriquecimiento de datos
# - Agentes
# - LangGraph
# ═══════════════════════════════════════════════════════════════════════════════

import json
import os

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate
from langchain_core.runnables import RunnableLambda, RunnableParallel
from langchain_openai import AzureChatOpenAI

load_dotenv()

# ═══════════════════════════════════════════════════════════════════════════════
# 🧠 CONFIGURACIÓN DEL MODELO
# ═══════════════════════════════════════════════════════════════════════════════
llm = AzureChatOpenAI(
    azure_deployment=os.getenv("DEPLOYMENT"),
    temperature=0,
    azure_endpoint=os.getenv("ENDPOINT"),
    api_key=os.getenv("KEY"),
    api_version=os.getenv("API_VERSION")
)


# ═══════════════════════════════════════════════════════════════════════════════
# 🧹 PASO 1 — PREPROCESAMIENTO
#
# Limpia texto y limita longitud.
# Esto ocurre ANTES del LLM.
# ═══════════════════════════════════════════════════════════════════════════════
def preprocess_text(text):
    texto_limpio = text.strip()
    return texto_limpio[:500]


preprocessor = RunnableLambda(preprocess_text)

# ═══════════════════════════════════════════════════════════════════════════════
# 🧩 PROMPT — RESUMEN
# ═══════════════════════════════════════════════════════════════════════════════
summary_template = PromptTemplate(
    template="""
Resume en una sola oración el texto.

Texto: {text}

Reglas:
- Una oración
- Máx 100 caracteres
""",
    input_variables=["text"]
)


def generate_summary(text):
    prompt = summary_template.format(text=text)
    response = llm.invoke(prompt)
    return response.content


# ═══════════════════════════════════════════════════════════════════════════════
# 🧩 PROMPT — SENTIMIENTO
# ═══════════════════════════════════════════════════════════════════════════════
sentiment_template = PromptTemplate(
    template="""
Analiza sentimiento del texto.

Devuelve SOLO JSON:
{{"sentimiento":"positivo|negativo|neutro","razon":"breve"}}

Texto: {text}
""",
    input_variables=["text"]
)


def analyze_sentiment(text):
    prompt = sentiment_template.format(text=text)
    response = llm.invoke(prompt)

    try:
        return json.loads(response.content)
    except:
        return {"sentimiento": "neutro", "razon": "error parseando"}


# ═══════════════════════════════════════════════════════════════════════════════
# ⚡ RUNNABLEPARALLEL
#
# Fan-out:
#     mismo input → múltiples tareas
#
# Fan-in:
#     resultados → un solo diccionario
# ═══════════════════════════════════════════════════════════════════════════════

summary_runnable = RunnableLambda(generate_summary)
sentiment_runnable = RunnableLambda(analyze_sentiment)

parallel_processor = RunnableParallel(
    resumen=summary_runnable,
    sentimiento=sentiment_runnable
)

# ═══════════════════════════════════════════════════════════════════════════════
# 🔗 PIPELINE COMPLETO
#
# Texto
#   ↓
# preprocessor
#   ↓
# parallel_processor
#
# Resultado:
# {
#   "resumen": "...",
#   "sentimiento": {...}
# }
# ═══════════════════════════════════════════════════════════════════════════════

chain = preprocessor | parallel_processor

# ═══════════════════════════════════════════════════════════════════════════════
# 📦 BATCH — procesar múltiples textos
#
# batch ejecuta el pipeline para cada elemento.
# Internamente aprovecha paralelismo.
# ═══════════════════════════════════════════════════════════════════════════════
reviews_batch = [
    "¡Me encanta este producto! Funciona perfectamente y llegó muy rápido.",
    "El servicio al cliente fue terrible, nadie me ayudó con mi problema.",
    "El clima está nublado hoy, probablemente llueva más tarde."
]

resultado_batch = chain.batch(reviews_batch)

print(resultado_batch)

# ═══════════════════════════════════════════════════════════════════════════════
# 🧠 RESUMEN DEL MÓDULO
#
# RunnableLambda  → convierte funciones en bloques
# RunnableParallel → ejecuta bloques simultáneamente
#
# Fan-out: una entrada → muchos procesos
# Fan-in: muchos resultados → un output
#
# batch(): ejecuta el pipeline para múltiples entradas
#
# Este patrón es la base de LangGraph.
# ═══════════════════════════════════════════════════════════════════════════════
