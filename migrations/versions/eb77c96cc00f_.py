"""empty message

Revision ID: eb77c96cc00f
Revises: 74269c5b3868
Create Date: 2021-05-29 12:54:40.655318

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'eb77c96cc00f'
down_revision = '74269c5b3868'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('cart', sa.Column('for_anonymous_user', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('cart', 'for_anonymous_user')
    # ### end Alembic commands ###