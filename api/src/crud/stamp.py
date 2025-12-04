from datetime import datetime
from typing import AsyncIterator, List

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only
from sqlalchemy.sql.expression import func

from models import Card, Stamp


async def update(
    db: AsyncSession,
    stamp: Stamp
) -> AsyncIterator[Stamp]:
    # stamp.place=None
    # stamp.place_id=None
    stamp.updated_at = datetime.now()
    db.add(stamp)

    await db.commit()
    await db.refresh(stamp)

    return stamp

async def create(db: AsyncSession, place_id: str, card: Card = None, card_id: int=None) -> Stamp:
    if not card_id:
        card_id=card.id
    """create user by email and password"""
    db_stamp = Stamp(place_id=place_id, card_id=card_id, is_stamped=True)

    db.add(db_stamp)
    await db.commit()

    await db.refresh(db_stamp)
    return db_stamp


async def count(db: AsyncSession, card_id: int) -> AsyncIterator[List[Stamp]]| None:
    stamp_count = await db.scalar(
        select(func.count(Stamp.id)).where(Stamp.card_id==card_id)
    )

    return stamp_count
