"""empty message

Revision ID: 1eaffac078cf
Revises: 6e6f04e85671
Create Date: 2017-03-07 11:37:38.910000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '1eaffac078cf'
down_revision = '6e6f04e85671'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_unique_constraint('_title_tenant', 'indicator', ['title', 'tenant_uuid'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('_title_tenant', 'indicator', type_='unique')
    # ### end Alembic commands ###
