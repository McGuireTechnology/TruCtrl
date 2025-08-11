# Frameworks like CIS Controls, NIST, HIPAA, etc.

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from ...utils import ulid_factory
from ..models import Control, ControlStub
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..implementation_groups.models import ControlImplementationGroup
    from ..functions.models import ControlFunction
    from ..asset_classes.models import ControlAssetClass

# Examples
EXAMPLE = "CIS Controls"

# Database Model
class ControlFramework(SQLModel, table=True):
    id: str = Field(default_factory=ulid_factory, primary_key=True, index=True)
    name: str = EXAMPLE
    short_name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = Field(default="#198754", description="Hex color code for UI display")
    controls: List["Control"] = Relationship(back_populates="framework")
    implementation_groups: List["ControlImplementationGroup"] = Relationship(back_populates="framework")
    functions: List["ControlFunction"] = Relationship(back_populates="framework")
    asset_classes: List["ControlAssetClass"] = Relationship(back_populates="framework")

# API Request Models
class ControlFrameworkCreate(SQLModel):
    name: str
    short_name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = Field(default="#198754", description="Hex color code for UI display")

class ControlFrameworkUpdate(SQLModel):
    name: Optional[str] = None
    short_name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None

# API Response Models
class ControlFrameworkStub(SQLModel):
    id: str
    name: str
    short_name: Optional[str] = None
    color: Optional[str] = None

class ControlFrameworkPublic(SQLModel):
    id: str
    name: str
    short_name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = None
    controls: List[ControlStub] = []

class ControlFrameworksPublic(SQLModel):
    data: List[ControlFrameworkPublic]
    count: int

