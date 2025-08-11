from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from ...db import get_session
from ... import models, deps
from .models import (
    ControlSafeguard, ControlSafeguardCreate, ControlSafeguardUpdate, ControlSafeguardPublic, ControlSafeguardsPublic,
    SafeguardRelationship, SafeguardRelationshipCreate, SafeguardRelationshipUpdate, SafeguardRelationshipPublic, SafeguardRelationshipsPublic,
    ControlSafeguardWithRelationships, SafeguardRelationshipType
)
from .crud import get_safeguard, get_safeguards, create_safeguard, update_safeguard, delete_safeguard

router = APIRouter(prefix="/safeguards", tags=["Control Safeguards"])

@router.get("/", response_model=ControlSafeguardsPublic)
def list_safeguards(
    skip: int = 0, 
    limit: int = 100, 
    session: Session = Depends(get_session),
    current_user: Optional[models.User] = Depends(deps.get_current_active_user)
):
    safeguards = get_safeguards(session, skip=skip, limit=limit)
    
    # Enrich with related object names
    enriched_safeguards = []
    for safeguard in safeguards:
        safeguard_dict = safeguard.model_dump()
        
        # Add related object names
        if safeguard.control:
            safeguard_dict['control_name'] = safeguard.control.name
            safeguard_dict['control_short_name'] = safeguard.control.short_name
            safeguard_dict['control_color'] = safeguard.control.color
            # Get framework name from control
            if safeguard.control.framework:
                safeguard_dict['framework_name'] = safeguard.control.framework.name
                safeguard_dict['framework_short_name'] = safeguard.control.framework.short_name
                safeguard_dict['framework_color'] = safeguard.control.framework.color
        
        if safeguard.function:
            safeguard_dict['function_name'] = safeguard.function.name
            safeguard_dict['function_short_name'] = safeguard.function.short_name
            safeguard_dict['function_color'] = safeguard.function.color
            
        if safeguard.implementation_group:
            safeguard_dict['implementation_group_name'] = safeguard.implementation_group.name
            safeguard_dict['implementation_group_short_name'] = safeguard.implementation_group.short_name
            safeguard_dict['implementation_group_color'] = safeguard.implementation_group.color
        
        if safeguard.asset_class:
            safeguard_dict['asset_class_name'] = safeguard.asset_class.name
            safeguard_dict['asset_class_short_name'] = safeguard.asset_class.short_name
            safeguard_dict['asset_class_color'] = safeguard.asset_class.color
        
        enriched_safeguards.append(ControlSafeguardPublic(**safeguard_dict))
    
    return {"data": enriched_safeguards, "count": len(enriched_safeguards)}

@router.get("/{id}", response_model=ControlSafeguardPublic)
def read_safeguard(
    id: str, 
    session: Session = Depends(get_session),
    current_user: Optional[models.User] = Depends(deps.get_current_active_user)
):
    safeguard = get_safeguard(session, id)
    if not safeguard:
        raise HTTPException(status_code=404, detail="Safeguard not found")
    
    # Enrich with related object names
    safeguard_dict = safeguard.model_dump()
    
    # Add related object names
    if safeguard.control:
        safeguard_dict['control_name'] = safeguard.control.name
        safeguard_dict['control_short_name'] = safeguard.control.short_name
        safeguard_dict['control_color'] = safeguard.control.color
        # Get framework name from control
        if safeguard.control.framework:
            safeguard_dict['framework_name'] = safeguard.control.framework.name
            safeguard_dict['framework_short_name'] = safeguard.control.framework.short_name
            safeguard_dict['framework_color'] = safeguard.control.framework.color
    
    if safeguard.function:
        safeguard_dict['function_name'] = safeguard.function.name
        safeguard_dict['function_short_name'] = safeguard.function.short_name
        safeguard_dict['function_color'] = safeguard.function.color
        
    if safeguard.implementation_group:
        safeguard_dict['implementation_group_name'] = safeguard.implementation_group.name
        safeguard_dict['implementation_group_short_name'] = safeguard.implementation_group.short_name
        safeguard_dict['implementation_group_color'] = safeguard.implementation_group.color
    
    if safeguard.asset_class:
        safeguard_dict['asset_class_name'] = safeguard.asset_class.name
        safeguard_dict['asset_class_short_name'] = safeguard.asset_class.short_name
        safeguard_dict['asset_class_color'] = safeguard.asset_class.color
    
    return ControlSafeguardPublic(**safeguard_dict)

@router.post("/", response_model=ControlSafeguardPublic)
def create_safeguard_route(
    safeguard: ControlSafeguardCreate, 
    session: Session = Depends(get_session),
    current_user: Optional[models.User] = Depends(deps.get_current_active_user)
):
    db_safeguard = ControlSafeguard.model_validate(safeguard)
    return create_safeguard(session, db_safeguard)

@router.patch("/{id}", response_model=ControlSafeguardPublic)
def update_safeguard_route(
    id: str, 
    updates: ControlSafeguardUpdate, 
    session: Session = Depends(get_session),
    current_user: Optional[models.User] = Depends(deps.get_current_active_user)
):
    db_safeguard = get_safeguard(session, id)
    if not db_safeguard:
        raise HTTPException(status_code=404, detail="Safeguard not found")
    return update_safeguard(session, db_safeguard, updates.model_dump(exclude_unset=True))

@router.delete("/{id}", status_code=204)
def delete_safeguard_route(
    id: str, 
    session: Session = Depends(get_session),
    current_user: Optional[models.User] = Depends(deps.get_current_active_user)
):
    delete_safeguard(session, id)
    return None

# Safeguard Relationship Routes
@router.get("/{id}/relationships", response_model=ControlSafeguardWithRelationships)
def get_safeguard_with_relationships(
    id: str,
    session: Session = Depends(get_session),
    current_user: Optional[models.User] = Depends(deps.get_current_active_user)
):
    """Get a safeguard with all its relationships"""
    safeguard = get_safeguard(session, id)
    if not safeguard:
        raise HTTPException(status_code=404, detail="Safeguard not found")
    
    # Build the response with enriched relationship data
    safeguard_dict = safeguard.model_dump()
    
    # Add basic safeguard enrichment (same as read_safeguard)
    if safeguard.control:
        safeguard_dict['control_name'] = safeguard.control.name
        safeguard_dict['control_short_name'] = safeguard.control.short_name
        safeguard_dict['control_color'] = safeguard.control.color
        if safeguard.control.framework:
            safeguard_dict['framework_name'] = safeguard.control.framework.name
            safeguard_dict['framework_short_name'] = safeguard.control.framework.short_name
            safeguard_dict['framework_color'] = safeguard.control.framework.color
    
    # Add relationship data
    outbound_relationships = []
    for rel in safeguard.outbound_relationships:
        rel_dict = rel.model_dump()
        if rel.target_safeguard:
            rel_dict['target_safeguard_name'] = rel.target_safeguard.name
            rel_dict['target_safeguard_short_name'] = rel.target_safeguard.short_name
            # Get framework info from target safeguard's control
            if rel.target_safeguard.control and rel.target_safeguard.control.framework:
                rel_dict['target_framework_name'] = rel.target_safeguard.control.framework.name
                rel_dict['target_framework_short_name'] = rel.target_safeguard.control.framework.short_name
        outbound_relationships.append(SafeguardRelationshipPublic(**rel_dict))
    
    inbound_relationships = []
    for rel in safeguard.inbound_relationships:
        rel_dict = rel.model_dump()
        # For inbound relationships, we want the source safeguard info
        rel_dict['target_safeguard_id'] = rel.source_safeguard_id  # Flip for consistency
        if rel.source_safeguard:
            rel_dict['target_safeguard_name'] = rel.source_safeguard.name
            rel_dict['target_safeguard_short_name'] = rel.source_safeguard.short_name
            if rel.source_safeguard.control and rel.source_safeguard.control.framework:
                rel_dict['target_framework_name'] = rel.source_safeguard.control.framework.name
                rel_dict['target_framework_short_name'] = rel.source_safeguard.control.framework.short_name
        inbound_relationships.append(SafeguardRelationshipPublic(**rel_dict))
    
    safeguard_dict['outbound_relationships'] = outbound_relationships
    safeguard_dict['inbound_relationships'] = inbound_relationships
    
    return ControlSafeguardWithRelationships(**safeguard_dict)

@router.post("/{id}/relationships", response_model=SafeguardRelationshipPublic)
def create_safeguard_relationship(
    id: str,
    relationship: SafeguardRelationshipCreate,
    session: Session = Depends(get_session),
    current_user: Optional[models.User] = Depends(deps.get_current_active_user)
):
    """Create a new relationship from this safeguard to another"""
    # Verify source safeguard exists
    source_safeguard = get_safeguard(session, id)
    if not source_safeguard:
        raise HTTPException(status_code=404, detail="Source safeguard not found")
    
    # Verify target safeguard exists
    target_safeguard = get_safeguard(session, relationship.target_safeguard_id)
    if not target_safeguard:
        raise HTTPException(status_code=404, detail="Target safeguard not found")
    
    # Prevent self-referencing relationships
    if id == relationship.target_safeguard_id:
        raise HTTPException(status_code=400, detail="Cannot create relationship to self")
    
    # Check if relationship already exists
    from sqlmodel import select
    existing = session.exec(
        select(SafeguardRelationship).where(
            SafeguardRelationship.source_safeguard_id == id,
            SafeguardRelationship.target_safeguard_id == relationship.target_safeguard_id
        )
    ).first()
    
    if existing:
        raise HTTPException(status_code=400, detail="Relationship already exists")
    
    # Create the relationship
    db_relationship = SafeguardRelationship(
        source_safeguard_id=id,
        target_safeguard_id=relationship.target_safeguard_id,
        relationship_type=relationship.relationship_type,
        confidence=relationship.confidence,
        notes=relationship.notes,
        created_by=current_user.id if current_user else None
    )
    
    session.add(db_relationship)
    session.commit()
    session.refresh(db_relationship)
    
    # Create automatic reverse relationship
    reverse_type = _get_reverse_relationship_type(relationship.relationship_type)
    reverse_relationship = SafeguardRelationship(
        source_safeguard_id=relationship.target_safeguard_id,
        target_safeguard_id=id,
        relationship_type=reverse_type,
        confidence=relationship.confidence,
        notes=f"Auto-generated reverse of: {relationship.notes}" if relationship.notes else "Auto-generated reverse relationship",
        created_by=current_user.id if current_user else None
    )
    
    session.add(reverse_relationship)
    session.commit()
    
    # Return enriched relationship data
    rel_dict = db_relationship.model_dump()
    if target_safeguard:
        rel_dict['target_safeguard_name'] = target_safeguard.name
        rel_dict['target_safeguard_short_name'] = target_safeguard.short_name
        if target_safeguard.control and target_safeguard.control.framework:
            rel_dict['target_framework_name'] = target_safeguard.control.framework.name
            rel_dict['target_framework_short_name'] = target_safeguard.control.framework.short_name
    
    return SafeguardRelationshipPublic(**rel_dict)

@router.patch("/relationships/{relationship_id}", response_model=SafeguardRelationshipPublic)
def update_safeguard_relationship(
    relationship_id: str,
    updates: SafeguardRelationshipUpdate,
    session: Session = Depends(get_session),
    current_user: Optional[models.User] = Depends(deps.get_current_active_user)
):
    """Update a safeguard relationship"""
    relationship = session.get(SafeguardRelationship, relationship_id)
    if not relationship:
        raise HTTPException(status_code=404, detail="Relationship not found")
    
    # Update the relationship
    for key, value in updates.model_dump(exclude_unset=True).items():
        setattr(relationship, key, value)
    
    session.add(relationship)
    session.commit()
    session.refresh(relationship)
    
    # Update reverse relationship if relationship type changed
    if updates.relationship_type:
        from sqlmodel import select
        reverse_rel = session.exec(
            select(SafeguardRelationship).where(
                SafeguardRelationship.source_safeguard_id == relationship.target_safeguard_id,
                SafeguardRelationship.target_safeguard_id == relationship.source_safeguard_id
            )
        ).first()
        
        if reverse_rel:
            reverse_rel.relationship_type = _get_reverse_relationship_type(updates.relationship_type)
            if updates.confidence is not None:
                reverse_rel.confidence = updates.confidence
            session.add(reverse_rel)
            session.commit()
    
    # Return enriched data
    rel_dict = relationship.model_dump()
    if relationship.target_safeguard:
        rel_dict['target_safeguard_name'] = relationship.target_safeguard.name
        rel_dict['target_safeguard_short_name'] = relationship.target_safeguard.short_name
        if relationship.target_safeguard.control and relationship.target_safeguard.control.framework:
            rel_dict['target_framework_name'] = relationship.target_safeguard.control.framework.name
            rel_dict['target_framework_short_name'] = relationship.target_safeguard.control.framework.short_name
    
    return SafeguardRelationshipPublic(**rel_dict)

@router.delete("/relationships/{relationship_id}", status_code=204)
def delete_safeguard_relationship(
    relationship_id: str,
    session: Session = Depends(get_session),
    current_user: Optional[models.User] = Depends(deps.get_current_active_user)
):
    """Delete a safeguard relationship and its reverse"""
    relationship = session.get(SafeguardRelationship, relationship_id)
    if not relationship:
        raise HTTPException(status_code=404, detail="Relationship not found")
    
    # Find and delete reverse relationship
    from sqlmodel import select
    reverse_rel = session.exec(
        select(SafeguardRelationship).where(
            SafeguardRelationship.source_safeguard_id == relationship.target_safeguard_id,
            SafeguardRelationship.target_safeguard_id == relationship.source_safeguard_id
        )
    ).first()
    
    if reverse_rel:
        session.delete(reverse_rel)
    
    session.delete(relationship)
    session.commit()
    return None

def _get_reverse_relationship_type(relationship_type: SafeguardRelationshipType) -> SafeguardRelationshipType:
    """Get the reverse relationship type"""
    if relationship_type == SafeguardRelationshipType.SUPERSET:
        return SafeguardRelationshipType.SUBSET
    elif relationship_type == SafeguardRelationshipType.SUBSET:
        return SafeguardRelationshipType.SUPERSET
    else:  # EQUIVALENT
        return SafeguardRelationshipType.EQUIVALENT
