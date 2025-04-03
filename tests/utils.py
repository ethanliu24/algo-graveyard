import jwt
import time

from app.config import Configs
from app.env_vars import ENV_VARS
from app.schemas.ai_analysis import AiAnalysis
from app.schemas.question import Question
from app.schemas.solution import Solution
from app.schemas.test_case import TestCase
from app.schemas.token import Token
from tests.seed import QUESTIONS

def populate_database():
    """ Populates the database. """
    configs = Configs()
    client = configs.firebase_manager.get_client()

    seen_q = set()
    for q_data in QUESTIONS:
        # sanity check for duplication
        q_id = q_data["id"]
        if q_id in seen_q:
            raise ValueError("Duplicate ID. Check if database question IDs are unique.")
        seen_q.add(q_id)

        # validate solutions
        seen_sln = set()
        for sln_data in q_data["solutions"]:
            # sanity check for duplication
            sln_id = sln_data["id"]
            if sln_id in seen_sln:
                raise ValueError(f"Duplicate ID. Check if database solution IDs in question {q_id} are unique.")
            seen_sln.add(sln_id)

            _ = Solution(**sln_data)
            _ = AiAnalysis(**sln_data["ai_analysis"])

            client.collection(configs.question_collection) \
                .document(q_id) \
                .collection(configs.solution_collection) \
                .document(sln_id) \
                .set(sln_data)

        _ = [TestCase(**test_data) for test_data in q_data["test_cases"]] # validate test cases

        _ = Question(**q_data)  # validate question
        client.collection(configs.question_collection).document(q_id).set(q_data)


def clear_database():
    """ Clears the database. """
    configs = Configs()
    client = configs.firebase_manager.get_client()
    questions = client.collection(configs.question_collection).stream()

    for question in questions:
        # delete solutions subcollection
        solutions = client \
            .collection(configs.question_collection) \
            .document(question.id) \
            .collection(configs.solution_collection) \
            .stream()

        for solution in solutions:
            solution_ref = solution.reference
            solution_ref.delete()

        question_ref = question.reference
        question_ref.delete()


def create_jwt_token(
    iss: str = ENV_VARS.get("JWT_ISS"),
    aud: str = ENV_VARS.get("JWT_AUD"),
    exp: float = float(ENV_VARS.get("JWT_EXP_TIME")),
    jwt_secret: str = ENV_VARS.get("JWT_SIGNITURE"),
    hs_alg: str = ENV_VARS.get("JWT_HS_ALG")
) -> str:
    payload = {
        "iss": iss,
        "aud": aud,
        "exp": time.time() + (exp * 60)
    }

    _ = Token(**payload)
    return jwt.encode(payload, jwt_secret, algorithm=hs_alg)


def set_jwt_cookie(endpoint, response):
    set_cookie_header = response.headers.get("set-cookie")
    cookie_values = set_cookie_header.split(";")
    for val in cookie_values:
        res = val.split("=")
        if res[0] == ENV_VARS.get("JWT_COOKIE"):
            endpoint.cookies.set(ENV_VARS.get("JWT_COOKIE"), res[1])
            break
        