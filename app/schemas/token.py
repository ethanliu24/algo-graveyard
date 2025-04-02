from datetime import datetime
from .base_config import BaseModelConfig

class Token(BaseModelConfig):
    iss: str
    aud: str
    exp: datetime


class AuthenticateReq(BaseModelConfig):
    secret: str
