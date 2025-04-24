import json

from app.env_vars import ENV_VARS
from tests.utils import set_jwt_cookie

API = "api/auth"
APP_SECRET = ENV_VARS.get("APP_SECRET")
JWT_COOKIE = ENV_VARS.get("JWT_COOKIE")

Q_JSON = {
    "source": "leetcode",
    "link": "",
    "difficulty": "easy",
    "status": "completed",
    "title": "Test authentication authorization",
    "prompt": "Test authentication authorization",
    "notes": [],
    "hints": [],
    "tags": []
}

S_JSON = {
    "summary": "For auth flow",
    "explanation": "For auth flow",
    "language": "python",
    "time_complexity": "n!",
    "space_complexity": "n!",
    "code": "",
    "accepted": False,
    "question_title": "A",
    "question_prompt": "A"
}


def test_authenticated_flow(endpoint):
    endpoint.cookies.clear()
    auth_payload = {"secret": APP_SECRET}
    response = endpoint.post("/api/auth", json=auth_payload)
    set_jwt_cookie(endpoint, response)

    response = endpoint.post("/api/questions", content=json.dumps(Q_JSON))
    assert response.status_code == 200
    q_id = response.json()["id"]

    response = endpoint.post(f"api/questions/{q_id}/solutions", json=S_JSON)
    assert response.status_code == 200

    response = endpoint.post("/api/questions", content=json.dumps({}))
    assert response.status_code == 422

    response = endpoint.delete(f"api/questions/{q_id}")
    assert response.status_code == 200


def test_not_authenticated_then_authenticated(endpoint):
    endpoint.cookies.clear()

    response = endpoint.post("/api/questions", json=Q_JSON)
    assert response.status_code == 401 or response.status_code == 403

    auth_payload = {"secret": APP_SECRET}
    response = endpoint.post("/api/auth", json=auth_payload)
    set_jwt_cookie(endpoint, response)

    response = endpoint.post("/api/questions", json=Q_JSON)
    assert response.status_code == 200
