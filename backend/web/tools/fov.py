from pydantic import ValidationError as PydanticValidationError

from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import HTMLResponse
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession
from loguru import logger

from backend.core.db import get_async_session
from backend.core.constants.message_constants import ERROR_LOAD_IN_DB
from backend.web.templates import render
from backend.crud.camera import get_active_cameras
from backend.schemas.fov import FovCalcInput
from backend.services.fov_service import (
    prepare_fov_response_data,
    EntityNotFoundError,
    FovServiceError,
    InvalidFovInputError,
)


web_router = APIRouter(tags=['FOV'])

TEMPLATE = 'tools/calculator_fov.html'

# todo
async def render_form(request: Request, session: AsyncSession, **context):
    """Рендер формы с данными."""
    try:
        cameras = await get_active_cameras(session)
    except SQLAlchemyError:
        cameras = []
        message = ERROR_LOAD_IN_DB
        message_type = 'error'

    return render(request=request, template_name=TEMPLATE, cameras=cameras, **context)


@web_router.get('/fov', name='fov', response_class=HTMLResponse)
async def show_form(
        request: Request,
        session: AsyncSession = Depends(get_async_session)
):
    return await render_form(request=request, session=session, data=None, result=None)


@web_router.post('/fov', name='fov_submit', response_class=HTMLResponse)
async def fov_submit(
        request: Request,
        camera_id: int = Form(...),
        lens_id: int = Form(...),
        distance: str = Form(...),
        focal: float | None = Form(None),
        teleconverter_id: str | None = Form(None),
        session: AsyncSession = Depends(get_async_session)
):
    """Представление форм расчета Field of View."""
    try:
        input_data = FovCalcInput(
            camera_id=camera_id,
            lens_id=lens_id,
            distance=distance, # Может прийти пустая строка.
            focal=focal,
            teleconverter_id=teleconverter_id

        )
    except PydanticValidationError as e:
        return await render_form(
            request=request,
            session=session,
            message_type='error',
            message=str(e.errors()[0]['msg']),
        )

    try:
        data = await prepare_fov_response_data(input_data, session)
        logger.debug('data: data="{}"', data)
    except (
            InvalidFovInputError,
            EntityNotFoundError,
            FovServiceError,
            SQLAlchemyError
    ) as e:
        return await render_form(
            request=request,
            session=session,
            message_type='error',
            message=str(e),
        )
    return await render_form(request=request, session=session, data=data, result=data.result)
