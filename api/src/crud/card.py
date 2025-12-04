from datetime import datetime
from typing import AsyncIterator

from sqlalchemy import select, text
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from models import Card, CardToken, Place, Stamp, User


async def get_by_id(db: AsyncSession, card_id: int=None, card: Card=None, user: User=None) -> AsyncIterator[Card]| None:
    stmt = select(
        Card
    ).options(
        joinedload(Card.stamps),
        joinedload(Card.stamps).joinedload(Stamp.place)
    )
    if card_id:
        stmt = stmt.where(Card.id == card_id)
    elif card is not None:
        stmt = stmt.where(Card.id == card.id)
    elif user:
        stmt = stmt.where(Card.id == user.card_id)
    else:
        raise TypeError()
    result = await db.execute(
        stmt.limit(1)
    )

    res_card = result.scalar()

    if res_card and res_card.stamps:
        # Stamp を Place.id でソートし、Place の id と name のみを抽出
        res_card.stamps.sort(key=lambda stamp: stamp.created_at)

    return res_card


async def create_with_token(db: AsyncSession, name: str = None) -> Card:
    """create user by email and password"""
    card = Card(name=name)
    db.add(card)
    await db.commit()
    await db.refresh(card)

    card_token = CardToken(card_id=card.id)

    db.add(card_token)
    await db.commit()
    card = await db.scalar(
        select(Card)
            .where(Card.id == card.id)
            .options(
                joinedload(Card.token)
            ).limit(1)
    )

    return card


async def update(
    db: AsyncSession,
    card: Card
) -> AsyncIterator[Card]:
    card.updated_at = datetime.now()
    db.add(card)

    await db.commit()
    await db.refresh(card)

    return card


async def reads(db: AsyncSession) -> AsyncIterator[Card] | None:
    cards = await db.execute(
        select(Card).options(
            joinedload(Card.stamps),
            joinedload(Card.stamps).joinedload(Stamp.place)
        )
    )

    return [card[0] for card in cards.unique().all()]
