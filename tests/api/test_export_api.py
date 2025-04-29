import json
import pytest

API = "/api/export"

@pytest.mark.asyncio
async def test_export_basic(endpoint):
    body = { "solution_ids": ["s1", "s2"] }
    response = endpoint.post(f"{API}/q2", content=json.dumps(body))
    assert response.status_code == 200
    assert response.headers["Content-Type"] == "application/pdf"
    assert "Content-Disposition" in response.headers
    assert "attachment; filename=q2.pdf" in response.headers["Content-Disposition"]
    assert response.content.startswith(b"%PDF")
    assert len(response.content) > 0


@pytest.mark.asyncio
@pytest.mark.skip(reason="Need PDF parsing probably")
async def test_export_all_solutions(endpoint):
    pass


@pytest.mark.asyncio
@pytest.mark.skip(reason="Need PDF parsing probably")
async def test_export_partial_solutions(endpoint):
    pass


@pytest.mark.asyncio
@pytest.mark.skip(reason="Need PDF parsing probably")
async def test_export_no_solutions(endpoint):
    pass


@pytest.mark.asyncio
async def test_export_invalid_body(endpoint):
    body = { "solutions": ["s1", "s2"] }
    response = endpoint.post(f"{API}/q2", content=json.dumps(body))
    assert response.status_code == 400

    body = { "solution_ids": 1 }
    response = endpoint.post(f"{API}/q2", content=json.dumps(body))
    assert response.status_code == 400

    body = { "solution_ids": ["s1", 1] }
    response = endpoint.post(f"{API}/q2", content=json.dumps(body))
    assert response.status_code == 400


@pytest.mark.asyncio
async def test_export_question_dne(endpoint):
    body = { "solutions": ["s1", "s2"] }
    response = endpoint.post(f"{API}/question_dne", content=json.dumps(body))
    assert response.status_code == 404
