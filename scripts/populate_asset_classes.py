#!/usr/bin/env python3
"""
Script to populate default asset classes.
"""

import sys
import os
from typing import Optional

# Add the api directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', 'api'))

from sqlmodel import Session, create_engine, SQLModel, Field

# Simple model definition for this script
class ControlAssetClass(SQLModel, table=True):
    id: str = Field(primary_key=True)
    name: str
    short_name: Optional[str] = None
    description: Optional[str] = None
    color: str = "#17a2b8"

# Database URL
DATABASE_URL = "sqlite:///tructrl.db"
engine = create_engine(DATABASE_URL)

def create_default_asset_classes():
    """Create default asset classes."""
    
    default_asset_classes = [
        {
            "id": "physical",
            "name": "Physical Controls",
            "short_name": "PHYS",
            "description": "Controls related to physical security and access",
            "color": "#e74c3c"
        },
        {
            "id": "technical",
            "name": "Technical Controls",
            "short_name": "TECH",
            "description": "Controls implemented through technology and systems",
            "color": "#3498db"
        },
        {
            "id": "administrative", 
            "name": "Administrative Controls",
            "short_name": "ADMIN",
            "description": "Controls related to policies, procedures, and governance",
            "color": "#2ecc71"
        },
        {
            "id": "detective",
            "name": "Detective Controls",
            "short_name": "DET",
            "description": "Controls that detect and identify security incidents",
            "color": "#f39c12"
        },
        {
            "id": "preventive",
            "name": "Preventive Controls",
            "short_name": "PREV",
            "description": "Controls that prevent security incidents from occurring",
            "color": "#9b59b6"
        },
        {
            "id": "corrective",
            "name": "Corrective Controls",
            "short_name": "CORR",
            "description": "Controls that correct identified security issues",
            "color": "#e67e22"
        }
    ]
    
    with Session(engine) as session:
        for asset_class_data in default_asset_classes:
            # Check if asset class already exists
            existing = session.get(ControlAssetClass, asset_class_data["id"])
            if not existing:
                asset_class = ControlAssetClass(**asset_class_data)
                session.add(asset_class)
                print(f"Created asset class: {asset_class.name}")
            else:
                print(f"Asset class already exists: {existing.name}")
        
        session.commit()
        print("Default asset classes created successfully!")

if __name__ == "__main__":
    create_default_asset_classes()
