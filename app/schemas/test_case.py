from __future__ import annotations
from pydantic import BaseModel, model_validator
from typing import Any

class TestCase(BaseModel):
    parameters: list[str]
    values: list[Any]
    result: Any
    explaination: str

    @model_validator(mode="after")
    def check_passwords_match(self) -> TestCase:
        if len(self.parameters) != len(self.values):
            raise ValueError("Paramter and values should have the same length.")
        return self
