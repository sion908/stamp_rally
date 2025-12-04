from fastapi_csrf_protect import CsrfProtect
from fastapi_csrf_protect.exceptions import CsrfProtectError
from pydantic import BaseModel

from setting import csrf_settings


class CsrfSettings(BaseModel):
    secret_key: str = csrf_settings.CSRF_SECRET_KEY
    cookie_samesite: str = "strict"
    # HTTPSであることを必須とする
    cookie_secure: bool = False
    token_location: str = "body"
    token_key: str = "csrfToken"


@CsrfProtect.load_config
def get_csrf_config():
    return CsrfSettings()
