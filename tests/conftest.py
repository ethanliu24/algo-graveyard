from fastapi.testclient import TestClient
import pytest

from app.config import Configs
from app.main import app
from app.schemas.ai_analysis import AiAnalysis
from app.schemas.question import Question
from app.schemas.solution import Solution
from app.schemas.test_case import TestCase
from .seed import QUESTIONS

def pytest_sessionstart():
    """ Populates the database when a test session starts. """
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


def pytest_sessionfinish():
    """ Clears the database when a test session ends. """
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


@pytest.fixture()
def setup():
    yield Configs()


@pytest.fixture()
def question_service(setup):
    yield setup.question_manager


@pytest.fixture()
def endpoint():
    client = TestClient(app)
    yield client
