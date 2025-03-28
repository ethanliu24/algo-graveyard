import pytest

from app.config import Configs
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
                client.collection(configs.question_collection) \
                    .document(q_id) \
                    .collection(configs.solution_collection) \
                    .document(sln_data["id"]) \
                    .set(sln_data)

            _ = Question(**q_data)  # validate
            client.collection(configs.question_collection).document(q_id).set(q_data)

    def clear_database(batch_size: int = 20):
        if batch_size == 0:
            return

        questions = client.collection(configs.question_collection).list_documents(page_size=batch_size)
        deleted = 0

        for question in questions:
            # delete solutions subcollection
            solutions = client \
                .collection(configs.question_collection) \
                .document(question.id) \
                .collection(configs.solution_collection)

            for solution in solutions:
                solution.delete()

            questions.delete()
            deleted = deleted + 1

        if deleted >= batch_size:
            return clear_database(batch_size)

    populate_database()
    yield configs
    # clear_database()


@pytest.fixture()
def question_service(setup):
    yield setup.question_manager
