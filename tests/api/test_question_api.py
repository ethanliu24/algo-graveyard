import pytest

from app.schemas.question import Question, QuestionBasicInfo, Difficulty
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


# TODO add a per page pagination queries
# Paginate
@pytest.mark.asyncio
async def test_pagination_query_all_pages(endpoint):
    """ Test pagination and query all pages. """
    response = endpoint.get(f"{API}")
    assert response.status_code == 200
    pagination = response.json()["data"]

    last_page = 1
    last_res = pagination["data"]
    while last_page < pagination["pages"]:
        response = endpoint.get(f"{API}?page={last_page}")
        pagination = response.json()["data"]
        assert last_page == pagination["page"] - 1
        assert last_res != pagination["data"]
        last_page += 1


@pytest.mark.asyncio
async def test_pagination_last_page(endpoint):
    """ Test pagination if requested beyond the total page size. """
    response = endpoint.get(f"{API}")
    total_pages = response.json()["data"]["page"]
    res1 = endpoint.get(f"{API}?page={total_pages}").json()["data"]["data"]
    res2 = endpoint.get(f"{API}?page={total_pages + 100}").json()["data"]["data"]
    assert res1 == res2


@pytest.mark.asyncio
async def test_pagination_one_per_page(endpoint):
    """ Test pagination quering one per page. """
    response = endpoint.get(f"{API}")
    assert response.status_code == 200
    pagination = response.json()["data"]

    total_pages = pagination["pages"]
    last_page = 1
    last_res = pagination["data"]
    while last_page < pagination["pages"]:
        response = endpoint.get(f"{API}?page={last_page}&per_page=1")
        pagination = response.json()["data"]
        assert pagination["per_page"] == 1
        assert last_page == pagination["page"] - 1
        assert last_res != pagination["data"]
        last_page += 1
    assert last_page == total_pages


@pytest.mark.asyncio
async def test_pagination_no_results(endpoint):
    """ Test pagination but no results are returned in the query. """
    response = endpoint.get(f"{API}?search=no_pagination_results")
    assert response.status_code == 200
    pagination = response.json()["data"]
    assert pagination["data"] == []
    assert pagination["page"] == 1
    assert pagination["pages"] == 1
    assert pagination["total"] == 0


# Search
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
    """ Test with a space in the search value. """
    response = endpoint.get(f"{API}?search=Space%20Here")
    assert response.status_code == 200
    pagination = response.json()["data"]
    assert len(pagination["data"]) == 1


# Filter
@pytest.mark.asyncio
async def test_filtering_for_source(endpoint):
    """ Test filtering for source. """
    response = endpoint.get(f"{API}?search=paginate&source=leetcode")
    assert response.status_code == 200
    pagination = response.json()["data"]
    assert len(pagination["data"]) == 6

@pytest.mark.asyncio
async def test_filtering_for_difficulty(endpoint):
    """ Test filtering for difficulty. """
    response = endpoint.get(f"{API}?search=paginate&difficulty=hard")
    assert response.status_code == 200
    pagination = response.json()["data"]
    assert len(pagination["data"]) == 1

@pytest.mark.asyncio
async def test_filtering_for_status(endpoint):
    """ Test filtering for status. """
    response = endpoint.get(f"{API}?search=paginate&status=unoptimized")
    assert response.status_code == 200
    pagination = response.json()["data"]
    assert len(pagination["data"]) == 3

@pytest.mark.asyncio
async def test_filtering_for_tags(endpoint):
    """ Test filtering for status. """
    response = endpoint.get(f"{API}?search=paginate&tags=graph&tags=dfs")
    assert response.status_code == 200
    pagination = response.json()["data"]
    assert len(pagination["data"]) == 5

@pytest.mark.asyncio
async def test_filtering_without_search(endpoint):
    """ Test filtering without a search value. """
    response = endpoint.get(f"{API}?difficulty=easy")
    pagination = response.json()["data"]
    response = endpoint.get(f"{API}?paginate=false")  # get everything as a list
    questions = response.json()["data"]
    count = sum(1 for q in questions if q["difficulty"] == "easy")
    assert len(pagination["data"]) == count

@pytest.mark.asyncio
async def test_multiple_filters(endpoint):
    """ Test filtering with a combination of the filters. """
    response = endpoint.get(f"{API}?search=paginate&source=leetcode&difficulty=easy&status=completed&tags=graph")
    pagination = response.json()["data"]
    assert response.status_code == 200
    pagination = response.json()["data"]
    assert len(pagination["data"]) == 1


# Sort and order
@pytest.mark.asyncio
async def test_sorting_by_created_at(endpoint):
    """ Test sorting by created at with both orders. """
    # check asc
    response = endpoint.get(f"{API}?search=paginate&sort_by=created_at&order=asc")
    assert response.status_code == 200
    questions = response.json()["data"]["data"]
    assert all([questions[i-1]["created_at"] <= questions[i]["created_at"] for i in range(1, len(questions))])

    # check desc
    response = endpoint.get(f"{API}?sort_by=created_at&order=desc")
    assert response.status_code == 200
    questions = response.json()["data"]["data"]
    assert all([questions[i-1]["created_at"] >= questions[i]["created_at"] for i in range(1, len(questions))])

@pytest.mark.asyncio
async def test_sorting_by_difficulty(endpoint):
    """ Test sorting by difficulty at with both orders. """
    prio = { Difficulty.EASY.value: 0, Difficulty.MEDIUM.value: 1, Difficulty.HARD.value: 2 }

    # check asc
    response = endpoint.get(f"{API}?sort_by=difficulty&order=asc")
    assert response.status_code == 200
    questions = response.json()["data"]["data"]
    assert all([prio[questions[i-1]["difficulty"]] <= prio[questions[i]["difficulty"]] for i in range(1, len(questions))])

    # check desc
    response = endpoint.get(f"{API}?search=paginate&sort_by=difficulty&order=desc")
    assert response.status_code == 200
    questions = response.json()["data"]["data"]
    assert all([prio[questions[i-1]["difficulty"]] >= prio[questions[i]["difficulty"]] for i in range(1, len(questions))])


@pytest.mark.asyncio
async def test_sorting_by_title(endpoint):
    """ Test sorting by title at with both orders. """
    # check asc
    response = endpoint.get(f"{API}?search=paginate&sort_by=title&order=asc")
    assert response.status_code == 200
    questions = response.json()["data"]["data"]
    assert all([questions[i-1]["title"] <= questions[i]["title"] for i in range(1, len(questions))])

    # check desc
    response = endpoint.get(f"{API}?sort_by=title&order=desc")
    assert response.status_code == 200
    questions = response.json()["data"]["data"]
    assert all([questions[i-1]["title"] >= questions[i]["title"] for i in range(1, len(questions))])


@pytest.mark.asyncio
async def test_sorting_invalid_query_param(endpoint):
    """ Test sorting but query params are invalid. """
    response = endpoint.get(f"{API}?sort_by=bad")
    assert response.status_code == 400

    response = endpoint.get(f"{API}?order=bad")
    assert response.status_code == 400

    response = endpoint.get(f"{API}?sort_by=created_at&order=bad")
    assert response.status_code == 400

    response = endpoint.get(f"{API}?sort_by=bad&order=asc")
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_sorting_default(endpoint):
    """ Test if return values are created date sorted in desc order. """
    # check asc
    response = endpoint.get(f"{API}?")
    assert response.status_code == 200
    questions = response.json()["data"]["data"]
    assert all([questions[i-1]["created_at"] >= questions[i]["created_at"] for i in range(1, len(questions))])
