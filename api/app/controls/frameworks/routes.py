from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ...db import get_session
from ... import models, deps
from .models import ControlFramework, ControlFrameworkCreate, ControlFrameworkUpdate, ControlFrameworkPublic, ControlFrameworksPublic
from .crud import get_framework, get_frameworks, create_framework, update_framework, delete_framework
from typing import List

router = APIRouter(prefix="/frameworks", tags=["Control Frameworks"])

@router.get("/", response_model=ControlFrameworksPublic)
def list_frameworks(
    skip: int = 0, 
    limit: int = 100, 
    session: Session = Depends(get_session),
    current_user: Annotated[models.User, Depends(deps.get_current_active_user)] = None
):
    frameworks = get_frameworks(session, skip=skip, limit=limit)
    return {"data": frameworks, "count": len(frameworks)}

@router.get("/{id}", response_model=ControlFrameworkPublic)
def read_framework(
    id: str, 
    session: Session = Depends(get_session),
    current_user: Annotated[models.User, Depends(deps.get_current_active_user)] = None
):
    framework = get_framework(session, id)
    if not framework:
        raise HTTPException(status_code=404, detail="Framework not found")
    return framework

@router.post("/", response_model=ControlFrameworkPublic)
def create_framework_route(
    framework: ControlFrameworkCreate, 
    session: Session = Depends(get_session),
    current_user: Annotated[models.User, Depends(deps.get_current_active_user)] = None
):
    db_framework = ControlFramework.from_orm(framework)
    return create_framework(session, db_framework)

@router.patch("/{id}", response_model=ControlFrameworkPublic)
def update_framework_route(
    id: str, 
    updates: ControlFrameworkUpdate, 
    session: Session = Depends(get_session),
    current_user: Annotated[models.User, Depends(deps.get_current_active_user)] = None
):
    db_framework = get_framework(session, id)
    if not db_framework:
        raise HTTPException(status_code=404, detail="Framework not found")
    return update_framework(session, db_framework, updates.dict(exclude_unset=True))

@router.delete("/{id}", status_code=204)
def delete_framework_route(
    id: str, 
    session: Session = Depends(get_session),
    current_user: Annotated[models.User, Depends(deps.get_current_active_user)] = None
):
    delete_framework(session, id)
    return None
