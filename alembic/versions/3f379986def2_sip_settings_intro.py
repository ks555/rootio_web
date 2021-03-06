"""sip_settings_intro

Revision ID: 3f379986def2
Revises: 1a24e052e5be
Create Date: 2018-12-30 20:23:46.321808

"""

# revision identifiers, used by Alembic.
revision = '3f379986def2'
down_revision = '1a24e052e5be'

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column('radio_station', sa.Column('call_volume', sa.Integer(), nullable=True))
    op.add_column('radio_station', sa.Column('sip_password', sa.String(length=100), nullable=True))
    op.add_column('radio_station', sa.Column('sip_port', sa.Integer(), nullable=True))
    op.add_column('radio_station', sa.Column('sip_protocol', sa.String(length=100), nullable=True))
    op.add_column('radio_station', sa.Column('sip_reregister_period', sa.Integer(), nullable=True))
    op.add_column('radio_station', sa.Column('sip_server', sa.String(length=100), nullable=True))
    op.add_column('radio_station', sa.Column('sip_stun_server', sa.String(length=100), nullable=True))
    op.add_column('radio_station', sa.Column('sip_username', sa.String(length=100), nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('radio_station', 'sip_username')
    op.drop_column('radio_station', 'sip_stun_server')
    op.drop_column('radio_station', 'sip_server')
    op.drop_column('radio_station', 'sip_reregister_period')
    op.drop_column('radio_station', 'sip_protocol')
    op.drop_column('radio_station', 'sip_port')
    op.drop_column('radio_station', 'sip_password')
    op.drop_column('radio_station', 'call_volume')
    ### end Alembic commands ###
