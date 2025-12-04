import pytest
import random

from pytest_mock import MockerFixture
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import joinedload

from services.card import CardService
from exception.exceptions import TeamRegistrationError
from crud.user import get_with_card
from models import RallyConfiguration, User, Card, Stamp, Place


@pytest.mark.asyncio()
class TestCardService():

    async def test_init_card_service(self):
        card_service = CardService()

        assert type(card_service) == CardService

    async def test_init_async_card_service(
            self,
            async_db: AsyncSession,
            create_rally_configuration: RallyConfiguration,
            create_user: User,
            create_places: 'function'
        ):
        places = await create_places(count=10)
        card_service = CardService()
        user = await get_with_card(db=async_db, lineUserID=create_user.lineUserID)

        await card_service.async_init(db=async_db,user=create_user,rally_configuration=create_rally_configuration)


@pytest.mark.asyncio()
class TestShowCards():

    async def test_main(
            self,
            mocker: MockerFixture,
            create_rally_configuration: RallyConfiguration,
            create_user: User,
            create_places: 'function'
        ):
        await create_places(count=5)
        rep_token = "rep_token"

        mock_rep_mess = mocker.patch("dependencies.line_bot_api.reply_message", return_value="")
        await CardService.showCard(rep_token=rep_token, luserid=create_user.lineUserID)
        assert mock_rep_mess.call_count == 1
        assert mock_rep_mess.call_args.args[0] == rep_token
        assert len(mock_rep_mess.call_args.args[1]) == 1


@pytest.mark.asyncio()
class TestSealStamp():

    async def test_main(
            self,
            async_db: AsyncSession,
            create_rally_configuration: RallyConfiguration,
            create_user: User,
            create_card: Card,
            create_places: 'function'
        ):
        place_count=5
        places = await create_places(count=place_count)
        card_service = CardService()
        user = await get_with_card(db=async_db, lineUserID=create_user.lineUserID)

        user.card_id = create_card.id
        async_db.add(user)
        await async_db.commit()

        await card_service.async_init(db=async_db, user=create_user, rally_configuration=create_rally_configuration)

        assert card_service.card == create_card

        selected_place = random.choice(places)
        await card_service.seal_stamp(place_id=selected_place.id)

        db_user = await get_with_card(db=async_db, lineUserID=create_user.lineUserID)

        for stamp in db_user.card.stamps:
            if stamp.place.id == selected_place.id:
                assert stamp.is_stamped
            else:
                assert not stamp.is_stamped


    async def test_not_assign(
            self,
            async_db: AsyncSession,
            create_rally_configuration: RallyConfiguration,
            create_user: User,
            create_places: 'function'
        ):
        place_count=5
        places = await create_places(count=place_count)
        card_service = CardService()
        user = await get_with_card(db=async_db, lineUserID=create_user.lineUserID)

        with pytest.raises(TeamRegistrationError):
            await card_service.async_init(db=async_db, user=create_user, rally_configuration=create_rally_configuration)
