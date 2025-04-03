from math import ceil
from datetime import datetime
from ..daos.question_dao import QuestionDAO
from ..exceptions.entity_not_found import EntityNotFoundError
from ..schemas.pagination import Pagination
from ..schemas.question import Question, QuestionCreate, QuestionBasicInfo, QuestionAll, \
    Source, Difficulty, Status

class QuestionManager(object):
    question_dao: QuestionDAO

    def __init__(self, question_dao: QuestionDAO):
        self.question_dao = question_dao

    async def get_all_questions(
        self,
        source: Source | None = None,
        difficulty: Difficulty | None = None,
        status: Status | None = None,
        tags: list[str] | None = None,
        search: str | None = None,
        sort_by: str | None = None,
        order: str | None = None,
        page: int | None = None,
        per_page: int | None = None,
        paginate: bool | None = True
    ) -> QuestionAll:
        # initialize query params
        tags = tags or []
        search = search or ""
        sort_by = sort_by or "created_at"
        order = order or "asc"
        page = page if page is not None else 1
        per_page = per_page if per_page is not None else 20
        paginate = paginate if paginate is not None else True

        # I am broke as fuck. I can't afford firebase queries. Efficiency ain't shit.
        if order not in ["asc", "desc"]:
            raise ValueError(f"Invalid order value {order}. Must be 'asc' or 'desc'.")
        if sort_by not in ["created_at", "difficulty", "title"]:
            raise ValueError(f"Invalid order value {order}. Must be 'created_at', 'difficulty' or 'title'.")
        if per_page == 0:
            raise ValueError(f"Invalid 'per_page' value. Cannot be 0.")
        if page == 0:
            raise ValueError(f"Invalid 'page' value. Cannot be 0.")

        questions = self.question_dao.get_all_questions()
        questions = self._filter_questions(questions, source, difficulty, status, tags, search)
        self._sort_questions(questions, sort_by, order)
        return QuestionAll(**{
            "paginated": False,
            "data": questions if not paginate else self._paginate_questions(questions, page, per_page)
        })

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
        question["solutions"] = []

        creation_time = datetime.now()
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
        tags: list[str] | None,
        search: str | None
    ) -> list[QuestionBasicInfo]:
        res = []
        for question in questions:
            if (source and question.source.value == source.value) or \
               (difficulty and question.difficulty.value == difficulty.value) or \
               (status and question.status.value == status.value) or \
               (search is None or search.lower() in question.title.lower()):
                res.append(question)
                continue

            for tag in tags:
                if tag in question.tags:
                    res.append(question)
                    break

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
