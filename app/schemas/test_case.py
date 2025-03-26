from __future__ import annotations, field_validator
from pydantic import BaseModel
from typing import Any

class TestCase(BaseModel):
    parameters: list[str]
    values: list[Any]
    result: Any
    explaination: str

    @field_validator("parameters")
    def check_param_value_is_parallel(parameters: list[str], fields: dict):
        values = fields.data.get("values")
        return len(values) == parameters
