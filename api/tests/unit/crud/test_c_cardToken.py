import pytest
from fastapi import status
from httpx import AsyncClient
from httpx_auth import Basic
import freezegun
from datetime import (datetime, timedelta)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import CardToken, Card, Stamp, Place, User
from crud.cardToken import read_by_token
from crud.card import create_with_token


@pytest.mark.asyncio()
class TestReadByToken:

    async def test_main(
            self,
            async_db: AsyncSession
        ) -> None:

        card_name ="card_name"

        init_card0 = await create_with_token(db=async_db, name=f"{card_name}-0")
        init_card = await create_with_token(db=async_db, name=card_name)
        init_card2 = await create_with_token(db=async_db, name=f"{card_name}-2")

        card_token = await read_by_token(db=async_db, token=init_card.token.token)

        assert type(card_token) == CardToken
        assert card_token.token == init_card.token.token
        assert type(card_token.card) == Card
        assert card_token.card.name == card_name
