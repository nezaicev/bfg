"""init

Revision ID: 2335bed67247
Revises: a72b380bda4a
Create Date: 2019-09-25 02:54:23.190782

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2335bed67247'
down_revision = 'a72b380bda4a'
branch_labels = None
depends_on = None

def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('request', sa.Column('count', sa.Integer(), nullable=True))
    # ### end Alembic commands ###

def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('request', 'count')
    # ### end Alembic commands ###
