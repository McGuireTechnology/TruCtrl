# Asset Classes within a control framework (e.g., Devices, Software, Data, Users, Network, Documentation)

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from ...utils import ulid_factory
from ..models import Control, ControlStub

if TYPE_CHECKING:
    from ..safeguards.models import ControlSafeguard
    from ..frameworks.models import ControlFramework

# Many-to-many relationship table for asset class hierarchies
class AssetClassRelationship(SQLModel, table=True):
    parent_id: str = Field(foreign_key="controlassetclass.id", primary_key=True)
    child_id: str = Field(foreign_key="controlassetclass.id", primary_key=True)

# Examples
EXAMPLE = "Devices"

# Database Model
class ControlAssetClass(SQLModel, table=True):
    id: str = Field(default_factory=ulid_factory, primary_key=True, index=True)
    framework_id: Optional[str] = Field(default=None, foreign_key="controlframework.id")
    name: str = Field(index=True, description="Asset class name")
    short_name: Optional[str] = Field(default=None, index=True, description="Asset class short name or abbreviation")
    description: Optional[str] = Field(default=None, description="Asset class description")
    color: str = Field(default="#17a2b8", description="Display color for the asset class")
    locked: bool = Field(default=False, description="Whether the asset class is locked from modification")
    
    # Framework relationship
    framework: Optional["ControlFramework"] = Relationship(back_populates="asset_classes")
    
    # Standard relationship with controls
    controls: List["Control"] = Relationship(back_populates="asset_class")
    
    # Relationship with safeguards
    safeguards: List["ControlSafeguard"] = Relationship(back_populates="asset_class")
    
    # Many-to-many relationships for asset class hierarchies (for CIS Controls modeling)
    # These will be managed through separate API endpoints for adding/removing relationships
    parent_relationships: List["AssetClassRelationship"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[AssetClassRelationship.child_id]"}
    )
    child_relationships: List["AssetClassRelationship"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[AssetClassRelationship.parent_id]"}
    )

# API Request Models
class ControlAssetClassCreate(SQLModel):
    framework_id: Optional[str] = Field(default=None, description="Framework ID this asset class belongs to")
    name: str = Field(description="Asset class name")
    short_name: Optional[str] = Field(default=None, description="Asset class short name or abbreviation")
    description: Optional[str] = Field(default=None, description="Asset class description")
    color: str = Field(default="#17a2b8", description="Display color for the asset class")
    locked: bool = Field(default=False, description="Whether the asset class is locked from modification")

class ControlAssetClassUpdate(SQLModel):
    framework_id: Optional[str] = Field(default=None, description="Framework ID this asset class belongs to")
    name: Optional[str] = Field(default=None, description="Asset class name")
    short_name: Optional[str] = Field(default=None, description="Asset class short name or abbreviation")
    description: Optional[str] = Field(default=None, description="Asset class description")
    color: Optional[str] = Field(default=None, description="Display color for the asset class")
    locked: Optional[bool] = Field(default=None, description="Whether the asset class is locked from modification")

# API Response Models
class ControlAssetClassStub(SQLModel):
    id: str
    name: str
    short_name: Optional[str] = None
    color: str
    locked: bool = False

class ControlAssetClassPublic(SQLModel):
    id: str
    name: str
    short_name: Optional[str] = None
    description: Optional[str] = None
    color: str
    locked: bool = False
    
    # Include parent and child relationships in the response
    parents: Optional[List["ControlAssetClassStub"]] = None
    children: Optional[List["ControlAssetClassStub"]] = None

class ControlAssetClassesPublic(SQLModel):
    data: List[ControlAssetClassPublic]
