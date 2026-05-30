from fastapi import APIRouter, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.ext.asyncio import AsyncSession

from backend.core.db import get_async_session
from backend.services.fov_service import get_lens_data, EntityNotFoundError
from backend.crud.camera import get_active_camera_with_sensor

web_router = APIRouter(
    prefix='/partials',
    tags=['Partials'],
)
templates = Jinja2Templates(directory='templates')


@web_router.get('/lens/focal-field', response_class=HTMLResponse)
async def get_focal_field(
        request: Request,
        lens_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    """Предоставляет поле с телеконверторами."""
    try:
        data = await get_lens_data(lens_id, session)

    except EntityNotFoundError:
        return HTMLResponse('')
    except SQLAlchemyError:
        return HTMLResponse('', status_code=500)

    return templates.TemplateResponse(
        'partials/focal_field.html',
        {'request': request, **data},
    )



@web_router.get('/lens/choice_lens_field', response_class=HTMLResponse)
async def get_choice_lens_field(
        request: Request,
        camera_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    try:
        camera = await get_active_camera_with_sensor(camera_id, session)

    except EntityNotFoundError:
        return HTMLResponse('')
    except SQLAlchemyError:
        return HTMLResponse('', status_code=500)

    return templates.TemplateResponse(
        'partials/choice_lens_field.html',
        {'request': request, 'lens_list': camera.compatible_lenses},
    )
