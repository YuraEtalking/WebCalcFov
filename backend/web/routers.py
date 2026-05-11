from sqlalchemy.ext.asyncio import AsyncSession

from loguru import logger

from fastapi import APIRouter, Form, Request, Depends
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates

from backend.core.db import get_async_session
from backend.crud.camera import get_active_cameras, get_camera_with_sensor
from backend.crud.lens import get_active_lenses, get_lens_with_teleconverters
from backend.services.calc_fov import calc


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
        tcs: list | None = None,
        selected_tc: float | None = None,
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
            'tcs': tcs,
            'selected_tc': selected_tc,
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
        distance: int = Form(...),
        focal: float | None = Form(None),
        tc: str | None = Form(None),
        session: AsyncSession = Depends(get_async_session)
):

    if distance <= 0:
        return await render_form(
            request=request,
            session=session,
            message_type='error',
            message='Расстояние должно быть больше нуля',
        )

    lens = await get_lens_with_teleconverters(lens_id, session)
    if not lens:
        return await render_form(
            request=request,
            session=session,
            message_type='error',
            message='Объектив не выбран',
        )

    camera = await get_camera_with_sensor(camera_id, session)
    if not camera:
        return await render_form(
            request=request,
            session=session,
            message_type='error',
            message='Камера не выбрана',
        )

    if focal is None:
        focal = lens.focal_max

    if tc in (None, ''):
        selected_tc = None
    else:
        selected_tc = float(tc)
    tcs = [{'multiplier': item.multiplier} for item in lens.teleconverters]

    result = calc(
        sensor=camera.sensor,
        focal=focal,
        distance=distance,
        selected_tc=selected_tc
    )

    data = {
        'camera': camera,
        'lens': lens,
        'sensor': camera.sensor,
        'distance': distance,
    }

    return await render_form(
        request=request,
        session=session,
        data=data,
        result=result,
        focal=focal,
        selected_tc=selected_tc,
        tcs=tcs,
        message='Расчёт выполнен',
        message_type='success',
    )


@web_router.get('/lens/focal-field', response_class=HTMLResponse)
async def get_focal_field(
        request: Request,
        lens_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    lens = await get_lens_with_teleconverters(lens_id, session)

    if not lens:
        return HTMLResponse('')

    tc_multiplier = []
    if lens.teleconverters:
        for tc in lens.teleconverters:
            tc_multiplier.append({'multiplier': tc.multiplier})

    return templates.TemplateResponse(
        'partials/focal_field.html',
        {
            'request': request,
            'lens': lens,
            'focal': lens.focal_max,
            'tcs': tc_multiplier,
        }
    )

