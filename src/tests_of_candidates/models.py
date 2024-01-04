from sqlalchemy import Table, Column, Integer, String, TIMESTAMP, MetaData, ForeignKey
from datetime import datetime
metadata = MetaData()

from auth.models import User
test = Table(
    "test",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("test_name", String, nullable=False)
)

test_question = Table(
    "test_question",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("test_id", Integer, ForeignKey(User.id), nullable=False),
    Column("question", String, nullable=False),
)

test_answer = Table(
    "test_answer",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("test_id", Integer, ForeignKey("test.id"), nullable=False),
    Column("user_id", Integer, ForeignKey(User.id), nullable=False),
    Column("date", TIMESTAMP,  default=datetime.utcnow),
    Column("question", String, nullable=False),
)

test_result = Table(
    "test_result",
    metadata,
    Column("id", Integer, primary_key=True, autoincrement=True),
    Column("test_id", Integer, ForeignKey("test.id"), nullable=False),
    Column("user_id", Integer, ForeignKey(User.id), nullable=False),
    Column("date", TIMESTAMP,  default=datetime.utcnow),
    Column("result", Integer, nullable=False),
)