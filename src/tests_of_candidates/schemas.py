from datetime import datetime

from pydantic import BaseModel


class Test_Result_Create(BaseModel):
    test_id: int
    result: int

class Test_Result_Get(BaseModel):
    id: int
    test_id: int
    user_id: int
    date: datetime
    result: int