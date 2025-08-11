"""migrate_asset_classes_to_cmdb_configuration_item_types

Revision ID: 59ceb9c92604
Revises: 6ec16068436f
Create Date: 2025-08-11 12:38:06.812352

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlmodel


# revision identifiers, used by Alembic.
revision: str = '59ceb9c92604'
down_revision: Union[str, Sequence[str], None] = '6ec16068436f'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema: Create CMDB tables and migrate asset classes."""
    
    # Create new CMDB tables
    # Configuration Item Type table (replaces controlassetclass)
    op.create_table('configurationitemtype',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('short_name', sa.String(), nullable=True),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('color', sa.String(), nullable=False),
        sa.Column('icon', sa.String(), nullable=True),
        sa.Column('locked', sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_configurationitemtype_id'), 'configurationitemtype', ['id'], unique=False)
    op.create_index(op.f('ix_configurationitemtype_name'), 'configurationitemtype', ['name'], unique=False)
    op.create_index(op.f('ix_configurationitemtype_short_name'), 'configurationitemtype', ['short_name'], unique=False)
    
    # CI Type Relationship table (replaces assetclassrelationship)
    op.create_table('cityperelationship',
        sa.Column('parent_id', sa.String(), nullable=False),
        sa.Column('child_id', sa.String(), nullable=False),
        sa.ForeignKeyConstraint(['child_id'], ['configurationitemtype.id'], ),
        sa.ForeignKeyConstraint(['parent_id'], ['configurationitemtype.id'], ),
        sa.PrimaryKeyConstraint('parent_id', 'child_id')
    )
    
    # Configuration Item table
    op.create_table('configurationitem',
        sa.Column('id', sa.String(), nullable=False),
        sa.Column('ci_type_id', sa.String(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('description', sa.String(), nullable=True),
        sa.Column('status', sa.String(), nullable=False),
        sa.Column('environment', sa.String(), nullable=True),
        sa.Column('owner', sa.String(), nullable=True),
        sa.Column('business_service', sa.String(), nullable=True),
        sa.Column('location', sa.String(), nullable=True),
        sa.Column('cost_center', sa.String(), nullable=True),
        sa.Column('purchase_cost', sa.Float(), nullable=True),
        sa.Column('annual_cost', sa.Float(), nullable=True),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.Column('updated_at', sa.DateTime(), nullable=False),
        sa.Column('discovered_at', sa.DateTime(), nullable=True),
        sa.Column('last_seen', sa.DateTime(), nullable=True),
        sa.Column('attributes', sa.JSON(), nullable=True),
        sa.ForeignKeyConstraint(['ci_type_id'], ['configurationitemtype.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_configurationitem_id'), 'configurationitem', ['id'], unique=False)
    op.create_index(op.f('ix_configurationitem_ci_type_id'), 'configurationitem', ['ci_type_id'], unique=False)
    op.create_index(op.f('ix_configurationitem_name'), 'configurationitem', ['name'], unique=False)
    
    # CI Relationship table
    op.create_table('cirelationship',
        sa.Column('parent_id', sa.String(), nullable=False),
        sa.Column('child_id', sa.String(), nullable=False),
        sa.Column('relationship_type', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(['child_id'], ['configurationitem.id'], ),
        sa.ForeignKeyConstraint(['parent_id'], ['configurationitem.id'], ),
        sa.PrimaryKeyConstraint('parent_id', 'child_id')
    )
    
    # Migrate data from controlassetclass to configurationitemtype
    connection = op.get_bind()
    
    # Check if the old table exists
    inspector = sa.inspect(connection)
    if 'controlassetclass' in inspector.get_table_names():
        # Copy data from controlassetclass to configurationitemtype
        connection.execute(sa.text("""
            INSERT INTO configurationitemtype (id, name, short_name, description, color, locked, icon)
            SELECT id, name, short_name, description, color, locked, NULL as icon
            FROM controlassetclass
        """))
        
        # Copy relationships from assetclassrelationship to cityperelationship
        if 'assetclassrelationship' in inspector.get_table_names():
            connection.execute(sa.text("""
                INSERT INTO cityperelationship (parent_id, child_id)
                SELECT parent_id, child_id FROM assetclassrelationship
            """))


def downgrade() -> None:
    """Downgrade schema: Remove CMDB tables and restore asset classes."""
    # Drop new CMDB tables
    op.drop_table('cirelationship')
    op.drop_table('configurationitem')
    op.drop_table('cityperelationship')
    op.drop_table('configurationitemtype')
