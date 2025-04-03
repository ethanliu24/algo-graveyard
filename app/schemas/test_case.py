from __future__ import annotations
from pydantic import model_validator
from typing import Any
from .base_config import BaseModelConfig

class TestCase(BaseModelConfig):
    parameters: dict[str, Any]
    explaination: str
