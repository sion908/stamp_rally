from operator import attrgetter

from fastapi import APIRouter, Depends, Request
from fastapi.responses import HTMLResponse
from sqlalchemy.ext.asyncio import AsyncSession

from crud.admin import create as create_admin
from crud.card import create_with_token
from crud.card import reads as reads_card
from crud.rallyconfigration import get_one as get_one_rc
from database.db import get_db
from dependencies import CsrfProtect, templates
from dependencies.jwt import JwtAuthenticator, get_current_active_admin
from models import Admin
from schemas.admin import AdminOut, GenerateAdmin, LoginAdmin, Token
from schemas.card import CardTokenResponse, InputCardToken
from services.card import CardService
from setting import Tags, api_settings, base_url, is_local, logger, stage_name

logger.name = __name__

router = APIRouter()


@router.post(
    "/create_user/",
    response_model=AdminOut,
    tags=[Tags.admin]
)
async def crete_login_user(
    request: Request,  # noqa: U100
    generate_admin: GenerateAdmin,
    db: AsyncSession = Depends(get_db)
):
    if generate_admin.token == api_settings.ADMIN_TOKEN:
        admin = await create_admin(db=db, generate_admin=generate_admin)

        return AdminOut(id=admin.id, username=admin.username)
    return {"error": "error"}


@router.get(
    "/login/",
    response_class=HTMLResponse,
    tags=[Tags.admin]
)
async def get_login_disp(
    request: Request,
    csrf_protect: CsrfProtect = Depends()
):
    csrf_token, signed_token = csrf_protect.generate_csrf_tokens()
    context = {
        "request": request,
        "csrf_token": csrf_token,
        "stage_name": stage_name,
        "base_url": base_url
    }
    response = templates.TemplateResponse(
        "login.html",
        context
    )
    csrf_protect.set_csrf_cookie(signed_token, response)
    return response


@router.post(
    "/login/",
    response_model=Token,
    tags=[Tags.admin]
)
async def post_login(
    request: Request,
    login_admin: LoginAdmin,
    csrf_protect: CsrfProtect = Depends(),
    db: AsyncSession = Depends(get_db)
):
    await csrf_protect.validate_csrf(request)
    jwt_authenticator, admin = await JwtAuthenticator.authenticate_admin(
        db=db,
        username=login_admin.username,
        password=login_admin.password
    )
    access_token = jwt_authenticator.create_access_token(
        admin
    )
    return Token(access_token=access_token, token_type="bearer")


@router.get(
    "/scores/",
    response_class=HTMLResponse,
    tags=[Tags.admin]
)
async def get_scores(
    request: Request,
    db: AsyncSession = Depends(get_db),
    csrf_protect: CsrfProtect = Depends(),
    current_admin: Admin = Depends(get_current_active_admin)  # noqa: U100
):
    csrf_token, signed_token = csrf_protect.generate_csrf_tokens()
    cards = await reads_card(db=db)
    rallyconfiguration = await get_one_rc(db=db)

    for card in cards:
        for stamp in card.stamps:
            if stamp.place and stamp.place.is_base:
                card.time = stamp.created_at
                break
        if hasattr(card, "time"):
            tardiness_penalty = CardService.calculate_tardiness_penalty(
                rallyconfiguration.end_time,
                getattr(card, "time", 0)
            )
            card.time_app = f'{card.time.strftime("%H:%M:%S")}({tardiness_penalty:4d})'
            card.score_added = card.score - tardiness_penalty
        else:
            card.score_added = card.score
            card.time_app = "-"

    sorted_cards = sorted(
        cards,
        key=lambda x: (x.time_app != "-", x.score_added),
        reverse=True
    )

    response = templates.TemplateResponse(
        "score_table.html",
        {
            "request": request,
            "cards": sorted_cards,
            "csrf_token": csrf_token,
            "liff_id": rallyconfiguration.liff_id,
            "end_time": rallyconfiguration.end_time.strftime("%H:%M")
        }
    )
    csrf_protect.set_csrf_cookie(signed_token, response)
    return response
