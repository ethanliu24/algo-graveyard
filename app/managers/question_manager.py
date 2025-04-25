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
        print(await self.web_scrap_service.parse_question("https://leetcode.com/problems/palindrome-number/description/", "leetcode"))

        question = self.question_dao.get_question(id)
        if not question:
            raise EntityNotFoundError("Invalid question ID.")
        return question

    async def create_question(self, data: QuestionCreate, id: str = None) -> Question:
        # TODO remove print from questions
        question = data.model_dump()
        question["source"] = question["source"].value
        question["difficulty"] = question["difficulty"].value
        question["status"] = question["status"].value
        question["tags"] = [tag.value for tag in question["tags"]]
        question["solutions"] = []

        creation_time = datetime.now(timezone.utc)
        question.update({ "created_at": creation_time, "last_modified": creation_time })

        return self.question_dao.create_question(question, id)

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
