from sqlmodel import Session, select
from .models import ControlImplementationGroup
from typing import List, Optional

def get_implementation_group(session: Session, group_id: str) -> Optional[ControlImplementationGroup]:
    return session.get(ControlImplementationGroup, group_id)

def get_implementation_groups(session: Session, skip: int = 0, limit: int = 100) -> List[ControlImplementationGroup]:
    return session.exec(select(ControlImplementationGroup).offset(skip).limit(limit)).all()

def create_implementation_group(session: Session, group: ControlImplementationGroup) -> ControlImplementationGroup:
    session.add(group)
    session.commit()
    session.refresh(group)
    return group

def update_implementation_group(session: Session, db_group: ControlImplementationGroup, updates: dict) -> ControlImplementationGroup:
    for key, value in updates.items():
        setattr(db_group, key, value)
    session.add(db_group)
    session.commit()
    session.refresh(db_group)
    return db_group

def delete_implementation_group(session: Session, group_id: str) -> None:
    db_group = session.get(ControlImplementationGroup, group_id)
    if db_group:
        session.delete(db_group)
        session.commit()
