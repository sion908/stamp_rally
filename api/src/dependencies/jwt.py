from datetime import datetime, timedelta, timezone
from typing import Optional, Union

from fastapi import Depends, FastAPI, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from fastapi.security.utils import get_authorization_scheme_param
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from sqlalchemy.ext.asyncio import AsyncSession
from starlette.status import HTTP_307_TEMPORARY_REDIRECT, HTTP_401_UNAUTHORIZED

from crud.admin import read as read_admin
from database.db import get_db
from models import Admin
from setting import is_local, jwt_settings, logger, stage_name


class TokenData(BaseModel):
    username: Union[str, None] = None


class OAuth2PasswordBearerOrCookie(OAuth2PasswordBearer):
    async def __call__(self, request: Request) -> Optional[str]:
        # クッキーからトークンを取得
        cookie_token = request.cookies.get("access_token")

        # ヘッダーからAuthorizationを取得
        authorization = request.headers.get("Authorization")

        # トークンとAuthorizationをログ出力
        logger.info(f"Cookie Token: {cookie_token}, Authorization: {authorization}")

        # Bearerトークンが空でクッキーのaccess_tokenに値が入っている場合
        if not authorization and cookie_token:
            authorization = f"Bearer {cookie_token}"

        scheme, param = get_authorization_scheme_param(authorization)
        if not authorization or scheme.lower() != "bearer":
            if self.auto_error:
                # ログインページにリダイレクト
                raise HTTPException(
                    status_code=HTTP_307_TEMPORARY_REDIRECT,
                    detail="Not authenticated",
                    headers={"Location": f"{'' if is_local else f'/{stage_name.lower()}'}/admin/login"}
                )
                raise HTTPException(
                    status_code=HTTP_401_UNAUTHORIZED,
                    detail="Not authenticated",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            else:
                return None
        return param

oauth2_scheme = OAuth2PasswordBearerOrCookie(tokenUrl="token")

class JwtAuthenticator:

    def __init__(self):
        self.SECRET_KEY = jwt_settings.SECRET_KEY
        self.ALGORITHM = jwt_settings.ALGORITHM
        self.ACCESS_TOKEN_EXPIRE_MINUTES = jwt_settings.ACCESS_TOKEN_EXPIRE_MINUTES
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
        self.oauth2_scheme = oauth2_scheme


    def verify_password(self, plain_password, hashed_password):
        return self.pwd_context.verify(plain_password, hashed_password)


    def get_password_hash(self, password):
        return self.pwd_context.hash(password)

    def decode(self, token):
        return jwt.decode(token, self.SECRET_KEY, algorithms=[self.ALGORITHM])


    @classmethod
    async def authenticate_admin(cls, db: AsyncSession, username: str, password: str):
        admin = await read_admin(db=db, username=username)
        if not admin:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        jwt_authenticator = cls()
        if not admin.password == password:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        return jwt_authenticator, admin


    def create_access_token(
        self,
        admin: Admin
    ) -> str:
        expires_delta = timedelta(minutes=self.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode = {"sub": admin.username}.copy()
        if expires_delta:
            expire = datetime.now(timezone.utc) + expires_delta
        else:
            expire = datetime.now(timezone.utc) + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, self.SECRET_KEY, algorithm=self.ALGORITHM)
        return encoded_jwt

async def get_current_user(
    request: Request,
    token: str = Depends(oauth2_scheme),
    db: AsyncSession = Depends(get_db)
):
    # クッキーからトークンを取得
    cookie_token = request.cookies.get("access_token")

    # Bearerトークンを取得
    bearer_token = request.headers.get("Authorization")
    logger.error(f"cookie_token: {cookie_token}, bearer_token: {bearer_token}")
    jwt_authenticator = JwtAuthenticator()
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt_authenticator.decode(token)
        username: str = payload.get("sub")
        if username is None:
            logger.error(f"incorrect token: not username: {payload}")
            raise credentials_exception
        token_data = TokenData(username=username)
    except JWTError as e:
        logger.error(f"each JWTError: {e}")
        raise credentials_exception
    admin = await read_admin(db=db, username=token_data.username)
    if admin is None:
        logger.error("incorrect admin")
        raise credentials_exception
    return admin

async def get_current_active_admin(current_admin: Admin = Depends(get_current_user)):

    return current_admin
