from fastapi import APIRouter, Request, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from backend.core.db import get_async_session
from backend.web.templates import render
from backend.crud.camera import get_cameras_for_compare
from backend.services.compare_service import (
    get_ids,
    add_to_compare,
    remove_from_comparison_list,
    clear_list_of_comparison,
)
from backend.web.constants import COMPARE_CAMERAS_COOKIE


web_router = APIRouter(
    tags=['Compare'],
)


@web_router.post(
    '/camera/add/{camera_id}',
    name='add_camera_to_compare',
)
async def add_camera_to_compare(request: Request, camera_id: int):
    """Добавляет камеру в список сравнений."""
    return add_to_compare(
        request=request,
        obj_id=camera_id,
        compare_list=COMPARE_CAMERAS_COOKIE,
    )


@web_router.get('/cameras', name='compare_cameras',)
async def compare_cameras(
        request: Request,
        session: AsyncSession = Depends(get_async_session)
):
    """Представление сравнений камера."""
    ids = get_ids(request, COMPARE_CAMERAS_COOKIE)
    logger.debug('Было: ids="{}"', ids)

    cameras = await get_cameras_for_compare(ids, session)
    return render(
        request,
        'gear/compare/camera_comparison.html',
        cameras=cameras,
    )


@web_router.post(
    '/camera/remove/{camera_id}',
    name='remove_camera_from_comparison_list',
)
async def remove_camera_from_comparison_list(request: Request, camera_id: int):
    """Удаляет камеру из списка сравнений."""
    return remove_from_comparison_list(
        request=request,
        obj_id=camera_id,
        compare_list=COMPARE_CAMERAS_COOKIE,
    )


@web_router.post(
    '/camera/clear/',
    name='clear_list_of_cameras_for_comparison',
)
async def clear_list_of_cameras_for_comparison(request: Request):
    """Чистит список сравнений."""
    return clear_list_of_comparison(request, COMPARE_CAMERAS_COOKIE)
