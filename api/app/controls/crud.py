from sqlmodel import Session, select
from .models import Control
from typing import List, Optional

def get_control(session: Session, control_id: str) -> Optional[Control]:
    return session.get(Control, control_id)

def get_controls(session: Session, skip: int = 0, limit: int = 100) -> List[Control]:
    return session.exec(select(Control).offset(skip).limit(limit)).all()

def create_control(session: Session, control: Control) -> Control:
    session.add(control)
    session.commit()
    session.refresh(control)
    return control

def update_control(session: Session, db_control: Control, updates: dict) -> Control:
    for key, value in updates.items():
        setattr(db_control, key, value)
    session.add(db_control)
    session.commit()
    session.refresh(db_control)
    return db_control

def delete_control(session: Session, control_id: str) -> None:
    db_control = session.get(Control, control_id)
    if db_control:
        session.delete(db_control)
        session.commit()
