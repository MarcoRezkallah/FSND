"""empty message

Revision ID: 91b6bb137d61
Revises: a3540200e295
Create Date: 2020-11-23 03:52:06.714170

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '91b6bb137d61'
down_revision = 'a3540200e295'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('genres', sa.String(length=120), nullable=True))
    op.drop_column('Venue', 'genre')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('Venue', sa.Column('genre', sa.VARCHAR(length=120), autoincrement=False, nullable=True))
    op.drop_column('Venue', 'genres')
    # ### end Alembic commands ###
