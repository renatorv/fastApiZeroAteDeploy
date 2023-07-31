"""Cria tabela de contas a pagar e receber.

Revision ID: 3f8f051e6970
Revises: 
Create Date: 2023-07-31 08:35:17.190555

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '3f8f051e6970'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('conta_pagar_receber',
                    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
                    sa.Column('descricao', sa.String(length=100), nullable=True),
                    sa.Column('valor', sa.Numeric(), nullable=True),
                    sa.Column('tipo', sa.String(length=30), nullable=True),
                    sa.PrimaryKeyConstraint('id')
                    )


def downgrade() -> None:
    op.drop_table('conta_pagar_receber')
