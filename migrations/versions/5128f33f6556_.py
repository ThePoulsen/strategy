"""empty message

Revision ID: 5128f33f6556
Revises:
Create Date: 2017-02-23 11:52:51.224000

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '5128f33f6556'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('UOM',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('abbr', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title'),
    sa.UniqueConstraint('title', 'abbr', name='_title_abbr')
    )
    op.create_table('actionStatus',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('goodPerformance',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('desc', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('indicatorType',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('desc', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('language',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('locale', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('measurementFrequency',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('month',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('no', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('abbr', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('abbr'),
    sa.UniqueConstraint('no'),
    sa.UniqueConstraint('title')
    )
    op.create_table('processType',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('desc', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('quarter',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('no', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('no'),
    sa.UniqueConstraint('title')
    )
    op.create_table('region',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('code', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('responsibilityObject',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('responsibilityType',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('strategyLevel',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('taskStatus',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title')
    )
    op.create_table('weekDay',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('no', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('abbr', sa.String(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('abbr'),
    sa.UniqueConstraint('no'),
    sa.UniqueConstraint('title')
    )
    op.create_table('calendar',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('date', sa.Date(), nullable=True),
    sa.Column('weekNumber', sa.Integer(), nullable=True),
    sa.Column('year', sa.Integer(), nullable=True),
    sa.Column('weekDay_id', sa.Integer(), nullable=True),
    sa.Column('month_id', sa.Integer(), nullable=True),
    sa.Column('quarter_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['month_id'], ['month.id'], ),
    sa.ForeignKeyConstraint(['quarter_id'], ['quarter.id'], ),
    sa.ForeignKeyConstraint(['weekDay_id'], ['weekDay.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('date')
    )
    op.create_table('indicator',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('uuid', sa.String(), nullable=True),
    sa.Column('title', sa.String(), nullable=True),
    sa.Column('desc', sa.String(), nullable=True),
    sa.Column('dataSource', sa.String(), nullable=True),
    sa.Column('tenant_uuid', sa.String(), nullable=True),
    sa.Column('measurementFrequency_id', sa.Integer(), nullable=True),
    sa.Column('UOM_id', sa.Integer(), nullable=True),
    sa.Column('processType_id', sa.Integer(), nullable=True),
    sa.Column('indicatorType_id', sa.Integer(), nullable=True),
    sa.Column('goodPerformance_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['UOM_id'], ['UOM.id'], ),
    sa.ForeignKeyConstraint(['goodPerformance_id'], ['goodPerformance.id'], ),
    sa.ForeignKeyConstraint(['indicatorType_id'], ['indicatorType.id'], ),
    sa.ForeignKeyConstraint(['measurementFrequency_id'], ['measurementFrequency.id'], ),
    sa.ForeignKeyConstraint(['processType_id'], ['processType.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('title'),
    sa.UniqueConstraint('uuid')
    )
    op.create_table('responsibilityAssignment',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('responsibilityObject_id', sa.Integer(), nullable=True),
    sa.Column('reference_id', sa.Integer(), nullable=True),
    sa.Column('responsibilityType_id', sa.Integer(), nullable=True),
    sa.Column('user_uuid', sa.String(), nullable=True),
    sa.ForeignKeyConstraint(['responsibilityObject_id'], ['region.id'], ),
    sa.ForeignKeyConstraint(['responsibilityType_id'], ['responsibilityType.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('responsibilityObject_id', 'reference_id', 'responsibilityType_id', 'user_uuid')
    )
    op.create_table('subRegion',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('code', sa.Integer(), nullable=True),
    sa.Column('region_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['region_id'], ['region.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.create_table('country',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=True),
    sa.Column('alpha2', sa.String(), nullable=True),
    sa.Column('alpha3', sa.String(), nullable=True),
    sa.Column('code', sa.Integer(), nullable=True),
    sa.Column('subRegion_id', sa.Integer(), nullable=True),
    sa.Column('language_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['language_id'], ['language.id'], ),
    sa.ForeignKeyConstraint(['subRegion_id'], ['subRegion.id'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('country')
    op.drop_table('subRegion')
    op.drop_table('responsibilityAssignment')
    op.drop_table('indicator')
    op.drop_table('calendar')
    op.drop_table('weekDay')
    op.drop_table('taskStatus')
    op.drop_table('strategyLevel')
    op.drop_table('responsibilityType')
    op.drop_table('responsibilityObject')
    op.drop_table('region')
    op.drop_table('quarter')
    op.drop_table('processType')
    op.drop_table('month')
    op.drop_table('measurementFrequency')
    op.drop_table('language')
    op.drop_table('indicatorType')
    op.drop_table('goodPerformance')
    op.drop_table('actionStatus')
    op.drop_table('UOM')
    # ### end Alembic commands ###
