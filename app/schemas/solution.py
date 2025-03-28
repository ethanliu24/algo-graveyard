from __future__ import annotations
from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from .ai_analysis import AiAnalysis

class Solution(BaseModel):
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


class Language(Enum):
    PYTHON = "python"
    JAVA = "java"
    JAVASCRIPT = "javascript"
