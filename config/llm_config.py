import os

from dotenv import load_dotenv

load_dotenv()


class LLMBuilder:
    def __init__(self, temperature: float):
        if temperature is None:
            raise ValueError("Debes especificar la temperatura al instanciar LLMBuilder")

        self.provider = os.getenv("LLM_PROVIDER", "OPENAI").upper()
        self.temperature = float(temperature)
        self.llm = self._initialize_llm()

    def _initialize_llm(self):
        if self.provider == "OPENAI":
            from langchain_openai import AzureChatOpenAI

            deployment_name = os.getenv("OPENAI_DEPLOYMENT")
            endpoint = os.getenv("OPENAI_ENDPOINT")
            api_key = os.getenv("OPENAI_API_KEY")
            api_version = os.getenv("OPENAI_API_VERSION")

            return AzureChatOpenAI(
                azure_deployment=deployment_name,
                temperature=self.temperature,
                azure_endpoint=endpoint,
                api_key=api_key,
                api_version=api_version
            )

        elif self.provider == "GOOGLE":
            from langchain_google_genai import ChatGoogleGenerativeAI

            model = os.getenv("GOOGLE_MODEL")
            api_key = os.getenv("GOOGLE_API_KEY")

            return ChatGoogleGenerativeAI(
                model=model,
                api_key=api_key,
                temperature=self.temperature,
            )

        else:
            raise ValueError("LLM_PROVIDER debe ser OPENAI o GOOGLE")

    def invoke(self, prompt, **kwargs):
        response = self.llm.invoke(prompt, **kwargs)

        if isinstance(response.content, str):
            clean_text = response.content
        elif isinstance(response.content, list):
            clean_text = "".join(
                block.get("text", "")
                for block in response.content
            )
        else:
            clean_text = str(response.content)

        response.content = clean_text
        return response
