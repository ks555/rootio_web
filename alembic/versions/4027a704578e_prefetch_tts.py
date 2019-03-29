"""prefetch_tts

Revision ID: 4027a704578e
Revises: 31ff8f016d59
Create Date: 2019-03-29 16:15:17.114846

"""

# revision identifiers, used by Alembic.
revision = '4027a704578e'
down_revision = '31ff8f016d59'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('content_communitymenu', sa.Column('prefetch_tts', sa.Boolean(), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('content_communitymenu', 'prefetch_tts')
    ### end Alembic commands ###
