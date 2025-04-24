from google import genai
from typing import Any

class AiAnalysisManager:
    client: Any

    def __init__(self, api_key: str, model: str):
        self.client = genai.Client(api_key=api_key)
        response = self.client.models.generate_content(
            model=model, contents="Explain how AI works in a few words"
        )
        print(response.text)
