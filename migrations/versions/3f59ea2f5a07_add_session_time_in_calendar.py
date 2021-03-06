"""add session time in calendar

Revision ID: 3f59ea2f5a07
Revises: 71b9b4083f1a
Create Date: 2020-07-09 23:59:16.773717

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3f59ea2f5a07'
down_revision = '71b9b4083f1a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('calendar', sa.Column('event_time', sa.Time(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('calendar', 'event_time')
    # ### end Alembic commands ###
