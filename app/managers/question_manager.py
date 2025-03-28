from datetime import datetime
from ..daos.question_dao import QuestionDAO
from ..schemas.question import Question, QuestionCreate

class QuestionManager(object):
    question_dao: QuestionDAO

    def __init__(self, question_dao: QuestionDAO):
        self.question_dao = question_dao

    async def get_all_questions(self) -> list[Question]:
        return self.question_dao.get_all_questions()

    async def get_question(self, id: str) -> Question:
        question = self.question_dao.get_question(id)
        if not question:
            raise ValueError("Invalid question ID.")
        return question

    async def create_question(self, data: QuestionCreate, id: str = None) -> str:
        question = data.model_dump()
        question["source"] = question["source"].value
        question["status"] = question["status"].value

        creation_time = datetime.now()
        question.update({ "created_at": creation_time, "last_modified": creation_time })

        return self.question_dao.create_question(question, id)

    async def update_question(self, data: dict, id: str) -> None:
        question_data = self.get_question(id).model_dump()
        question_data.update(data)
        _ = Question(**question_data) # validate data
        self.question_dao.update_question(id, question_data)

    async def delete_question(self, id: str) -> None:
        return self.question_dao.delete_question(id)
