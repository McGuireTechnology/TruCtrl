# Configuration Item Types CRUD Operations

from sqlmodel import Session, select
from typing import Optional, Sequence
from .models import (
    ConfigurationItemType,
    ConfigurationItemTypeCreate,
    ConfigurationItemTypeUpdate,
    CITypeRelationship
)

def get_ci_types(session: Session) -> Sequence[ConfigurationItemType]:
    """Get all configuration item types"""
    statement = select(ConfigurationItemType)
    return session.exec(statement).all()

def get_ci_type(session: Session, ci_type_id: str) -> Optional[ConfigurationItemType]:
    """Get a specific configuration item type by ID"""
    statement = select(ConfigurationItemType).where(ConfigurationItemType.id == ci_type_id)
    return session.exec(statement).first()

def create_ci_type(session: Session, ci_type_create: ConfigurationItemTypeCreate) -> ConfigurationItemType:
    """Create a new configuration item type"""
    ci_type = ConfigurationItemType.model_validate(ci_type_create.model_dump())
    session.add(ci_type)
    session.commit()
    session.refresh(ci_type)
    return ci_type

def update_ci_type(session: Session, ci_type_id: str, ci_type_update: ConfigurationItemTypeUpdate) -> Optional[ConfigurationItemType]:
    """Update a configuration item type"""
    ci_type = get_ci_type(session, ci_type_id)
    if not ci_type:
        return None
    
    # Update only provided fields
    update_data = ci_type_update.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(ci_type, field, value)
    
    session.commit()
    session.refresh(ci_type)
    return ci_type

def delete_ci_type(session: Session, ci_type_id: str) -> bool:
    """Delete a configuration item type"""
    ci_type = get_ci_type(session, ci_type_id)
    if not ci_type:
        return False
    
    # Check if CI type is locked
    if ci_type.locked:
        return False
    
    session.delete(ci_type)
    session.commit()
    return True

# Relationship management
def get_ci_type_parents(session: Session, ci_type_id: str) -> Sequence[ConfigurationItemType]:
    """Get parent CI types for a given CI type"""
    statement = (
        select(ConfigurationItemType)
        .join(CITypeRelationship, ConfigurationItemType.id == CITypeRelationship.parent_id)
        .where(CITypeRelationship.child_id == ci_type_id)
    )
    return session.exec(statement).all()

def get_ci_type_children(session: Session, ci_type_id: str) -> Sequence[ConfigurationItemType]:
    """Get child CI types for a given CI type"""
    statement = (
        select(ConfigurationItemType)
        .join(CITypeRelationship, ConfigurationItemType.id == CITypeRelationship.child_id)
        .where(CITypeRelationship.parent_id == ci_type_id)
    )
    return session.exec(statement).all()

def add_ci_type_relationship(session: Session, parent_id: str, child_id: str) -> tuple[bool, str]:
    """Add a parent-child relationship between CI types"""
    # Validate that both CI types exist
    parent = get_ci_type(session, parent_id)
    child = get_ci_type(session, child_id)
    
    if not parent:
        return False, "Parent CI type not found"
    if not child:
        return False, "Child CI type not found"
    if parent_id == child_id:
        return False, "Cannot create self-referential relationship"
    
    # Check if relationship already exists
    existing = session.exec(
        select(CITypeRelationship).where(
            CITypeRelationship.parent_id == parent_id,
            CITypeRelationship.child_id == child_id
        )
    ).first()
    
    if existing:
        return False, "Relationship already exists"
    
    # TODO: Add cycle detection to prevent circular references
    
    # Create the relationship
    relationship = CITypeRelationship(parent_id=parent_id, child_id=child_id)
    session.add(relationship)
    session.commit()
    
    return True, "Relationship added successfully"

def remove_ci_type_relationship(session: Session, parent_id: str, child_id: str) -> bool:
    """Remove a parent-child relationship between CI types"""
    relationship = session.exec(
        select(CITypeRelationship).where(
            CITypeRelationship.parent_id == parent_id,
            CITypeRelationship.child_id == child_id
        )
    ).first()
    
    if not relationship:
        return False
    
    session.delete(relationship)
    session.commit()
    return True
