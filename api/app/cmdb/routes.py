# CMDB Main Routes

from fastapi import APIRouter
from .configuration_item_types.routes import router as ci_types_router
# from .configuration_items.routes import router as ci_router  # Will add this later

router = APIRouter()

# Include sub-routers
router.include_router(ci_types_router, prefix="/configuration-item-types", tags=["Configuration Item Types"])
# router.include_router(ci_router, prefix="/configuration-items", tags=["Configuration Items"])  # Will add this later
