"""empty message

Revision ID: 930a9dca5322
Revises: 26365d5905f3
Create Date: 2017-02-24 12:33:15.110000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '930a9dca5322'
down_revision = '26365d5905f3'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(u'responsibilityAssignment_responsibilityObject_id_fkey', 'responsibilityAssignment', type_='foreignkey')
    op.create_foreign_key(None, 'responsibilityAssignment', 'responsibilityObject', ['responsibilityObject_id'], ['id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'responsibilityAssignment', type_='foreignkey')
    op.create_foreign_key(u'responsibilityAssignment_responsibilityObject_id_fkey', 'responsibilityAssignment', 'region', ['responsibilityObject_id'], ['id'])
    # ### end Alembic commands ###