"""rm_sip_json_fld

Revision ID: 3ec6447ec908
Revises: 3f379986def2
Create Date: 2018-12-30 22:28:47.091168

"""

# revision identifiers, used by Alembic.
revision = '3ec6447ec908'
down_revision = '3f379986def2'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('radio_station', 'sip_settings')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('radio_station', sa.Column('sip_settings', sa.TEXT(), nullable=True))
    ### end Alembic commands ###
