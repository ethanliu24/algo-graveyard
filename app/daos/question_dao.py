from typing import Any

class QuestionDAO:
    db: Any
    question_collection: str
    solution_collection: str

    def __init__(self, client, question_collection: str, solution_collection: str):
        self.db = client
        self.question_collection = question_collection
        self.solution_collection = solution_collection

    def get_all_questions(self):
        # TODO implement filter, use where() function
        return self.db.collection(self.question_collection).stream()

    def get_question(self, id: str):
        return self.db.collection(self.question_collection).document(id).get()

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
