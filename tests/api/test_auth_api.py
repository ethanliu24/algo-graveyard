from app.env_vars import ENV_VARS
from tests.utils import set_jwt_cookie

API = "api/auth"
APP_SECRET = ENV_VARS.get("APP_SECRET")
JWT_COOKIE = ENV_VARS.get("JWT_COOKIE")

def test_verify_correct_secret(endpoint):
    endpoint.cookies.clear()
    payload = {"secret": APP_SECRET}
    response = endpoint.post(API, json=payload)

    # check cookie and update to header
    set_jwt_cookie(endpoint, response)
    set_cookie_header = response.headers.get("set-cookie")
    cookie_values = set_cookie_header.split(";")
    assert len(cookie_values) > 0
    assert "HttpOnly" in set_cookie_header
    assert "Secure" in set_cookie_header
    assert endpoint.cookies.get(JWT_COOKIE)
    for val in cookie_values:
        res = val.split("=")
        if res[0] == " Max-Age": assert res[1] == str(float(ENV_VARS.get("JWT_EXP_TIME")) * 60 * 60)
        elif res[0] == " Path": assert res[1] == "/"
        elif res[0] == " SameSite": assert res[1] == "strict"

    assert response.status_code == 200


def test_verify_incorrect_secret(endpoint):
    endpoint.cookies.clear()
    payload = {"secret": APP_SECRET + "INCORRECT"}
    response = endpoint.post(API, json=payload)
    assert response.status_code == 401
    assert not endpoint.cookies.get(JWT_COOKIE)
    assert not response.headers.get("set-cookie")


def test_public_routes(endpoint):
    """ These routes shuold still be accessible even when not authed. """
    endpoint.cookies.clear()
    response = endpoint.get("api/questions")
    assert response.status_code == 200
