import pytest
import time
from fastapi import status
from httpx import AsyncClient
from httpx_auth import Basic
import freezegun
from datetime import (datetime, timedelta)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import CardToken, Card, Stamp, Place, User
from crud.card import get_by_id, create_with_token, reads


@pytest.mark.asyncio()
class TestGetById:
    async def test_main(
            self,
            async_db: AsyncSession,
            create_user: User,
            create_places: 'function',
            create_card_with_another: 'function',
        ) -> None:

        stamp_count = 5
        places = await create_places(count=stamp_count)
        init_card = await create_card_with_another(owner=create_user, stamp_count=stamp_count,places=places)
        await async_db.commit()
        card = await get_by_id(db=async_db, card=init_card)
        assert type(card) == Card
        assert len(card.stamps) == stamp_count
        assert type(card.stamps[0]) == Stamp
        assert type(card.stamps[0].place) == Place
        assert type(card.stamps[0].place.name) == str


@pytest.mark.asyncio()
class TestCreateWithToken:

    async def test_main(
            self,
            async_db: AsyncSession
        ) -> None:

        card_name ="card_name"

        card = await create_with_token(db=async_db, name=card_name)
        assert type(card) == Card
        assert card.name == card_name
        assert type(card.token) == CardToken


@pytest.mark.asyncio()
class TestReads:

    async def test_main(
            self,
            async_db: AsyncSession,
            create_places: 'function',
            create_card_with_another: 'function',
        ) -> None:

        stamp_count = 5
        places = await create_places(count=stamp_count, exsist_base=True)
        init_card = await create_card_with_another(stamp_count=stamp_count,places=places)
        init_card = await create_card_with_another(stamp_count=stamp_count-1,places=places)

        cards = await reads(db=async_db)
        for card_or in cards:
            card = card_or[0]
            assert type(card) == Card
            for stamp in card.stamps:
                assert type(stamp) == Stamp
                assert type(stamp.place) == Place

    async def test_many(
            self,
            async_db: AsyncSession,
            create_places: 'function',
            create_card_with_another: 'function',
        ) -> None:

        stamp_count = 50
        places = await create_places(count=stamp_count, exsist_base=True)
        for i in range(100):
            init_card = await create_card_with_another(stamp_count=stamp_count,places=places)

        cards = await reads(db=async_db)
        for card_or in cards:
            card = card_or[0]
            assert type(card) == Card
            for stamp in card.stamps:
                assert type(stamp) == Stamp
                assert type(stamp.place) == Place
