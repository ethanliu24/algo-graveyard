from typing import Any
from ..schemas.question import Source, Difficulty, Status, Tag
from ..schemas.solution import Language

class MetadataManager:
    def get_metadata(
        self,
        sources: bool | None = False,
        difficulties: bool | None = False,
        statuses: bool | None = False,
        tags: bool | None = False,
        languages: bool | None = False,
    ) -> dict[str, list[Any]]:
        sources = sources if sources is not None else False
        difficulties = difficulties if difficulties is not None else False
        statuses = statuses if statuses is not None else False
        tags = tags if tags is not None else False
        languages = languages if languages is not None else False

        metadata = {}
        if sources: metadata.update({ "sources": self.get_sources() })
        if difficulties: metadata.update({ "difficulties": self.get_difficulties() })
        if statuses: metadata.update({ "statuses": self.get_statuses() })
        if tags: metadata.update({ "tags": self.get_tags() })
        if languages: metadata.update({ "languages": self.get_languages() })

        return metadata

    def get_sources(self) -> list[str]:
        return [source.value for source in Source]

    def get_difficulties(self) -> list[str]:
        return [difficulty.value for difficulty in Difficulty]

    def get_statuses(self) -> list[str]:
        return [status.value for status in Status]

    def get_tags(self) -> list[str]:
        return [tag.value for tag in Tag]

    def get_languages(self) -> list[str]:
        return [language.value for language in Language]
