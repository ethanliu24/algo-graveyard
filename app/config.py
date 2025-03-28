from .managers.firebase_manager import FirebaseManager
from .managers.question_manager import QuestionManager

class Configs:
    firebase_manager: FirebaseManager
    question_collection: str

    def __init__(self):
        self.firebase_manager = FirebaseManager(question_collection="Questions")
        self.question_manager = QuestionManager(self.firebase_manager)
