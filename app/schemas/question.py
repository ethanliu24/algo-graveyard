from __future__ import annotations
from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from .solution import Solution
from .test_case import TestCase

class Question(BaseModel):
    id: str | None
    source: Source
    link: str | None
    status: Status
    title: str
    prompt: str
    test_cases: list[TestCase] | None
    notes: list[str] | None
    hints: list[str] | None
    tags: list[str] | None
    solutions: list[Solution] | None
    created_at: datetime
    last_modified: datetime


class Source(Enum):
    LEETCODE = "leetcode"
    OTHER = "other"


class Status(Enum):
    COMPLETED = "completed"
    UNOPTIMIZED = "unoptimized"
    ATTEMPTED = "attempted"
