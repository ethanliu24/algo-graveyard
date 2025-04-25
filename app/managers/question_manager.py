from datetime import datetime, timezone
from .metadata_manager import MetadataManager
from .web_scrape_manager import WebScrapeManager
from ..daos.question_dao import QuestionDAO
from ..exceptions.entity_not_found import EntityNotFoundError
from ..schemas.pagination import Pagination
from ..schemas.question import Question, QuestionCreate, Source, Difficulty, Status, Tag

class QuestionManager(object):
    question_dao: QuestionDAO
    metadata_manager: MetadataManager
    web_scrap_service: WebScrapeManager

    def __init__(self, question_dao: QuestionDAO, metadata_manager: MetadataManager, web_scrap_service: WebScrapeManager):
        self.question_dao = question_dao
        self.metadata_manager = metadata_manager
        self.web_scrap_service = web_scrap_service

    async def get_all_questions(
        self,
        source: Source | None = None,
        difficulty: Difficulty | None = None,
        status: Status | None = None,
        tags: list[Tag] | None = None,
        search: str | None = None,
        sort_by: str | None = None,
        order: str | None = None,
        page: int | None = None,
        per_page: int | None = None,
    ) -> Pagination:
        # initialize query params
        tags = tags or []
        search = search or ""
        sort_by = sort_by or "last_modified"
        order = order or ("desc" if sort_by == "last_modified" or sort_by == "created_at" else "asc")
        page = max(1, page) if page is not None else 1
        per_page = min(50, max(1, per_page)) if per_page is not None else 20

        if order not in self.metadata_manager.get_order():
            raise ValueError(f"Invalid order value {order}. Valid values: {self.metadata_manager.get_order()}.")
        if sort_by not in self.metadata_manager.get_sort_by():
            raise ValueError(f"Invalid order value {order}. Valid values: {self.metadata_manager.get_sort_by()}.")

        return self.question_dao.get_all_questions(
            source, difficulty, status, tags, search, sort_by, order, page, per_page
        )

    async def get_question(self, id: str) -> Question:
        question = self.question_dao.get_question(id)
        if not question:
            raise EntityNotFoundError("Invalid question ID.")
        return question

    async def create_question(self, data: dict, id: str = None) -> Question:
        link = data.get("link", "")
        source = data.get("source", "")
        scraped_data = {}
        if link != "":
            scraped_data = await self.web_scrap_service.parse_question(link, source)
            self._sanitize_scraped_data(scraped_data)

            if not scraped_data["title"] or not scraped_data["prompt"]:
                raise ValueError("Parsing failed.")

            self._merge_data(data, scraped_data)

        # validate data
        data = QuestionCreate(**data).model_dump()
        data["solutions"] = []
        data["source"] = data["source"].value
        data["difficulty"] = data["difficulty"].value
        data["status"] = data["status"].value
        data["tags"] = [t.value for t in data["tags"]]
        creation_time = datetime.now(timezone.utc)
        data.update({ "created_at": creation_time, "last_modified": creation_time })

        return self.question_dao.create_question(data, id)

    def _sanitize_scraped_data(self, data: dict) -> None:
        if not data["difficulty"] in self.metadata_manager.get_difficulties():
            data["difficulty"] = Difficulty.EASY.value

        data["tags"] = [tag for tag in data["tags"] if tag in self.metadata_manager.get_tags()]

    def _merge_data(self, data: dict, scraped_data: dict):
        title = data.get("title", "")
        data["title"] = title if title else scraped_data["title"]
        prompt = data.get("prompt", "")
        data["prompt"] = prompt if prompt else scraped_data["title"]
        difficulty = data.get("difficulty", "")
        data["difficulty"] = difficulty if difficulty else scraped_data["difficulty"]
        data["hints"] = data.get("hints", []) + scraped_data["hints"]
        data["tags"] = list(set(data.get("tags", []) + scraped_data["tags"]))

    async def update_question(self, data: dict, id: str) -> Question:
        question = await self.get_question(id)
        question_data = question.model_dump()
        data.update({ "last_modified": datetime.now() })
        question_data.update(data)
        _ = Question(**question_data) # validate data
        return self.question_dao.update_question(id, data)

    async def delete_question(self, id: str) -> None:
        if not self.question_dao.delete_question(id):
            raise EntityNotFoundError("Invalid question ID.")
