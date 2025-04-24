from __future__ import annotations
from datetime import datetime
from enum import Enum
from pydantic import field_validator, model_validator
from .ai_analysis import AiAnalysis
from .base_config import BaseModelConfig

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

    @model_validator(mode="after")
    def sanitize_inputs(data: SolutionCreate) -> SolutionCreate:
        data.summary = data.summary.strip()
        data.summary = data.summary[0].upper() + data.summary[1:]
        data.explanation = data.explanation.strip()
        return data

    @field_validator("summary")
    def summary_exists_and_is_long_enough(title: str) -> int:
        if not (0 < len(title) <= 50):
            raise ValueError("There must be a summary and it should be less or equal than 50 characters.")
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
