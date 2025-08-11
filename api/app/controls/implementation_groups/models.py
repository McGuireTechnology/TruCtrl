# Implementation Groups (e.g., IG1, IG2, IG3)

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from ...utils import ulid_factory
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from ..frameworks.models import ControlFramework
    from ..safeguards.models import ControlSafeguard

# Examples
EXAMPLE = "IG1"

# Database Model
class ControlImplementationGroup(SQLModel, table=True):
    id: str = Field(default_factory=ulid_factory, primary_key=True, index=True)
    framework_id: Optional[str] = Field(default=None, foreign_key="controlframework.id")
    name: str = EXAMPLE
    short_name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = Field(default="#ffc107", description="Hex color code for UI display")
    framework: Optional["ControlFramework"] = Relationship(back_populates="implementation_groups")
    safeguards: List["ControlSafeguard"] = Relationship(back_populates="implementation_group")

# API Request Models
class ControlImplementationGroupCreate(SQLModel):
    name: str
    short_name: Optional[str] = None
    description: Optional[str] = None
    framework_id: Optional[str] = None
    color: Optional[str] = Field(default="#ffc107", description="Hex color code for UI display")

class ControlImplementationGroupUpdate(SQLModel):
    name: Optional[str] = None
    short_name: Optional[str] = None
    description: Optional[str] = None
    framework_id: Optional[str] = None
    color: Optional[str] = None

# API Response Models
class ControlImplementationGroupStub(SQLModel):
    id: str
    name: str
    short_name: Optional[str] = None
    color: Optional[str] = None

class ControlImplementationGroupPublic(SQLModel):
    id: str
    name: str
    short_name: Optional[str] = None
    description: Optional[str] = None
    framework_id: Optional[str] = None
    color: Optional[str] = None

class ControlImplementationGroupsPublic(SQLModel):
    data: List[ControlImplementationGroupPublic]
    count: int
