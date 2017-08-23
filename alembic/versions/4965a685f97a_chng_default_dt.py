"""chng_default_dt

Revision ID: 4965a685f97a
Revises: 1d1e8683e144
Create Date: 2017-08-23 14:31:19.143634

"""

# revision identifiers, used by Alembic.
revision = '4965a685f97a'
down_revision = '1d1e8683e144'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.add_column(u'content_podcast', sa.Column('date_created', sa.DateTime(timezone=True), server_default='now()', nullable=True))
    op.alter_column(u'content_podcast', 'updated_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=True,
               existing_server_default="2017-01-11 21:14:53.469648+00'::timestamp with time zone")
    op.add_column(u'content_podcastdownload', sa.Column('date_downloaded', sa.DateTime(timezone=True), server_default='now()', nullable=True))
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_column(u'content_podcastdownload', 'date_downloaded')
    op.alter_column(u'content_podcast', 'updated_at',
               existing_type=postgresql.TIMESTAMP(timezone=True),
               nullable=False,
               existing_server_default="2017-01-11 21:14:53.469648+00'::timestamp with time zone")
    op.drop_column(u'content_podcast', 'date_created')
    ### end Alembic commands ###