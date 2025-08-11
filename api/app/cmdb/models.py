# CMDB Core Models

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List, Dict, Any, TYPE_CHECKING
from ..utils import ulid_factory
from datetime import datetime
from enum import Enum

if TYPE_CHECKING:
    from .configuration_item_types.models import ConfigurationItemType
    from ..controls.models import Control

class CIStatus(str, Enum):
    """Configuration Item Status"""
    ACTIVE = "active"
    INACTIVE = "inactive"
    DECOMMISSIONED = "decommissioned"
    PLANNED = "planned"
    UNDER_MAINTENANCE = "under_maintenance"

class CIEnvironment(str, Enum):
    """Configuration Item Environment"""
    PRODUCTION = "production"
    STAGING = "staging"
    DEVELOPMENT = "development"
    TEST = "test"
    DR = "disaster_recovery"

# Many-to-many relationship table for CI hierarchies
class CIRelationship(SQLModel, table=True):
    parent_id: str = Field(foreign_key="configurationitem.id", primary_key=True)
    child_id: str = Field(foreign_key="configurationitem.id", primary_key=True)
    relationship_type: str = Field(default="contains", description="Type of relationship (contains, depends_on, etc.)")
    created_at: datetime = Field(default_factory=datetime.utcnow)

# Core Configuration Item Model
class ConfigurationItem(SQLModel, table=True):
    """
    Root table for all Configuration Items in the CMDB.
    This table stores common attributes for all CIs.
    Specific CI types extend this through ci_* prefixed tables.
    """
    id: str = Field(default_factory=ulid_factory, primary_key=True, index=True)
    ci_type_id: str = Field(foreign_key="configurationitemtype.id", index=True)
    name: str = Field(index=True, description="Configuration item name")
    description: Optional[str] = Field(default=None, description="Configuration item description")
    
    # Status and lifecycle
    status: CIStatus = Field(default=CIStatus.ACTIVE, description="Current status of the CI")
    environment: Optional[CIEnvironment] = Field(default=None, description="Environment this CI belongs to")
    
    # Ownership and responsibility
    owner: Optional[str] = Field(default=None, description="Primary owner/responsible party")
    business_service: Optional[str] = Field(default=None, description="Business service this CI supports")
    
    # Location and physical attributes
    location: Optional[str] = Field(default=None, description="Physical or logical location")
    
    # Financial attributes
    cost_center: Optional[str] = Field(default=None, description="Cost center responsible for this CI")
    purchase_cost: Optional[float] = Field(default=None, description="Initial purchase cost")
    annual_cost: Optional[float] = Field(default=None, description="Annual operating cost")
    
    # Timestamps
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
    discovered_at: Optional[datetime] = Field(default=None, description="When this CI was first discovered")
    last_seen: Optional[datetime] = Field(default=None, description="When this CI was last seen/verified")
    
    # Custom attributes (JSON field for flexibility)
    attributes: Optional[Dict[str, Any]] = Field(default=None, description="Custom attributes specific to CI type")
    
    # Relationships
    ci_type: "ConfigurationItemType" = Relationship(back_populates="configuration_items")
    
    # Self-referential relationships for CI hierarchies
    parent_relationships: List["CIRelationship"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[CIRelationship.child_id]"}
    )
    child_relationships: List["CIRelationship"] = Relationship(
        sa_relationship_kwargs={"foreign_keys": "[CIRelationship.parent_id]"}
    )

# API Request Models
class ConfigurationItemCreate(SQLModel):
    ci_type_id: str = Field(description="Configuration item type ID")
    name: str = Field(description="Configuration item name")
    description: Optional[str] = Field(default=None, description="Configuration item description")
    status: CIStatus = Field(default=CIStatus.ACTIVE, description="Current status of the CI")
    environment: Optional[CIEnvironment] = Field(default=None, description="Environment this CI belongs to")
    owner: Optional[str] = Field(default=None, description="Primary owner/responsible party")
    business_service: Optional[str] = Field(default=None, description="Business service this CI supports")
    location: Optional[str] = Field(default=None, description="Physical or logical location")
    cost_center: Optional[str] = Field(default=None, description="Cost center responsible for this CI")
    purchase_cost: Optional[float] = Field(default=None, description="Initial purchase cost")
    annual_cost: Optional[float] = Field(default=None, description="Annual operating cost")
    attributes: Optional[Dict[str, Any]] = Field(default=None, description="Custom attributes specific to CI type")

class ConfigurationItemUpdate(SQLModel):
    ci_type_id: Optional[str] = Field(default=None, description="Configuration item type ID")
    name: Optional[str] = Field(default=None, description="Configuration item name")
    description: Optional[str] = Field(default=None, description="Configuration item description")
    status: Optional[CIStatus] = Field(default=None, description="Current status of the CI")
    environment: Optional[CIEnvironment] = Field(default=None, description="Environment this CI belongs to")
    owner: Optional[str] = Field(default=None, description="Primary owner/responsible party")
    business_service: Optional[str] = Field(default=None, description="Business service this CI supports")
    location: Optional[str] = Field(default=None, description="Physical or logical location")
    cost_center: Optional[str] = Field(default=None, description="Cost center responsible for this CI")
    purchase_cost: Optional[float] = Field(default=None, description="Initial purchase cost")
    annual_cost: Optional[float] = Field(default=None, description="Annual operating cost")
    attributes: Optional[Dict[str, Any]] = Field(default=None, description="Custom attributes specific to CI type")

# API Response Models
class ConfigurationItemStub(SQLModel):
    id: str
    name: str
    status: CIStatus
    environment: Optional[CIEnvironment] = None

class ConfigurationItemPublic(SQLModel):
    id: str
    ci_type_id: str
    name: str
    description: Optional[str] = None
    status: CIStatus
    environment: Optional[CIEnvironment] = None
    owner: Optional[str] = None
    business_service: Optional[str] = None
    location: Optional[str] = None
    cost_center: Optional[str] = None
    purchase_cost: Optional[float] = None
    annual_cost: Optional[float] = None
    created_at: datetime
    updated_at: datetime
    discovered_at: Optional[datetime] = None
    last_seen: Optional[datetime] = None
    attributes: Optional[Dict[str, Any]] = None
    
    # Include parent and child relationships in the response
    parents: Optional[List["ConfigurationItemStub"]] = None
    children: Optional[List["ConfigurationItemStub"]] = None

class ConfigurationItemsPublic(SQLModel):
    data: List[ConfigurationItemPublic]
