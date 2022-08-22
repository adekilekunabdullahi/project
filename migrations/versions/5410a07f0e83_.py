"""empty message

Revision ID: 5410a07f0e83
Revises: 5d8b60bb53f7
Create Date: 2022-08-19 14:50:27.799772

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5410a07f0e83'
down_revision = '5d8b60bb53f7'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Show', sa.Column('artist_id', sa.Integer(), nullable=False))
    op.drop_constraint('Show_Venue_id_fkey', 'Show', type_='foreignkey')
    op.drop_constraint('Show_Artist_id_fkey', 'Show', type_='foreignkey')
    op.create_foreign_key(None, 'Show', 'Artist', ['artist_id'], ['id'])
    op.drop_column('Show', 'Venue_id')
    op.drop_column('Show', 'Artist_name')
    op.drop_column('Show', 'Artist_id')
    op.drop_column('Show', 'Artist_image_link')
    op.drop_column('Show', 'Venue_name')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Show', sa.Column('Venue_name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('Show', sa.Column('Artist_image_link', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('Show', sa.Column('Artist_id', sa.INTEGER(), autoincrement=False, nullable=False))
    op.add_column('Show', sa.Column('Artist_name', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.add_column('Show', sa.Column('Venue_id', sa.INTEGER(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'Show', type_='foreignkey')
    op.create_foreign_key('Show_Artist_id_fkey', 'Show', 'Artist', ['Artist_id'], ['id'])
    op.create_foreign_key('Show_Venue_id_fkey', 'Show', 'Venue', ['Venue_id'], ['id'])
    op.drop_column('Show', 'artist_id')
    # ### end Alembic commands ###