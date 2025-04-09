from __future__ import annotations
from typing import Any
from .base_config import BaseModelConfig

class TestCase(BaseModelConfig):
    parameters: list[dict[str, Any]]
    output: Any
    explanation: str
