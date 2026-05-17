from pydantic import ValidationError as PydanticValidationError

from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.db import get_async_session
from backend.core.constants import ERROR_LOAD_IN_DB
from backend.crud.camera import get_active_cameras, get_active_camera_with_sensor
from backend.crud.lens import get_active_lenses
from backend.schemas.fov import FovCalcInput
from backend.services.fov_service import (
    prepare_fov_response_data,
    EntityNotFoundError,
    FovServiceError,
    InvalidFovInputError,
)

web_router = APIRouter(
    prefix='/cameras',
    tags=['Cameras'],
)
templates = Jinja2Templates(directory='templates')


@web_router.get('/', name='cameras_list', response_class=HTMLResponse)
async def wiki_cameras(
        request: Request,
        session: AsyncSession = Depends(get_async_session)
):
    cameras = await get_active_cameras(session)
    return templates.TemplateResponse('wiki_cameras.html', {
        'request': request,
        'cameras': cameras
    })


@web_router.get('/{camera_id}', name='camera_detail', response_class=HTMLResponse)
async def wiki_camera_detail(
        request: Request,
        camera_id: int,
        session: AsyncSession = Depends(get_async_session)
):
    camera = await get_active_camera_with_sensor(camera_id, session)
    return templates.TemplateResponse('camera_detail.html', {
        'request': request,
        'camera': camera
    })