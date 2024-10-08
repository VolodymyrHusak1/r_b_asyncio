"""v2

Revision ID: bf01c6329d69
Revises: 939d45b6fa98
Create Date: 2024-09-02 19:44:46.196195

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bf01c6329d69'
down_revision: Union[str, None] = '939d45b6fa98'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cve_record_data', sa.Column('cve_id', sa.UUID(), nullable=False))
    op.create_foreign_key(None, 'cve_record_data', 'cve_record', ['cve_id'], ['id'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'cve_record_data', type_='foreignkey')
    op.drop_column('cve_record_data', 'cve_id')
    # ### end Alembic commands ###
