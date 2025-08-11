

# Controls API router
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session
from ..db import get_session
from .. import models, deps
from .models import Control, ControlCreate, ControlUpdate, ControlPublic, ControlListPublic
from .crud import get_control, get_controls, create_control, update_control, delete_control
from .implementation_groups.routes import router as implementation_groups_router
from .safeguards.routes import router as safeguards_router
from .frameworks.routes import router as frameworks_router
from .functions.routes import router as functions_router
from .asset_classes.routes import router as asset_classes_router

controls_router = APIRouter(prefix="", tags=["Controls"])

@controls_router.get("/", response_model=ControlListPublic)
def list_controls(
    skip: int = 0, 
    limit: int = 100, 
    session: Session = Depends(get_session),
    current_user: Annotated[models.User, Depends(deps.get_current_active_user)] = None
):
    controls = get_controls(session, skip=skip, limit=limit)
    return {"data": controls, "count": len(controls)}

@controls_router.get("/{id}", response_model=ControlPublic)
def read_control(
    id: str, 
    session: Session = Depends(get_session),
    current_user: Annotated[models.User, Depends(deps.get_current_active_user)] = None
):
    control = get_control(session, id)
    if not control:
        raise HTTPException(status_code=404, detail="Control not found")
    return control

@controls_router.post("/", response_model=ControlPublic)
def create_control_route(
    control: ControlCreate, 
    session: Session = Depends(get_session),
    current_user: Annotated[models.User, Depends(deps.get_current_active_user)] = None
):
    db_control = Control.from_orm(control)
    return create_control(session, db_control)

@controls_router.patch("/{id}", response_model=ControlPublic)
def update_control_route(
    id: str, 
    updates: ControlUpdate, 
    session: Session = Depends(get_session),
    current_user: Annotated[models.User, Depends(deps.get_current_active_user)] = None
):
    db_control = get_control(session, id)
    if not db_control:
        raise HTTPException(status_code=404, detail="Control not found")
    return update_control(session, db_control, updates.dict(exclude_unset=True))

@controls_router.delete("/{id}", status_code=204)
def delete_control_route(
    id: str, 
    session: Session = Depends(get_session),
    current_user: Annotated[models.User, Depends(deps.get_current_active_user)] = None
):
    delete_control(session, id)
    return None


router = APIRouter(prefix="/controls")

# Include sub-routers
router.include_router(controls_router)
router.include_router(frameworks_router)
router.include_router(implementation_groups_router)
router.include_router(safeguards_router)
router.include_router(functions_router)
router.include_router(asset_classes_router, prefix="/asset-classes", tags=["Asset Classes"])
