from sqlmodel import Session, select
from .models import ControlFramework
from typing import List, Optional

def get_framework(session: Session, framework_id: str) -> Optional[ControlFramework]:
    return session.get(ControlFramework, framework_id)

def get_frameworks(session: Session, skip: int = 0, limit: int = 100) -> List[ControlFramework]:
    return session.exec(select(ControlFramework).offset(skip).limit(limit)).all()

def create_framework(session: Session, framework: ControlFramework) -> ControlFramework:
    session.add(framework)
    session.commit()
    session.refresh(framework)
    return framework

def update_framework(session: Session, db_framework: ControlFramework, updates: dict) -> ControlFramework:
    for key, value in updates.items():
        setattr(db_framework, key, value)
    session.add(db_framework)
    session.commit()
    session.refresh(db_framework)
    return db_framework

def delete_framework(session: Session, framework_id: str) -> None:
    db_framework = session.get(ControlFramework, framework_id)
    if db_framework:
        session.delete(db_framework)
        session.commit()
