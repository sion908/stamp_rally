import math
from datetime import datetime, timedelta

from linebot.models import FlexSendMessage, TextSendMessage
from sqlalchemy.ext.asyncio import AsyncSession

from crud.card import get_by_id as get_card_by_id
from crud.card import update as update_card
from crud.place import get_by_id as get_place_by_id
from crud.place import reads_exctude_is_base as reads_exctude_is_base_place
from crud.rallyconfigration import get_one as get_one_rc
from crud.stamp import count as count_stamp
from crud.stamp import create as create_stamp
from crud.user import get_with_card
from database.db import session_aware
from dependencies import line_bot_api
from exception.exceptions import TeamRegistrationError
from models import Place, RallyConfiguration, Stamp, User
from setting import logger


class CardService():
    async def async_init(
        self,
        db: AsyncSession,
        user: User,
        rally_configuration: RallyConfiguration = None,
        rep_token: str = None
    ) -> None:
        self.db = db
        self.rally_configuration = rally_configuration or (await get_one_rc(db=db))
        self.user = user
        card_id = getattr(user, "card_id", None)
        if user.card_id is not None:
            self.card = await get_card_by_id(db=self.db, user=user)

        if not (hasattr(self, "card") and self.card):
            raise TeamRegistrationError(rep_token=rep_token)

    async def _get_stamped_count(self):
        if hasattr(self, "stamped_count"):
            return getattr(self, "stamped_count", 0)
        else:
            stamp_count = await count_stamp(db=self.db, card_id=self.card.id)

            return stamp_count

    async def seal_stamp(self, place_id: str) -> Place:

        context = {}

        for stamp in self.card.stamps:
            if str(stamp.place.id) == place_id:
                context["already"] = True
                context["name"] = stamp.place.name

        if not context.get("already"):
            await create_stamp(db=self.db, place_id=place_id, card=self.card)
            place = await get_place_by_id(db=self.db, place_id=place_id)
            context["name"] = place.name
            if place.is_base:
                context["end_text"] = "おつかれさまでした"
            else:
                self.card.score += place.score
            await update_card(db=self.db, card=self.card)
        context["count"] = await self._get_stamped_count()
        return context

    @classmethod
    @session_aware
    async def showCard(self, rep_token: str, luserid: str, db: AsyncSession = None):
        user = await get_with_card(db=db, lineUserID=luserid)

        if user and getattr(user, "card_id") is not None:
            service = self()
            await service.async_init(db=db, user=user, rep_token=rep_token)
            bubble = await service._makeCardBubble()
            message = [FlexSendMessage(**bubble)]
        else:
            message = [
                TextSendMessage("チーム登録に登録されていません")
            ]
        line_bot_api.reply_message(rep_token, message)

    async def _makeCardBubble(self) -> dict:
        card = self.card
        stamps = card.stamps
        places = await reads_exctude_is_base_place(db=self.db)
        penalty_points = self._calculate_tardiness_penalty()
        count_bubble = {
            "type": "bubble",
            "header": {
                "type": "box",
                "layout": "vertical",
                "contents": [
                    {
                        "type": "text",
                        "text": "ながさき",
                        "align": "center",
                        "size": "lg"
                    },
                    {
                        "type": "text",
                        "text": "まちぶら ロゲイング",
                        "align": "center",
                        "size": "xl"
                    }
                ],
                "backgroundColor": "#d5edea"
            },
            "body": {
            "type": "box",
            "layout": "vertical",
            "contents": [
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "チェックインした数"
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": f"{len(stamps) - int(bool(self.get_base_stamp()))}",
                            "flex": 4,
                            "size": "4xl",
                            "weight": "bold",
                            "align": "end",
                            "gravity": "center"
                        },
                        {
                            "type": "text",
                            "text": "/",
                            "flex": 1,
                            "size": "4xl",
                            "align": "center"
                        },
                        {
                            "type": "text",
                            "text": f"{len(places)}",
                            "flex": 3,
                            "align": "start",
                            "gravity": "bottom",
                            "weight": "bold",
                            "size": "xl"
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                            "type": "text",
                            "text": "スコア"
                        }
                    ]
                },
                {
                    "type": "box",
                    "layout": "horizontal",
                    "contents": [
                        {
                            "type": "text",
                            "text": f"{self.card.score - penalty_points}",
                            "flex": 4,
                            "size": "4xl",
                            "align": "end",
                            "gravity": "center"
                        },
                        {
                            "type": "text",
                            "text": "点",
                            "size": "xxl",
                            "align": "start",
                            "gravity": "bottom"
                        }
                    ]
                }
            ],
            "backgroundColor": "#d5edea"
            },
            "footer": {
                "type": "box",
                "layout": "vertical",
                "spacing": "sm",
                "contents": [
                    {
                        "type": "text",
                        "text": "2024 55hubs",
                        "align": "end",
                        "size": "xxs"
                    }
                ],
                "flex": 0,
                "backgroundColor": "#d5edea"
            }
        }

        place_cont = [
            {
              "type": "box",
              "layout": "horizontal",
              "contents": [
                {
                    "type": "text",
                    "text": "●",
                    "flex": 1,
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": f"[{str(s.place.score).rjust(3, ' ')}]",
                    "flex": 2,
                    "align": "center"
                },
                {
                    "type": "text",
                    "text": s.place.name,
                    "flex": 8
                }
              ]
            } for s in stamps
        ]
        place_bubble = []
        for i in range(math.ceil(len(stamps) / 10)):
            bubble = {
                "type": "bubble",
                "header": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": [
                        {
                        "type": "text",
                        "text": "チェックインした場所",
                        "size": "lg",
                        "align": "center"
                        }
                    ],
                    "margin": "sm"
                },
                "body": {
                    "type": "box",
                    "layout": "vertical",
                    "contents": place_cont[i * 10: (i + 1) * 10]
                }
            }
            place_bubble.append(bubble)

        carousel = {
            "type": "carousel",
            "contents": [
                count_bubble,
                *place_bubble
            ]
        }
        flexDatas = {"alt_text": f"{len(stamps)}箇所訪れました", "contents": carousel}
        return flexDatas


    def _calculate_tardiness_penalty(self):
        base_stamp = self.get_base_stamp()
        if not base_stamp:
            return 0
        created_at = base_stamp.created_at
        base_time = self.rally_configuration.end_time

        return self.calculate_tardiness_penalty(base_time, created_at)


    @classmethod
    def calculate_tardiness_penalty(cls, base_time, created_at):
        if not created_at:
            return 0

        # 時間差を計算します
        time_difference = created_at - base_time

        # 時間差を秒単位に変換します
        time_difference_seconds = time_difference.total_seconds()

        # 秒を切り上げて分単位に変換します
        time_difference_minutes = math.ceil(time_difference_seconds / 60)

        # 時間差が正であれば、1分ごとに50点マイナスする計算を行います
        penalty_points = time_difference_minutes * 50 if time_difference_seconds > 0 else 0

        return penalty_points


    def get_base_stamp(self):
        if hasattr(self, "get_base_stamp_stamp"):
            return getattr(self, "get_base_stamp_stamp")
        for stamp in self.card.stamps:
            if stamp.place.is_base:
                return stamp
        return None
