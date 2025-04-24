from __future__ import annotations
from datetime import datetime
from enum import Enum
from pydantic import field_validator, model_validator
from .ai_analysis import AiAnalysis
from .base_config import BaseModelConfig
from ..utils import sanitize_str

class Solution(BaseModelConfig):
    id: str
    summary: str
    explanation: str
    language: Language
    time_complexity: str
    space_complexity: str
    ai_analysis: AiAnalysis
    code: str
    accepted: bool
    created_at: datetime
    last_modified: datetime


class SolutionCreate(BaseModelConfig):
    summary: str
    explanation: str
    language: Language
    time_complexity: str
    space_complexity: str
    code: str
    accepted: bool
    question_title: str
    question_prompt: str

    @model_validator(mode="after")
    def sanitize_inputs(data: SolutionCreate) -> SolutionCreate:
        data.summary = sanitize_str(data.summary)
        data.explanation = sanitize_str(data.explanation)
        data.code = data.code.strip()
        data.time_complexity = data.time_complexity.strip()
        data.space_complexity = data.space_complexity.strip()
        return data

    @field_validator("summary")
    def summary_exists_and_is_long_enough(title: str) -> int:
        if not (0 < len(title) <= 70):
            raise ValueError("There must be a summary and it should be less or equal than 70 characters.")
        return title


class Language(Enum):
    PYTHON = "python"
    JAVA = "java"
    JAVASCRIPT = "javascript"
    TYPESCRIPT = "typescript"
    C = "c"
    CPP = "c++"
    C_SHARP = "c#"
    SWIFT = "swift"
    KOTLIN = "kotlin"
    RUBY = "ruby"
    RUST = "rust"
    GO = "go"
    HASKELL = "haskell"
    PHP = "php"
