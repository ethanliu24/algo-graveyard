from .env_vars import ENV_VARS
from .managers.firebase_manager import FirebaseManager
from .managers.question_manager import QuestionManager

class Configs:
    firebase_manager: FirebaseManager
    question_manager: QuestionManager

    def __init__(self):
        app_env = ENV_VARS.get("APP_ENV")
        if app_env == "production":
            question_collection = "Questions"
        elif app_env == "development":
            question_collection = "dev_questions"
        else:
            question_collection = "test_db"

        self.firebase_manager = FirebaseManager()
        self.question_manager = QuestionManager(self.firebase_manager, question_collection)
