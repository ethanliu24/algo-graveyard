from google.cloud import firestore
from google.cloud.firestore_v1 import aggregation
from google.cloud.firestore_v1.base_query import FieldFilter
from math import ceil
from typing import Any
from ..schemas.pagination import Pagination
from ..schemas.question import Question, Source, Difficulty, Status, Tag
from ..schemas.solution import Solution

class QuestionDAO:
    db: Any
    question_collection: str
    solution_collection: str

    def __init__(self, client, question_collection: str, solution_collection: str):
        self.db = client
        self.question_collection = question_collection
        self.solution_collection = solution_collection

    def get_all_questions(
        self,
        source: Source | None,
        difficulty: Difficulty | None,
        status: Status | None,
        tags: list[Tag],
        search: str,
        sort_by: str,
        order: str,
        page: int,
        per_page: int,
    ) -> Pagination:
        query = self.db.collection(self.question_collection).offset(0)

        if tags:
            query = query.where(filter=FieldFilter("tags", "array_contains_any", [t.value for t in tags]))
        if difficulty is not None:
            query = query.where(filter=FieldFilter("difficulty", "==", difficulty.value))
        if source is not None:
            query = query.where(filter=FieldFilter("source", "==", source.value))
        if status is not None:
            query = query.where(filter=FieldFilter("status", "==", status.value))

        # count number of questions before pagination
        count_aggregation = aggregation.AggregationQuery(query).count(alias="total")
        total_questions = 0
        for result in count_aggregation.get():
            total_questions += result[0].value
        total_pages = max(1, ceil(total_questions / per_page))
        questions = query.stream()

        res = []
        for q_data in questions:
            d = q_data.to_dict()
            if search.lower() not in d["title"].lower():
                total_questions -= 1
                continue

            d.update({ "solutions": [Solution(**sln) for sln in d["solutions"]] })

            res.append(Question(**d))

        page = min(page, total_pages)
        start = (page - 1) * per_page
        res = res[start:start+per_page]
        self._sort_questions(res, sort_by, order)

        pagination = {
            "data": res,
            "page": page,
            "per_page": per_page,
            "pages": total_pages,
            "total": total_questions,
        }

        return Pagination(**pagination)

    def _sort_questions(self, questions: list[Question], sort_by: str, order: bool) -> None:
        diff_prio = {
            Difficulty.EASY.value: 0,
            Difficulty.MEDIUM.value: 1,
            Difficulty.HARD.value: 2,
        }

        sorting_key = {
            "created_at": lambda q: (q.created_at.timestamp(), q.title),
            "last_modified": lambda q: (q.last_modified.timestamp(), q.title),
            "difficulty": lambda q: (diff_prio[q.difficulty.value], -q.created_at.timestamp()),
            "title": lambda q: (q.title, -q.created_at.timestamp()),
        }

        questions.sort(
            key=sorting_key[sort_by],
            reverse=(False if order == "asc" else True)
        )

    def get_question(self, id: str) -> Question:
        doc_ref = self.db.collection(self.question_collection).document(id)
        if not doc_ref.get().exists:
            return None

        question_data = doc_ref.get().to_dict()
        solutions_ref = doc_ref.collection(self.solution_collection) \
            .order_by("last_modified", direction=firestore.Query.DESCENDING)
        solutions = [s.to_dict() for s in solutions_ref.get()]
        question_data.update({ "solutions": solutions })
        return Question(**question_data)

    def create_question(self, data: dict, id: str = None) -> Question:
        collection_ref = self.db.collection(self.question_collection)
        doc_ref = collection_ref.document(id) if id else collection_ref.document()

        data.update({ "id": doc_ref.id })
        doc_ref.set(data)
        return Question(**data)

    def delete_question(self, id: str) -> bool:
        q_ref = self.db.collection(self.question_collection).document(id)
        if not q_ref.get().exists: return False

        # del solutions
        sln_collection_ref = q_ref.collection(self.solution_collection)
        for sln in sln_collection_ref.stream():
            sln.reference.delete()  # Delete each solution document

        q_ref.delete()
        return True

    def update_question(self, id: str, data: dict) -> Question:
        doc_ref = self.db.collection(self.question_collection).document(id)
        doc_ref.update(data)
        return Question(**doc_ref.get().to_dict())
