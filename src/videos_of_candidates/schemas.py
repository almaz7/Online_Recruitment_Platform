from datetime import datetime

from pydantic import BaseModel


class Video_Candidate_Create(BaseModel):
    # user_id: int
    question_id: int
    # path: str


class Video_Candidate_Get(BaseModel):
    id: int
    user_id: int
    question_id: int
    path: str
    date: datetime