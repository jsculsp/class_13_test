"""initial migration

Revision ID: fafef60eac6a
Revises: None
Create Date: 2016-09-13 10:33:32.253478

"""

# revision identifiers, used by Alembic.
revision = 'fafef60eac6a'
down_revision = None

from alembic import op
import sqlalchemy as sa


def upgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('what_the_fucks')
    op.drop_table('contents')
    ### end Alembic commands ###


def downgrade():
    ### commands auto generated by Alembic - please adjust! ###
    op.create_table('contents',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('content', sa.VARCHAR(), nullable=True),
    sa.Column('created_time', sa.INTEGER(), nullable=True),
    sa.Column('weibo_id', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('what_the_fucks',
    sa.Column('id', sa.INTEGER(), nullable=False),
    sa.Column('fuck', sa.VARCHAR(), nullable=True),
    sa.Column('fuck_time', sa.INTEGER(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    ### end Alembic commands ###
