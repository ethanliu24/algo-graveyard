import pytest

from app.schemas.question import Question, QuestionBasicInfo
from tests.seed import QUESTIONS

API = "/api/questions"

# Getting Questions
@pytest.mark.asyncio
async def test_get_all_questions_no_filter(endpoint):
    """ Test the properties of the result of the endpoint to get all questions_no_filter """
    response = endpoint.get(f"{API}?paginate=false")
    assert response.status_code == 200
    data = response.json()["data"]
    assert len(data) > 0
    assert isinstance(data, list)
    for d in data:
        QuestionBasicInfo(**d)  # validate


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
        "difficulty": "easy",
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
    q = Question(**response.json())
    assert q.title == "Create Question Basic"

@pytest.mark.asyncio
async def test_create_question_invalid_input(endpoint):
    """ Test creating a question with invalid input values. """
    question = {
        "source": "l",
        "link": "",
        "difficulty": "easy",
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
    q = Question(**response.json())
    assert q.title == "Updated title"
    assert q.prompt == "Updated prompt"
    assert q.tags == ["graph", "queue"]
    assert q.source.value == "leetcode"


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


@pytest.mark.asyncio
async def test_update_question_invalid_id(endpoint):
    """ Test updating a question but the question isn't in the db. """
    update_data = {"title": "title"}

    response = endpoint.put(f"{API}/question_dne", json=update_data)
    assert response.status_code == 404


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
    assert response.status_code == 404


# Filter, sort, search and pagination
@pytest.mark.asyncio
async def test_search_questions(endpoint):
    """ Testing if searching questions works. """
    response = endpoint.get(f"{API}?search=paginate")
    assert response.status_code == 200
    pagination = response.json()["data"]
    assert pagination["total"] == 6
    assert len(pagination["data"]) == 6
    assert pagination["pages"] == 1

@pytest.mark.asyncio
async def test_search_no_questions(endpoint):
    """ Testing if searching questions returns nothing if no questions match. """
    response = endpoint.get(f"{API}?search=paginate_no_match")
    assert response.status_code == 200
    pagination = response.json()["data"]
    assert pagination["total"] == 0
    assert len(pagination["data"]) == 0
    assert pagination["pages"] == 1

@pytest.mark.asyncio
async def test_search_case_sensitive(endpoint):
    """ Test if search returns right result when it's not case sensitive. """
    response = endpoint.get(f"{API}?search=space")
    assert response.status_code == 200
    pagination = response.json()["data"]
    assert len(pagination["data"]) == 1

@pytest.mark.asyncio
async def test_search_title_with_space(endpoint):
    """ Test with a space in the search value """
    response = endpoint.get(f"{API}?search=Space%20Here")
    assert response.status_code == 200
    pagination = response.json()["data"]
    assert len(pagination["data"]) == 1
