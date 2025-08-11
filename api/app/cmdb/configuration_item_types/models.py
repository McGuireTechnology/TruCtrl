# Configuration Item Types Models (formerly Asset Classes)

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, TYPE_CHECKING
from ...utils import ulid_factory

if TYPE_CHECKING:
    from ..models import ConfigurationItem

# Many-to-many relationship table for CI type hierarchies
class CITypeRelationship(SQLModel, table=True):
    parent_id: str = Field(foreign_key="configurationitemtype.id", primary_key=True)
    child_id: str = Field(foreign_key="configurationitemtype.id", primary_key=True)

# Configuration Item Type Model (formerly ControlAssetClass)
class ConfigurationItemType(SQLModel, table=True):
    """
    Defines types of configuration items in the CMDB.
    This replaces the former ControlAssetClass and is no longer tied to control frameworks.
    """
    id: str = Field(default_factory=ulid_factory, primary_key=True, index=True)
    name: str = Field(index=True, description="Configuration item type name")
    short_name: Optional[str] = Field(default=None, index=True, description="Short name or abbreviation")
    description: Optional[str] = Field(default=None, description="Configuration item type description")
    color: str = Field(default="#17a2b8", description="Display color for the CI type")
    icon: Optional[str] = Field(default=None, description="Icon identifier for the CI type")
    locked: bool = Field(default=False, description="Whether the CI type is locked from modification")
    
    # Hierarchical relationships
    parent_relationships: List["CITypeRelationship"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[CITypeRelationship.child_id]"}
    )
    child_relationships: List["CITypeRelationship"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[CITypeRelationship.parent_id]"}
    )
    
    # Relationship with configuration items
    configuration_items: List["ConfigurationItem"] = Relationship(back_populates="ci_type")

# API Request Models
class ConfigurationItemTypeCreate(SQLModel):
    name: str = Field(description="Configuration item type name")
    short_name: Optional[str] = Field(default=None, description="Short name or abbreviation")
    description: Optional[str] = Field(default=None, description="Configuration item type description")
    color: str = Field(default="#17a2b8", description="Display color for the CI type")
    icon: Optional[str] = Field(default=None, description="Icon identifier for the CI type")
    locked: bool = Field(default=False, description="Whether the CI type is locked from modification")

class ConfigurationItemTypeUpdate(SQLModel):
    name: Optional[str] = Field(default=None, description="Configuration item type name")
    short_name: Optional[str] = Field(default=None, description="Short name or abbreviation")
    description: Optional[str] = Field(default=None, description="Configuration item type description")
    color: Optional[str] = Field(default=None, description="Display color for the CI type")
    icon: Optional[str] = Field(default=None, description="Icon identifier for the CI type")
    locked: Optional[bool] = Field(default=None, description="Whether the CI type is locked from modification")

# API Response Models
class ConfigurationItemTypeStub(SQLModel):
    id: str
    name: str
    short_name: Optional[str] = None
    color: str
    icon: Optional[str] = None
    locked: bool = False

class ConfigurationItemTypePublic(SQLModel):
    id: str
    name: str
    short_name: Optional[str] = None
    description: Optional[str] = None
    color: str
    icon: Optional[str] = None
    locked: bool = False
    
    # Include parent and child relationships in the response
    parents: Optional[List["ConfigurationItemTypeStub"]] = None
    children: Optional[List["ConfigurationItemTypeStub"]] = None

class ConfigurationItemTypesPublic(SQLModel):
    data: List[ConfigurationItemTypePublic]
