"""test_answer changed

Revision ID: dd0200c101ed
Revises: c451f5e08d54
Create Date: 2024-01-05 18:46:14.998472

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'dd0200c101ed'
down_revision: Union[str, None] = 'c451f5e08d54'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('test_answer', sa.Column('answer_num', sa.Integer(), nullable=False))
    op.add_column('test_answer', sa.Column('question_id', sa.Integer(), nullable=False))
    op.add_column('test_answer', sa.Column('answer', sa.String(), nullable=False))
    op.create_foreign_key(None, 'test_answer', 'test_question', ['question_id'], ['id'])
    op.drop_column('test_answer', 'question')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('test_answer', sa.Column('question', sa.VARCHAR(), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'test_answer', type_='foreignkey')
    op.drop_column('test_answer', 'answer')
    op.drop_column('test_answer', 'question_id')
    op.drop_column('test_answer', 'answer_num')
    # ### end Alembic commands ###