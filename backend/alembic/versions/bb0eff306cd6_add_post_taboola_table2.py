"""add post_taboola_table2

Revision ID: bb0eff306cd6
Revises: 345071af008a
Create Date: 2023-09-12 10:10:16.918356

"""
from alembic import op
import sqlalchemy as sa
import fastapi_users_db_sqlalchemy


# revision identifiers, used by Alembic.
revision = 'bb0eff306cd6'
down_revision = '345071af008a'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('post_taboola_table', 'post_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('post_taboola_table', 'taboola_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.drop_column('post_taboola_table', 'id')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('post_taboola_table', sa.Column('id', sa.INTEGER(), autoincrement=True, nullable=False))
    op.alter_column('post_taboola_table', 'taboola_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('post_taboola_table', 'post_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # ### end Alembic commands ###
