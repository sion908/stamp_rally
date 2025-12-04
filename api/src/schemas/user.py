from typing import Optional

from pydantic import BaseModel, Field

from .mixin import ForOrm


class UserCreate(BaseModel, ForOrm):
    """Input"""

    lineUserID: Optional[str] = None
    username: Optional[str] = None
    is_active: Optional[bool] = Field(None, description="activeか")
