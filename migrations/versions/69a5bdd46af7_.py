"""empty message

Revision ID: 69a5bdd46af7
Revises: 2bbb83277553
Create Date: 2022-04-25 15:46:44.152677

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '69a5bdd46af7'
down_revision = '2bbb83277553'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dbsppi',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nama', sa.String(length=30), nullable=True),
    sa.Column('jabatan', sa.String(length=20), nullable=True),
    sa.Column('nip', sa.String(length=10), nullable=True),
    sa.Column('exp_date', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dbsppi')
    # ### end Alembic commands ###
