import pytest

from app.schemas.solution import Solution

API = "/api/questions"

# Getting solutions
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


@pytest.mark.asyncio
async def test_get_single_solution_from_q_exists(endpoint):
    """ Get a specific solution of a question. """
    response = endpoint.get(f"{API}/q1/solutions/s1")
    assert response.status_code == 200
    data = response.json()
    s = Solution(**data)
    assert s.id == "s1"
    assert s.summary == "Test"
    assert s.explanation == "test"


@pytest.mark.asyncio
async def test_get_single_solution_from_q_dne(endpoint):
    """ Get a specific solution of a question but it doesn't exist in db. """
    response = endpoint.get(f"{API}/q1/solutions/solution_dne")
    assert response.status_code == 404


# Creating solutions
@pytest.mark.asyncio
async def test_create_solution_basic(endpoint):
    """ Test creating a solution with basic inputs. """
    solution = {
        "summary": "Created",
        "explanation": "created in test_create_solution_basic",
        "language": "python",
        "time_complexity": "n!",
        "space_complexity": "n!",
        "code": "",
        "accepted": True
    }

    response = endpoint.post(f"{API}/modify/solutions", json=solution)
    assert response.status_code == 200
    data = response.json()
    s = Solution(**data)
    assert s.summary == "Created"
    assert s.time_complexity == "n!"


@pytest.mark.asyncio
async def test_create_solution_q_dne(endpoint):
    """ Test creating a solution but the question doesn't exist. """
    solution = {
        "summary": "Created",
        "explanation": "created in test_create_solution_basic",
        "language": "python",
        "time_complexity": "n!",
        "space_complexity": "n!",
        "code": "",
        "accepted": False
    }

    response = endpoint.post(f"{API}/question_dne/solutions", json=solution)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_create_solution_invalid_input(endpoint):
    """ Test creating a question with invalid input values. """
    solution = {
        "summary": "Created",
        "explanation": "created in test_create_solution_basic",
        "language": "n",
        "time_complexity": "n!",
        "space_complexity": "n!",
        "code": "",
    }

    response = endpoint.post(f"{API}/modify/solutions", json=solution)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_solution_missing_fields(endpoint):
    """ Test creating a question with missing fields. """
    solution = {
        "explanation": "created in test_create_solution_basic",
        "time_complexity": "n!",
        "code": "",
    }

    response = endpoint.post(f"{API}/modify/solutions", json=solution)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_create_question_validate_summary(endpoint):
    """ Test prompt validation. """
    solution = {
        "summary": "Valid suammary",
        "explanation": "created in test_create_solution_basic",
        "language": "python",
        "time_complexity": "n!",
        "space_complexity": "n!",
        "code": "",
        "accepted": True
    }

    solution["summary"] = ""
    response = endpoint.post(f"{API}/modify/solutions", json=solution)
    assert response.status_code == 422

    solution["summary"] = "a" * 51
    response = endpoint.post(f"{API}/modify/solutions", json=solution)
    assert response.status_code == 422

    solution["summary"] = "a" * 50  # upperbound
    response = endpoint.post(f"{API}/modify/solutions", json=solution)
    assert response.status_code == 200


# Updating solutions
@pytest.mark.asyncio
async def test_update_solution(endpoint):
    """ Test updating a solution with different fields being updated. """
    summary = "Updated title"
    explanation = "Updated explaination"
    language = "python"
    time_complexity = "1"
    space_complexity = "1"
    code = "print()"
    update_data = {
        "summary": summary,
        "explanation": explanation,
        "language": language,
        "time_complexity": time_complexity,
        "space_complexity": space_complexity,
        "code": code,
    }

    response = endpoint.put(f"{API}/modify/solutions/s1", json=update_data)
    assert response.status_code == 200
    s = Solution(**response.json())
    assert s.summary == summary
    assert s.explanation == explanation
    assert s.language.value == language
    assert s.time_complexity == time_complexity
    assert s.space_complexity == space_complexity
    assert s.code == code


@pytest.mark.asyncio
async def test_update_solution_invalid_data(endpoint):
    """ Test updating a solution but the data is invalid. """
    language = "asdfasd"
    update_data = {"language": language}

    response = endpoint.put(f"{API}/modify/solutions/s1", json=update_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_solution_invalid_field(endpoint):
    """ Test updating a solution but the field is invalid. """
    invalid = "invalid"
    update_data = {"invalid": invalid}

    response = endpoint.put(f"{API}/modify/solutions/s1", json=update_data)
    assert response.status_code == 422


@pytest.mark.asyncio
async def test_update_solution_question_dne(endpoint):
    """ Test updating a solution but the question id doesn't exist. """
    update_data = {"language": "python"}
    response = endpoint.put(f"{API}/question_dne/solutions/s1", json=update_data)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_solution_solution_dne(endpoint):
    """ Test updating a solution but the solution id doesn't exist. """
    update_data = {"language": "python"}
    response = endpoint.put(f"{API}/modify/solutions/solution_dne", json=update_data)
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_solution_both_id_dne(endpoint):
    """ Test updating a solution but both ids doesn't exist. """
    update_data = {"language": "python"}
    response = endpoint.put(f"{API}/question_dne/solutions/solution_dne", json=update_data)
    assert response.status_code == 404


# Delete solutions
@pytest.mark.asyncio
async def test_update_solution_exists(endpoint):
    """ Test deleting a solution that exists in the database. """
    response = endpoint.delete(f"{API}/modify/solutions/s2")
    assert response.status_code == 200


@pytest.mark.asyncio
async def test_update_solution_doesnt_exist(endpoint):
    """ Test deleting a solution that doesn't exist in the database. """
    response = endpoint.delete(f"{API}/modify/solutions/solution_dne")
    assert response.status_code == 404


@pytest.mark.asyncio
async def test_update_solution_question_doesnt_exist(endpoint):
    """ Test deleting a solution but the question id doesn't exist in the database. """
    response = endpoint.delete(f"{API}/question_dne/solutions/solution_dne")
    assert response.status_code == 404
