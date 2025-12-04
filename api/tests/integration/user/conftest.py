import pytest
from sqlalchemy.ext.asyncio import AsyncSession

from models import User


@pytest.fixture()
async def async_user_orm(async_db: AsyncSession) -> User:
    user = User(username='test', sex=1, age=20)
    async_db.add(user)
    await async_db.commit()
    await async_db.refresh(user)
    return user
