"""init

Revision ID: d8625cd7a2ed
Revises: 1f3a353e7170
Create Date: 2019-08-27 01:53:16.113762

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import mysql

# revision identifiers, used by Alembic.
revision = 'd8625cd7a2ed'
down_revision = '1f3a353e7170'
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index('fk_answer_request_id_request', table_name='answer')
    op.drop_column('answer', 'request_id')
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('answer', sa.Column('request_id', mysql.INTEGER(display_width=11), autoincrement=False, nullable=True))
    op.create_index('fk_answer_request_id_request', 'answer', ['request_id'], unique=False)
    # ### end Alembic commands ###
