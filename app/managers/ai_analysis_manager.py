from google import genai
import json
from typing import Any
from ..env_vars import ENV_VARS
from ..schemas.ai_analysis import AiAnalysis

class AiAnalysisManager:
    """
    Really should be GeminiManager.
    """
    client: Any
    model: str
    context: str

    def __init__(self, api_key: str, model: str, context: str):
        self.client = genai.Client(api_key=api_key)
        self.model = model
        self.context = context

    def get_feedback(self, title: str, prompt: str, language: str, solution: str) -> None:
        if ENV_VARS.get("APP_ENV") == "test":
            return AiAnalysis(**{"ai_analysis": {
                "time_complexity": "",
                "space_complexity": "",
                "feedback": ""
            }})
        response = self.client.models.generate_content(
            model=self.model,
            contents=[
                self.context,
                f"Question title: {title}",
                f"Question prompt: {prompt}",
                f"Solution language: ${language}",
                f"Solution: {solution}"
            ]
        )

        # assumes the content is returned in the format "```json{ ... }```"
        analysis = json.loads(response.text.strip().removeprefix("```json").removesuffix("```").strip())
        return AiAnalysis(**analysis)

