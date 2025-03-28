from __future__ import annotations
from fastapi import Depends
from typing import Annotated
from .daos.question_dao import QuestionDAO
from .env_vars import ENV_VARS
from .managers.firebase_manager import FirebaseManager
from .managers.question_manager import QuestionManager

class Configs:
    instance: Configs = None
    firebase_manager: FirebaseManager = None
    question_manager: QuestionManager = None

    def __new__(cls):
        if not cls.instance:
            cls.instance = cls.instance = super(Configs, cls).__new__(cls)

            app_env = ENV_VARS.get("APP_ENV")
            if app_env == "production":
                question_collection = "Questions"
            elif app_env == "development":
                question_collection = "dev_questions"
            else:
                question_collection = "test_db"

            solution_collection = "Solutions"

            cls.firebase_manager = FirebaseManager()
            cls.question_dao = QuestionDAO(cls.firebase_manager.get_client(), question_collection, solution_collection)
            cls.question_manager = QuestionManager(cls.question_dao)
        return cls.instance


def init_config() -> Configs:
    return Configs()


def get_question_service(configs: Annotated[Configs, Depends(init_config)]):
    return configs.question_manager
