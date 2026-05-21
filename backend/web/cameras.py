from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.db import get_async_session
from backend.crud.camera import get_active_cameras, get_active_camera_with_sensor
from backend.crud.lens import get_active_lenses

web_router = APIRouter(
    prefix='/cameras',
    tags=['Cameras'],
)
templates = Jinja2Templates(directory='templates')


@web_router.get('/', name='cameras_list', response_class=HTMLResponse)
async def camera_list(
        request: Request,
        session: AsyncSession = Depends(get_async_session)
):
    cameras = await get_active_cameras(session)
    lenses = await get_active_lenses(session) # todo потом вынесу отдельно
    return templates.TemplateResponse('camera_list.html', {
        'request': request,
        'cameras': cameras,
        'lenses': lenses
    })


@web_router.get('/{camera_id}', name='camera_detail', response_class=HTMLResponse)
async def camera_detail(
        request: Request,
        camera_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    camera = await get_active_camera_with_sensor(camera_id, session)
    return templates.TemplateResponse('camera_detail.html', {
        'request': request,
        'camera': camera
    })
