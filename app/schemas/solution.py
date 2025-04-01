from __future__ import annotations
from datetime import datetime
from enum import Enum
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


class Language(Enum):
    PYTHON = "python"
    JAVA = "java"
    JAVASCRIPT = "javascript"
