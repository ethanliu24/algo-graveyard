import jwt
import pytest
import time

from app.env_vars import ENV_VARS
from jwt.exceptions import (
    InvalidAudienceError,
    InvalidIssuerError,
    InvalidSignatureError,
    InvalidAlgorithmError,
    InvalidTokenError,
    ExpiredSignatureError
    )
from tests.utils import create_jwt_token


def test_valid_token():
    token = create_jwt_token()
    assert token != ""


def test_invalid_token(auth_service):
    token = "invalid"
    with pytest.raises(InvalidTokenError):
        auth_service.verify_token(token)


def test_expired_token(auth_service):
    token = create_jwt_token(exp=0.0000001)
    time.sleep(0.2)
    with pytest.raises(ExpiredSignatureError):
        auth_service.verify_token(token)


def test_incorrect_signiture(auth_service):
    token = create_jwt_token(jwt_secret="1234")
    with pytest.raises(InvalidSignatureError):
        auth_service.verify_token(token)


def test_incorrect_issueer(auth_service):
    token = create_jwt_token(iss="me lol")
    with pytest.raises(InvalidIssuerError):
        auth_service.verify_token(token)


def test_incorrect_audience(auth_service):
    token = create_jwt_token(aud="me lol")
    with pytest.raises(InvalidAudienceError):
        auth_service.verify_token(token)


def test_incorrect_token_payload(auth_service):
    token = jwt.encode({"invalid": "invalid"}, ENV_VARS.get("JWT_SIGNITURE"), algorithm=ENV_VARS.get("JWT_HS_ALGO"))
    with pytest.raises(InvalidTokenError):
        auth_service.verify_token(token)


def test_correct_app_secret(auth_service):
    assert auth_service.verify_secret(ENV_VARS.get("APP_SECRET"))


def test_correct_app_secret(auth_service):
    assert not auth_service.verify_secret(ENV_VARS.get("APP_SECRET") + "a")
