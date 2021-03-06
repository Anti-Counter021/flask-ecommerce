"""empty message

Revision ID: 4304b4ec280c
Revises: 56eab3fde1fc
Create Date: 2021-05-31 15:22:59.557891

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4304b4ec280c'
down_revision = '56eab3fde1fc'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('product', sa.Column('delivery_product_terminated', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('product', 'delivery_product_terminated')
    # ### end Alembic commands ###
