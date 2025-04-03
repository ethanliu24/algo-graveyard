import pytest
import tests.utils as utils

from fastapi.testclient import TestClient

from app.config import Configs
from app.main import app
from app.env_vars import ENV_VARS

def pytest_sessionstart():
    utils.seed_database()


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
def auth_service(setup):
    yield setup.auth_manager


@pytest.fixture()
def endpoint():
    client = TestClient(app)
    client.cookies.set(ENV_VARS.get("JWT_COOKIE"), utils.create_jwt_token())
    yield client

