import jwt
import time

from fastapi import Request, HTTPException, status
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
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


class JWTBearer(HTTPBearer):
    auth_service: AuthManager

    def __init__(self, auth_service: AuthManager, auto_error = True):
        super().__init__(auto_error=auto_error)
        self.auth_service = auth_service

    def __call__(self, request: Request):
        err_msg = ""

        cred: HTTPAuthorizationCredentials = super().__call__(request)
        if not cred:
            err_msg = "Invalid authorization code."
        else:
            try:
                if cred.scheme != "Bearer":
                    err_msg = "Invalid authentication scheme"
                elif not self.auth_service.verify_token(cred.credentials):
                    err_msg = "Invalid token."
                else:
                    return cred.credentials
            except PyJWTError as e:
                err_msg = str(e)

        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=str(err_msg))
