from datetime import datetime
from ..managers.firebase_manager import FirebaseManager
from ..schemas.question import Question, QuestionCreate

class QuestionManager(object):
    instance = None
    db = None

    def __new__(cls, db: FirebaseManager):
        if not cls.instance:
            cls.instance = super(QuestionManager, cls).__new__(cls)
            cls.db = db
        return cls.instance

    def get_all_questions(self) -> list[Question]:
        return self.db.get_all_question()

    def get_question(self, id: str) -> Question:
        return self.db.get_question(id)

    def create_question(self, data: QuestionCreate) -> str:
        question = data.model_dump()
        question["source"] = question["source"].value
        question["status"] = question["status"].value

        creation_time = datetime.now()
        question.update({ "created_at": creation_time, "last_modified": creation_time })

        return self.db.create_question(question)

    def delete_question(self, id: str) -> None:
        return self.db.delete(id)
