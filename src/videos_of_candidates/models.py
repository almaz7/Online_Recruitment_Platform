from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, MetaData
from datetime import datetime
metadata = MetaData()

video_candidate = Table(
    "video_candidate",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("question_id", Integer, nullable=False),
    Column("user_id", Integer, nullable=False),
    Column("path", String, nullable=False),
    Column("date", TIMESTAMP,  default=datetime.utcnow)
)