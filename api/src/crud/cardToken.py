from datetime import datetime
from typing import AsyncIterator

from sqlalchemy import select, text
from sqlalchemy.dialects.mysql import insert
from sqlalchemy.exc import IntegrityError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from models import CardToken


async def read_by_token(db: AsyncSession, token: str) -> AsyncIterator[CardToken] | None:
    card_token = await db.scalar(
        select(CardToken)
            .options(
                joinedload(CardToken.card)
            ).where(
                CardToken.token == token
            ).limit(1)
    )
    return card_token
