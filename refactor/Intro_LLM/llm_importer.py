import os

from dotenv import load_dotenv
from langchain_openai import AzureChatOpenAI

load_dotenv()

DEPLOYMENT_NAME = os.getenv("DEPLOYMENT")
TEMPERATURE = 0
ENDPOINT = os.getenv("ENDPOINT")
API_KEY = os.getenv("KEY")
API_VERSION = os.getenv("API_VERSION")

llm = AzureChatOpenAI(
    azure_deployment=DEPLOYMENT_NAME,
    temperature=TEMPERATURE,
    azure_endpoint=ENDPOINT,
    api_key=API_KEY,
    api_version=API_VERSION
)

print("✅ LLM inicializado correctamente")


respuesta = llm.invoke("Que dia es hoy")
print(respuesta.content)