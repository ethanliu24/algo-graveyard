from __future__ import annotations
from datetime import datetime
from enum import Enum
from pydantic import BaseModel
from .solution import Solution
from .test_case import TestCase

class Question(BaseModel):
    source: Source
    link: str
    status: Status
    title: str
    prompt: str
    test_cases: list[TestCase]
    notes: list[str]
    hints: list[str]
    tags: list[str]
    solutions: list[Solution]
    created_at: datetime
    last_modified: datetime


class QuestionCreate(BaseModel):
    source: Source
    link: str
    status: Status
    title: str
    prompt: str
    test_cases: list[TestCase]
    notes: list[str]
    hints: list[str]
    tags: list[str]


class Source(Enum):
    LEETCODE = "leetcode"
    OTHER = "other"


class Status(Enum):
    COMPLETED = "completed"
    UNOPTIMIZED = "unoptimized"
    ATTEMPTED = "attempted"
