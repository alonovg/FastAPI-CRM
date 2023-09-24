"""Initial migration

Revision ID: e36e76cf0e67
Revises: 
Create Date: 2023-09-22 19:02:34.939141

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'e36e76cf0e67'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('clients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('executors',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('pays_methods',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('services',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('statuses',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(), nullable=False),
    sa.Column('hashed_password', sa.String(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_num', sa.Integer(), nullable=False),
    sa.Column('order_creator', sa.Integer(), nullable=True),
    sa.Column('order_name', sa.String(), nullable=False),
    sa.Column('order_date_create', sa.Date(), nullable=False),
    sa.Column('order_date_close', sa.Date(), nullable=True),
    sa.Column('order_client', sa.Integer(), nullable=False),
    sa.Column('order_get_pay', sa.Boolean(), nullable=False),
    sa.Column('order_pay_method', sa.Integer(), nullable=True),
    sa.Column('order_sum', sa.Float(), nullable=True),
    sa.Column('order_status', sa.Integer(), nullable=True),
    sa.Column('order_profit', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['order_client'], ['clients.id'], ),
    sa.ForeignKeyConstraint(['order_creator'], ['users.id'], ),
    sa.ForeignKeyConstraint(['order_pay_method'], ['pays_methods.id'], ),
    sa.ForeignKeyConstraint(['order_status'], ['statuses.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('executor_orders',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('order_name', sa.String(), nullable=True),
    sa.Column('order_num', sa.Integer(), nullable=False),
    sa.Column('order_executor', sa.Integer(), nullable=False),
    sa.Column('order_status', sa.Integer(), nullable=False),
    sa.Column('order_send_pay', sa.Boolean(), nullable=False),
    sa.Column('order_pay_method', sa.Integer(), nullable=True),
    sa.Column('order_sum', sa.Float(), nullable=True),
    sa.Column('order_service', sa.Integer(), nullable=False),
    sa.Column('order_date_create', sa.Date(), nullable=False),
    sa.Column('order_date_close', sa.Date(), nullable=True),
    sa.ForeignKeyConstraint(['order_executor'], ['executors.id'], ),
    sa.ForeignKeyConstraint(['order_num'], ['orders.id'], ),
    sa.ForeignKeyConstraint(['order_pay_method'], ['pays_methods.id'], ),
    sa.ForeignKeyConstraint(['order_service'], ['services.id'], ),
    sa.ForeignKeyConstraint(['order_status'], ['statuses.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('executor_orders')
    op.drop_table('orders')
    op.drop_table('users')
    op.drop_table('statuses')
    op.drop_table('services')
    op.drop_table('pays_methods')
    op.drop_table('executors')
    op.drop_table('clients')
    # ### end Alembic commands ###
