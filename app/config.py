from __future__ import annotations
from fastapi import Depends
from typing import Annotated
from .daos.question_dao import QuestionDAO
from .daos.solution_dao import SolutionDAO
from .env_vars import ENV_VARS
from .managers.auth_manager import AuthManager, JWTBearer
from .managers.firebase_manager import FirebaseManager
from .managers.ai_analysis_manager import AiAnalysisManager
from .managers.metadata_manager import MetadataManager
from .managers.question_manager import QuestionManager
from .managers.solution_manager import SolutionManager

class Configs:
    instance: Configs = None
    firebase_manager: FirebaseManager = None
    question_dao: QuestionDAO = None
    solution_dao: SolutionDAO = None
    question_manager: QuestionManager = None
    solution_manager: SolutionManager = None
    auth_manager: AuthManager = None
    metadata_manager: MetadataManager = None
    ai_analysis_manager = None
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

            cls.metadata_manager = MetadataManager()

            cls.auth_manager = AuthManager(
                ENV_VARS.get("APP_SECRET"),
                ENV_VARS.get("JWT_SIGNITURE"),
                ENV_VARS.get("JWT_HS_ALG"),
                float(ENV_VARS.get("JWT_EXP_TIME")),
                ENV_VARS.get("JWT_ISS"),
                ENV_VARS.get("JWT_AUD")
            )

            ai_ctx = """
            You are an expert code reviewer. You will be given a coding problem,
            a solution and the language its written in.
            Note that the solution may be invalid, empty or incorrect.
            Analyze the solution briefly but insightfully in 1-2 paragraphs.

            Your feedback should assess correctness, efficiency, and clarity.
            Mention strengths and suggest improvements if applicable.
            Point out any errors in the code if applicable.
            Highlight the worst-case time and space complexity.

            Return the data in a serilized JSON string for python to deserialize with the following fields:
            - time_complexity: str, the WC time complexity of the solution (e.g. n^2, not O(n^2))
            - space_complexity: str, the WC space complexity of the solution (e.g. n, not O(n))
            - feedback: str, the feedback to the solution

            If any information is missing or invalid, ignore it. Do NOT provide a solution nor a possible solution.
            If rate limit reached return empty string for each field.
            """

            cls.ai_analysis_manager = AiAnalysisManager(
                ENV_VARS.get("GEMINI_API_KEY"), ENV_VARS.get("GEMINI_MODEL"), ai_ctx
            )

            cls.question_manager = QuestionManager(cls.question_dao, cls.metadata_manager)
            cls.solution_manager = SolutionManager(cls.solution_dao, cls.ai_analysis_manager)

        return cls.instance


def init_config() -> Configs:
    return Configs()


def get_question_service(configs: Annotated[Configs, Depends(init_config)]):
    return configs.question_manager


def get_solution_service(configs: Annotated[Configs, Depends(init_config)]):
    return configs.solution_manager


def get_metadata_service(configs: Annotated[Configs, Depends(init_config)]):
    return configs.metadata_manager


def get_auth_service(configs: Annotated[Configs, Depends(init_config)]):
    return configs.auth_manager


def get_ai_analysis_service(configs: Annotated[Configs, Depends(init_config)]):
    return configs.ai_analysis_manager


auth_user_jwt = JWTBearer(Configs().auth_manager)
