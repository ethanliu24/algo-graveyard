from typing import Any
from ..schemas.question import Question, QuestionBasicInfo

class QuestionDAO:
    db: Any
    question_collection: str
    solution_collection: str

    def __init__(self, client, question_collection: str, solution_collection: str):
        self.db = client
        self.question_collection = question_collection
        self.solution_collection = solution_collection

    def get_all_questions(self) -> list[QuestionBasicInfo]:
        # TODO implement filter, use where() function
        # TODO implement pagination
        questions = self.db.collection(self.question_collection).get()
        res = []
        for q_data in questions:
            d = q_data.to_dict()
            d.update({ "solutions": [] })  # What the solution is doesn't matter
            q = Question(**d)
            data = {"id": q.id, "source": q.source.value, "difficulty": q.difficulty.value, "status": q.status.value,
                    "title": q.title, "tags": q.tags, "created_at": q.created_at, "last_modified": q.last_modified}
            res.append(QuestionBasicInfo(**data))
        return res

    def get_question(self, id: str) -> Question:
        doc_ref = self.db.collection(self.question_collection).document(id)
        if not doc_ref.get().exists:
            return None

        question_data = doc_ref.get().to_dict()
        solutions_ref = doc_ref.collection(self.solution_collection)
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
        doc_ref = self.db.collection(self.question_collection).document(id)
        res = doc_ref.get().exists
        doc_ref.delete()
        return res

    def update_question(self, id: str, data: dict) -> Question:
        doc_ref = self.db.collection(self.question_collection).document(id)
        doc_ref.update(data)
        return Question(**doc_ref.get().to_dict())
