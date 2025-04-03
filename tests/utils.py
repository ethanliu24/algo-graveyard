import jwt
import time

from app.config import Configs
from app.env_vars import ENV_VARS
from app.main import app
from app.schemas.ai_analysis import AiAnalysis
from app.schemas.question import Question
from app.schemas.solution import Solution
from app.schemas.test_case import TestCase
from app.schemas.token import Token
from .seed import QUESTIONS

def create_jwt_token(
    iss: str = ENV_VARS.get("JWT_ISS"),
    aud: str = ENV_VARS.get("JWT_AUD"),
    exp: str = ENV_VARS.get("JWT_EXP_TIME"),
    enable_exp: bool = False,
    jwt_secret: str = ENV_VARS.get("JWT_SIGNITURE"),
    hs_alg: str = ENV_VARS.get("JWT_HS_ALG")
) -> str:
    payload = {
        "iss": iss,
        "aud": aud,
    }

    if enable_exp:
        payload.update({"exp": time.time() + (exp * 60)})
        
    _ = Token(**payload)
    return jwt.encode(payload, jwt_secret, algorithm=hs_alg)