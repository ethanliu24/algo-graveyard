from .base_config import BaseModelConfig

class Token(BaseModelConfig):
    iss: str
    aud: str
    exp: float
