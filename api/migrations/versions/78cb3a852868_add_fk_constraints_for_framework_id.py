"""add_fk_constraints_for_framework_id

Revision ID: 78cb3a852868
Revises: 67e7f418afb6
Create Date: 2025-07-25 13:41:33.202586

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '78cb3a852868'
down_revision: Union[str, Sequence[str], None] = '67e7f418afb6'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # Use batch operations to add foreign key constraints for SQLite
    with op.batch_alter_table('controlfunction') as batch_op:
        batch_op.create_foreign_key(
            'fk_controlfunction_framework_id',
            'controlframework',
            ['framework_id'],
            ['id']
        )
    
    with op.batch_alter_table('controlassetclass') as batch_op:
        batch_op.create_foreign_key(
            'fk_controlassetclass_framework_id',
            'controlframework',
            ['framework_id'],
            ['id']
        )


def downgrade() -> None:
    """Downgrade schema."""
    # Drop foreign key constraints
    with op.batch_alter_table('controlfunction') as batch_op:
        batch_op.drop_constraint('fk_controlfunction_framework_id', type_='foreignkey')
    
    with op.batch_alter_table('controlassetclass') as batch_op:
        batch_op.drop_constraint('fk_controlassetclass_framework_id', type_='foreignkey')
