"""empty message

Revision ID: 6d76ba6bedea
Revises: 6255224a2846
Create Date: 2017-03-07 10:12:57.955000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '6d76ba6bedea'
down_revision = '6255224a2846'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chartContainer', sa.Column('containerSize_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'chartContainer', 'containerSize', ['containerSize_id'], ['id'])
    op.drop_column('chartContainer', 'startsize')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('chartContainer', sa.Column('startsize', sa.VARCHAR(), autoincrement=False, nullable=True))
    op.drop_constraint(None, 'chartContainer', type_='foreignkey')
    op.drop_column('chartContainer', 'containerSize_id')
    # ### end Alembic commands ###