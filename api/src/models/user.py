from __future__ import annotations

from typing import TYPE_CHECKING

from sqlalchemy import ForeignKey
from sqlalchemy.dialects.mysql import BOOLEAN, SMALLINT, VARCHAR
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, mapped_column, relationship

from database.base_class import Base

from .mixins import TimeStampMixin

if TYPE_CHECKING:
    from models import *

class User(Base, TimeStampMixin):

    @declared_attr
    def __table_args__(self):  # noqa:U100
        args = Base.__table_args__[0]
        return (
            {**args, "comment": "ユーザー"},
        )

    id: Mapped[int] = mapped_column(SMALLINT(unsigned=True), primary_key=True)
    lineUserID: Mapped[str] = mapped_column(VARCHAR(40), unique=True)
    username: Mapped[str] = mapped_column(VARCHAR(48), nullable=True)
    is_active: Mapped[bool] = mapped_column(BOOLEAN, default=True, nullable=False)

    card_id: Mapped[int] = mapped_column(SMALLINT(unsigned=True),
        ForeignKey('card.id'),
        nullable=True,
        comment="所持カード")
    admin: Mapped['Admin'] = relationship("Admin", backref="user")

    card: Mapped['Card'] = relationship("Card", back_populates="user", lazy="joined")

    def convert_output(self):
        self.id = str(self.id)
        self.password = "*****"
        return self
