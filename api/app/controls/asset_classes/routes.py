# API routes for Asset Classes

from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from typing import Optional, Sequence
from ...deps import get_session
from ... import models
from ... import deps
from .models import (
    ControlAssetClass,
    ControlAssetClassCreate,
    ControlAssetClassUpdate,
    ControlAssetClassPublic,
    ControlAssetClassesPublic
)
from .crud import (
    get_asset_classes,
    get_asset_class,
    create_asset_class,
    update_asset_class,
    delete_asset_class,
    get_asset_class_parents,
    get_asset_class_children,
    add_asset_class_relationship,
    remove_asset_class_relationship
)

router = APIRouter()

@router.get("/", response_model=ControlAssetClassesPublic)
def get_asset_classes_route(
    session: Session = Depends(get_session),
    current_user: Optional[models.User] = Depends(deps.get_current_active_user)
):
    """Get all asset classes"""
    asset_classes = get_asset_classes(session)
    return {"data": list(asset_classes)}

@router.get("/{id}", response_model=ControlAssetClassPublic)
def get_asset_class_route(
    id: str,
    session: Session = Depends(get_session),
    current_user: Optional[models.User] = Depends(deps.get_current_active_user)
):
    """Get a specific asset class"""
    asset_class = get_asset_class(session, id)
    if not asset_class:
        raise HTTPException(status_code=404, detail="Asset class not found")
    
    # Get relationships
    parents = get_asset_class_parents(session, id)
    children = get_asset_class_children(session, id)
    
    # Create response with relationships
    from .models import ControlAssetClassStub
    
    # Convert the base asset class to dict first
    response_dict = {
        "id": asset_class.id,
        "name": asset_class.name,
        "short_name": asset_class.short_name,
        "description": asset_class.description,
        "color": asset_class.color,
        "locked": asset_class.locked,
        "parents": [ControlAssetClassStub.model_validate(p) for p in parents],
        "children": [ControlAssetClassStub.model_validate(c) for c in children]
    }
    
    return ControlAssetClassPublic.model_validate(response_dict)

@router.post("/", response_model=ControlAssetClassPublic)
def create_asset_class_route(
    asset_class: ControlAssetClassCreate,
    session: Session = Depends(get_session),
    current_user: Optional[models.User] = Depends(deps.get_current_active_user)
):
    """Create a new asset class"""
    return create_asset_class(session, asset_class)

@router.patch("/{id}", response_model=ControlAssetClassPublic)
def update_asset_class_route(
    id: str,
    updates: ControlAssetClassUpdate,
    session: Session = Depends(get_session),
    current_user: Optional[models.User] = Depends(deps.get_current_active_user)
):
    """Update an asset class"""
    asset_class = update_asset_class(session, id, updates)
    if not asset_class:
        raise HTTPException(status_code=404, detail="Asset class not found")
    return asset_class

@router.delete("/{id}")
def delete_asset_class_route(
    id: str,
    session: Session = Depends(get_session),
    current_user: Optional[models.User] = Depends(deps.get_current_active_user)
):
    """Delete an asset class"""
    success = delete_asset_class(session, id)
    if not success:
        raise HTTPException(status_code=404, detail="Asset class not found")
    return {"message": "Asset class deleted successfully"}

# Asset Class Relationship endpoints

@router.get("/{id}/parents", response_model=ControlAssetClassesPublic)
def get_asset_class_parents_route(
    id: str,
    session: Session = Depends(get_session),
    current_user: Optional[models.User] = Depends(deps.get_current_active_user)
):
    """Get parent asset classes for a given asset class"""
    parents = get_asset_class_parents(session, id)
    return {"data": list(parents)}

@router.get("/{id}/children", response_model=ControlAssetClassesPublic)
def get_asset_class_children_route(
    id: str,
    session: Session = Depends(get_session),
    current_user: Optional[models.User] = Depends(deps.get_current_active_user)
):
    """Get child asset classes for a given asset class"""
    children = get_asset_class_children(session, id)
    return {"data": list(children)}

@router.post("/{child_id}/parents/{parent_id}")
def add_asset_class_parent_route(
    child_id: str,
    parent_id: str,
    session: Session = Depends(get_session),
    current_user: Optional[models.User] = Depends(deps.get_current_active_user)
):
    """Add a parent-child relationship between asset classes"""
    success, message = add_asset_class_relationship(session, parent_id, child_id)
    if not success:
        raise HTTPException(status_code=400, detail=message)
    return {"message": message}

@router.delete("/{child_id}/parents/{parent_id}")
def remove_asset_class_parent_route(
    child_id: str,
    parent_id: str,
    session: Session = Depends(get_session),
    current_user: Optional[models.User] = Depends(deps.get_current_active_user)
):
    """Remove a parent-child relationship between asset classes"""
    success = remove_asset_class_relationship(session, parent_id, child_id)
    if not success:
        raise HTTPException(status_code=404, detail="Relationship not found")
    return {"message": "Relationship removed successfully"}
