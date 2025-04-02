import jwt
from jwt import ExpiredSignatureError, InvalidTokenError
from ..schemas.token import Token

class AuthManager:
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
        pass

    def generate_token(self) -> str:
        pass

    def verify_token(self, token: str) -> bool:
        # decode & verify claims. assume everything is valid, smth else will handle the errs
        pass

