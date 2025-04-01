from typing import Any
from ..schemas.question import Question

class QuestionDAO:
    db: Any
    question_collection: str
    solution_collection: str

    def __init__(self, client, question_collection: str, solution_collection: str):
        self.db = client
        self.question_collection = question_collection
        self.solution_collection = solution_collection

    def get_all_questions(self) -> list[Question]:
        # TODO implement filter, use where() function
        # questions_ref = self.db.collection(self.question_collection)
        # return [self._format_question(q) for q in questions_ref.get()]
        pass

    def get_question(self, id: str) -> Question:
        doc_ref = self.db.collection(self.question_collection).document(id)
        return None if not doc_ref.get().exists else self._format_question(doc_ref)

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

    def _format_question(self, doc_ref) -> Question:
        question_data = doc_ref.get().to_dict()
        solutions_ref = doc_ref.collection(self.solution_collection)
        solutions = [s.to_dict() for s in solutions_ref.get()]
        question_data.update({ "solutions": solutions })
        return Question(**question_data)
