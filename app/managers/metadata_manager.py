from ..schemas.metadata import Metadata
from ..schemas.question import Source, Difficulty, Status, Tag

class MetadataManager:
    def get_all_metadata(self) -> Metadata:
        metadata = {
            "sources": self.get_sources(),
            "difficulties": self.get_difficulties(),
            "statuses": self.get_statuses(),
            "tags": self.get_tags()
        }

        return Metadata(**metadata)

    def get_sources(self) -> list[str]:
        return [source.value for source in Source]

    def get_difficulties(self) -> list[str]:
        return [difficulty.value for difficulty in Difficulty]

    def get_statuses(self) -> list[str]:
        return [status.value for status in Status]

    def get_tags(self) -> list[str]:
        return [tag.value for tag in Tag]
