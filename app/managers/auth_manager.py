import jwt
import time

from jwt import PyJWTError
from ..schemas.token import Token

class AuthManager:
    # These should never be changed
    app_secret: str
    jwt_secret: str
    hs_alg: str
    exp_time: int  # in hours
    iss: str
    aud: str

    def __init__(self, app_secret: str, jwt_secret: str, hs_alg: str, exp_time: int, iss: str, aud: str):
        self.app_secret = app_secret
        self.jwt_secret = jwt_secret
        self.hs_alg = hs_alg
        self.exp_time = exp_time
        self.iss = iss
        self.aud = aud

    def verify_secret(self, secret: str) -> bool:
        """ Verifies input with the app secret. Returns whether verification is successful. """
        return secret == self.app_secret

    def generate_token(self) -> str:
        payload = {
            "iss": self.iss,
            "aud": self.aud,
            "exp": time.time() + (self.exp_time * 60)
        }

        _ = Token(**payload)  # don't think its needed, but why not, sanity check
        token = jwt.encode(payload, self.jwt_secret, algorithm=self.hs_alg)
        return token

    def verify_token(self, token: str) -> bool:
        # decode will verify all the claims in our token schema since they are must checks
        payload = jwt.decode(token, self.jwt_secret, algorithms=[self.hs_alg], audience=self.aud)
        _ = Token(**payload)  # sanity check
        return True


