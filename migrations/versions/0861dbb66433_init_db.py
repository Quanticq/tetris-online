"""init db

Revision ID: 0861dbb66433
Revises: 
Create Date: 2018-05-16 21:14:57.960624

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0861dbb66433'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('tournaments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.Column('description', sa.String(length=1024), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_tournaments_name'), 'tournaments', ['name'], unique=True)
    op.create_table('users',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=120), nullable=True),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('max_score', sa.Integer(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_users_max_score'), 'users', ['max_score'], unique=False)
    op.create_index(op.f('ix_users_name'), 'users', ['name'], unique=True)
    op.create_table('fights',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('tournament_id', sa.Integer(), nullable=True),
    sa.Column('user1_id', sa.Integer(), nullable=True),
    sa.Column('user2_id', sa.Integer(), nullable=True),
    sa.Column('user1_score', sa.Integer(), nullable=True),
    sa.Column('user2_score', sa.Integer(), nullable=True),
    sa.Column('status', sa.String(length=128), nullable=True),
    sa.ForeignKeyConstraint(['tournament_id'], ['tournaments.id'], ),
    sa.ForeignKeyConstraint(['user1_id'], ['users.id'], ),
    sa.ForeignKeyConstraint(['user2_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('tournaments_users',
    sa.Column('tournament_id', sa.Integer(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['tournament_id'], ['tournaments.id'], ),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], )
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('tournaments_users')
    op.drop_table('fights')
    op.drop_index(op.f('ix_users_name'), table_name='users')
    op.drop_index(op.f('ix_users_max_score'), table_name='users')
    op.drop_table('users')
    op.drop_index(op.f('ix_tournaments_name'), table_name='tournaments')
    op.drop_table('tournaments')
    # ### end Alembic commands ###
