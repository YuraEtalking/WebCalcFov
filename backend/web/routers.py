from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession


from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from backend.core.db import get_async_session
from backend.crud.camera import get_active_cameras
from backend.crud.lens import get_active_lenses
from backend.schemas.fov import FovCalcInput
from backend.services.fov_service import (
    prepare_fov_response_data,
    get_lens_data,
    EntityNotFoundError,
    ValidationError,
)


web_router = APIRouter()
templates = Jinja2Templates(directory='templates')


async def render_form(
        request: Request,
        session: AsyncSession,
        data: dict | None = None,
        message: str | None = None,
        message_type: str | None = None,
        result: dict | None = None,
        focal: int | float | None = None,
        teleconverters: list | None = None,
        teleconverter_id: str | None = None,
):
    """Рендер формы с данными."""
    cameras = await get_active_cameras(session)
    lenses = await get_active_lenses(session)

    return templates.TemplateResponse(
        'form.html',
        {
            'data': data,
            'result': result,
            'request': request,
            'cameras': cameras,
            'lenses': lenses,
            'focal': focal,
            'teleconverters': teleconverters,
            'teleconverter_id': teleconverter_id,
            'message': message,
            'message_type': message_type,
    })



@web_router.get('/', response_class=HTMLResponse)
async def show_form(
        request: Request,
        session: AsyncSession = Depends(get_async_session)
):
    return await render_form(request=request, session=session)


@web_router.post('/', response_class=HTMLResponse)
async def submit_form(
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
            distance=distance,
            focal=focal,
            teleconverter_id=teleconverter_id

        )
    except ValidationError as e:
        return await render_form(
            request=request,
            session=session,
            message_type='error',
            message=str(e.errors()[0]['msg']),
        )

    try:
        payload = await prepare_fov_response_data(input_data, session)
    except ValidationError as e:
        return await render_form(
            request=request,
            session=session,
            message_type='error',
            message=str(e),
        )

    except EntityNotFoundError as e:
        return await render_form(
            request=request,
            session=session,
            message_type='error',
            message=str(e),
        )

    return await render_form(request=request, session=session, **payload)


@web_router.get('/lens/focal-field', response_class=HTMLResponse)
async def get_focal_field(
        request: Request,
        lens_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Предоставляет поле с телеконверторами."""
    try:
        data = await get_lens_data(lens_id, session)
    except Exception:
        return HTMLResponse('')

    return templates.TemplateResponse(
        'partials/focal_field.html',
        {'request': request, **data},
    )

