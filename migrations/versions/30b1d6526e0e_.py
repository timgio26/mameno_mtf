"""empty message

Revision ID: 30b1d6526e0e
Revises: 2bd29887dab6
Create Date: 2022-02-24 16:35:32.557894

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '30b1d6526e0e'
down_revision = '2bd29887dab6'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dbfucomp',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('idcomp', sa.Integer(), nullable=True),
    sa.Column('fudate', sa.Date(), nullable=True),
    sa.Column('notes', sa.Text(), nullable=True),
    sa.Column('status', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('dbfucomp')
    # ### end Alembic commands ###