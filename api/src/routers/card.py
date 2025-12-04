from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from crud.admin import create as create_admin
from crud.admin import read as read_admin
from crud.card import create_with_token
from crud.place import reads as reads_place
from crud.rallyconfigration import get_one
from database.db import get_db
from dependencies import CsrfProtect, get_lineuser_by_token, templates
from dependencies.jwt import JwtAuthenticator, get_current_active_admin
from models import Admin, Card
from schemas.admin import AdminOut, GenerateAdmin, LoginAdmin, Token
from schemas.card import AttachCardForm, CardTokenResponse, InputCardToken
from services.cardToken import CardTokenService
from setting import Tags, base_url, is_local, logger, stage_name

logger.name = __name__

router = APIRouter(
    tags=[Tags.card]
)

@router.post(
    "/card_token/",
    response_model=CardTokenResponse,
    tags=[Tags.admin]
)
async def generate_card_token(
    request: Request,
    input_card_token: InputCardToken,
    db: AsyncSession = Depends(get_db),
    csrf_protect: CsrfProtect = Depends(),
    current_admin: Admin = Depends(get_current_active_admin)
):
    await csrf_protect.validate_csrf(request)
    card = await create_with_token(db=db, name=input_card_token.team_name)

    return CardTokenResponse(
        cardToken=card.token.token,
        name=card.name
    )


@router.post(
    "/",
    response_class=JSONResponse,
    tags=[Tags.seal]
)
async def attach_card(
    request: Request,
    attach_card_form: AttachCardForm,
    db: AsyncSession = Depends(get_db),
    csrf_protect: CsrfProtect = Depends()
):
    """
    Creates a new Post
    """
    await csrf_protect.validate_csrf(request)

    user, _ = await get_lineuser_by_token(db=db, token=attach_card_form.lineToken, create=True)

    card_token_service = CardTokenService(db=db, user=user)
    card = await card_token_service.regist_user(card_token=attach_card_form.card_token)
    context = {
        "name": card.name,
        "html": f"<p>チームに登録されました</p><p>チーム名</p><p>{card.name}</p>"
    }

    return JSONResponse(context)
