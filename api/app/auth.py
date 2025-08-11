from typing import Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlmodel import Session
from . import crud, models, security, deps

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=models.Token)
async def login_for_access_token(
    form_data: Annotated[OAuth2PasswordRequestForm, Depends()],
    db: Session = Depends(deps.get_db)
):
    """
    OAuth2 compatible token login, get an access token for future requests.
    """
    user = security.authenticate_user(db, form_data.username, form_data.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    tokens = security.create_user_tokens(user)
    return tokens

@router.post("/login/json", response_model=models.Token)
async def login_json(
    user_credentials: models.UserLogin,
    db: Session = Depends(deps.get_db)
):
    """
    JSON login endpoint for frontend applications.
    """
    user = security.authenticate_user(db, user_credentials.email, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Inactive user"
        )
    
    tokens = security.create_user_tokens(user)
    return tokens

@router.post("/refresh", response_model=models.Token)
async def refresh_token(
    refresh_data: models.RefreshToken,
    db: Session = Depends(deps.get_db)
):
    """
    Refresh an access token using a refresh token.
    """
    try:
        payload = security.verify_token(refresh_data.refresh_token, token_type="refresh")
        email: str = payload.get("sub")
        user_id: str = payload.get("user_id")
        
        if email is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        user = crud.get_user_by_email(db, email)
        if user is None or not user.is_active:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate credentials",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        tokens = security.create_user_tokens(user)
        return tokens
        
    except Exception:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

@router.post("/register", response_model=models.UserPublic, status_code=status.HTTP_201_CREATED)
async def register(
    user_in: models.UserCreate,
    db: Session = Depends(deps.get_db)
):
    """
    Create a new user account.
    """
    existing_user = crud.get_user_by_email(db, user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The user with this email already exists in the system"
        )
    
    user = crud.create_user(db, user_in)
    return models.UserPublic.from_orm(user)

@router.get("/me", response_model=models.UserPublic)
async def read_users_me(
    current_user: Annotated[models.User, Depends(deps.get_current_active_user)]
):
    """
    Get current user information.
    """
    return models.UserPublic.from_orm(current_user)

@router.patch("/me", response_model=models.UserPublic)
async def update_user_me(
    user_in: models.UserUpdate,
    current_user: Annotated[models.User, Depends(deps.get_current_active_user)],
    db: Session = Depends(deps.get_db)
):
    """
    Update current user information.
    """
    user = crud.update_user(db, current_user.id, user_in)
    return models.UserPublic.from_orm(user)
