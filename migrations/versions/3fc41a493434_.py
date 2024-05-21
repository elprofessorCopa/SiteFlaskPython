"""empty message

Revision ID: 3fc41a493434
Revises: 
Create Date: 2024-01-30 19:06:27.392512

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '3fc41a493434'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('billets',
    sa.Column('numero', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('destination', sa.String(length=50), nullable=False),
    sa.Column('prix', sa.Integer(), nullable=False),
    sa.Column('date_depart', sa.DateTime(), nullable=False),
    sa.Column('date_retour', sa.DateTime(), nullable=False),
    sa.Column('date_creation', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('numero')
    )
    op.create_table('utilisateur',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('nom', sa.String(length=50), nullable=False),
    sa.Column('prenom', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('password', sa.String(length=50), nullable=False),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('email')
    )
    op.create_table('reservations',
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('utilisateur_id', sa.Integer(), nullable=False),
    sa.Column('billet_id', sa.Integer(), nullable=False),
    sa.Column('date_reservation', sa.DateTime(), nullable=False),
    sa.ForeignKeyConstraint(['billet_id'], ['billets.numero'], ),
    sa.ForeignKeyConstraint(['utilisateur_id'], ['utilisateur.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('reservations')
    op.drop_table('utilisateur')
    op.drop_table('billets')
    # ### end Alembic commands ###
