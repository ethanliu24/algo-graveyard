from fastapi import HTTPException
import pytest

from app.schemas.question import Question
from tests.seed import QUESTIONS

API = "/api/questions"

# Getting Questions
@pytest.mark.asyncio
async def test_get_all_questions_no_filter(endpoint):
    """ Test the properties of the result of the endpoint to get all questions_no_filter """
    response = endpoint.get(f"{API}")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert isinstance(data, list)
    for d in data:
        Question(**d)  # validate


@pytest.mark.asyncio
async def test_get_question_exists(endpoint):
    """ Test if endpoint gets the right question if it exists in the database. """
    expected = Question(**QUESTIONS[0])

    response = endpoint.get(f"{API}/q1")
    assert response.status_code == 200
    actual = Question(**response.json())
    assert actual == expected


@pytest.mark.asyncio
async def test_get_question_doesnt_exist(endpoint):
    """ Test if endpoint when question id doesn't exist in the database. """
    response = endpoint.get(f"{API}/question_dne")
    assert response.status_code == 404


# Creating questions
@pytest.mark.asyncio
async def test_create_question_basic(endpoint):
    """ Test creating a question with basic inputs. """
    question = {
        "source": "leetcode",
        "link": "",
        "status": "completed",
        "title": "Create Question Basic",
        "prompt": "create a basic question",
        "test_cases": [],
        "notes": [],
        "hints": [],
        "tags": []
    }

    response = endpoint.post(f"{API}", json=question)
    assert response.status_code == 200
    assert isinstance(response.text, str)


@pytest.mark.asyncio
async def test_create_question_invalid_input(endpoint):
    """ Test creating a question with invalid input values. """
    question = {
        "source": "l",
        "link": "",
        "status": "",
        "title": "Create Question Basic",
        "prompt": "create a basic question",
        "test_cases": [],
        "notes": [],
        "hints": [],
        "tags": []
    }

    response = endpoint.post(f"{API}", json=question)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_question_missing_fields(endpoint):
    """ Test creating a question with missing fields. """
    question = {
        "link": "",
        "status": "",
        "title": "Create Question Basic",
        "test_cases": [],
        "hints": [],
        "tags": []
    }

    response = endpoint.post(f"{API}", json=question)
    assert response.status_code == 422


# Updating questions
@pytest.mark.asyncio
async def test_update_question_basic(endpoint):
    """ Test updating a question with basic update values. """
    title = "Updated title"
    prompt = "Updated prompt"
    tags = ["graph", "queue"]
    update_data = {"title": title, "prompt": prompt, "tags": tags}

    response = endpoint.put(f"{API}/q1", json=update_data)
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_update_question_invalid_data(endpoint):
    """ Test updating a question but the data is invalid. """
    source = "aslkdjf"
    update_data = {"source": source}

    response = endpoint.put(f"{API}/q1", json=update_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_question_invalid_field(endpoint):
    """ Test updating a question but the field is invalid. """
    invalid = "invalid"
    update_data = {"invalid": invalid}

    response = endpoint.put(f"{API}/q1", json=update_data)
    assert response.status_code == 422


# Delete questions
@pytest.mark.asyncio
async def test_update_question_exists(endpoint):
    """ Test deleting a question that exists in the database. """
    response = endpoint.delete(f"{API}/delete_endpoint")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_update_question_doesnt_exist(endpoint):
    """ Test deleting a question that doesn't exist in the database. """
    response = endpoint.delete(f"{API}/delete_dne")
    assert response.status_code == 200
