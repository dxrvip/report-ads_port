"""domain

Revision ID: da84a0acb4b1
Revises: 5c89a726934c
Create Date: 2023-09-05 12:10:05.157966

"""
from alembic import op
import sqlalchemy as sa
import fastapi_users_db_sqlalchemy


# revision identifiers, used by Alembic.
revision = 'da84a0acb4b1'
down_revision = '5c89a726934c'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('domain',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('base_url', sa.String(length=60), nullable=False, comment='套利网址'),
    sa.Column('create', sa.DateTime(timezone=True), server_default=sa.text('now()'), nullable=False, comment='添加时间'),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('base_url')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('domain')
    # ### end Alembic commands ###
