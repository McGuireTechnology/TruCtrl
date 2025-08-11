# API routes for Configuration Item Types

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import Optional
from ...deps import get_session, get_current_active_user
from ...models import User
from .models import (
    ConfigurationItemType,
    ConfigurationItemTypeCreate,
    ConfigurationItemTypeUpdate,
    ConfigurationItemTypePublic,
    ConfigurationItemTypesPublic
)
from .crud import (
    get_ci_types,
    get_ci_type,
    create_ci_type,
    update_ci_type,
    delete_ci_type,
    get_ci_type_parents,
    get_ci_type_children,
    add_ci_type_relationship,
    remove_ci_type_relationship
)

router = APIRouter()

@router.get("/", response_model=ConfigurationItemTypesPublic)
def get_ci_types_route(
    session: Session = Depends(get_session),
    current_user: Optional[User] = Depends(get_current_active_user)
):
    """Get all configuration item types"""
    ci_types = get_ci_types(session)
    return {"data": list(ci_types)}

@router.get("/{id}", response_model=ConfigurationItemTypePublic)
def get_ci_type_route(
    id: str,
    session: Session = Depends(get_session),
    current_user: Optional[User] = Depends(get_current_active_user)
):
    """Get a specific configuration item type"""
    ci_type = get_ci_type(session, id)
    if not ci_type:
        raise HTTPException(status_code=404, detail="Configuration item type not found")
    
    # Get relationships
    parents = get_ci_type_parents(session, id)
    children = get_ci_type_children(session, id)
    
    # Create response with relationships
    from .models import ConfigurationItemTypeStub
    
    response_dict = {
        "id": ci_type.id,
        "name": ci_type.name,
        "short_name": ci_type.short_name,
        "description": ci_type.description,
        "color": ci_type.color,
        "icon": ci_type.icon,
        "locked": ci_type.locked,
        "parents": [ConfigurationItemTypeStub.model_validate(p) for p in parents],
        "children": [ConfigurationItemTypeStub.model_validate(c) for c in children]
    }
    
    return ConfigurationItemTypePublic.model_validate(response_dict)

@router.post("/", response_model=ConfigurationItemTypePublic)
def create_ci_type_route(
    ci_type: ConfigurationItemTypeCreate,
    session: Session = Depends(get_session),
    current_user: Optional[User] = Depends(get_current_active_user)
):
    """Create a new configuration item type"""
    return create_ci_type(session, ci_type)

@router.patch("/{id}", response_model=ConfigurationItemTypePublic)
def update_ci_type_route(
    id: str,
    updates: ConfigurationItemTypeUpdate,
    session: Session = Depends(get_session),
    current_user: Optional[User] = Depends(get_current_active_user)
):
    """Update a configuration item type"""
    ci_type = update_ci_type(session, id, updates)
    if not ci_type:
        raise HTTPException(status_code=404, detail="Configuration item type not found")
    return ci_type

@router.delete("/{id}")
def delete_ci_type_route(
    id: str,
    session: Session = Depends(get_session),
    current_user: Optional[User] = Depends(get_current_active_user)
):
    """Delete a configuration item type"""
    success = delete_ci_type(session, id)
    if not success:
        raise HTTPException(status_code=404, detail="Configuration item type not found or is locked")
    return {"message": "Configuration item type deleted successfully"}

# Configuration Item Type Relationship endpoints

@router.get("/{id}/parents", response_model=ConfigurationItemTypesPublic)
def get_ci_type_parents_route(
    id: str,
    session: Session = Depends(get_session),
    current_user: Optional[User] = Depends(get_current_active_user)
):
    """Get parent configuration item types for a given CI type"""
    parents = get_ci_type_parents(session, id)
    return {"data": list(parents)}

@router.get("/{id}/children", response_model=ConfigurationItemTypesPublic)
def get_ci_type_children_route(
    id: str,
    session: Session = Depends(get_session),
    current_user: Optional[User] = Depends(get_current_active_user)
):
    """Get child configuration item types for a given CI type"""
    children = get_ci_type_children(session, id)
    return {"data": list(children)}

@router.post("/{child_id}/parents/{parent_id}")
def add_ci_type_parent_route(
    child_id: str,
    parent_id: str,
    session: Session = Depends(get_session),
    current_user: Optional[User] = Depends(get_current_active_user)
):
    """Add a parent-child relationship between configuration item types"""
    success, message = add_ci_type_relationship(session, parent_id, child_id)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return {"message": message}

@router.delete("/{child_id}/parents/{parent_id}")
def remove_ci_type_parent_route(
    child_id: str,
    parent_id: str,
    session: Session = Depends(get_session),
    current_user: Optional[User] = Depends(get_current_active_user)
):
    """Remove a parent-child relationship between configuration item types"""
    success = remove_ci_type_relationship(session, parent_id, child_id)
    if not success:
        raise HTTPException(status_code=404, detail="Relationship not found")
    return {"message": "Relationship removed successfully"}
