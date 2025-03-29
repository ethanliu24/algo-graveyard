import pytest

from app.schemas.question import Question

@pytest.mark.asyncio
async def test_get_all_questions(endpoint):
    response = endpoint.get("/api/questions")
    assert response.status_code == 200
    data = response.json()
    assert len(data) > 0
    assert isinstance(data, list)
    for d in data:
        Question(**d)  # validate
