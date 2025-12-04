import pytest
from fastapi import status
from httpx import AsyncClient
from httpx_auth import Basic
import freezegun
import copy
from datetime import (datetime, timedelta)
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import User, Stamp, RallyConfiguration, Card
from crud.stamp import update, create, count



@pytest.mark.asyncio()
class TestUpdate:

    async def test_main(self, async_db: AsyncSession, create_user: User, create_rally_configuration:RallyConfiguration, create_place, create_card_with_another) -> None:
        await create_card_with_another(owner=create_user, stamp_count=1, places=[create_place])
        stamp = (
            await async_db.execute(select(Stamp).limit(1))
        ).scalar_one()

        stamp_be = copy.deepcopy(stamp)

        stamp.is_stamped=True
        with freezegun.freeze_time('2015-10-21'):
            stamp = await update(db=async_db, stamp=stamp)
            db_stamp = (
                await async_db.execute(select(Stamp).limit(1))
            ).scalar_one()

        assert stamp_be.is_stamped != db_stamp.is_stamped
        assert stamp_be.id == db_stamp.id

    async def test_5_in_3(self, async_db: AsyncSession, create_user: User, create_rally_configuration:RallyConfiguration, create_places, create_card_with_another) -> None:
        stamp_id=3
        places = await create_places(count=5)
        await create_card_with_another(owner=create_user, stamp_count=5, places=places)

        stamp = (
            await async_db.execute(select(Stamp).where(Stamp.id==stamp_id).limit(1))
        ).scalar_one()
        stamp_be = copy.deepcopy(stamp)

        stamp.is_stamped=True
        stamp = await update(db=async_db, stamp=stamp)
        db_stamp = (
            await async_db.execute(select(Stamp).where(Stamp.id==stamp_id).limit(1))
        ).scalar_one()


        assert stamp_be.is_stamped != db_stamp.is_stamped
        assert stamp_be.id == db_stamp.id

@pytest.mark.asyncio()
class TestCreate:

    async def test_main(
        self,
        async_db: AsyncSession,
        create_user: User,
        create_rally_configuration:RallyConfiguration,
        create_places: 'function',
        create_card: Card
    ) -> None:
        places = await create_places(3)

        db_stamp=await create(db=async_db, place_id=places[0].id, card=create_card)

        assert places[0].id == db_stamp.place_id
        assert db_stamp.card_id == create_card.id

@pytest.mark.asyncio()
class TestReads:

    async def test_main(
        self,
        async_db: AsyncSession,
        create_user: User,
        create_rally_configuration:RallyConfiguration,
        create_places: 'function',
        create_card_with_another: 'function'
    ) -> None:
        places = await create_places(3)
        card = await create_card_with_another(owner=create_user, stamp_count=3, places=places)

        stamp_count=await count(db=async_db, card_id=card.id)

        assert type(stamp_count) == int
        assert stamp_count == 3
