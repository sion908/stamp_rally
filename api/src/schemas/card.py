from typing import Optional

from pydantic import BaseModel, ConfigDict, Field

from .mixin import FromLiff


class InputCardToken(BaseModel):

    team_name: Optional[str] = Field(None, description="スタンプを押した場所")

    model_config = ConfigDict(from_attributes=True)


class CardTokenResponse(BaseModel):
    cardToken: str
    name: Optional[str]

    model_config = ConfigDict(from_attributes=True)


class AttachCardForm(BaseModel, FromLiff):

    card_token: str = Field(..., description="カードのトークン")
