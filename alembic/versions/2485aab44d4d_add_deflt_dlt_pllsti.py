"""add_deflt_dlt_pllstitm

Revision ID: 2485aab44d4d
Revises: 309c2255ee7d
Create Date: 2016-11-29 18:51:18.844580

"""

# revision identifiers, used by Alembic.
revision = '2485aab44d4d'
down_revision = '309c2255ee7d'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('content_musicplaylistitem', 'deleted')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('content_musicplaylistitem', sa.Column('deleted', sa.BOOLEAN(), nullable=True))
    ### end Alembic commands ###
