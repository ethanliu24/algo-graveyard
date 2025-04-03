from fastapi.testclient import TestClient
import pytest
import utils

from app.config import Configs
from app.main import app

def pytest_sessionstart():
    utils.populate_database()


def pytest_sessionfinish():
    utils.clear_database()


@pytest.fixture()
def setup():
    yield Configs()


@pytest.fixture()
def solution_service(setup):
    yield setup.solution_manager


@pytest.fixture()
def question_service(setup):
    yield setup.question_manager


@pytest.fixture()
def endpoint():
    client = TestClient(app)
    yield client


@pytest.fixture()
def cookie():
    {"jwt_cookie": utils.create_jwt_token()}
