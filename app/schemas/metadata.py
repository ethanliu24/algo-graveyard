from .base_config import BaseModelConfig
from .question import Source, Difficulty, Status, Tag

class Metadata(BaseModelConfig):
    sources: list[Source]
    difficulties: list[Difficulty]
    statuses: list[Status]
    tags: list[Tag]
