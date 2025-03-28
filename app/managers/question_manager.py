from datetime import datetime
from ..managers.firebase_manager import FirebaseManager
from ..schemas.question import Question, QuestionCreate

class QuestionManager(object):
    instance = None
    db = None
    question_collection = None

    def __new__(cls, db: FirebaseManager, question_collection: str):
        if not cls.instance:
            cls.instance = super(QuestionManager, cls).__new__(cls)
            cls.db = db
            cls.question_collection = question_collection
        return cls.instance

    def get_all_questions(cls) -> list[Question]:
        return cls.db.get_all_question(cls.question_collection)

    def get_question(cls, id: str) -> Question:
        return cls.db.get_question(cls.question_collection, id)

    def create_question(cls, data: QuestionCreate, id: str = None) -> str:
        question = data.model_dump()
        question["source"] = question["source"].value
        question["status"] = question["status"].value

        creation_time = datetime.now()
        question.update({ "created_at": creation_time, "last_modified": creation_time })

        return cls.db.create_question(question, cls.question_collection, id)

    def delete_question(cls, id: str) -> None:
        return cls.db.delete(cls.question_collection, id)
