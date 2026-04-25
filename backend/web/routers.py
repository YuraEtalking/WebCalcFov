from typing import Optional

from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from backend.core.db import get_async_session
from backend.models import Camera, Lens, Sensor
from backend.services.calc_fov import calc


web_router = APIRouter()
templates = Jinja2Templates(directory='templates')


async def get_obj_from_db(model, obj_id, session: AsyncSession):
    """Получаем объект."""
    stmt = await session.execute(select(
        model
    ).where(model.id == obj_id))
    result = stmt.scalars().first()
    return result


async def get_list_obj_from_db(model, session: AsyncSession):
    """Получаем список объектов."""
    stmt = await session.execute(select(
        model
    ).where(model.is_active.is_(True)))
    result = stmt.scalars().all()
    return result


async def render_form(
        request: Request,
        session: AsyncSession,
        data: dict | None = None,
        message: str | None = None,
        result: dict | None = None,
):
    """Рендер формы с данными."""
    cameras = await get_list_obj_from_db(Camera, session)
    lenses = await get_list_obj_from_db(Lens, session)
    sensors = await get_list_obj_from_db(Sensor, session)

    return templates.TemplateResponse(
        'form.html',
        {
            'data': data,
            'result': result,
            'request': request,
            'cameras': cameras,
            'lenses': lenses,
            'sensors': sensors,
            'message': message,
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
        sensor_id: int = Form(...),
        distance: int = Form(...),
        session: AsyncSession = Depends(get_async_session)
):

    sensor = await get_obj_from_db(Sensor, sensor_id, session)
    lens = await get_obj_from_db(Lens, lens_id, session)
    camera = await get_obj_from_db(Camera, camera_id, session)

    result = calc(sensor, lens, distance)

    data = {
        'camera': camera,
        'lens': lens,
        'sensor': sensor,
        'distance': distance,
    }

    return await render_form(
        request=request,
        session=session,
        data=data,
        result=result,
        message='Форма отправлена'
    )