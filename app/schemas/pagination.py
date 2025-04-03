from typing import Any
from .base_config import BaseModelConfig

class Pagination(BaseModelConfig):
    data: list[Any]
    page: int
    per_page: int
    pages: int
    total: int
    