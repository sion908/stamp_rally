from pydantic import BaseModel, Field

from .mixin import FromLiff


class StampSealForm(BaseModel, FromLiff):
    """スタンプの押印処理時に受け取るpostのform的なもの"""

    place_id: str = Field(..., description="スタンプを押した場所")


class AssignTeamForm(BaseModel, FromLiff):
    """スタンプの押印処理時に受け取るpostのform的なもの"""

    card_token: str = Field(..., description="カードのトークン")
