from sqlmodel import Session, select
from .models import ControlSafeguard
from typing import List, Optional

def get_safeguard(session: Session, safeguard_id: str) -> Optional[ControlSafeguard]:
    safeguard = session.get(ControlSafeguard, safeguard_id)
    if safeguard:
        # Force load relationships
        if safeguard.control_id:
            _ = safeguard.control  # This will trigger the relationship load
            if safeguard.control and safeguard.control.framework_id:
                _ = safeguard.control.framework  # Load the framework too
        if safeguard.function_id:
            _ = safeguard.function  # This will trigger the relationship load
        if safeguard.implementation_group_id:
            _ = safeguard.implementation_group  # This will trigger the relationship load
        if safeguard.asset_class_id:
            _ = safeguard.asset_class  # This will trigger the relationship load
    return safeguard

def get_safeguards(session: Session, skip: int = 0, limit: int = 100) -> List[ControlSafeguard]:
    # Use select to get safeguards with their relationships
    from sqlmodel import select
    
    statement = select(ControlSafeguard).offset(skip).limit(limit)
    safeguards = session.exec(statement).all()
    
    # Force load relationships for each safeguard
    for safeguard in safeguards:
        if safeguard.control_id:
            _ = safeguard.control  # This will trigger the relationship load
            if safeguard.control and safeguard.control.framework_id:
                _ = safeguard.control.framework  # Load the framework too
        if safeguard.function_id:
            _ = safeguard.function  # This will trigger the relationship load
        if safeguard.implementation_group_id:
            _ = safeguard.implementation_group  # This will trigger the relationship load
        if safeguard.asset_class_id:
            _ = safeguard.asset_class  # This will trigger the relationship load
    
    return list(safeguards)

def create_safeguard(session: Session, safeguard: ControlSafeguard) -> ControlSafeguard:
    session.add(safeguard)
    session.commit()
    session.refresh(safeguard)
    return safeguard

def update_safeguard(session: Session, db_safeguard: ControlSafeguard, updates: dict) -> ControlSafeguard:
    for key, value in updates.items():
        setattr(db_safeguard, key, value)
    session.add(db_safeguard)
    session.commit()
    session.refresh(db_safeguard)
    return db_safeguard

def delete_safeguard(session: Session, safeguard_id: str) -> None:
    db_safeguard = session.get(ControlSafeguard, safeguard_id)
    if db_safeguard:
        session.delete(db_safeguard)
        session.commit()
