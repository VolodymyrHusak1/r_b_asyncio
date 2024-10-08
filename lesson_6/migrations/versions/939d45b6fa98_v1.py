"""v1

Revision ID: 939d45b6fa98
Revises: 9fbc79691571
Create Date: 2024-09-02 19:14:31.808566

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '939d45b6fa98'
down_revision: Union[str, None] = '9fbc79691571'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('cve_record_data',
    sa.Column('id', sa.UUID(), server_default=sa.text('gen_random_uuid()'), nullable=False),
    sa.Column('date_published', sa.DateTime(), nullable=False),
    sa.Column('date_updated', sa.DateTime(), nullable=False),
    sa.Column('descriptions', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.add_column('cve_record', sa.Column('cve_id', sa.String(length=5), nullable=False))
    op.add_column('cve_record', sa.Column('title', sa.String(length=50), nullable=False))
    op.drop_column('cve_record', 'data_version')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cve_record', sa.Column('data_version', sa.VARCHAR(length=5), autoincrement=False, nullable=False))
    op.drop_column('cve_record', 'title')
    op.drop_column('cve_record', 'cve_id')
    op.drop_table('cve_record_data')
    # ### end Alembic commands ###
