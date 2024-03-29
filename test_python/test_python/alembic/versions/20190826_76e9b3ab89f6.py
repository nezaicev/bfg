"""init

Revision ID: 76e9b3ab89f6
Revises: 1880fd8e263b
Create Date: 2019-08-26 16:48:42.267747

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '76e9b3ab89f6'
down_revision = '1880fd8e263b'
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('fk_answer_request_id_request', 'answer', type_='foreignkey')
    op.create_foreign_key(op.f('fk_answer_request_id_request'), 'answer', 'request', ['request_id'], ['id'])
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(op.f('fk_answer_request_id_request'), 'answer', type_='foreignkey')
    op.create_foreign_key('fk_answer_request_id_request', 'answer', 'request', ['request_id'], ['id'], onupdate='CASCADE')
    # ### end Alembic commands ###
