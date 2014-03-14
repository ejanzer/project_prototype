"""add salt column to user table

Revision ID: 22fe0ad611c5
Revises: None
Create Date: 2014-03-13 22:23:05.018834

"""

# revision identifiers, used by Alembic.
revision = '22fe0ad611c5'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    op.create_table(
	'users',
	sa.Column('id', sa.Integer, primary_key=True),
	sa.Column('username', sa.String(64), nullable=False),
	sa.Column('password', sa.String(64), nullable=False),
	sa.Column('salt', sa.String(64), nullable=False),
	)


def downgrade():
    op.drop_table('users')
