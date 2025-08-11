from sqlmodel import Session, select
from .models import ControlFunction
from typing import Optional, Sequence

def get_function(session: Session, function_id: str) -> Optional[ControlFunction]:
    return session.get(ControlFunction, function_id)

def get_functions(session: Session, skip: int = 0, limit: int = 100) -> Sequence[ControlFunction]:
    return session.exec(select(ControlFunction).offset(skip).limit(limit)).all()

def create_function(session: Session, function: ControlFunction) -> ControlFunction:
    session.add(function)
    session.commit()
    session.refresh(function)
    return function

def update_function(session: Session, db_function: ControlFunction, updates: dict) -> ControlFunction:
    for key, value in updates.items():
        setattr(db_function, key, value)
    session.add(db_function)
    session.commit()
    session.refresh(db_function)
    return db_function

def delete_function(session: Session, function_id: str) -> None:
    db_function = session.get(ControlFunction, function_id)
    if db_function:
        session.delete(db_function)
        session.commit()
