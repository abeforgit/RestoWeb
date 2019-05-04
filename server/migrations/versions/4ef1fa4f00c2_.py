"""empty message

Revision ID: 4ef1fa4f00c2
Revises: e7a35d7df82e
Create Date: 2019-05-03 14:10:37.613058

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4ef1fa4f00c2'
down_revision = 'e7a35d7df82e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('dish_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=30), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name')
    )
    op.add_column('dish', sa.Column('type_id', sa.Integer(), nullable=True))
    op.create_foreign_key(None, 'dish', 'dish_type', ['type_id'], ['id'])
    op.drop_column('dish', 'type')
    op.add_column('user', sa.Column('admin', sa.Boolean(), nullable=False))
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('user', 'admin')
    op.add_column('dish', sa.Column('type', sa.VARCHAR(length=30), nullable=False))
    op.drop_constraint(None, 'dish', type_='foreignkey')
    op.drop_column('dish', 'type_id')
    op.drop_table('dish_type')
    # ### end Alembic commands ###