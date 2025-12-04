
from __future__ import annotations

from typing import Union

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import BOOLEAN, SMALLINT
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.schema import UniqueConstraint
from sqlalchemy_utils import UUIDType

from database.base_class import Base

from .mixins import TimeStampMixin


class Stamp(Base, TimeStampMixin):

    @declared_attr
    def __table_args__(self):  # noqa:U100
        args = Base.__table_args__[0]

        return (
            UniqueConstraint('card_id', 'place_id', name='card_place_unique'),
            {**args, "comment": "カード"}
        )

    id: Mapped[int] = mapped_column(SMALLINT(unsigned=True), primary_key=True)
    is_stamped: Mapped[bool] = mapped_column(BOOLEAN, default=False, comment="スタンプが押されているか")
    card_id: Mapped[int] = mapped_column(
        SMALLINT(unsigned=True),
        ForeignKey('card.id'),
        comment="カード")
    place_id: Mapped[str] = mapped_column(
        UUIDType(binary=True),
        ForeignKey('place.id'),
        comment="場所")

    place = relationship("Place", back_populates="stamps", lazy='joined')
