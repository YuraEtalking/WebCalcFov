from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger
from backend.core.db import get_async_session
from backend.crud.camera import get_active_cameras, get_active_camera_with_sensor
from backend.web.templates import render

web_router = APIRouter(
    prefix='/cameras',
    tags=['Cameras'],
)
templates = Jinja2Templates(directory='templates')


@web_router.get('/', name='cameras_list', response_class=HTMLResponse)
async def camera_list(
        request: Request,
        slug: str,
        session: AsyncSession = Depends(get_async_session)
):
    cameras = await get_active_cameras(session, slug)

    return render(
        request,
        'camera_list.html',
        {'cameras': cameras, 'slug': slug, }
    )


@web_router.get('/{camera_id}', name='camera_detail', response_class=HTMLResponse)
async def camera_detail(
        request: Request,
        camera_id: int,
        slug: str,
        session: AsyncSession = Depends(get_async_session)
):
    logger.debug('camera_id="{}"', camera_id)
    camera = await get_active_camera_with_sensor(camera_id, session)

    return render(
        request,
        'camera_detail.html',
        {'camera': camera, 'slug': slug, }
    )
