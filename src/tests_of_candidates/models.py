from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, MetaData
from datetime import datetime
metadata = MetaData()

test_candidate = Table(
    "test_candidate",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("user_id", Integer, nullable=False),
    Column("result_type", String, nullable=False),
    Column("date", TIMESTAMP,  default=datetime.utcnow),
    Column("result", Integer, nullable=False),
)