from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ...db import get_session
from ... import models, deps
from .models import ControlImplementationGroup, ControlImplementationGroupCreate, ControlImplementationGroupUpdate, ControlImplementationGroupPublic, ControlImplementationGroupsPublic
from .crud import get_implementation_group, get_implementation_groups, create_implementation_group, update_implementation_group, delete_implementation_group
from typing import List

router = APIRouter(prefix="/implementation-groups", tags=["Control Implementation Groups"])

@router.get("/", response_model=ControlImplementationGroupsPublic)
def list_implementation_groups(
    skip: int = 0, 
    limit: int = 100, 
    session: Session = Depends(get_session),
    current_user: Annotated[models.User, Depends(deps.get_current_active_user)] = None
):
    groups = get_implementation_groups(session, skip=skip, limit=limit)
    return {"data": groups, "count": len(groups)}

@router.get("/{id}", response_model=ControlImplementationGroupPublic)
def read_implementation_group(
    id: str, 
    session: Session = Depends(get_session),
    current_user: Annotated[models.User, Depends(deps.get_current_active_user)] = None
):
    group = get_implementation_group(session, id)
    if not group:
        raise HTTPException(status_code=404, detail="Implementation Group not found")
    return group

@router.post("/", response_model=ControlImplementationGroupPublic)
def create_implementation_group_route(
    group: ControlImplementationGroupCreate, 
    session: Session = Depends(get_session),
    current_user: Annotated[models.User, Depends(deps.get_current_active_user)] = None
):
    db_group = ControlImplementationGroup.from_orm(group)
    return create_implementation_group(session, db_group)

@router.patch("/{id}", response_model=ControlImplementationGroupPublic)
def update_implementation_group_route(
    id: str, 
    updates: ControlImplementationGroupUpdate, 
    session: Session = Depends(get_session),
    current_user: Annotated[models.User, Depends(deps.get_current_active_user)] = None
):
    db_group = get_implementation_group(session, id)
    if not db_group:
        raise HTTPException(status_code=404, detail="Implementation Group not found")
    return update_implementation_group(session, db_group, updates.dict(exclude_unset=True))

@router.delete("/{id}", status_code=204)
def delete_implementation_group_route(
    id: str, 
    session: Session = Depends(get_session),
    current_user: Annotated[models.User, Depends(deps.get_current_active_user)] = None
):
    delete_implementation_group(session, id)
    return None
