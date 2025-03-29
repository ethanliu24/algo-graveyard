from fastapi import HTTPException
import pytest

from app.schemas.question import Question
from tests.seed import QUESTIONS

API = "/api/questions"

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
    """ Test if endpoint gets the right question if it exists in the database. """
    response = endpoint.get(f"{API}/question_dne")
    assert response.status_code == 404
