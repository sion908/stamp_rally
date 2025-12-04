import math

from linebot.models import FlexSendMessage, TextSendMessage
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from crud.card import get_by_id as get_card_by_id
from crud.card import update as update_card
from crud.cardToken import read_by_token as read_by_token_card
from crud.place import get_by_id as get_place_by_id
from crud.place import reads as reads_place
from crud.rallyconfigration import get_one as get_one_rc
from crud.stamp import count as count_stamp
from crud.stamp import create as create_stamp
from crud.user import get_with_card
from database.db import session_aware
from dependencies import line_bot_api
from exception.exceptions import SimpleException, UserAlreadyRegistrationError
from models import Card, User
from setting import logger


class CardTokenService():
    def __init__(self, db:AsyncSession, user:User):
        self.db = db
        self.user = user


    async def regist_user(self, card_token: str) -> Card:
        if self.user.card_id:
            raise UserAlreadyRegistrationError(team_name=self.user.card.name)
        card_token_model = await read_by_token_card(db=self.db, token=card_token)

        if card_token_model.count <= 0:
            raise SimpleException("チームの登録人数の上限です")

        self.user.card_id = card_token_model.card_id
        card_token_model.count -= 1

        self.db.add(self.user)
        self.db.add(card_token_model)
        await self.db.commit()

        self.card_token = card_token_model
        self.card = card_token_model.card

        return card_token_model.card
