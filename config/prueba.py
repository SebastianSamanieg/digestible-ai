from config.llm_config import LLMBuilder

llm = LLMBuilder(temperature=0)

response = llm.invoke("Cuanto es 2+2")
print(response.content)
print(response.usage_metadata)