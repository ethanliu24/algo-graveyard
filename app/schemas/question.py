from __future__ import annotations
from datetime import datetime
from enum import Enum
from .base_config import BaseModelConfig
from .solution import Solution
from .test_case import TestCase

class Question(BaseModelConfig):
    id: str
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


class QuestionCreate(BaseModelConfig):
    source: Source
    link: str
    status: Status
    title: str
    prompt: str
    test_cases: list[TestCase]
    notes: list[str]
    hints: list[str]
    tags: list[str]


class QuestionBasicInfo(BaseModelConfig):
    id: str
    source: Source
    status: Status
    title: str
    tags: list[str]
    created_at: datetime
    last_modified: datetime


class Source(Enum):
    LEETCODE = "leetcode"
    OTHER = "other"


class Status(Enum):
    COMPLETED = "completed"
    UNOPTIMIZED = "unoptimized"
    ATTEMPTED = "attempted"
