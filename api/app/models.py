from pydantic import EmailStr
from sqlmodel import SQLModel, Field
from typing import Optional
from .utils import ulid_factory
from .controls import Control, ControlSafeguard, ControlFramework, ControlImplementationGroup

PASSWORD_MIN_LENGTH = 8

# Examples
EXAMPLE_USER_ID = "01JZQ0YQ8YQ2Z4K7Q2JQ0YQ8YQ"
EXAMPLE_USER = "John Smith"
EXAMPLE_USER_EMAIL = "jsmith@tructrl.app"
EXAMPLE_USER_PASSWORD = "MyS3cretP@ssw0rd!"
EXAMPLE_USER_IS_ACTIVE = True

# Database Model
class User(SQLModel, table=True):
    id: str = Field(default_factory=ulid_factory, primary_key=True, index=True)
    name: str
    email: EmailStr = Field(unique=True, index=True)
    password: str
    is_active: bool = False

# API Request Models
class UserCreate(SQLModel):
    name: str = EXAMPLE_USER
    email: EmailStr = EXAMPLE_USER_EMAIL
    password: str = EXAMPLE_USER_PASSWORD
    is_active: Optional[bool] = EXAMPLE_USER_IS_ACTIVE

class UserUpdate(SQLModel):
    name: Optional[str] = EXAMPLE_USER
    email: Optional[EmailStr] = EXAMPLE_USER_EMAIL
    password: Optional[str] = Field(EXAMPLE_USER_PASSWORD, min_length=PASSWORD_MIN_LENGTH)
    is_active: Optional[bool] = EXAMPLE_USER_IS_ACTIVE

# API Response Models
class UserStub(SQLModel):
    id: str = EXAMPLE_USER_ID
    name: str = EXAMPLE_USER

class UserPublic(SQLModel):
    id: str = EXAMPLE_USER_ID
    name: str = EXAMPLE_USER
    email: EmailStr = EXAMPLE_USER_EMAIL
    is_active: bool = EXAMPLE_USER_IS_ACTIVE

class UsersPublic(SQLModel):
    data: list[UserPublic]
    count: int

# Authentication Models
class UserLogin(SQLModel):
    email: EmailStr = EXAMPLE_USER_EMAIL
    password: str = EXAMPLE_USER_PASSWORD

class Token(SQLModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"
    expires_in: int

class TokenData(SQLModel):
    email: Optional[str] = None
    user_id: Optional[str] = None

class RefreshToken(SQLModel):
    refresh_token: str