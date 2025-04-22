from google.cloud import firestore
from typing import Any
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
    ) -> list[Question]:
        query = self.db.collection(self.question_collection)

        if difficulty is not None:
            query = query.where("difficulty", "==", difficulty.value)
        if source is not None:
            query = query.where("source", "==", source.value)
        if status is not None:
            query = query.where("status", "==", status.value)

        sort_dir = firestore.Query.DESCENDING if order == 'desc' else firestore.Query.ASCENDING
        questions = \
            query.order_by(sort_by, direction=sort_dir) \
            .offset((page - 1) * per_page) \
            .limit(per_page) \
            .stream()

        res = []
        for q_data in questions:
            d = q_data.to_dict()
            if search not in d["title"]:
                continue

            d.update({ "solutions": [Solution(**sln) for sln in d["solutions"]] })
            q = Question(**d)

            if not tags:
                res.append(q)
                continue

            for tag in tags:
                if tag.value in d["tags"]:
                    res.append(q)
                    break

        return res

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
