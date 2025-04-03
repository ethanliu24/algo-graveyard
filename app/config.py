from __future__ import annotations
from fastapi import Depends
from typing import Annotated
from .daos.question_dao import QuestionDAO
from .daos.solution_dao import SolutionDAO
from .env_vars import ENV_VARS
from .managers.firebase_manager import FirebaseManager
from .managers.question_manager import QuestionManager
from .managers.solution_manager import SolutionManager
from .managers.auth_manager import AuthManager, JWTBearer

class Configs:
    instance: Configs = None
    firebase_manager: FirebaseManager = None
    question_dao: QuestionDAO = None
    solution_dao: SolutionDAO = None
    question_manager: QuestionManager = None
    solution_manager: SolutionManager = None
    auth_manager: AuthManager = None
    question_collection: str = ""
    solution_collection: str = ""

    def __new__(cls):
        if not cls.instance:
            cls.instance = cls.instance = super(Configs, cls).__new__(cls)

            app_env = ENV_VARS.get("APP_ENV")
            if app_env == "production":
                cls.question_collection = "Questions"
            elif app_env == "development":
                cls.question_collection = "dev_questions"
            else:
                cls.question_collection = "test_db"

            cls.solution_collection = "Solutions"

            cls.firebase_manager = FirebaseManager()
            cls.question_dao = QuestionDAO(
                cls.firebase_manager.get_client(),
                cls.question_collection,
                cls.solution_collection
            )
            cls.solution_dao = SolutionDAO(
                cls.firebase_manager.get_client(),
                cls.question_collection,
                cls.solution_collection
            )

            cls.question_manager = QuestionManager(cls.question_dao)
            cls.solution_manager = SolutionManager(cls.solution_dao)
            cls.auth_manager = AuthManager(
                ENV_VARS.get("APP_SECRET"),
                ENV_VARS.get("JWT_SIGNITURE"),
                ENV_VARS.get("JWT_HS_ALG"),
                float(ENV_VARS.get("JWT_EXP_TIME")),
                ENV_VARS.get("JWT_ISS"),
                ENV_VARS.get("JWT_AUD")
            )

        return cls.instance


def init_config() -> Configs:
    return Configs()


def get_question_service(configs: Annotated[Configs, Depends(init_config)]):
    return configs.question_manager


def get_solution_service(configs: Annotated[Configs, Depends(init_config)]):
    return configs.solution_manager


def get_auth_service(configs: Annotated[Configs, Depends(init_config)]):
    return configs.auth_manager

jwt_auth = JWTBearer(Configs().auth_manager)
