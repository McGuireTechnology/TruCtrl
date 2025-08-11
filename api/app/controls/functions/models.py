# Security Functions within a control framework (e.g., Asset Management, Access Control, etc.)

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from ...utils import ulid_factory
from ..models import Control, ControlStub
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from ..safeguards.models import ControlSafeguard
    from ..frameworks.models import ControlFramework

# Examples
EXAMPLE = "Asset Management"

# Database Model
class ControlFunction(SQLModel, table=True):
    id: str = Field(default_factory=ulid_factory, primary_key=True, index=True)
    framework_id: Optional[str] = Field(default=None, foreign_key="controlframework.id")
    name: str = EXAMPLE
    short_name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = Field(default="#0d6efd", description="Hex color code for UI display")
    
    # Relationships
    framework: Optional["ControlFramework"] = Relationship(back_populates="functions")
    controls: List["Control"] = Relationship(back_populates="function")
    safeguards: List["ControlSafeguard"] = Relationship(back_populates="function")

# API Request Models
class ControlFunctionCreate(SQLModel):
    framework_id: Optional[str] = Field(default=None, description="Framework ID this function belongs to")
    name: str
    short_name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = Field(default="#0d6efd", description="Hex color code for UI display")

class ControlFunctionUpdate(SQLModel):
    framework_id: Optional[str] = Field(default=None, description="Framework ID this function belongs to")
    name: Optional[str] = None
    short_name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None

# API Response Models
class ControlFunctionStub(SQLModel):
    id: str
    name: str
    short_name: Optional[str] = None
    color: Optional[str] = None

class ControlFunctionPublic(SQLModel):
    id: str
    name: str
    short_name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    controls: List[ControlStub] = []

class ControlFunctionsPublic(SQLModel):
    data: List[ControlFunctionPublic]
    count: int
