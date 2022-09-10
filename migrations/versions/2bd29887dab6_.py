"""empty message

Revision ID: 2bd29887dab6
Revises: 
Create Date: 2022-02-24 13:57:13.562117

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2bd29887dab6'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dbcomp',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('no_agr', sa.String(length=20), nullable=True),
    sa.Column('nama', sa.String(length=20), nullable=True),
    sa.Column('area_cg', sa.String(length=20), nullable=True),
    sa.Column('cg_name', sa.String(length=20), nullable=True),
    sa.Column('class_comp', sa.String(length=20), nullable=True),
    sa.Column('agent_notes', sa.Text(), nullable=True),
    sa.Column('input_date', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('no_agr')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dbcomp')
    # ### end Alembic commands ###