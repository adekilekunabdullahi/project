"""empty message

Revision ID: a5d9d71b2b44
Revises: e94b1d254b8f
Create Date: 2022-08-20 10:37:42.307438

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'a5d9d71b2b44'
down_revision = 'e94b1d254b8f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('Artist', 'past_shows')
    op.drop_column('Artist', 'past_shows_count')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Artist', sa.Column('past_shows_count', sa.INTEGER(), autoincrement=False, nullable=True))
    op.add_column('Artist', sa.Column('past_shows', sa.VARCHAR(), autoincrement=False, nullable=True))
    # ### end Alembic commands ###