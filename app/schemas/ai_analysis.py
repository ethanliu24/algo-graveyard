from pydantic import BaseModel

class AiAnalysis(BaseModel):
    # big O only for complexity for now
    time_complexity: str
    space_complexity: str
    feedback: str
