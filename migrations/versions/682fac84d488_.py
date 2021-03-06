"""empty message

Revision ID: 682fac84d488
Revises: 02b734e5307b
Create Date: 2020-09-10 22:27:48.129586

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '682fac84d488'
down_revision = '02b734e5307b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('usuario',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=20), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('task',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('label', sa.String(length=50), nullable=False),
    sa.Column('done', sa.Boolean(), nullable=False),
    sa.Column('usuario_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['usuario_id'], ['usuario.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('task')
    op.drop_table('usuario')
    # ### end Alembic commands ###
