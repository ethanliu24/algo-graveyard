from fastapi.testclient import TestClient
import pytest

from app.config import Configs
from app.main import app
from app.schemas.ai_analysis import AiAnalysis
from app.schemas.question import Question
from app.schemas.solution import Solution
from app.schemas.test_case import TestCase
from .seed import QUESTIONS

@pytest.fixture()
def setup():
    configs = Configs()
    client = configs.firebase_manager.get_client()


    def populate_database():
        for q_data in QUESTIONS:
            q_id = q_data["id"]

            # validate solutions
            for sln_data in q_data["solutions"]:
                _ = Solution(**sln_data)
                _ = [AiAnalysis(**analysis_data) for analysis_data in q_data["ai_analysis"]]

                client.collection(configs.question_collection) \
                    .document(q_id) \
                    .collection(configs.solution_collection) \
                    .document(sln_data["id"]) \
                    .set(sln_data)

            # validate test cases
            _ = [TestCase(**test_data) for test_data in q_data["test_cases"]]

            _ = Question(**q_data)  # validate question
            client.collection(configs.question_collection).document(q_id).set(q_data)

    def clear_database():
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

    populate_database()
    yield configs
    clear_database()


@pytest.fixture()
def question_service(setup):
    yield setup.question_manager


@pytest.fixture()
def endpoint():
    client = TestClient(app)
    yield client
