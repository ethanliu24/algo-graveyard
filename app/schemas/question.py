from __future__ import annotations
from datetime import datetime
from enum import Enum
from pydantic import field_validator, model_validator
from .base_config import BaseModelConfig
from .pagination import Pagination
from .solution import Solution
from ..utils import sanitize_str

class Question(BaseModelConfig):
    id: str
    source: Source
    link: str
    difficulty: Difficulty
    status: Status
    title: str
    prompt: str
    notes: list[str]
    hints: list[str]
    tags: list[Tag]
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
    notes: list[str]
    hints: list[str]
    tags: list[Tag]

    @model_validator(mode="after")
    def sanitize_input(data: QuestionCreate) -> QuestionCreate:
        data.title = sanitize_str(data.title)
        data.prompt = sanitize_str(data.prompt)
        data.notes = [sanitize_str(note) for note in data.notes if note.strip() != ""]
        data.hints = [sanitize_str(hint) for hint in data.hints if hint.strip() != ""]
        return data

    @model_validator(mode="after")
    def if_link_doesnt_exist(data: QuestionCreate) -> QuestionCreate:
        if data.link == "":
            if len(data.title) == 0:
                raise ValueError("There must be a title.")
            if len(data.prompt) == 0:
                raise ValueError("There must be a prompt.")
        return data

    @field_validator("title")
    def title_exists_and_is_long_enough(title: str) -> int:
        if len(title) > 50:
            raise ValueError("The title should be less or equal than 50 characters.")
        return title


class QuestionBasicInfo(BaseModelConfig):
    id: str
    source: Source
    difficulty: Difficulty
    status: Status
    title: str
    tags: list[Tag]
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
    ATTEMPTED = "attempted"
    UNOPTIMIZED = "unoptimized"


class Difficulty(Enum):
    EASY = "easy"
    MEDIUM = "medium"
    HARD = "hard"


from enum import Enum

class Tag(Enum):
    ARRAY = "array"
    STRING = "string"
    HASH_TABLE = "hash table"
    DYNAMIC_PROGRAMMING = "dynamic programming"
    MATH = "math"
    SORTING = "sorting"
    GREEDY = "greedy"
    DFS = "dfs"
    BINARY_SEARCH = "binary search"
    MATRIX = "matrix"
    BFS = "bfs"
    TREE = "tree"
    BIT_MANIPULATION = "bit manipulation"
    TWO_POINTERS = "two pointers"
    HEAP = "heap"
    BINARY_TREE = "binary tree"
    SIMULATION = "simulation"
    STACK = "stack"
    GRAPH = "graph"
    SLIDING_WINDOW = "sliding window"
    DESIGN = "design"
    BACKTRACKING = "backtracking"
    DISJOINT_SET = "disjoint set"
    LINKED_LIST = "linked list"
    TRIE = "trie"
    QUEUE = "queue"
    RECURSION = "recursion"
    DIVIDE_AND_CONQUER = "divide and conquer"
    BINARY_SEARCH_TREE = "binary search tree"
    RANDOMIZED = "randomized"
    ITERATOR = "iterator"
    CONCURRENCY = "concurrency"
    SHELL = "shell"
