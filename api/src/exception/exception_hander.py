from fastapi import Request
from fastapi.responses import JSONResponse
from fastapi_csrf_protect.exceptions import CsrfProtectError

from dependencies import line_bot_api
from setting import logger

from .exceptions import SimpleException, TeamRegistrationError, UserAlreadyRegistrationError

logger.name = __name__


def add_exception_handlers(app):

    @app.exception_handler(Exception)
    async def simple_exception_handler(request: Request, exc: Exception):  # noqa: U100
        if hasattr(exc, "msg"):
            logger.warning(f"MyException occured!!! {exc.msg}")
            return JSONResponse(status_code=exc.status_code, content=exc.msg)
        else:
            return JSONResponse(status_code=404, content="error")


    @app.exception_handler(SimpleException)
    async def simple_exception_handler(request: Request, exc: SimpleException):  # noqa: U100
        logger.warning(f"MyException occured!!! {exc.msg}")
        return JSONResponse(status_code=exc.status_code, content=exc.msg)

    @app.exception_handler(CsrfProtectError)
    def csrf_protect_exception_handler(request: Request, exc: CsrfProtectError):
        logger.warning(f"CsrfProtectError occured!!! {exc.message}")
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

    @app.exception_handler(TeamRegistrationError)
    def team_registration_error_exception_handler(request: Request, exc: TeamRegistrationError):
        logger.info(f"TeamRegistrationError occured!!! {exc.message}")
        if exc.rep_token:
            message = [
                TextSendMessage("チーム登録を行なってください")
            ]
            line_bot_api.reply_message(exc.rep_token, message)
            return
        else:
            return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})

    @app.exception_handler(UserAlreadyRegistrationError)
    def team_registration_error_exception_handler(
        request: Request,  # noqa: U100
        exc: UserAlreadyRegistrationError
    ):
        logger.warning(f"UserAlreadyRegistrationError occured!!! {exc.message}")
        return JSONResponse(status_code=exc.status_code, content={"detail": exc.message})
