import os
from typing import Optional

from dotenv import load_dotenv
from openai import OpenAI


class OpenAIClientProvider:
    def __init__(self, api_key: Optional[str] = None) -> None:
        load_dotenv()
        key = api_key or os.getenv("OPENAI_API_KEY")
        if not key:
            raise RuntimeError("Missing required environment variable: OPENAI_API_KEY")
        self._client: OpenAI = OpenAI(api_key=key)

    def getOpenAiClient(self) -> OpenAI:
        return self._client


if __name__ == "__main__":
    provider = OpenAIClientProvider()
    client = provider.getOpenAiClient()
    print(type(client).__name__)
