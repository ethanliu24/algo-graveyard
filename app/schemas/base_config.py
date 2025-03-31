from pydantic import BaseModel, ConfigDict

""" Configuration class for Pydantic model to forbid any extra fields not defined in schema. """
class BaseModelConfig(BaseModel):
    model_config = ConfigDict(extra="forbid")
