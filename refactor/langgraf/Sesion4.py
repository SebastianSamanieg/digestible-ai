import sys
from pathlib import Path

project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.messages import HumanMessage, AIMessage

from config.logger_config import log
from config.llm_config import LLMBuilder

# Obtener el LLM interno del builder
llm_builder = LLMBuilder(temperature=0)
llm = llm_builder.llm  # ✅ Acceder al LLM interno que SÍ es Runnable

prompt = ChatPromptTemplate.from_messages([
    ("system", "Eres un asistente útil"),
    MessagesPlaceholder(variable_name="history"),
    ("human", "{input}")
])

chain = prompt | llm  # ✅ Ahora funciona porque llm es AzureChatOpenAI
history = []

log.info("Chat en terminal (escribe 'Salir' para terminar)")

while True:
    try:
        user_input = input("> Tu: ").strip()
    except (EOFError, KeyboardInterrupt):
        log.info("Terminating...")
        break

    if not user_input:
        continue
    if user_input.lower() in {"salir", "exit", "quit"}:
        log.info("Terminating...")
        break

    respuesta = chain.invoke({"history": history, "input": user_input})
    log.info(f"Asistente: {respuesta.content}")

    history.extend(
        [
            HumanMessage(content=user_input),
            AIMessage(content=respuesta.content),
        ]
    )
