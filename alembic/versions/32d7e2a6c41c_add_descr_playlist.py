"""add_descr_playlist

Revision ID: 32d7e2a6c41c
Revises: 3f5410820abe
Create Date: 2016-11-25 17:14:39.648507

"""

# revision identifiers, used by Alembic.
revision = '32d7e2a6c41c'
down_revision = '3f5410820abe'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('content_musicplaylist', sa.Column('description', sa.Text(), nullable=True))
    op.drop_column('content_musicplaylistitemtype', 'description')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('content_musicplaylistitemtype', sa.Column('description', sa.TEXT(), nullable=True))
    op.drop_column('content_musicplaylist', 'description')
    ### end Alembic commands ###