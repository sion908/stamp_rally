from typing import List, Optional

from pydantic import UUID4, BaseModel, ConfigDict, Field


class Place(BaseModel):
    name: str = Field(..., description="名前")
    # altname: Optional[str] = Field("", description="仮称")
    score: int = Field(..., description="スコア")
    # access: Optional[str] = Field("", description="住所")
    gpsLatitude: Optional[float] = Field(None, description="緯度")
    gpsLongitude: Optional[float] = Field(None, description="経度")
    is_active: Optional[bool] = Field(True, description="有効か")


class PlacesInput(BaseModel):
    places: List[Place]

    model_config = ConfigDict(from_attributes=True)

class PlaceOutput(Place):
    id: UUID4
