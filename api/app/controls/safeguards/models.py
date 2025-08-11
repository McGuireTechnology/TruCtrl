# Safeguards (sub-controls, actions, etc.)

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from ...utils import ulid_factory
from ..models import Control
from typing import TYPE_CHECKING
from enum import Enum

if TYPE_CHECKING:
    from ..functions.models import ControlFunction
    from ..implementation_groups.models import ControlImplementationGroup
    from ..asset_classes.models import ControlAssetClass

EXAMPLE = "Establish and Maintain Detailed Enterprise Asset Inventory"

# Enum for safeguard relationship types
class SafeguardRelationshipType(str, Enum):
    SUPERSET = "superset"      # Source safeguard covers more than target
    EQUIVALENT = "equivalent"  # Source and target safeguards are equivalent
    SUBSET = "subset"         # Source safeguard covers less than target

# Safeguard-to-safeguard relationship mapping table
class SafeguardRelationship(SQLModel, table=True):
    id: str = Field(default_factory=ulid_factory, primary_key=True)
    source_safeguard_id: str = Field(foreign_key="controlsafeguard.id")
    target_safeguard_id: str = Field(foreign_key="controlsafeguard.id")
    relationship_type: SafeguardRelationshipType = Field(index=True)
    confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="Confidence level of the mapping (0.0 to 1.0)")
    notes: Optional[str] = Field(default=None, description="Additional notes about this relationship")
    created_by: Optional[str] = Field(default=None, description="User who created this mapping")
    
    # Relationships
    source_safeguard: "ControlSafeguard" = Relationship(
        back_populates="outbound_relationships",
        sa_relationship_kwargs={"foreign_keys": "[SafeguardRelationship.source_safeguard_id]"}
    )
    target_safeguard: "ControlSafeguard" = Relationship(
        back_populates="inbound_relationships", 
        sa_relationship_kwargs={"foreign_keys": "[SafeguardRelationship.target_safeguard_id]"}
    )

class ControlSafeguard(SQLModel, table=True):
    id: str = Field(default_factory=ulid_factory, primary_key=True, index=True)
    control_id: Optional[str] = Field(default=None, foreign_key="control.id")
    function_id: Optional[str] = Field(default=None, foreign_key="controlfunction.id")
    implementation_group_id: Optional[str] = Field(default=None, foreign_key="controlimplementationgroup.id")
    asset_class_id: Optional[str] = Field(default=None, foreign_key="controlassetclass.id")
    name: str = EXAMPLE
    short_name: Optional[str] = None
    description: Optional[str] = None
    
    # Relationships to other entities
    control: Optional[Control] = Relationship(back_populates="safeguards")
    function: Optional["ControlFunction"] = Relationship(back_populates="safeguards")
    implementation_group: Optional["ControlImplementationGroup"] = Relationship(back_populates="safeguards")
    asset_class: Optional["ControlAssetClass"] = Relationship(back_populates="safeguards")
    
    # Safeguard-to-safeguard relationships
    outbound_relationships: List[SafeguardRelationship] = Relationship(
        back_populates="source_safeguard",
        sa_relationship_kwargs={"foreign_keys": "[SafeguardRelationship.source_safeguard_id]"}
    )
    inbound_relationships: List[SafeguardRelationship] = Relationship(
        back_populates="target_safeguard",
        sa_relationship_kwargs={"foreign_keys": "[SafeguardRelationship.target_safeguard_id]"}
    )

class ControlSafeguardBase(SQLModel):
    name: str
    short_name: Optional[str] = None
    description: Optional[str] = None
    control_id: Optional[str] = None
    function_id: Optional[str] = None
    implementation_group_id: Optional[str] = None
    asset_class_id: Optional[str] = None

class ControlSafeguardCreate(ControlSafeguardBase):
    pass

class ControlSafeguardRead(ControlSafeguardBase):
    id: str

class ControlSafeguardUpdate(SQLModel):
    name: Optional[str] = None
    short_name: Optional[str] = None
    description: Optional[str] = None
    control_id: Optional[str] = None
    function_id: Optional[str] = None
    implementation_group_id: Optional[str] = None
    asset_class_id: Optional[str] = None

# API Response Models
class ControlSafeguardStub(SQLModel):
    id: str
    name: str
    short_name: Optional[str] = None

class ControlSafeguardPublic(SQLModel):
    id: str
    name: str
    short_name: Optional[str] = None
    description: Optional[str] = None
    control_id: Optional[str] = None
    function_id: Optional[str] = None
    implementation_group_id: Optional[str] = None
    asset_class_id: Optional[str] = None
    
    # Related object names for display
    control_name: Optional[str] = None
    control_short_name: Optional[str] = None
    control_color: Optional[str] = None
    function_name: Optional[str] = None
    function_short_name: Optional[str] = None
    function_color: Optional[str] = None
    implementation_group_name: Optional[str] = None
    implementation_group_short_name: Optional[str] = None
    implementation_group_color: Optional[str] = None
    asset_class_name: Optional[str] = None
    asset_class_short_name: Optional[str] = None
    asset_class_color: Optional[str] = None
    framework_name: Optional[str] = None  # Derived from control's framework
    framework_short_name: Optional[str] = None  # Derived from control's framework
    framework_color: Optional[str] = None  # Derived from control's framework

class ControlSafeguardsPublic(SQLModel):
    data: List[ControlSafeguardPublic]
    count: int

# Safeguard Relationship API Models
class SafeguardRelationshipCreate(SQLModel):
    target_safeguard_id: str = Field(description="ID of the target safeguard")
    relationship_type: SafeguardRelationshipType = Field(description="Type of relationship")
    confidence: float = Field(default=1.0, ge=0.0, le=1.0, description="Confidence level (0.0 to 1.0)")
    notes: Optional[str] = Field(default=None, description="Additional notes about this relationship")

class SafeguardRelationshipUpdate(SQLModel):
    relationship_type: Optional[SafeguardRelationshipType] = Field(default=None, description="Type of relationship")
    confidence: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Confidence level (0.0 to 1.0)")
    notes: Optional[str] = Field(default=None, description="Additional notes about this relationship")

class SafeguardRelationshipPublic(SQLModel):
    id: str
    source_safeguard_id: str
    target_safeguard_id: str
    relationship_type: SafeguardRelationshipType
    confidence: float
    notes: Optional[str] = None
    created_by: Optional[str] = None
    
    # Include target safeguard details for display
    target_safeguard_name: Optional[str] = None
    target_safeguard_short_name: Optional[str] = None
    target_framework_name: Optional[str] = None
    target_framework_short_name: Optional[str] = None

class SafeguardRelationshipsPublic(SQLModel):
    data: List[SafeguardRelationshipPublic]
    count: int

# Enhanced ControlSafeguardPublic with relationships
class ControlSafeguardWithRelationships(ControlSafeguardPublic):
    # Include relationship data
    outbound_relationships: List[SafeguardRelationshipPublic] = []
    inbound_relationships: List[SafeguardRelationshipPublic] = []
