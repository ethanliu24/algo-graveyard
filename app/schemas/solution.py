from __future__ import annotations
from datetime import datetime
from enum import Enum
from pydantic import field_validator
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
    created_at: datetime
    last_modified: datetime


class SolutionCreate(BaseModelConfig):
    summary: str
    explanation: str
    language: Language
    time_complexity: str
    space_complexity: str
    code: str

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
