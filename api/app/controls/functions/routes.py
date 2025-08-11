from typing import Annotated, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session
from ...db import get_session
from ... import models, deps
from .models import ControlFunction, ControlFunctionCreate, ControlFunctionUpdate, ControlFunctionPublic, ControlFunctionsPublic
from .crud import get_function, get_functions, create_function, update_function, delete_function

router = APIRouter(prefix="/functions", tags=["Control Functions"])

@router.get("/", response_model=ControlFunctionsPublic)
def list_functions(
    skip: int = 0, 
    limit: int = 100,
    session: Session = Depends(get_session),
    current_user: Optional[models.User] = Depends(deps.get_current_active_user)
):
    functions = get_functions(session, skip=skip, limit=limit)
    return {"data": list(functions), "count": len(functions)}

@router.get("/{id}", response_model=ControlFunctionPublic)
def read_function(
    id: str, 
    session: Session = Depends(get_session),
    current_user: Optional[models.User] = Depends(deps.get_current_active_user)
):
    function = get_function(session, id)
    if not function:
        raise HTTPException(status_code=404, detail="Function not found")
    return function

@router.post("/", response_model=ControlFunctionPublic)
def create_function_route(
    function: ControlFunctionCreate, 
    session: Session = Depends(get_session),
    current_user: Optional[models.User] = Depends(deps.get_current_active_user)
):
    db_function = ControlFunction.model_validate(function)
    return create_function(session, db_function)

@router.patch("/{id}", response_model=ControlFunctionPublic)
def update_function_route(
    id: str, 
    updates: ControlFunctionUpdate, 
    session: Session = Depends(get_session),
    current_user: Optional[models.User] = Depends(deps.get_current_active_user)
):
    db_function = get_function(session, id)
    if not db_function:
        raise HTTPException(status_code=404, detail="Function not found")
    
    update_dict = updates.model_dump(exclude_unset=True)
    return update_function(session, db_function, update_dict)

@router.delete("/{id}")
def delete_function_route(
    id: str, 
    session: Session = Depends(get_session),
    current_user: Optional[models.User] = Depends(deps.get_current_active_user)
):
    db_function = get_function(session, id)
    if not db_function:
        raise HTTPException(status_code=404, detail="Function not found")
    
    delete_function(session, id)
    return {"message": "Function deleted successfully"}
