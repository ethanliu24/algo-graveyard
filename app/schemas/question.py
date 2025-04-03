from __future__ import annotations
from datetime import datetime
from enum import Enum
from pydantic import field_validator
from .base_config import BaseModelConfig
from .pagination import Pagination
from .solution import Solution
from .test_case import TestCase

class Question(BaseModelConfig):
    id: str
    source: Source
    link: str
    difficulty: Difficulty
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
    difficulty: Difficulty
    status: Status
    title: str
    prompt: str
    test_cases: list[TestCase]
    notes: list[str]
    hints: list[str]
    tags: list[str]

    @field_validator("title")
    def title_exists_and_is_long_enough(title: str) -> int:
        if not (0 <= len(title) <= 50):
            raise ValueError("There must be a title and it should be less or equal than 50 characters.")
        return title

    @field_validator("prompt")
    def prompt_exists(prompt: str) -> int:
        if len(prompt) == 0:
            raise ValueError("There must be a prompt for a question.")
        return prompt


class QuestionBasicInfo(BaseModelConfig):
    id: str
    source: Source
    difficulty: Difficulty
    status: Status
    title: str
    tags: list[str]
    created_at: datetime
    last_modified: datetime


class QuestionAll(BaseModelConfig):
    paginated: bool
    data: Pagination | list[QuestionBasicInfo]

class Source(Enum):
    LEETCODE = "leetcode"
    OTHER = "other"


class Status(Enum):
    COMPLETED = "completed"
    UNOPTIMIZED = "unoptimized"
    ATTEMPTED = "attempted"


class Difficulty(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"
