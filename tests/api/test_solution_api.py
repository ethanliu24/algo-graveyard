import pytest

from tests.seed import QUESTIONS
from app.schemas.solution import Solution

API = "/api/questions"

# Getting Questions
@pytest.mark.asyncio
async def test_get_q_has_one_solution(endpoint):
    """ Get all solutions of a question that has one solution. """
    response = endpoint.get(f"{API}/q1/solutions")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert isinstance(data, list)
    s = Solution(**data[0])
    assert s.summary == "Test"
    assert s.explanation == "test"

@pytest.mark.asyncio
async def test_get_q_has_many_solutions(endpoint):
    """ Get all solutions of a question that has many solutions. """
    response = endpoint.get(f"{API}/q2/solutions")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 2
    assert isinstance(data, list)
    for d in data:
        s = Solution(**d)
        assert s.code == "print(\"hello world\")"

@pytest.mark.asyncio
async def test_get_q_has_no_solutions(endpoint):
    """ Get all solutions of a question that has no solutions. """
    response = endpoint.get(f"{API}/q3/solutions")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 0

@pytest.mark.asyncio
async def test_get_solution_question_doesnt_exist(endpoint):
    """ Get all solutions of a question that doesn't exist. """
    response = endpoint.get(f"{API}/question_dne/solutions")
    assert response.status_code == 404


# # Creating questions
# @pytest.mark.asyncio
# async def test_create_question_basic(endpoint):
#     """ Test creating a question with basic inputs. """
#     question = {
#         "source": "leetcode",
#         "link": "",
#         "status": "completed",
#         "title": "Create Question Basic",
#         "prompt": "create a basic question",
#         "test_cases": [],
#         "notes": [],
#         "hints": [],
#         "tags": []
#     }

#     response = endpoint.post(f"{API}", json=question)
#     assert response.status_code == 200
#     assert isinstance(response.text, str)


# @pytest.mark.asyncio
# async def test_create_question_invalid_input(endpoint):
#     """ Test creating a question with invalid input values. """
#     question = {
#         "source": "l",
#         "link": "",
#         "status": "",
#         "title": "Create Question Basic",
#         "prompt": "create a basic question",
#         "test_cases": [],
#         "notes": [],
#         "hints": [],
#         "tags": []
#     }

#     response = endpoint.post(f"{API}", json=question)
#     assert response.status_code == 422


# @pytest.mark.asyncio
# async def test_create_question_missing_fields(endpoint):
#     """ Test creating a question with missing fields. """
#     question = {
#         "link": "",
#         "status": "",
#         "title": "Create Question Basic",
#         "test_cases": [],
#         "hints": [],
#         "tags": []
#     }

#     response = endpoint.post(f"{API}", json=question)
#     assert response.status_code == 422


# # Updating questions
# @pytest.mark.asyncio
# async def test_update_question_basic(endpoint):
#     """ Test updating a question with basic update values. """
#     title = "Updated title"
#     prompt = "Updated prompt"
#     tags = ["graph", "queue"]
#     update_data = {"title": title, "prompt": prompt, "tags": tags}

#     response = endpoint.put(f"{API}/q1", json=update_data)
#     assert response.status_code == 200


# @pytest.mark.asyncio
# async def test_update_question_invalid_data(endpoint):
#     """ Test updating a question but the data is invalid. """
#     source = "aslkdjf"
#     update_data = {"source": source}

#     response = endpoint.put(f"{API}/q1", json=update_data)
#     assert response.status_code == 422


# @pytest.mark.asyncio
# async def test_update_question_invalid_field(endpoint):
#     """ Test updating a question but the field is invalid. """
#     invalid = "invalid"
#     update_data = {"invalid": invalid}

#     response = endpoint.put(f"{API}/q1", json=update_data)
#     assert response.status_code == 422


# # Delete questions
# @pytest.mark.asyncio
# async def test_update_question_exists(endpoint):
#     """ Test deleting a question that exists in the database. """
#     response = endpoint.delete(f"{API}/delete_endpoint")
#     assert response.status_code == 200


# @pytest.mark.asyncio
# async def test_update_question_doesnt_exist(endpoint):
#     """ Test deleting a question that doesn't exist in the database. """
#     response = endpoint.delete(f"{API}/delete_dne")
#     assert response.status_code == 200
