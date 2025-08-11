
from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session
from typing import List
from . import crud, models, deps

from .controls.routes import router as controls_router
from .auth import router as auth_router
from .cmdb.routes import router as cmdb_router

api_router = APIRouter()

users_router = APIRouter(prefix="/users", tags=["Users"])

@users_router.post("/", response_model=models.UserPublic, status_code=status.HTTP_201_CREATED)
def create_user(
    user_in: models.UserCreate, 
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
):
    existing = crud.get_user_by_email(db, user_in.email)
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")
    user = crud.create_user(db, user_in)
    return models.UserPublic.from_orm(user)

@users_router.get("/", response_model=models.UsersPublic)
def list_users(
    skip: int = 0, 
    limit: int = 100, 
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
):
    users = crud.list_users(db, skip=skip, limit=limit)
    return models.UsersPublic(data=[models.UserPublic.from_orm(u) for u in users], count=len(users))

@users_router.get("/{id}", response_model=models.UserPublic)
def get_user(
    id: str, 
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
):
    user = crud.get_user(db, id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return models.UserPublic.from_orm(user)

@users_router.patch("/{id}", response_model=models.UserPublic)
def update_user(
    id: str, 
    user_in: models.UserUpdate, 
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
):
    user = crud.update_user(db, id, user_in)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return models.UserPublic.from_orm(user)

@users_router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_user(
    id: str, 
    db: Session = Depends(deps.get_db),
    current_user: models.User = Depends(deps.get_current_active_user)
):
    ok = crud.delete_user(db, id)
    if not ok:
        raise HTTPException(status_code=404, detail="User not found")

# Register all routers
api_router.include_router(auth_router)
api_router.include_router(controls_router)
api_router.include_router(cmdb_router, prefix="/cmdb", tags=["CMDB"])
api_router.include_router(users_router)
