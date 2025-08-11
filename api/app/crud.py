
from typing import Optional, List
from sqlmodel import Session, select
from .models import User, UserCreate, UserUpdate
from . import security

def create_user(session: Session, user_in: UserCreate) -> User:
    # Hash the password before storing
    user_data = user_in.dict()
    user_data["password"] = security.get_password_hash(user_data["password"])
    user = User(**user_data)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def get_user(session: Session, user_id: str) -> Optional[User]:
    return session.get(User, user_id)

def get_user_by_email(session: Session, email: str) -> Optional[User]:
    statement = select(User).where(User.email == email)
    return session.exec(statement).first()

def list_users(session: Session, skip: int = 0, limit: int = 100) -> List[User]:
    statement = select(User).offset(skip).limit(limit)
    return session.exec(statement).all()

def update_user(session: Session, user_id: str, user_in: UserUpdate) -> Optional[User]:
    user = get_user(session, user_id)
    if not user:
        return None
    user_data = user_in.dict(exclude_unset=True)
    
    # Hash password if it's being updated
    if "password" in user_data:
        user_data["password"] = security.get_password_hash(user_data["password"])
    
    for key, value in user_data.items():
        setattr(user, key, value)
    session.add(user)
    session.commit()
    session.refresh(user)
    return user

def delete_user(session: Session, user_id: str) -> bool:
    user = get_user(session, user_id)
    if not user:
        return False
    session.delete(user)
    session.commit()
    return True
