from http import HTTPStatus

from fastapi import APIRouter, Request, Depends
from fastapi.responses import Response
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from backend.core.db import get_async_session
from backend.web.templates import render
from backend.crud.lens import get_lenses_for_compare
from backend.crud.camera import get_cameras_for_compare
from backend.services.compare_service import get_ids
from backend.web.templates import set_default_cookie
from backend.web.constants import COMPARE_LENSES_COOKIE, COMPARE_CAMERAS_COOKIE



web_router = APIRouter(
    tags=['Compare'],
)



@web_router.get(
    '/comparison_lists',
    name='comparison_lists',
)
async def comparison_lists(request: Request, session: AsyncSession = Depends(get_async_session)):
    """."""
    lens_ids = get_ids(request, COMPARE_LENSES_COOKIE)
    camera_ids = get_ids(request, COMPARE_CAMERAS_COOKIE)
    logger.debug('lens_ids: lens_ids="{}"', lens_ids)
    lenses_list = await get_lenses_for_compare(lens_ids, session)
    cameras_list = await get_cameras_for_compare(camera_ids, session)
    return render(request, 'gear/compare/comparison_lists.html', {
        'lenses_list': lenses_list,
        'cameras_list': cameras_list,
    })