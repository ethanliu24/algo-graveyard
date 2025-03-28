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

    def get_all_questions(self) -> Question:
        # TODO implement filter, use where() function
        questions = self.db.collection(self.question_collection).stream()
        return [self._format_question(q) for q in questions]

    def get_question(self, id: str):
        doc = self.db.collection(self.question_collection).document(id).get()
        return None if not doc.exists else self._format_question(doc)

    def create_question(self, data: dict, id: str = None) -> str:
        collection = self.db.collection(self.question_collection)
        if id:
            _, doc = collection.document(id).set(data)
        else:
            _, doc = collection.add(data)

        return doc.id

    def delete_question(self, id: str):
        self.db.collection(self.question_collection).document(id).delete()

    def update_question(self, id: str, data: dict):
        self.db.collection(self.question_collection).document(id).update(data)

    def _format_question(self, doc) -> Question:
        question_data = doc.to_dict()
        question_data.update({ "id": doc.id })
        solutions_ref = self.db.collection(self.question_collection).document(doc.id).collection(self.solution_collection)
        solutions = [s.to_dict() for s in solutions_ref.get()]
        question_data.update({ "solutions": solutions })
        return Question(**question_data)
