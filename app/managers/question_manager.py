from ..managers.firebase_manager import FirebaseManager
from ..schemas.question import Question

class QuestionManager(object):
    instance = None
    db = None

    def __new__(cls, db: FirebaseManager):
        if not cls.instance:
            cls.instance = super(QuestionManager, cls).__new__(cls)
            cls.db = db
        return cls.instance

    def get_all_questions(self) -> list[Question]:
        return self.db.get_questions()