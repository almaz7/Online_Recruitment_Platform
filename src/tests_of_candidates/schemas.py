from datetime import datetime

from pydantic import BaseModel


class Test_Candidate_Create(BaseModel):
    result_type: str
    result: int

class Test_Candidate_Get(BaseModel):
    id: int
    user_id: int
    result_type: str
    date: datetime
    result: int