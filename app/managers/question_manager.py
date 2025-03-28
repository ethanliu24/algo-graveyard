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

    async def get_all_questions(cls) -> list[Question]:
        docs = cls.db.get_all(cls.question_collection)
        return [cls._format_question(doc) for doc in docs]

    async def get_question(cls, id: str) -> Question:
        return cls.db.get(cls.question_collection, id)

    async def create_question(cls, data: QuestionCreate, id: str = None) -> str:
        question = data.model_dump()
        question["source"] = question["source"].value
        question["status"] = question["status"].value

        creation_time = datetime.now()
        question.update({ "created_at": creation_time, "last_modified": creation_time })

        return cls.db.create(question, cls.question_collection, id)

    async def update_question(cls, data: dict, id: str) -> None:
        question_data = cls.get_question(id).model_dump()
        question_data.update(data)
        _ = Question(**question_data) # validate data
        cls.db.update(cls.question_collection, id, question_data)

    async def delete_question(cls, id: str) -> None:
        return cls.db.delete(cls.question_collection, id)

    def _format_question(cls, doc) -> Question:
        return Question(**(doc.to_dict().update({ "id": doc.id })))
