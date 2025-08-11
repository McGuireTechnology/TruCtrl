# CRUD operations for Asset Classes

from sqlmodel import Session, select
from typing import Sequence, Optional
from fastapi import HTTPException
from .models import ControlAssetClass, ControlAssetClassCreate, ControlAssetClassUpdate, AssetClassRelationship

def get_asset_classes(session: Session) -> Sequence[ControlAssetClass]:
    """Get all asset classes"""
    statement = select(ControlAssetClass).order_by(ControlAssetClass.name)
    return session.exec(statement).all()

def get_asset_class(session: Session, asset_class_id: str) -> Optional[ControlAssetClass]:
    """Get a specific asset class by ID"""
    statement = select(ControlAssetClass).where(ControlAssetClass.id == asset_class_id)
    return session.exec(statement).first()

def create_asset_class(session: Session, asset_class_data: ControlAssetClassCreate) -> ControlAssetClass:
    """Create a new asset class"""
    asset_class = ControlAssetClass.model_validate(asset_class_data)
    session.add(asset_class)
    session.commit()
    session.refresh(asset_class)
    return asset_class

def update_asset_class(session: Session, asset_class_id: str, asset_class_data: ControlAssetClassUpdate) -> Optional[ControlAssetClass]:
    """Update an existing asset class"""
    asset_class = get_asset_class(session, asset_class_id)
    if not asset_class:
        return None
    
    # Check if asset class is locked
    if asset_class.locked:
        raise HTTPException(status_code=403, detail="Cannot modify locked asset class")
    
    update_data = asset_class_data.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(asset_class, field, value)
    
    session.add(asset_class)
    session.commit()
    session.refresh(asset_class)
    return asset_class

def delete_asset_class(session: Session, asset_class_id: str) -> bool:
    """Delete an asset class"""
    asset_class = get_asset_class(session, asset_class_id)
    if not asset_class:
        return False
    
    # Check if asset class is locked
    if asset_class.locked:
        raise HTTPException(status_code=403, detail="Cannot delete locked asset class")
    
    # First, delete all relationships where this asset class is either parent or child
    # Delete relationships where this asset class is the parent
    parent_relationships = session.exec(
        select(AssetClassRelationship).where(AssetClassRelationship.parent_id == asset_class_id)
    ).all()
    for rel in parent_relationships:
        session.delete(rel)
    
    # Delete relationships where this asset class is the child
    child_relationships = session.exec(
        select(AssetClassRelationship).where(AssetClassRelationship.child_id == asset_class_id)
    ).all()
    for rel in child_relationships:
        session.delete(rel)
    
    # Now delete the asset class itself
    session.delete(asset_class)
    session.commit()
    return True

# Asset Class Relationship CRUD operations

def get_asset_class_parents(session: Session, asset_class_id: str) -> Sequence[ControlAssetClass]:
    """Get all parent asset classes for a given asset class"""
    # Get parent relationships
    parent_relationships = session.exec(
        select(AssetClassRelationship).where(AssetClassRelationship.child_id == asset_class_id)
    ).all()
    
    # Get the parent asset classes
    parents = []
    for rel in parent_relationships:
        parent = get_asset_class(session, rel.parent_id)
        if parent:
            parents.append(parent)
    
    return sorted(parents, key=lambda x: x.name)

def get_asset_class_children(session: Session, asset_class_id: str) -> Sequence[ControlAssetClass]:
    """Get all child asset classes for a given asset class"""
    # Get child relationships
    child_relationships = session.exec(
        select(AssetClassRelationship).where(AssetClassRelationship.parent_id == asset_class_id)
    ).all()
    
    # Get the child asset classes
    children = []
    for rel in child_relationships:
        child = get_asset_class(session, rel.child_id)
        if child:
            children.append(child)
    
    return sorted(children, key=lambda x: x.name)

def add_asset_class_relationship(session: Session, parent_id: str, child_id: str) -> tuple[bool, str]:
    """Add a parent-child relationship between asset classes"""
    # Prevent self-reference
    if parent_id == child_id:
        return False, "An asset class cannot be a parent of itself"
    
    # Check if both asset classes exist
    parent = get_asset_class(session, parent_id)
    child = get_asset_class(session, child_id)
    if not parent:
        return False, f"Parent asset class with ID {parent_id} not found"
    if not child:
        return False, f"Child asset class with ID {child_id} not found"
    
    # Check if relationship already exists
    existing = session.exec(
        select(AssetClassRelationship)
        .where(AssetClassRelationship.parent_id == parent_id)
        .where(AssetClassRelationship.child_id == child_id)
    ).first()
    
    if existing:
        return False, f"Relationship already exists: {parent.name} -> {child.name}"
    
    # Check for circular dependency (if child is already a parent of parent)
    circular = session.exec(
        select(AssetClassRelationship)
        .where(AssetClassRelationship.parent_id == child_id)
        .where(AssetClassRelationship.child_id == parent_id)
    ).first()
    
    if circular:
        return False, f"Would create circular dependency: {child.name} is already a parent of {parent.name}"
    
    # Create new relationship
    try:
        relationship = AssetClassRelationship(parent_id=parent_id, child_id=child_id)
        session.add(relationship)
        session.commit()
        return True, f"Successfully added relationship: {parent.name} -> {child.name}"
    except Exception as e:
        session.rollback()
        return False, f"Database error: {str(e)}"

def remove_asset_class_relationship(session: Session, parent_id: str, child_id: str) -> bool:
    """Remove a parent-child relationship between asset classes"""
    relationship = session.exec(
        select(AssetClassRelationship)
        .where(AssetClassRelationship.parent_id == parent_id)
        .where(AssetClassRelationship.child_id == child_id)
    ).first()
    
    if not relationship:
        return False
    
    session.delete(relationship)
    session.commit()
    return True
