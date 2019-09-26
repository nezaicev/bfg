"""init

Revision ID: 4b29e394b6f6
Revises: e2cb0eaabf46
Create Date: 2019-08-26 15:38:58.159953

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b29e394b6f6'
down_revision = 'e2cb0eaabf46'
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('fk_answer_request_id_request', 'answer', type_='foreignkey')
    op.create_foreign_key(op.f('fk_answer_request_id_request'), 'answer', 'request', ['request_id'], ['id'], onupdate='cascade')
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('fk_answer_request_id_request'), 'answer', type_='foreignkey')
    op.create_foreign_key('fk_answer_request_id_request', 'answer', 'request', ['request_id'], ['id'])
    # ### end Alembic commands ###
