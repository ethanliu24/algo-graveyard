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
        questions = self.db.collection(self.question_collection).stream()
        return [self._format_question(q) for q in questions]

    def get_question(self, id: str) -> Question:
        doc = self.db.collection(self.question_collection).document(id).get()
        return None if not doc.exists else self._format_question(doc)

    def create_question(self, data: dict, id: str = None) -> str:
        collection_ref = self.db.collection(self.question_collection)
        doc_ref = collection_ref.document(id) if id else collection_ref.document()

        data.update({ "id": doc_ref.id })
        doc_ref.set(data)
        return doc_ref.id

    def delete_question(self, id: str) -> None:
        self.db.collection(self.question_collection).document(id).delete()

    def update_question(self, id: str, data: dict) -> None:
        self.db.collection(self.question_collection).document(id).update(data)

    def _format_question(self, doc) -> Question:
        question_data = doc.to_dict()
        solutions_ref = self.db.collection(self.question_collection).document(doc.id).collection(self.solution_collection)
        solutions = [s.to_dict() for s in solutions_ref.get()]
        question_data.update({ "solutions": solutions })
        return Question(**question_data)
