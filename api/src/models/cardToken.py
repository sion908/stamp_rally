from __future__ import annotations

import random
import string
from enum import IntEnum

from sqlalchemy import ForeignKey, String
from sqlalchemy.dialects.mysql import SMALLINT, TINYINT, VARCHAR
from sqlalchemy.ext.declarative import declared_attr
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import TypeDecorator
from sqlalchemy_utils.types.choice import ChoiceType

from database.base_class import Base

from .mixins import TimeStampMixin


class TokenType(TypeDecorator):
    impl = String(32)
    length = 32
    cache_ok = True

    def __init__(self, length=32, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.length = length

    def process_bind_param(self, value, dialect):
        return value

    def process_result_value(self, value, dialect):
        return value

    @property
    def python_type(self):
        return str

    def generate_token(self):
        characters = string.ascii_letters + string.digits
        return ''.join(random.choice(characters) for _ in range(32))


class CardToken(Base, TimeStampMixin):

    @declared_attr
    def __table_args__(self):  # noqa:U100
        args = Base.__table_args__[0]
        return (
            {**args, "comment": "カード"},
        )

    id: Mapped[int] = mapped_column(SMALLINT(unsigned=True), primary_key=True)
    card_id: Mapped[int] = mapped_column(SMALLINT(unsigned=True),
        ForeignKey('card.id'),
        comment="作成されたカード")
    token: Mapped[str] = mapped_column(TokenType(length=32), default=TokenType.generate_token, unique=True)
    count: Mapped[int] = mapped_column(TINYINT(unsigned=True), default=1)


    card = relationship("Card", back_populates="token", lazy='joined')
