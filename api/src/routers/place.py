import json
from typing import List

from fastapi import APIRouter, Depends, HTTPException, Request
from fastapi.responses import HTMLResponse, JSONResponse
from sqlalchemy.ext.asyncio import AsyncSession

from crud.place import creates as create_places
from crud.place import reads as reads_place
from crud.rallyconfigration import get_one
from database.db import get_db
from dependencies import CsrfProtect, templates
from dependencies.jwt import get_current_active_admin
from models import Admin
from schemas.place import PlaceOutput, PlacesInput
from setting import Tags, logger

logger.name = __name__

router = APIRouter()


@router.get(
    "/",
    response_class=HTMLResponse,
    tags=[Tags.admin]
)
async def get_places(
    request: Request,
    db: AsyncSession = Depends(get_db),
    csrf_protect: CsrfProtect = Depends(),
    current_admin: Admin = Depends(get_current_active_admin)
):
    csrf_token, signed_token = csrf_protect.generate_csrf_tokens()
    places = await reads_place(db=db)
    rally_configuration = await get_one(db=db, is_active=True)
    response = templates.TemplateResponse(
        "place_table.html",
        {
            "request": request,
            "places": places,
            "liff_id": rally_configuration.liff_id,
        }
    )
    csrf_protect.set_csrf_cookie(signed_token, response)
    return response

@router.post(
    "/",
    response_model=List[PlaceOutput],
    tags=[Tags.admin]
)
async def post_places(
    request: Request,
    places_input: PlacesInput,
    db: AsyncSession = Depends(get_db),
    csrf_protect: CsrfProtect = Depends(),
    # current_admin: Admin = Depends(get_current_active_admin)
):
    """
    get all place
    """

    places = await create_places(db=db, places=places_input)
    return places
