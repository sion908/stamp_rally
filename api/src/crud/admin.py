from datetime import datetime
from typing import AsyncIterator

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from models import Admin, User
from schemas.admin import GenerateAdmin, LoginAdmin


async def read(
    db: AsyncSession,
    username: str
) -> AsyncIterator[Admin]:
    db_admin = await db.scalar(
        select(Admin).where(
            Admin.username == username
        ).limit(1)
    )
    return db_admin


async def create(db: AsyncSession, generate_admin: GenerateAdmin) -> Admin:
    """create user by email and password"""

    db_admin = Admin(**generate_admin.model_dump())

    db.add(db_admin)
    await db.commit()

    await db.refresh(db_admin)
    return db_admin


async def get_or_create(db: AsyncSession, lineUserID: str) -> User:
    user = await db.scalar(
        select(User).where(User.lineUserID == lineUserID).limit(1)
    ).scalar_one()

    if user:
        return user
    else:
        user = User(lineUserID=lineUserID)
        db.add(user)

        await db.commit()
        await db.refresh(user)

        return user
