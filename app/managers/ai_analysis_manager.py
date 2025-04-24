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

    def get_feedback(self, title: str, prompt: str, language: str, solution: str, additional_info: str = "") -> None:
        if ENV_VARS.get("APP_ENV") == "test" or not prompt or not solution:
            return AiAnalysis(**{
                "time_complexity": "",
                "space_complexity": "",
                "feedback": "No prompt or solution provided."
            })

        response = self.client.models.generate_content(
            model=self.model,
            contents=[
                self.context,
                f"Question title: {title}",
                f"Question prompt: {prompt}",
                f"Additional info: {additional_info}",
                f"Solution language: ${language}",
                f"Solution: {solution}"
            ]
        )

        # assumes the content is returned in the format "```json{ ... }```"
        analysis = json.loads(response.text.strip().removeprefix("```json").removesuffix("```").strip())
        return AiAnalysis(**analysis)

