from typing import AsyncIterator

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import load_only

from models import Place


async def get_by_id(db: AsyncSession, place_id: str) -> AsyncIterator[Place]| None:
    place = await db.scalar(
        select(Place)
            .where(Place.id == place_id)
            .limit(1)
    )
    return place


async def get_active_places(
    db: AsyncSession,
    limit: int = None,
    only_id: bool = False
) -> AsyncIterator[list[Place]]:

    stmt = select(Place).filter(Place.is_active==True)
    if only_id:
        stmt = stmt.options(load_only(Place.id))
    if limit:
        stmt = stmt.limit(limit)
    result = await db.execute(stmt)
    places = result.scalars().all()

    return places

async def reads(db: AsyncSession) -> AsyncIterator[Place]| None:
    places = await db.execute(
        select(Place.id, Place.name, Place.score, Place.is_active, Place.altname, Place.access)
    )

    return places.all()

async def reads_exctude_is_base(db: AsyncSession) -> AsyncIterator[Place]| None:
    places = await db.execute(
        select(Place.id).filter(Place.is_base==False)
    )

    return places.all()

async def creates(db: AsyncSession, places: list[Place]) -> list[Place]:

    place_attrs = [p.model_dump() for p in places.places]

    await db.execute(
        Place.__table__.insert(),
        place_attrs
    )

    await db.commit()
    places = await reads(db=db)
    return places
