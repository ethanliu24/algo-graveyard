from math import ceil
from datetime import datetime, timezone
from .metadata_manager import MetadataManager
from ..daos.question_dao import QuestionDAO
from ..exceptions.entity_not_found import EntityNotFoundError
from ..schemas.pagination import Pagination
from ..schemas.question import Question, QuestionCreate, QuestionBasicInfo, \
    Source, Difficulty, Status, Tag

class QuestionManager(object):
    question_dao: QuestionDAO
    metadata_manager: MetadataManager

    def __init__(self, question_dao: QuestionDAO, metadata_manager: MetadataManager):
        self.question_dao = question_dao
        self.metadata_manager = metadata_manager

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
        paginate: bool | None = True
    ) -> Pagination:
        # initialize query params
        tags = tags or []
        search = search or ""
        sort_by = sort_by or "created_at"
        order = order or "asc"
        page = min(50, page) if page is not None else 1
        per_page = max(1, per_page) if per_page is not None else 20
        paginate = paginate if paginate is not None else True

        if order not in self.metadata_manager.get_order():
            raise ValueError(f"Invalid order value {order}. Valid values: {self.metadata_manager.get_order()}.")
        if sort_by not in self.metadata_manager.get_sort_by():
            raise ValueError(f"Invalid order value {order}. Valid values: {self.metadata_manager.get_sort_by()}.")

        questions = self.question_dao.get_all_questions(
            source, difficulty, status, tags, search, sort_by, order, page, per_page
        )
        return self._paginate_questions(questions, page, per_page)

    async def get_question(self, id: str) -> Question:
        question = self.question_dao.get_question(id)
        if not question:
            raise EntityNotFoundError("Invalid question ID.")
        return question

    async def create_question(self, data: QuestionCreate, id: str = None) -> Question:
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

    def _filter_questions(
        self,
        questions: list[QuestionBasicInfo],
        source: Source | None,
        difficulty: Difficulty | None,
        status: Status | None,
        tags: list[Tag] | None,
        search: str | None
    ) -> list[QuestionBasicInfo]:
        """
        Source, difficulty and status are primary filters. Tags and search are secondary filters.
        For each filtering, we must check:
            1. For all filters, if all of them are None, check search and tag.
            2. If all are not None, everything must match. Then, check search and tag.
            3. If one of the filters is not None, check these filters, and then check search and tag.
            4. If search is contained in the title. If search is empty or None, treat it as a match.
            5. If tag is present in the the question. If tags is empty or None, treat it as a match.
            6. If the question's tag is empty, treat it as a mismatch unless the tag filter is empty or None.
        """
        res = []

        for question in questions:
            if all([
                not source or question.source.value == source.value,
                not difficulty or question.difficulty.value == difficulty.value,
                not status or question.status.value == status.value
            ]) or all(ftr is None for ftr in [source, difficulty, status]):
                if not search or search.lower() in question.title.lower():
                    if not tags or any(question.tags and tag in question.tags for tag in tags):
                        res.append(question)

        return res

    def _sort_questions(self, questions: list[QuestionBasicInfo], sort_by: str, order: bool) -> None:
        diff_prio = {
            Difficulty.EASY.value: 0,
            Difficulty.MEDIUM.value: 1,
            Difficulty.HARD.value: 2,
        }

        sorting_key = {
            "created_at": lambda q: (q.created_at.timestamp(), q.title),
            "difficulty": lambda q: (diff_prio[q.difficulty.value], -q.created_at.timestamp()),
            "title": lambda q: (q.title, -q.created_at.timestamp()),
        }

        questions.sort(
            key=sorting_key[sort_by],
            reverse=(False if order == "asc" else True)
        )

    def _paginate_questions(self, questions: list[QuestionBasicInfo], page: int, per_page: int) -> Pagination:
        total = len(questions)
        total_pages = max(1, ceil(total / per_page))
        page = max(1, min(page, total_pages))
        start = (page - 1) * per_page
        data = {
            "data": questions[start:start+per_page],
            "page": page,
            "per_page": per_page,
            "pages": total_pages,
            "total": total,
        }
        return Pagination(**data)
