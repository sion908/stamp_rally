import json
import logging
import os

from linebot.models import TextSendMessage
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import DeclarativeBase, sessionmaker

from dependencies import line_bot_api
from setting import stage_name


class SQLJSONFormatter(logging.Formatter):
    def format(self, record):
        # レコードのメッセージ内の '\n' を '\r' に置換
        record.msg = record.msg.replace('\n', '\r')

        # ログレコードをJSONフォーマットに変換
        log_data = {
            'name': record.name,
            'level': record.levelname,
            'message': record.msg
        }

        return json.dumps(log_data)

# ロガーを取得
logger = logging.getLogger('sqlalchemy.engine')
logger.setLevel(logging.WARNING if stage_name=="prod" else logging.INFO)

handler = logging.StreamHandler()
# カスタムフォーマッタを作成
formatter = SQLJSONFormatter()

# ハンドラーにカスタムフォーマッタを設定
handler.setFormatter(formatter)

# ロガーにハンドラーを追加
logger.addHandler(handler)

DB_URL = os.environ.get(
    "DB_URL",
    # "mysql+aiomysql://as:os@rogaining_system_db:3306/local_db?charset=utf8mb4"
    "mysql+aiomysql://rogeiuser:a,*3R#AcqFh!@stamp-rally-db.cf8gtmhlcguy.ap-northeast-1.rds.amazonaws.com:3306/rogeingDev?charset=utf8mb4"
)

async_engine = create_async_engine(DB_URL, echo=True, hide_parameters=True)
async_session = sessionmaker(
    expire_on_commit=False, autocommit=False, autoflush=False, bind=async_engine, class_=AsyncSession
)


class Base(DeclarativeBase):

    def __repr__(self):
        """Dump all columns and value automagically.

        This code is copied a lot from followings.
        See also:
            - https://gist.github.com/exhuma/5935162#file-representable_base-py
            - http://stackoverflow.com/a/15929677
        modelのデバッグ用,多分うざい
        """
        #: Columns.
        columns = ', '.join([
            '{0}={1}å'.format(k, repr(self.__dict__[k]))
            for k in self.__dict__.keys() if k[0] != '_'
        ])

        return '<{0}({1})>'.format(
            self.__class__.__name_å_, columns
        )


async def get_db():
    """
    fastapiのルーティングで使う用のdb処理
    """
    async with async_session() as session:
        yield session

def session_aware(func):
    """
    fastapiのルーティング外で行われる処理で使うラッパー
    """
    async def wrapper(*args, **kwargs):
        try:
            async with async_session() as session:
                # デコレータ内で利用するために関数に値を渡す
                kwargs["db"] = session
                result = await func(*args, **kwargs)
            return result
        except Exception as e:
            import traceback
            exc_traceback = traceback.extract_tb(e.__traceback__)
            filename, line_number, func_name, text = exc_traceback[-1]
            logger.error(
                f"{exc_traceback}\t{exc_traceback[0]}\t"+
                f"An exception occurred in file '{filename}' on line {line_number}.\t"+
                f"Exception message: {e}"
            )

            if (not (hasattr(e, "custom_rep") and e.custom_rep)) and "rep_token" in kwargs:
                line_bot_api.reply_message(
                    kwargs.get("rep_token"),
                    TextSendMessage("何かしらの問題が起こりました．\nもう一度お試しください")
                )

    return wrapper
