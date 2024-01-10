from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, MetaData, ForeignKey
from datetime import datetime
from auth.models import User
metadata = MetaData()

video_candidate = Table(
    "video_candidate",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("question_id", Integer, nullable=False),
    Column("user_id", Integer, ForeignKey(User.id), nullable=False),
    Column("path", String, nullable=False),
    Column("date", TIMESTAMP,  default=datetime.utcnow)
)