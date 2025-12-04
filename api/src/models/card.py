from __future__ import annotations

from enum import IntEnum
from typing import TYPE_CHECKING, List

from sqlalchemy.dialects.mysql import SMALLINT, TINYINT, VARCHAR
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy_utils.types.choice import ChoiceType

from database.base_class import Base

from .mixins import TimeStampMixin

if TYPE_CHECKING:
    from models import CardToken, Stamp, User


class AwardType(IntEnum):
    AWARD_NONE = 0
    AWARD_MIDWAY = 1
    AWARD_COMPLETE = 2


class AttainmentType(IntEnum):
    ATTAINMENT_NONE = 0
    ATTAINMENT_MIDWAY = 1
    ATTAINMENT_COMPLETE = 2


class Card(Base, TimeStampMixin):

    @declared_attr
    def __table_args__(self):  # noqa:U100
        args = Base.__table_args__[0]
        return (
            {**args, "comment": "カード"},
        )

    id: Mapped[int] = mapped_column(SMALLINT(unsigned=True), primary_key=True)
    attainment: Mapped[int] = mapped_column(
        ChoiceType(AttainmentType, impl=TINYINT(unsigned=True)),
        default=AttainmentType.ATTAINMENT_NONE,
        comment="達成状況"
    )
    name: Mapped[str] = mapped_column(VARCHAR(48), nullable=True)
    score: Mapped[int] = mapped_column(
        SMALLINT(unsigned=True),
        nullable=True,
        comment="スコア",
        default=0
    )

    user: Mapped[List['User']] = relationship("User", back_populates="card", uselist=True)
    stamps: Mapped[List['Stamp']] = relationship("Stamp", backref="card")
    token: Mapped['CardToken'] = relationship("CardToken", back_populates="card", uselist=False)
