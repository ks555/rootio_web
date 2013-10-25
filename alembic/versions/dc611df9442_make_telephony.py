"""make telephony_phonenumber raw_number nullable True

Revision ID: initial
Revises: 57f461d001ec
Create Date: 2013-10-25 18:15:47.156128

"""

# revision identifiers, used by Alembic.
revision = 'initial'
down_revision = '57f461d001ec'

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.alter_column("telephony_phonenumber", "raw_number", nullable=True)


def downgrade():
    op.alter_column("telephony_phonenumber", "raw_number", nullable=False)
