import os
from enum import Enum
from functools import lru_cache
from logging import RootLogger

from pydantic import ValidationError
from pydantic_settings import BaseSettings

from .log import log_setting


class Tags(str, Enum):
    # https://fastapi.tiangolo.com/tutorial/metadata/#use-your-tags
    admin = "admin"
    user = "user"
    seal = "seal"
    card = "card"


DEBUG = os.environ.get("DEBUG", "false").lower() == "true"


class ApiSettings(BaseSettings):
    ADMIN_TOKEN: str


class LineSettings(BaseSettings):
    CHANNEL_ACCESS_TOKEN: str = os.environ.get("CHANNEL_ACCESS_TOKEN")
    LINE_ACCESS_SECRET: str = os.environ.get("LINE_ACCESS_SECRET")


class JwtSettings(BaseSettings):
    SECRET_KEY: str = os.environ.get("JWT_SECRET_KEY")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 24*60*30


class CsrfSettings(BaseSettings):
    CSRF_SECRET_KEY: str = os.environ.get("CSRF_SECRET_KEY")


@lru_cache
def load_settings() -> (
    tuple[
        bool,
        str,
        str,
        ApiSettings,
        LineSettings,
        JwtSettings,
        CsrfSettings,
        bool,
        RootLogger,
        str
    ]
):
    try:
        DEBUG = os.environ.get("DEBUG", "false").lower() == "true"
        stage_name = os.environ.get("STAGE_NAME")
        base_url = os.environ.get("BASE_URL")

        api_settings: ApiSettings = ApiSettings()
        line_settings: LineSettings = LineSettings()
        jwt_settings: JwtSettings = JwtSettings()
        csrf_settings: CsrfSettings = CsrfSettings()

        is_local = (stage_name == "local")
        RSLinehandlerName = os.environ.get("RSLinehandlerName")
        custom_logger = log_setting(stage=stage_name)
    except ValidationError as e:
        import logging
        logging.error("Could not load settings: ", e)
        raise

    return (
        DEBUG,
        stage_name,
        base_url,
        api_settings,
        line_settings,
        jwt_settings,
        csrf_settings,
        is_local,
        custom_logger,
        RSLinehandlerName
    )

(
    DEBUG,
    stage_name,
    base_url,
    api_settings,
    line_settings,
    jwt_settings,
    csrf_settings,
    is_local,
    logger,
    RSLinehandlerName
) = load_settings()
