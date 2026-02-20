# document_loaders

from pydantic import BaseModel, Field
from langchain_openai import ChatOpenAI
import os

from dotenv import load_dotenv
from langchain_core.prompts import PromptTemplate, ChatPromptTemplate, MessagesPlaceholder
from langchain_openai import AzureChatOpenAI

from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter

#import kagglehub
# Download latest version
#path = kagglehub.dataset_download("sadiajavedd/social-media-user-activity-dataset")
#print("Path to dataset files:", path)

loader = PyPDFLoader("C:\\Users\\JSSAMANIEGPO\\PycharmProjects\\llm-learning-resources\\Intro_LLM\\pdfcoffee.com_storytelling-with-data-espaol-7-pdf-free.pdf")
pages = loader.load()

text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=3000,
    chunk_overlap=200
)

chunks = text_splitter.split_documents(pages)

load_dotenv()

deployment_name = os.getenv("DEPLOYMENT")  # Nombre del deployment en Azure
temperature_ia = 0.7  # Creatividad del modelo (0 = determinista, 1 = creativo)
endpoint = os.getenv("ENDPOINT")  # Endpoint del recurso Azure OpenAI
api_key = os.getenv("KEY")  # API Key
api_version = os.getenv("API_VERSION")  # Versión del API

llm = AzureChatOpenAI(
    azure_deployment=deployment_name,
    temperature=temperature_ia,
    azure_endpoint=endpoint,
    api_key=api_key,
    api_version=api_version
)

sumaries = []

i = 0
for chunk in chunks:
    if i>2:
        break
    response = llm.invoke(f"Haz un resumen de los puntos mas importantes del siguiente texto: {chunk.page_content}")
    sumaries.append(response.content)
    i += 1

print(sumaries)
final_summary = llm.invoke(f"Combina y sintetiza estos resumenes en un resumen coherente y completo: {" ".join(sumaries)}")
print(final_summary.content)