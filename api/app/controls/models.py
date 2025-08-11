# Controls (e.g., CIS Control 1, NIST AC-1)

from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List
from ..utils import ulid_factory
from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from .frameworks.models import ControlFramework
    from .safeguards.models import ControlSafeguard
    from .functions.models import ControlFunction
    from .asset_classes.models import ControlAssetClass

# Examples
EXAMPLE = "Inventory and Control of Enterprise Assets"

# Database Model
class Control(SQLModel, table=True):
    id: str = Field(default_factory=ulid_factory, primary_key=True, index=True)
    framework_id: str = Field(foreign_key="controlframework.id")
    function_id: Optional[str] = Field(default=None, foreign_key="controlfunction.id")
    asset_class_id: Optional[str] = Field(default=None, foreign_key="controlassetclass.id")
    name: str = EXAMPLE
    short_name: Optional[str] = None
    description: Optional[str] = None
    color: Optional[str] = Field(default="#6c757d", description="Hex color code for UI display")
    framework: Optional["ControlFramework"] = Relationship(back_populates="controls")
    function: Optional["ControlFunction"] = Relationship(back_populates="controls")
    asset_class: Optional["ControlAssetClass"] = Relationship(back_populates="controls")
    safeguards: List["ControlSafeguard"] = Relationship(back_populates="control")


# API Request Models
class ControlCreate(SQLModel):
    name: str
    short_name: Optional[str] = None
    description: Optional[str] = None
    framework_id: str
    function_id: Optional[str] = None
    asset_class_id: Optional[str] = None
    color: Optional[str] = Field(default="#6c757d", description="Hex color code for UI display")

class ControlUpdate(SQLModel):
    name: Optional[str] = None
    short_name: Optional[str] = None
    description: Optional[str] = None
    framework_id: Optional[str] = None
    function_id: Optional[str] = None
    asset_class_id: Optional[str] = None
    color: Optional[str] = None


# API Response Models
class ControlStub(SQLModel):
    id: str
    name: str
    short_name: Optional[str] = None
    color: Optional[str] = None

class ControlPublic(SQLModel):
    id: str
    name: str
    short_name: Optional[str] = None
    description: Optional[str] = None
    framework_id: str
    function_id: Optional[str] = None
    color: Optional[str] = None

class ControlListPublic(SQLModel):
    data: List[ControlPublic]
    count: int

