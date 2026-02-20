from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma
from langchain_community.document_loaders import PyPDFDirectoryLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
import numpy as np
import os
from Intro_LLM.llm_importer import llm

loader = PyPDFDirectoryLoader("C:\\Users\\JSSAMANIEGPO\\PycharmProjects\\llm-learning-resources\\insumos")
documentos = loader.load()
print(f"Se cargan {len(documentos)} documentos desde el directorio")

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

docs_split = text_splitter.split_documents(documentos)

print(f"Se crearon {len(docs_split)} chunks de texto")

MODEL_PATH = r"C:\Users\JSSAMANIEGPO\PycharmProjects\llm-learning-resources\models"

if not os.path.exists(os.path.join(MODEL_PATH, "config.json")):
    print(f"❌ Error: No se encuentra config.json en {MODEL_PATH}")
    exit(1)

if not os.path.exists(os.path.join(MODEL_PATH, "pytorch_model.bin")):
    print(f"❌ Error: No se encuentra pytorch_model.bin en {MODEL_PATH}")
    exit(1)

# Crear el objeto de embeddings
embeddings = HuggingFaceEmbeddings(
    model_name=MODEL_PATH,
    model_kwargs={
        'device': 'cpu',
        'local_files_only': True
    },
    encode_kwargs={
        'normalize_embeddings': True
    }
)

# Usar from_documents() en lugar del constructor directo
vectorstore = Chroma.from_documents(
    documents=docs_split,
    embedding=embeddings,
    persist_directory="C:\\Users\\JSSAMANIEGPO\\PycharmProjects\\llm-learning-resources\\chroma_db"
)

retriever = vectorstore.as_retriever(search_type='similarity', search_kwargs={"k":2})

consulta = "Que experiencia tiene sebastian?"

resultados = retriever.invoke(consulta)

print("Top 3 documentos mas similares a la consulta:")
for i, doc in enumerate(resultados, start=1):
    print(f"\n--- Documento {i} ---")
    print(f"Contenido: {doc.page_content}")
    print(f"Metadatos: {doc.metadata}")