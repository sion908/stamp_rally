import pytest
from fastapi import status
from httpx import AsyncClient
from httpx_auth import Basic
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload, joinedload

from models import User, Card, CardToken
from crud.user import create as create_user
from schemas.user import UserCreate

@pytest.mark.asyncio()
class TestCardTokenModel:

    async def test_create_cardToken(self, async_db: AsyncSession, create_card: Card) -> None:
        card_token = CardToken(card_id=create_card.id)

        async_db.add(card_token)

        await async_db.commit()
        await async_db.refresh(card_token)

        db_card_token = await async_db.scalar(
            select(CardToken)
                .where(CardToken.id == card_token.id)
                .options(joinedload(CardToken.card))
                .limit(1)
        )

        assert db_card_token.id == card_token.id
        assert db_card_token.card_id == card_token.card_id
        assert db_card_token.token == card_token.token
        assert type(db_card_token.token) == str
        assert db_card_token.count == card_token.count
        assert db_card_token.card == card_token.card
