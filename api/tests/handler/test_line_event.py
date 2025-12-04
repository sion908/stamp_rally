import pytest
from fastapi import status
from httpx import AsyncClient
from httpx_auth import Basic
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from linebot.models import Profile

from models import User
from line_event import line_handler
from dependencies import line_bot_api
from crud.user import get_by_lineUserID
from services.lineHandler import handler

@pytest.mark.asyncio()
class TestReadUser:

    async def test_line_handler(self,  async_db: AsyncSession, mocker) -> None:
        # mocker.patch()
        mock_some_class = mocker.patch("database.db.async_session")
        mock_some_class.return_value.__enter__.return_value = async_db
        mocker_get_profile = mocker.patch.object(line_bot_api, "get_profile", lambda _:Profile(display_name="display_name"))
        mocker_reply_message = mocker.patch.object(line_bot_api, "reply_message", return_value="l")
        lineUserID = "Uf75f473c756d4b64d9d2106034706130"
        await handler.do_each_event({
                "type": "follow",
                "follow": {
                    "isUnblocked": True
                },
                "webhookEventId": "01HVRZNYXE576A57PW865SJVMT",
                "deliveryContext": {
                    "isRedelivery": False
                },
                "timestamp": 1713456740695,
                "source": {
                    "type": "user",
                    "userId": lineUserID
                },
                "replyToken": "a66d7a8627c040de9d44c1230a1ca34a",
                "mode": "active"
            },
            {
                "destination": "U283f21a1517f3a2757595ad75c1a0e99"

        })
        # mocker_get_profile.assert_called_once()

        user = await get_by_lineUserID(db=async_db, lineUserID=lineUserID)
        assert user.is_active==True
