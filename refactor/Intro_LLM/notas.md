# Cosas para aplicar
Prompt templates, dinamicas
cheins, cadenas, que se ejecuten paso a paso o en paralelo (runnables)
pydantic
roles, user, system, assistant
Retriever


# Paquetes principales
pip install langchain
pip install langchain-community
pip install langchain-openai
pip install langchain-core
pip install pydantic
pip install python-dotenv
pip install streamlit


Librerías Core de LangChain Utilizadas
1. langchain-core
Componentes fundamentales del framework LangChain.
Submódulos utilizados:

langchain_core.prompts - Gestión de prompts y plantillas
langchain_core.messages - Manejo de mensajes del chat
langchain_core.runnables - Componentes ejecutables y encadenables


Descripción Detallada por Librería
pydantic
bashpip install pydantic
Propósito: Validación de datos y definición de modelos con tipado estático.

BaseModel - Clase base para crear modelos de datos validados
Field - Decorador para agregar validaciones y metadatos a campos


langchain-openai
bashpip install langchain-openai
Propósito: Integración de LangChain con modelos de OpenAI/Azure OpenAI.

ChatOpenAI - Cliente para modelos de OpenAI estándar
AzureChatOpenAI - Cliente específico para Azure OpenAI Service


python-dotenv
bashpip install python-dotenv
Propósito: Cargar variables de entorno desde archivos .env.

load_dotenv() - Función para cargar configuraciones del archivo .env


langchain-core (Componentes Específicos)
langchain_core.prompts
Propósito: Crear y gestionar plantillas de prompts.

PromptTemplate - Plantillas simples con variables
ChatPromptTemplate - Plantillas para conversaciones
MessagesPlaceholder - Placeholder para mensajes dinámicos
SystemMessagePromptTemplate - Plantilla para mensajes del sistema
HumanMessagePromptTemplate - Plantilla para mensajes del usuario

langchain_core.messages
Propósito: Representar diferentes tipos de mensajes en conversaciones.

HumanMessage - Mensajes del usuario
AIMessage - Respuestas del modelo AI
SystemMessage - Instrucciones del sistema

langchain_core.runnables
Propósito: Componentes para crear cadenas ejecutables y pipelines.

RunnableLambda - Ejecutar funciones personalizadas en cadenas
RunnableParallel - Ejecutar múltiples operaciones en paralelo



from langchain_community.document_loaders



    rag_chain = (
            {
                "context": final_retriever | format_docs,
                "question": RunnablePassthrough()
            }
            | prompt
            | llm_generation
            | StrOutputParser()
    )