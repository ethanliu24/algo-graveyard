import jwt
import time

from jwt import ExpiredSignatureError, InvalidTokenError
from ..schemas.token import Token

class AuthManager:
    # These should never be changed
    app_secret: str
    jwt_secret: str
    hs_alg: str
    exp_time: int  # in hours

    def __init__(self, app_secret: str, jwt_secret: str, hs_alg: str, exp_time: int):
        self.app_secret = app_secret
        self.jwt_secret = jwt_secret
        self.hs_alg = hs_alg
        self.exp_time = exp_time

    def verify_secret(self, secret: str) -> bool:
        """ Verifies input with the app secret. Returns whether verification is successful. """
        return secret == self.app_secret

    def generate_token(self) -> str:
        payload = {
            "iss": "algograveyard",
            "aud": "algograveyard",
            "exp": time.time() + (self.exp_time * 60)
        }

        token = jwt.encode(payload, self.jwt_secret, algorithm=self.hs_alg)
        return token

    def verify_token(self, token: str) -> bool:
        # decode & verify claims. assume everything is valid, smth else will handle the errs
        pass

