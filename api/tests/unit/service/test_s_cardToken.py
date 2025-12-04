from sqlalchemy.ext.asyncio import AsyncSession
import pytest
import random
from pytest_mock import MockerFixture

from services.cardToken import CardTokenService
from crud.user import get_with_card
from crud.card import create_with_token
from models import RallyConfiguration, User


class TestCardTokenService():

    async def test_init_card_service(
            self,
            async_db: AsyncSession,
            create_user: User
        ):
        card_token_service = CardTokenService(db=async_db, user=create_user)

        assert type(card_token_service) == CardTokenService
        assert card_token_service.db == async_db
        assert card_token_service.user == create_user


@pytest.mark.asyncio()
class TestRegistUser():

    async def test_main(
            self,
            async_db: AsyncSession,
            create_user: User
        ):
        card_name = "rep_token"
        init_card = await create_with_token(db=async_db, name=card_name)

        card_token_service = CardTokenService(db=async_db, user=create_user)
        card = await card_token_service.regist_user(card_token=init_card.token.token)

        await async_db.refresh(create_user)

        assert card == init_card
        assert create_user.card == card
        assert create_user.card.name == card_name
